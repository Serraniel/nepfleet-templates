#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Installs templates the way a user does, with test values.

  test-templates.py deploy <nepfleet> NAME...     nepfleet apply (health-gated), then tear down
  test-templates.py deploy-swarm <nepfleet> NAME...
                                                 the same as a swarm stack, on a one-node
                                                 swarm (docker swarm init when there is none)
  test-templates.py list   [--deploy] [--swarm] [--changed BASE]
                                                 template names (for a CI matrix); with
                                                 --swarm, only those that support it; with
                                                 --changed, only those touched since BASE

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
RCLONE = "rclone/rclone:1.76.0@sha256:7cbeec24a44f206067597c0368be4de90ae19a64d5113c7d1938bd737a81e466"
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
                    check_stays_up(name)
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


def supports_swarm(name):
    """Whether template NAME declares supports.swarm (read from its template.yaml)."""
    for tier in ("system", "apps"):
        f = ROOT / tier / name / "template.yaml"
        if f.exists():
            for line in f.read_text().splitlines():
                if line.strip().startswith("supports:"):
                    return "swarm: true" in line
    return False


def short_services(stack):
    """The stack's services that run fewer replicas than they want, as
    "name running/wanted". A one-shot that finished shows 0/1 with its task
    Complete: that is fine."""
    out = []
    ls = run("docker", "service", "ls", "--filter", f"label=com.docker.stack.namespace={stack}",
             "--format", "{{.Name}} {{.Replicas}}").stdout
    for line in ls.splitlines():
        if not line.strip():
            continue
        svc, replicas = line.split(" ", 1)
        running, wanted = replicas.split(" ")[0].split("/")
        if running == wanted:
            continue
        states = run("docker", "service", "ps", svc, "--format", "{{.CurrentState}}", check=False).stdout.splitlines()
        if states and states[0].startswith("Complete"):
            continue
        out.append(f"{svc} {running}/{wanted}")
    return out


def stack_gone(stack):
    """Waits until docker stack rm has removed the stack's services and containers."""
    for _ in range(90):
        services = run("docker", "service", "ls", "-q", "--filter", f"label=com.docker.stack.namespace={stack}", check=False).stdout.strip()
        containers = run("docker", "ps", "-aq", "--filter", f"label=com.docker.stack.namespace={stack}", check=False).stdout.strip()
        if not services and not containers:
            return
        time.sleep(1)


def deploy_swarm(nf, names):
    """Each template as a swarm stack, through nepfleet apply, on a one-node swarm."""
    if not os.environ.get("CI") and "--local" not in sys.argv:
        raise SystemExit("deploy-swarm starts real services and may turn swarm mode on; run it in CI, or pass --local")
    names = [n for n in names if n != "--local"]
    if run("docker", "info", "--format", "{{.Swarm.LocalNodeState}}").stdout.strip() != "active":
        run("docker", "swarm", "init", "--advertise-addr", "127.0.0.1")
    tpls = {t["name"]: t for t in catalogue(nf)}
    failed = []
    for name in names:
        fleet = Fleet(nf)
        stack = stack_name(name)
        try:
            fleet.new(tpls[name], mode="swarm")
            p = fleet.nepfleet("apply", "--yes", "--wait", "5m", stack, check=False)
            print(p.stdout + p.stderr)
            ok = p.returncode == 0
            if ok:
                short = short_services(stack)
                if short:
                    print("not all replicas run: " + "; ".join(short))
                    ok = False
                label = run("docker", "node", "ls", "--filter", f"node.label=nepfleet.data.{stack}", "-q").stdout.strip()
                print(f"data node for {stack}: {label or '(none: no local volumes)'}")
            print(("ok   " if ok else "FAIL ") + name + " (swarm)")
            if not ok:
                failed.append(name)
                ps = run("docker", "stack", "ps", stack, "--no-trunc", "--format", "{{.Name}} {{.CurrentState}} {{.Error}}", check=False)
                print(ps.stdout + ps.stderr)
        finally:
            run("docker", "stack", "rm", stack, check=False)
            stack_gone(stack)
            for v in run("docker", "volume", "ls", "-q", "--filter", f"label=com.docker.stack.namespace={stack}", check=False).stdout.split():
                run("docker", "volume", "rm", v, check=False)
            node = run("docker", "info", "--format", "{{.Swarm.NodeID}}", check=False).stdout.strip()
            if node:  # docker node update takes no "self"
                run("docker", "node", "update", "--label-rm", f"nepfleet.data.{stack}", node, check=False)
            run("docker", "network", "rm", NETWORK, check=False)
            run("docker", "run", "--rm", "-v", f"{fleet.dir}:/w", ALPINE, "rm", "-rf", "/w/paths", "/w/state", check=False)
            fleet.cleanup()
    if failed:
        raise SystemExit(f"{len(failed)} swarm template(s) did not deploy: {', '.join(failed)}")


