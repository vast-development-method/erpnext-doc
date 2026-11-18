# Supporting services · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Crm form

<a id="op-bfa18ed3a6f3f7"></a>
### Resolve route

`operation_relationships_public_pages_customer_relationship_management_form_business_behavior_resolve_route`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** route · path at slice len(prefix) to no value when path.startswith(prefix), otherwise path.

**Local steps**

- Set route from (Platform.form\_dict.get(“route”) or empty text).strip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.get(“route”) → empty text.
- If (route and route differs from “crm-form”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in route → route differs from “crm-form”.
  - Return route.
- Set path from (getattr(Platform.request, “path”, empty text) or empty text).strip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(Platform.request, “path”, empty text) → empty text.
- Set prefix from “crm-form/”.
- Return path at slice len(prefix) to no value when path.startswith(prefix), otherwise path.
  - Value choice on path.startswith(prefix) — true gives path at slice len(prefix) to no value, false gives path.

**Values supplied outside this operation** selected callable from getattr(Platform.request, “path”, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0068.json#L1461) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1497) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1471)

## Service · Data import

<a id="op-b3fe87bde30758"></a>
### Get permission query conditions

`operation_relationships_binding_crm_permissions_data_import_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L217) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L373) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L354)

<a id="op-4fe544bcb3fc4b"></a>
### Has permission

`operation_relationships_binding_crm_permissions_data_import_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true, a comparison result.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L218) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L374) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L355)

<a id="op-a98ec8b7691030"></a>
### Is unrestricted

`operation_relationships_binding_crm_permissions_data_import_is_unrestricted`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L220) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L376) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L357)

<a id="op-d460822bb00644"></a>
### Is sales user only

`operation_relationships_binding_crm_permissions_data_import_is_sales_user_only`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a comparison result.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L219) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L375) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L356)

## Service · Deals

<a id="op-7a7c053b98f5f2"></a>
### Create demo deals

`operation_relationships_demo_deals_business_behavior_create_demo_deals`

**Inputs** lead\_names, demo\_users.

**Record and data access** read “CRM Deal” via get\_value · read “CRM Contacts” via get\_all.

**State and service calls** request set\_value on “CRM Organization”.

**Explicit results** mapping(“deals” → deal\_names\_list, “comments” → comment\_names, “communications” → communication\_names).

**Local steps**

