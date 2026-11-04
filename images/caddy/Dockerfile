# SPDX-License-Identifier: AGPL-3.0-or-later
# Caddy with Docker label support and DNS-01 providers, used by system/caddy.
# Base images are pinned by digest; Dependabot bumps both tag and digest together.
FROM caddy:2.11.7-builder@sha256:c4cd20eaa0b69112fd5d4f721ffc9671687e1d5d0b155c8620cf7546dbef94c0 AS build
RUN xcaddy build \
      --with github.com/lucaslorentz/caddy-docker-proxy/v2 \
      --with github.com/caddy-dns/cloudflare \
      --with github.com/caddy-dns/hetzner/v2 \
      --with github.com/caddy-dns/desec

FROM caddy:2.11.7-alpine@sha256:e70b164da81ef698b3ad19af799ea6086ce6d9e48ed4079eb9fe26f6fbf14ee5
COPY --from=build /usr/bin/caddy /usr/bin/caddy
CMD ["caddy", "docker-proxy"]
