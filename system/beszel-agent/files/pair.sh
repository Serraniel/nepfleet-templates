#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# Reads the hub's public key, which the agent needs to trust the hub, so it
# isn't copied from Beszel's Add System dialog. It signs in as the hub
# stack's read-only user agents@beszel.invalid with PAIR_PASSWORD and keeps
# the key in the agent's volume (KEY_FILE). With KEY set, there is nothing
# to do: the agent takes KEY first.
# Runs before every start of the agent. A key read earlier stays in use
# while the hub can't be reached, so the agent still starts.
# No dollar-brace placeholders in here: NepFleet would fill them in when it
# renders the file.
set -eu

[ -n "$KEY" ] && exit 0

file=$KEY_FILE
if [ -z "$PAIR_PASSWORD" ]; then
    [ -s "$file" ] && exit 0
    echo "set PAIR_PASSWORD (from the hub stack) or KEY (from Beszel's Add System)" >&2
    exit 1
fi

hub=$(printf '%s' "$HUB_URL" | sed 's:/*$::')/api
umask 077
tmp=$(mktemp -d)
trap 'rm -r "$tmp"' EXIT
printf '%s' "$PAIR_PASSWORD" > "$tmp/pair"

tries=60
[ -s "$file" ] && tries=3
for i in $(seq "$tries"); do
    token=$(curl -fsS --data-urlencode "identity=agents@beszel.invalid" --data-urlencode "password@$tmp/pair" \
        "$hub/collections/users/auth-with-password" | sed -n 's/.*"token":"\([^"]*\)".*/\1/p') || true
    if [ -n "$token" ]; then
        key=$(curl -fsS -H "Authorization: $token" "$hub/beszel/info" |
            sed -n 's/.*"key":"\(ssh-ed25519 [^"]*\)".*/\1/p') || true
        if [ -n "$key" ]; then
            printf '%s\n' "$key" > "$tmp/key"
            mv "$tmp/key" "$file"
            echo "hub key: $key"
            exit 0
        fi
    fi
    [ "$i" = "$tries" ] && break
    sleep 5
done

if [ -s "$file" ]; then
    echo "the hub didn't answer: the key read earlier stays in use" >&2
    exit 0
fi
echo "couldn't read the hub's key from $HUB_URL: is the hub stack applied, and is PAIR_PASSWORD its PAIR_PASSWORD?" >&2
exit 1
