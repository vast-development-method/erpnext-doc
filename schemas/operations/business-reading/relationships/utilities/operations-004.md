# Supporting services · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Search sqlite

<a id="op-8be92682c09e28"></a>
### CRMSearch.index doc

`operation_relationships_binding_crm_search_sqlite_crmsearch_index_doc`

**Inputs** self, doctype, docname.

**Local steps**

- Attempt the following.
  - Evaluate super().index\_doc(doctype, docname).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = formatted text CRM search: failed to index {doctype} {docname}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L223) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L379) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L360)

<a id="op-de6ad60c3230ec"></a>
### CRMSearch.remove doc

`operation_relationships_binding_crm_search_sqlite_crmsearch_remove_doc`

**Inputs** self, doctype, docname.

**Local steps**

- Attempt the following.
  - Evaluate super().remove\_doc(doctype, docname).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = formatted text CRM search: failed to remove {doctype} {docname}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L225) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L381) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L362)

<a id="op-fa1fd717bf5b3a"></a>
### Parent key

`operation_relationships_binding_crm_search_sqlite_parent_key`

**Inputs** doctype, name.

**Declared result** str.

**Explicit results** formatted text {doctype}:{name}.

**Local steps**

- Return formatted text {doctype}:{name}.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L227) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L383) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L364)

<a id="op-ffdc46a45aa831"></a>
### Strip quoted reply

`operation_relationships_binding_crm_search_sqlite_strip_quoted_reply`

**Inputs** html.

**Declared result** str.

**Explicit results** EmailReplyParser.parse\_reply(soup.get\_text(whitespace '\\n')).

**Local steps**

- Set soup from BeautifulSoup(html, “html.parser”).
- For each quote in soup.select(QUOTE\_SELECTORS).
  - Evaluate quote.decompose().
- Return EmailReplyParser.parse\_reply(soup.get\_text(whitespace '\\n')).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L228) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L384) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L365)

<a id="op-dfe99ed58a10de"></a>
### Matches filters

`operation_relationships_binding_crm_search_sqlite_matches_filters`

**Inputs** doc, filters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- For each tuple(field, value) in filters.items().
  - Set actual from doc.get(field).
  - If isinstance(value, tuple).
    - If actual does not belong to value at 1.
      - Return false.
  - Otherwise.
    - If actual differs from value.
      - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L226) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L382) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L363)

## Service · Tasks

<a id="op-2a3d33cc8a1ad6"></a>
### Create demo tasks

`operation_relationships_demo_tasks_business_behavior_create_demo_tasks`

**Inputs** lead\_names, demo\_users.

**Record and data access** resolve a document from mapping(“doctype” → “CRM Task”, expand data) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Task”, expand data)).

**Explicit results** created.

**Local steps**

- Bind dependencies date, datetime, timedelta.
- Set today from date.today().
- Set now from datetime.now().
- Set tuple(session\_user, owner\_1, owner\_2, \_) from resolve\_owners(demo\_users).
- Set tasks\_data from list(mapping(“title” → “Send proposal document”, “priority” → “High”, “status” → “Todo”, “assigned\_to” → session\_user, …), mapping(“title” → “Schedule technical demo”, “priority” → “Medium”, “status” → “In ….
- Set created from list().
- For each data in tasks\_data.
  - Set owner from data at “assigned\_to”.
  - Set ts from (now − timedelta(days = data.pop(“days\_ago”))).
  - Set task from Platform.get\_doc(mapping(“doctype” → “CRM Task”, expand data)).insert(ignore\_permissions = true).
  - Evaluate backdate(“CRM Task”, task.name, owner, ts).
  - Evaluate created.append(task.name).
- Return created.

**Values supplied outside this operation** clock or generated value from date.today(), datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L5756) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L407) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L388)

<a id="op-99327b87af6ecc"></a>
### Delete demo tasks

`operation_relationships_demo_tasks_business_behavior_delete_demo_tasks`

**Inputs** task\_names.

**Record and data access** read “CRM Task” via exists.

**State and service calls** request delete\_doc for “CRM Task”.

**Local steps**

- For each name in task\_names.
  - If Platform.db.exists(“CRM Task”, name).
    - Evaluate Platform.delete\_doc(“CRM Task”, name, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L408) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L389)

## Service · Telemetry

<a id="op-89447f9d594ac8"></a>
### Capture feature state

`operation_relationships_telemetry_business_behavior_capture_feature_state`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not is\_pulse\_enabled().
  - Return no value.
