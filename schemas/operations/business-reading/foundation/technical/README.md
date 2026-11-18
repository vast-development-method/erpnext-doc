# Site operations and diagnostics

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/services/site-operations.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

458 bindings across 28 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · Apps | 7 | [get docked apps … get incomplete setup route](operations-001.md#op-aa9148a7eb2d4a) |
| Service · Bundler | 27 | [download file … get node env](operations-001.md#op-7a2d0a8b34dadb) · [get safe max old space size … html to js template](operations-002.md#op-9fb004b70d010e) |
| Service · Cache manager | 16 | [get doctype map key … build domain restricted page cache](operations-002.md#op-f3ec243c34afde) · [clear cache … reset metadata version](operations-003.md#op-3be08af38611ec) |
| Service · Commands | 7 | [pass context … get commands](operations-003.md#op-c1b130d990d233) |
| Service · Config | 8 | [get site config … get conf](operations-003.md#op-c36bad25eee807) |
| Service · Coverage | 3 | [initialize … exit context](operations-003.md#op-267fbe7aa9ce19) |
| Service · Discovery | 4 | [discover all tests … add module tests](operations-003.md#op-7c1583f225f3c4) |
| Service · Environment | 12 | [initialize test environment … create global test record dependencies](operations-004.md#op-1a10e565279e50) |
| Service · Exceptions | 5 | [initialize … initialize](operations-004.md#op-ecb000533b5d09) |
| Service · Export file | 14 | [export doc … export root](operations-004.md#op-94c26baba7760f) · [exported file path … create if not exists](operations-005.md#op-f3cc064ccc2f50) |
| Service · Gettext | 6 | [generate pot file … connect to site](operations-005.md#op-fc8b4572ae8545) |
| Service · Import file | 11 | [calculate hash … reset tree properties](operations-005.md#op-ce97d7c06619a3) |
| Service · Installer | 47 | [is scheduler enabled … update site config](operations-006.md#op-68486822692571) · [update config file … get db dump header](operations-007.md#op-4a41653b1af8aa) |
| Service · Loader | 5 | [recursive load suites in pymodule](operations-007.md#op-fe92ff8c090474) · [load testsuites in pymodule … discover tests](operations-008.md#op-5d6d4fb8a6f4b1) |
| Service · Migrate | 15 | [atomic … stop](operations-008.md#op-2a2170460a8d5f) |
| Service · Monitor | 12 | [start … log file](operations-008.md#op-d3e302ab7ea9fa) · [initialize … flush](operations-009.md#op-0549a3ba36e4dc) |
| Service · Optimizations | 13 | [optimize all … parse thread siblings](operations-009.md#op-3d4526ef55431c) |
| Service · Parallel test runner | 20 | [initialize … before test setup](operations-009.md#op-ae17cb8c3dd06b) · [setup test file list … call orchestrator](operations-010.md#op-a842e3d3b733e8) |
| Service · Patch handler | 12 | [run all … execute patch](operations-010.md#op-404769aeb952a0) · [should never skip … patch mode](operations-011.md#op-4031bce8881be9) |
| Service · Recorder | 35 | [post init … dump](operations-011.md#op-da67ad6815cf87) · [patch sql … import data](operations-012.md#op-034cd6c2df3c0b) |
| Service · Redis utils | 1 | [create rq users](operations-012.md#op-a8d1fa8bc3abe5) |
| Service · Result | 27 | [initialize … get Test Method Name](operations-012.md#op-b4784ea124d379) · [add Success … add Unexpected Success](operations-013.md#op-9ba68ba23fa52d) |
| Service · Runner | 7 | [initialize … apply debug decorators](operations-013.md#op-17a6bbec25f64c) · [profile … iterate suite](operations-014.md#op-931bb81402f338) |
| Service · Scheduler | 12 | [trigger scheduler event … ready for migration](operations-014.md#op-4aab023a793680) |
| Service · Site | 48 | [new site … format app](operations-014.md#op-4e278c29441eac) · [add db index … publish realtime](operations-015.md#op-c827de99edb7b7) · [browse … sync desktop icons](operations-016.md#op-4d2b0973f55786) |
| Service · Testing | 14 | [main … has config](operations-016.md#op-2496d044448bf7) · [yarn add … run cypress](operations-017.md#op-902920db2cbd99) |
| Service · Translate | 6 | [build message files … migrate translations](operations-017.md#op-f5609b81f8f2ef) |
| Service · Utils | 64 | [build … export json](operations-017.md#op-3aa46b98434949) · [export csv … list sites](operations-018.md#op-8e12d05b7d0abc) · [setup chrome … delete app level folder](operations-019.md#op-593be544a86607) · [debug timer … wrapper](operations-020.md#op-bc2dc0306767b7) |
