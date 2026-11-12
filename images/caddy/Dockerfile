# SPDX-License-Identifier: AGPL-3.0-or-later
# Caddy with Docker label support and DNS-01 providers, used by system/caddy.
# Base images are pinned by digest; Dependabot bumps both tag and digest together.
FROM caddy:2.11.9-builder@sha256:3fddbec729442a56b942d4c9eaef1df80893dbf2cf5b86701bfae6aad1408eeb AS build
RUN xcaddy build \
      --with github.com/lucaslorentz/caddy-docker-proxy/v2 \
      --with github.com/caddy-dns/cloudflare \
      --with github.com/caddy-dns/hetzner/v2 \
      --with github.com/caddy-dns/desec

FROM caddy:2.11.9-alpine@sha256:0bbb055bda6793c999bde78b1b5ce3e89f829fb031af2cf50056ea1246559fee
COPY --from=build /usr/bin/caddy /usr/bin/caddy
CMD ["caddy", "docker-proxy"]