- Bind dependencies convert\_to\_deal.
- Set tuple(session\_user, owner\_1, owner\_2, \_) from resolve\_owners(demo\_users).
- Set \_full\_names from build\_full\_names(session\_user).
- Set d\_alice from convert\_to\_deal(lead = lead\_names at 0, deal = mapping(“status” → “Demo/Making”, “deal\_value” → 120000, “probability” → 50, “deal\_owner” → session\_user)).
- Set d\_david from convert\_to\_deal(lead = lead\_names at 3, deal = mapping(“status” → “Proposal/Quotation”, “deal\_value” → 45000, “probability” → 70, “deal\_owner” → owner\_1)).
- Set d\_henry from convert\_to\_deal(lead = lead\_names at 7, deal = mapping(“status” → “Negotiation”, “deal\_value” → 85000, “probability” → 60, “deal\_owner” → owner\_2)).
- Set d\_iris from convert\_to\_deal(lead = lead\_names at 8, deal = mapping(“status” → “Qualification”, “deal\_value” → 60000, “probability” → 35, “deal\_owner” → session\_user)).
- Set d\_jack from convert\_to\_deal(lead = lead\_names at 9, deal = mapping(“status” → “Won”, “deal\_value” → 175000, “probability” → 100, “deal\_owner” → owner\_1)).
- Set d\_karen from convert\_to\_deal(lead = lead\_names at 10, deal = mapping(“status” → “Lost”, “deal\_value” → 95000, “probability” → 0, “deal\_owner” → owner\_2, …)).
- Set d\_leo from convert\_to\_deal(lead = lead\_names at 11, deal = mapping(“status” → “Lost”, “deal\_value” → 55000, “probability” → 0, “deal\_owner” → session\_user, …)).
- Set deal\_names\_list from list(d\_alice, d\_david, d\_henry, d\_iris, …).
- Set \_converted\_lead\_indices from list(0, 3, 7, 8, …).
- Set \_deal\_days from list(50, 37, 18, 11, …).
- Set \_deal\_owners from list(session\_user, owner\_1, owner\_2, session\_user, …).
- Set \_org\_logos from mapping(“Acme Corp” → “/assets/crm/images/demo/acme-corp.png”, “TechStart Inc” → “/assets/crm/images/demo/techstart-inc.png”, “PivotTech Solutions” → “/assets/crm/images/demo/pivottech-solutions.png”, “Sca ….
- Set now from datetime.now().
- For each tuple(d\_name, days, d\_owner, li) in zip(deal\_names\_list, \_deal\_days, \_deal\_owners, \_converted\_lead\_indices, strict = false).
  - Set ts from (now − timedelta(days = days)).
  - Evaluate backdate(“CRM Deal”, d\_name, d\_owner, ts).
  - Set org from Platform.db.get\_value(“CRM Deal”, d\_name, “organization”).
  - If org.
    - Set logo from \_org\_logos.get(org).
    - If logo.
      - Evaluate Platform.db.set\_value(“CRM Organization”, org, “organization\_logo”, logo, update\_modified = false).
    - Evaluate backdate(“CRM Organization”, org, d\_owner, ts).
  - Set contacts from Platform.get\_all(“CRM Contacts”, filters = mapping(“parent” → d\_name, “parenttype” → “CRM Deal”), pluck = “contact”).
  - For each contact in contacts.
    - If contact.
      - Evaluate backdate(“Contact”, contact, d\_owner, ts).
  - Evaluate backdate(“CRM Lead”, lead\_names at li, d\_owner, ts, set\_creation = false).
  - Evaluate fix\_auto\_records(“CRM Deal”, d\_name, d\_owner, ts).
  - Evaluate fix\_auto\_records(“CRM Lead”, lead\_names at li, d\_owner, ts).
- Set comment\_names from \_create\_deal\_comments(deal\_names\_list, session\_user, owner\_1, owner\_2, …).
- Set communication\_names from \_create\_deal\_communications(deal\_names\_list, session\_user, owner\_1, \_full\_names, …).
- Evaluate \_create\_deal\_versions(deal\_names\_list, session\_user, owner\_1, owner\_2, …).
- Set \_deal\_last\_touched\_days from list(2, 4, 7, 10, …).
- For each tuple(d\_name, days, d\_owner) in zip(deal\_names\_list, \_deal\_last\_touched\_days, \_deal\_owners, strict = false).
  - Evaluate backdate(“CRM Deal”, d\_name, d\_owner, (now − timedelta(days = days)), set\_creation = false).
- Return mapping(“deals” → deal\_names\_list, “comments” → comment\_names, “communications” → communication\_names).

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L3544) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L400) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L381)

<a id="op-ea48703166d2cf"></a>
### Create deal comments

`operation_relationships_demo_deals_business_behavior_create_deal_comments`

**Inputs** deal\_names, session\_user, owner\_1, owner\_2, full\_names, now.

**Explicit results** list of insert\_comment(“CRM Deal”, data at “deal”, data at “owner”, data at “content”, …) for data drawn from comments\_data.

**Local steps**

- Set comments\_data from list(mapping(“deal” → deal\_names at 0, “owner” → session\_user, “content” → text in the contract, “days\_ago” → 3), mapping(“deal” → deal\_names at 1, “owner” → owner\_1, “content” → text in the contract, “day ….
- Return list of insert\_comment(“CRM Deal”, data at “deal”, data at “owner”, data at “content”, …) for data drawn from comments\_data.
  - Draw data from comments\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L5761) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L397) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L378)

<a id="op-91b630c34a191b"></a>
### Create deal communications

`operation_relationships_demo_deals_business_behavior_create_deal_communications`

**Inputs** deal\_names, session\_user, owner\_1, full\_names, now.

**Explicit results** list of insert\_communication(“CRM Deal”, data at “deal”, data, full\_names, …) for data drawn from comms\_data.

**Local steps**

- Set comms\_data from list(mapping(“deal” → deal\_names at 0, “owner” → session\_user, “sent\_or\_received” → “Sent”, “subject” → “Sandbox access details — Acme Corp CRM Evaluation”, …), mapping(“deal” → deal\_names at 1, “owner” →  ….
- Return list of insert\_communication(“CRM Deal”, data at “deal”, data, full\_names, …) for data drawn from comms\_data.
  - Draw data from comms\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L6431) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L398) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L379)

