#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check template images against their registries. Standard library only.

  images.py tags <image>       list tags of an image
  images.py check [--strict]   verify every pinned tag exists, report newer
                               releases beyond each image's `track`; writes
                               JSON to stdout. --strict fails on missing tags.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "nepfleet-templates-image-check"
ACCEPT = ", ".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])
_tokens = {}


def parse_ref(ref):
    name, _, digest = ref.partition("@")
    last = name.rsplit("/", 1)[-1]
    tag = None
    if ":" in last:
        name, tag = name.rsplit(":", 1)
    first = name.split("/", 1)[0]
    if "/" in name and ("." in first or ":" in first or first == "localhost"):
        registry, repo = name.split("/", 1)
    else:
        registry, repo = "registry-1.docker.io", name
        if "/" not in repo:
            repo = "library/" + repo
    return registry, repo, tag, digest or None


def _request(url, registry, repo, method="GET"):
    headers = {"User-Agent": UA, "Accept": ACCEPT}
    key = (registry, repo)
    if key in _tokens:
        headers["Authorization"] = "Bearer " + _tokens[key]
    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        return urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        if e.code != 401 or key in _tokens:
            raise
        challenge = e.headers.get("WWW-Authenticate", "")
        params = dict(re.findall(r'(\w+)="([^"]*)"', challenge))
        if "realm" not in params:
            raise
        q = {"service": params.get("service", ""), "scope": f"repository:{repo}:pull"}
        treq = urllib.request.Request(params["realm"] + "?" + urllib.parse.urlencode(q), headers={"User-Agent": UA})
        with urllib.request.urlopen(treq, timeout=30) as r:
            body = json.load(r)
        _tokens[key] = body.get("token") or body.get("access_token")
        return _request(url, registry, repo, method)


def list_tags(image):
    registry, repo, _, _ = parse_ref(image)
    url = f"https://{registry}/v2/{repo}/tags/list?n=1000"
    tags = []
    while url:
        with _request(url, registry, repo) as r:
            tags += json.load(r).get("tags") or []
            link = r.headers.get("Link", "")
        m = re.search(r"<([^>]+)>", link)
        url = urllib.parse.urljoin(f"https://{registry}", m.group(1)) if m else None
    return tags


def exists(ref):
    registry, repo, tag, digest = parse_ref(ref)
    url = f"https://{registry}/v2/{repo}/manifests/{digest or tag}"
    try:
        with _request(url, registry, repo, method="HEAD"):
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


VERSION = re.compile(r"^(?P<prefix>[^\d]*)(?P<num>\d+(?:\.\d+)*)(?P<suffix>.*)$")


def version_of(tag, prefix, suffix):
    m = VERSION.match(tag)
    if not m or m["prefix"] != prefix or m["suffix"] != suffix:
        return None
    return tuple(int(x) for x in m["num"].split("."))


def beyond_track(current, candidate, track):
    """True if candidate is newer than what `track` lets NepFleet apply alone."""
    width = {"major": 0, "minor": 1, "patch": 2}[track]
    if width == 0:
        return False
    return candidate[:width] > current[:width]


# Images from our own product repos that may not be published yet.
OWN_PRODUCTS = {"serraniel/neptide", "serraniel/nepfleet", "serraniel/nepfleet-ui"}


def built_here(ref):
    """Images under images/<name>/ (published as ghcr.io/<owner>/nepfleet-<name>)
    or by one of our product repos; checked by their own release pipelines."""
    registry, repo, _, _ = parse_ref(ref)
    owner, _, name = repo.partition("/")
    if registry == "ghcr.io" and repo in OWN_PRODUCTS:
        return True
    return name.startswith("nepfleet-") and (ROOT / "images" / name.removeprefix("nepfleet-")).is_dir()


def templates():
    for path in sorted(ROOT.glob("*/*/template.yaml")):
        yield path.parent, path.read_text()


def images_of(tdir, text):
    """(ref, track) for each image in the compose file. Tags live only there;
    template.yaml maps image names to a track. No YAML library needed."""
    tracks = dict(re.findall(r"-\s*name:\s*(\S+)\s*\n\s*track:\s*(\w+)", text))
    compose = (tdir / "compose.yaml").read_text()
    out = []
    for ref in sorted(set(re.findall(r"^\s*image:\s*[\"']?([^\s\"']+)", compose, re.M))):
        name = ref.split("@")[0]
        if name.rfind(":") > name.rfind("/"):
            name = name[: name.rfind(":")]
        out.append((ref, tracks.get(name, "patch")))
    return out


def check(strict):
    report, missing = [], []
    for tdir, text in templates():
        for ref, track in images_of(tdir, text):
            entry = {"template": str(tdir.relative_to(ROOT)), "ref": ref, "track": track}
            if built_here(ref):
                entry["builtHere"] = True  # published by this repo's images workflow
                report.append(entry)
                continue
            try:
                if not exists(ref):
                    missing.append(ref)
                    entry["error"] = "tag not found"
                    report.append(entry)
                    continue
                _, _, tag, _ = parse_ref(ref)
                m = VERSION.match(tag or "")
                if m:
                    cur = tuple(int(x) for x in m["num"].split("."))
                    # Fewer components than the pinned tag means another scheme
                    # (e.g. Jellyfin's 2026110213 date tags next to 10.11.11).
                    newer = [v for t in list_tags(ref)
                             if (v := version_of(t, m["prefix"], m["suffix"])) and len(v) >= len(cur)]
                    if newer:
                        latest = max(newer)
                        entry["latest"] = m["prefix"] + ".".join(map(str, latest)) + m["suffix"]
                        entry["beyondTrack"] = beyond_track(cur, latest, track)
            except Exception as e:  # report, keep going
                entry["error"] = f"{type(e).__name__}: {e}"
            report.append(entry)
    json.dump(report, sys.stdout, indent=2)
    print()
    if strict and missing:
        print(f"missing tags: {', '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "tags":
        print("\n".join(list_tags(sys.argv[2])))
    elif len(sys.argv) >= 2 and sys.argv[1] == "check":
        sys.exit(check("--strict" in sys.argv))
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
