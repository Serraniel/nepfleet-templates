# SPDX-License-Identifier: AGPL-3.0-or-later
# Caddy with Docker label support and DNS-01 providers, used by system/caddy.
# Base images are pinned by digest; Dependabot bumps both tag and digest together.
FROM caddy:2.11.8-builder@sha256:d4eb070c36154bd2d4c94b40359a03c6168346d5af5404963c74691ab77fb63f AS build
RUN xcaddy build \
      --with github.com/lucaslorentz/caddy-docker-proxy/v2 \
      --with github.com/caddy-dns/cloudflare \
      --with github.com/caddy-dns/hetzner/v2 \
      --with github.com/caddy-dns/desec

FROM caddy:2.11.8-alpine@sha256:f6228111e5fafa1a5238258d0858e103f10599b8d1659a146e7726681a002bb9
COPY --from=build /usr/bin/caddy /usr/bin/caddy
CMD ["caddy", "docker-proxy"]