def check_immich():
    """The setup job created the admin from the inputs: Immich offers no admin
    sign-up any more, skips its welcome steps, and the admin signs in."""
    c = stack_name("immich")
    base = "http://localhost:2283/api"
    creds = json.dumps({"email": OVERRIDES["immich"]["ADMIN_EMAIL"], "password": OVERRIDES["immich"]["ADMIN_PASSWORD"]})

    def curl(*args):
        return run("docker", "exec", f"{c}-immich-server-1", "curl", "-s", *args, check=False).stdout

    config = json.loads(curl(f"{base}/server/config") or "{}")
    if not config.get("isInitialized") or not config.get("isOnboarded"):
        raise SystemExit(f"immich: still offers its first-run setup: {config}")
    login = json.loads(curl("-X", "POST", "-H", "Content-Type: application/json", "-d", creds, f"{base}/auth/login") or "{}")
    if not login.get("accessToken") or not login.get("isAdmin") or login.get("shouldChangePassword") or not login.get("isOnboarded"):
        raise SystemExit(f"immich: the admin from the inputs doesn't sign in ready to use: {login}")
    signup = curl("-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json",
                  "-d", '{"email":"other@example.test","password":"x","name":"x"}', f"{base}/auth/admin-sign-up")
    if signup != "400":
        raise SystemExit(f"immich: admin sign-up answered {signup}, not 400")


def check_sure():
    """The worker processes jobs, the sign-up page renders for the stack's
    domain, and no usage data goes to Sure's PostHog project."""
    c = stack_name("sure")
    state = run("docker", "inspect", "--format", "{{.State.Status}} {{.RestartCount}}", f"{c}-worker-1").stdout.split()
    # A running Sidekiq registers itself in Redis (database 1, REDIS_URL).
    workers = []
    for _ in range(30):
        workers = run("docker", "exec", f"{c}-redis-1", "valkey-cli", "-n", "1", "smembers", "processes").stdout.split()
        if workers:
            break
        time.sleep(2)
    if state != ["running", "0"] or not workers:
        logs = run("docker", "logs", "--tail", "40", f"{c}-worker-1", check=False)
        raise SystemExit(f"sure: the worker isn't processing jobs ({state}):\n{logs.stdout}{logs.stderr}")
    domain = run("docker", "exec", f"{c}-web-1", "printenv", "APP_DOMAIN").stdout.strip()
    code = run("docker", "exec", f"{c}-web-1", "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
               "-H", f"Host: {domain}", "-H", "X-Forwarded-Proto: https", "http://localhost:3000/registration/new").stdout
    if code != "200":
        raise SystemExit(f"sure: the sign-up page answered {code}")
    if run("docker", "exec", f"{c}-web-1", "printenv", "POSTHOG_FEEDBACK_ENABLED").stdout.strip() != "false":
        raise SystemExit("sure: shared PostHog feedback is on")

