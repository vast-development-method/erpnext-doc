# Record lifecycle and persistence

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/runtime/document-lifecycle-and-transactions.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

2,593 bindings across 122 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Access log | 2 | [clear old logs … make access log](operations-001.md#op-9b55aa7fd5940f) |
| Record · Activity log | 9 | [before insert … logout feed](operations-001.md#op-e2b1b3316bdbf0) |
| Record · Api request log | 1 | [clear old logs](operations-001.md#op-2a53aef37be843) |
| Record · Attachment queue | 12 | [validate … get permission query conditions](operations-001.md#op-8198d0b12f5b74) |
| Record · Audit trail | 10 | [validate … filter fields for gridview](operations-002.md#op-728eb87837b68b) |
| Service · Builder | 13 | [flatten … from](operations-002.md#op-3869dee0dfd265) |
| Service · Client | 23 | [get list](operations-002.md#op-5405f228fa2b70) · [get count … delete doc](operations-003.md#op-b675861194d961) |
| Record · Comment | 14 | [after insert … validate](operations-003.md#op-44b797b1f9a7be) · [on update … update comments in parent](operations-004.md#op-3cbc10ff8dc8df) |
| Record · Communication | 74 | [onload … cc list](operations-004.md#op-d7110fea1ddc8b) · [bcc list … get email without link](operations-005.md#op-b5bcbcec825b9e) · [update parent document on communication … mail sender](operations-006.md#op-7ccdd0c77b4332) · [mail sender fullname … send email](operations-007.md#op-321fb4243aef13) |
| Record · Communication link | 1 | [on doctype update](operations-007.md#op-22ae9d6bf179a0) |
| Service · Create new | 9 | [get new doc … get default based on another field](operations-007.md#op-1d063ca5de20dc) |
| Service · Custom | 16 | [initialize … initialize](operations-008.md#op-cc6b84af6617cd) |
| Record · Custom docperm | 3 | [on update … update custom docperm](operations-008.md#op-01bade788760aa) |
| Record · Custom role | 3 | [validate … get custom allowed roles](operations-008.md#op-3d4b743fdb43b2) |
| Record · Data export | 15 | [get data keys … export data](operations-008.md#op-69f84d22a10616) · [initialize … append name column](operations-009.md#op-9a68e775acf0b9) |
| Record · Data import | 175 | [value mapping state … get preview from template](operations-009.md#op-892abee023aa5f) · [start import … export csv](operations-010.md#op-7b8f4b1edc420d) · [get export filters … get import provider](operations-011.md#op-f88eb4157ebfbb) · [get fixed csv delimiter … print grouped warnings](operations-012.md#op-9b232c7b45d486) · [initialize … get import column index](operations-013.md#op-d1ede0f47489f8) · [build import reference sets … get column indexes](operations-014.md#op-0b5103dfddf56d) · [is table field … get field key from df](operations-015.md#op-1daf1bf9082fdf) · [normalize source value … sync value mappings](operations-016.md#op-6f88455d3940f0) |
| Service · Database | 286 | [setup database … get db](operations-016.md#op-ebe161d95e0b0f) · [get duckdb … sql list](operations-017.md#op-bd4ce4722bd221) · [sql ddl … get global](operations-018.md#op-bd7b8b43be038a) · [get default … get db table columns](operations-019.md#op-d9bba948775069) · [get table columns … get routines](operations-020.md#op-4d814e1f1d32e8) · [savepoint … is duplicate fieldname](operations-021.md#op-c6dbe019591167) · [is duplicate entry … is type datetime](operations-022.md#op-d15cff8f5cab71) · [rename table … is syntax error](operations-023.md#op-7175db57f31280) · [is table missing … transform result](operations-024.md#op-698c43d5f6e44b) · [sql … estimate count](operations-025.md#op-9f02be2ab06ad1) · [unbuffered cursor … create connection](operations-026.md#op-aaaac83a6e5d5e) · [get db path … updatedb](operations-027.md#op-cf59b9c03f54cf) · [get database list … regexp replace](operations-028.md#op-34f5364f1bc94a) |
| Report · Database storage usage by tables | 3 | [execute … optimize doctype job](operations-028.md#op-940ef57f08f80e) |
| Service · Db manager | 10 | [initialize … create user](operations-028.md#op-b03b1d93adeab6) · [delete user … restore database](operations-029.md#op-64fb813b56789e) |
| Service · Db query | 54 | [parse sql … is query](operations-029.md#op-ebd67acfa323ed) · [extract tables … add comment count](operations-030.md#op-ebaeeca9e28d31) · [selects own name … strip alias](operations-031.md#op-2e4e1aa2b857a8) |
| Service · Defaults | 18 | [set user default … set global default](operations-031.md#op-f5e4975e91c05a) · [add global default … clear cache](operations-032.md#op-ca3a48e74cb0a9) |
| Record · Defaultvalue | 1 | [on doctype update](operations-032.md#op-91c483ff4f0a63) |
| Service · Deferred insert | 5 | [deferred insert … get doctype name](operations-032.md#op-a04ad96f67e261) |
| Service · Delete doc | 17 | [delete doc … raise link exists exception](operations-032.md#op-31dfba6224a009) · [delete dynamic links … delete controllers](operations-033.md#op-247cc451f09c69) |
| Record · Deleted document | 3 | [clear old logs … bulk restore](operations-033.md#op-48dfe00ff2f895) |
| Record · Docfield | 3 | [get link doctype … repr](operations-033.md#op-69b91f3aa7aed6) |
| Service · Docfield | 1 | [supports translation](operations-033.md#op-23515df11a4306) |
| Record · Docshare | 9 | [validate … on doctype update](operations-033.md#op-4896a730f0733e) |
| Service · Docstatus | 6 | [is draft … is submitted](operations-033.md#op-795af625aa2c03) · [is cancelled … cancelled](operations-034.md#op-43d74c546a361f) |
| Record · Doctype | 111 | [before insert … sync doctype layouts](operations-034.md#op-ee946a35ee6aab) · [setup autoincrement and sequence … validate child table](operations-035.md#op-28894e08119b08) · [add child table fields … check dynamic link options](operations-036.md#op-87be035194dc75) · [check illegal default … validate link filters](operations-037.md#op-532931d11cc19d) · [get fields not allowed in list view … get row size utilization](operations-038.md#op-6e6068df64aca0) |
| Record · Doctype settings map | 13 | [before naming … on update](operations-038.md#op-47314810924f1c) · [export doc … set sibling active](operations-039.md#op-883f798454d362) |
| Service · Document | 232 | [reduce extended instance … get doc](operations-039.md#op-b3fb4f29a94cf2) · [get doc str … validate amended from](operations-040.md#op-92000f88191c3e) · [copy attachments from amended from … has fieldlevel read restrictions](operations-041.md#op-d4b9d1aec534bc) · [restore masked fields from db … submit](operations-042.md#op-7eac18ffc32aae) · [cancel … get url](operations-043.md#op-e2321ee3f434d5) · [add comment … permitted fieldnames](operations-044.md#op-db8630eefd40e1) · [weakref … init valid columns](operations-045.md#op-3fe732946ccc3d) · [get valid columns … validate selects](operations-046.md#op-a9935a702ba2d8) · [validate data fields … document values generator](operations-047.md#op-8d6ef10ed6f164) · [unlock document … get single](operations-048.md#op-f89dcd40f8d59e) |
| Record · Document naming rule | 6 | [validate … apply](operations-049.md#op-13d632f0ed6a82) |
| Record · Document naming settings | 19 | [get transactions and prefixes … preview series](operations-049.md#op-074f957f56312e) · [fetch last doc if available](operations-050.md#op-49216643529ee2) |
| Record · Document share key | 2 | [before insert … is expired](operations-050.md#op-96973317ccb827) |
| Record · Domain | 10 | [setup domain … setup sidebar items](operations-050.md#op-1ce7a51190cd8e) |
| Record · Domain settings | 8 | [set active domains … get active modules](operations-050.md#op-a22b589854ad35) |
| Record · Duckdb sync | 14 | [before save … get duckdb conn](operations-050.md#op-650642c85738f8) · [sync schema … sync data to duckdb](operations-051.md#op-14a4bccf5352c1) |
| Record · Dynamic link | 2 | [on doctype update … deduplicate dynamic links](operations-051.md#op-7f34d14d02ae8e) |
| Service · Dynamic links | 5 | [get dynamic link map … invalidate distinct link doctypes](operations-051.md#op-7f0529fe3e705a) |
| Service · Edit profile | 1 | [get context](operations-051.md#op-3746980a26e385) |
| Record · Error log | 5 | [validate … get fingerprint stats](operations-051.md#op-ebb98bf09c38c1) |
| Service · Exporter | 12 | [initialize … guess indentation](operations-052.md#op-4e5538e202d0a1) |
| Record · File | 86 | [initialize … after rename](operations-052.md#op-5d025c1c0518ac) · [on trash … unzip](operations-053.md#op-1d6aa9426fa18a) · [exists on disk … split doctypes by user permissions](operations-054.md#op-80caa2af066da6) · [get user permission field conditions … find file by url](operations-055.md#op-98ed8911f8abe0) · [get safe file name … check path safety](operations-056.md#op-9e1a7dfe46a3c7) |
| Service · File | 11 | [unzip file … zip files](operations-056.md#op-fd8569c55afce0) |
| Service · Filter | 14 | [bool … optimize](operations-056.md#op-a5635846294c01) · [group key … str](operations-057.md#op-81d92b3f6646f1) |
| Service · Functions | 20 | [initialize … sum](operations-057.md#op-697f33bccdaea2) |
| Record · Has role | 1 | [before insert](operations-057.md#op-b002b3ea0637e2) |
| Record · Installed applications | 12 | [update versions … get setup wizard pending apps](operations-058.md#op-2b81ed94685523) |
| Record · Language | 6 | [validate … sync languages](operations-058.md#op-1aa7c863326a14) |
| Service · Lazytranslatedstring | 8 | [initialize … repr](operations-058.md#op-2c56d9ee220979) · [eq … lt](operations-059.md#op-40bacd0394dc46) |
| Service · Link count | 3 | [notify link count … update link count](operations-059.md#op-4049e401054a3b) |
| Record · Log settings | 12 | [clear old logs … clear log table](operations-059.md#op-44ad419cd0063a) |
| Service · Mapper | 7 | [make mapped doc … map child doc](operations-059.md#op-7e15d8caf73774) |
| Service · Mask | 4 | [mask field value … mask list results](operations-060.md#op-40f2955fed4155) |
| Service · Meta | 80 | [get meta … set only once fields](operations-060.md#op-4de910ab257a1f) · [get table fields … add custom links and actions](operations-061.md#op-993022051b04f8) · [check if large table … get web template](operations-062.md#op-f518a7fe820a9b) · [is nested set … serialize](operations-063.md#op-f0ceba60cd7806) |
| Service · Model | 3 | [delete fields … is default field](operations-063.md#op-5071337b0298d4) |
| Record · Module def | 10 | [validate … before rename](operations-063.md#op-471e54a4008733) · [get installed apps](operations-064.md#op-b1f912770f9dbf) |
| Record · Module profile | 4 | [onload … update all users](operations-064.md#op-8dba81e5d6f227) |
| Service · Mysqlclient | 54 | [is deadlocked … get connection](operations-064.md#op-99ffc524ad3a1d) · [get connection … get table columns description](operations-065.md#op-b651883c1ddeea) · [get column type … estimate count](operations-066.md#op-816f41d4aeab65) |
| Service · Naming | 30 | [initialize … set naming from document naming rule](operations-066.md#op-036c70ac28eb67) · [set name by naming series … get param value for match](operations-067.md#op-aa8bb5785cf7c8) |
| Record · Navbar settings | 4 | [get app logo … sync table](operations-067.md#op-754f8536f8372e) |
| Service · Notifications | 3 | [get notification config … get todays events](operations-067.md#op-0dd2a3dd772612) |
| Service · Operator map | 9 | [like … func timespan](operations-068.md#op-5ca444aae6c5fa) |
| Record · Package | 2 | [validate … get license text](operations-068.md#op-e10e5436c04187) |
| Record · Package import | 2 | [validate … import package](operations-068.md#op-0c014879075e67) |
| Record · Package release | 7 | [set version … make tarfile](operations-068.md#op-0ae9ca80e2a5dd) |
| Record · Page | 17 | [autoname … validate island](operations-068.md#op-ca6b3c731cde04) · [get folder path … as js string](operations-069.md#op-c3be235312309a) |
| Record · Patch log | 1 | [before migrate](operations-069.md#op-0ef70c394d6804) |
| Record · Permission inspector | 9 | [onload … delete](operations-069.md#op-4914c82b94016f) |
| Record · Permission log | 7 | [changed at](operations-069.md#op-7732927b0c490e) · [make perm log … filter child docs](operations-070.md#op-f0ab6f67ed18c4) |
| Workspace · Permission manager | 9 | [get roles and doctypes … get standard permissions](operations-070.md#op-b4071779eaff66) |
| Record · Permission type | 13 | [autoname … create custom field](operations-070.md#op-b01b162de25610) · [on trash … get doctype ptype map](operations-071.md#op-9e146398da41bd) |
| Report · Permitted documents for user | 3 | [execute … query doctypes](operations-071.md#op-ac0d2c8d74f311) |
| Service · Platform | 87 | [init … whitelist](operations-071.md#op-c244531bbd9ded) · [innerfn … scrub](operations-072.md#op-c869f36e99e194) · [unscrub … import doc](operations-073.md#op-b894eb6a219bb8) · [respond as web page … override whitelisted method](operations-074.md#op-26b9f04c8bb28c) |
| Service · Platformclient | 27 | [initialize … enter context](operations-074.md#op-5aff30a92bd1c9) · [exit context … post process](operations-075.md#op-408299a5d0f86e) · [initialize](operations-076.md#op-f60031ea397b90) |
| Service · Platformdict | 6 | [getstate … copy](operations-076.md#op-409d3964c85abc) |
| Record · Prepared report | 25 | [queued by … expire stalled report](operations-076.md#op-cd754b72230145) · [delete prepared reports … convert json to csv](operations-077.md#op-8281595bbde260) |
| Report · Prepared report analytics | 3 | [execute … get data](operations-077.md#op-fd3411376f0947) |
| Service · Qb query | 5 | [initialize … handle virtual doctype](operations-077.md#op-73bd16529b0ccd) |
| Service · Query | 81 | [apply date field filter conversion … apply dict filters](operations-077.md#op-be587f0da7471c) · [apply filter … get user permission conditions](operations-078.md#op-7ca1cfbeb14d76) · [get doctype link fields … initialize](operations-079.md#op-03865d67c902aa) · [apply select … validate alias](operations-080.md#op-ba14742246e6cd) · [check function field permission](operations-081.md#op-269e6ba82a7f5b) |
| Record · Recorder | 38 | [from Platform ouput … get filtered requests](operations-081.md#op-ccd494922b49f2) · [get stats … get doctype name](operations-082.md#op-84f831baac951a) |
| Record · Recorder query | 7 | [db insert … delete](operations-082.md#op-a2e1af90a2a600) |
| Record · Recorder suggested index | 7 | [db insert … load from db](operations-082.md#op-8ef65bf9661409) · [db update … get stats](operations-083.md#op-fe10439a674698) |
| Service · Rename doc | 22 | [update document title … rename dynamic links](operations-083.md#op-d81d37afb6d0aa) · [bulk rename … get fetch fields](operations-084.md#op-5a5fb81913adaf) |
| Service · Rename field | 6 | [rename field … update user settings](operations-084.md#op-3ebfd5f877d801) |
| Record · Report | 42 | [execute … set doctype roles](operations-084.md#op-4f7323cd0b975f) · [is permitted … get report module dotted path](operations-085.md#op-24e6108dc15d0c) · [get group by field … enable prepared report](operations-086.md#op-0cedf92f09f977) |
| Record · Role | 14 | [before rename … role query](operations-086.md#op-5e517d44f250eb) |
| Record · Role permission for page and report | 11 | [set report page data … update custom roles](operations-086.md#op-34d0537ee0babe) · [update disable prepared report … update status](operations-087.md#op-84c3b0ad11ae9d) |
| Record · Role profile | 4 | [autoname … get permission log options](operations-087.md#op-f64533c0d492d0) |
| Record · Rq job | 26 | [check permissions … filter current site jobs](operations-087.md#op-8547dc00c11df1) · [eval filters … get custom queues](operations-088.md#op-9ddaf22349457a) |
| Record · Rq worker | 9 | [load from db … compute utilization](operations-088.md#op-91174092ac420b) |
| Record · Scheduled job log | 1 | [clear old logs](operations-088.md#op-9dd733d10b28f2) |
| Record · Scheduled job type | 23 | [validate … is job in queue](operations-088.md#op-a7391a505191a2) · [rq job id … on doctype update](operations-089.md#op-8511d105409ca8) |
| Service · Schema | 43 | [get definition … get all column definitions](operations-089.md#op-587688700aeb31) · [get docfields … alter](operations-090.md#op-65725b2eb34f2f) · [initialize … alter primary key](operations-091.md#op-46411757c99817) |
| Record · Security settings | 13 | [security txt … validate expires](operations-091.md#op-f19aeb6ef8d0bb) · [check security txt expiry … get email subject](operations-092.md#op-8ddddd7553dff8) |
| Service · Sequence | 5 | [create sequence … create missing sequences](operations-092.md#op-30128a7e6769ef) |
| Record · Server script | 19 | [validate … execute api server script](operations-092.md#op-dadfe057ca6afd) · [enabled … get server script map](operations-093.md#op-b1f1e1b056cdeb) |
| Record · Session default settings | 3 | [get session default values … clear session defaults](operations-093.md#op-3318d1d753a312) |
| Service · Setup db | 19 | [get mariadb variables … drop database](operations-093.md#op-6e9d652b897e94) · [get root connection](operations-094.md#op-019a145a41ffe0) |
| Record · Sms settings | 9 | [validate receiver nos … create sms log](operations-094.md#op-721fe61a651015) |
| Record · Submission queue | 15 | [created at … get latest submissions](operations-094.md#op-56c47723064cf5) · [format tb](operations-095.md#op-a347eeeb623dfd) |
| Service · Sync | 9 | [sync all … delete duplicate icons](operations-095.md#op-a14f20b6664a61) |
| Record · System settings | 17 | [validate … sync system settings](operations-095.md#op-75c01dd7b8f8f6) · [disable duckdb cron job … snapshot report scheduler](operations-096.md#op-769c65ff10aafc) |
| Service · Terms | 8 | [initialize … get sql](operations-096.md#op-7fb1855fbc1955) |
| Service · Trace | 6 | [initialize … traced field](operations-096.md#op-28b378088e5584) |
| Record · Translation | 4 | [validate … clear user translation cache](operations-096.md#op-ce3ab3b5b158cb) |
| Record · User | 99 | [active sessions … setup](operations-096.md#op-27e422d488f33d) · [autoname … reset password](operations-097.md#op-369e3091eb3c5c) · [get fullname … get blocked modules](operations-098.md#op-c245b44bc955a7) · [validate user email inbox … sign up](operations-099.md#op-a557e454733cbb) · [needs password setup … clear session](operations-100.md#op-18662d46ca51fb) |
| Report · User doctype permissions | 5 | [execute … get perm types](operations-101.md#op-178a5b33c23313) |
| Record · User group | 2 | [after insert … on trash](operations-101.md#op-c2d23389731d3d) |
| Record · User invitation | 24 | [before insert … validate app name](operations-101.md#op-c932edd9a89961) · [validate role … get user](operations-102.md#op-8eee35d8482886) |
| Service · User invitation | 7 | [invite by email … accept invitation](operations-102.md#op-851d885fcb1465) |
| Record · User permission | 21 | [validate … add doc to perm](operations-102.md#op-b82116dad25a1c) · [user permission exists … update applicable](operations-103.md#op-ac775c6532554f) |
| Record · User session display | 4 | [db insert … delete](operations-103.md#op-cdc658d9f94e64) |
| Service · User settings | 7 | [get user settings … update user settings data](operations-103.md#op-b077a13ec8613a) |
| Record · User social login | 2 | [validate … disallow Platform userid change](operations-103.md#op-ade38294771212) |
| Record · User type | 21 | [validate … get data](operations-104.md#op-f1578758286a41) |
| Service · Utils | 59 | [get parent doc … find](operations-104.md#op-234794b28cd73d) · [find all … commit after response](operations-105.md#op-aff9c88294b640) · [drop index if exists … execute query](operations-106.md#op-0248a3a0df9ca0) · [mask child query fields … patch all](operations-107.md#op-fbdea2fb91119b) |
| Record · Version | 11 | [update version info … as string](operations-107.md#op-d45033a189abe8) |
| Record · View log | 1 | [clear old logs](operations-107.md#op-1e4b0f80139202) |
| Service · Virtual doctype | 9 | [get list … db insert](operations-107.md#op-a2eced77a4b305) · [load from db … as str](operations-108.md#op-8b0ab6ca2b49f7) |
| Service · Workflow | 20 | [get workflow name … show progress](operations-108.md#op-8f0809653d1a58) · [set workflow state on action](operations-109.md#op-9bd274ff42e898) |