<a id="op-2a1c8a1a463515"></a>
### Create deal versions

`operation_relationships_demo_deals_business_behavior_create_deal_versions`

**Inputs** deal\_names, session\_user, owner\_1, owner\_2, now.

**Local steps**

- Set versions\_data from list(mapping(“deal” → deal\_names at 0, “owner” → session\_user, “changed” → list(list(“probability”, “30”, “50”)), “days\_ago” → 4), mapping(“deal” → deal\_names at 1, “owner” → owner\_1, “changed” → list(list ….
- For each data in versions\_data.
  - Evaluate insert\_version(“CRM Deal”, data at “deal”, data at “owner”, data at “changed”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0015.json#L6864) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L399) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L380)

<a id="op-263b852c266d50"></a>
### Delete demo deals

`operation_relationships_demo_deals_business_behavior_delete_demo_deals`

**Inputs** deal\_data, lead\_names.

**Record and data access** read “CRM Deal” via get\_all · read “Communication” via exists · read “CRM Deal” via exists · read “CRM Contacts” via get\_all · read “CRM Deal” via get\_value · 2 additional forms in the steps below.

**State and service calls** request delete\_doc for “Communication” · request delete\_doc for “CRM Deal” · request delete\_doc for “CRM Organization”.

**Local steps**

- Set communication\_names from deal\_data.get(“communications”, list()).
- Set deal\_names from set(deal\_data.get(“deals”, list())).
- If lead\_names.
  - Set demo\_lead\_deals from Platform.get\_all(“CRM Deal”, filters = mapping(“lead” → list(“in”, lead\_names)), pluck = “name”).
  - Evaluate deal\_names.update(demo\_lead\_deals).
- For each name in communication\_names.
  - If Platform.db.exists(“Communication”, name).
    - Evaluate Platform.delete\_doc(“Communication”, name, ignore\_permissions = true, force = true).
- For each name in deal\_names.
  - If not Platform.db.exists(“CRM Deal”, name).
    - Continue with the next iteration or loop test.
  - Set contact\_names from Platform.get\_all(“CRM Contacts”, filters = mapping(“parent” → name, “parenttype” → “CRM Deal”), pluck = “contact”).
  - Set org from Platform.db.get\_value(“CRM Deal”, name, “organization”).
  - Evaluate Platform.delete\_doc(“CRM Deal”, name, ignore\_permissions = true, force = true).
  - For each contact in contact\_names.
    - If (contact and Platform.db.exists(“Contact”, contact)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact → Platform.db.exists(“Contact”, contact).
      - For each child\_doctype in tuple(“Contact Email”, “Contact Phone”, “Dynamic Link”).
        - Set Child from DocType(child\_doctype).
        - Evaluate nested operand in the contract(nested operand in the contract).delete().where(Child.parent equals contact).run().
      - Set Contact from DocType(“Contact”).
      - Evaluate nested operand in the contract(nested operand in the contract).delete().where(Contact.name equals contact).run().
  - If (org and Platform.db.exists(“CRM Organization”, org)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in org → Platform.db.exists(“CRM Organization”, org).
    - Evaluate Platform.delete\_doc(“CRM Organization”, org, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0016.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L401) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L382)

## Service · Install

<a id="op-ae7e33f8af4c60"></a>
### Before install

`operation_relationships_install_business_behavior_before_install`

**Inputs** no declared parameters.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L6159) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1257) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1233)

<a id="op-527fb9f47f69f0"></a>
### After install

`operation_relationships_install_business_behavior_after_install`

**Inputs** force = false.

**State and service calls** commit.

**Local steps**

- Evaluate add\_default\_lead\_statuses().
- Evaluate add\_default\_deal\_statuses().
- Evaluate add\_default\_communication\_statuses().
- Evaluate add\_default\_fields\_layout(force).
- Evaluate add\_property\_setter().
- Evaluate add\_email\_template\_custom\_fields().
- Evaluate add\_email\_account\_custom\_field().
- Evaluate add\_web\_form\_custom\_fields().
- Evaluate add\_default\_industries().
- Evaluate add\_default\_lead\_sources().
- Evaluate add\_default\_lost\_reasons().
- Evaluate add\_default\_quick\_filters().
- Evaluate add\_standard\_dropdown\_items().
- Evaluate add\_default\_availability\_statuses().
- Evaluate add\_availability\_user\_fields().
- Evaluate add\_default\_scripts().
- Evaluate create\_default\_manager\_dashboard(force).
- Evaluate create\_assignment\_rule\_custom\_fields().
- Evaluate add\_assignment\_rule\_property\_setters().
- Evaluate add\_data\_import\_permissions().
- Evaluate seed\_default\_rules\_and\_mappings().
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L28) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1256) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1232)

