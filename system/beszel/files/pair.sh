#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# Lets beszel-agent stacks pair with this hub with nothing copied from
# Beszel's Add System dialog:
#  - AGENT_TOKEN becomes the admin's permanent universal token: an agent that
#    connects with it is added as a new system;
#  - a read-only user, agents@beszel.invalid with PAIR_PASSWORD, may read the
#    hub's public key, which an agent needs to trust the hub. It sees no
#    systems and can change nothing.
# Runs on every apply; both steps are upserts. Uses the admin from the
# stack's inputs (Beszel also makes a superuser with it on its first start).
# No dollar-brace placeholders in here: NepFleet would fill them in when it
# renders the file.
set -eu

hub=http://beszel:8090/api
pair_email=agents@beszel.invalid

fail() {
    echo "$1" >&2
    exit 1
}

# Passwords go to curl from files, never as arguments other processes see.
umask 077
tmp=$(mktemp -d)
trap 'rm -r "$tmp"' EXIT
printf '%s' "$ADMIN_PASSWORD" > "$tmp/admin"
printf '%s' "$PAIR_PASSWORD" > "$tmp/pair"
# Beszel's universal-token endpoint reads JSON only (a form body is ignored).
printf '{"token":"%s","enable":1,"permanent":1}' \
    "$(printf '%s' "$AGENT_TOKEN" | sed 's/\\/\\\\/g; s/"/\\"/g')" > "$tmp/token.json"

# auth <collection>: a token for the admin, or nothing when it can't sign in.
auth() {
    curl -fsS --data-urlencode "identity=$ADMIN_EMAIL" --data-urlencode "password@$tmp/admin" \
        "$hub/collections/$1/auth-with-password" 2>/dev/null |
        sed -n 's/.*"token":"\([^"]*\)".*/\1/p'
}

for i in $(seq 60); do
    curl -fsS -o /dev/null "$hub/health" && break
    [ "$i" = 60 ] && fail "Beszel didn't answer within 5 minutes"
    sleep 5
done

user=$(auth users)
superuser=$(auth _superusers)
if [ -z "$user" ] || [ -z "$superuser" ]; then
    # The password was changed in Beszel, or the admin was made by hand.
    # What an earlier run set up stays; new agents need Add System.
    echo "the admin from the stack's inputs doesn't sign in: agents can't pair by themselves" >&2
else
    answer=$(curl -fsS -H "Authorization: $user" -H "Content-Type: application/json" \
        --data-binary "@$tmp/token.json" "$hub/beszel/universal-token") || answer=
    case $answer in
        *'"permanent":true'*) echo "universal token set" ;;
        *) fail "Beszel didn't keep the universal token" ;;
    esac

    id=$(curl -fsS -G -H "Authorization: $superuser" \
        --data-urlencode "filter=email='$pair_email'" "$hub/collections/users/records" |
        sed -n 's/.*"id":"\([^"]*\)".*/\1/p') || fail "Beszel didn't list its users"
    fields="--data-urlencode password@$tmp/pair --data-urlencode passwordConfirm@$tmp/pair -d role=readonly -d verified=true"
    if [ -z "$id" ]; then
        # shellcheck disable=SC2086
        curl -fsS -o /dev/null -H "Authorization: $superuser" -d "email=$pair_email" $fields \
            "$hub/collections/users/records" || fail "Beszel refused to create $pair_email"
        echo "user $pair_email created"
    else
        # shellcheck disable=SC2086
        curl -fsS -o /dev/null -X PATCH -H "Authorization: $superuser" $fields \
            "$hub/collections/users/records/$id" || fail "Beszel refused to update $pair_email"
        echo "user $pair_email updated"
    fi
fi