def check_pihole():
    """Names under the home domain answer with the server's address, never upstream."""
    v = OVERRIDES["pihole"]
    c = stack_name("pihole") + "-pihole-1"
    got = run("docker", "exec", c, "dig", "+short", "@127.0.0.1", "jellyfin." + v["HOME_DOMAIN"]).stdout.split()
    if got != [v["HOME_ADDRESS"]]:
        raise SystemExit(f"pihole: jellyfin.{v['HOME_DOMAIN']} answered {got}, not {v['HOME_ADDRESS']}")

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
    # A log line with "panic" must reach "NepFleet's API" (a stand-in that
    # prints requests) in NepFleet's alert format, with the token.
    recv, emitter = prefix + "-recv", prefix + "-emitter"
    for c in (recv, emitter):
        run("docker", "rm", "-f", c, check=False)
    try:
        run("docker", "run", "-d", "--name", recv, "--network", NETWORK, ALPINE, "sh", "-c",
            r'while true; do printf "HTTP/1.1 202 Accepted\r\nContent-Length: 0\r\nConnection: close\r\n\r\n" | nc -l -p 8080; echo; done')
        run("docker", "run", "-d", "--name", emitter, ALPINE, "sh", "-c",
            # Again and again: Dozzle may start following it after the first.
            "while :; do sleep 10; echo 'panic: ci test line'; done")
        got = ""
        for _ in range(24):
            time.sleep(5)
            got = run("docker", "logs", recv, check=False).stdout
            if '"rule":"Fatal log lines"' in got:
                break
        token = OVERRIDES["dozzle"]["ALERTS_TOKEN"]
        for want in ("POST /api/v1/alerts", f"Authorization: Bearer {token}", '"source":"dozzle"',
                     f'"container":"{emitter}"', "panic: ci test line"):
            if want not in got:
                raise SystemExit(f"dozzle: the alert lacks {want!r}:\n{got[-1500:]}")
    finally:
        for c in (recv, emitter):
            run("docker", "rm", "-f", c, check=False)


def check_stays_up(name, settle=10):
    """A container without a healthcheck counts as healthy while it runs, even
    in a restart loop (rclone 1.76 refusing its flags did that). After a short
    wait, none may have restarted, be restarting, or have exited with an error;
    one-shot jobs that finished with 0 are fine."""
    time.sleep(settle)
    ids = run("docker", "ps", "-aq", "--filter", f"label=com.docker.compose.project={stack_name(name)}").stdout.split()
    bad = []
    for cid in ids:
        out = run("docker", "inspect", "-f",
                  "{{.Name}} {{.RestartCount}} {{.State.Status}} {{.State.ExitCode}}", cid).stdout.split()
        cname, restarts, status, code = out[0].lstrip("/"), int(out[1]), out[2], int(out[3])
        if restarts > 0 or status == "restarting" or (status == "exited" and code != 0):
            logs = run("docker", "logs", "--tail", "20", cid, check=False)
            bad.append(f"{cname}: {status}, exit code {code}, {restarts} restart(s)\n{logs.stdout}{logs.stderr}")
    if bad:
        raise SystemExit(f"{name}: containers don't stay up:\n" + "\n".join(bad))
    print(f"ok   {name} stays up ({len(ids)} containers)")


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
            p = run("docker", "run", "--rm", "--network", NETWORK, ALPINE, "wget", "-qO-", url, check=False)
            out = p.stdout
            # An app with nothing counted yet may answer empty: still a valid scrape.
            if "# TYPE" in out or "# HELP" in out or (p.returncode == 0 and not out.strip()):
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
    for _ in range(12):  # healthy isn't always answering yet: a 502 may pass
        body, head = get(BOT_CHECK[name])
        if marker in body:
            break  # the check itself: no point waiting
        if "HTTP/1.1 502" not in head and "HTTP/" in head:
            break
        time.sleep(5)
    if marker in body or "HTTP/1.1 502" in head or "HTTP/" not in head:
        raise SystemExit(f"{name}: {BOT_CHECK[name]} must reach the app past Anubis:\n{head}\n{body[:500]}")
    print(f"ok   {name} behind Anubis: / is checked, {BOT_CHECK[name]} passes")


def check_forgejo():
    """The identity provider from the test values is a sign-in option, and the
    runner runs with its rendered config."""
    c = stack_name("forgejo")
    auths = run("docker", "exec", "-u", "1000", f"{c}-forgejo-1", "forgejo", "admin", "auth", "list").stdout
    if not any(line.split()[1:3] == ["SSO", "OAuth2"] for line in auths.splitlines() if len(line.split()) >= 3):
        raise SystemExit(f"forgejo: no identity provider named SSO:\n{auths}")
    state = run("docker", "inspect", "--format", "{{.State.Status}} {{.RestartCount}}", f"{c}-runner-1").stdout.split()
    logs = run("docker", "logs", "--tail", "40", f"{c}-runner-1", check=False)
    if state != ["running", "0"]:
        raise SystemExit(f"forgejo: the runner isn't running steadily ({state}):\n{logs.stdout}{logs.stderr}")
    # Connected with the UUID and token from its config: Forgejo accepted it.
    if "declared successfully" not in logs.stdout + logs.stderr:
        raise SystemExit(f"forgejo: the runner didn't declare itself to Forgejo:\n{logs.stdout}{logs.stderr}")


