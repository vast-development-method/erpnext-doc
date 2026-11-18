# Lead and deal records · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm view settings

<a id="op-d88df8abc3eec0"></a>
### Sync default rows

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_sync_default_rows`

**Inputs** doctype, type = “list”.

**Explicit results** rows.

**Local steps**

- Set list from get\_controller(doctype).
- Set rows from list().
- If hasattr(list, “default\_list\_data”).
  - Set rows from list.default\_list\_data().get(“rows”).
- Return rows.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L4195) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1175) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1151)

<a id="op-3206fb9de17475"></a>
### Sync default columns

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_sync_default_columns`

**Inputs** view.

**Record and data access** read field\_meta.options via get\_all.

**Explicit results** columns.

**Local steps**

- Set doctype from (view.dt or view.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.dt → view.doctype.
- Set list from get\_controller(doctype).
- Set columns from list().
- If (view.type equals “kanban” and view.column\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in view.type equals “kanban” → view.column\_field.
  - Set field\_meta from Platform.get\_meta(doctype).get\_field(view.column\_field).
  - If field\_meta.fieldtype equals “Link”.
    - Set columns from Platform.get\_all(field\_meta.options, fields = list(“name”), order\_by = “modified asc”).
  - Otherwise.
    - If field\_meta.fieldtype equals “Select”.
      - Set columns from list of mapping(“name” → option) for option drawn from field\_meta.options.split(whitespace '\\n').
        - Draw option from field\_meta.options.split(whitespace '\\n').
- Otherwise.
  - If hasattr(list, “default\_list\_data”).
    - Set columns from list.default\_list\_data().get(“columns”).
- Return columns.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L4356) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1174) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1150)

<a id="op-fe355f1d5d8155"></a>
### Set as default

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_set_as_default`

**Inputs** name = no value, type = no value, doctype = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM View Settings” via get\_value.

**State and service calls** request set\_value on “CRM View Settings”.

**Local steps**

- If name.
  - Evaluate Platform.db.set\_value(“CRM View Settings”, name, “is\_default”, 1).
  - Set doctype from (doctype or Platform.db.get\_value(“CRM View Settings”, name, “dt”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → Platform.db.get\_value(“CRM View Settings”, name, “dt”).
- Otherwise.
  - Set doc from create\_or\_update\_standard\_view(mapping(“type” → type, “doctype” → doctype, “is\_default” → 1)).
  - Set name from doc.name.
- Evaluate Platform.db.set\_value(“CRM View Settings”, mapping(“name” → tuple(“!=”, name), “user” → Platform.session.user, “is\_default” → 1, “dt” → doctype), “is\_default”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L22) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1173) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1149)

<a id="op-4747fed3a2db49"></a>
### Create or update standard view

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_create_or_update_standard_view`

**Inputs** view.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM View Settings” via exists · resolve a document from “CRM View Settings” via get\_doc.

**State and service calls** call save on doc · request new\_doc for “CRM View Settings” · call insert on doc.

**Explicit results** doc.

**Local steps**

