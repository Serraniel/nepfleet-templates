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
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = json.loads((ROOT / "scripts" / "test-values.json").read_text())


def run(*args, cwd=None, env=None, check=True, capture=True):
    p = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=capture)
    if check and p.returncode != 0:
        raise SystemExit(f"$ {' '.join(map(str, args))}\n{p.stdout}{p.stderr}")
    return p


def catalogue(nf):
    return json.loads(run(nf, "template", "index", ROOT).stdout)["templates"]


def value(tpl, inp, workdir):
    name, typ = inp["name"], inp.get("type", "string")
    over = OVERRIDES.get(tpl["name"], {})
    if name in over:
        return over[name].replace("{workdir}", str(workdir))
    if inp.get("default") and typ != "secret":
        return inp["default"]
    v = {
        "hostname": f"{tpl['name']}.example.test",
        "url": f"https://{tpl['name']}.example.test",
        "email": "ci@example.test",
        "int": "1",
        "bool": "false",
        "secret": "ci-" + secrets.token_hex(16),
        "path": str(workdir / "paths" / tpl["name"] / name.lower()),
    }.get(typ)
    if typ == "enum":
        v = inp["options"][0]
    if v is None:
        v = "ci"
    if typ == "path":
        Path(v).mkdir(parents=True, exist_ok=True)
    if inp.get("pattern") and not re.fullmatch(inp["pattern"], v):
        raise SystemExit(f"{tpl['name']}: no test value for {name} matches {inp['pattern']}; add one to scripts/test-values.json")
    return v


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
        y = y.replace("      url: https://github.com/Serraniel/nepfleet-templates\n", f"      path: {ROOT}\n")
        y = y.replace("      ref: main\n", "").replace("    age: []", f'    age: ["{pub}"]')
        y = y.replace("spec:\n", "spec:\n  ingressNetwork: nepfleet_templates_it\n", 1)
        (self.fleet / "fleet.yaml").write_text(y)

    def nepfleet(self, cmd, *args, check=True):
        return run(self.nf, cmd, "--fleet", self.fleet, "--state", self.dir / "state", "--host", "it", *args,
                   cwd=self.fleet, env=self.env, check=check)

    def new(self, tpl, mode="compose"):
        """Creates stack it-<template>: never a name a real project may have."""
        sets = []
        for inp in tpl["inputs"]:
            sets += ["--set", f"{inp['name']}={value(tpl, inp, self.dir)}"]
        run(self.nf, "new", tpl["name"], stack_name(tpl["name"]), *sets, cwd=self.fleet, env=self.env)
        stack = self.fleet / ("system" if tpl["tier"] == "system" else "stacks") / stack_name(tpl["name"]) / "stack.yaml"
        s = stack.read_text().replace("target: local", "target: it")
        if mode == "swarm":
            s = s.replace("spec:\n", "spec:\n    mode: swarm\n", 1)  # yaml.v3 indents by 4
        stack.write_text(s)

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)


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
                    env[k] = v.strip("'\"")
            p = run("docker", "stack", "config", "--compose-file", work / "compose.yaml", cwd=work, env=env, check=False)
            print(("ok   " if p.returncode == 0 else "FAIL ") + tpl["path"])
            if p.returncode != 0:
                print(p.stderr.strip())
                failed.append(tpl["name"])
        finally:
            fleet.cleanup()
    if failed:
        raise SystemExit(f"{len(failed)} swarm template(s) invalid: {', '.join(failed)}")


def deploy(nf, names):
    tpls = {t["name"]: t for t in catalogue(nf)}
    failed = []
    for name in names:
        fleet = Fleet(nf)
        try:
            fleet.new(tpls[name])
            p = fleet.nepfleet("apply", "--yes", "--wait", "5m", stack_name(name), check=False)
            print(p.stdout + p.stderr)
            print(("ok   " if p.returncode == 0 else "FAIL ") + name)
            if p.returncode != 0:
                failed.append(name)
        finally:
            # Only this test's own project: it-<template>, created above.
            run("docker", "compose", "--project-name", stack_name(name), "down", "--volumes", "--remove-orphans", check=False)
            run("docker", "network", "rm", "nepfleet_templates_it", check=False)
            fleet.cleanup()
    if failed:
        raise SystemExit(f"{len(failed)} template(s) did not become healthy: {', '.join(failed)}")


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
