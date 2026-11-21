# SPDX-License-Identifier: AGPL-3.0-or-later
# Runs in the Pocket ID container, next to Pocket ID, on every start.
# Creates the admin from the stack's inputs as soon as Pocket ID answers, so
# its /setup page (whose first visitor becomes the admin) is closed before
# anyone can use it. Pocket ID signs in with passkeys only, and a new admin
# has none: while it has none, every start prints a one-time sign-in link,
# valid for an hour, to Pocket ID's log. The owner opens it, is signed in and
# adds a passkey. Once the admin has one, or when Pocket ID was set up by
# hand before, it does nothing.
# Uses what the image has (Alpine: sh and BusyBox wget) and Pocket ID's API
# with the static API key. No dollar-brace placeholders in here: NepFleet
# would fill them in when it renders the file.
set -u

api=http://127.0.0.1:1411
# The admin's fixed ID: later starts find it without parsing JSON.
admin_id=6f1e2c7a-0b5d-4c3e-9a8f-2d4b6c8e0a11
ttl=1h

say() {
    echo "setup: $*"
}

# get PATH: prints the body, fails on any status but 2xx.
get() {
    wget -q -O - --header "X-API-Key: $STATIC_API_KEY" "$api$1"
}

# post PATH JSON: prints the body, fails on any status but 2xx.
post() {
    wget -q -O - --header "X-API-Key: $STATIC_API_KEY" \
        --header "Content-Type: application/json" --post-data "$2" "$api$1"
}

# JSON string contents: backslashes and quotes escaped.
esc() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

i=0
until wget -q -O /dev/null "$api/healthz" 2>/dev/null; do
    i=$((i + 1))
    if [ "$i" -ge 600 ]; then
        say "Pocket ID did not answer within 5 minutes; no admin was created" >&2
        exit 1
    fi
    sleep 0.5
done

# 204: no user yet, so /setup is open. 404: someone exists already.
if wget -q -O /dev/null "$api/api/signup/setup" 2>/dev/null; then
    name=$(esc "$ADMIN_NAME")
    body="{\"id\":\"$admin_id\",\"username\":\"$(esc "$ADMIN_USERNAME")\",\"email\":\"$(esc "$ADMIN_EMAIL")\",\"emailVerified\":true,\"firstName\":\"$name\",\"displayName\":\"$name\",\"isAdmin\":true}"
    if ! post /api/users "$body" >/dev/null; then
        # /setup stays open to whoever comes first: rather stop Pocket ID.
        say "creating the admin $ADMIN_USERNAME failed; stopping Pocket ID, as its /setup page is still open" >&2
        kill 1
        exit 1
    fi
    say "created the admin $ADMIN_USERNAME ($ADMIN_EMAIL); /setup is closed"
elif ! get "/api/users/$admin_id" >/dev/null 2>&1; then
    say "Pocket ID was set up by hand before: nothing to do"
    exit 0
fi

if ! creds=$(get "/api/users/$admin_id/webauthn-credentials"); then
    say "could not read the admin's passkeys" >&2
    exit 1
fi
case "$creds" in
    null | "[]" | "") ;;
    *)
        say "the admin $ADMIN_USERNAME has a passkey: nothing to do"
        exit 0
        ;;
esac

token=$(post "/api/users/$admin_id/one-time-access-token" "{\"ttl\":\"$ttl\"}" |
    sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
if [ -z "$token" ]; then
    say "Pocket ID gave no one-time sign-in link" >&2
    exit 1
fi
say "the admin $ADMIN_USERNAME has no passkey yet. Open this link once, within an hour, to sign in and add one:"
say "$APP_URL/lc/$token"
say "expired? Restart Pocket ID (or re-apply the stack) for a new link"