- Set view from Platform.\_dict(view).
- Set filters from (parse\_json(view.filters) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json(view.filters) → mapping().
- Set columns from parse\_json((view.columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.columns → “&#91;&#93;”.
- Set rows from parse\_json((view.rows or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.rows → “&#91;&#93;”.
- Set kanban\_columns from parse\_json((view.kanban\_columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.kanban\_columns → “&#91;&#93;”.
- Set kanban\_fields from parse\_json((view.kanban\_fields or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.kanban\_fields → “&#91;&#93;”.
- Set view.column\_field from (view.column\_field or “status”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.column\_field → “status”.
- Set default\_rows from sync\_default\_rows(view.doctype, view.type).
- Set rows from (rows + default\_rows) when default\_rows, otherwise rows.
  - Value choice on default\_rows — true gives (rows + default\_rows), false gives rows.
- Set rows from remove\_duplicates(rows).
- If (not kanban\_columns and view.type equals “kanban”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kanban\_columns → view.type equals “kanban”.
  - Set kanban\_columns from sync\_default\_columns(view).
- Otherwise.
  - If not columns.
    - Set columns from sync\_default\_columns(view).
- Set doc from Platform.db.exists(“CRM View Settings”, mapping(“dt” → view.doctype, “type” → (view.type or “list”), “is\_standard” → true, “user” → Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.type → “list”.
- If doc.
  - Set doc from Platform.get\_doc(“CRM View Settings”, doc).
  - Set doc.label from view.label.
  - Set doc.type from (view.type or “list”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.type → “list”.
  - Set doc.route\_name from (view.route\_name or get\_route\_name(view.doctype)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.route\_name → get\_route\_name(view.doctype).
  - Set doc.load\_default\_columns from (view.load\_default\_columns or false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.load\_default\_columns → false.
  - Set doc.filters from json.dumps(filters).
  - Set doc.order\_by from (view.order\_by or “modified desc”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.order\_by → “modified desc”.
  - Set doc.group\_by\_field from (view.group\_by\_field or “owner”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.group\_by\_field → “owner”.
  - Set doc.column\_field from view.column\_field.
  - Set doc.title\_field from view.title\_field.
  - Set doc.kanban\_columns from json.dumps(kanban\_columns).
  - Set doc.kanban\_fields from json.dumps(kanban\_fields).
  - Set doc.columns from json.dumps(columns).
  - Set doc.rows from json.dumps(rows).
  - If view.is\_default.
    - Set doc.is\_default from 1.
  - Evaluate doc.save().
- Otherwise.
  - Set doc from Platform.new\_doc(“CRM View Settings”).
  - Set label from “List”.
  - If view.type equals “group\_by”.
    - Set label from “Group By”.
  - Otherwise.
    - If view.type equals “kanban”.
      - Set label from “Kanban”.
  - Set doc.name from (view.label or label).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.label → label.
  - Set doc.label from (view.label or label).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.label → label.
  - Set doc.type from (view.type or “list”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.type → “list”.
  - Set doc.dt from view.doctype.
  - Set doc.user from Platform.session.user.
  - Set doc.route\_name from (view.route\_name or get\_route\_name(view.doctype)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.route\_name → get\_route\_name(view.doctype).
  - Set doc.load\_default\_columns from (view.load\_default\_columns or false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.load\_default\_columns → false.
  - Set doc.filters from json.dumps(filters).
  - Set doc.order\_by from (view.order\_by or “modified desc”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.order\_by → “modified desc”.
  - Set doc.group\_by\_field from (view.group\_by\_field or “owner”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.group\_by\_field → “owner”.
  - Set doc.column\_field from view.column\_field.
  - Set doc.title\_field from view.title\_field.
  - Set doc.kanban\_columns from json.dumps(kanban\_columns).
  - Set doc.kanban\_fields from json.dumps(kanban\_fields).
  - Set doc.columns from json.dumps(columns).
  - Set doc.rows from json.dumps(rows).
  - Set doc.is\_standard from true.
  - Set doc.is\_default from (view.is\_default or false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.is\_default → false.
  - Evaluate doc.insert().
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L21) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1166) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1142)

<a id="op-368ddc5e57e1f8"></a>
### Fetch and update kanban columns

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_fetch_and_update_kanban_columns`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM View Settings” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value · doc.kanban\_columns.

**Local steps**

- Set doc from Platform.get\_doc(“CRM View Settings”, name).
- If doc.type differs from “kanban”.
  - Return no value.
- Set new\_columns from sync\_default\_columns(doc).
- Set existing\_columns from parse\_json((doc.kanban\_columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.kanban\_columns → “&#91;&#93;”.
- Set existing\_column\_names from list of column.get(“name”) for column drawn from existing\_columns.
  - Draw column from existing\_columns.
- For each column in new\_columns.
  - If column.get(“name”) does not belong to existing\_column\_names.
    - Evaluate existing\_columns.append(mapping(“name” → column.get(“name”), “delete” → true)).
- Set doc.kanban\_columns from json.dumps(existing\_columns).
- Evaluate doc.save(ignore\_permissions = true).
- Return doc.kanban\_columns.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L7067) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1168) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1144)

<a id="op-ec25b5e08ddb2e"></a>
### Clear old versions

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_clear_old_versions`

**Inputs** days = 14.

**State and service calls** request delete on “Version”.

**Local steps**

- Bind dependencies add\_days, now\_datetime.
- Evaluate Platform.db.delete(“Version”, mapping(“ref\_doctype” → “CRM View Settings”, “creation” → tuple(“&lt;”, add\_days(now\_datetime(), negative days)))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L7527) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1164) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1140)

<a id="op-f37bb71d032d25"></a>
### Get route name

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_get_route_name`

**Inputs** doctype.

**Explicit results** doctype.

**Local steps**

- If doctype.startswith(“CRM ”).
  - Set doctype from doctype at slice 4 to no value.
- If doctype at negative 1 differs from “s”.
  - Update doctype using + “s”.
- Return doctype.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L7686) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1169) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1145)

## Record · Enterprise crm settings

<a id="op-3421ff8fbbbe52"></a>
### Is Enterprise installed

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_is_enterprise_installed`

**Inputs** no declared parameters.

**Explicit results** “Enterprise” belongs to Platform.get\_installed\_apps().

**Local steps**

- Return “Enterprise” belongs to Platform.get\_installed\_apps().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L7824) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1213) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1189)

<a id="op-1bf498e7f2fb42"></a>
### Log and throw

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_log_and_throw`

**Inputs** message, title = no value.

**Explicit failure paths** validation helper — translated message.

**Local steps**

- Evaluate Platform.log\_error(Platform.get\_traceback(), (title or message)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → message.
- Call the validation error handler Platform.throw(translated message).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L7877) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1214) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1190)

<a id="op-dbd9d360960ae9"></a>
### Get enabled settings

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_enabled_settings`

**Inputs** no declared parameters.

**Record and data access** read “Enterprise CRM Settings” via get\_single.

**Explicit results** settings.

**Explicit failure paths** validation helper — translated “Enterprise is not integrated with the CRM”.

**Local steps**

- Set settings from Platform.get\_single(“Enterprise CRM Settings”).
- If not settings.enabled.
  - Call the validation error handler Platform.throw(translated “Enterprise is not integrated with the CRM”).
- Return settings.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1202) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1178)

<a id="op-9303045f6a96f8"></a>
### Enterprise CRMSettings.validate

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_validate`

**Inputs** self.

**Local steps**

- Set old from self.get\_doc\_before\_save().
- Set was\_active from bool((old and old.enabled and not old.is\_Enterprise\_in\_different\_site)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old → old.enabled → not old.is\_Enterprise\_in\_different\_site.
- If self.enabled.
  - Evaluate self.validate\_if\_Enterprise\_installed().
  - Evaluate self.add\_quotation\_to\_option().
  - Evaluate self.create\_custom\_fields().
  - Evaluate self.create\_crm\_form\_script().
  - Evaluate self.grant\_item\_access\_to\_sales\_roles().
  - If (not was\_active and not self.is\_Enterprise\_in\_different\_site and self.sync\_products).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not was\_active → not self.is\_Enterprise\_in\_different\_site → self.sync\_products.
    - Bind dependencies enqueue\_reconciliation.
    - Evaluate enqueue\_reconciliation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate if Enterprise installed](operations-010.md#op-aa1b071e560b3e), [add quotation to option](operations-010.md#op-0d380f55b04fc4), [create custom fields](operations-010.md#op-dd6ad09c5e4177), [create crm form script](operations-010.md#op-ab51d9ce93d8ad), [grant item access to sales roles](operations-010.md#op-740412229016ea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L24) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1196) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1172)

<a id="op-aa1b071e560b3e"></a>
### Enterprise CRMSettings.validate if Enterprise installed

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_validate_if_enterprise_installed`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enterprise is not installed in the current site”.

**Local steps**

- If not self.is\_Enterprise\_in\_different\_site.
  - If not \_is\_Enterprise\_installed().
    - Call the validation error handler Platform.throw(translated “Enterprise is not installed in the current site”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L409) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1197) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1173)

<a id="op-0d380f55b04fc4"></a>
### Enterprise CRMSettings.add quotation to option

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_add_quotation_to_option`

**Inputs** self.

**Record and data access** read “Property Setter” via exists.

**Local steps**

- If not self.is\_Enterprise\_in\_different\_site.
  - If not Platform.db.exists(“Property Setter”, mapping(“name” → “Quotation-quotation\_to-link\_filters”)).
    - Evaluate make\_property\_setter(doctype = “Quotation”, fieldname = “quotation\_to”, property = “link\_filters”, value = “&#91;&#91;"DocType","name","in", &#91;"Customer", "Lead", "Prospect", "CRM Deal"&#93;&#93;&#93;”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L522) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1186) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1162)

<a id="op-dd6ad09c5e4177"></a>
### Enterprise CRMSettings.create custom fields

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_create_custom_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enterprise is not installed in the current site”.

**Local steps**

- If not self.is\_Enterprise\_in\_different\_site.
  - If not \_is\_Enterprise\_installed().
    - Call the validation error handler Platform.throw(translated “Enterprise is not installed in the current site”).
- Otherwise.
  - Evaluate self.create\_custom\_fields\_in\_remote\_site().
- Evaluate self.create\_custom\_fields\_in\_Platform\_crm().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create custom fields in remote site](operations-010.md#op-2797eb7e840686), [create custom fields in Platform crm](operations-010.md#op-3530cb73de62fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L726) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1187) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1163)

<a id="op-3530cb73de62fb"></a>
### Enterprise CRMSettings.create custom fields in Platform crm

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_create_custom_fields_in_foundation_customer_relationship`

**Inputs** self.

**Record and data access** read “DocType” via exists.

**Local steps**

- Set custom\_fields from mapping(“CRM Deal” → list(mapping(“fieldname” → “Enterprise\_customer”, “fieldtype” → “Data”, “label” → “Customer in Enterprise”, “insert\_after” → “lead\_name”)), “CRM Product” → list(mapping(“fieldname” → “ ….
- If Platform.db.exists(“DocType”, “Item”).
  - Set custom\_fields at “Item” from list(mapping(“fieldname” → “crm\_product\_code”, “fieldtype” → “Data”, “label” → “CRM Product”, “read\_only” → 1, …)).
- If Platform.db.exists(“DocType”, “Quotation”).
  - Set custom\_fields at “Quotation” from list(mapping(“fieldname” → “crm\_deal”, “fieldtype” → “Data”, “label” → “Platform CRM Deal”, “read\_only” → 1, …)).
- If Platform.db.exists(“DocType”, “Customer”).
  - Set custom\_fields at “Customer” from list(mapping(“fieldname” → “crm\_deal”, “fieldtype” → “Data”, “label” → “Platform CRM Deal”, “read\_only” → 1, …)).
- Evaluate \_create\_custom\_fields(custom\_fields, ignore\_validate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L880) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1188) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1164)

<a id="op-2797eb7e840686"></a>
### Enterprise CRMSettings.create custom fields in remote site

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_create_custom_fields_in_remote_site`

**Inputs** self.

**State and service calls** msgprint with translated “Could not create the Platform CRM custom fields on {0} automatically. If it is running the latest Enterprise …”.format(self.Enterprise\_site\_url).

**Local steps**

- Set client from get\_Enterprise\_site\_client(self).
- Attempt the following.
  - Evaluate client.post\_api(“Enterprise.crm.Platform\_crm\_api.create\_custom\_fields\_for\_Platform\_crm”).
- On failure (Exception).
  - Evaluate Platform.log\_error(Platform.get\_traceback(), formatted text Could not create custom fields on remote Enterprise site: {self.Enterprise\_site\_url}).
  - Evaluate Platform.msgprint(translated “Could not create the Platform CRM custom fields on {0} automatically. If it is running the latest Enterprise …”.format(self.Enterprise\_site\_url), title = translated “Enterpris ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L1655) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1189) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1165)

<a id="op-740412229016ea"></a>
### Enterprise CRMSettings.grant item access to sales roles

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_grant_item_access_to_sales_roles`

**Inputs** self.

**Record and data access** read “DocType” via exists · read “Custom DocPerm” via exists.

**Explicit results** no value.

**Local steps**

- If self.is\_Enterprise\_in\_different\_site.
  - Return no value.
- If not Platform.db.exists(“DocType”, “Item”).
  - Return no value.
- Bind dependencies add\_permission, update\_permission\_property.
- For each role in tuple(“Sales User”, “Sales Manager”).
  - If Platform.db.exists(“Custom DocPerm”, mapping(“parent” → “Item”, “role” → role, “permlevel” → 0)).
    - Continue with the next iteration or loop test.
  - Evaluate add\_permission(“Item”, role, 0, “write”).
  - For each prop in tuple(“create”, “delete”, “share”, “print”, …).
    - Evaluate update\_permission\_property(“Item”, role, 0, prop, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L1957) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1192) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1168)

<a id="op-ab51d9ce93d8ad"></a>
### Enterprise CRMSettings.create crm form script

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_create_customer_relationship_form_script`

**Inputs** self.

**Record and data access** read “CRM Form Script” via exists · resolve a document from mapping(“doctype” → “CRM Form Script”, “name” → “Create Quotation from CRM Deal”, “dt” → “CRM Deal”, “view” → “Form”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Form Script”, “name” → “Create Quotation from CRM Deal”, “dt” → “CRM Deal”, “view” → “Form”, …)).

**Local steps**

- If not Platform.db.exists(“CRM Form Script”, “Create Quotation from CRM Deal”).
  - Set script from get\_crm\_form\_script().
  - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Form Script”, “name” → “Create Quotation from CRM Deal”, “dt” → “CRM Deal”, “view” → “Form”, …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L2348) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1190) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1166)

<a id="op-df88c17b48c754"></a>
### Enterprise CRMSettings.reset Enterprise form script

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_reset_enterprise_form_script`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Form Script” via exists.

**State and service calls** request set\_value on “CRM Form Script”.

**Explicit results** true · false.

**Local steps**

- Attempt the following.
  - If Platform.db.exists(“CRM Form Script”, “Create Quotation from CRM Deal”).
    - Set script from get\_crm\_form\_script().
    - Evaluate Platform.db.set\_value(“CRM Form Script”, “Create Quotation from CRM Deal”, “script”, script).
    - Return true.
  - Return false.
- On failure (Exception).
  - Evaluate Platform.log\_error(Platform.get\_traceback(), “Error while resetting form script”).
  - Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L2602) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1194) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1170)

<a id="op-36871fa16dbbaa"></a>
### Enterprise CRMSettings.get external companies

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_get_external_companies`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list() · client.get\_list(“Company”, fields = list(“company\_name”)).

**Local steps**

- If (not self.Enterprise\_site\_url or not self.api\_key or not self.api\_secret).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.Enterprise\_site\_url → not self.api\_key → not self.api\_secret.
  - Return list().
- Set client from get\_Enterprise\_site\_client(self).
- Return client.get\_list(“Company”, fields = list(“company\_name”)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L2841) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1191) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1167)

<a id="op-2c38c60526be68"></a>
### Enterprise CRMSettings.is Enterprise installed

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_is_enterprise_installed`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_is\_Enterprise\_installed().

**Local steps**

- Return \_is\_Enterprise\_installed().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L3027) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1193) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1169)

<a id="op-d4b5c843694fdd"></a>
### Enterprise CRMSettings.run product sync

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_enterprise_resource_planning_next_customer_relationship_settings_run_product_sync`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** true.

**Explicit failure paths** validation helper — translated “Enterprise integration must be enabled on the same site”.

**Local steps**

- If (not self.enabled or self.is\_Enterprise\_in\_different\_site).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.enabled → self.is\_Enterprise\_in\_different\_site.
  - Call the validation error handler Platform.throw(translated “Enterprise integration must be enabled on the same site”).
- Bind dependencies enqueue\_reconciliation.
- Evaluate enqueue\_reconciliation().
- Return true.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L3092) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1195) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1171)

<a id="op-649d61d3cbde7b"></a>
### Get open sync issues

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_open_sync_issues`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Enterprise CRM Settings” via get\_single.

**Explicit results** list() · list of mapping(“name” → issue.name, “product” → issue.product, “kind” → issue.kind, “detail” → issue.detail, …) for issue drawn from settings.sync\_issues where not issue.dismissed.

**Local steps**

- If not Platform.has\_permission(“CRM Product”, “read”).
  - Return list().
- Set settings from Platform.get\_single(“Enterprise CRM Settings”).
- Return list of mapping(“name” → issue.name, “product” → issue.product, “kind” → issue.kind, “detail” → issue.detail, …) for issue drawn from settings.sync\_issues where not issue.dismissed.
  - Draw issue from settings.sync\_issues, keep a combination only if (not issue.dismissed).

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Product”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L3246) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1205) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1181)

<a id="op-7a0a6e21670d14"></a>
### Dismiss sync issue

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_dismiss_sync_issue`

**Inputs** issue\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Enterprise CRM Settings” via get\_single.

**State and service calls** call save on settings.

**Explicit results** true · false.

**Local steps**

- Set settings from Platform.get\_single(“Enterprise CRM Settings”).
- For each issue in settings.sync\_issues.
  - If issue.name equals issue\_name.
    - Set issue.dismissed from 1.
    - Evaluate settings.save().
    - Return true.
- Return false.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L3520) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1185) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1161)
