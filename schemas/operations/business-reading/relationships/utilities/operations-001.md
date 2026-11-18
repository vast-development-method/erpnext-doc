# Supporting services · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Activation

<a id="op-e1caa98e6f720d"></a>
### Get site info

`operation_relationships_activation_business_behavior_get_site_info`

**Inputs** site\_info.

**Explicit results** mapping(“activation” → get\_sales\_data(site\_info)).

**Local steps**

- Return mapping(“activation” → get\_sales\_data(site\_info)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L3) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L3)

<a id="op-55fbb0649dea2c"></a>
### Get sales data

`operation_relationships_activation_business_behavior_get_sales_data`

**Inputs** site\_info.

**Record and data access** read doctype via count.

**Explicit results** mapping(“activation\_level” → activation\_level, “sales\_data” → sales\_data).

**Local steps**

- Set activation\_level from site\_info.get(“activation”, mapping()).get(“activation\_level”, 0).
- Set sales\_data from site\_info.get(“activation”, mapping()).get(“sales\_data”, list()).
- Set doctypes from list(“CRM Lead”, “CRM Deal”, “CRM Organization”, “Contact”, …).
- For each doctype in doctypes.
  - Set count from Platform.db.count(doctype).
  - Evaluate sales\_data.append(mapping(doctype → count)).
- Return mapping(“activation\_level” → activation\_level, “sales\_data” → sales\_data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L70) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L2) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L2)

## Service · Activities

<a id="op-f77faabbf85235"></a>
### Create demo activities

`operation_relationships_demo_activities_business_behavior_create_demo_activities`

**Inputs** lead\_names, demo\_users.

**Explicit results** mapping(“comments” → comment\_names, “communications” → communication\_names).

**Local steps**

- Set tuple(session\_user, owner\_1, owner\_2, \_) from resolve\_owners(demo\_users).
- Set \_full\_names from build\_full\_names(session\_user).
- Set now from datetime.now().
- Set comment\_names from \_create\_comments(lead\_names, session\_user, owner\_1, owner\_2, …).
- Set communication\_names from \_create\_communications(lead\_names, session\_user, owner\_1, \_full\_names, …).
- Evaluate \_create\_versions(lead\_names, session\_user, owner\_1, owner\_2, …).
- Return mapping(“comments” → comment\_names, “communications” → communication\_names).

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L4792) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L389) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L370)

<a id="op-5940aedf742ab1"></a>
### Create comments

`operation_relationships_demo_activities_business_behavior_create_comments`

**Inputs** lead\_names, session\_user, owner\_1, owner\_2, full\_names, now.

**Explicit results** list of insert\_comment(“CRM Lead”, data at “lead”, data at “owner”, data at “content”, …) for data drawn from comments\_data.

**Local steps**

- Set comments\_data from list(mapping(“lead” → lead\_names at 0, “owner” → session\_user, “content” → text in the contract, “days\_ago” → 56), mapping(“lead” → lead\_names at 1, “owner” → owner\_1, “content” → text in the contract, “da ….
- Return list of insert\_comment(“CRM Lead”, data at “lead”, data at “owner”, data at “content”, …) for data drawn from comments\_data.
  - Draw data from comments\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L5088) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L387) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L368)

<a id="op-5a1f6927efdc8d"></a>
### Create communications

`operation_relationships_demo_activities_business_behavior_create_communications`

**Inputs** lead\_names, session\_user, owner\_1, full\_names, now.

**Explicit results** list of insert\_communication(“CRM Lead”, data at “lead”, data, full\_names, …) for data drawn from comms\_data.

**Local steps**

- Set lead\_emails from mapping(lead\_names at 0 → “alice.johnson@example.com”, lead\_names at 1 → “bob.martinez@example.com”, lead\_names at 3 → “david.lee@example.com”).
- Set comms\_data from list(mapping(“lead” → lead\_names at 0, “owner” → session\_user, “sent\_or\_received” → “Sent”, “subject” → “Following up on our discovery call — Acme Corp”, …), mapping(“lead” → lead\_names at 1, “owner” → own ….
- Return list of insert\_communication(“CRM Lead”, data at “lead”, data, full\_names, …) for data drawn from comms\_data.
  - Draw data from comms\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L5585) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L388) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L369)

<a id="op-999fc2eeb955cf"></a>
### Create versions

