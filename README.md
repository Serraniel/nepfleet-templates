# NepFleet templates

The official catalogue of [NepFleet](https://github.com/Serraniel/nepfleet) templates. The format is described in the [template spec](https://github.com/Serraniel/nepfleet/blob/main/docs/spec/template.md).

- `system/`: services NepFleet itself builds on, such as ingress, logs, uptime and tunnels. All of them are opt-in.
- `apps/`: services you run.
- `images/`: images this repository builds, published as `ghcr.io/serraniel/nepfleet-<name>`.

> Templates are validated and every image tag is checked in CI, but they are **not yet integration-tested** ([#integration tests](https://github.com/Serraniel/nepfleet-templates/milestones)). Review them before production use.

## Catalogue

Legend: 🌐 ingress (Caddy) · 📈 monitors (AutoKuma) · 🏠 dashboard (Homepage) · 🐝 swarm-ready · 💾 backup

| Template | Tier | Integrations |
|---|---|---|
| [caddy](system/caddy) | system | 🐝 💾 · public ACME + DNS-01 for home networks |
| [dozzle](system/dozzle) | system | 🌐 📈 🏠 🐝 |
| [uptime-kuma](system/uptime-kuma) | system | 🌐 🏠 🐝 💾 · fleet-wide or per-stack status page |
| [homepage](system/homepage) | system | 🌐 📈 🐝 💾 |
| [neptide](system/neptide) | system | 🐝 · default updater: health-gated, with rollback |
| [watchtower](system/watchtower) | system | alternative, notify-only by default (fork `nickfedor/watchtower`) |
| [binfmt](system/binfmt) | system | run foreign-architecture images |
| [frps](system/frps) / [frpc](system/frpc) | system | 🌐 · expose home services through a public host |
| [forgejo](apps/forgejo) | app | 🌐 📈 🏠 💾 · with an Actions runner in DinD |
| [homeassistant](apps/homeassistant) | app | 🌐 📈 🏠 💾 |
| [jellyfin](apps/jellyfin) | app | 🌐 📈 🏠 💾 |
| [kutt](apps/kutt) | app | 🌐 📈 🏠 💾 |
| [opencloud](apps/opencloud) | app | 🌐 📈 🏠 💾 |
| [owncast](apps/owncast) | app | 🌐 📈 🏠 💾 |
| [paperless](apps/paperless) | app | 🌐 📈 🏠 💾 |
| [rclone](apps/rclone) | app | 🌐 📈 🏠 💾 |
| [registry](apps/registry) | app | 🌐 📈 🐝 💾 |
| [sendan](apps/sendan) | app | 🌐 📈 🏠 💾 |
| [sweetfolio](apps/sweetfolio) | app | 🌐 📈 🏠 🐝 |
| [vaultwarden](apps/vaultwarden) | app | 🌐 📈 🏠 🐝 💾 |

## Automation

- **Validate** runs on every PR. It runs NepFleet's own validator and `docker compose config`, and checks that every pinned tag exists.
- **Image updates** runs weekly. It opens an issue when an image publishes a release beyond its template's `track`, usually a new major version.
- **Images** builds `images/*` on change and weekly to pick up base-image fixes.

## Using other catalogues

Any git repository with the same layout works. Add it to `fleet.yaml` under `spec.templateSources`.

## Contributing

1. Copy a similar template and change it.
2. Run `nepfleet template validate apps/<name>` and `./scripts/compose-check.sh`.
3. Pin real tags (never `:latest`), add integration labels and set the matching `supports` flags.
4. If the change is breaking for existing installs, bump `spec.version` to the next major version and add a `migrations` entry.

License: AGPL-3.0-or-later.
