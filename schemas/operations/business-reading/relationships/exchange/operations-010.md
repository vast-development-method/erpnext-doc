# Integrations and service calls · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Mirror sync

<a id="op-bcdc28432c1952"></a>
### Mirror Sync.should mirror

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_should_mirror`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · self.doc.get(self.DOCTYPE\_FIELD) belongs to ALLOWED\_DOCTYPES.

**Local steps**

- If self.doc.flags.get(MIRROR\_FLAG).
  - Return false.
- If not self.sync\_active().
  - Return false.
- Return self.doc.get(self.DOCTYPE\_FIELD) belongs to ALLOWED\_DOCTYPES.

**Methods declared on this owner** [sync active](operations-009.md#op-7221debb3c3236).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L3860) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1291) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1267)

<a id="op-88c7c909d8407d"></a>
### Mirror Sync.has data updated

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_has_data_updated`

**Inputs** self, old.

**Declared result** bool.

**Explicit results** (self.doc.get(self.DOCTYPE\_FIELD) differs from old.get(self.DOCTYPE\_FIELD) or self.doc.get(self.VALUE\_FIELD) differs from old.get(self.VALUE\_FIELD)).

**Local steps**

- Return (self.doc.get(self.DOCTYPE\_FIELD) differs from old.get(self.DOCTYPE\_FIELD) or self.doc.get(self.VALUE\_FIELD) differs from old.get(self.VALUE\_FIELD)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(self.DOCTYPE\_FIELD) differs from old.get(self.DOCTYPE\_FIELD) → self.doc.get(self.VALUE\_FIELD) differs from old.get(self.VALUE\_FIELD).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L4012) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1287) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1263)

<a id="op-f13fa8cb99b3dd"></a>
### Mirror Sync.target

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_target`

**Inputs** self.

**Explicit results** find\_target\_for(self.doc.get(self.DOCTYPE\_FIELD), self.doc.get(self.VALUE\_FIELD)).

**Local steps**

- Return find\_target\_for(self.doc.get(self.DOCTYPE\_FIELD), self.doc.get(self.VALUE\_FIELD)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L4179) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1294) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1270)

<a id="op-d2312fb38adf42"></a>
### Mirror Sync.dedup filter

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_dedup_filter`

**Inputs** self, target\_doctype, target\_value.

**Declared result** dict.

**Explicit results** filters.

**Local steps**

- Set filters from mapping(self.DOCTYPE\_FIELD → target\_doctype, self.VALUE\_FIELD → target\_value, “user” → self.doc.user).
- If self.\_extra\_dedup.
  - Evaluate filters.update(self.\_extra\_dedup(self.doc)).
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L4283) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1284) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1260)

<a id="op-25df0fd6dc8ee0"></a>
### Mirror Sync.find mirror

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_find_mirror`

**Inputs** self.

**Record and data access** read self.doc.doctype via get\_value · resolve a document from self.doc.doctype via get\_doc.

**Explicit results** no value · Platform.get\_doc(self.doc.doctype, name) when name, otherwise no value.

**Local steps**

- Set target from self.\_target().
- If not target.
  - Return no value.
- Set tuple(target\_doctype, target\_value) from target.
- Set filters from self.dedup\_filter(target\_doctype, target\_value).
- Set name from Platform.db.get\_value(self.doc.doctype, filters, “name”).
- Return Platform.get\_doc(self.doc.doctype, name) when name, otherwise no value.
  - Value choice on name — true gives Platform.get\_doc(self.doc.doctype, name), false gives no value.

**Methods declared on this owner** [target](operations-010.md#op-f13fa8cb99b3dd), [dedup filter](operations-010.md#op-d2312fb38adf42).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L4472) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1286) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1262)

<a id="op-b4045d2d3858db"></a>
### Mirror Sync.set mirror flags

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_set_mirror_flags`

**Inputs** self, mirror.

**Local steps**

- Set mirror.flags at MIRROR\_FLAG from true.
- For each tuple(flag, value) in self.\_extra\_mirror\_flags.items().
  - Set mirror.flags at flag from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L4706) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1290) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1266)