`operation_relationships_demo_activities_business_behavior_create_versions`

**Inputs** lead\_names, session\_user, owner\_1, owner\_2, now.

**Local steps**

- Set versions\_data from list(mapping(“lead” → lead\_names at 0, “owner” → session\_user, “changed” → list(list(“no\_of\_employees”, “201-500”, “501-1000”)), “days\_ago” → 52), mapping(“lead” → lead\_names at 1, “owner” → owner\_1, “chan ….
- For each data in versions\_data.
  - Evaluate insert\_version(“CRM Lead”, data at “lead”, data at “owner”, data at “changed”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L6278) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L390) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L371)

<a id="op-fc3066880f346a"></a>
### Delete demo activities

`operation_relationships_demo_activities_business_behavior_delete_demo_activities`

**Inputs** activity\_data.

**Record and data access** read “Communication” via exists.

**State and service calls** request delete\_doc for “Communication”.

**Local steps**

- Set communication\_names from activity\_data.get(“communications”, list()).
- For each name in communication\_names.
  - If Platform.db.exists(“Communication”, name).
    - Evaluate Platform.delete\_doc(“Communication”, name, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L6827) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L391) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L372)

## Service · Api

<a id="op-add6f44aa5fada"></a>
### Create demo data

`operation_relationships_demo_application_interface_business_behavior_create_demo_data`

**Inputs** \_args = no value.

**Explicit results** no value.

**Local steps**

- If Platform.db.get\_default(DEMO\_STATE\_KEY).
  - Return no value.
- Bind dependencies create\_demo\_activities.
- Bind dependencies create\_demo\_call\_logs.
- Bind dependencies create\_demo\_deals.
- Bind dependencies create\_demo\_leads.
- Bind dependencies create\_demo\_notes.
- Bind dependencies create\_demo\_tasks.
- Bind dependencies create\_demo\_users.
- Set demo\_users from create\_demo\_users().
- Set lead\_names from create\_demo\_leads(demo\_users).
- Set note\_names from create\_demo\_notes(lead\_names, demo\_users).
- Set task\_names from create\_demo\_tasks(lead\_names, demo\_users).
- Set call\_log\_names from create\_demo\_call\_logs(lead\_names, demo\_users).
- Set activity\_data from create\_demo\_activities(lead\_names, demo\_users).
- Bind dependencies rebackdate\_demo\_leads.
- Evaluate rebackdate\_demo\_leads(lead\_names, demo\_users).
- Set deal\_data from create\_demo\_deals(lead\_names, demo\_users).
- Evaluate Platform.db.set\_default(DEMO\_LEADS\_KEY, json.dumps(lead\_names)).
- Evaluate Platform.db.set\_default(DEMO\_NOTES\_KEY, json.dumps(note\_names)).
- Evaluate Platform.db.set\_default(DEMO\_TASKS\_KEY, json.dumps(task\_names)).
- Evaluate Platform.db.set\_default(DEMO\_CALL\_LOGS\_KEY, json.dumps(call\_log\_names)).
- Evaluate Platform.db.set\_default(DEMO\_ACTIVITIES\_KEY, json.dumps(activity\_data)).
- Evaluate Platform.db.set\_default(DEMO\_DEALS\_KEY, json.dumps(deal\_data)).
- Evaluate Platform.db.set\_default(DEMO\_STATE\_KEY, “1”).
- Evaluate capture(“demo\_data\_created”, “crm”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L7001) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L393) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L374)

<a id="op-40abdde6814568"></a>
### Clear demo data