def bookstack_login(container, email, password):
    """Signs in to BookStack through its form; returns where it sent us."""
    def curl(*args):
        out = run("docker", "exec", container, "curl", "-s", "-i", *args).stdout
        head, _, body = out.replace("\r\n", "\n").partition("\n\n")
        return head.splitlines(), body
    head, body = curl("http://localhost/login")
    # Secure cookies (APP_URL is https): pass them by hand, curl's jar would hold them back on http.
    cookies = "; ".join(h.split(":", 1)[1].split(";")[0].strip() for h in head if h.lower().startswith("set-cookie:"))
    token = body.split('name="_token" value="', 1)[1].split('"', 1)[0]
    head, _ = curl("-b", cookies, "--data-urlencode", f"_token={token}", "--data-urlencode", f"email={email}",
                   "--data-urlencode", f"password={password}", "http://localhost/login")
    return next((h.split(":", 1)[1].strip() for h in head if h.lower().startswith("location:")), "")


def check_bookstack():
    """The admin from the inputs signs in, the default admin@admin.com / password
    no longer does, and nobody can register."""
    c = stack_name("bookstack") + "-bookstack-1"
    v = OVERRIDES["bookstack"]
    # Every later start runs the one-shot again: it must find the admin done and succeed.
    again = run("docker", "start", "-a", stack_name("bookstack") + "-setup-1", check=False)
    if again.returncode != 0:
        raise SystemExit(f"bookstack: the setup one-shot fails when run again:\n{again.stdout}{again.stderr}")
    print("     setup run again: " + (again.stdout + again.stderr).strip().splitlines()[-1])
    where = bookstack_login(c, v["ADMIN_EMAIL"], v["ADMIN_PASSWORD"])
    if not where or where.endswith("/login"):
        raise SystemExit(f"bookstack: the admin from the inputs can't sign in (sent to {where!r})")
    print(f"     {v['ADMIN_EMAIL']} signs in: sent to {where}")
    where = bookstack_login(c, "admin@admin.com", "password")
    if not where.endswith("/login"):
        raise SystemExit(f"bookstack: the default admin@admin.com / password still signs in (sent to {where!r})")
    print(f"     admin@admin.com / password is refused: sent back to {where}")
    code = run("docker", "exec", c, "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost/register").stdout
    if code == "200":
        raise SystemExit("bookstack: the sign-up page is open")
    print(f"     /register answers {code}")


def check_opencloud():
    """With the office profile, Euro-Office answers WOPI discovery on the ingress
    network. (OpenCloud registers it by its domain, which doesn't resolve here, so
    that part can only be seen on a real host.)"""
    c = stack_name("opencloud")
    checks = {f"http://{c}-euro-office-1/hosting/discovery": "wopi-discovery"}
    for url, want in checks.items():
        out = ""
        for _ in range(24):
            out = run("docker", "run", "--rm", "--network", NETWORK, ALPINE, "wget", "-qO-", url, check=False).stdout
            if want in out:
                break
            time.sleep(5)
        else:
            raise SystemExit(f"opencloud: {url} lacks {want!r}:\n{out[:500]}")


def check_sweetcaptcha():
    """The widget's script and the health check answer, from the ingress network."""
    base = f"http://{stack_name('sweetcaptcha')}-sweetcaptcha-1:8080"
    for path, want in (("/healthz", ""), ("/v1/api.js", "sweetcaptcha")):
        p = run("docker", "run", "--rm", "--network", NETWORK, ALPINE, "wget", "-qO-", base + path, check=False)
        if p.returncode != 0 or want not in p.stdout.lower():
            raise SystemExit(f"sweetcaptcha: {path} didn't answer as expected:\n{p.stdout[:300]}{p.stderr}")