<a id="op-1664450b9e52a5"></a>
### Mirror Sync.mirror payload

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_mirror_payload`

**Inputs** self, target\_doctype, target\_value.

**Explicit results** data.

**Local steps**

- Set data from self.doc.as\_dict().
- For each k in \_SKIP\_PAYLOAD\_FIELDS.
  - Evaluate data.pop(k, no value).
- Set data at self.DOCTYPE\_FIELD from target\_doctype.
- Set data at self.VALUE\_FIELD from target\_value.
- Set data at “doctype” from self.doc.doctype.
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L4831) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1289) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1265)

<a id="op-44eccd90d5d0e3"></a>
### Mirror Sync.create mirror

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_create_mirror`

**Inputs** self.

**Record and data access** read self.doc.doctype via exists · resolve a document from self.\_mirror\_payload(target\_doctype, target\_value) via get\_doc.

**State and service calls** call insert on mirror.

**Explicit results** no value.

**Local steps**

- Set target from self.\_target().
- If not target.
  - Return no value.
- Set tuple(target\_doctype, target\_value) from target.
- If Platform.db.exists(self.doc.doctype, self.dedup\_filter(target\_doctype, target\_value)).
  - Return no value.
- Set mirror from Platform.get\_doc(self.\_mirror\_payload(target\_doctype, target\_value)).
- Evaluate self.set\_mirror\_flags(mirror).
- Evaluate mirror.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [target](operations-010.md#op-f13fa8cb99b3dd), [dedup filter](operations-010.md#op-d2312fb38adf42), [mirror payload](operations-010.md#op-1664450b9e52a5), [set mirror flags](operations-010.md#op-b4045d2d3858db).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L5033) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1283) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1259)

<a id="op-18e379f5db61df"></a>
### Mirror Sync.sync state to mirror

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_sync_state_to_mirror`

**Inputs** self.

**State and service calls** call save on mirror.

**Explicit results** no value.

**Local steps**

- Set mirror from self.find\_mirror().
- If not mirror.
  - Return no value.
- Set changed from false.
- For each tuple(field, value) in self.doc.as\_dict().items().
  - If (field belongs to \_SKIP\_PAYLOAD\_FIELDS or field belongs to tuple(self.DOCTYPE\_FIELD, self.VALUE\_FIELD)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field belongs to \_SKIP\_PAYLOAD\_FIELDS → field belongs to tuple(self.DOCTYPE\_FIELD, self.VALUE\_FIELD).
    - Continue with the next iteration or loop test.
  - If mirror.get(field) differs from value.
    - Evaluate mirror.set(field, value).
    - Set changed from true.
- If not changed.
  - Return no value.
- Evaluate self.set\_mirror\_flags(mirror).
- Evaluate mirror.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [find mirror](operations-010.md#op-25df0fd6dc8ee0), [set mirror flags](operations-010.md#op-b4045d2d3858db).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L5307) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1293) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1269)

<a id="op-46e9af01ae65e3"></a>
### Mirror Sync.delete mirror for

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_delete_mirror_for`

**Inputs** self, old.

**Record and data access** read self.doc.doctype via get\_value · resolve a document from self.doc.doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- Set old\_target from find\_target\_for(old.get(self.DOCTYPE\_FIELD), old.get(self.VALUE\_FIELD)).
- If not old\_target.
  - Return no value.
- Set tuple(target\_doctype, target\_value) from old\_target.
- Set filters from self.dedup\_filter(target\_doctype, target\_value).
- Set name from Platform.db.get\_value(self.doc.doctype, filters, “name”).
- If not name.
  - Return no value.
- Set mirror from Platform.get\_doc(self.doc.doctype, name).
- Evaluate self.set\_mirror\_flags(mirror).
- Evaluate mirror.delete(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [dedup filter](operations-010.md#op-d2312fb38adf42), [set mirror flags](operations-010.md#op-b4045d2d3858db).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L5663) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1285) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1261)

## Service · Notifications

<a id="op-92f59276db1a3b"></a>
### Get notifications

`operation_relationships_application_interface_notifications_business_behavior_get_notifications`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_value.

**Explicit results** \_notifications.

**Local steps**

- Set Notification from Platform.qb.DocType(“CRM Notification”).
- Set query from nested operand in the contract(nested operand in the contract).select(“\*”).where(Notification.to\_user equals Platform.session.user).orderby(“creation”, order = Order.desc).
- Set notifications from query.run(as\_dict = true).
- Set \_notifications from list().
- For each notification in notifications.
  - Evaluate \_notifications.append(mapping(“creation” → notification.creation, “from\_user” → mapping(“name” → notification.from\_user, “full\_name” → Platform.get\_value(“User”, notification.from\_user, “full\_name”)), “typ ….
    - Value choice on notification.reference\_doctype equals “CRM Deal” — true gives “deal”, false gives “lead”.
    - Value choice on notification.reference\_doctype equals “CRM Deal” — true gives “Deal”, false gives “Lead”.
- Return \_notifications.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L675) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L116) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L98)

<a id="op-e9b584d39ae478"></a>
### Mark as read

`operation_relationships_application_interface_notifications_business_behavior_mark_as_read`

**Inputs** doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Notification” via get\_all · resolve a document from “CRM Notification” via get\_doc.

**State and service calls** call save on d.

**Local steps**

- Set user from Platform.session.user.
- Set filters from mapping(“to\_user” → user, “read” → false).
- Set or\_filters from list().
- If doc.
  - Set or\_filters from list(mapping(“comment” → doc), mapping(“notification\_type\_doc” → doc)).
- For each n in Platform.get\_all(“CRM Notification”, filters = filters, or\_filters = or\_filters).
  - Set d from Platform.get\_doc(“CRM Notification”, n.name).
  - Set d.read from true.
  - Evaluate d.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L1358) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L117) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L99)

