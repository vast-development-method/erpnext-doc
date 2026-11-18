# Web content and issued documents

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/services/files-and-reports.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

602 bindings across 76 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · About us settings | 2 | [on update … get args](operations-001.md#op-6fd3e03ceb65ca) |
| Service · Base renderer | 4 | [initialize … build response](operations-001.md#op-b9b8f889a3353e) |
| Service · Base template page | 8 | [initialize … update website context](operations-001.md#op-d20ec11ef8472c) |
| Service · Comments | 2 | [get limit … add comment](operations-001.md#op-a6d9c97d923619) |
| Record · Contact us settings | 1 | [on update](operations-001.md#op-1452069040d5cb) |
| Service · Custom field | 1 | [extract](operations-001.md#op-a99578b0adac8c) |
| Service · Customization | 1 | [extract](operations-001.md#op-665da83f9b6224) |
| Service · Dashboard fixtures | 3 | [get data … get charts](operations-001.md#op-1b55002ba4e5c8) |
| Service · Desktop icon | 1 | [extract](operations-001.md#op-494c0d154cdcec) |
| Record · Discussion reply | 4 | [on update](operations-001.md#op-7d96579f013b71) · [after insert … delete message](operations-002.md#op-cbde1dd2170453) |
| Record · Discussion topic | 2 | [submit discussion … save message](operations-002.md#op-74c70f1e3d20d5) |
| Service · Doctype | 1 | [extract](operations-002.md#op-bb0ebc88a54f60) |
| Service · Document page | 8 | [can render … find matching document webview](operations-002.md#op-fd52a5a86772ad) |
| Service · Error page | 3 | [initialize … init context](operations-002.md#op-308728590861d1) |
| Service · Fieldtypes | 1 | [is image column](operations-002.md#op-ce8f253ee316e4) |
| Record · Help article | 13 | [validate … get context](operations-002.md#op-43410cad1b8abd) · [get parents … add feedback](operations-003.md#op-dea8d36dc06516) |
| Record · Help category | 5 | [before insert … clear cache](operations-003.md#op-b42d1a2f557bce) |
| Service · Html template | 1 | [extract](operations-003.md#op-2f56ed289e9e93) |
| Service · Javascript | 3 | [extract … parse template string](operations-003.md#op-7d4d5c7e82370b) |
| Service · Kanban board | 1 | [extract](operations-003.md#op-1ab635aa27f856) |
| Service · Layout | 5 | [iter zones … iter nodes](operations-003.md#op-c89734c87ffd37) |
| Record · Letter head | 8 | [before insert … on trash](operations-003.md#op-a36c798f30ce07) · [validate … set as default](operations-004.md#op-a9050abcf7a391) |
| Service · List filter | 1 | [extract](operations-004.md#op-37741885e5a4a2) |
| Service · List renderer | 2 | [can render … render](operations-004.md#op-56669a6657de77) |
| Service · Locale | 5 | [get number format … get locale value](operations-004.md#op-9db5c908a45e89) |
| Service · Metatags | 7 | [initialize … has meta tags](operations-004.md#op-c30ae3e6f280b4) |
| Service · Module onboarding | 1 | [extract](operations-004.md#op-436a5adca1e385) |
| Service · Navbar | 2 | [extract … get module](operations-004.md#op-a6a728d86024d2) |
| Record · Network printer settings | 2 | [get printers list … get network printer settings](operations-005.md#op-83af676e7e0df7) |
| Service · Not found page | 5 | [initialize … is custom home page](operations-005.md#op-caf49d03f0e5ab) |
| Service · Not permitted page | 3 | [initialize … render](operations-005.md#op-0ba53215a8ce48) |
| Service · Onboarding step | 1 | [extract](operations-005.md#op-66acc043cae39f) |
| Service · Path resolver | 12 | [is Platform test fixture … validate path](operations-005.md#op-30c4a844493ce5) |
| Record · Personal data deletion request | 27 | [initialize](operations-005.md#op-c693caad232e06) · [autoname … remove unverified record](operations-006.md#op-4447af31134498) · [confirm deletion … get pattern](operations-007.md#op-6e138610767e8c) |
| Record · Personal data download request | 5 | [as dict … get user data](operations-007.md#op-8cfe1a654d8590) |
| Record · Portal settings | 9 | [get all menu items … validate](operations-007.md#op-278bf9ba8f743d) |
| Workspace · Print | 2 | [get print styles … get print settings to show](operations-007.md#op-c8bca55fe71e78) |
| Record · Print format | 67 | [renders from file … new section](operations-007.md#op-5604a082280ff2) · [new column … validate no classic layout](operations-008.md#op-9763e220270532) · [extract images … check draft](operations-009.md#op-07a1dce55f6ed5) · [apply draft … generate preview](operations-010.md#op-09a5bdfb3e305b) |
| Workspace · Print format builder beta | 2 | [get google fonts … get google fonts](operations-010.md#op-5bb23321fd923a) |
| Record · Print format field template | 5 | [validate … export doc](operations-010.md#op-3860b57c65bbab) |
| Record · Print format snippet | 4 | [validate … export doc](operations-010.md#op-04291be848965f) |
| Service · Print page | 2 | [can render … render](operations-011.md#op-3171664b60bd23) |
| Record · Print settings | 5 | [validate … follow print settings pdf generator](operations-011.md#op-b5dae185b8db32) |
| Record · Print style | 3 | [validate … export doc](operations-011.md#op-722bbb95fa1bf7) |
| Service · Python | 1 | [extract](operations-011.md#op-ffe66cd724ece5) |
| Service · Redirect page | 3 | [initialize … render](operations-011.md#op-8b85d082bc3d2c) |
| Service · Report | 1 | [extract](operations-011.md#op-3c4336dd42ba64) |
| Service · Request data | 1 | [get context](operations-011.md#op-7d99f844747dd9) |
| Service · Request to delete data | 1 | [get context](operations-011.md#op-9431a78ece4456) |
| Service · Router | 15 | [get page info from web page with dynamic routes … get page info](operations-011.md#op-c0b72ec298208f) · [setup source … clear routing cache](operations-012.md#op-d7509117b4572c) |
| Service · Serve | 4 | [get response … get response without exception handling](operations-012.md#op-f38fc1d5c49f06) |
| Service · Sidebar | 1 | [extract](operations-012.md#op-01f34fb20e0ed0) |
| Service · Static page | 5 | [initialize … render](operations-012.md#op-bad0bde7378f1f) |
| Service · Template page | 28 | [initialize … get html](operations-012.md#op-946e06ceba9e47) · [post process context … get start folders](operations-013.md#op-ea924c88c79509) |
| Service · Translate | 71 | [new catalog … get hook](operations-013.md#op-ce3cd6b2528d2b) · [get po dir … get parent language](operations-014.md#op-2eca4eda9e8051) · [get user lang … get all messages from js files](operations-015.md#op-f8ea73452399b6) · [get messages from file … print language](operations-016.md#op-3a2eae4243a5bb) |
| Service · Utils | 40 | [extract messages from code … add line number](operations-016.md#op-ac69692f27a061) · [get line number … get frontmatter](operations-017.md#op-88c9e46157fe10) · [get sidebar items … check if webform exists](operations-018.md#op-fa79b4930274d9) |
| Record · Utm campaign | 1 | [before save](operations-018.md#op-ca514bc911fd6c) |
| Record · Utm medium | 1 | [before save](operations-018.md#op-0ef15252c0f030) |
| Record · Utm source | 1 | [before save](operations-018.md#op-6af669e845be34) |
| Record · Web form | 47 | [validate … reset field parent](operations-018.md#op-051889a2db9822) · [on update … delete](operations-019.md#op-ae55dc179c129f) · [delete multiple … get published web forms](operations-020.md#op-b0da0aa6c96c5e) |
| Service · Web form | 3 | [extract … set headers](operations-020.md#op-9c626772de4313) |
| Record · Web form request | 22 | [initialize … get doc values](operations-020.md#op-8db7b82996dc09) · [has reference … get web form request](operations-021.md#op-9977ebe46cb79b) |
| Record · Web page | 14 | [validate … check for redirect](operations-021.md#op-4f97a27c14a82f) · [set metatags … get dynamic web pages](operations-022.md#op-2617dc750dc238) |
| Record · Web page view | 4 | [clear old logs … is tracking enabled](operations-022.md#op-75d09135376219) |
| Record · Web template | 11 | [validate … render](operations-022.md#op-75be82c84c631b) |
| Report · Website analytics | 11 | [execute … run](operations-022.md#op-07902066967604) · [get columns … get report summary](operations-023.md#op-927817b26071d6) |
| Service · Website generator | 22 | [initialize … is website published](operations-023.md#op-e0581590052fb1) · [get condition field … update website search index](operations-024.md#op-7f922c446941bd) |
| Record · Website meta tag | 3 | [get content … set in context](operations-024.md#op-1145540df26d92) |
| Record · Website route meta | 2 | [autoname … clear cache](operations-024.md#op-9e77c15964f6b9) |
| Record · Website script | 1 | [on update](operations-024.md#op-83b78699cf312e) |
| Record · Website settings | 16 | [authorize access … get access token](operations-024.md#op-3780c60d91ae91) · [get website settings … get auto account deletion](operations-025.md#op-0cdd98ee37e6f2) |
| Record · Website sidebar | 1 | [get items](operations-025.md#op-4cb41aa4bfb9de) |
| Record · Website slideshow | 4 | [validate … get slideshow](operations-025.md#op-cc75344a34f2eb) |
| Record · Website theme | 15 | [validate … after migrate](operations-025.md#op-c6137c0e5600ff) |
| Service · Workspace | 1 | [extract](operations-026.md#op-fa9eeccf9f1194) |
| Service · Workspace sidebar | 1 | [extract](operations-026.md#op-47ea13ae40a78f) |
