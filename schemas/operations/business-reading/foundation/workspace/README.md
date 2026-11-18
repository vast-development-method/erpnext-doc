# Forms, reports and navigation

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/services/desktop-workflows.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

2,015 bindings across 148 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · 404 | 1 | [get context](operations-001.md#op-58426a87b29add) |
| Service · About | 1 | [get context](operations-001.md#op-bcbab96c264e38) |
| Service · Activity | 30 | [get activity timeline … get milestone activities](operations-001.md#op-d366d859e5b2b0) · [get version activities … truncate value](operations-002.md#op-16d994e435085b) |
| Record · Address | 24 | [setup … has website permission](operations-002.md#op-53819d65f3deef) · [get address templates … get address display list](operations-003.md#op-2f5289c4d86c97) |
| Service · Address and contact | 12 | [load address and contact … set link title](operations-003.md#op-a03cb344f3363e) |
| Record · Address template | 5 | [validate … get previous default](operations-003.md#op-62c00a415ca1b3) · [get default address template](operations-004.md#op-4e4ae449076497) |
| Report · Addresses and contacts | 6 | [execute … add blank columns for](operations-004.md#op-985855f58bad4c) |
| Service · Api | 32 | [run … get studio page scripts](operations-004.md#op-c9099c042fe6a3) · [get studio component … build studio file tree](operations-005.md#op-1c61cd1d1820d5) |
| Service · Artifact | 3 | [generate page json … available data note](operations-005.md#op-5b83b16ce77584) |
| Service · Assign to | 14 | [get … close all assignments](operations-005.md#op-0779f69901b6df) · [remove … format message for assign to](operations-006.md#op-dbcde3fd4b3887) |
| Service · Attribution | 1 | [get context](operations-006.md#op-4f47ddf6205653) |
| Report · Audit system hooks | 5 | [execute … delist](operations-006.md#op-e1db7d17de4523) |
| Workspace · Backups | 9 | [get time … get downloadable links](operations-006.md#op-9d36e1091ff7fc) |
| Service · Billing | 2 | [get context](operations-006.md#op-887484c4860735) · [get boot](operations-007.md#op-48f0507442fcf6) |
| Service · Block codec | 10 | [compress … validate image data](operations-007.md#op-aa5561515684db) |
| Service · Boot | 33 | [get bootinfo … add home page](operations-007.md#op-dbcb0cfa80d289) · [add timezone info … get desktop icon urls](operations-008.md#op-98bc8b20fd76f3) |
| Service · Build | 31 | [can build bundle … build](operations-008.md#op-616a3b331be123) · [write page sources … is vue component](operations-009.md#op-9038897be65f22) · [get editor assets … after app build](operations-010.md#op-4002ac68d190e3) |
| Record · Bulk update | 3 | [bulk update … bulk action](operations-010.md#op-407c65580f8a0a) |
| Service · Calendar | 3 | [update event … get events](operations-010.md#op-ef6a5f3484a7fe) |
| Record · Client script | 2 | [on update … on trash](operations-010.md#op-da186361478fc3) |
| Service · Commands | 2 | [build studio app … watch studio](operations-010.md#op-cac20a6ae80189) |
| Service · Components | 2 | [get component definition … get schema files](operations-010.md#op-70f9e0cd85afb0) |
| Record · Console log | 1 | [after delete](operations-010.md#op-2fbd904ce304a7) |
| Record · Contact | 29 | [autoname … has link](operations-010.md#op-2e99f8527d6844) · [has common link … get contact display list](operations-011.md#op-fbb983fe6bdf69) |
| Service · Contact | 2 | [get context … send message](operations-011.md#op-120d3291c94261) |
| Service · Conversation | 3 | [ask clarification](operations-011.md#op-5d64533b4882c3) · [normalize sections … propose plan](operations-012.md#op-6c31e14141d1a5) |
| Record · Country | 3 | [validate … get countries and currencies](operations-012.md#op-6d916c6c67752b) |
| Service · Country info | 6 | [get country info … update](operations-012.md#op-e91746247ff927) |
| Record · Currency | 2 | [validate … enable default currencies](operations-012.md#op-90083f05ee5560) |
| Record · Custom field | 17 | [autoname … create custom field](operations-012.md#op-efc0b22c21da43) · [create custom fields … delete custom fields](operations-013.md#op-6838dab866e12b) |
| Record · Custom html block | 3 | [validate … get custom blocks for user](operations-013.md#op-df5fd38a83478a) |
| Record · Custom sidebar | 47 | [validate … resolve arrangement](operations-013.md#op-5790c981461b1b) · [merge layers … shape row](operations-014.md#op-e603f490ba9ea2) · [settle references … get permission query conditions](operations-015.md#op-1dacbf96dcb494) |
| Record · Custom workspace | 19 | [before validate … upsert property customization](operations-015.md#op-3d66b7fc3d4eb9) · [upsert settings customization … reset workspace customization](operations-016.md#op-59bd41a5ef2413) |
| Record · Customize form | 34 | [on update … delete custom fields](operations-016.md#op-9013e53fd76d18) · [make property setter … get link filters from doc without customisations](operations-017.md#op-55a98050d46882) |
| Record · Dashboard | 15 | [onload … get permitted cards](operations-017.md#op-44131e96a6c9fa) · [get non standard charts in dashboard … get html](operations-018.md#op-9aff4a86a40f84) |
| Record · Dashboard chart | 18 | [get permission query conditions … get parent doctypes](operations-018.md#op-7412105c35f03c) |
| Record · Dashboard chart source | 6 | [get config … on update](operations-018.md#op-2336cfb86661c7) · [on trash … get folder path](operations-019.md#op-641b6c6704c42a) |
| Record · Dashboard settings | 4 | [create dashboard settings … save chart config](operations-019.md#op-e7200417e23109) |
| Service · Data | 10 | [invalid filter message … describe resource](operations-019.md#op-f997457a7b1d95) |
| Service · Desk | 3 | [get session boot failed error … get context](operations-019.md#op-d5e87517c67f90) |
| Service · Desk page | 2 | [get … getpage](operations-019.md#op-ce094742bb023f) |
| Service · Desk views | 21 | [initialize](operations-019.md#op-19f72a516bf5be) · [build entities … exclude disabled reports](operations-020.md#op-3e76b83322a33a) |
| Service · Desktop | 33 | [handle not exist … is permitted](operations-020.md#op-16b16238ae1546) · [get cached … save new widget](operations-021.md#op-ca9a78311f3478) · [clean up … get installed apps](operations-022.md#op-98bea89d4b17a0) |
| Workspace · Desktop | 1 | [get context](operations-022.md#op-bc207d0c77454f) |
| Record · Desktop icon | 25 | [validate … is desk link](operations-022.md#op-be56f0bacd4fe9) · [clear every users desktop icons … add workspace to desktop](operations-023.md#op-31237f9266fb1f) |
| Record · Desktop layout | 2 | [save layout … delete layout](operations-023.md#op-6d70d156505ab9) |
| Record · Desktop settings | 4 | [on update … is desktop icons page](operations-023.md#op-67d43249d6aba6) |
| Service · Doc preview | 1 | [get preview](operations-023.md#op-821d5d84527d98) |
| Record · Dock | 63 | [autoname … on trash](operations-023.md#op-73d72bfba1de47) · [clear dock cache … apps screen sort key](operations-024.md#op-0e7f6a7de52399) · [sequence … get site dock layer](operations-025.md#op-4f5393a40c7399) · [save app dock … get permission query conditions](operations-026.md#op-4fdc60c8110117) |
| Record · Doctype layout | 4 | [validate … remove fields](operations-026.md#op-ccc9a87ec7b64e) |
| Service · Document follow | 23 | [update follow … get row changed](operations-026.md#op-72ef16110fe516) · [get added row … can read table field](operations-027.md#op-460ddf8345e1a8) |
| Service · Error | 1 | [get context](operations-027.md#op-341dce90369767) |
| Record · Event | 20 | [validate … has permission](operations-027.md#op-3a415741bc780e) · [send event digest … set status of events](operations-028.md#op-c97a50ba94dd05) |
| Service · Export | 10 | [write document file … remove empty values from slots](operations-028.md#op-8688fa4945a5dc) |
| Service · Files | 45 | [run list app files … is page script path](operations-028.md#op-c90e4320c96bc6) · [page script owner … restore db files from disk](operations-029.md#op-698dca5f09dd8b) · [walk export folder … validate folder removable](operations-030.md#op-c2c5bcd66ac6d3) |
| Record · Form tour | 6 | [before save … get onboarding ui tours](operations-030.md#op-f750cd8cff07ec) |
| Service · Full text search | 16 | [initialize … get document to index](operations-030.md#op-3c8afdeff968c2) · [build … get index path](operations-031.md#op-3ef28939fb7313) |
| Service · Gantt | 1 | [update task](operations-031.md#op-94eb5e0d7babe7) |
| Record · Global search settings | 11 | [validate … update global search fields](operations-031.md#op-d0e7369e3a6f5c) |
| Service · Grid import | 18 | [download template … parse file](operations-031.md#op-e55221d272c89c) · [parse google sheet … stringify](operations-032.md#op-245082c6253a8d) |
| Service · Index | 2 | [get context … get boot](operations-032.md#op-43b5cd0b4b70b3) |
| Service · Introspect | 7 | [describe page data … run get sort fields](operations-032.md#op-e805ae3e6cbfe3) · [run get whitelisted methods](operations-033.md#op-151903180bbcc4) |
| Record · Kanban board | 53 | [validate … usable](operations-033.md#op-e86980bd40e70a) · [default group by fieldnames … publish kanban board update](operations-034.md#op-8dada4d6ed1013) · [add card … save settings](operations-035.md#op-6a55ef8d561385) |
| Service · Layers | 2 | [resolve layers … apply layer](operations-035.md#op-ea31a85b9fa3a3) |
| Service · Like | 4 | [toggle like … add comment](operations-035.md#op-b575603e2c18e3) |
| Service · Link preview | 1 | [get preview data](operations-035.md#op-2fe9fe8c3d247f) |
| Service · Link title | 5 | [get link title field … get link names by doctype](operations-035.md#op-bca7e6c1c3cbc6) |
| Service · Linked with | 43 | [get submitted linked docs … get next level children](operations-035.md#op-f439a4266692ee) · [get doctype references … process linked docs in dependency order](operations-036.md#op-53ea6e704f16be) · [mark processed … get dynamic linked fields](operations-037.md#op-73e7734c7b6cd1) |
| Service · List | 7 | [get list data … get dynamic filters](operations-037.md#op-a1024fcc67b9ca) |
| Record · List filter | 22 | [autoname … validate standard](operations-037.md#op-daa95b25ce7180) · [was standard … delete list layout](operations-038.md#op-870a8ed1e4d24b) |
| Record · List view settings | 4 | [save listview settings … get default listview fields](operations-038.md#op-b70d503a4fa60c) |
| Service · Listview | 3 | [get list settings … set list settings](operations-038.md#op-921b2f046d9419) · [get group by count](operations-039.md#op-a146db95432d4e) |
| Service · Llm | 7 | [is retryable … get api key](operations-039.md#op-d1fb326db99540) |
| Service · Load | 24 | [getdoc … get view logs](operations-039.md#op-fcbaa88b5125cb) · [get tags … get user info for viewers](operations-040.md#op-fc811bdac60259) |
| Service · Login | 7 | [get context … sanitize redirect](operations-040.md#op-61e15abe69ec88) |
| Service · Logout | 1 | [get context](operations-040.md#op-ffd6ad7bb96dbc) |
| Service · Loop | 20 | [initialize … page root](operations-040.md#op-3913c569fac1e8) · [build page context … run agent job](operations-041.md#op-6f8593c3bffe40) |
| Service · Me | 1 | [get context](operations-041.md#op-9cf1875dd4cebc) |
| Service · Message | 1 | [get context](operations-041.md#op-172a0fb4c7dd38) |
| Service · Meta | 19 | [get meta … add custom script](operations-041.md#op-03a218edc33dc5) · [show missing doctype msg … get js](operations-042.md#op-029eaeb4546f82) |
| Service · Models | 5 | [get label … get ai models](operations-042.md#op-c03e319e55efba) |
| Record · Module onboarding | 14 | [on update … update completion](operations-042.md#op-f9d229d32c2984) · [capture step update … get permitted onboardings](operations-043.md#op-2bec7232071692) |
| Record · Note | 10 | [validate … get unseen notes](operations-043.md#op-8480fba78f9c28) |
| Record · Notification log | 22 | [before insert … get title html](operations-043.md#op-bc3d2920a16ade) · [enqueue create notification … set notifications as unseen](operations-044.md#op-34ea8dbd3466f0) |
| Record · Notification settings | 13 | [on update … has permission](operations-044.md#op-c4426ff1da2821) · [set seen value](operations-045.md#op-d18d18908144a6) |
| Record · Notification type | 5 | [on trash … seed type into settings](operations-045.md#op-32b847730f4729) |
| Service · Notifications | 24 | [get notifications … get child doctypes with field](operations-045.md#op-8d7a97defcbeaf) · [get external links … extract mentions](operations-046.md#op-2073af6eedd9e5) |
| Record · Number card | 12 | [autoname … add card to dashboard](operations-046.md#op-a85c91be2a268c) |
| Service · Onboarding | 2 | [get onboarding status … update user onboarding status](operations-046.md#op-fd60d9bf11ea1b) |
| Record · Onboarding step | 9 | [before export … is onboarding done](operations-046.md#op-6c5da22bc46a0c) · [get record filters … can import](operations-047.md#op-a21a37b0881cda) |
| Service · Page | 4 | [text arg … dangling binding warning](operations-047.md#op-04d4f94cb48f8d) |
| Service · Permissions | 4 | [has session permission … message query conditions](operations-047.md#op-82a1b438e0ddd0) |
| Service · Portal | 3 | [get context … get](operations-047.md#op-7ad4708c7e1bd7) |
| Service · Printpreview | 1 | [get context](operations-047.md#op-962fce750beee3) |
| Service · Printview | 38 | [get context … get template from string](operations-047.md#op-eb1fc8190944b6) · [set link titles … get page rule properties](operations-048.md#op-4865dab0ef5b38) · [get page rule margins … column has value](operations-049.md#op-b9f2299898b238) |
| Service · Profile | 1 | [get context](operations-049.md#op-1315933b74ed61) |
| Service · Prompts | 4 | [get generation prompt … get system prompt for mode](operations-049.md#op-ffcb1994c34582) |
| Record · Property setter | 10 | [autoname … delete property setters](operations-049.md#op-81c567c9baad2f) |
| Service · Qrcode | 3 | [get context … get query key](operations-049.md#op-0805ca301ad36f) · [get user svg from cache](operations-050.md#op-8bd1f14c1f7bdd) |
| Service · Query | 2 | [run query blocks … run read block](operations-050.md#op-f59099481b5120) |
| Service · Query report | 35 | [get report doc … build xlsx data](operations-050.md#op-faf709e4f1f79b) · [get xlsx styles … translate report data](operations-051.md#op-1ee520b75d51d0) |
| Service · Realtime | 1 | [publish doc change](operations-051.md#op-cd19c4bc357651) |
| Service · Registry | 12 | [schema … build shared registry](operations-051.md#op-871556ca12d813) · [build custom page registry … get tool registry for mode](operations-052.md#op-73e21aedc1bde0) |
| Service · Reportview | 41 | [get … get result key](operations-052.md#op-714658bbf1b6cf) · [compress … get filters cond](operations-053.md#op-c21118cda6e594) |
| Service · Robots | 1 | [get context](operations-053.md#op-ccd00055a6432f) |
| Record · Route history | 3 | [clear old logs … frequently visited links](operations-053.md#op-72341431ae94a9) |
| Service · Save | 6 | [savedocs … set local name](operations-054.md#op-4fbc5b073a4682) |
| Service · Scripts | 4 | [run get page script … write file script](operations-054.md#op-c49f966002e4f8) |
| Service · Search | 23 | [sanitize searchfield … scrub custom query](operations-054.md#op-feaa92293b3b10) · [relevance sorter … web search](operations-055.md#op-c5142ce68363f4) |
| Service · Selectors | 6 | [child blocks … match block](operations-055.md#op-8fdacaa4d71602) |
| Service · Session | 19 | [initialize … last task type](operations-055.md#op-347af42b9d936c) · [row to message … clear](operations-056.md#op-dd2ae5a434105d) |
| Service · Settings map | 2 | [has settings map … get settings map](operations-056.md#op-fd3385db0f5a2c) |
| Workspace · Setup wizard | 43 | [unnamed value … complete app setup](operations-056.md#op-5bddcf1755b575) · [initialize system settings and user … load user details](operations-057.md#op-d28055ce32722b) · [prettify args … show document insert error](operations-058.md#op-65daba7da278c8) |
| Record · Sidebar | 91 | [apps with old fixtures … rename to title](operations-058.md#op-28d60050e056a2) · [after rename … is linked](operations-059.md#op-41c2446ee6e7c0) · [validate item route … resolve sidebar](operations-060.md#op-fe9a354eddbfc6) · [resolve private sidebar … listed in](operations-061.md#op-306ef1d734cdd0) · [resolve … routable entities](operations-062.md#op-fdb789fd23d629) |
| Record · Sidebar item group | 1 | [get reports](operations-062.md#op-3efe7dc2631861) |
| Service · Sitemap | 3 | [get context … is dynamic route](operations-062.md#op-9ba2c283eee12f) |
| Service · Sqlite search | 86 | [strip surrogates … clear vocabulary](operations-062.md#op-46fb1d5b6cddda) · [insert vocabulary … calculate advanced score](operations-063.md#op-92497c95ddf86f) · [get base score … add text fields to document](operations-064.md#op-be3eec70816d10) · [add metadata fields to document … get search classes](operations-065.md#op-251a425a075bf1) |
| Service · Studio | 3 | [get context … get site url](operations-065.md#op-58bc52a4c0c2c5) |
| Record · Studio ai session | 2 | [on trash](operations-065.md#op-e58dc762f30857) · [delete ai messages](operations-066.md#op-ff85a23de46044) |
| Record · Studio app | 54 | [render … delete app folder](operations-066.md#op-709c2a0de5f0de) · [delete app build … get folder path](operations-067.md#op-92327e4f5188ea) · [validate app name … get vite dev server host](operations-068.md#op-9f5e432d64f4e4) |
| Record · Studio app file | 5 | [validate … on doctype update](operations-068.md#op-912ba92c331b1e) |
| Record · Studio component | 36 | [autoname … after rename](operations-068.md#op-445be0c3d090e9) · [rename references … fetch component batch](operations-069.md#op-a015886e60bb69) |
| Record · Studio page | 74 | [duplicate page … before insert](operations-070.md#op-729227d0c1b1d1) · [after insert … set resource json fields](operations-071.md#op-1d919c1c2f452e) · [before export … child lists](operations-072.md#op-acf32b7fe76910) · [get app page … get page](operations-073.md#op-001a5a7d469cec) |
| Service · Sync | 10 | [after migrate … read json file](operations-073.md#op-b45467370f37e4) |
| Service · Sync json | 11 | [sync file … get studio folders](operations-073.md#op-a836d4232a9b74) |
| Record · System console | 4 | [run](operations-073.md#op-25b527a8c33308) · [execute code … show processlist](operations-074.md#op-55bfb490989343) |
| Record · System health report | 22 | [no wait … get directory size](operations-074.md#op-db70d020d54e38) · [get directory size](operations-075.md#op-0054429b9df406) |
| Record · System health report errors | 7 | [db insert … get stats](operations-075.md#op-8d73171fed246b) |
| Record · System health report failing jobs | 7 | [db insert … get stats](operations-075.md#op-418e4c67faa751) |
| Record · System health report queue | 7 | [db insert … get stats](operations-075.md#op-98c4a0d9b6ddd1) |
| Record · System health report tables | 7 | [db insert … load from db](operations-075.md#op-2e5dd5fc897096) · [db update … get stats](operations-076.md#op-f6c8c4dcdae1c5) |
| Record · System health report workers | 7 | [db insert … get stats](operations-076.md#op-4783cce41b827f) |
| Record · Tag | 18 | [check user tags … remove all](operations-076.md#op-47a8361c1695bb) · [update … get tags list for awesomebar](operations-077.md#op-356ad7438d80ee) |
| Record · Tag link | 5 | [clear cache … check db](operations-077.md#op-0a7269b5dc41a1) |
| Service · Third party apps | 3 | [get context … delete client](operations-077.md#op-ea6e461ea7573b) |
| Record · Todo | 11 | [validate … has permission](operations-077.md#op-5958e93dee74dc) · [new todo](operations-078.md#op-17d8beda0316d2) |
| Report · Todo | 1 | [execute](operations-078.md#op-f4003de3a58b5a) |
| Service · Tree | 15 | [initialize … apply interactivity](operations-078.md#op-5938584b37e9bb) |
| Service · Treeview | 5 | [get all nodes … make tree args](operations-078.md#op-982418f975b4d2) |
| Service · Update password | 1 | [get context](operations-078.md#op-ae6800be6a46f2) |
| Service · Utils | 35 | [remove attach](operations-078.md#op-ad532e3ff91308) · [add comment … get export folder](operations-079.md#op-4af8c48dadf895) · [get export folder name … get exported app folders](operations-080.md#op-5f6976aa5ab165) |
| Service · Variables | 7 | [run add variable … reload](operations-080.md#op-6c8ada68f96af2) |
| Service · Watch | 12 | [watch … queue](operations-080.md#op-4e7abad9d5cc17) · [restart timer … is migrating](operations-081.md#op-f3015fcb9f549b) |
| Service · Website script | 3 | [get context … get setting](operations-081.md#op-151d0e7f0da871) |
| Service · Website search | 11 | [get schema … build index for all routes](operations-081.md#op-13fe9a0cdc8c7f) |
| Record · Workspace | 54 | [before validate … get widget label counts](operations-081.md#op-b62314db9ea151) · [validate duplicate widget labels … welcome blocks](operations-082.md#op-26ad5983b32cc0) · [make module workspace … is workspace manager](operations-083.md#op-9fc73fb6688947) · [check workspace manager](operations-084.md#op-338cb6aebd33bd) |
| Workspace · Workspace restore | 20 | [get restorable workspaces … bold](operations-084.md#op-56caf209bc74eb) |
| Record · Workspace sidebar | 2 | [validate … refuse new rows](operations-084.md#op-302fd004458d5a) |