<a id="op-016a367b16f84e"></a>
### Get hash

`operation_relationships_application_interface_notifications_business_behavior_get_hash`

**Inputs** notification.

**Explicit results** \_hash.

**Local steps**

- Set \_hash from empty text.
- If (notification.type equals “Mention” and notification.notification\_type\_doc).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in notification.type equals “Mention” → notification.notification\_type\_doc.
  - Set \_hash from (“#” + notification.notification\_type\_doc).
  - If notification.notification\_type\_doctype equals “FCRM Note”.
    - Set \_hash from “#notes”.
- If notification.type equals “WhatsApp”.
  - Set \_hash from “#whatsapp”.
- If (notification.type equals “Assignment” and notification.notification\_type\_doctype equals “CRM Task”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in notification.type equals “Assignment” → notification.notification\_type\_doctype equals “CRM Task”.
  - Set \_hash from “#tasks”.
  - If “has been removed by” belongs to notification.message.
    - Set \_hash from empty text.
- Return \_hash.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L8) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L115) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L97)

## Service · Onboarding

<a id="op-7a81dc17bd9c20"></a>
### Complete setup for fc site

`operation_relationships_binding_crm_api_onboarding_complete_setup_for_fc_site`

**Inputs** login\_manager = no value.

**Explicit results** no value.

**Local steps**

- If not should\_auto\_complete\_setup().
  - Return no value.
- Bind dependencies setup\_complete.
- Attempt the following.
  - Evaluate setup\_complete(get\_prefilled\_setup\_args()).
- On failure (Exception).
  - Evaluate Platform.log\_error(“Platform Cloud setup auto-complete failed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L61) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L217) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L198)

<a id="op-edce1f623f683b"></a>
### Should auto complete setup

`operation_relationships_binding_crm_api_onboarding_should_auto_complete_setup`

**Inputs** no declared parameters.

**Explicit results** false · (has\_prefilled\_settings() and has\_non\_admin\_user()) · (is\_v2\_site() and has\_non\_admin\_user()).

**Local steps**

- Bind dependencies has\_non\_admin\_user.
- Bind dependencies is\_fc\_site.
- If (Platform.is\_setup\_complete() or Platform.conf.skip\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.is\_setup\_complete() → Platform.conf.skip\_setup\_wizard.
  - Return false.
- If apps\_need\_wizard\_input().
  - Return false.
- If is\_fc\_site().
  - Return (has\_prefilled\_settings() and has\_non\_admin\_user()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_prefilled\_settings() → has\_non\_admin\_user().
- Return (is\_v2\_site() and has\_non\_admin\_user()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_v2\_site() → has\_non\_admin\_user().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L65) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L221) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L202)

<a id="op-7dc6416e901163"></a>
### Is v2 site

`operation_relationships_binding_crm_api_onboarding_is_v2_site`

**Inputs** no declared parameters.

**Explicit results** false · is\_v2\_site().

**Local steps**

- Attempt the following.
  - Bind dependencies is\_v2\_site.
- On failure (ImportError).
  - Return false.
