"""Lets Home Assistant accept requests through Caddy: X-Forwarded-For from the
proxies given as arguments (the host's Docker networks), on every start.

Home Assistant keeps its HTTP settings in .storage/http and reads http: from
configuration.yaml only once (since 2026.x, and that copy is a trial that
reverts after five minutes unless confirmed in the UI), so the setting is
written there, before Home Assistant starts. Proxies you added stay; other
settings are left alone."""

import json
import os
import sys
from datetime import datetime, timezone

from homeassistant.components.http.config import HTTP_STORAGE_SCHEMA, STORAGE_MINOR_VERSION, STORAGE_VERSION

PATH = "/config/.storage/http"


def log(msg):
    print(f"nepfleet http: {msg}", flush=True)


def with_proxies(conf, proxies):
    """conf trusting proxies, or None when it does already."""
    have = conf.get("trusted_proxies") or []
    want = have + [p for p in proxies if p not in have]
    if conf.get("use_x_forwarded_for") is True and want == have:
        return None
    return {**conf, "use_x_forwarded_for": True, "trusted_proxies": want}


def main():
    proxies = [str(p) for p in HTTP_STORAGE_SCHEMA({"trusted_proxies": sys.argv[1:]})["trusted_proxies"]]
    if os.path.exists(PATH):
        with open(PATH, encoding="utf-8") as f:
            raw = json.load(f)
        if raw.get("version") != STORAGE_VERSION:
            # Home Assistant migrates it on this start; the next start sets it.
            log(f".storage/http is version {raw.get('version')}, not {STORAGE_VERSION}: unchanged on this start")
            return
        data = raw["data"]
        changed = False
        for slot in ("stable", "pending"):
            if data.get(slot) is not None and (new := with_proxies(data[slot], proxies)) is not None:
                data[slot] = new
                changed = True
        if not changed:
            return
    else:
        stable = dict(HTTP_STORAGE_SCHEMA({"use_x_forwarded_for": True, "trusted_proxies": proxies}))
        stable.update(created_at=datetime.now(timezone.utc).isoformat(), error=None, error_message=None)
        # No http: in configuration.yaml to migrate any more.
        data = {"stable": stable, "pending": None, "yaml_migration_done": True}
        raw = {"version": STORAGE_VERSION, "minor_version": STORAGE_MINOR_VERSION, "key": "http"}
    raw["data"] = data
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    tmp = PATH + ".nepfleet"
    with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)
    os.replace(tmp, PATH)
    # The subnets as given (the same as validated above), not the schema's output.
    log("trusts X-Forwarded-For from " + ", ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
