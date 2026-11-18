# Supporting services · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Install

<a id="op-469482b5150eb5"></a>
### Add standard dropdown items

`operation_relationships_install_business_behavior_add_standard_dropdown_items`

**Inputs** no declared parameters.

**Record and data access** read “FCRM Settings” via get\_single.

**State and service calls** call save on crm\_settings.

**Explicit results** no value.

**Local steps**

- Set crm\_settings from Platform.get\_single(“FCRM Settings”).
- If crm\_settings.dropdown\_items.
  - Return no value.
- Set crm\_settings.dropdown\_items from list().
- For each item in Platform.get\_hooks(“standard\_dropdown\_items”).
  - Evaluate crm\_settings.append(“dropdown\_items”, item).
- Evaluate crm\_settings.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“standard\_dropdown\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L5563) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1254) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1230)

<a id="op-d09b1e5a2452b0"></a>
### Add default availability statuses

`operation_relationships_binding_crm_install_add_default_availability_statuses`

**Inputs** no declared parameters.

**Record and data access** read “CRM Availability Status” via exists · resolve a document from mapping(“doctype” → “CRM Availability Status”, expand status) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Availability Status”, expand status)).

**Local steps**

- Set statuses from list(mapping(“availability\_status” → “Active”, “category” → “Active”, “color” → “green”, “position” → 1), mapping(“availability\_status” → “Away”, “category” → “Away”, “color” → “amber”, “position” → 2), ma ….
- For each status in statuses.
  - If not Platform.db.exists(“CRM Availability Status”, status at “availability\_status”).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Availability Status”, expand status)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L211) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L367) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L348)

<a id="op-4db91ce5986989"></a>
### Add availability user fields

`operation_relationships_binding_crm_install_add_availability_user_fields`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set meta from Platform.get\_meta(“User”).
- Set fields from list(mapping(“fieldname” → “crm\_availability”, “fieldtype” → “Link”, “options” → “CRM Availability Status”, “label” → “CRM Availability”, …), mapping(“fieldname” → “crm\_availability\_changed\_on”, “fieldtype ….
- Set fields from list of field for field drawn from fields where not meta.has\_field(field at “fieldname”).
  - Draw field from fields, keep a combination only if (not meta.has\_field(field at “fieldname”)).
- If not fields.
  - Return no value.
- Evaluate click.secho(“\* Installing Custom Fields in User”).
- Evaluate create\_custom\_fields(mapping(“User” → fields)).
- Evaluate Platform.clear\_cache(doctype = “User”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L209) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L365) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L346)

<a id="op-a56641bfe626a8"></a>
### Add default scripts

`operation_relationships_install_business_behavior_add_default_scripts`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies create\_forecasting\_script.
- For each doctype in list(“CRM Lead”, “CRM Deal”).
  - Evaluate create\_product\_details\_script(doctype).
- Evaluate create\_forecasting\_script().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L5741) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1250) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1226)

<a id="op-98527b29f492d0"></a>
### Add assignment rule property setters

`operation_relationships_install_business_behavior_add_assignment_rule_property_setters`

**Inputs** no declared parameters.

**Record and data access** read “Property Setter” via exists · resolve a document from mapping(expand default\_fields, “name” → “Assignment Rule-assign\_condition-depends\_on”, “field\_name” → “assign\_condition”, “property” → “depends\_on”, …) via get\_doc · resolve a document from mapping(expand default\_fields, “name” → “Assignment Rule-unassign\_condition-depends\_on”, “field\_name” → “unassign\_condition”, “property” → “depends\_on”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(expand default\_fields, “name” → “Assignment Rule-assign\_condition-depends\_on”, “field\_name” → “assign\_condition”, “property” → “depends\_on”, …)) · request set\_value on “Property Setter” · call insert on Platform.get\_doc(mapping(expand default\_fields, “name” → “Assignment Rule-unassign\_condition-depends\_on”, “field\_name” → “unassign\_condition”, “property” → “depends\_on”, …)).