`operation_relationships_demo_application_interface_business_behavior_clear_demo_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- Evaluate Platform.only\_for(list(“Sales Manager”, “System Manager”), true).
- If not Platform.db.get\_default(DEMO\_STATE\_KEY).
  - Return no value.
- Bind dependencies delete\_demo\_activities.
- Bind dependencies delete\_demo\_call\_logs.
- Bind dependencies delete\_demo\_deals.
- Bind dependencies delete\_demo\_leads.
- Bind dependencies delete\_demo\_notes.
- Bind dependencies delete\_demo\_tasks.
- Bind dependencies DEMO\_USER\_EMAILS, delete\_demo\_users.
- Set lead\_names from json.loads((Platform.db.get\_default(DEMO\_LEADS\_KEY) or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(DEMO\_LEADS\_KEY) → “&#91;&#93;”.
- Set note\_names from json.loads((Platform.db.get\_default(DEMO\_NOTES\_KEY) or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(DEMO\_NOTES\_KEY) → “&#91;&#93;”.
- Set task\_names from json.loads((Platform.db.get\_default(DEMO\_TASKS\_KEY) or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(DEMO\_TASKS\_KEY) → “&#91;&#93;”.
- Set call\_log\_names from json.loads((Platform.db.get\_default(DEMO\_CALL\_LOGS\_KEY) or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(DEMO\_CALL\_LOGS\_KEY) → “&#91;&#93;”.
- Set activity\_data from json.loads((Platform.db.get\_default(DEMO\_ACTIVITIES\_KEY) or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(DEMO\_ACTIVITIES\_KEY) → “{}”.
- Set deal\_data from json.loads((Platform.db.get\_default(DEMO\_DEALS\_KEY) or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(DEMO\_DEALS\_KEY) → “{}”.
- Evaluate delete\_demo\_deals(deal\_data, lead\_names).
- Evaluate delete\_demo\_activities(activity\_data).
- Evaluate delete\_demo\_notes(note\_names).
- Evaluate delete\_demo\_tasks(task\_names).
- Evaluate delete\_demo\_call\_logs(call\_log\_names).
- Evaluate delete\_demo\_leads(lead\_names).
- Evaluate delete\_demo\_users(DEMO\_USER\_EMAILS).
- Evaluate Platform.db.set\_default(DEMO\_LEADS\_KEY, no value).
- Evaluate Platform.db.set\_default(DEMO\_NOTES\_KEY, no value).
- Evaluate Platform.db.set\_default(DEMO\_TASKS\_KEY, no value).
- Evaluate Platform.db.set\_default(DEMO\_CALL\_LOGS\_KEY, no value).
- Evaluate Platform.db.set\_default(DEMO\_ACTIVITIES\_KEY, no value).
- Evaluate Platform.db.set\_default(DEMO\_DEALS\_KEY, no value).
- Evaluate Platform.db.set\_default(DEMO\_STATE\_KEY, no value).
- Evaluate capture(“demo\_data\_cleared”, “crm”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(list(“Sales Manager”, “System Manager”), true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L392) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L373)

<a id="op-b0f2d9bd9a547f"></a>
### Get demo state

`operation_relationships_demo_application_interface_business_behavior_get_demo_state`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“demo\_data\_created” → bool(Platform.db.get\_default(DEMO\_STATE\_KEY))).

**Local steps**

- Return mapping(“demo\_data\_created” → bool(Platform.db.get\_default(DEMO\_STATE\_KEY))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L909) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L394) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L375)

## Service · Call logs

<a id="op-8659d70d71decb"></a>
### Create demo call logs

`operation_relationships_demo_call_logs_business_behavior_create_demo_call_logs`

**Inputs** lead\_names, demo\_users.

**Record and data access** resolve a document from mapping(“doctype” → “CRM Call Log”, “id” → Platform.generate\_hash(length = 10), expand data) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Call Log”, “id” → Platform.generate\_hash(length = 10), expand data)) · request set\_value on “CRM Call Log”.

**Explicit results** created.

**Local steps**

- Bind dependencies datetime, timedelta.
- Set now from datetime.now().
- Set tuple(session\_user, owner\_1, owner\_2, \_) from resolve\_owners(demo\_users).
- Set \_user\_mobile from mapping of u at “email” → u at “mobile\_no” for u drawn from DEMO\_USERS.
  - Draw u from DEMO\_USERS.
- Set rep\_numbers from mapping(session\_user → \_user\_mobile.get(session\_user, “+1 555 100 0001”), owner\_1 → \_user\_mobile.get(owner\_1, “+1 555 100 0002”), owner\_2 → \_user\_mobile.get(owner\_2, “+1 555 100 0003”)).
- Set call\_logs\_data from list(mapping(“type” → “Outgoing”, “status” → “Completed”, “telephony\_medium” → “Manual”, “duration” → 720, …), mapping(“type” → “Incoming”, “status” → “Completed”, “telephony\_medium” → “Manual”, “duration” ….
- Set created from list().
- For each data in call\_logs\_data.
  - Set log\_owner from (data.get(“caller”) or data.get(“receiver”) or Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.get(“caller”) → data.get(“receiver”) → Platform.session.user.
  - Set log\_ts from data.get(“start\_time”).
  - Set log from Platform.get\_doc(mapping(“doctype” → “CRM Call Log”, “id” → Platform.generate\_hash(length = 10), expand data)).insert(ignore\_permissions = true).
  - Set patch from mapping(“owner” → log\_owner, “modified\_by” → log\_owner).
  - If log\_ts.
    - Set patch at “creation” from log\_ts.
    - Set patch at “modified” from log\_ts.
  - Evaluate Platform.db.set\_value(“CRM Call Log”, log.name, patch, update\_modified = false).
  - Evaluate created.append(log.name).
- Return created.

**Values supplied outside this operation** clock or generated value from datetime.now(), Platform.generate\_hash(length = 10).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L1002) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L395) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L376)

<a id="op-c7df2266ea9640"></a>
### Delete demo call logs

`operation_relationships_demo_call_logs_business_behavior_delete_demo_call_logs`

**Inputs** call\_log\_names.

**Record and data access** read “CRM Call Log” via exists.

**State and service calls** request delete\_doc for “CRM Call Log”.

**Local steps**

- For each name in call\_log\_names.
  - If Platform.db.exists(“CRM Call Log”, name).
    - Evaluate Platform.delete\_doc(“CRM Call Log”, name, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L3403) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L396) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L377)

## Service · Crm

<a id="op-d1a43963ed5916"></a>
### Get context

`operation_relationships_public_pages_customer_relationship_management_business_behavior_get_context`

**Inputs** no declared parameters.

**State and service calls** commit.

**Explicit results** context.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have permission to access Platform CRM”.

**Local steps**

- Bind dependencies check\_app\_permission.
- If not check\_app\_permission().
  - Call the validation error handler Platform.throw(translated “You do not have permission to access Platform CRM”, Platform.PermissionError).
- Evaluate redirect\_to\_set\_password().
- Evaluate Platform.db.commit().
- Set context from Platform.\_dict().
- Set context.boot from get\_boot().
- If Platform.session.user differs from “Guest”.
  - Evaluate capture(“active\_site”, “crm”).
- Return context.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L4715) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1488) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1462)

<a id="op-3f7206bb12ac95"></a>
### Redirect to set password

`operation_relationships_public_pages_customer_relationship_management_business_behavior_redirect_to_set_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Locally raised failures** redirect.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L4967) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1492) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1466)