<a id="op-5fe90e92db730a"></a>
### Add default lead statuses

`operation_relationships_install_business_behavior_add_default_lead_statuses`

**Inputs** no declared parameters.

**Record and data access** read “CRM Lead Status” via exists.

**State and service calls** request new\_doc for “CRM Lead Status” · call insert on doc.

**Local steps**

- Set statuses from mapping(“New” → mapping(“color” → “gray”, “type” → “Open”, “position” → 1), “Contacted” → mapping(“color” → “orange”, “type” → “Ongoing”, “position” → 2), “Nurture” → mapping(“color” → “blue”, “type” → “On ….
- For each status in statuses.
  - If Platform.db.exists(“CRM Lead Status”, status).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Lead Status”).
  - Set doc.lead\_status from status.
  - Set doc.color from statuses at status at “color”.
  - Set doc.type from statuses at status at “type”.
  - Set doc.position from statuses at status at “position”.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L6540) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1247) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1223)

<a id="op-f558ebbbb17d72"></a>
### Add default deal statuses

`operation_relationships_install_business_behavior_add_default_deal_statuses`

**Inputs** no declared parameters.

**Record and data access** read “CRM Deal Status” via exists.

**State and service calls** request new\_doc for “CRM Deal Status” · call insert on doc.

**Local steps**

- Set statuses from mapping(“Qualification” → mapping(“color” → “gray”, “type” → “Open”, “probability” → 10, “position” → 1), “Demo/Making” → mapping(“color” → “orange”, “type” → “Ongoing”, “probability” → 25, “position” → 2) ….
- For each status in statuses.
  - If Platform.db.exists(“CRM Deal Status”, status).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Deal Status”).
  - Set doc.deal\_status from status.
  - Set doc.color from statuses at status at “color”.
  - Set doc.type from statuses at status at “type”.
  - Set doc.probability from statuses at status at “probability”.
  - Set doc.position from statuses at status at “position”.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1243) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1219)

<a id="op-fb14eff8715af4"></a>
### Add default communication statuses

`operation_relationships_install_business_behavior_add_default_communication_statuses`

**Inputs** no declared parameters.

**Record and data access** read “CRM Communication Status” via exists.

**State and service calls** request new\_doc for “CRM Communication Status” · call insert on doc.

**Local steps**

- Set statuses from list(“Open”, “Replied”).
- For each status in statuses.
  - If Platform.db.exists(“CRM Communication Status”, status).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Communication Status”).
  - Set doc.status from status.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L845) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1242) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1218)

<a id="op-a313a94081162f"></a>
### Add default fields layout

`operation_relationships_install_business_behavior_add_default_fields_layout`

**Inputs** force = false.

**Record and data access** read “CRM Fields Layout” via exists.

**State and service calls** request delete\_doc for “CRM Fields Layout” · request new\_doc for “CRM Fields Layout” · call insert on doc.

**Local steps**