**Local steps**

- Set default\_fields from mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → “DocField”, “doc\_type” → “Assignment Rule”, “property\_type” → “Data”, …).
- If not Platform.db.exists(“Property Setter”, mapping(“name” → “Assignment Rule-assign\_condition-depends\_on”)).
  - Evaluate Platform.get\_doc(mapping(expand default\_fields, “name” → “Assignment Rule-assign\_condition-depends\_on”, “field\_name” → “assign\_condition”, “property” → “depends\_on”, …)).insert().
- Otherwise.
  - Evaluate Platform.db.set\_value(“Property Setter”, mapping(“name” → “Assignment Rule-assign\_condition-depends\_on”), “value”, “eval: !doc.assign\_condition\_json”).
- If not Platform.db.exists(“Property Setter”, mapping(“name” → “Assignment Rule-unassign\_condition-depends\_on”)).
  - Evaluate Platform.get\_doc(mapping(expand default\_fields, “name” → “Assignment Rule-unassign\_condition-depends\_on”, “field\_name” → “unassign\_condition”, “property” → “depends\_on”, …)).insert().
- Otherwise.
  - Evaluate Platform.db.set\_value(“Property Setter”, mapping(“name” → “Assignment Rule-unassign\_condition-depends\_on”), “value”, “eval: !doc.unassign\_condition\_json”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L5844) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1241) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1217)

<a id="op-4e56e2cce17239"></a>
### Create assignment rule custom fields

`operation_relationships_install_business_behavior_create_assignment_rule_custom_fields`

**Inputs** no declared parameters.

**Local steps**

