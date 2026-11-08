#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Installs templates the way a user does, with test values.

  test-templates.py swarm  <nepfleet>             docker stack config for every swarm template
  test-templates.py deploy <nepfleet> NAME...     nepfleet apply (health-gated), then tear down
  test-templates.py list   [--deploy]             template names (for a CI matrix)

Needs docker, git, sops and age-keygen on PATH. Values come from each
input's default, else from its type; scripts/test-values.json overrides
them per template where a type alone is not enough.
"""
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NETWORK = "nepfleet_templates_it"  # never a real install's ingress network
ALPINE = "alpine:3.24@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a"
OVERRIDES = json.loads((ROOT / "scripts" / "test-values.json").read_text())
# Templates deployed behind Anubis, each with a path its spec.botCheck.allow lets through.
BOT_CHECK = OVERRIDES.get("_bot_check", {})


def run(*args, cwd=None, env=None, check=True, capture=True):
    p = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=capture)
    if check and p.returncode != 0:
        raise SystemExit(f"$ {' '.join(map(str, args))}\n{p.stdout}{p.stderr}")
    return p


def catalogue(nf):
    return json.loads(run(nf, "template", "index", ROOT).stdout)["templates"]


def value(tpl, inp, fleet):
    """A test value for inp, or None to leave an optional input empty."""
    name, typ = inp["name"], inp.get("type", "string")
    over = OVERRIDES.get(tpl["name"], {})
    if name in over:
        return over[name].format(**fleet.facts)
    if name in ("PUID", "PGID"):  # the runner's user owns the test's directories
        return str(fleet.facts["uid" if name == "PUID" else "gid"])
    if typ == "path":
        # Never a real host directory, even when the template defaults to one.
        v = fleet.dir / "paths" / tpl["name"] / name.lower()
        v.mkdir(parents=True, exist_ok=True)
        return str(v)
    if inp.get("default") and typ != "secret":
        return inp["default"]
    if not inp.get("required"):
        return None
    v = {
        "hostname": f"{tpl['name']}.example.test",
        "url": f"https://{tpl['name']}.example.test",
        "email": "ci@example.test",
        "int": "1",
        "bool": "false",
        "secret": "ci-" + secrets.token_hex(16),
    }.get(typ)
    if typ == "enum":
        v = inp["options"][0]
    return v if v is not None else "ci"


def replace(text, old, new):
    """str.replace that fails when nothing matched, so a changed skeleton
    cannot silently test the wrong thing."""
    if old not in text:
        raise SystemExit(f"test-templates.py: expected {old!r} in a generated file; nepfleet changed, update the script")
    return text.replace(old, new, 1)


class Fleet:
    """A throwaway fleet repository with this checkout as template source."""

    def __init__(self, nf):
        self.nf = nf
        self.dir = Path(tempfile.mkdtemp(prefix="nepfleet-templates-it."))
        key = self.dir / "age.key"
        run("age-keygen", "-o", key)
        self.env = dict(os.environ, SOPS_AGE_KEY_FILE=str(key))
        pub = run("age-keygen", "-y", key).stdout.strip()
        run(nf, "init", self.dir / "fleet")
        self.fleet = self.dir / "fleet"
        y = (self.fleet / "fleet.yaml").read_text()
        y = replace(y, "      url: https://github.com/Serraniel/nepfleet-templates\n", f"      path: {ROOT}\n")
        y = replace(y, "      ref: main\n", "")
        y = replace(y, "    age: []", f'    age: ["{pub}"]')
        y = replace(y, "spec:\n", f"spec:\n  ingressNetwork: {NETWORK}\n")
        (self.fleet / "fleet.yaml").write_text(y)
        self.facts = {"workdir": self.dir, "age_public_key": pub, "uid": os.getuid(), "gid": os.getgid(),
                      "docker_gid": docker_gid()}

    def nepfleet(self, cmd, *args, check=True):
        return run(self.nf, cmd, "--fleet", self.fleet, "--state", self.dir / "state", "--host", "it", *args,
                   cwd=self.fleet, env=self.env, check=check)

    def new(self, tpl, mode="compose"):
        """Creates stack it-<template>: never a name a real project may have."""
        sets = []
        for inp in tpl["inputs"]:
            v = value(tpl, inp, self)
            if v is not None:
                sets += ["--set", f"{inp['name']}={v}"]
        p = run(self.nf, "new", tpl["name"], stack_name(tpl["name"]), "--target", "it", *sets,
                cwd=self.fleet, env=self.env, check=False)
        if p.returncode != 0:
            raise SystemExit(f"{tpl['name']}: nepfleet new refused the test values (add one to scripts/test-values.json):\n{p.stdout}{p.stderr}")
        stack = self.fleet / ("system" if tpl["tier"] == "system" else "stacks") / stack_name(tpl["name"]) / "stack.yaml"
        if mode == "swarm":
            stack.write_text(replace(stack.read_text(), "\nspec:\n", "\nspec:\n    mode: swarm\n"))  # yaml.v3 indents by 4
        elif tpl["name"] in BOT_CHECK:
            stack.write_text(replace(stack.read_text(), "\nspec:\n", "\nspec:\n    botCheck:\n        enabled: true\n"))

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)


def docker_gid():
    """The group of the Docker socket (rootless Docker or DOCKER_HOST: ours)."""
    try:
        return os.stat("/var/run/docker.sock").st_gid
    except OSError:
        return os.getgid()


def stack_name(template):
    return "it-" + template


def rendered(fleet, name):
    """Files of `nepfleet render`, split on its "# ---- path" headers."""
    out, files, cur = fleet.nepfleet("render", name).stdout, {}, None
    for line in out.splitlines(keepends=True):
        if line.startswith("# ---- "):
            cur = line[7:].strip()
            files[cur] = ""
        elif cur:
            files[cur] += line
    return files


def swarm(nf):
    failed = []
    for tpl in catalogue(nf):
        if not tpl["supports"].get("swarm"):
            continue
        fleet = Fleet(nf)
        try:
            fleet.new(tpl, mode="swarm")
            files = rendered(fleet, stack_name(tpl["name"]))
            work = fleet.dir / "render"
            work.mkdir()
            for path, content in files.items():
                (work / path).parent.mkdir(parents=True, exist_ok=True)
                (work / path).write_text(content)
            # docker stack deploy does not read .env; nepfleet interpolates
            # it first, so pass it as the environment here.
            env = dict(os.environ)
            for line in files.get(".env", "").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    if len(v) >= 2 and v[0] == v[-1] == "'":  # nepfleet writes KEY='value'
                        v = v[1:-1]
                    env[k] = v
            p = run("docker", "stack", "config", "--compose-file", work / "compose.yaml", cwd=work, env=env, check=False)
            ok = p.returncode == 0 and "is not set" not in p.stderr  # a missing variable only warns
            print(("ok   " if ok else "FAIL ") + tpl["path"])
            if not ok:
                print(p.stderr.strip())
                failed.append(tpl["name"])
        finally:
            fleet.cleanup()
    if failed:
        raise SystemExit(f"{len(failed)} swarm template(s) invalid: {', '.join(failed)}")


def deploy(nf, names):
    if not os.environ.get("CI") and "--local" not in sys.argv:
        raise SystemExit("deploy starts real containers (some watch or update the host's other containers); run it in CI, or pass --local")
    names = [n for n in names if n != "--local"]
    tpls = {t["name"]: t for t in catalogue(nf)}
    failed = []
    for name in names:
        if name in OVERRIDES.get("_ci_only", {}) and not os.environ.get("CI"):
            print(f"skip {name}: {OVERRIDES['_ci_only'][name]}")
            continue
        fleet = Fleet(nf)
        try:
            fleet.new(tpls[name])
            p = fleet.nepfleet("apply", "--yes", "--wait", "5m", stack_name(name), check=False)
            print(p.stdout + p.stderr)
            print(("ok   " if p.returncode == 0 else "FAIL ") + name)
            if p.returncode != 0:
                failed.append(name)
                # "Unhealthy" says little: the containers' own words are why.
                logs = run("docker", "compose", "-p", stack_name(name), "logs", "--no-color", "--tail", "40", check=False)
                print(logs.stdout + logs.stderr)
            else:
                try:
                    check_metrics(name)
                    check_bot_check(name)
                    if name in AFTER_DEPLOY:
                        AFTER_DEPLOY[name]()
                        print("ok   " + name + " works")
                except SystemExit as e:
                    print(e)
                    failed.append(name)
        finally:
            # Only this test's own project, by its rendered files: without
            # --file, compose would pick up a compose.yaml from the cwd.
            d = fleet.dir / "state" / "stacks" / stack_name(name)
            if (d / "compose.yaml").exists():
                run("docker", "compose", "--project-name", stack_name(name), "--project-directory", d,
                    "--file", d / "compose.yaml", "--env-file", d / ".env",
                    "down", "--volumes", "--remove-orphans", cwd=d, check=False)
            run("docker", "network", "rm", NETWORK, check=False)
            # Bind mounts may hold files containers wrote as root.
            run("docker", "run", "--rm", "-v", f"{fleet.dir}:/w", ALPINE, "rm", "-rf", "/w/paths", "/w/state", check=False)
            fleet.cleanup()
    if failed:
        raise SystemExit(f"{len(failed)} template(s) did not become healthy: {', '.join(failed)}")


def check_fail2ban():
    """A ban must really reach the host's firewall: looking active isn't enough."""
    address = "203.0.113.9"  # TEST-NET-3, nobody's
    c = stack_name("fail2ban") + "-fail2ban-1"
    run("docker", "exec", c, "fail2ban-client", "set", "sshd", "banip", address)
    rules = run("sudo", "-n", "iptables", "-S").stdout
    if "-A INPUT -p tcp" not in rules or "f2b-sshd" not in rules or address not in rules:
        raise SystemExit(f"fail2ban: the ban is not in the host's firewall:\n{rules}")
    run("docker", "exec", c, "fail2ban-client", "set", "sshd", "unbanip", address)
    if address in run("sudo", "-n", "iptables", "-S").stdout:
        raise SystemExit("fail2ban: unbanning did not remove the rule")


def check_dozzle():
    """Dozzle stays healthy with its logs refused: its proxy must let them through."""
    prefix = stack_name("dozzle")
    proxy = prefix + "-socket-proxy-1"
    run("docker", "exec", proxy, "wget", "-q", "-O", "/dev/null",
        f"http://127.0.0.1:2375/containers/{prefix}-dozzle-1/logs?stdout=1&tail=1")
    # And it stays read-only.
    stop = run("docker", "exec", proxy, "wget", "-q", "-O", "/dev/null", "--post-data=",
               f"http://127.0.0.1:2375/containers/{prefix}-dozzle-1/stop", check=False)
    if stop.returncode == 0:
        raise SystemExit("dozzle: its proxy let a container be stopped")


def check_metrics(name):
    """Every nepfleet.metrics label must lead to metrics, from the ingress network."""
    ids = run("docker", "ps", "-q", "--filter", f"label=com.docker.compose.project={stack_name(name)}",
              "--filter", "label=nepfleet.metrics.port").stdout.split()
    for cid in ids:
        fmt = ('{{index .Config.Labels "com.docker.compose.service"}} '
               '{{index .Config.Labels "nepfleet.metrics.port"}} '
               '{{index .Config.Labels "nepfleet.metrics.path"}}')
        service, port, *path = run("docker", "inspect", "--format", fmt, cid).stdout.split() + [""]
        url = f"http://{stack_name(name)}-{service}-1:{port}{path[0] or '/metrics'}"
        for _ in range(12):
            out = run("docker", "run", "--rm", "--network", NETWORK, ALPINE,
                      "wget", "-qO-", url, check=False).stdout
            if "# TYPE" in out or "# HELP" in out:
                break
            time.sleep(5)
        else:
            raise SystemExit(f"{name}: no metrics at {url}")
        print(f"ok   {name} metrics at {url}")


def check_bot_check(name):
    """Behind Anubis, a browser gets the check, and an allowed path reaches the app."""
    if name not in BOT_CHECK:
        return
    ids = run("docker", "ps", "-q", "--filter", f"label=com.docker.compose.project={stack_name(name)}").stdout.split()
    services = [run("docker", "inspect", "--format", '{{index .Config.Labels "com.docker.compose.service"}}', c).stdout.strip()
                for c in ids]
    anubis = [s for s in services if s.endswith("-anubis")]
    if not anubis:
        raise SystemExit(f"{name}: botCheck is on, but no Anubis service runs: {services}")
    base = f"http://{stack_name(name)}-{anubis[0]}-1:8923"
    marker = ".within.website/x/"  # the check page's own assets

    def get(path):
        p = run("docker", "run", "--rm", "--network", NETWORK, ALPINE, "wget", "-S", "-O", "-",
                "-U", "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
                "--header", "X-Real-Ip: 203.0.113.7", base + path, check=False)
        return p.stdout, p.stderr

    for _ in range(12):
        body, head = get("/")
        if marker in body:
            break
        time.sleep(5)
    else:
        raise SystemExit(f"{name}: a browser on / didn't get Anubis's check:\n{head}\n{body[:500]}")
    body, head = get(BOT_CHECK[name])
    if marker in body or "HTTP/1.1 502" in head or "HTTP/" not in head:
        raise SystemExit(f"{name}: {BOT_CHECK[name]} must reach the app past Anubis:\n{head}\n{body[:500]}")
    print(f"ok   {name} behind Anubis: / is checked, {BOT_CHECK[name]} passes")


def check_prometheus():
    """Ready says little: it must really scrape this host, and find services by label."""
    c = stack_name("prometheus") + "-prometheus-1"
    for _ in range(30):
        out = run("docker", "exec", c, "wget", "-qO-", "http://localhost:9090/api/v1/targets").stdout
        targets = json.loads(out)["data"]["activeTargets"]
        up = {t["labels"]["job"] for t in targets if t["health"] == "up"}
        if "node" in up and "prometheus" in up:
            break
        time.sleep(5)
    else:
        raise SystemExit(f"prometheus: not scraping this host: {out[:800]}")


# Checks beyond "healthy", for templates where that proves little.
AFTER_DEPLOY = {"fail2ban": check_fail2ban, "dozzle": check_dozzle, "prometheus": check_prometheus}


def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "list":
        skip = set(OVERRIDES.get("_skip_deploy", {}))
        names = [p.parent.name for tier in ("system", "apps") for p in sorted((ROOT / tier).glob("*/template.yaml"))]
        if "--deploy" in args:
            names = [n for n in names if n not in skip]
        print(json.dumps(names))
    elif cmd == "swarm":
        swarm(args[0])
    elif cmd == "deploy":
        deploy(args[0], args[1:])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