- Set properties from mapping().
- For each collect in tuple(lead\_sync\_state, product\_sync\_state, sales\_hierarchy\_state).
  - Attempt the following.
    - Evaluate properties.update(collect()).
  - On failure (Exception).
    - Evaluate Platform.log\_error(formatted text Feature state telemetry failed: {collect.\_\_name\_\_}).
- If properties.
  - Evaluate capture(“crm\_feature\_state”, “crm”, properties = properties, interval = “1d”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0058.json#L2699) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1499) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1473)

<a id="op-c16a7d5d3232d3"></a>
### Lead sync state

`operation_relationships_telemetry_business_behavior_lead_sync_state`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “Lead Sync Source” via get\_all.

**Explicit results** mapping(“lead\_sync\_enabled” → bool(enabled\_types), “lead\_sync\_sources” → len(sources), “lead\_sync\_source\_types” → sorted(enabled\_types), “leads\_synced\_total” → count\_synced\_leads(), …).

**Local steps**

- Set sources from Platform.get\_all(“Lead Sync Source”, fields = list(“type”, “enabled”)).
- Set enabled\_types from set of s.type for s drawn from sources where s.enabled.
  - Draw s from sources, keep a combination only if (s.enabled).
- Return mapping(“lead\_sync\_enabled” → bool(enabled\_types), “lead\_sync\_sources” → len(sources), “lead\_sync\_source\_types” → sorted(enabled\_types), “leads\_synced\_total” → count\_synced\_leads(), …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0058.json#L2940) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1501) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1475)

<a id="op-ead1c895bfc6a3"></a>
### Count synced leads

`operation_relationships_telemetry_business_behavior_count_synced_leads`

**Inputs** days = no value.

**Declared result** int.

**Record and data access** read “CRM Lead” via count.

**Explicit results** Platform.db.count(“CRM Lead”, filters).

**Local steps**

- Set filters from mapping(“facebook\_lead\_id” → list(“is”, “set”)).
- If days.
  - Set filters at “creation” from list(“&gt;”, add\_days(nowdate(), negative days)).
- Return Platform.db.count(“CRM Lead”, filters).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0058.json#L3202) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1500) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1474)

<a id="op-01d4cd1a92aab0"></a>
### Product sync state

`operation_relationships_telemetry_business_behavior_product_sync_state`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** resolve a document from “Enterprise CRM Settings” via get\_cached\_doc · read “CRM Product” via count · read “CRM Product Sync Issue” via count.

**Explicit results** state.

**Local steps**

- Set settings from Platform.get\_cached\_doc(“Enterprise CRM Settings”).
- Set state from mapping(“Enterprise\_sync\_enabled” → bool(settings.enabled), “products\_sync\_enabled” → bool(settings.sync\_products), “products\_total” → Platform.db.count(“CRM Product”), “product\_sync\_issues\_open” → Platfor ….
- If Platform.db.has\_column(“CRM Product”, “Enterprise\_item\_code”).
  - Set state at “products\_synced\_total” from Platform.db.count(“CRM Product”, mapping(“Enterprise\_item\_code” → list(“is”, “set”))).
- Return state.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Enterprise CRM Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0058.json#L3402) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1502) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1476)

<a id="op-78747e444ba0e7"></a>
### Sales hierarchy state

`operation_relationships_telemetry_business_behavior_sales_hierarchy_state`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “FCRM Settings” via get\_single\_value · read “CRM Sales Hierarchy” via count.

**Explicit results** mapping(“sales\_hierarchy\_enabled” → bool(Platform.db.get\_single\_value(“FCRM Settings”, “enable\_sales\_hierarchy”)), “sales\_hierarchy\_nodes” → Platform.db.count(“CRM Sales Hierarchy”)).

**Local steps**

- Return mapping(“sales\_hierarchy\_enabled” → bool(Platform.db.get\_single\_value(“FCRM Settings”, “enable\_sales\_hierarchy”)), “sales\_hierarchy\_nodes” → Platform.db.count(“CRM Sales Hierarchy”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “enable\_sales\_hierarchy”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0058.json#L3735) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1503) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1477)

## Service · Uninstall

<a id="op-80eaa8956424ca"></a>
### Before uninstall

`operation_relationships_uninstall_business_behavior_before_uninstall`

**Inputs** no declared parameters.

**Local steps**

- Evaluate delete\_email\_template\_custom\_fields().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0066.json#L6685) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1733) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L163)

<a id="op-ffbf15966818fe"></a>
### Delete email template custom fields

`operation_relationships_uninstall_business_behavior_delete_email_template_custom_fields`

**Inputs** no declared parameters.

**State and service calls** request delete on “Custom Field”.

**Local steps**

- If Platform.get\_meta(“Email Template”).has\_field(“enabled”).
  - Evaluate click.secho(“\* Uninstalling Custom Fields from Email Template”).
  - Set fieldnames from tuple(“enabled”, “reference\_doctype”).
  - For each fieldname in fieldnames.
    - Evaluate Platform.db.delete(“Custom Field”, mapping(“name” → (“Email Template-” + fieldname))).
  - Evaluate Platform.clear\_cache(doctype = “Email Template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0066.json#L6724) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1734) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L164)

## Service · Users

<a id="op-ff734e9d7c1e3c"></a>
### Create demo users

`operation_relationships_demo_users_business_behavior_create_demo_users`

**Inputs** no declared parameters.

**Record and data access** read “User” via exists · resolve a document from mapping(“doctype” → “User”, “email” → user\_data at “email”, “first\_name” → user\_data at “first\_name”, “last\_name” → user\_data at “last\_name”, …) via get\_doc · read “CRM Availability Status” via exists · read “Contact” via get\_all.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “User”, “email” → user\_data at “email”, “first\_name” → user\_data at “first\_name”, “last\_name” → user\_data at “last\_name”, …)) · request set\_value on “Contact”.

**Explicit results** DEMO\_USER\_EMAILS.

**Local steps**

- For each user\_data in DEMO\_USERS.
  - If not Platform.db.exists(“User”, user\_data at “email”).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “User”, “email” → user\_data at “email”, “first\_name” → user\_data at “first\_name”, “last\_name” → user\_data at “last\_name”, …)).insert(ignore\_permissions = true).
      - Draw r from user\_data at “roles”.
      - Value choice on Platform.db.exists(“CRM Availability Status”, user\_data at “availability”) — true gives user\_data at “availability”, false gives no value.
- Set \_ts from (datetime.now() − timedelta(days = 70)).
- Set \_avatar\_by\_email from mapping of u at “email” → u at “avatar” for u drawn from DEMO\_USERS.
  - Draw u from DEMO\_USERS.
- Set contact\_names from Platform.get\_all(“Contact”, filters = mapping(“user” → list(“in”, DEMO\_USER\_EMAILS)), fields = list(“name”, “user”)).
- For each row in contact\_names.
  - Evaluate Platform.db.set\_value(“Contact”, row.name, mapping(“image” → \_avatar\_by\_email.get(row.user, empty text), “creation” → \_ts, “modified” → \_ts), update\_modified = false).
- Return DEMO\_USER\_EMAILS.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L231) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L409) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L390)