- Set quick\_entry\_layouts from mapping(“CRM Lead-Quick Entry” → mapping(“doctype” → “CRM Lead”, “layout” → “&#91;{"name": "person\_section", "columns": &#91;{"name": "column\_5jrk", "fields": &#91;"salutation", "email"&#93;}, {"name": …”), “CRM Deal-Quic ….
- Set sidebar\_fields\_layouts from mapping(“CRM Lead-Side Panel” → mapping(“doctype” → “CRM Lead”, “layout” → “&#91;{"label": "Details", "name": "details\_section", "opened": true, "columns": &#91;{"name": "column\_kl92", "fields …”), “CRM Deal-Side  ….
- Set data\_fields\_layouts from mapping(“CRM Lead-Data Fields” → mapping(“doctype” → “CRM Lead”, “layout” → “&#91;{"label": "Details", "name": "details\_section", "opened": true, "columns": &#91;{"name": "column\_ZgLG", "fields …”), “CRM Deal-Data ….
- For each layout in quick\_entry\_layouts.
  - If Platform.db.exists(“CRM Fields Layout”, layout).
    - If force.
      - Evaluate Platform.delete\_doc(“CRM Fields Layout”, layout).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Fields Layout”).
  - Set doc.type from “Quick Entry”.
  - Set doc.dt from quick\_entry\_layouts at layout at “doctype”.
  - Set doc.layout from quick\_entry\_layouts at layout at “layout”.
  - Evaluate doc.insert().
- For each layout in sidebar\_fields\_layouts.
  - If Platform.db.exists(“CRM Fields Layout”, layout).
    - If force.
      - Evaluate Platform.delete\_doc(“CRM Fields Layout”, layout).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Fields Layout”).
  - Set doc.type from “Side Panel”.
  - Set doc.dt from sidebar\_fields\_layouts at layout at “doctype”.
  - Set doc.layout from sidebar\_fields\_layouts at layout at “layout”.
  - Evaluate doc.insert().
- For each layout in data\_fields\_layouts.
  - If Platform.db.exists(“CRM Fields Layout”, layout).
    - If force.
      - Evaluate Platform.delete\_doc(“CRM Fields Layout”, layout).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Fields Layout”).
  - Set doc.type from “Data Fields”.
  - Set doc.dt from data\_fields\_layouts at layout at “doctype”.
  - Set doc.layout from data\_fields\_layouts at layout at “layout”.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L1016) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1244) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1220)

<a id="op-e42c7f064ebda3"></a>
### Add property setter

`operation_relationships_install_business_behavior_add_property_setter`

**Inputs** no declared parameters.

**Record and data access** read “Property Setter” via exists.

**State and service calls** request new\_doc for “Property Setter” · call insert on doc.

**Local steps**

- If not Platform.db.exists(“Property Setter”, mapping(“name” → “Contact-main-search\_fields”)).
  - Set doc from Platform.new\_doc(“Property Setter”).
  - Set doc.doctype\_or\_field from “DocType”.
  - Set doc.doc\_type from “Contact”.
  - Set doc.property from “search\_fields”.
  - Set doc.property\_type from “Data”.
  - Set doc.value from “email\_id”.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L2501) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1253) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1229)

<a id="op-a49e8e529c4e69"></a>
### Add email template custom fields

`operation_relationships_install_business_behavior_add_email_template_custom_fields`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set meta from Platform.get\_meta(“Email Template”).
- Set fields from list(mapping(“default” → “0”, “fieldname” → “enabled”, “fieldtype” → “Check”, “label” → “Enabled”, …), mapping(“fieldname” → “reference\_doctype”, “fieldtype” → “Link”, “label” → “Doctype”, “options” → “DocType”, …)).
- Set fields from list of field for field drawn from fields where not meta.has\_field(field at “fieldname”).
  - Draw field from fields, keep a combination only if (not meta.has\_field(field at “fieldname”)).
- If not fields.
  - Return no value.
- Evaluate click.secho(“\* Installing Custom Fields in Email Template”).
- Evaluate create\_custom\_fields(mapping(“Email Template” → fields)).
- Evaluate Platform.clear\_cache(doctype = “Email Template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L2741) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1252) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1228)

<a id="op-b958c45d9f2cb6"></a>
### Add email account custom field

`operation_relationships_install_business_behavior_add_email_account_custom_field`

**Inputs** no declared parameters.

**Local steps**

- If not Platform.get\_meta(“Email Account”).has\_field(“create\_lead\_from\_incoming\_email”).
  - Evaluate click.secho(“\* Installing Custom Fields in Email Account”).
  - Evaluate create\_custom\_fields(mapping(“Email Account” → list(mapping(“default” → “0”, “fieldname” → “create\_lead\_from\_incoming\_email”, “fieldtype” → “Check”, “label” → “Create Lead from Incoming Emails”, …)))).
  - Evaluate Platform.clear\_cache(doctype = “Email Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L3185) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1251) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1227)

<a id="op-4ee4a7ea7e805d"></a>
### Add web form custom fields

