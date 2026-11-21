#!/bin/bash
# Vaultwarden's own start, with one step before it: on the first start, the
# owner's account is created from the stack's inputs (OWNER_EMAIL,
# OWNER_PASSWORD), so sign-ups can stay closed to everyone else.
#
# Accounts are end-to-end encrypted: the server never sees the master
# password, only what the Bitwarden clients derive from it. So this does what
# a client does when it registers (the PBKDF2 master key and its hash, the
# account key encrypted with it, an RSA key pair encrypted with that, all with
# openssl) and registers through the API of a Vaultwarden that listens only on
# 127.0.0.1, with sign-ups open for that moment. Then it stops that one and
# starts the real one. A marker in /data makes later starts skip all this, so
# the password can be changed in Vaultwarden afterwards.
set -u

marker=/data/.nepfleet-owner-created
port=8079   # the temporary Vaultwarden, on 127.0.0.1 only
api=http://127.0.0.1:$port

hex() { od -An -tx1 -v "$1" | tr -d ' \n'; }
b64() { base64 -w0 "$1"; }

# encstr FILE ENC_KEY_HEX MAC_KEY_HEX: FILE as a Bitwarden EncString of type 2
# (AES-256-CBC, then HMAC-SHA256 over IV and ciphertext).
encstr() {
  local d
  d=$(mktemp -d -p "$work")
  openssl rand -out "$d/iv" 16
  openssl enc -aes-256-cbc -K "$2" -iv "$(hex "$d/iv")" -in "$1" -out "$d/ct" || return 1
  cat "$d/iv" "$d/ct" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:$3" -binary > "$d/mac" || return 1
  printf '2.%s|%s|%s' "$(b64 "$d/iv")" "$(b64 "$d/ct")" "$(b64 "$d/mac")"
}

kdf() { openssl kdf -binary -keylen 32 -kdfopt digest:SHA256 "$@"; }

create_owner() {
  set -e
  local email name pw iter=600000
  email=$(printf %s "$OWNER_EMAIL" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
  case "$email" in
    *@*) ;;
    *) echo "owner: OWNER_EMAIL is not an e-mail address"; return 1 ;;
  esac
  case "$email" in *[\"\\]*) echo "owner: OWNER_EMAIL has a quote or backslash"; return 1 ;; esac
  if [ -z "$OWNER_PASSWORD" ]; then echo "owner: OWNER_PASSWORD is empty"; return 1; fi
  name=$(printf %s "$email" | cut -d@ -f1 | tr -cd 'A-Za-z0-9._-' | cut -c1-50)
  pw=$(printf %s "$OWNER_PASSWORD" | od -An -tx1 -v | tr -d ' \n')

  # What the clients derive (KDF PBKDF2-SHA256, 600000 iterations, the
  # e-mail as salt): the master key, and the hash the server stores.
  kdf -kdfopt "hexpass:$pw" -kdfopt "salt:$email" -kdfopt "iter:$iter" -out "$work/master" PBKDF2
  kdf -kdfopt "hexpass:$(hex "$work/master")" -kdfopt "hexsalt:$pw" -kdfopt iter:1 -out "$work/hash" PBKDF2
  # The master key stretched (HKDF-Expand) into an encryption and a MAC key.
  kdf -kdfopt mode:EXPAND_ONLY -kdfopt "hexkey:$(hex "$work/master")" -kdfopt info:enc -out "$work/enc" HKDF
  kdf -kdfopt mode:EXPAND_ONLY -kdfopt "hexkey:$(hex "$work/master")" -kdfopt info:mac -out "$work/mac" HKDF
  # The account key (64 random bytes: encryption and MAC key), encrypted
  # with the stretched master key; and the RSA key pair, its private key
  # encrypted with the account key.
  openssl rand -out "$work/user" 64
  local user key priv pub
  user=$(hex "$work/user")
  key=$(encstr "$work/user" "$(hex "$work/enc")" "$(hex "$work/mac")")
  openssl genpkey -quiet -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -outform DER -out "$work/rsa"
  openssl pkey -inform DER -in "$work/rsa" -pubout -outform DER -out "$work/rsa.pub"
  priv=$(encstr "$work/rsa" "$(printf %s "$user" | cut -c1-64)" "$(printf %s "$user" | cut -c65-128)")
  pub=$(b64 "$work/rsa.pub")

  env -u ADMIN_TOKEN ROCKET_ADDRESS=127.0.0.1 ROCKET_PORT=$port SIGNUPS_ALLOWED=true SIGNUPS_DOMAINS_WHITELIST= \
    SIGNUPS_VERIFY=false /start.sh &
  pid=$!
  trap 'kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null' EXIT
  local i
  for i in $(seq 120); do
    curl -fsS -o /dev/null "$api/alive" 2>/dev/null && break
    kill -0 "$pid" 2>/dev/null || { echo "owner: Vaultwarden did not start"; return 1; }
    sleep 0.5
  done

  local token out
  token=$(curl -sS -H 'Content-Type: application/json' \
    -d "{\"email\":\"$email\",\"name\":\"$name\"}" "$api/identity/accounts/register/send-verification-email")
  case "$token" in
    eyJ*) ;;
    *) echo "owner: no registration token: $token"; return 1 ;;
  esac
  out=$(curl -sS -H 'Content-Type: application/json' -d @- "$api/identity/accounts/register/finish" <<EOF
{"email":"$email","emailVerificationToken":"$token","masterPasswordHash":"$(b64 "$work/hash")","key":"$key","kdf":0,"kdfIterations":$iter,"keys":{"publicKey":"$pub","encryptedPrivateKey":"$priv"}}
EOF
)
  case "$out" in
    *registerFinish*) echo "owner: account $email created" ;;
    *"already exists"*) echo "owner: account $email exists" ;;
    *) echo "owner: registration failed: $out"; return 1 ;;
  esac
}

if [ ! -e "$marker" ]; then
  work=$(mktemp -d)
  (umask 077; create_owner)
  if [ $? -eq 0 ]; then
    touch "$marker"
  else
    echo "owner: the account was not created; trying again on the next start" >&2
  fi
  rm -r "$work"
fi
unset OWNER_PASSWORD
# An empty admin token: no admin page, without Vaultwarden's warnings about it.
[ -n "$(printenv ADMIN_TOKEN)" ] || unset ADMIN_TOKEN
exec /start.sh