<a id="op-5291afa27b090d"></a>
### Delete demo users

`operation_relationships_demo_users_business_behavior_delete_demo_users`

**Inputs** demo\_user\_emails.

**Record and data access** read “Contact” via get\_all · read “User” via exists.

**State and service calls** request delete\_doc for “User”.

**Local steps**

- Set Notification from DocType(“CRM Notification”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((nested operand in the contract.from\_user.isin(demo\_user\_emails) bitwise or nested operand in the contract.to\_user.isin(demo\_us ….run().
- Set contact\_names from Platform.get\_all(“Contact”, filters = mapping(“user” → list(“in”, demo\_user\_emails)), pluck = “name”).
- For each email in demo\_user\_emails.
  - If Platform.db.exists(“User”, email).
    - Evaluate Platform.delete\_doc(“User”, email, ignore\_permissions = true, force = true).
- If contact\_names.
  - For each child\_doctype in tuple(“Contact Email”, “Contact Phone”, “Dynamic Link”).
    - Set Child from DocType(child\_doctype).
    - Evaluate nested operand in the contract(nested operand in the contract).delete().where(Child.parent.isin(contact\_names)).run().
  - Set Contact from DocType(“Contact”).
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where(Contact.name.isin(contact\_names)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L891) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L410) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L391)

## Service · Utils

<a id="op-92ca4e13faae24"></a>
### Resolve owners

`operation_relationships_demo_utils_business_behavior_resolve_owners`

**Inputs** demo\_users.

**Explicit results** tuple(s, expanded owners).

**Local steps**

- Set s from Platform.session.user.
- If s belongs to tuple(“Administrator”, “Guest”).
  - Set s from demo\_users at 0 when demo\_users, otherwise s.
    - Value choice on demo\_users — true gives demo\_users at 0, false gives s.
- Set owners from list of demo\_users at i when i &lt; len(demo\_users), otherwise s for i drawn from range(3).
  - Draw i from range(3).
  - Value choice on i &lt; len(demo\_users) — true gives demo\_users at i, false gives s.
- Return tuple(s, expanded owners).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L1539) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L417) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L398)

<a id="op-951d0a80da2edd"></a>
### Build full names

`operation_relationships_demo_utils_business_behavior_build_full_names`