`operation_relationships_install_business_behavior_add_web_form_custom_fields`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set custom\_fields from mapping().
- Set meta from Platform.get\_meta(“Web Form”).
- If not (meta.has\_field(“crm\_published”) and meta.has\_field(“crm\_hidden\_defaults”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.has\_field(“crm\_published”) → meta.has\_field(“crm\_hidden\_defaults”).
  - Set custom\_fields at “Web Form” from list(mapping(“default” → “0”, “fieldname” → “crm\_published”, “fieldtype” → “Check”, “label” → “CRM Published”, …), mapping(“fieldname” → “crm\_hidden\_defaults”, “fieldtype” → “Long Text”, “label” → “CRM Hid ….
- If not Platform.get\_meta(“Web Form Field”).has\_field(“placeholder”).
  - Set custom\_fields at “Web Form Field” from list(mapping(“fieldname” → “placeholder”, “fieldtype” → “Data”, “label” → “Placeholder”, “insert\_after” → “description”)).
- If not custom\_fields.
  - Return no value.
- Evaluate click.secho(“\* Installing Custom Fields in Web Form”).
- Evaluate create\_custom\_fields(custom\_fields).
- Evaluate Platform.clear\_cache(doctype = “Web Form”).
- Evaluate Platform.clear\_cache(doctype = “Web Form Field”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L27) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1255) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1231)

<a id="op-1ae33dd961021e"></a>
### Add default industries

`operation_relationships_install_business_behavior_add_default_industries`

**Inputs** no declared parameters.

**Record and data access** read “CRM Industry” via exists.

**State and service calls** request new\_doc for “CRM Industry” · call insert on doc.

**Local steps**

- Set industries from list(“Accounting”, “Advertising”, “Aerospace”, “Agriculture”, …).
- For each industry in industries.
  - If Platform.db.exists(“CRM Industry”, industry).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Industry”).
  - Set doc.industry from industry.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L3862) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1245) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1221)

<a id="op-e7c61ce22f31e8"></a>
### Add default lead sources

`operation_relationships_install_business_behavior_add_default_lead_sources`

**Inputs** no declared parameters.

**Record and data access** read “CRM Lead Source” via exists.

**State and service calls** request new\_doc for “CRM Lead Source” · call insert on doc.

**Local steps**

- Set lead\_sources from list(“Email”, “Existing Customer”, “Reference”, “Advertisement”, …).
- For each source in lead\_sources.
  - If Platform.db.exists(“CRM Lead Source”, source).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Lead Source”).
  - Set doc.source\_name from source.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L4229) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1246) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1222)

<a id="op-9a322b42e62ffc"></a>
### Add default lost reasons

`operation_relationships_install_business_behavior_add_default_lost_reasons`

**Inputs** no declared parameters.

**Record and data access** read “CRM Lost Reason” via exists.

**State and service calls** request new\_doc for “CRM Lost Reason” · call insert on doc.

**Local steps**

- Set lost\_reasons from list(mapping(“reason” → “Pricing”, “description” → “The prospect found the pricing to be too high or not competitive.”), mapping(“reason” → “Competition”, “description” → “The prospect chose a competitor's ….
- For each reason in lost\_reasons.
  - If Platform.db.exists(“CRM Lost Reason”, reason at “reason”).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Lost Reason”).
  - Set doc.lost\_reason from reason at “reason”.
  - Set doc.description from reason at “description”.
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L4458) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1248) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1224)

<a id="op-58ded90fc1c07e"></a>
### Add default quick filters

`operation_relationships_install_business_behavior_add_default_quick_filters`

**Inputs** no declared parameters.

**Record and data access** read “CRM Global Settings” via exists.

**State and service calls** request new\_doc for “CRM Global Settings” · call insert on doc.

**Local steps**

- Set quick\_filters from mapping(“CRM Lead” → list(“lead\_name”, “email”, “organization”, “status”, …), “CRM Deal” → list(“organization”, “status”, “probability”, “email”), “Contact” → list(“status”, “email\_id”, “phone”), “CRM Orga ….
- For each quick\_filter in quick\_filters.
  - If Platform.db.exists(“CRM Global Settings”, mapping(“dt” → quick\_filter)).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“CRM Global Settings”).
  - Set doc.dt from quick\_filter.
  - Set doc.json from json.dumps(quick\_filters at quick\_filter).
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L26) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1249) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1225)
