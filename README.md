# NepFleet templates

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/Serraniel/nepfleet-templates/badge)](https://scorecard.dev/viewer/?uri=github.com/Serraniel/nepfleet-templates)

The official catalogue of [NepFleet](https://github.com/Serraniel/nepfleet) templates. The format is described in the [template spec](https://github.com/Serraniel/nepfleet/blob/main/docs/spec/template.md).

- `system/`: services NepFleet itself builds on, such as ingress, logs, uptime and tunnels. All of them are opt-in.
- `apps/`: services you run.
- `images/`: images this repository builds, published as `ghcr.io/serraniel/nepfleet-<name>`.

> In CI every template is validated, every image tag is checked, swarm templates pass `docker stack config`, and every template is installed with test values through `nepfleet apply` and must become healthy (except the few `_skip_deploy` lists in `scripts/test-values.json`, each with its reason). Integrations such as TLS and SSO are not exercised end to end yet. Review templates before production use.

## Catalogue

<!-- catalogue:start -->

Legend: 🌐 ingress · 📈 monitoring · 📊 statusPage · 🏠 dashboard · 🐝 swarm · 💾 backup · 🔑 sso · 🦾 arm64

| Template | Project | Tier | Integrations |
|---|---|---|---|
| [backrest](system/backrest) | [Backrest (restic)](https://github.com/garethgeorge/backrest) | system | 🌐 📈 🏠 💾 🦾 |
| [binfmt](system/binfmt) | [Foreign-architecture emulation](https://github.com/tonistiigi/binfmt) | system | 🦾 |
| [caddy](system/caddy) | [Caddy ingress](https://github.com/lucaslorentz/caddy-docker-proxy) | system | 🐝 💾 🦾 |
| [dozzle](system/dozzle) | [Dozzle](https://dozzle.dev) · [source](https://github.com/amir20/dozzle) | system | 🌐 📈 🏠 🐝 🦾 |
| [frpc](system/frpc) | [frp client (home side)](https://github.com/fatedier/frp) | system | 🦾 |
| [frps](system/frps) | [frp server (public side)](https://github.com/fatedier/frp) | system | 🌐 🦾 |
| [homepage](system/homepage) | [Homepage](https://gethomepage.dev) · [source](https://github.com/gethomepage/homepage) | system | 🌐 📈 🐝 💾 🦾 |
| [neptide](system/neptide) | [neptide image updates](https://github.com/Serraniel/neptide) | system | 🐝 🦾 |
| [uptime-kuma](system/uptime-kuma) | [Uptime Kuma + AutoKuma](https://github.com/louislam/uptime-kuma) | system | 🌐 📊 🏠 🐝 💾 🦾 |
| [volume-backup](system/volume-backup) | [Volume backups (docker-volume-backup)](https://offen.github.io/docker-volume-backup/) · [source](https://github.com/offen/docker-volume-backup) | system | 🦾 |
| [watchtower](system/watchtower) | [Watchtower (maintained fork)](https://github.com/nicholas-fedor/watchtower) | system | 🦾 |
| [actual](apps/actual) | [Actual Budget](https://actualbudget.org) · [source](https://github.com/actualbudget/actual) | app | 🌐 📈 🏠 💾 🦾 |
| [audiobookshelf](apps/audiobookshelf) | [Audiobookshelf](https://www.audiobookshelf.org) · [source](https://github.com/advplyr/audiobookshelf) | app | 🌐 📈 🏠 💾 🦾 |
| [bookstack](apps/bookstack) | [BookStack](https://www.bookstackapp.com) · [source](https://github.com/BookStackApp/BookStack) | app | 🌐 📈 🏠 💾 🦾 |
| [forgejo](apps/forgejo) | [Forgejo + Actions runner](https://forgejo.org) · [source](https://codeberg.org/forgejo/forgejo) | app | 🌐 📈 🏠 💾 🦾 |
| [homeassistant](apps/homeassistant) | [Home Assistant](https://www.home-assistant.io) · [source](https://github.com/home-assistant/core) | app | 🌐 📈 🏠 💾 🦾 |
| [homebox](apps/homebox) | [Homebox](https://homebox.software) · [source](https://github.com/sysadminsmedia/homebox) | app | 🌐 📈 🏠 🐝 💾 🦾 |
| [immich](apps/immich) | [Immich (+ Power Tools)](https://immich.app) · [source](https://github.com/immich-app/immich) | app | 🌐 📈 🏠 💾 🦾 |
| [jellyfin](apps/jellyfin) | [Jellyfin](https://jellyfin.org) · [source](https://github.com/jellyfin/jellyfin) | app | 🌐 📈 🏠 💾 🦾 |
| [kutt](apps/kutt) | [Kutt](https://github.com/thedevs-network/kutt) | app | 🌐 📈 🏠 💾 🦾 |
| [mealie](apps/mealie) | [Mealie](https://mealie.io) · [source](https://github.com/mealie-recipes/mealie) | app | 🌐 📈 🏠 💾 🦾 |
| [metube](apps/metube) | [MeTube (yt-dlp web UI)](https://github.com/alexta69/metube) | app | 🌐 📈 🏠 🦾 |
| [n8n](apps/n8n) | [n8n](https://n8n.io) · [source](https://github.com/n8n-io/n8n) | app | 🌐 📈 🏠 💾 🦾 |
| [navidrome](apps/navidrome) | [Navidrome](https://www.navidrome.org) · [source](https://github.com/navidrome/navidrome) | app | 🌐 📈 🏠 💾 🦾 |
| [open-webui](apps/open-webui) | [Open WebUI (+ Ollama, LiteLLM)](https://openwebui.com) · [source](https://github.com/open-webui/open-webui) | app | 🌐 📈 🏠 💾 |
| [opencloud](apps/opencloud) | [OpenCloud](https://opencloud.eu) · [source](https://github.com/opencloud-eu/opencloud) | app | 🌐 📈 🏠 💾 🦾 |
| [owncast](apps/owncast) | [Owncast](https://owncast.online) · [source](https://github.com/owncast/owncast) | app | 🌐 📈 🏠 💾 🦾 |
| [paperless](apps/paperless) | [Paperless-ngx](https://docs.paperless-ngx.com) · [source](https://github.com/paperless-ngx/paperless-ngx) | app | 🌐 📈 🏠 💾 🦾 |
| [rclone](apps/rclone) | [rclone](https://rclone.org) · [source](https://github.com/rclone/rclone) | app | 🌐 📈 🏠 🦾 |
| [registry](apps/registry) | [Container registry](https://distribution.github.io/distribution/) · [source](https://github.com/distribution/distribution) | app | 🌐 📈 🐝 💾 🦾 |
| [sendan](apps/sendan) | [Sendan](https://github.com/Serraniel/sendan) | app | 🌐 📈 🏠 💾 🦾 |
| [stirling-pdf](apps/stirling-pdf) | [Stirling-PDF](https://www.stirlingpdf.com) · [source](https://github.com/Stirling-Tools/Stirling-PDF) | app | 🌐 📈 🏠 💾 🦾 |
| [sweetfolio](apps/sweetfolio) | [Sweetfolio](https://github.com/Serraniel/Sweetfolio) | app | 🌐 📈 🏠 🐝 🦾 |
| [syncthing](apps/syncthing) | [Syncthing](https://syncthing.net) · [source](https://github.com/syncthing/syncthing) | app | 🌐 📈 🏠 💾 🦾 |
| [tdarr](apps/tdarr) | [Tdarr](https://home.tdarr.io) · [source](https://github.com/HaveAGitGat/Tdarr) | app | 🌐 📈 🏠 💾 🦾 |
| [vaultwarden](apps/vaultwarden) | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | app | 🌐 📈 🏠 🐝 💾 🦾 |

<!-- catalogue:end -->

The table is generated from the templates (`scripts/catalogue.py`); CI keeps it current.

## Automation

- **Validate** runs on every PR. It runs NepFleet's own validator and `docker compose config`, and checks that every pinned tag exists.
- **Validate** also installs every template the way a user does (`scripts/test-templates.py`): `nepfleet new` with test values from each input's type or `scripts/test-values.json`, then a health-gated `nepfleet apply`, then teardown.
- **`index.json`** is the catalogue frontends read (`nepfleet template index .`); CI fails when it is stale.
- **Image updates** runs weekly. It opens an issue when an image publishes a release beyond its template's `track`, usually a new major version.
- **Images** builds `images/*` on change and weekly to pick up base-image fixes, then checks that the image can be pulled without logging in.

## Images

Images built here are published as `ghcr.io/serraniel/nepfleet-<name>`. They are public, so hosts pull them without credentials, and they come with SBOMs and cosign signatures like every NepFleet image. `nepfleet-caddy` is Caddy with caddy-docker-proxy and the DNS-01 providers the `caddy` template offers.

GHCR creates a new package as **private** on its first push, and there is no API to change that. When you add an image under `images/`:

1. Let the **Images** workflow push it once. Its last step fails while the package is private.
2. On GitHub, open the package (profile → Packages → `nepfleet-<name>`) → **Package settings** → **Change visibility** → **Public**. This cannot be undone: GitHub does not let a public package become private again.
3. Re-run the workflow. The anonymous-pull check then passes, and so does the tag check in **Validate**.

The `org.opencontainers.image.source` label links the package to this repository, so it shows up under the repository's packages.

## Using other catalogues

Any git repository with the same layout works. Add it to `fleet.yaml` under `spec.templateSources`.

## Contributing

1. Copy a similar template and change it.
2. Run `nepfleet template validate apps/<name>` and `./scripts/compose-check.sh`.
3. Pin real tags (never `:latest`), add integration labels and set the matching `supports` flags.
4. If the change is breaking for existing installs, bump `spec.version` to the next major version and add a `migrations` entry.

License: AGPL-3.0-or-later.