**Inputs** session\_user.

**Explicit results** names.

**Local steps**

- Bind dependencies DEMO\_USERS.
- Set names from mapping of u at “email” → formatted text {u at “first\_name”} {u at “last\_name”} for u drawn from DEMO\_USERS.
  - Draw u from DEMO\_USERS.
- Set names at session\_user from Platform.utils.get\_fullname(session\_user).
- Return names.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L1757) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L412) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L393)

<a id="op-3b8ad2b97e952f"></a>
### Backdate

`operation_relationships_demo_utils_business_behavior_backdate`

**Inputs** doctype, name, owner, ts, set\_creation (named only, default true).

**State and service calls** request set\_value on doctype.

**Local steps**

- Set fields from mapping(“owner” → owner, “modified\_by” → owner, “modified” → ts).
- If set\_creation.
  - Set fields at “creation” from ts.
- Evaluate Platform.db.set\_value(doctype, name, fields, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L1945) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L411) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L392)

<a id="op-4b1adfcf5c422e"></a>
### Fix auto records

`operation_relationships_demo_utils_business_behavior_fix_auto_records`

**Inputs** doctype, docname, owner, ts.

**Local steps**

- Set Version from DocType(“Version”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Version.modified, ts).where(((nested operand in the contract.ref\_doctype equals doctype bitwise and nested ….run().
- Set Comment from DocType(“Comment”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Comment.modified, ts).where(((nested operand in the contract.reference\_doctype equals doctype bitwise and  ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L2150) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L413) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L394)

<a id="op-413e1bcd29fb20"></a>
### Insert comment

`operation_relationships_demo_utils_business_behavior_insert_comment`

**Inputs** reference\_doctype, reference\_name, owner, content, full\_names, ts.

**Record and data access** resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, …)).

**Explicit results** comment.name.

**Local steps**

- Set comment from Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, …)).insert(ignore\_permissions = true).
- Evaluate backdate(“Comment”, comment.name, owner, ts).
- Return comment.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L2715) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L414) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L395)

<a id="op-235ea8e17f7673"></a>
### Insert communication

`operation_relationships_demo_utils_business_behavior_insert_communication`

**Inputs** reference\_doctype, reference\_name, data, full\_names, ts.

**Record and data access** resolve a document from mapping(“doctype” → “Communication”, “communication\_type” → “Communication”, “communication\_medium” → “Email”, “status” → “Linked”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Communication”, “communication\_type” → “Communication”, “communication\_medium” → “Email”, “status” → “Linked”, …)).

**Explicit results** comm.name.

**Local steps**

- Set comm from Platform.get\_doc(mapping(“doctype” → “Communication”, “communication\_type” → “Communication”, “communication\_medium” → “Email”, “status” → “Linked”, …)).insert(ignore\_permissions = true).
- Evaluate backdate(“Communication”, comm.name, data at “owner”, ts).
- Return comm.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L3032) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L415) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L396)

<a id="op-7c9db9930f3764"></a>
### Insert version

`operation_relationships_demo_utils_business_behavior_insert_version`

**Inputs** ref\_doctype, docname, owner, changed, ts.

**Record and data access** resolve a document from mapping(“doctype” → “Version”, “ref\_doctype” → ref\_doctype, “docname” → docname, “data” → json.dumps(mapping(“changed” → changed))) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Version”, “ref\_doctype” → ref\_doctype, “docname” → docname, “data” → json.dumps(mapping(“changed” → changed)))).

**Explicit results** version.name.

**Local steps**

- Set version from Platform.get\_doc(mapping(“doctype” → “Version”, “ref\_doctype” → ref\_doctype, “docname” → docname, “data” → json.dumps(mapping(“changed” → changed)))).insert(ignore\_permissions = true).
- Evaluate backdate(“Version”, version.name, owner, ts).
- Return version.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L3534) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L416) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L397)

<a id="op-a24c72e424c871"></a>
### Parse phone number

`operation_relationships_utils_initialize_business_behavior_parse_phone_number`

**Inputs** phone\_number, default\_country = “IN”.

**Explicit results** mapping(“success” → true, expand result) · mapping(“success” → false, “error” → str(e)).

**Local steps**

- Attempt the following.
  - Set number from phonenumbers.parse(phone\_number, default\_country).
  - Set result from mapping(“is\_valid” → phonenumbers.is\_valid\_number(number), “country\_code” → number.country\_code, “national\_number” → str(number.national\_number), “formats” → mapping(“international” → phonenumbers.format\_n ….
  - Return mapping(“success” → true, expand result).
- On failure (NumberParseException) bound to e.
  - Return mapping(“success” → false, “error” → str(e)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1744) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L174)