<a id="op-11faa31b586dfb"></a>
### Get context for dev

`operation_relationships_public_pages_customer_relationship_management_business_behavior_get_context_for_development`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”), allow\_guest = true).

**Explicit results** get\_boot().

**Explicit failure paths** validation helper — translated “This method is only meant for developer mode”.

**Local steps**

- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “This method is only meant for developer mode”).
- Return get\_boot().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L5200) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1489) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1463)

<a id="op-c2c945cd0271b6"></a>
### Get boot

`operation_relationships_public_pages_customer_relationship_management_business_behavior_get_boot`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.\_dict(mapping(“Platform\_version” → Platform.\_\_version\_\_, “has\_automation\_engine” → HAS\_AUTOMATION\_ENGINE, “default\_route” → get\_default\_route(), “site\_name” → Platform.local.site, …)).

**Local steps**

- Return Platform.\_dict(mapping(“Platform\_version” → Platform.\_\_version\_\_, “has\_automation\_engine” → HAS\_AUTOMATION\_ENGINE, “default\_route” → get\_default\_route(), “site\_name” → Platform.local.site, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“User”, Platform.session.user, “time\_zone”) → get\_system\_timezone().

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“setup\_complete”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L37) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1487) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1461)

<a id="op-ac4589392d08f9"></a>
### Get cloud settings

`operation_relationships_binding_crm_www_crm_get_cloud_settings`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“enabled” → false) · get\_boot\_context().

**Local steps**

- Attempt the following.
  - Bind dependencies get\_boot\_context.
- On failure (ImportError).
  - Return mapping(“enabled” → false).
- Return get\_boot\_context().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L230) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L386) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L367)

<a id="op-dff6ffdbd94280"></a>
### Get state options

`operation_relationships_public_pages_customer_relationship_management_business_behavior_get_state_options`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, list at str).

