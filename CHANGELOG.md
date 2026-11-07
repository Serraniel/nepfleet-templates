# Changelog

## 0.1.0 (2026-11-07)


### ⚠ BREAKING CHANGES

* volume-backup encrypts to the fleet's keys and skips backup: false volumes ([#82](https://github.com/Serraniel/nepfleet-templates/issues/82))

### Features

* Actual Budget template ([#66](https://github.com/Serraniel/nepfleet-templates/issues/66)) ([8d3d257](https://github.com/Serraniel/nepfleet-templates/commit/8d3d25711e94498cf9c6a240c2d2b9741423f94f))
* Audiobookshelf template ([#68](https://github.com/Serraniel/nepfleet-templates/issues/68)) ([4e91b8d](https://github.com/Serraniel/nepfleet-templates/commit/4e91b8d594e10eca438d5fe778df020c6ef5f665))
* backup system templates and Immich, Homebox, Tdarr, Navidrome, MeTube, Open WebUI ([#39](https://github.com/Serraniel/nepfleet-templates/issues/39)) ([336bf5a](https://github.com/Serraniel/nepfleet-templates/commit/336bf5adc627ce11d19783bfe4e1d3d8609a61e2))
* BookStack template ([#63](https://github.com/Serraniel/nepfleet-templates/issues/63)) ([3a65904](https://github.com/Serraniel/nepfleet-templates/commit/3a65904e29158e19545e1f414773a3298c374c28))
* consistent backups for database and SQLite templates ([#40](https://github.com/Serraniel/nepfleet-templates/issues/40)) ([e22e9d9](https://github.com/Serraniel/nepfleet-templates/commit/e22e9d96c6c5067ba142383e1d97ea41e5b5e156))
* dozzle can show logs, and alerts on fatal ones ([#89](https://github.com/Serraniel/nepfleet-templates/issues/89)) ([651b033](https://github.com/Serraniel/nepfleet-templates/commit/651b0337f7d42be16addcab546fa4ba9e41db125))
* fail2ban template (ban repeated failed SSH logins) ([#88](https://github.com/Serraniel/nepfleet-templates/issues/88)) ([0a55b74](https://github.com/Serraniel/nepfleet-templates/commit/0a55b74b18e54baa6e41011a87bb7faa74e1dd18))
* Homepage settings and info widgets as values ([#70](https://github.com/Serraniel/nepfleet-templates/issues/70)) ([bf34389](https://github.com/Serraniel/nepfleet-templates/commit/bf34389dbf62362628408c7f0d7d3241b55624a8))
* initial version ([f648a8d](https://github.com/Serraniel/nepfleet-templates/commit/f648a8d332f85ee267b0e2cd794b5e8b4b3cc886))
* Kuma monitors for databases, caches and workers, grouped per stack ([#84](https://github.com/Serraniel/nepfleet-templates/issues/84)) ([6adfa47](https://github.com/Serraniel/nepfleet-templates/commit/6adfa473131ff2b2e36c02f69ac264197e320c2f))
* Mealie template ([#67](https://github.com/Serraniel/nepfleet-templates/issues/67)) ([99d5411](https://github.com/Serraniel/nepfleet-templates/commit/99d54119e6901a04d0ad3eb593ee3d966cb74b4a))
* n8n template ([#65](https://github.com/Serraniel/nepfleet-templates/issues/65)) ([629fce3](https://github.com/Serraniel/nepfleet-templates/commit/629fce3d2289d5023f6e0d54fe66dc1fc5091e77))
* ntfy template ([#79](https://github.com/Serraniel/nepfleet-templates/issues/79)) ([b8aab57](https://github.com/Serraniel/nepfleet-templates/commit/b8aab577c45100986a305b2d2b26ab8bf96c2128))
* Pi-hole template (DNS ad blocking for the local network) ([#86](https://github.com/Serraniel/nepfleet-templates/issues/86)) ([d2f1814](https://github.com/Serraniel/nepfleet-templates/commit/d2f1814ea0fb410ea5637f3b1e28c328644cd133))
* Stirling-PDF template ([#69](https://github.com/Serraniel/nepfleet-templates/issues/69)) ([ac69b3b](https://github.com/Serraniel/nepfleet-templates/commit/ac69b3bbe0a5e9df229e160f3953bfd305ad6e96))
* Syncthing template ([#71](https://github.com/Serraniel/nepfleet-templates/issues/71)) ([5de4b42](https://github.com/Serraniel/nepfleet-templates/commit/5de4b422118e9f6de7d04e535ca3b4a6fea4f5a4))
* template for AdGuard Home ([#94](https://github.com/Serraniel/nepfleet-templates/issues/94)) ([7742778](https://github.com/Serraniel/nepfleet-templates/commit/77427785d38efe38484da1166d234caead7eb8ad))
* template for Authelia ([#95](https://github.com/Serraniel/nepfleet-templates/issues/95)) ([ab142f1](https://github.com/Serraniel/nepfleet-templates/commit/ab142f11797c3eb1e9c99f67e383345669ef223a))
* template for Matrix with Synapse and Element ([#96](https://github.com/Serraniel/nepfleet-templates/issues/96)) ([771a081](https://github.com/Serraniel/nepfleet-templates/commit/771a081aac5b2c688c6ed530170382d3e19ebf40))
* template for Pocket ID ([#90](https://github.com/Serraniel/nepfleet-templates/issues/90)) ([03c8de0](https://github.com/Serraniel/nepfleet-templates/commit/03c8de0a30cbdd8dd3f6579b4b6b610f799e0728))
* template for the Beszel hub ([#91](https://github.com/Serraniel/nepfleet-templates/issues/91)) ([1bfec89](https://github.com/Serraniel/nepfleet-templates/commit/1bfec89381066b97a61e726bfaaa57a942bb7efa))
* templates for Prometheus and Grafana ([#93](https://github.com/Serraniel/nepfleet-templates/issues/93)) ([cf56dc8](https://github.com/Serraniel/nepfleet-templates/commit/cf56dc824d203ca236816a2b197ef5d828097004))
* templates use ${NEPFLEET_URL} and declare their web UI ([#85](https://github.com/Serraniel/nepfleet-templates/issues/85)) ([9d92dae](https://github.com/Serraniel/nepfleet-templates/commit/9d92daebe6256ef6cba43c1b98b5cc18cae30acc))
* USB sticks for Home Assistant, hardware transcoding for Jellyfin and Tdarr ([#64](https://github.com/Serraniel/nepfleet-templates/issues/64)) ([5f85ca5](https://github.com/Serraniel/nepfleet-templates/commit/5f85ca5f4c7a62f926caa76ac116cb9cccb4b7d1))
* volume-backup encrypts to the fleet's keys and skips backup: false volumes ([#82](https://github.com/Serraniel/nepfleet-templates/issues/82)) ([0111865](https://github.com/Serraniel/nepfleet-templates/commit/0111865f4684f212ee5863e0cf3fae2a3c8b9098))
* VPN egress template (gluetun) for Mullvad and other providers ([#78](https://github.com/Serraniel/nepfleet-templates/issues/78)) ([1f2e36b](https://github.com/Serraniel/nepfleet-templates/commit/1f2e36b98556d18aef0e4a0ed587f2be36a2ea95))
* WireGuard home VPN template (wg-easy) ([#83](https://github.com/Serraniel/nepfleet-templates/issues/83)) ([53f63aa](https://github.com/Serraniel/nepfleet-templates/commit/53f63aa02033307fd175152f2bb4d10dcbae6bba))


### Bug Fixes

* **frps:** do not claim monitoring without kuma labels ([#32](https://github.com/Serraniel/nepfleet-templates/issues/32)) ([c23678a](https://github.com/Serraniel/nepfleet-templates/commit/c23678ad4b68220196299be6b19565ed80eb437a))
* **homebox:** generate the API key pepper Homebox 0.27 requires ([#52](https://github.com/Serraniel/nepfleet-templates/issues/52)) ([c8838a1](https://github.com/Serraniel/nepfleet-templates/commit/c8838a127bf72e0c7e7eae33ea017c43013dfbd3))
* turn off telemetry in Immich ML, Navidrome, Open WebUI and Stirling-PDF ([#73](https://github.com/Serraniel/nepfleet-templates/issues/73)) ([53c7575](https://github.com/Serraniel/nepfleet-templates/commit/53c757577b64ac02a5efaf9e9ed072edf35990d1))
* turn off update checks and crash reports that phone home ([#77](https://github.com/Serraniel/nepfleet-templates/issues/77)) ([dfb0e88](https://github.com/Serraniel/nepfleet-templates/commit/dfb0e8816ce02222a31bc4e115d24786fb5ba44e))


### Dependencies

* Bump home-assistant/home-assistant from 2026.10 to 2026.11 in /apps/homeassistant ([#55](https://github.com/Serraniel/nepfleet-templates/issues/55)) ([838dda0](https://github.com/Serraniel/nepfleet-templates/commit/838dda0e2fcd06c128556074efde4e54d6b3bc1f))
* Bump immich-app/immich-server from v3.3.5 to v3.3.6 in /apps/immich in the templates group across 1 directory ([#54](https://github.com/Serraniel/nepfleet-templates/issues/54)) ([d49073d](https://github.com/Serraniel/nepfleet-templates/commit/d49073d1c14e52a869a4c6644f33f129de85dbc7))
* Bump serraniel/sweetfolio from 0.5.4 to 0.6.0 in /apps/sweetfolio ([#56](https://github.com/Serraniel/nepfleet-templates/issues/56)) ([5efaf82](https://github.com/Serraniel/nepfleet-templates/commit/5efaf82d8896c7f2a59393a8e8e2fc0f7b53c35f))
