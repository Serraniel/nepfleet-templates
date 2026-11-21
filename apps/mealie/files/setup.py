# SPDX-License-Identifier: AGPL-3.0-or-later
# Makes Mealie's admin the one from the stack's inputs. Mealie creates its
# admin on the first start as changeme@example.com / MyPassword, and has no
# setting for it. While that login still works, this signs in with it and
# changes the admin's email, name and password to ADMIN_EMAIL, ADMIN_NAME and
# ADMIN_PASSWORD. Once they are changed the default login fails and this does
# nothing, so later changes made in Mealie stay.
# Runs in Mealie's container, started next to Mealie, with Python's standard
# library only. When done it leaves READY_FILE, which the health check wants.
# No dollar-brace placeholders in here: NepFleet would fill them in when it
# renders the file.
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_EMAIL = "changeme@example.com"
DEFAULT_PASSWORD = "MyPassword"

email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
name = os.environ.get("ADMIN_NAME", "").strip()
password = os.environ.get("ADMIN_PASSWORD", "")
if not email or not password:
    sys.exit("setup: ADMIN_EMAIL and ADMIN_PASSWORD are required")
if len(password) < 8:
    sys.exit("setup: ADMIN_PASSWORD must have at least 8 characters (Mealie's rule)")

api = os.environ.get("MEALIE_URL", "http://127.0.0.1:9000").rstrip("/") + "/api"
ready_file = os.environ.get("READY_FILE", "/tmp/admin-set")


def done(message):
    print("setup: " + message, flush=True)
    with open(ready_file, "w") as f:
        f.write(message + "\n")
    sys.exit(0)


def call(method, path, token=None, body=None, form=None):
    headers = {"Accept": "application/json"}
    data = None
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(api + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as res:
        raw = res.read()
        return json.loads(raw) if raw else None


# Until Mealie answers (it starts alongside), keep asking.
for attempt in range(180):
    try:
        call("GET", "/app/about")
        break
    except (urllib.error.URLError, OSError):
        time.sleep(5)
else:
    sys.exit("setup: Mealie did not answer at " + api)

try:
    token = call("POST", "/auth/token", form={"username": DEFAULT_EMAIL, "password": DEFAULT_PASSWORD})["access_token"]
except urllib.error.HTTPError as e:
    if e.code == 401:
        done("the default admin login no longer works: nothing to do")
    raise

user = call("GET", "/users/self", token)
user["email"] = email
if name:
    user["fullName"] = name
call("PUT", "/users/" + user["id"], token, body=user)
call("PUT", "/users/password", token, body={"currentPassword": DEFAULT_PASSWORD, "newPassword": password})

# Check: the new login works, the default one no longer does.
call("POST", "/auth/token", form={"username": email, "password": password})
try:
    call("POST", "/auth/token", form={"username": DEFAULT_EMAIL, "password": DEFAULT_PASSWORD})
    sys.exit("setup: the default admin login still works")
except urllib.error.HTTPError as e:
    if e.code != 401:
        raise
done("admin set to " + email)
