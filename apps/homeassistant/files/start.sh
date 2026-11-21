#!/bin/sh
# Runs before Home Assistant on every start, then hands over to the image's
# own /init.
set -eu

# Requests through Caddy carry X-Forwarded-For, which Home Assistant answers
# with 400 unless they come from a trusted proxy: trust this host's Docker
# bridges (host networking sees them; Caddy is on one) and the host itself.
# Docker may have put the ingress network in 172.16.0.0/12 or in
# 192.168.0.0/16, and the LAN is not trusted.
# shellcheck disable=SC2046
python3 -P /setup/http_config.py 127.0.0.1/32 \
  $(ip -4 -o addr show | awk '$2 == "docker0" || $2 ~ /^br-/ { print $4 }' |
    python3 -P -c 'import ipaddress, sys; print(" ".join(str(ipaddress.ip_interface(a).network) for a in sys.stdin.read().split()))') ||
  echo "nepfleet http: proxies not set; requests through Caddy may get 400"

# Finishes onboarding (the owner from the stack's inputs) once the API is up,
# so the first-run wizard is never open; does nothing when it is done.
python3 -P /setup/onboard.py &

exec /init