- If not Platform.get\_meta(“Assignment Rule”).has\_field(“assign\_condition\_json”).
  - Evaluate click.secho(“\* Installing Custom Fields in Assignment Rule”).
  - Evaluate create\_custom\_fields(mapping(“Assignment Rule” → list(mapping(“description” → “Autogenerated field by CRM App”, “fieldname” → “assign\_condition\_json”, “fieldtype” → “Code”, “label” → “Assign Condition JSON ….
  - Evaluate Platform.clear\_cache(doctype = “Assignment Rule”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L6464) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1258) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1234)

<a id="op-d44cdaa70ea895"></a>
### Add data import permissions

`operation_relationships_binding_crm_install_add_data_import_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 3 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L210) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L366) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L347)

## Service · Leads

<a id="op-3ac48220043651"></a>
### Create demo leads

`operation_relationships_demo_leads_business_behavior_create_demo_leads`

**Inputs** demo\_users.

**Record and data access** resolve a document from mapping(“doctype” → “CRM Lead”, expand data) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Lead”, expand data)).

**Explicit results** created.

**Local steps**

- Set tuple(session\_user, owner\_1, owner\_2, owner\_3) from resolve\_owners(demo\_users).
- Set leads\_data from list(mapping(“first\_name” → “Alice”, “last\_name” → “Johnson”, “email” → “alice.johnson@example.com”, “mobile\_no” → “+1 555 000 1234”, …), mapping(“first\_name” → “Bob”, “last\_name” → “Martinez”, “email” → “ ….
- Set now from datetime.now().
- Set created from list().
- For each tuple(data, days) in zip(leads\_data, \_LEAD\_DAYS, strict = false).
  - Set ts from (now − timedelta(days = days)).
  - Set owner from data at “lead\_owner”.
  - Set lead from Platform.get\_doc(mapping(“doctype” → “CRM Lead”, expand data)).insert(ignore\_permissions = true).
  - Evaluate backdate(“CRM Lead”, lead.name, owner, ts).
  - Evaluate fix\_auto\_records(“CRM Lead”, lead.name, owner, ts).
  - Evaluate created.append(lead.name).
- Return created.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L1040) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L402) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L383)

<a id="op-a1c2e8d66455cb"></a>
### Rebackdate demo leads

`operation_relationships_demo_leads_business_behavior_rebackdate_demo_leads`

**Inputs** lead\_names, demo\_users.

**Local steps**

- Set tuple(session\_user, owner\_1, owner\_2, owner\_3) from resolve\_owners(demo\_users).
- Set \_owners from list(session\_user, owner\_1, owner\_2, owner\_1, …).
- Set now from datetime.now().
- For each tuple(name, days, owner) in zip(lead\_names, \_LEAD\_LAST\_TOUCHED\_DAYS, \_owners, strict = false).
  - Evaluate backdate(“CRM Lead”, name, owner, (now − timedelta(days = days)), set\_creation = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L4042) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L404) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L385)

<a id="op-e0d3dda7b34ff9"></a>
### Delete demo leads

`operation_relationships_demo_leads_business_behavior_delete_demo_leads`

**Inputs** lead\_names.

**Record and data access** read “CRM Lead” via exists.

**State and service calls** request delete\_doc for “CRM Lead”.

**Local steps**

- For each name in lead\_names.
  - If Platform.db.exists(“CRM Lead”, name).
    - Evaluate Platform.delete\_doc(“CRM Lead”, name, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L4343) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L403) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L384)

## Service · Notes

<a id="op-5c158ad732acfb"></a>
### Create demo notes

`operation_relationships_demo_notes_business_behavior_create_demo_notes`

**Inputs** lead\_names, demo\_users.

**Record and data access** resolve a document from mapping(“doctype” → “FCRM Note”, “title” → data at “title”, “content” → data at “content”, “reference\_doctype” → data at “reference\_doctype”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “FCRM Note”, “title” → data at “title”, “content” → data at “content”, “reference\_doctype” → data at “reference\_doctype”, …)).

**Explicit results** created.

**Local steps**

- Set tuple(session\_user, owner\_1, owner\_2, \_) from resolve\_owners(demo\_users).
- Set now from datetime.now().
- Set notes\_data from list(mapping(“title” → “Initial Discovery Call”, “content” → text in the contract, “reference\_doctype” → “CRM Lead”, “reference\_docname” → lead\_names at 0, …), mapping(“title” → “Pain Points Identified”, “ ….
- Set created from list().
- For each data in notes\_data.
  - Set ts from (now − timedelta(days = data at “days\_ago”)).
  - Set owner from data at “owner”.
  - Set note from Platform.get\_doc(mapping(“doctype” → “FCRM Note”, “title” → data at “title”, “content” → data at “content”, “reference\_doctype” → data at “reference\_doctype”, …)).insert(ignore\_permissions = true).
  - Evaluate backdate(“FCRM Note”, note.name, owner, ts).
  - Evaluate created.append(note.name).
- Return created.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L4484) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L405) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L386)

<a id="op-1df32432df2339"></a>
### Delete demo notes

`operation_relationships_demo_notes_business_behavior_delete_demo_notes`

**Inputs** note\_names.

**Record and data access** read “FCRM Note” via exists.

**State and service calls** request delete\_doc for “FCRM Note”.

**Local steps**

- For each name in note\_names.
  - If Platform.db.exists(“FCRM Note”, name).
    - Evaluate Platform.delete\_doc(“FCRM Note”, name, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L5615) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L406) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L387)

## Service · Org hierarchy

<a id="op-ba46dfc2c3d966"></a>
### Hierarchy enabled

`operation_relationships_permissions_org_hierarchy_business_behavior_hierarchy_enabled`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L2918) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1455) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1430)

<a id="op-70b61ae593c332"></a>
### Permission query conditions

`operation_relationships_permissions_org_hierarchy_business_behavior_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L2996) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1457) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1432)

<a id="op-7011d6580e55e0"></a>
### Get lead permission query conditions

`operation_relationships_permissions_org_hierarchy_business_behavior_get_lead_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L3868) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1451) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1426)

<a id="op-204527eb3b1be2"></a>
### Get deal permission query conditions

`operation_relationships_permissions_org_hierarchy_business_behavior_get_deal_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L3996) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1450) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1425)

<a id="op-76ac7c1ff28909"></a>
### Has permission

