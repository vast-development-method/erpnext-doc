# Shared value and file services

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/services/persistence-identity-and-values.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

1,462 bindings across 83 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · App heartbeat event | 2 | [capture app heartbeat … should capture](operations-001.md#op-681416c2612e74) |
| Service · Background jobs | 42 | [get queues timeout … get workers](operations-001.md#op-3d4402abedcffe) · [get running jobs in queue … start sentry](operations-002.md#op-7a9019bc197a4e) |
| Service · Backups | 33 | [initialize … setup backup tables](operations-002.md#op-66b20ec45d7bb1) · [set backup tables from config … is file old](operations-003.md#op-2d77169fb4b560) · [get backup path … backup](operations-004.md#op-5758ef8a3f5bba) |
| Service · Bench helper | 14 | [Platform Click Wrapper … get apps](operations-004.md#op-9e90f272258b0f) |
| Service · Boilerplate | 18 | [make boilerplate … get license options](operations-004.md#op-5493879f816bbd) · [get license text … create parent folder if not exists](operations-005.md#op-47966062ebedf1) |
| Service · Browser | 27 | [initialize … prepare header footer](operations-005.md#op-9a82b395e134d8) · [add page number … get](operations-006.md#op-bf34c0f00c8496) |
| Service · Caching | 15 | [generate request cache key … redis cache](operations-006.md#op-77e825dc56437f) · [wrapper … deprecated local cache](operations-007.md#op-40c843bb9daa1c) |
| Service · Cdp connection | 13 | [initialize … remove listener](operations-007.md#op-25c1e44f3c29bb) |
| Service · Change log | 21 | [get change log … update last known versions](operations-007.md#op-e21ae86cc3fd0e) · [get versions … get pyproject](operations-008.md#op-a187bd08c8b72f) |
| Service · Chrome pdf generator | 15 | [add browser … start chromium process](operations-008.md#op-071c6392c1314f) · [start chromium process … fetch devtools url](operations-009.md#op-688f71c98bdf61) |
| Service · Client | 8 | [is enabled … get debug info](operations-009.md#op-1c1b506ed7dc91) |
| Service · Collector | 26 | [summary … get python package](operations-009.md#op-232fe0b0ca041e) · [add js dependencies … npm author](operations-010.md#op-20f8d4000fe274) |
| Service · Commands | 8 | [get first party apps … empty line](operations-010.md#op-ed8f92e8392cc4) · [log … warn](operations-011.md#op-50a6b75ae6a46a) |
| Service · Connections | 5 | [can connect … check connection](operations-011.md#op-09a6b959358981) |
| Service · Csvutils | 15 | [escape formula injection … validate google sheets url](operations-011.md#op-a2527085630cb1) |
| Service · Dashboard | 7 | [cache source … wrapper](operations-011.md#op-d69b95e7f58479) · [generate and cache results … make records](operations-012.md#op-7f7db6a20cc192) |
| Service · Data | 188 | [get start of week index … time diff in hours](operations-012.md#op-0e9273cdc3cd32) · [now datetime … get year start](operations-013.md#op-468719bb5a71b8) · [get year start … duration to seconds](operations-014.md#op-c7d1decfda9537) · [validate duration format … safe div](operations-015.md#op-852bf8f95000b1) · [round based on smallest currency fraction … new line sep](operations-016.md#op-6f474f20dfa2a8) · [filter strip join … compare](operations-017.md#op-e6f5e0dcc1fedf) · [get filter … guess date format](operations-018.md#op-0aaf9acaa4e7ed) · [get date format … map trackers](operations-019.md#op-1819e6a9dcde58) · [attach expanded links](operations-020.md#op-02f3fe6dc4c34d) |
| Service · Dateutils | 9 | [user to str … get period ending](operations-020.md#op-c98d5eeff1f416) |
| Service · Defaults | 1 | [get not null defaults](operations-020.md#op-3908559d1f5751) |
| Service · Diff | 3 | [get version diff … version query](operations-020.md#op-247faedee5252d) |
| Service · Doctor | 9 | [get workers … pending jobs](operations-020.md#op-97826d93dcfce6) |
| Service · Error | 10 | [is ldap exception](operations-020.md#op-7020377db9a435) · [log error … guess exception source](operations-021.md#op-53e78387d36094) |
| Service · File lock | 7 | [create lock … release document locks](operations-021.md#op-9ba193b60771b3) |
| Service · File manager | 24 | [safe b64decode … save file](operations-021.md#op-833f7cc24fae60) · [get file data from hash … is safe path](operations-022.md#op-e8f329f2bc6199) |
| Service · Fixtures | 4 | [sync fixtures … export fixtures](operations-022.md#op-aa593c08bce31d) |
| Service · Formatters | 1 | [format value](operations-022.md#op-61ed7a6301cbed) |
| Service · Global search | 25 | [setup global search table … get doctypes with global search](operations-022.md#op-a5bcaf15c0bef1) · [get … get distinct words](operations-023.md#op-02a99f945907d4) |
| Service · Goal | 2 | [get monthly results … get monthly goal graph data](operations-023.md#op-9c10d9913e6e07) |
| Service · Html utils | 8 | [clean html … unescape html](operations-024.md#op-d5ce9d1a8d5916) |
| Service · Identicon | 5 | [initialize … base64](operations-024.md#op-1e0b58b9c3f063) |
| Service · Image | 3 | [resize images … optimize image](operations-024.md#op-6e071aa555b8fe) |
| Service · Inplacevar | 13 | [iadd … ilshift](operations-024.md#op-c7d69849034a5e) · [irshift … protected inplacevar](operations-025.md#op-c65a3151fcd491) |
| Service · Install | 10 | [before install … delete desktop icons for app](operations-025.md#op-29e278c89201b2) |
| Service · Island | 5 | [page island name … get island assets](operations-025.md#op-246f7388412299) |
| Service · Jinja | 15 | [get jenv … get template](operations-025.md#op-523efcb91115dd) · [get email from template … safe render flags](operations-026.md#op-68d51c812dc598) |
| Service · Jinja globals | 10 | [resolve class … is rtl](operations-026.md#op-b9e14a7294b754) |
| Service · Lazy loader | 1 | [lazy import](operations-026.md#op-492d33568338a1) |
| Service · Legacy gravatar cleanup | 6 | [get gravatar image fields … should show gravatar deletion prompt](operations-026.md#op-369f4343068650) · [has gravatar image urls … delete gravatar image urls](operations-027.md#op-1b8aabfb27c1d1) |
| Service · Licenses | 2 | [to spdx license … canonicalize](operations-027.md#op-955e955ad688da) |
| Service · Local | 16 | [getattribute … release local](operations-027.md#op-06794cdde772a4) |
| Service · Logger | 5 | [create handler … get logger](operations-027.md#op-15407bdff8e8ea) · [filter … sanitized dict](operations-028.md#op-ce7e96667dead6) |
| Service · Make random | 4 | [add random children … how many](operations-028.md#op-c8e5f1b2a9743b) |
| Service · Messages | 8 | [msgprint … throw permission error](operations-028.md#op-9fb445b6ceb23b) |
| Service · Modules | 12 | [get module placement … get blockable module names](operations-028.md#op-4dd73c7836f5bb) · [get modules from app … is module](operations-029.md#op-38491c90c62760) |
| Service · Momentjs | 2 | [update … get all timezones](operations-029.md#op-6b9145b257b18f) |
| Service · Nestedset | 25 | [update nsm … validate ledger](operations-029.md#op-01c5624adb39d1) · [get ancestors … get descendants of](operations-030.md#op-5a8d9ef2b8bf7f) |
| Service · New navigation nudge | 3 | [should show new navigation prompt … skip new navigation prompt](operations-030.md#op-4719b4976f1a4f) |
| Service · Number format | 2 | [from string … str](operations-030.md#op-91f0913b4b3cb7) |
| Service · Oauth | 18 | [build oauth url … get user record](operations-030.md#op-54d88c6980cf36) · [update oauth user … redirect post login](operations-031.md#op-ae9c0b5e0902cc) |
| Service · Page | 29 | [read local resource … on lifecycle event](operations-031.md#op-3d60ca53a4602e) · [start wait … close](operations-032.md#op-47bdd1da2cd69d) |
| Service · Password | 15 | [get decrypted password … get encryption key](operations-032.md#op-146f0b2d45af0d) · [get password reset limit](operations-033.md#op-42364d1d534c38) |
| Service · Password strength | 11 | [test password strength … get dictionary match feedback](operations-033.md#op-eed6b7ac6405a4) |
| Service · Pdf | 26 | [find options in meta … get file data from writer](operations-033.md#op-202aa417f1a681) · [prepare options … get host url](operations-034.md#op-382e441c7b54d4) |
| Service · Pdf merge | 7 | [initialize … get file data from writer](operations-034.md#op-bafee45c15d53d) |
| Service · Platformcloud | 1 | [on Platformcloud](operations-034.md#op-c032f2b47bcdf5) |
| Service · Pluto | 36 | [resolve container queries … resolve](operations-034.md#op-9eb8c5734eeaa3) · [plutoprint can render … get pdf from stream](operations-035.md#op-2f9b94086d855b) · [close … fetch](operations-036.md#op-c0d19c1718e12f) |
| Service · Preview | 5 | [get preview from html … safe execute](operations-036.md#op-bcb22a80b2ba6f) |
| Service · Print format | 21 | [get max bulk print docs … publish failure](operations-036.md#op-8f6084a76c3aba) · [download multi pdf … print by server](operations-037.md#op-565c33348f118b) |
| Service · Print format generator | 65 | [render jinja template … get qr code](operations-037.md#op-82bfa3cefdbe29) · [format field value … underlay background](operations-038.md#op-402bee7fd462ca) · [page options … filter conditional rows](operations-039.md#op-9b957aa64b0063) · [prepare html … process margin texts](operations-040.md#op-84967f5f16c158) |
| Service · Print utils | 16 | [print format doc or none … convert uom](operations-040.md#op-5874df47686e12) |
| Service · Queue | 13 | [initialize … add](operations-040.md#op-ecf61a79f15cd4) · [is ratelimited … get last sent events](operations-041.md#op-8ddedbbf4fb0ac) |
| Service · Redis queue | 9 | [initialize … gen acl list](operations-041.md#op-b3cc0e00fa5650) |
| Service · Redis semaphore | 7 | [initialize … exit context](operations-041.md#op-844908b040cd13) · [ensure tokens … decode](operations-042.md#op-ac3e80b12fe9df) |
| Service · Redis wrapper | 62 | [sugadd … llen](operations-042.md#op-3150a95a8d58e3) · [lrange … get value](operations-043.md#op-730c5fdcac1507) · [set value … clear](operations-044.md#op-6813b8ddfe6257) |
| Service · Response | 20 | [report error … as json](operations-044.md#op-88bfb516b15175) · [as pdf … handle session stopped](operations-045.md#op-548ccaca22fc0c) |
| Service · Safe exec | 63 | [getattr … initialize](operations-045.md#op-5f0316f9650db8) · [meta … send](operations-046.md#op-97aeefb241b922) · [get safe request session … get attr for eval](operations-047.md#op-4369890cedec0b) · [validate attribute read … get module properties](operations-048.md#op-6c11e1432e3b45) |
| Service · Sbom | 3 | [generate sbom … notify](operations-048.md#op-a1b76e36e9a6d5) |
| Service · Scheduler | 20 | [cprint … activate scheduler](operations-048.md#op-67a5aea85352d8) · [get scheduler status … get scheduler tick](operations-049.md#op-16deb1fb944758) |
| Service · Sentry | 7 | [setup once … capture exception](operations-049.md#op-1c37fe12d4cecb) |
| Service · Spdx | 13 | [to spdx … checksums](operations-049.md#op-b018104e713579) |
| Service · Synchronization | 1 | [filelock](operations-049.md#op-9c6bbeaa98efbf) |
| Service · Telemetry | 4 | [add bootinfo](operations-049.md#op-1d2c0e5d3f623c) · [capture … site age](operations-050.md#op-1d6ccaf84b4935) |
| Service · Testutils | 2 | [add custom field … clear custom fields](operations-050.md#op-ea111a47a0a7d4) |
| Service · Translations | 4 | [unnamed value … set user lang](operations-050.md#op-c9637620626f60) |
| Service · Transport | 4 | [initialize … post](operations-050.md#op-d6886cd26168be) |
| Service · Typing validations | 7 | [is mock … transform parameter types](operations-050.md#op-1c532753008b5c) |
| Service · Typst emitter | 67 | [pt … list names](operations-050.md#op-1e2023dc6f23f4) · [barcode blocker … text value](operations-051.md#op-58bf7e94cfa000) · [initialize … label color](operations-052.md#op-2535ca4ed2a3e4) · [data field … table thumb](operations-053.md#op-96622ac65b6bfb) |
| Service · User | 24 | [initialize … get](operations-053.md#op-d18703cca3ecb2) · [get can read … get portal roles](operations-054.md#op-36e5d194835381) |
| Service · Utils | 98 | [get fullname … split emails](operations-054.md#op-eb36b43e4db03d) · [validate url … get site path](operations-055.md#op-fee3ddbcf256e8) · [get files path … sanitize email](operations-056.md#op-5754b760a9c3b3) · [parse addr … initialize](operations-057.md#op-d33401305a74df) · [add … ensure http](operations-058.md#op-f2992306d291ab) |
| Service · Verified command | 8 | [get signed params … verify using doc](operations-058.md#op-4ee979a77a9411) · [get url using doc](operations-059.md#op-f0798532a91548) |
| Service · Weasyprint | 7 | [warn deprecated … get weasyprint pdf](operations-059.md#op-cd0e4eab7fb8ea) |
| Service · Weasyprint legacy | 21 | [legacy blockers … set field renderers](operations-059.md#op-06ad995b3739cb) · [process zones … import weasyprint](operations-060.md#op-fc12226d51297a) |
| Service · Xlsxutils | 41 | [get column … get value](operations-060.md#op-fdd2741a6bea16) · [parse options … build xlsx response](operations-061.md#op-3fc93e8ee389f4) |
