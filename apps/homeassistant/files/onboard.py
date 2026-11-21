"""Finishes Home Assistant's onboarding through its API, as the wizard would:
the owner from the stack's inputs (ADMIN_NAME, ADMIN_USER, ADMIN_PASSWORD),
then the remaining steps. Started in the background by start.sh; does
nothing when onboarding is done. Analytics stay off (the step only records
that it was shown)."""

import asyncio
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8123"
CLIENT_ID = BASE + "/"


def log(msg):
    print(f"nepfleet onboarding: {msg}", flush=True)


def call(path, data=None, token=None, form=False):
    headers = {}
    body = None
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(BASE + path, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"null")


def steps():
    """The onboarding steps still to do, or None while the API is not up.
    Once onboarding is done, Home Assistant no longer serves /api/onboarding."""
    try:
        return [s["step"] for s in call("/api/onboarding") if not s["done"]]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return None
        try:
            with open("/config/.storage/onboarding", encoding="utf-8") as f:
                done = json.load(f)["data"]["done"]
        except (OSError, ValueError, KeyError):
            return None
        return [s for s in ("user", "core_config", "analytics", "integration") if s not in done]
    except (urllib.error.URLError, OSError, ValueError):
        return None


def status():
    """The steps still to do, once the API answers."""
    for _ in range(600):  # first start installs packages: allow 20 minutes
        todo = steps()
        if todo is not None:
            return todo
        time.sleep(2)
    raise SystemExit("Home Assistant's API did not come up")


def login(user, password):
    """An auth code for an existing owner, through the login flow."""
    flow = call("/auth/login_flow", {"client_id": CLIENT_ID, "handler": ["homeassistant", None],
                                     "redirect_uri": CLIENT_ID})
    res = call(f"/auth/login_flow/{flow['flow_id']}", {"client_id": CLIENT_ID, "username": user,
                                                       "password": password})
    if res.get("type") != "create_entry":
        raise SystemExit(f"cannot sign in as {user} to finish onboarding: {res.get('errors')}")
    return res["result"]


def country(tz):
    """The country of time zone tz (zone.tab), as the wizard would guess it."""
    try:
        with open("/usr/share/zoneinfo/zone.tab", encoding="utf-8") as f:
            for line in f:
                cols = line.split("\t")
                if len(cols) >= 3 and not line.startswith("#") and cols[2].strip() == tz:
                    return cols[0]
    except OSError:
        pass
    return None


async def set_location(token, tz):
    """Home Assistant's own time zone (UTC until set) and country (asked for
    in Repairs until set), from the stack's TZ."""
    import aiohttp  # in the image

    update = {"time_zone": tz}
    if cc := country(tz):
        update["country"] = cc
    async with aiohttp.ClientSession() as s, s.ws_connect(BASE.replace("http", "ws") + "/api/websocket") as ws:
        await ws.receive_json()
        await ws.send_json({"type": "auth", "access_token": token})
        if (await ws.receive_json()).get("type") != "auth_ok":
            raise RuntimeError("websocket auth failed")
        await ws.send_json({"id": 1, "type": "config/core/update", **update})
        res = await ws.receive_json()
        if not res.get("success"):
            raise RuntimeError(res.get("error"))


def main():
    todo = status()
    if not todo:
        log("done already")
        return
    name = os.environ.get("ADMIN_NAME") or "Admin"
    user = os.environ["ADMIN_USER"]
    password = os.environ["ADMIN_PASSWORD"]
    if "user" in todo:
        code = call("/api/onboarding/users", {"client_id": CLIENT_ID, "name": name, "username": user,
                                              "password": password, "language": "en"})["auth_code"]
        log(f"owner {user} created")
    else:
        code = login(user, password)
    token = call("/auth/token", {"grant_type": "authorization_code", "code": code, "client_id": CLIENT_ID},
                 form=True)["access_token"]
    if "core_config" in todo:
        tz = os.environ.get("TZ")
        if tz:
            try:
                asyncio.run(set_location(token, tz))
            except Exception as e:  # not worth failing onboarding for
                log(f"time zone {tz} and its country not set: {e}")
        call("/api/onboarding/core_config", {}, token)
    if "analytics" in todo:
        call("/api/onboarding/analytics", {}, token)
    if "integration" in todo:
        call("/api/onboarding/integration", {"client_id": CLIENT_ID, "redirect_uri": CLIENT_ID + "?auth_callback=1"},
             token)
    log("done")


if __name__ == "__main__":
    if sys.argv[1:] == ["--health"]:
        # Healthy once the API answers and the owner exists: before that,
        # whoever reaches it first could claim it.
        todo = steps()
        sys.exit(todo is None or "user" in todo)
    try:
        main()
    except urllib.error.HTTPError as e:
        sys.exit(f"nepfleet onboarding: {e.code} from {e.url}: {e.read()[:300]!r}")