- Return is\_v2\_site().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L64) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L220) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L201)

<a id="op-886e478f378283"></a>
### Apps need wizard input

`operation_relationships_binding_crm_api_onboarding_apps_need_wizard_input`

**Inputs** no declared parameters.

**Explicit results** true · false.

**Local steps**

- For each app in Platform.get\_installed\_apps().
  - Set hooks from Platform.get\_hooks(app\_name = app).
  - If (hooks.get(“setup\_wizard\_stages”) or hooks.get(“setup\_wizard\_complete”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.get(“setup\_wizard\_stages”) → hooks.get(“setup\_wizard\_complete”).
    - Return true.
- Return false.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L60) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L216) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L197)

<a id="op-ca496cf6ffc70d"></a>
### Has prefilled settings

`operation_relationships_binding_crm_api_onboarding_has_prefilled_settings`

**Inputs** no declared parameters.

**Record and data access** read “System Settings” via get\_single.

**Explicit results** bool((settings.country and settings.time\_zone and settings.currency)).

**Local steps**

- Set settings from Platform.get\_single(“System Settings”).
- Return bool((settings.country and settings.time\_zone and settings.currency)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.country → settings.time\_zone → settings.currency.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L63) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L219) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L200)

<a id="op-83a9077a7ebf88"></a>
### Get prefilled setup args

`operation_relationships_binding_crm_api_onboarding_get_prefilled_setup_args`

**Inputs** no declared parameters.

**Record and data access** read “System Settings” via get\_single · read “Language” via get\_value.

**Explicit results** mapping(“language” → language, “lang” → language, “country” → settings.country, “timezone” → settings.time\_zone, …).

**Local steps**

- Set settings from Platform.get\_single(“System Settings”).
- Set language from (Platform.db.get\_value(“Language”, settings.language, “language\_name”) or “English”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Language”, settings.language, “language\_name”) → “English”.
- Return mapping(“language” → language, “lang” → language, “country” → settings.country, “timezone” → settings.time\_zone, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L62) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L218) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L199)

<a id="op-578ac5a11ab622"></a>
### Get first lead

`operation_relationships_application_interface_onboarding_business_behavior_get_first_lead`

**Inputs** name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Lead” via get\_list.

**Explicit results** name · lead at 0 when lead, otherwise no value.

**Local steps**

- If (name and Platform.get\_list(“CRM Lead”, filters = mapping(“name” → name, “converted” → 0), pluck = “name”, limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name → Platform.get\_list(“CRM Lead”, filters = mapping(“name” → name, “converted” → 0), pluck = “name”, limit = 1).
  - Return name.
- Set lead from Platform.get\_list(“CRM Lead”, filters = mapping(“converted” → 0), pluck = “name”, order\_by = “creation”, limit = 1).
- Return lead at 0 when lead, otherwise no value.
  - Value choice on lead — true gives lead at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L10) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L119) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L101)

<a id="op-1a7a8d9c3f229b"></a>
### Get first deal

`operation_relationships_application_interface_onboarding_business_behavior_get_first_deal`

**Inputs** name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Deal” via get\_list.

**Explicit results** name · deal at 0 when deal, otherwise no value.

**Local steps**

- If (name and Platform.get\_list(“CRM Deal”, filters = mapping(“name” → name), pluck = “name”, limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name → Platform.get\_list(“CRM Deal”, filters = mapping(“name” → name), pluck = “name”, limit = 1).
  - Return name.
- Set deal from Platform.get\_list(“CRM Deal”, pluck = “name”, order\_by = “creation”, limit = 1).
- Return deal at 0 when deal, otherwise no value.
  - Value choice on deal — true gives deal at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L9) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L118) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L100)

## Service · Session

<a id="op-54ac7c091e1750"></a>
### Get session role flags

`operation_relationships_application_interface_session_business_behavior_get_session_role_flags`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L2295) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L143) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L124)

<a id="op-eb7e5e3ae4e318"></a>
### Get users

`operation_relationships_application_interface_session_business_behavior_get_users`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** include\_all.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 10 condition or selection sites, 3 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L2582) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L145) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L126)

<a id="op-d9ac007c90c267"></a>
### Get user info

`operation_relationships_application_interface_session_business_behavior_get_user_info`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** users.

**Explicit result forms** a structured result, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L4003) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L144) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L125)