`operation_relationships_permissions_org_hierarchy_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, doctype.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L4124) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1454) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1429)

<a id="op-dcb89b3c949bb6"></a>
### Has lead permission

`operation_relationships_permissions_org_hierarchy_business_behavior_has_lead_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L4666) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1453) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1428)

<a id="op-dbb5df161711ab"></a>
### Has deal permission

`operation_relationships_permissions_org_hierarchy_business_behavior_has_deal_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L4749) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1452) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1427)

<a id="op-bb66c013ea469c"></a>
### In hierarchy

`operation_relationships_permissions_org_hierarchy_business_behavior_in_hierarchy`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L4832) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1456) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1431)

<a id="op-8a5deab591f51d"></a>
### Team mem query

`operation_relationships_permissions_org_hierarchy_business_behavior_team_memory_query`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0057.json#L4935) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1458) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1433)

## Service · Search sqlite

<a id="op-de8c7594c1f0f8"></a>
### CRMSearch.get search filters

`operation_relationships_binding_crm_search_sqlite_crmsearch_get_search_filters`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping() when parents is identical to no value, otherwise mapping(“parent” → parents).

**Local steps**

- Set parents from self.get\_readable\_parents().
- Set self.is\_post\_filter\_required from parents is identical to no value.
- Return mapping() when parents is identical to no value, otherwise mapping(“parent” → parents).
  - Value choice on parents is identical to no value — true gives mapping(), false gives mapping(“parent” → parents).

**Methods declared on this owner** [get readable parents](operations-003.md#op-14ba7a53fd1251).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L222) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L378) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L359)

<a id="op-14ba7a53fd1251"></a>
### CRMSearch.get readable parents

`operation_relationships_binding_crm_search_sqlite_crmsearch_get_readable_parents`

**Inputs** self.

**Declared result** (list at str bitwise or no value).

**Record and data access** read “CRM Lead” via get\_list · read “CRM Deal” via get\_list.

**Explicit results** no value · (list of parent\_key(“CRM Lead”, name) for name drawn from leads + list of parent\_key(“CRM Deal”, name) for name drawn from deals).

**Local steps**

- Set leads from Platform.get\_list(“CRM Lead”, pluck = “name”, limit = (PREFILTER\_LIMIT + 1)).
- Set deals from Platform.get\_list(“CRM Deal”, pluck = “name”, limit = (PREFILTER\_LIMIT + 1)).
- If (len(leads) &gt; PREFILTER\_LIMIT or len(deals) &gt; PREFILTER\_LIMIT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(leads) &gt; PREFILTER\_LIMIT → len(deals) &gt; PREFILTER\_LIMIT.
  - Return no value.
- Return (list of parent\_key(“CRM Lead”, name) for name drawn from leads + list of parent\_key(“CRM Deal”, name) for name drawn from deals).
  - Draw name from leads.
  - Draw name from deals.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L221) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L377) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L358)

<a id="op-1eeb525a9ba36e"></a>
### CRMSearch.prepare document

`operation_relationships_binding_crm_search_sqlite_crmsearch_prepare_document`

**Inputs** self, doc.

**Explicit results** no value · document.

**Local steps**

- Set config from self.doc\_configs.get(doc.doctype).
- If (not config or not matches\_filters(doc, config at “filters”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not config → not matches\_filters(doc, config at “filters”).
  - Return no value.
- Set document from super().prepare\_document(doc).
- If not document.
  - Return no value.
- Set reference\_name from doc.reference\_docname when doc.doctype equals “FCRM Note”, otherwise doc.reference\_name.
  - Value choice on doc.doctype equals “FCRM Note” — true gives doc.reference\_docname, false gives doc.reference\_name.
- Set document at “parent” from parent\_key(doc.reference\_doctype, reference\_name).
- If doc.doctype equals “Communication”.
  - Set document at “content” from self.\_process\_content(strip\_quoted\_reply(doc.content)).
- Return document.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L224) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L380) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L361)
