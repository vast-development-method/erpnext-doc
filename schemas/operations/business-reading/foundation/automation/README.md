# Workflow, automation and dispatch

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/services/work-dispatch.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

1,257 bindings across 77 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · Agent | 12 | [sync agents … tool import path](operations-001.md#op-8e77afe16c0d14) |
| Service · Api | 60 | [check config permission … user options](operations-001.md#op-d126426af37870) · [notification recipient options … system prompt](operations-002.md#op-d252fa2958e3d9) · [set model … parse answers](operations-003.md#op-db2b4f31300257) |
| Record · Assignment rule | 24 | [validate … get repeated](operations-004.md#op-2a1c8f7fd3245a) |
| Service · Assistant | 3 | [ensure builtin assistant … sync builtin assistant](operations-005.md#op-457e8a62759dec) |
| Service · Attachment store | 6 | [ensure table … table exists](operations-005.md#op-8ad86b853c3a84) |
| Service · Auth | 26 | [headers … request](operations-005.md#op-bc7d7aecabe9eb) · [get local client … close clients](operations-006.md#op-f5c88a5d4da666) |
| Record · Auto repeat | 39 | [validate … update auto repeat id](operations-006.md#op-145cd5f1992b75) · [update status … get auto repeat doctypes](operations-007.md#op-c60d805cee8090) · [update reference … generate message preview](operations-008.md#op-d53d09b0712fb9) |
| Record · Automation event subscription | 2 | [autoname … on doctype update](operations-008.md#op-7fa434e330ffcf) |
| Record · Automation flow | 21 | [validate … on update](operations-008.md#op-25ebe647b5256c) · [on trash](operations-009.md#op-d6d73ac0a0c352) |
| Record · Automation run | 2 | [clear old logs … on doctype update](operations-009.md#op-61f7cb9813f517) |
| Record · Automation trigger queue | 6 | [on doctype update … rebuild dedup column](operations-009.md#op-05460f7c6ea50c) |
| Service · Base | 14 | [render value … iter action classes](operations-009.md#op-e744a10cd4b5d1) |
| Service · Boot | 1 | [boot session](operations-009.md#op-d0542d564c8974) |
| Service · Bridge | 7 | [from raw … handle](operations-010.md#op-4b9e4575f447e5) |
| Service · Builtins | 72 | [builtin name … count](operations-010.md#op-360c25e9d4c61d) · [run report … error text](operations-011.md#op-db3917f5dc9c71) · [summarize names … is read function](operations-012.md#op-3cfea508d67c54) · [api server script … sync builtin tools](operations-013.md#op-b116fc7b4bd762) |
| Service · Callback | 16 | [callback … humanize](operations-013.md#op-1c406feddd9bf9) |
| Service · Chunker | 1 | [chunk text](operations-013.md#op-e28788e485e055) |
| Service · Client | 25 | [initialize … cleanup attachments](operations-014.md#op-eb804b9333e8ea) · [detail](operations-015.md#op-7b0c96fafb5088) |
| Service · Commands | 10 | [flow server … sync tools](operations-015.md#op-56fc6bf7225078) |
| Service · Conditions | 17 | [evaluate filter tree … render value](operations-015.md#op-d4c6f4780eafae) · [condition fieldnames … evaluate condition](operations-016.md#op-5ebcb687cd9ed2) |
| Service · Config | 1 | [get config](operations-016.md#op-4d484338452a70) |
| Service · Context | 1 | [Platform context](operations-016.md#op-5a7a2d72f6bc64) |
| Service · Core | 33 | [require doc … notify system](operations-016.md#op-55164b7fe0da68) · [validate … compile script](operations-017.md#op-6e2d8da438067c) |
| Service · Dispatch | 17 | [run automations … kick drainer](operations-017.md#op-59261ff484ba7b) · [run in context … disconnect](operations-018.md#op-f7099b6c8cbbbf) |
| Service · Drainer | 20 | [drain … supports skip locked](operations-018.md#op-8f426a9b8b74a9) · [has due pending … purge queue](operations-019.md#op-750288e55094e4) |
| Service · Embedder | 6 | [embed texts … get](operations-019.md#op-fb4d9024624db3) |
| Service · Events | 19 | [emit … claim subscriptions](operations-019.md#op-17595633a23ce6) · [claim subscription … validate payload size](operations-020.md#op-68cee5c5cfb252) |
| Service · Extract | 26 | [extract … as bytes](operations-020.md#op-3689a733ee814d) · [as text … read capped](operations-021.md#op-7583a074764de5) |
| Record · Flow agent | 30 | [on update … subagent configs](operations-021.md#op-d4dd4b6d355b28) · [session tool config … one line](operations-022.md#op-5d3e4a68759ffe) |
| Record · Flow agent memory | 3 | [validate … on trash](operations-022.md#op-e88ba7a9c6ebff) |
| Service · Flow handlers | 15 | [initialize … resync](operations-022.md#op-4b31fac4011519) · [recheck … disconnect](operations-023.md#op-38399107622f1b) |
| Record · Flow knowledge base | 4 | [validate … after rename](operations-023.md#op-091b52060df757) |
| Record · Flow knowledge settings | 6 | [validate … require embedding model](operations-023.md#op-5d870ecdf49b6d) |
| Record · Flow knowledge source | 7 | [validate … reconcile](operations-023.md#op-b92a38a29aa561) |
| Record · Flow model | 15 | [validate … live models](operations-024.md#op-9e15ddbed4b612) |
| Record · Flow provider | 5 | [autoname … validate base url](operations-024.md#op-e1c25c978874aa) |
| Record · Flow run | 6 | [validate … validate status invariants](operations-024.md#op-62034f7b08414e) · [mark failed … json has items](operations-025.md#op-daac69d8c32e7c) |
| Record · Flow session | 36 | [before insert … entries](operations-025.md#op-37cbb29c7e5210) · [system prompt … row to message](operations-026.md#op-5ebb87e2512103) |
| Record · Flow session attachment | 29 | [build turn … model sees images](operations-026.md#op-3c53d3b7461d42) · [session model … xml attr](operations-027.md#op-ce795d1edfc78a) |
| Record · Flow settings | 1 | [validate](operations-027.md#op-287351dc0e4119) |
| Record · Flow skill | 14 | [before insert … before rename](operations-027.md#op-11b2a7f50b5b49) · [validate description … list files](operations-028.md#op-fe13d455162cb9) |
| Record · Flow tool | 13 | [validate … unavailable tools](operations-028.md#op-59bb841a4d1c66) |
| Record · Flow trigger | 10 | [before insert](operations-028.md#op-1cec15f4a10d19) · [before rename … validate template](operations-029.md#op-888507a03155c5) |
| Service · Handlers | 19 | [user room … doc open](operations-029.md#op-072be5829c1355) · [doc close … open in editor](operations-030.md#op-5ed4764ea22673) |
| Service · Ingest | 19 | [enqueue ingestion … mark failed](operations-030.md#op-8e8b0f169703ee) |
| Service · Knowledge | 9 | [initialize](operations-030.md#op-c36ecc6420eac2) · [add text … snippet](operations-031.md#op-8fb60bddf3ee84) |
| Service · Launcher | 2 | [add to page … get app roots](operations-031.md#op-bf5a3e44738702) |
| Service · Lifecycle | 41 | [after install … restart](operations-031.md#op-d80b585ef9ca60) · [start … sites dir](operations-032.md#op-dab1ca1d524037) · [flow bin … runtime dir](operations-033.md#op-6a50da162c4f77) |
| Service · Memory | 10 | [save memory … has memory tool](operations-033.md#op-13e8c0f1f16955) |
| Record · Milestone | 1 | [on doctype update](operations-033.md#op-65be37e0f21035) |
| Record · Milestone tracker | 5 | [on update … get milestone trackers](operations-033.md#op-78f4d694f06ba9) |
| Service · Model | 6 | [model config … site credentials](operations-033.md#op-2e44d8140e4c56) · [litellm route](operations-034.md#op-7d25f611a6c0f4) |
| Service · Permissions | 9 | [ensure flow role … skill query conditions](operations-034.md#op-ff6718e68604d8) |
| Service · Push notification | 18 | [initialize … site protocol](operations-034.md#op-71c681c9c14f38) · [site port … unsubscribe](operations-035.md#op-7680517840fc80) |
| Service · Queue | 5 | [queue status … clear effects](operations-035.md#op-b2fe3a45b2bcc6) |
| Service · Realtime | 22 | [publish progress … publish to user](operations-035.md#op-d0f5ec11c99a9d) · [publish to doc … getattr](operations-036.md#op-1cc4c99904e92e) |
| Service · Registry | 14 | [get automations for … discover app handlers](operations-036.md#op-3ffc1612808a78) |
| Service · Relationships | 26 | [get definitions … query](operations-036.md#op-08778760055684) · [get relationship definitions … query resolved](operations-037.md#op-7344495a31008f) |
| Record · Reminder | 5 | [clear old logs](operations-037.md#op-c38234d16b6cb8) · [validate … send reminders](operations-038.md#op-fb41eaf5037d50) |
| Service · Resolver | 16 | [resolve tool … annotated schema](operations-038.md#op-bb93ec0a189b5b) |
| Service · Retriever | 5 | [retrieve attachments … hydrate](operations-038.md#op-c0302e963cbb5d) · [source titles](operations-039.md#op-c8fd38d5df14a3) |
| Service · Runner | 107 | [execute automation … simulated wait](operations-039.md#op-3e7e1fa775d96a) · [begin event wait … settle queue row](operations-040.md#op-ac8ebec9033bcc) · [error summary … count](operations-041.md#op-3cb45c63aded6a) · [count web … initialize](operations-042.md#op-89978a725a7e9a) · [run … main](operations-043.md#op-8e909a4643a4f7) |
| Service · Safe exec | 23 | [safe exec … permissioned get value](operations-043.md#op-ca3512641c0160) · [permissioned get single value … get flow safe globals](operations-044.md#op-dbeeb16c415494) |
| Service · Scheduler | 22 | [process cron … condition columns](operations-044.md#op-45f0a12b86fa08) · [filter fieldnames … date payload](operations-045.md#op-95ebc54d543d80) |
| Service · Schema relationships | 19 | [get definitions … is queryable](operations-045.md#op-17d55f377173ed) · [ignored … references](operations-046.md#op-c8ee8923bea88c) |
| Service · Server | 11 | [connect … main](operations-046.md#op-ae13f3e8feb720) |
| Service · Session | 25 | [new session … find or create run](operations-046.md#op-0f7b923f9c86d9) · [add user message … default agent name](operations-047.md#op-5804ee8ecfffd3) |
| Service · Settings | 4 | [settings … skip automations](operations-047.md#op-a696bd555ab10b) |
| Service · Socket | 30 | [initialize … user type](operations-047.md#op-43d0298751a04b) · [installed apps … user of](operations-048.md#op-2497803cef2fee) · [has permission … run](operations-049.md#op-e41143301e98ff) |
| Service · Store | 29 | [db path … rename agent](operations-049.md#op-0a9b26b8ee9264) · [make personal … insert](operations-050.md#op-a409df15c1da2f) |
| Service · System generated | 8 | [validate immutable … skip if invalid](operations-050.md#op-16ec6403563a96) |
| Service · Tool | 12 | [post init … type to schema](operations-050.md#op-7c9fd321b9837e) · [inline pydantic refs … enum schema](operations-051.md#op-1bc528aff2985e) |
| Service · Trigger | 3 | [sync triggers … sync](operations-051.md#op-c34267c7addb61) |
| Service · Triggers | 9 | [dispatch … eval condition](operations-051.md#op-ee793f89a477f8) |
| Service · Util | 4 | [read header … get url](operations-051.md#op-ed647c0aa8eb5f) |
| Record · Workflow | 10 | [validate … update default workflow status](operations-051.md#op-e87ff6a3617814) · [validate docstatus … get workflow methods](operations-052.md#op-028cfb3a549146) |
| Record · Workflow action | 28 | [on doctype update … send workflow action email](operations-052.md#op-f433bb781a331d) · [deduplicate actions … get state optional field value](operations-053.md#op-4ddd191c078a0d) |
