# SPDX-License-Identifier: AGPL-3.0-or-later
# Caddy with Docker label support, DNS-01 providers and DNS record updates
# (caddy-dynamicdns), used by system/caddy.
# Base images are pinned by digest; Dependabot bumps both tag and digest together.
FROM caddy:2.11.9-builder@sha256:3fddbec729442a56b942d4c9eaef1df80893dbf2cf5b86701bfae6aad1408eeb AS build
# caddy-dynamicdns at a pinned commit, patched: its dynamic_domains looks for
# host matchers as values, but Caddy stores them as pointers, so it never found
# a site. Drop that patch once upstream accepts both. NepFleet's own patch: it
# never manages the zone's apex, which often points at another server.
ARG DYNAMICDNS_COMMIT=67d107a42c0279f6e6d58a6afe646745c8b44f78
RUN git clone --quiet https://github.com/mholt/caddy-dynamicdns /src/dynamicdns \
 && git -C /src/dynamicdns checkout --quiet "$DYNAMICDNS_COMMIT" \
 && sed -i 's|if hs, ok := rm.(caddyhttp.MatchHost); ok {|if p, isPtr := rm.(*caddyhttp.MatchHost); isPtr \&\& p != nil { rm = *p }\n\t\t\t\t\tif hs, ok := rm.(caddyhttp.MatchHost); ok {|' /src/dynamicdns/dynamicdns.go \
 && sed -i '/if h == zone {/{n;s|return "@", true|return "", false // NepFleet: never the apex|}' /src/dynamicdns/dynamicdns.go \
 && grep -q 'rm.(\*caddyhttp.MatchHost)' /src/dynamicdns/dynamicdns.go \
 && grep -q 'never the apex' /src/dynamicdns/dynamicdns.go
RUN xcaddy build \
      --with github.com/lucaslorentz/caddy-docker-proxy/v2 \
      --with github.com/caddy-dns/cloudflare \
      --with github.com/caddy-dns/hetzner/v2 \
      --with github.com/caddy-dns/desec \
      --with github.com/mholt/caddy-dynamicdns=/src/dynamicdns

FROM caddy:2.11.9-alpine@sha256:0bbb055bda6793c999bde78b1b5ce3e89f829fb031af2cf50056ea1246559fee
COPY --from=build /usr/bin/caddy /usr/bin/caddy
CMD ["caddy", "docker-proxy"]