def check_garage():
    """The bucket and key Garage made on first start must store and return an object."""
    c = stack_name("garage") + "-garage-1"
    env = dict(line.split("=", 1) for line in run(
        "docker", "inspect", "--format", "{{range .Config.Env}}{{println .}}{{end}}", c).stdout.split() if "=" in line)
    s3 = ["-e", "RCLONE_CONFIG_G_TYPE=s3", "-e", "RCLONE_CONFIG_G_PROVIDER=Other",
          "-e", f"RCLONE_CONFIG_G_ACCESS_KEY_ID={env['GARAGE_DEFAULT_ACCESS_KEY']}",
          "-e", f"RCLONE_CONFIG_G_SECRET_ACCESS_KEY={env['GARAGE_DEFAULT_SECRET_KEY']}",
          "-e", f"RCLONE_CONFIG_G_ENDPOINT=http://{c}:3900", "-e", "RCLONE_CONFIG_G_REGION=garage",
          "-e", "RCLONE_CONFIG_G_FORCE_PATH_STYLE=true"]
    bucket = env["GARAGE_DEFAULT_BUCKET"]
    out = run("docker", "run", "--rm", "--network", NETWORK, *s3, "--entrypoint", "sh", RCLONE, "-c",
              f"echo stored-by-ci | rclone rcat g:{bucket}/ci.txt && rclone cat g:{bucket}/ci.txt", check=False)
    if out.stdout.strip() != "stored-by-ci":
        raise SystemExit(f"garage: an object didn't round-trip:\n{out.stdout}{out.stderr}")


def check_loki():
    """Logs from this host's containers must arrive in Loki, labelled by stack."""
    url = f"http://{stack_name('loki')}-loki-1:3100/loki/api/v1/query_range?limit=5&query=%7Bstack%3D~%22.%2B%22%7D"
    out = ""
    for _ in range(24):
        out = run("docker", "run", "--rm", "--network", NETWORK, ALPINE, "wget", "-qO-", url, check=False).stdout
        if '"values":[[' in out:
            return
        time.sleep(5)
    logs = run("docker", "logs", "--tail", "30", stack_name("loki") + "-alloy-1", check=False)
    raise SystemExit(f"loki: no logs arrived:\n{out[:500]}\n{logs.stdout}{logs.stderr}")


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
AFTER_DEPLOY = {"bookstack": check_bookstack, "immich": check_immich, "sweetcaptcha": check_sweetcaptcha, "opencloud": check_opencloud, "forgejo": check_forgejo, "loki": check_loki, "garage": check_garage, "fail2ban": check_fail2ban, "dozzle": check_dozzle, "prometheus": check_prometheus, "pihole": check_pihole, "sure": check_sure}


# Changing these can affect every template, so all of them are tested again.
SHARED = ("scripts/test-templates.py", ".github/workflows/validate.yml")


def changed_templates(base):
    """The templates a change since base touches, or None for all of them: no
    base (a scheduled run), an unknown one (a new branch), or shared files."""
    if not base or set(base) == {"0"}:
        return None
    diff = run("git", "diff", "--name-only", f"{base}...HEAD", cwd=ROOT, check=False)
    if diff.returncode != 0:
        return None
    files = diff.stdout.split()
    if any(f in SHARED for f in files):
        return None
    names = {f.split("/")[1] for f in files if f.split("/")[0] in ("apps", "system") and f.count("/") >= 2}
    if "scripts/test-values.json" in files:
        before = run("git", "show", f"{base}:scripts/test-values.json", cwd=ROOT, check=False)
        if before.returncode != 0:
            return None
        old = json.loads(before.stdout)
        keys = set(old) | set(OVERRIDES)
        changed = {k for k in keys if old.get(k) != OVERRIDES.get(k)}
        # Skipping a template, or no longer skipping it, concerns that one only.
        if "_skip_deploy" in changed:
            changed.discard("_skip_deploy")
            changed |= set(old.get("_skip_deploy", {})) ^ set(OVERRIDES.get("_skip_deploy", {}))
        if any(k.startswith("_") for k in changed):
            return None  # other shared settings: test everything
        names |= changed
    return names


def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "list":
        skip = set(OVERRIDES.get("_skip_deploy", {}))
        names = [p.parent.name for tier in ("system", "apps") for p in sorted((ROOT / tier).glob("*/template.yaml"))]
        if "--deploy" in args:
            names = [n for n in names if n not in skip]
        if "--swarm" in args:
            names = [n for n in names if supports_swarm(n)]
        if "--changed" in args:
            only = changed_templates(args[args.index("--changed") + 1])
            if only is not None:
                names = [n for n in names if n in only]
        print(json.dumps(names))
    elif cmd == "deploy":
        deploy(args[0], args[1:])
    elif cmd == "deploy-swarm":
        deploy_swarm(args[0], args[1:])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