**Explicit results** mapping() · mapping(“India” → list(INDIAN\_STATES)).

**Local steps**

- Attempt the following.
  - If “india\_compliance” does not belong to get\_installed\_apps().
    - Return mapping().
  - Bind dependencies INDIAN\_STATES.
  - Return mapping(“India” → list(INDIAN\_STATES)).
- On failure (Exception).
  - Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L5857) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1491) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1465)

<a id="op-d7dfa0dcafc566"></a>
### Get default route

`operation_relationships_public_pages_customer_relationship_management_business_behavior_get_default_route`

**Inputs** no declared parameters.

**Explicit results** “/crm”.

**Local steps**

- Return “/crm”.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L6011) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1490) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1464)

## Service · Crm form

<a id="op-53b5b6f5c0b74f"></a>
### Get context

`operation_relationships_public_pages_customer_relationship_management_form_business_behavior_get_context`

**Inputs** context.

**Record and data access** read “Web Form” via get\_value · resolve a document from “Web Form” via get\_doc.

**Explicit results** context.

**Explicit failure paths** Platform.DoesNotExistError.

**Local steps**

- Set route from resolve\_route().
- Set filters from mapping(“route” → route, “crm\_published” → 1, “doc\_type” → list(“in”, ALLOWED\_DOCTYPES)).
- Set name from Platform.db.get\_value(“Web Form”, filters).
- Set is\_author from (Platform.session.user differs from “Guest” and bool((set(Platform.get\_roles()) bitwise and set(“System Manager”, “Sales Manager”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user differs from “Guest” → bool((set(Platform.get\_roles()) bitwise and set(“System Manager”, “Sales Manager”))).
- If (not name and is\_author).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not name → is\_author.
  - Set name from Platform.db.get\_value(“Web Form”, mapping(“route” → route, “doc\_type” → list(“in”, ALLOWED\_DOCTYPES))).
- If not name.
  - Raise Platform.DoesNotExistError.
- Set doc from Platform.get\_doc(“Web Form”, name).
- Evaluate set\_embedding\_headers(doc).
- Set context.no\_cache from 1.
- Attempt the following.
  - Set context.csrf\_token from Platform.sessions.get\_csrf\_token().
- On failure (Exception).
  - Set context.csrf\_token from empty text.
- Set context.web\_form\_name from doc.name.
- Set context.form\_doctype from doc.doc\_type.
- Set context.embed from Platform.form\_dict.get(“embed”) belongs to tuple(“1”, “true”, “yes”).
- Set context.draft\_preview from not doc.crm\_published.
- Set context.form\_title from doc.title.
- Set context.form\_description from (doc.introduction\_text or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.introduction\_text → empty text.
- Set context.form\_route from doc.route.
- Set context.submit\_label from (doc.button\_label or “Submit”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.button\_label → “Submit”.
- Set context.success\_message from (doc.success\_message or “Thank you!”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.success\_message → “Thank you!”.
- Set context.success\_url from (doc.success\_url or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.success\_url → empty text.
- Set context.fields from list of mapping(“fieldname” → f.fieldname, “label” → (f.label or empty text when f.fieldtype belongs to tuple(“Section Break”, “Column Break”), otherwise f.fieldname), “fieldtype” → f.fieldtype, “options”  ….
  - Draw f from doc.web\_form\_fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.label → empty text when f.fieldtype belongs to tuple(“Section Break”, “Column Break”), otherwise f.fieldname.
  - Value choice on f.fieldtype belongs to tuple(“Section Break”, “Column Break”) — true gives empty text, false gives f.fieldname.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.options → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.reqd → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.get(“placeholder”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.description → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.depends\_on → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.mandatory\_depends\_on → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.read\_only\_depends\_on → empty text.
- Set context.layout from build\_layout(context.fields).
- Set context.link\_options from mapping of f at “fieldname” → \_link\_field\_options(f at “options”) for f drawn from context.fields where (f at “fieldtype” equals “Link” and f at “options”).
  - Draw f from context.fields, keep a combination only if ((f at “fieldtype” equals “Link” and f at “options”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f at “fieldtype” equals “Link” → f at “options”.
- Return context.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L38) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1494) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1468)

<a id="op-e88164d5c72adc"></a>
### Link field options

`operation_relationships_public_pages_customer_relationship_management_form_business_behavior_link_field_options`

**Inputs** doctype.

**Declared result** list at dict.

**Record and data access** read “DocType” via exists.

**Explicit results** list() · list of mapping(“value” → r at “name”, “label” → (r.get(title\_field) or r at “name”)) for r drawn from rows.

**Local steps**

- If (not doctype or not Platform.db.exists(“DocType”, doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not Platform.db.exists(“DocType”, doctype).
  - Return list().
- If not guest\_can\_select(doctype).
  - Return list().
- Set meta from Platform.get\_meta(doctype).
- Set title\_field from (meta.title\_field or “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.title\_field → “name”.
- Set fields from list(“name”) when title\_field equals “name”, otherwise list(“name”, title\_field).
  - Value choice on title\_field equals “name” — true gives list(“name”), false gives list(“name”, title\_field).
- Bind local operation \_query for subsequent calls.
- Set current\_user from Platform.session.user.
- If current\_user equals “Guest”.
  - Set rows from \_query().
- Otherwise.
  - Set saved\_sid from Platform.session.sid.
  - Set saved\_data from Platform.session.data.
  - Attempt the following.
    - Evaluate Platform.set\_user(“Guest”).
    - Set rows from \_query().
  - On exit, including pending return or failure.
    - Evaluate Platform.set\_user(current\_user).
    - Set Platform.session.sid from saved\_sid.
    - Set Platform.session.data from saved\_data.
- Return list of mapping(“value” → r at “name”, “label” → (r.get(title\_field) or r at “name”)) for r drawn from rows.
  - Draw r from rows.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in r.get(title\_field) → r at “name”.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0068.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1495) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1469)

<a id="op-e1361051925831"></a>
### Link field options.query

`operation_relationships_public_pages_customer_relationship_management_form_business_behavior_link_field_options_query`

**Inputs** no declared parameters.

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, fields = fields, order\_by = formatted text {title\_field} asc, limit = MAX\_LINK\_OPTIONS).

**Local steps**

- Return Platform.get\_list(doctype, fields = fields, order\_by = formatted text {title\_field} asc, limit = MAX\_LINK\_OPTIONS).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0068.json#L696) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1496) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1470)

<a id="op-1fdfc7f470b41a"></a>
### Set embedding headers

`operation_relationships_public_pages_customer_relationship_management_form_business_behavior_set_embedding_headers`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- Set raw\_domains from (doc.allowed\_embedding\_domains or empty text).split().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.allowed\_embedding\_domains → empty text.
- Set domains from list of d for d drawn from raw\_domains where ALLOWED\_EMBEDDING\_DOMAIN\_RE.match(d).
  - Draw d from raw\_domains, keep a combination only if (ALLOWED\_EMBEDDING\_DOMAIN\_RE.match(d)).
- If not domains.
  - Return no value.
- Set Platform.local.response\_headers at “Content-Security-Policy” from (“frame-ancestors 'self' ” + one space.join(domains)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0068.json#L788) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1498) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1472)

<a id="op-453677ff9508f7"></a>
### Build layout

`operation_relationships_public_pages_customer_relationship_management_form_business_behavior_build_layout`

**Inputs** fields.

**Explicit results** list of s for s drawn from sections where (s at “label” or any(generator of col for col drawn from s at “columns”)).

**Local steps**

- Set sections from list().
- Set current from mapping(“label” → no value, “columns” → list(list())).
- For each f in fields.
  - Set ft from f at “fieldtype”.
  - If ft equals “Section Break”.
    - Evaluate sections.append(current).
    - Set current from mapping(“label” → (f.get(“label”) or no value), “columns” → list(list())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.get(“label”) → no value.
  - Otherwise.
    - If ft equals “Column Break”.
      - Evaluate current at “columns”.append(list()).
    - Otherwise.
      - Evaluate current at “columns” at negative 1.append(f).
- Evaluate sections.append(current).
- Return list of s for s drawn from sections where (s at “label” or any(generator of col for col drawn from s at “columns”)).
  - Draw s from sections, keep a combination only if ((s at “label” or any(generator of col for col drawn from s at “columns”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in s at “label” → any(generator of col for col drawn from s at “columns”).
  - Draw col from s at “columns”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0068.json#L981) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1493) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1467)
