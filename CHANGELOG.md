# Changelog

## [0.4.0](https://github.com/Serraniel/nepfleet-templates/compare/v0.3.1...v0.4.0) (2026-11-28)


### ⚠ BREAKING CHANGES

* **opencloud:** OpenCloud 9.1, rebuilding the search index ([#290](https://github.com/Serraniel/nepfleet-templates/issues/290))

### Security

* **deps:** bump binwiederhier/ntfy from v2.37.2 to v2.38.0 in /apps/ntfy ([#223](https://github.com/Serraniel/nepfleet-templates/issues/223)) ([a0a7196](https://github.com/Serraniel/nepfleet-templates/commit/a0a71961ac10ff4ae450b1ed9d2fe2983c5f2fba))
* **sendan:** update to 0.4.0 ([#214](https://github.com/Serraniel/nepfleet-templates/issues/214)) ([faae0de](https://github.com/Serraniel/nepfleet-templates/commit/faae0dea2261936575fdc65b537c3dcb4945faed))


### Features

* **apps:** forgejo, mastodon and sure use the fleet's mail settings ([#292](https://github.com/Serraniel/nepfleet-templates/issues/292)) ([aaed0cd](https://github.com/Serraniel/nepfleet-templates/commit/aaed0cd0f1fb21696d7d7c7336cd86d1a67e165f))
* **apps:** mastodon and sure follow the fleet's mail TLS mode ([#293](https://github.com/Serraniel/nepfleet-templates/issues/293)) ([dd702b8](https://github.com/Serraniel/nepfleet-templates/commit/dd702b8ed78c46aae09e66f4b65c7ac9e97d7fe5))
* **apps:** open-webui and mealie sign in through the stack's sign-on ([#296](https://github.com/Serraniel/nepfleet-templates/issues/296)) ([e18e2e4](https://github.com/Serraniel/nepfleet-templates/commit/e18e2e417163f8a73c5aaf955045320fbd0b7087))
* **apps:** paperless, mastodon and matrix sign in through the stack's sign-on ([#297](https://github.com/Serraniel/nepfleet-templates/issues/297)) ([2fe08d1](https://github.com/Serraniel/nepfleet-templates/commit/2fe08d101e04aea71e2c69676a196ae89664c1e7))
* **apps:** sure and forgejo use the stack's sign-on ([#295](https://github.com/Serraniel/nepfleet-templates/issues/295)) ([101370c](https://github.com/Serraniel/nepfleet-templates/commit/101370c903c4480fef7d360ee173ba3d1241254e))
* **apps:** vaultwarden and homebox sign in through the stack's sign-on ([#294](https://github.com/Serraniel/nepfleet-templates/issues/294)) ([8368054](https://github.com/Serraniel/nepfleet-templates/commit/8368054f555dd594ca5be06009c2db491e72782b))
* **beszel-agent:** pair with a hub in the fleet by itself ([#285](https://github.com/Serraniel/nepfleet-templates/issues/285)) ([3383831](https://github.com/Serraniel/nepfleet-templates/commit/33838319be93b6809edacf1860f0bed79b1b56be))
* bot check paths for matrix, n8n, stirling-pdf, pihole and adguard-home ([#192](https://github.com/Serraniel/nepfleet-templates/issues/192)) ([221b831](https://github.com/Serraniel/nepfleet-templates/commit/221b83162cd3f87c0376111eb7b1f5ea523106f4))
* bot check paths for the remaining web apps ([#216](https://github.com/Serraniel/nepfleet-templates/issues/216)) ([5188f23](https://github.com/Serraniel/nepfleet-templates/commit/5188f231d471ffa2a96d658b9af69eafb2072a17))
* **caddy:** keep the sites' DNS records pointed at the host ([#182](https://github.com/Serraniel/nepfleet-templates/issues/182)) ([518c82e](https://github.com/Serraniel/nepfleet-templates/commit/518c82ecbca69df704fe2d261a71f4a3548933c5))
* **caddy:** token help for the selected DNS provider only ([#188](https://github.com/Serraniel/nepfleet-templates/issues/188)) ([5ca054f](https://github.com/Serraniel/nepfleet-templates/commit/5ca054fac836694cd7feb66aa91bc1f600ee381f))
* dashboard tiles say what each app is ([#231](https://github.com/Serraniel/nepfleet-templates/issues/231)) ([2c8f379](https://github.com/Serraniel/nepfleet-templates/commit/2c8f37920d3cd835573a216d16d2d10d07668709))
* **dozzle:** alerts go to NepFleet's own API with the stack's token ([#185](https://github.com/Serraniel/nepfleet-templates/issues/185)) ([34daeb8](https://github.com/Serraniel/nepfleet-templates/commit/34daeb8055059bf333a399e616cc6677326ee056))
* neptide, Watchtower and volume backups notify through NepFleet ([#186](https://github.com/Serraniel/nepfleet-templates/issues/186)) ([b56fbce](https://github.com/Serraniel/nepfleet-templates/commit/b56fbcecd4efecbb1ed41211634b50ab898dfe05))
* **neptide:** the docker group ID comes from the host ([#183](https://github.com/Serraniel/nepfleet-templates/issues/183)) ([9f0b39e](https://github.com/Serraniel/nepfleet-templates/commit/9f0b39e90916aea8aecd0343c2dbe747834156eb))
* **openclaw:** onboard without prompts, model provider and Telegram from inputs ([#291](https://github.com/Serraniel/nepfleet-templates/issues/291)) ([2dd2869](https://github.com/Serraniel/nepfleet-templates/commit/2dd2869b2bf3f14b2f7646a0d05c68014b7918ba))
* **opencloud:** OpenCloud 9.1, rebuilding the search index ([#290](https://github.com/Serraniel/nepfleet-templates/issues/290)) ([572bfe0](https://github.com/Serraniel/nepfleet-templates/commit/572bfe00afb6949f74977f32697de78cc19663ba))
* swarm support for eight more apps ([#196](https://github.com/Serraniel/nepfleet-templates/issues/196)) ([f476caa](https://github.com/Serraniel/nepfleet-templates/commit/f476caa8c1e984c8afb542396ceeb5fd6af10827))
* swarm support for immich, mastodon, sure and mealie ([#195](https://github.com/Serraniel/nepfleet-templates/issues/195)) ([f6ef179](https://github.com/Serraniel/nepfleet-templates/commit/f6ef179ba758535a63fc35105a001e1ece4ca6f4))
* swarm support for n8n, bookstack, matrix and paperless ([#194](https://github.com/Serraniel/nepfleet-templates/issues/194)) ([7cd061f](https://github.com/Serraniel/nepfleet-templates/commit/7cd061f5c932fb3c078cf8bf3d7b6f4ccd7ac08e))
* swarm support for open-webui, sweetcaptcha, owncast, garage and openclaw ([#198](https://github.com/Serraniel/nepfleet-templates/issues/198)) ([70d2b32](https://github.com/Serraniel/nepfleet-templates/commit/70d2b320ed32fcf2da8899a408f3b06ba725ff3c))
* template for imgproxy ([#211](https://github.com/Serraniel/nepfleet-templates/issues/211)) ([c7856a7](https://github.com/Serraniel/nepfleet-templates/commit/c7856a78d257e5ed6f6718a8aa014816fd8c9866))
* template for OpenBao ([#212](https://github.com/Serraniel/nepfleet-templates/issues/212)) ([f762c76](https://github.com/Serraniel/nepfleet-templates/commit/f762c767365b6520ca737a4ecfaa6243b4d18496))
* template for RabbitMQ ([#210](https://github.com/Serraniel/nepfleet-templates/issues/210)) ([d632e06](https://github.com/Serraniel/nepfleet-templates/commit/d632e06db1d82fcad18adb5e52bd2924ff0c960c))
* **uptime-kuma:** monitors alert through NepFleet's channels ([#187](https://github.com/Serraniel/nepfleet-templates/issues/187)) ([542ce6c](https://github.com/Serraniel/nepfleet-templates/commit/542ce6c1660c367e5c11b775d47b3d91fe996c33))
* **uptime-kuma:** set up Kuma on its first start, so AutoKuma connects ([#184](https://github.com/Serraniel/nepfleet-templates/issues/184)) ([6c006b1](https://github.com/Serraniel/nepfleet-templates/commit/6c006b1bc2530073ae0339a00589386aec3d01ad))


### Bug Fixes

* **actual:** set the server password inside the app container ([#266](https://github.com/Serraniel/nepfleet-templates/issues/266)) ([40bed3e](https://github.com/Serraniel/nepfleet-templates/commit/40bed3e08bda006eed3acec2651ca6153a5ab1d3))
* **actual:** the server password from the stack's inputs ([#238](https://github.com/Serraniel/nepfleet-templates/issues/238)) ([58cb5fc](https://github.com/Serraniel/nepfleet-templates/commit/58cb5fc37741f7c99d7a9294fee6a51b35c0eda8))
* **adguard-home:** set up from the stack's inputs, no wizard ([#242](https://github.com/Serraniel/nepfleet-templates/issues/242)) ([be0d4d7](https://github.com/Serraniel/nepfleet-templates/commit/be0d4d7ffde496f5db333a6bb9b99b9b90f9def8))
* apps create their admin from the stack's inputs ([#229](https://github.com/Serraniel/nepfleet-templates/issues/229)) ([a16da0d](https://github.com/Serraniel/nepfleet-templates/commit/a16da0d24ed04affbb754785e349714324d7e3a2))
* **audiobookshelf:** the root user from the stack's inputs ([#240](https://github.com/Serraniel/nepfleet-templates/issues/240)) ([2e13b26](https://github.com/Serraniel/nepfleet-templates/commit/2e13b26b5a44874a609252831a8c82fd73df2667))
* **authelia:** an admin from the stack's inputs, 2FA setup without docker exec ([#249](https://github.com/Serraniel/nepfleet-templates/issues/249)) ([109df11](https://github.com/Serraniel/nepfleet-templates/commit/109df11ea5572b4be4976f88044e66c66711b402))
* **backrest:** an admin from the stack's inputs ([#246](https://github.com/Serraniel/nepfleet-templates/issues/246)) ([d61db1a](https://github.com/Serraniel/nepfleet-templates/commit/d61db1a59afa1dc862ffef4b70e4066852ee90d2))
* **bookstack:** an admin from the stack's inputs ([#233](https://github.com/Serraniel/nepfleet-templates/issues/233)) ([81360b4](https://github.com/Serraniel/nepfleet-templates/commit/81360b468ec0a2b3e9cc2640fe6646f13f5b9443))
* **caddy:** allow /info on its socket proxy, for the Swarm check ([#179](https://github.com/Serraniel/nepfleet-templates/issues/179)) ([558ff32](https://github.com/Serraniel/nepfleet-templates/commit/558ff3249e1bcfe4caa299fc095457aa83c05f5f))
* **ci:** a floating tag isn't behind the releases it follows ([#213](https://github.com/Serraniel/nepfleet-templates/issues/213)) ([9a7e6fa](https://github.com/Serraniel/nepfleet-templates/commit/9a7e6fac23a4338bdaffb9522e5c53af01de0103))
* **dozzle:** an admin user to sign in with ([#226](https://github.com/Serraniel/nepfleet-templates/issues/226)) ([d18b315](https://github.com/Serraniel/nepfleet-templates/commit/d18b315506e3a83061c9bd978997736821d1a352))
* **dozzle:** wait until its socket proxy answers ([#265](https://github.com/Serraniel/nepfleet-templates/issues/265)) ([51bb3ad](https://github.com/Serraniel/nepfleet-templates/commit/51bb3ad8b6d160295fbfab5baa4669a27b7a82dd))
* **forgejo:** an admin from the stack's inputs ([#232](https://github.com/Serraniel/nepfleet-templates/issues/232)) ([74c34d6](https://github.com/Serraniel/nepfleet-templates/commit/74c34d6a81f8cbffbae35d59646be7550c76c6bd))
* **hermes-agent:** nobody but the listed users, and say so ([#284](https://github.com/Serraniel/nepfleet-templates/issues/284)) ([e95d005](https://github.com/Serraniel/nepfleet-templates/commit/e95d0050db8249ee8f81e7c3eb6c7f82188fe955))
* **homeassistant:** an owner from the stack's inputs, and Caddy trusted ([#247](https://github.com/Serraniel/nepfleet-templates/issues/247)) ([88cebc6](https://github.com/Serraniel/nepfleet-templates/commit/88cebc6b8323f3edfdcdef3d60864c5023a0e13f))
* **homebox:** the admin from the stack's inputs, registration closed ([#237](https://github.com/Serraniel/nepfleet-templates/issues/237)) ([f6bb982](https://github.com/Serraniel/nepfleet-templates/commit/f6bb982bcdff34843f0064f29c856bafdbb5c207))
* **homepage:** list swarm stacks' services on the dashboard ([#263](https://github.com/Serraniel/nepfleet-templates/issues/263)) ([78eb7b2](https://github.com/Serraniel/nepfleet-templates/commit/78eb7b2e49d126dbdd43aec01dc625154240f69f))
* **homepage:** no sample groups and bookmarks ([#230](https://github.com/Serraniel/nepfleet-templates/issues/230)) ([dc5d5f0](https://github.com/Serraniel/nepfleet-templates/commit/dc5d5f04d1a9da35d952a1883980ede78cd93d28))
* **immich:** an admin from the stack's inputs, ML on the server's version ([#234](https://github.com/Serraniel/nepfleet-templates/issues/234)) ([87e675e](https://github.com/Serraniel/nepfleet-templates/commit/87e675e9f5e4b1960c6ac72b288f5d5ef4afbf7a))
* **jellyfin:** an admin from the stack's inputs, no open startup wizard ([#236](https://github.com/Serraniel/nepfleet-templates/issues/236)) ([07acfe7](https://github.com/Serraniel/nepfleet-templates/commit/07acfe7a3726c21fc8ae983472c4cf35d3d7de5a))
* **kutt:** an admin from the stack's inputs ([#241](https://github.com/Serraniel/nepfleet-templates/issues/241)) ([9f4bfbf](https://github.com/Serraniel/nepfleet-templates/commit/9f4bfbf174be2a4f6657e0e808604ce04a8da082))
* **mastodon:** an owner account from the stack's inputs and push keys made once ([#250](https://github.com/Serraniel/nepfleet-templates/issues/250)) ([529dab2](https://github.com/Serraniel/nepfleet-templates/commit/529dab25e1f331060175a597222c62664635014c))
* **matrix:** an admin from the stack's inputs ([#243](https://github.com/Serraniel/nepfleet-templates/issues/243)) ([539124d](https://github.com/Serraniel/nepfleet-templates/commit/539124dc2947d017ac067045eeb5338a659b8322))
* **mealie:** an admin from the stack's inputs ([#239](https://github.com/Serraniel/nepfleet-templates/issues/239)) ([0471baf](https://github.com/Serraniel/nepfleet-templates/commit/0471baff8d8997b8b256051cb55f9ec23bf4d8f9))
* **metube:** a sign-in in front of MeTube ([#251](https://github.com/Serraniel/nepfleet-templates/issues/251)) ([f13624c](https://github.com/Serraniel/nepfleet-templates/commit/f13624c552665e06181913e6e322a0aaba684b8c))
* **open-webui:** models to chat with after install ([#262](https://github.com/Serraniel/nepfleet-templates/issues/262)) ([ac9dda3](https://github.com/Serraniel/nepfleet-templates/commit/ac9dda3bca2760d7bf411b30560e0fa27026e44d))
* **openbao:** initialise and unseal itself, an admin from the stack's inputs ([#248](https://github.com/Serraniel/nepfleet-templates/issues/248)) ([08291fd](https://github.com/Serraniel/nepfleet-templates/commit/08291fd1a4aed4fcb6335d7b884ecad4eea3e588))
* **opencloud:** the browser may show the Euro-Office editor ([#261](https://github.com/Serraniel/nepfleet-templates/issues/261)) ([f9a7bd1](https://github.com/Serraniel/nepfleet-templates/commit/f9a7bd18b33de5c144b0da3fb256d31a539fc3c0))
* passwords and keys you need are inputs, not generated ([#228](https://github.com/Serraniel/nepfleet-templates/issues/228)) ([458af2c](https://github.com/Serraniel/nepfleet-templates/commit/458af2c7a532731841b00cb3a1266240e9fbdbc2))
* **pocket-id:** an admin from the stack's inputs, /setup closed ([#244](https://github.com/Serraniel/nepfleet-templates/issues/244)) ([93be418](https://github.com/Serraniel/nepfleet-templates/commit/93be418ffeb4b8afcd9a87fe58840ba2c8a52c56))
* **rclone:** run the web GUI with rclone gui, as 1.76 requires ([#217](https://github.com/Serraniel/nepfleet-templates/issues/217)) ([5ee0aec](https://github.com/Serraniel/nepfleet-templates/commit/5ee0aeca05fc1fd45e47aeeaf85bf6451846191b))
* **sure:** ask for the admin e-mail instead of a placeholder ([#267](https://github.com/Serraniel/nepfleet-templates/issues/267)) ([ad560ae](https://github.com/Serraniel/nepfleet-templates/commit/ad560aefdbf2173b4a12059f8a76cb1c6fcd224e))
* **sure:** the first account from the stack's inputs, sign-up closed ([#235](https://github.com/Serraniel/nepfleet-templates/issues/235)) ([df0322d](https://github.com/Serraniel/nepfleet-templates/commit/df0322d4c4bfb6f2fb1330114d0aa2ea7d98fc35))
* **syncthing:** create DATA_PATH and give it to PUID:PGID ([#252](https://github.com/Serraniel/nepfleet-templates/issues/252)) ([13ee7ef](https://github.com/Serraniel/nepfleet-templates/commit/13ee7ef55694eb3d076c1b15d38ce126b6bc2f7a))
* update metadata so templates keep updating by themselves ([#283](https://github.com/Serraniel/nepfleet-templates/issues/283)) ([60a0714](https://github.com/Serraniel/nepfleet-templates/commit/60a0714273333ac822f99e4df30f8cf9d57ca5d8))
* **uptime-kuma:** the admin always matches the stack's inputs ([#255](https://github.com/Serraniel/nepfleet-templates/issues/255)) ([a26fe85](https://github.com/Serraniel/nepfleet-templates/commit/a26fe85d5c3353c4b7c120d6de7b7756a88d0623))
* **vaultwarden:** the owner's account from the stack's inputs ([#245](https://github.com/Serraniel/nepfleet-templates/issues/245)) ([84968d5](https://github.com/Serraniel/nepfleet-templates/commit/84968d56cb2f7987257377522483a597b590899b))


### Dependencies

* **adguard-home:** update to v1.0.0 ([#287](https://github.com/Serraniel/nepfleet-templates/issues/287)) ([64e82be](https://github.com/Serraniel/nepfleet-templates/commit/64e82be2c45b0d839e7f3cc72939fb25749445ce))
* Bump advplyr/audiobookshelf from 2.37.2 to 2.38.0 in /apps/audiobookshelf ([#221](https://github.com/Serraniel/nepfleet-templates/issues/221)) ([1467af9](https://github.com/Serraniel/nepfleet-templates/commit/1467af983c1a455e860f12b8ca1e572ef96a7b95))
* Bump apache/tika from 3.3.3.0 to 3.3.3.1 in /apps/paperless ([#299](https://github.com/Serraniel/nepfleet-templates/issues/299)) ([237e1b3](https://github.com/Serraniel/nepfleet-templates/commit/237e1b392e97b4be7063dc5455912b6a71be6cc0))
* Bump caddy from `345264d` to `345264d` in /images/caddy ([#219](https://github.com/Serraniel/nepfleet-templates/issues/219)) ([4a48215](https://github.com/Serraniel/nepfleet-templates/commit/4a48215dc1f5c3a019c21a09ac74881e5f83e765))
* Bump caddy from `345264d` to `f9beaa5` in /images/caddy ([#253](https://github.com/Serraniel/nepfleet-templates/issues/253)) ([5350d6d](https://github.com/Serraniel/nepfleet-templates/commit/5350d6de6108ac2f1aa3ef7176364e4197321809))
* Bump caddy from `3fddbec` to `345264d` in /images/caddy ([#199](https://github.com/Serraniel/nepfleet-templates/issues/199)) ([62dd411](https://github.com/Serraniel/nepfleet-templates/commit/62dd41181e1d28b63651786928f8d9d4682d90d3))
* Bump caddy from `f9beaa5` to `cda07fe` in /images/caddy ([#303](https://github.com/Serraniel/nepfleet-templates/issues/303)) ([d8a4169](https://github.com/Serraniel/nepfleet-templates/commit/d8a41693b710c26eb9183a965d774ec5c9a29df2))
* Bump gotenberg/gotenberg from 9.3.0 to 9.4.1 in /apps/paperless ([#203](https://github.com/Serraniel/nepfleet-templates/issues/203)) ([f21ac1c](https://github.com/Serraniel/nepfleet-templates/commit/f21ac1cb61e66dc1cfe91c21744cf3378f82fe2e))
* Bump gotenberg/gotenberg from 9.4.1 to 9.7.0 in /apps/paperless ([#257](https://github.com/Serraniel/nepfleet-templates/issues/257)) ([2c2f088](https://github.com/Serraniel/nepfleet-templates/commit/2c2f088790d4381e0ab0c6993e049015eb36f8dd))
* Bump gotenberg/gotenberg from 9.7.0 to 9.9.0 in /apps/paperless ([#269](https://github.com/Serraniel/nepfleet-templates/issues/269)) ([021f6ea](https://github.com/Serraniel/nepfleet-templates/commit/021f6ea85a3d3068a71fcbff551bc56ddfe348b7))
* Bump haveagitgat/tdarr from 3.07.00 to 3.08.00 in /apps/tdarr ([#258](https://github.com/Serraniel/nepfleet-templates/issues/258)) ([9e257b0](https://github.com/Serraniel/nepfleet-templates/commit/9e257b07fabaccef92f1846496dbc93aa8e29e70))
* Bump haveagitgat/tdarr from 3.08.00 to 3.09.00 in /apps/tdarr ([#271](https://github.com/Serraniel/nepfleet-templates/issues/271)) ([b0cd685](https://github.com/Serraniel/nepfleet-templates/commit/b0cd6856ed335c24dadfa0c9ee34040b2dbca9ce))
* Bump haveagitgat/tdarr from 3.09.00 to 3.10.00 in /apps/tdarr ([#301](https://github.com/Serraniel/nepfleet-templates/issues/301)) ([9d26371](https://github.com/Serraniel/nepfleet-templates/commit/9d2637118427d78832712a9e1897a61d6dad6011))
* Bump haveagitgat/tdarr_node from 3.07.00 to 3.08.00 in /apps/tdarr-node ([#259](https://github.com/Serraniel/nepfleet-templates/issues/259)) ([4e9b082](https://github.com/Serraniel/nepfleet-templates/commit/4e9b08233d0c2b0578c6ef507934ef680eb16b96))
* Bump haveagitgat/tdarr_node from 3.08.00 to 3.09.00 in /apps/tdarr-node ([#272](https://github.com/Serraniel/nepfleet-templates/issues/272)) ([394df02](https://github.com/Serraniel/nepfleet-templates/commit/394df02a0c066b7d07148a16ec8c231a97641996))
* Bump haveagitgat/tdarr_node from 3.09.00 to 3.10.00 in /apps/tdarr-node ([#302](https://github.com/Serraniel/nepfleet-templates/issues/302)) ([ffd979b](https://github.com/Serraniel/nepfleet-templates/commit/ffd979baef4098c4a1884d747742a78bd08818d0))
* Bump immich-power-tools/immich-power-tools from 0.25.0 to v0.26.0 in /apps/immich ([#222](https://github.com/Serraniel/nepfleet-templates/issues/222)) ([f4d22ac](https://github.com/Serraniel/nepfleet-templates/commit/f4d22acb5541badaca9392aacef3c80f2d633954))
* Bump matrixdotorg/synapse from v1.164.2 to v1.165.0 in /apps/matrix ([#201](https://github.com/Serraniel/nepfleet-templates/issues/201)) ([9171ef9](https://github.com/Serraniel/nepfleet-templates/commit/9171ef994432e13725335ff3b1d211e560f964e3))
* Bump mealie-recipes/mealie from v3.30.0 to v3.31.0 in /apps/mealie ([#202](https://github.com/Serraniel/nepfleet-templates/issues/202)) ([4ef5ff4](https://github.com/Serraniel/nepfleet-templates/commit/4ef5ff4d298c1ca3cfafe6f7ffe5e3b0a0efaf53))
* Bump paperless-ngx/paperless-ngx from 3.4 to 3.5 in /apps/paperless ([#224](https://github.com/Serraniel/nepfleet-templates/issues/224)) ([2a349de](https://github.com/Serraniel/nepfleet-templates/commit/2a349de24b1b6386877646133b3ea59038e794b7))
* Bump pihole/pihole from 2026.10.1 to 2026.11.0 in /apps/pihole ([#204](https://github.com/Serraniel/nepfleet-templates/issues/204)) ([bbbd3dc](https://github.com/Serraniel/nepfleet-templates/commit/bbbd3dccff384e5873ab377af47edf787b4eba68))
* Bump serraniel/wokko from 0.3.0 to 0.5.0 in /apps/wokko ([#260](https://github.com/Serraniel/nepfleet-templates/issues/260)) ([f9abb38](https://github.com/Serraniel/nepfleet-templates/commit/f9abb3847562985ef90fb32a506f8adbe902bc05))
* Bump stirlingtools/stirling-pdf from 3.3.0 to 3.4.0 in /apps/stirling-pdf ([#270](https://github.com/Serraniel/nepfleet-templates/issues/270)) ([7b0b703](https://github.com/Serraniel/nepfleet-templates/commit/7b0b703877e7e8890097628168da8082ea90f61a))
* Bump stirlingtools/stirling-pdf from 3.4.0 to 3.5.0 in /apps/stirling-pdf ([#300](https://github.com/Serraniel/nepfleet-templates/issues/300)) ([7507d99](https://github.com/Serraniel/nepfleet-templates/commit/7507d99384ecce79c8448dcfe32f91bbe58636af))
* Bump the templates group across 12 directories with 7 updates ([#256](https://github.com/Serraniel/nepfleet-templates/issues/256)) ([2143f78](https://github.com/Serraniel/nepfleet-templates/commit/2143f78b1543bcd18ecb0b2deee1539f97633fa6))
* Bump the templates group across 4 directories with 4 updates ([#268](https://github.com/Serraniel/nepfleet-templates/issues/268)) ([4685c15](https://github.com/Serraniel/nepfleet-templates/commit/4685c15ba7c1d5c55fb1a85cc5129df03bd823f9))
* Bump the templates group across 4 directories with 5 updates ([#225](https://github.com/Serraniel/nepfleet-templates/issues/225)) ([c807dee](https://github.com/Serraniel/nepfleet-templates/commit/c807dee699baf9c43952cbb896676ef3607b78e3))
* Bump the templates group across 7 directories with 8 updates ([#298](https://github.com/Serraniel/nepfleet-templates/issues/298)) ([ce12681](https://github.com/Serraniel/nepfleet-templates/commit/ce12681d42f1cafa0a91cbc2c4e5e9bbc6c9af61))
* Bump the templates group across 9 directories with 10 updates ([#209](https://github.com/Serraniel/nepfleet-templates/issues/209)) ([b2d3607](https://github.com/Serraniel/nepfleet-templates/commit/b2d360713560483c3915104208207b63a6f0fc8f))
* **n8n:** update to 2.49.1, the last step before 3.x ([#215](https://github.com/Serraniel/nepfleet-templates/issues/215)) ([1ce7708](https://github.com/Serraniel/nepfleet-templates/commit/1ce7708423c8ed7d90fab2210fa0c429d0ff7632))

## [0.3.1](https://github.com/Serraniel/nepfleet-templates/compare/v0.3.0...v0.3.1) (2026-11-14)


### Bug Fixes

* Postgres templates are healthy only once the database answers over TCP ([#175](https://github.com/Serraniel/nepfleet-templates/issues/175)) ([e724d8a](https://github.com/Serraniel/nepfleet-templates/commit/e724d8a40cb94474ad77a98274244c74716a80bf))

## [0.3.0](https://github.com/Serraniel/nepfleet-templates/compare/v0.2.0...v0.3.0) (2026-11-14)


### Features

* **caddy:** say what the DNS API token needs at each provider ([#171](https://github.com/Serraniel/nepfleet-templates/issues/171)) ([9b2fa28](https://github.com/Serraniel/nepfleet-templates/commit/9b2fa284f8f1342fddde869b21f061ba5031c479))

## [0.2.0](https://github.com/Serraniel/nepfleet-templates/compare/v0.1.0...v0.2.0) (2026-11-13)


### Features

* **caddy:** one wildcard certificate for a home domain ([#157](https://github.com/Serraniel/nepfleet-templates/issues/157)) ([a3f8afe](https://github.com/Serraniel/nepfleet-templates/commit/a3f8afe4d63fbca848dee30c433eba27c8c1422e))
* **homebox:** label maker settings and a shared labels volume ([#137](https://github.com/Serraniel/nepfleet-templates/issues/137)) ([e400979](https://github.com/Serraniel/nepfleet-templates/commit/e400979151b5cb63d42946710d78a364b63f5e45))
* **pihole:** answer the home domain with the server's address ([#158](https://github.com/Serraniel/nepfleet-templates/issues/158)) ([a4d81a7](https://github.com/Serraniel/nepfleet-templates/commit/a4d81a7851a8c462653a0b6efb296f2f0f37b352))
* Sure template (personal finance) ([#160](https://github.com/Serraniel/nepfleet-templates/issues/160)) ([9911698](https://github.com/Serraniel/nepfleet-templates/commit/99116989e77657a2083bb8b1bc1c51ad49e370e3))
* tdarr-node template for workers on other hosts ([#136](https://github.com/Serraniel/nepfleet-templates/issues/136)) ([d74ab4a](https://github.com/Serraniel/nepfleet-templates/commit/d74ab4a524612c26258eb0923d0b06a2930c36c7))


### Bug Fixes

* **binfmt:** say what registers the emulators after a reboot ([#135](https://github.com/Serraniel/nepfleet-templates/issues/135)) ([c2fd72f](https://github.com/Serraniel/nepfleet-templates/commit/c2fd72f95c6418304105b60771cf768c9c822761))


### Dependencies

* Bump caddy from 2.11.7-alpine to 2.11.9-alpine in /images/caddy ([#139](https://github.com/Serraniel/nepfleet-templates/issues/139)) ([63b7b21](https://github.com/Serraniel/nepfleet-templates/commit/63b7b2167b4430218b3bb8748e6485224eecf493))
* Bump fatedier/frpc from v0.71.1 to v0.72.0 in /system/frpc ([#126](https://github.com/Serraniel/nepfleet-templates/issues/126)) ([066e498](https://github.com/Serraniel/nepfleet-templates/commit/066e498b65237edb7eb1d7ae7fde36d12366466b))
* Bump fatedier/frps from v0.71.1 to v0.72.0 in /system/frps ([#127](https://github.com/Serraniel/nepfleet-templates/issues/127)) ([6a4792d](https://github.com/Serraniel/nepfleet-templates/commit/6a4792dda2ddcf90ad779f681e766a6c8bfa9eb7))
* Bump gotenberg/gotenberg from 9.1.0 to 9.2.0 in /apps/paperless ([#153](https://github.com/Serraniel/nepfleet-templates/issues/153)) ([1bf8337](https://github.com/Serraniel/nepfleet-templates/commit/1bf8337b266b83106f5b0b58727e830e2900f697))
* Bump gotenberg/gotenberg from 9.2.0 to 9.3.0 in /apps/paperless ([#156](https://github.com/Serraniel/nepfleet-templates/issues/156)) ([ca24fe8](https://github.com/Serraniel/nepfleet-templates/commit/ca24fe884bf8043850a23dabf63055f3d14449c5))
* Bump haveagitgat/tdarr from 3.06.00 to 3.07.00 in /apps/tdarr ([#146](https://github.com/Serraniel/nepfleet-templates/issues/146)) ([2c9ee5c](https://github.com/Serraniel/nepfleet-templates/commit/2c9ee5c8ff5635b32b19ae0cf522e9b465bd4952))
* Bump haveagitgat/tdarr_node from 3.06.00 to 3.07.00 in /apps/tdarr-node ([#154](https://github.com/Serraniel/nepfleet-templates/issues/154)) ([ae04eb8](https://github.com/Serraniel/nepfleet-templates/commit/ae04eb80abdbfaa5c39f29f44d75f381369b01a0))
* Bump immich-app/immich-server from v3.3.6 to v3.4.1 in /apps/immich ([#152](https://github.com/Serraniel/nepfleet-templates/issues/152)) ([1d9ec4b](https://github.com/Serraniel/nepfleet-templates/commit/1d9ec4b8abb8461ddd6f1ff45364a72743b5d4c6))
* Bump linuxserver/bookstack from 26.09.2 to 26.09.3 in /apps/bookstack in the templates group across 1 directory ([#151](https://github.com/Serraniel/nepfleet-templates/issues/151)) ([6be79d9](https://github.com/Serraniel/nepfleet-templates/commit/6be79d9a64ed599caf3a9a28a1f5c65a9bc5061a))
* Bump n8nio/n8n from 2.46.6 to 2.47.2 in /apps/n8n ([#144](https://github.com/Serraniel/nepfleet-templates/issues/144)) ([7d2acd9](https://github.com/Serraniel/nepfleet-templates/commit/7d2acd9297062770a291752cff6de5547ce6d1be))
* Bump prometheus/node-exporter from v1.10.2 to v1.12.1 in /system/prometheus ([#128](https://github.com/Serraniel/nepfleet-templates/issues/128)) ([b16d2bf](https://github.com/Serraniel/nepfleet-templates/commit/b16d2bf74d05dbb6c3c81a7296c3e48cb0c2f7f3))
* Bump rclone/rclone from 1.75 to 1.76 in /apps/rclone ([#145](https://github.com/Serraniel/nepfleet-templates/issues/145)) ([7385870](https://github.com/Serraniel/nepfleet-templates/commit/73858701446c16eeb40233eda389d4153147b6e8))
* Bump the templates group across 2 directories with 2 updates ([#142](https://github.com/Serraniel/nepfleet-templates/issues/142)) ([9a6131a](https://github.com/Serraniel/nepfleet-templates/commit/9a6131adb74d68d5e2f546a939f5b96b59b4f459))
* Bump the templates group across 2 directories with 2 updates ([#155](https://github.com/Serraniel/nepfleet-templates/issues/155)) ([77fd0f4](https://github.com/Serraniel/nepfleet-templates/commit/77fd0f4e749eaacae4679a502d5c91d092fff8b4))
* Bump the templates group across 4 directories with 5 updates ([#140](https://github.com/Serraniel/nepfleet-templates/issues/140)) ([b4f334a](https://github.com/Serraniel/nepfleet-templates/commit/b4f334a0677ca985f596cc8b1ca55db15a9c2180))

## 0.1.0 (2026-11-08)


### ⚠ BREAKING CHANGES

* volume-backup encrypts to the fleet's keys and skips backup: false volumes ([#82](https://github.com/Serraniel/nepfleet-templates/issues/82))

### Features

* Actual Budget template ([#66](https://github.com/Serraniel/nepfleet-templates/issues/66)) ([8d3d257](https://github.com/Serraniel/nepfleet-templates/commit/8d3d25711e94498cf9c6a240c2d2b9741423f94f))
* Audiobookshelf template ([#68](https://github.com/Serraniel/nepfleet-templates/issues/68)) ([4e91b8d](https://github.com/Serraniel/nepfleet-templates/commit/4e91b8d594e10eca438d5fe778df020c6ef5f665))
* backup system templates and Immich, Homebox, Tdarr, Navidrome, MeTube, Open WebUI ([#39](https://github.com/Serraniel/nepfleet-templates/issues/39)) ([336bf5a](https://github.com/Serraniel/nepfleet-templates/commit/336bf5adc627ce11d19783bfe4e1d3d8609a61e2))
* BookStack template ([#63](https://github.com/Serraniel/nepfleet-templates/issues/63)) ([3a65904](https://github.com/Serraniel/nepfleet-templates/commit/3a65904e29158e19545e1f414773a3298c374c28))
* bot check paths for vaultwarden, mastodon and opencloud ([#116](https://github.com/Serraniel/nepfleet-templates/issues/116)) ([55ec62f](https://github.com/Serraniel/nepfleet-templates/commit/55ec62fc804ecd12801b28734bebf40ce3074740))
* consistent backups for database and SQLite templates ([#40](https://github.com/Serraniel/nepfleet-templates/issues/40)) ([e22e9d9](https://github.com/Serraniel/nepfleet-templates/commit/e22e9d96c6c5067ba142383e1d97ea41e5b5e156))
* dozzle can show logs, and alerts on fatal ones ([#89](https://github.com/Serraniel/nepfleet-templates/issues/89)) ([651b033](https://github.com/Serraniel/nepfleet-templates/commit/651b0337f7d42be16addcab546fa4ba9e41db125))
* dozzle sends log alerts to NepFleet's alerts API ([#115](https://github.com/Serraniel/nepfleet-templates/issues/115)) ([90d0464](https://github.com/Serraniel/nepfleet-templates/commit/90d046414cfba04aa57dba1b9168ab954fb45bb5))
* fail2ban template (ban repeated failed SSH logins) ([#88](https://github.com/Serraniel/nepfleet-templates/issues/88)) ([0a55b74](https://github.com/Serraniel/nepfleet-templates/commit/0a55b74b18e54baa6e41011a87bb7faa74e1dd18))
* forgejo mail and runner labels as inputs ([#102](https://github.com/Serraniel/nepfleet-templates/issues/102)) ([859ed22](https://github.com/Serraniel/nepfleet-templates/commit/859ed22f1deea3090fe90b32897d4514de476aa7))
* forgejo signs in through an identity provider; runner capacity as an input ([#117](https://github.com/Serraniel/nepfleet-templates/issues/117)) ([97c0bf6](https://github.com/Serraniel/nepfleet-templates/commit/97c0bf67ca72aadffa00c6be86005b258e179064))
* grafana gets loki as a data source ([#114](https://github.com/Serraniel/nepfleet-templates/issues/114)) ([61d1d41](https://github.com/Serraniel/nepfleet-templates/commit/61d1d410d0388a3f7d2d7681f269b4a317aba1b5))
* Homepage settings and info widgets as values ([#70](https://github.com/Serraniel/nepfleet-templates/issues/70)) ([bf34389](https://github.com/Serraniel/nepfleet-templates/commit/bf34389dbf62362628408c7f0d7d3241b55624a8))
* initial version ([f648a8d](https://github.com/Serraniel/nepfleet-templates/commit/f648a8d332f85ee267b0e2cd794b5e8b4b3cc886))
* Kuma monitors for databases, caches and workers, grouped per stack ([#84](https://github.com/Serraniel/nepfleet-templates/issues/84)) ([6adfa47](https://github.com/Serraniel/nepfleet-templates/commit/6adfa473131ff2b2e36c02f69ac264197e320c2f))
* Mealie template ([#67](https://github.com/Serraniel/nepfleet-templates/issues/67)) ([99d5411](https://github.com/Serraniel/nepfleet-templates/commit/99d54119e6901a04d0ad3eb593ee3d966cb74b4a))
* metrics labels for registry and immich, checked in CI ([#103](https://github.com/Serraniel/nepfleet-templates/issues/103)) ([058bd23](https://github.com/Serraniel/nepfleet-templates/commit/058bd23a42f1a72887022f070d515eff34e0aebf))
* n8n template ([#65](https://github.com/Serraniel/nepfleet-templates/issues/65)) ([629fce3](https://github.com/Serraniel/nepfleet-templates/commit/629fce3d2289d5023f6e0d54fe66dc1fc5091e77))
* ntfy template ([#79](https://github.com/Serraniel/nepfleet-templates/issues/79)) ([b8aab57](https://github.com/Serraniel/nepfleet-templates/commit/b8aab577c45100986a305b2d2b26ab8bf96c2128))
* opencloud edits Office documents with Euro-Office, optionally ([#119](https://github.com/Serraniel/nepfleet-templates/issues/119)) ([ba0d179](https://github.com/Serraniel/nepfleet-templates/commit/ba0d17944364f7aa8f24a962470ddb3931b73ad2))
* paperless can read Office documents ([#101](https://github.com/Serraniel/nepfleet-templates/issues/101)) ([960a03b](https://github.com/Serraniel/nepfleet-templates/commit/960a03bce52d294018203fd0448d14518b801c32))
* paths that skip the bot check, tested behind Anubis in CI ([#111](https://github.com/Serraniel/nepfleet-templates/issues/111)) ([38613a0](https://github.com/Serraniel/nepfleet-templates/commit/38613a0d3a5deaac115f061b45e54cd9b5a5cde0))
* Pi-hole template (DNS ad blocking for the local network) ([#86](https://github.com/Serraniel/nepfleet-templates/issues/86)) ([d2f1814](https://github.com/Serraniel/nepfleet-templates/commit/d2f1814ea0fb410ea5637f3b1e28c328644cd133))
* Stirling-PDF template ([#69](https://github.com/Serraniel/nepfleet-templates/issues/69)) ([ac69b3b](https://github.com/Serraniel/nepfleet-templates/commit/ac69b3bbe0a5e9df229e160f3953bfd305ad6e96))
* Syncthing template ([#71](https://github.com/Serraniel/nepfleet-templates/issues/71)) ([5de4b42](https://github.com/Serraniel/nepfleet-templates/commit/5de4b422118e9f6de7d04e535ca3b4a6fea4f5a4))
* template for AdGuard Home ([#94](https://github.com/Serraniel/nepfleet-templates/issues/94)) ([7742778](https://github.com/Serraniel/nepfleet-templates/commit/77427785d38efe38484da1166d234caead7eb8ad))
* template for Authelia ([#95](https://github.com/Serraniel/nepfleet-templates/issues/95)) ([ab142f1](https://github.com/Serraniel/nepfleet-templates/commit/ab142f11797c3eb1e9c99f67e383345669ef223a))
* template for Garage (S3-compatible storage) ([#112](https://github.com/Serraniel/nepfleet-templates/issues/112)) ([6de214d](https://github.com/Serraniel/nepfleet-templates/commit/6de214d699417fbbc7c247d660d7852a2ceaab90))
* template for Hermes Agent ([#97](https://github.com/Serraniel/nepfleet-templates/issues/97)) ([42b89f5](https://github.com/Serraniel/nepfleet-templates/commit/42b89f5eb765cebe860af99a6216d21df3e57764))
* template for Loki with Alloy (central logs) ([#113](https://github.com/Serraniel/nepfleet-templates/issues/113)) ([83d6f5f](https://github.com/Serraniel/nepfleet-templates/commit/83d6f5f73adaa8af8940890e0455e846938416b5))
* template for Mastodon ([#99](https://github.com/Serraniel/nepfleet-templates/issues/99)) ([773fe50](https://github.com/Serraniel/nepfleet-templates/commit/773fe506b78eccab00db958953aeec66f32cc6b2))
* template for Matrix with Synapse and Element ([#96](https://github.com/Serraniel/nepfleet-templates/issues/96)) ([771a081](https://github.com/Serraniel/nepfleet-templates/commit/771a081aac5b2c688c6ed530170382d3e19ebf40))
* template for OpenClaw ([#98](https://github.com/Serraniel/nepfleet-templates/issues/98)) ([999bf73](https://github.com/Serraniel/nepfleet-templates/commit/999bf73adcb707918e832d554a42e00c21f2d623))
* template for Pocket ID ([#90](https://github.com/Serraniel/nepfleet-templates/issues/90)) ([03c8de0](https://github.com/Serraniel/nepfleet-templates/commit/03c8de0a30cbdd8dd3f6579b4b6b610f799e0728))
* template for SweetCaptcha ([#121](https://github.com/Serraniel/nepfleet-templates/issues/121)) ([93dbff7](https://github.com/Serraniel/nepfleet-templates/commit/93dbff78e66b443ec77b423640ad3df000be92be))
* template for the Beszel agent ([#104](https://github.com/Serraniel/nepfleet-templates/issues/104)) ([e050c25](https://github.com/Serraniel/nepfleet-templates/commit/e050c2559688257a7882905353dac67ae16b9e6b))
* template for the Beszel hub ([#91](https://github.com/Serraniel/nepfleet-templates/issues/91)) ([1bfec89](https://github.com/Serraniel/nepfleet-templates/commit/1bfec89381066b97a61e726bfaaa57a942bb7efa))
* template for Wokko ([#120](https://github.com/Serraniel/nepfleet-templates/issues/120)) ([5b73449](https://github.com/Serraniel/nepfleet-templates/commit/5b73449806ec39fa51f2ce90721dd6c5e965f9bc))
* templates for Prometheus and Grafana ([#93](https://github.com/Serraniel/nepfleet-templates/issues/93)) ([cf56dc8](https://github.com/Serraniel/nepfleet-templates/commit/cf56dc824d203ca236816a2b197ef5d828097004))
* templates use ${NEPFLEET_URL} and declare their web UI ([#85](https://github.com/Serraniel/nepfleet-templates/issues/85)) ([9d92dae](https://github.com/Serraniel/nepfleet-templates/commit/9d92daebe6256ef6cba43c1b98b5cc18cae30acc))
* USB sticks for Home Assistant, hardware transcoding for Jellyfin and Tdarr ([#64](https://github.com/Serraniel/nepfleet-templates/issues/64)) ([5f85ca5](https://github.com/Serraniel/nepfleet-templates/commit/5f85ca5f4c7a62f926caa76ac116cb9cccb4b7d1))
* volume-backup encrypts to the fleet's keys and skips backup: false volumes ([#82](https://github.com/Serraniel/nepfleet-templates/issues/82)) ([0111865](https://github.com/Serraniel/nepfleet-templates/commit/0111865f4684f212ee5863e0cf3fae2a3c8b9098))
* VPN egress template (gluetun) for Mullvad and other providers ([#78](https://github.com/Serraniel/nepfleet-templates/issues/78)) ([1f2e36b](https://github.com/Serraniel/nepfleet-templates/commit/1f2e36b98556d18aef0e4a0ed587f2be36a2ea95))
* WireGuard home VPN template (wg-easy) ([#83](https://github.com/Serraniel/nepfleet-templates/issues/83)) ([53f63aa](https://github.com/Serraniel/nepfleet-templates/commit/53f63aa02033307fd175152f2bb4d10dcbae6bba))


### Bug Fixes

* forgejo's runner declares its connection in its config ([#122](https://github.com/Serraniel/nepfleet-templates/issues/122)) ([4e0b6c1](https://github.com/Serraniel/nepfleet-templates/commit/4e0b6c1c02c8ba382f21ed6699494a4969797f50))
* **frps:** do not claim monitoring without kuma labels ([#32](https://github.com/Serraniel/nepfleet-templates/issues/32)) ([c23678a](https://github.com/Serraniel/nepfleet-templates/commit/c23678ad4b68220196299be6b19565ed80eb437a))
* **homebox:** generate the API key pepper Homebox 0.27 requires ([#52](https://github.com/Serraniel/nepfleet-templates/issues/52)) ([c8838a1](https://github.com/Serraniel/nepfleet-templates/commit/c8838a127bf72e0c7e7eae33ea017c43013dfbd3))
* turn off telemetry in Immich ML, Navidrome, Open WebUI and Stirling-PDF ([#73](https://github.com/Serraniel/nepfleet-templates/issues/73)) ([53c7575](https://github.com/Serraniel/nepfleet-templates/commit/53c757577b64ac02a5efaf9e9ed072edf35990d1))
* turn off update checks and crash reports that phone home ([#77](https://github.com/Serraniel/nepfleet-templates/issues/77)) ([dfb0e88](https://github.com/Serraniel/nepfleet-templates/commit/dfb0e8816ce02222a31bc4e115d24786fb5ba44e))


### Dependencies

* Bump home-assistant/home-assistant from 2026.10 to 2026.11 in /apps/homeassistant ([#55](https://github.com/Serraniel/nepfleet-templates/issues/55)) ([838dda0](https://github.com/Serraniel/nepfleet-templates/commit/838dda0e2fcd06c128556074efde4e54d6b3bc1f))
* Bump immich-app/immich-server from v3.3.5 to v3.3.6 in /apps/immich in the templates group across 1 directory ([#54](https://github.com/Serraniel/nepfleet-templates/issues/54)) ([d49073d](https://github.com/Serraniel/nepfleet-templates/commit/d49073d1c14e52a869a4c6644f33f129de85dbc7))
* Bump serraniel/sweetfolio from 0.5.4 to 0.6.0 in /apps/sweetfolio ([#56](https://github.com/Serraniel/nepfleet-templates/issues/56)) ([5efaf82](https://github.com/Serraniel/nepfleet-templates/commit/5efaf82d8896c7f2a59393a8e8e2fc0f7b53c35f))
