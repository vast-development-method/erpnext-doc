# Lead and deal records · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Enterprise crm settings

<a id="op-7d5c740569ae85"></a>
### Check customer for quotation

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_check_customer_for_quotation`

**Inputs** quotation.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Quotation” via get\_value.

**Explicit results** no value · check\_customer\_for\_deal(crm\_deal).

**Local steps**

- Set crm\_deal from Platform.db.get\_value(“Quotation”, quotation, “crm\_deal”).
- If not crm\_deal.
  - Return no value.
- Return check\_customer\_for\_deal(crm\_deal).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L3130) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1179) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1155)

<a id="op-4044250742ae59"></a>
### Get deal from sales order

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_deal_from_sales_order`

**Inputs** doc.

**Record and data access** read “Quotation” via get\_value.

**Explicit results** crm\_deal · no value.

**Local steps**

- For each item in doc.items.
  - Set quotation from item.get(“prevdoc\_docname”).
  - If quotation.
    - Set crm\_deal from Platform.db.get\_value(“Quotation”, quotation, “crm\_deal”).
    - If crm\_deal.
      - Return crm\_deal.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L3272) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1201) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1177)

<a id="op-a3cb134311707a"></a>
### Create customer from deal

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_create_customer_from_deal`

**Inputs** doc, Enterprise\_crm\_settings.

**Record and data access** read “Territory” via exists · read “Industry Type” via exists.

**State and service calls** request set\_value on “CRM Deal” · publish realtime with “crm\_customer\_created”.

**Explicit results** customer\_name.

**Explicit failure paths** validation helper — translated “Organization or a primary Contact is required to create a customer” · validation helper — translated “Enterprise is not installed in the current site” · propagate active failure.

**Local steps**

- Set contacts from get\_contacts(doc).
- Set address from get\_organization\_address(doc.organization).
- If doc.organization.
  - Set customer\_title from doc.organization.
  - Set customer\_type from “Company”.
- Otherwise.
  - Set primary\_contact from next(generator of c for c drawn from contacts where c.get(“is\_primary”), no value).
    - Draw c from contacts, keep a combination only if (c.get(“is\_primary”)).
  - Set customer\_title from ((primary\_contact or mapping()).get(“full\_name”) or doc.lead\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (primary\_contact or mapping()).get(“full\_name”) → doc.lead\_name.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in primary\_contact → mapping().
  - If not customer\_title.
    - Call the validation error handler Platform.throw(translated “Organization or a primary Contact is required to create a customer”).
  - Set customer\_type from “Individual”.
- Set customer\_data from mapping(“customer\_name” → customer\_title, “customer\_type” → customer\_type, “territory” → doc.territory, “default\_currency” → doc.currency, …).
  - Value choice on address — true gives json.dumps(address), false gives no value.
- Attempt the following.
  - If not Enterprise\_crm\_settings.is\_Enterprise\_in\_different\_site.
    - Attempt the following.
      - Bind dependencies create\_customer.
    - On failure (ImportError).
      - Call the validation error handler Platform.throw(translated “Enterprise is not installed in the current site”).
    - If (doc.territory and not Platform.db.exists(“Territory”, doc.territory)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.territory → not Platform.db.exists(“Territory”, doc.territory).
      - Set customer\_data at “territory” from empty text.
    - If (doc.industry and not Platform.db.exists(“Industry Type”, doc.industry)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.industry → not Platform.db.exists(“Industry Type”, doc.industry).
      - Set customer\_data at “industry” from empty text.
    - Set customer\_name from create\_customer(customer\_data).
  - Otherwise.
    - Set client from get\_Enterprise\_site\_client(Enterprise\_crm\_settings).
    - If (doc.territory and not client.get\_list(“Territory”, filters = mapping(“name” → doc.territory))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.territory → not client.get\_list(“Territory”, filters = mapping(“name” → doc.territory)).
      - Set customer\_data at “territory” from empty text.
    - If (doc.industry and not client.get\_list(“Industry Type”, filters = mapping(“name” → doc.industry))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.industry → not client.get\_list(“Industry Type”, filters = mapping(“name” → doc.industry)).
      - Set customer\_data at “industry” from empty text.
    - Set customer\_name from client.post\_api(“Enterprise.crm.Platform\_crm\_api.create\_customer”, customer\_data).
  - If not customer\_name.
    - Evaluate \_log\_and\_throw(“Error while creating customer in Enterprise, check error log for more details”, formatted text Error while creating customer in Enterprise for CRM Deal: {doc.name}).
- On failure (tuple(Platform.ValidationError, Platform.PermissionError)).
  - Propagate the active failure.
- On failure (Exception).
  - Evaluate \_log\_and\_throw(“Error while creating customer in Enterprise, check error log for more details”).
- If customer\_name.
  - Evaluate Platform.db.set\_value(“CRM Deal”, doc.name, “Enterprise\_customer”, customer\_name).
  - Evaluate Platform.publish\_realtime(“crm\_customer\_created”, user = Platform.session.user).
- Return customer\_name.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“crm\_customer\_created”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L23) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1181) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1157)

<a id="op-589cec10fc5755"></a>
### Get crm form script

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_customer_relationship_form_script`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** multiline text in the contract.

**Local steps**

- Return multiline text in the contract.

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L25) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1200) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1176)

## Record · Fcrm note

<a id="op-f26d6dccbcf155"></a>
### FCRMNote.default list data

`operation_relationships_fcrm_record_definitions_fcrm_note_business_behavior_customer_relationship_note_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → list(), “rows” → rows).

**Local steps**

- Set rows from list(“name”, “title”, “content”, “reference\_doctype”, …).
- Return mapping(“columns” → list(), “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L4874) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1217) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1193)

<a id="op-f86d4a9b60a0e5"></a>
### FCRMNote.on update

`operation_relationships_binding_crm_fcrm_doctype_fcrm_note_fcrm_note_fcrmnote_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.notify\_mentions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify mentions](operations-012.md#op-ab50195786ae13).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L207) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L363) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L344)

<a id="op-ab50195786ae13"></a>
### FCRMNote.notify mentions

`operation_relationships_binding_crm_fcrm_doctype_fcrm_note_fcrm_note_fcrmnote_notify_mentions`

**Inputs** self.

**Record and data access** read “CRM Notification” via get\_all · read self.reference\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.reference\_doctype does not belong to tuple(“CRM Lead”, “CRM Deal”) or not self.reference\_docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.reference\_doctype does not belong to tuple(“CRM Lead”, “CRM Deal”) → not self.reference\_docname.
  - Return no value.
- Set before from self.get\_doc\_before\_save().
- Set already\_mentioned from set of m.email for m drawn from extract\_mentions(before.content) when before, otherwise set().
  - Value choice on before — true gives set of m.email for m drawn from extract\_mentions(before.content), false gives set().
  - Draw m from extract\_mentions(before.content).
- Set mentioned from (set of m.email for m drawn from extract\_mentions(self.content) − already\_mentioned).
  - Draw m from extract\_mentions(self.content).
- If mentioned.
  - Update mentioned using − set(Platform.get\_all(“CRM Notification”, filters = mapping(“type” → “Mention”, “notification\_type\_doctype” → “FCRM Note”, “notification\_type\_doc” → self.name, “to\_user” → tuple(“in”, list(mentioned))), pluck = …).
- If not mentioned.
  - Return no value.
- Set is\_lead from self.reference\_doctype equals “CRM Lead”.
- Set record from Platform.db.get\_value(self.reference\_doctype, self.reference\_docname, list(“lead\_name”) when is\_lead, otherwise list(“organization”, “lead\_name”), as\_dict = true).
  - Value choice on is\_lead — true gives list(“lead\_name”), false gives list(“organization”, “lead\_name”).
- Set name from record.lead\_name when is\_lead, otherwise (record.organization or record.lead\_name) when record, otherwise empty text.
  - Value choice on record — true gives record.lead\_name when is\_lead, otherwise (record.organization or record.lead\_name), false gives empty text.
  - Value choice on is\_lead — true gives record.lead\_name, false gives (record.organization or record.lead\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in record.organization → record.lead\_name.
- Set author from get\_fullname(Platform.session.user).
- Set notification\_text from formatted text   &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;  &lt;span class="font-medium text-ink-gray-9"&gt;{escape\_html(author)}&lt;/span&gt;  &lt;span&gt;{translated “men.
  - Value choice on is\_lead — true gives translated “lead”, false gives translated “deal”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → self.reference\_docname.
- For each email in mentioned.
  - Evaluate notify\_user(mapping(“owner” → Platform.session.user, “assigned\_to” → email, “notification\_type” → “Mention”, “message” → self.content, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L206) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L362) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L343)

<a id="op-ee72f39bf0c61c"></a>
### Set pinned

`operation_relationships_binding_crm_fcrm_doctype_fcrm_note_fcrm_note_set_pinned`

**Inputs** name, pinned.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “FCRM Note” via get\_doc · resolve a document from mapping(“doctype” → “Version”, “ref\_doctype” → “FCRM Note”, “docname” → name, “data” → Platform.as\_json(mapping(“changed” → list(list(“pinned”, int(nested operand in the contract.pinned), int(pinned)))))) via get\_doc.

**State and service calls** request set\_value on “FCRM Note” · call insert on Platform.get\_doc(mapping(“doctype” → “Version”, “ref\_doctype” → “FCRM Note”, “docname” → name, “data” → Platform.as\_json(mapping(“changed” → list(list(“pinned”, nested operand in the contract(nested operan ….

**Explicit results** no value.

**Local steps**

- Set note from Platform.get\_doc(“FCRM Note”, name).
- Evaluate note.check\_permission(“write”).
- If bool(note.pinned) equals bool(pinned).
  - Return no value.
- Evaluate Platform.db.set\_value(“FCRM Note”, name, mapping(“pinned” → int(pinned), “pinned\_by” → Platform.session.user when pinned, otherwise no value, “pinned\_on” → Platform.utils.now() when pinned, otherwise no va ….
  - Value choice on pinned — true gives Platform.session.user, false gives no value.
  - Value choice on pinned — true gives Platform.utils.now(), false gives no value.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Version”, “ref\_doctype” → “FCRM Note”, “docname” → name, “data” → Platform.as\_json(mapping(“changed” → list(nested operand in the contract))))).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from note.check\_permission(“write”) · clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L208) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L364) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L345)

## Record · Fcrm settings

<a id="op-9f55d56359ceff"></a>
### FCRMSettings.restore defaults

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_restore_defaults`

**Inputs** self, force = false.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate after\_install(force).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L5018) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1224) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1200)

<a id="op-9b576c8afa4cda"></a>
### FCRMSettings.restore demo data

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_restore_demo_data`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate create\_demo\_data().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L5104) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1225) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1201)

<a id="op-9072b1efe7fc9e"></a>
### FCRMSettings.validate

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.do\_not\_allow\_to\_delete\_if\_standard().
- Evaluate self.setup\_forecasting().
- Evaluate self.make\_currency\_read\_only().

If control reaches the end, it returns no value.

**Methods declared on this owner** [do not allow to delete if standard](operations-012.md#op-f0dc79a61dccb1), [setup forecasting](operations-012.md#op-429e9796892148), [make currency read only](operations-012.md#op-5d438c3d29e23e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L5169) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1227) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1203)

<a id="op-f0dc79a61dccb1"></a>
### FCRMSettings.do not allow to delete if standard

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_do_not_allow_to_delete_if_standard`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot delete standard items {0}”.format(“, ”.join(deleted\_standard\_items)).

**Local steps**

- If not self.has\_value\_changed(“dropdown\_items”).
  - Return no value.
- Set old\_items from self.get\_doc\_before\_save().get(“dropdown\_items”).
- Set standard\_new\_items from list of d.name1 for d drawn from self.dropdown\_items where d.is\_standard.
  - Draw d from self.dropdown\_items, keep a combination only if (d.is\_standard).
- Set standard\_old\_items from list of d.name1 for d drawn from old\_items where d.is\_standard.
  - Draw d from old\_items, keep a combination only if (d.is\_standard).
- Set deleted\_standard\_items from (set(standard\_old\_items) − set(standard\_new\_items)).
- If deleted\_standard\_items.
  - Set standard\_dropdown\_items from get\_standard\_dropdown\_items().
  - If not deleted\_standard\_items.intersection(standard\_dropdown\_items).
    - Return no value.
  - Call the validation error handler Platform.throw(translated “Cannot delete standard items {0}”.format(“, ”.join(deleted\_standard\_items))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L5260) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1221) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1197)

<a id="op-429e9796892148"></a>
### FCRMSettings.setup forecasting

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_setup_forecasting`

**Inputs** self.

**Local steps**

- If self.has\_value\_changed(“enable\_forecasting”).
  - If not self.enable\_forecasting.
    - Evaluate self.remove\_forecasting\_section(“Side Panel”).
    - Evaluate self.remove\_forecasting\_section(“Quick Entry”).
    - Evaluate delete\_property\_setter(“CRM Deal”, “reqd”, “expected\_closure\_date”).
    - Evaluate delete\_property\_setter(“CRM Deal”, “reqd”, “expected\_deal\_value”).
  - Otherwise.
    - Evaluate self.add\_forecasting\_section(“Side Panel”).
    - Evaluate self.add\_forecasting\_section(“Quick Entry”).
    - Evaluate make\_property\_setter(“CRM Deal”, “expected\_closure\_date”, “reqd”, 1 when self.enable\_forecasting, otherwise 0, …).
      - Value choice on self.enable\_forecasting — true gives 1, false gives 0.
    - Evaluate make\_property\_setter(“CRM Deal”, “expected\_deal\_value”, “reqd”, 1 when self.enable\_forecasting, otherwise 0, …).
      - Value choice on self.enable\_forecasting — true gives 1, false gives 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove forecasting section](operations-012.md#op-e8785d2edcbd56), [add forecasting section](operations-012.md#op-b8d57788aab237).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L5657) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1226) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1202)

<a id="op-5d438c3d29e23e"></a>
### FCRMSettings.make currency read only

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_make_currency_read_only`

**Inputs** self.

**Local steps**

- If (self.currency and self.has\_value\_changed(“currency”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency → self.has\_value\_changed(“currency”).
  - Evaluate make\_property\_setter(“FCRM Settings”, “currency”, “read\_only”, 1, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L6057) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1222) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1198)

<a id="op-b8d57788aab237"></a>
### FCRMSettings.add forecasting section

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_add_forecasting_section`

**Inputs** self, layout\_type.

**Record and data access** read “CRM Fields Layout” via exists · resolve a document from “CRM Fields Layout” via get\_doc.

**State and service calls** call insert on sections · call save on doc.

**Explicit results** no value.

**Local steps**

- Set layout\_name from formatted text CRM Deal-{layout\_type}.
- If not Platform.db.exists(“CRM Fields Layout”, layout\_name).
  - Return no value.
- Set doc from Platform.get\_doc(“CRM Fields Layout”, layout\_name).
- Set layout from json.loads(doc.layout) when doc.layout, otherwise list().
  - Value choice on doc.layout — true gives json.loads(doc.layout), false gives list().
- Set has\_tabs from any(generator of “sections” belongs to item for item drawn from layout).
  - Draw item from layout.
- Set sections from layout at negative 1.setdefault(“sections”, list()) when has\_tabs, otherwise layout.
  - Value choice on has\_tabs — true gives layout at negative 1.setdefault(“sections”, list()), false gives layout.
- Set all\_sections from list of section for tab drawn from layout, then section drawn from tab.get(“sections”, list()) when has\_tabs, otherwise layout.
  - Value choice on has\_tabs — true gives list of section for tab drawn from layout, then section drawn from tab.get(“sections”, list()), false gives layout.
  - Draw tab from layout.
  - Draw section from tab.get(“sections”, list()).
- If any(generator of section.get(“name”) equals “forecasted\_sales\_section” for section drawn from all\_sections).
  - Draw section from all\_sections.
  - Return no value.
- Set existing\_fields from set of (field.get(“fieldname”) or field.get(“name”)) when isinstance(field, dict), otherwise field for section drawn from all\_sections, then column drawn from (section.get(“columns”) or list()), then field ….
  - Draw section from all\_sections.
  - Draw column from (section.get(“columns”) or list()).
  - Draw field from (column.get(“fields”) or list()).
  - Value choice on isinstance(field, dict) — true gives (field.get(“fieldname”) or field.get(“name”)), false gives field.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“fieldname”) → field.get(“name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“columns”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in column.get(“fields”) → list().
- Set fields from list of field for field drawn from tuple(“expected\_deal\_value”, “expected\_closure\_date”, “probability”) where field does not belong to existing\_fields.
  - Draw field from tuple(“expected\_deal\_value”, “expected\_closure\_date”, “probability”), keep a combination only if (field does not belong to existing\_fields).
- If not fields.
  - Return no value.
- If layout\_type equals “Side Panel”.
  - Set new\_section from mapping(“name” → “forecasted\_sales\_section”, “label” → “Forecasted Sales”, “opened” → true, “columns” → list(mapping(“name” → “forecasted\_sales\_column”, “fields” → fields))).
  - If (sections and sections at 0.get(“name”) equals “contacts\_section”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sections → sections at 0.get(“name”) equals “contacts\_section”.
    - Evaluate sections.insert(1, new\_section).
  - Otherwise.
    - Evaluate sections.insert(0, new\_section).
- Otherwise.
  - Set new\_section from mapping(“name” → “forecasted\_sales\_section”, “columns” → list of mapping(“name” → (field + “\_column”), “fields” → list(field)) for field drawn from fields).
    - Draw field from fields.
  - Evaluate sections.append(new\_section).
- Set doc.layout from json.dumps(layout).
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1220) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1196)

<a id="op-e8785d2edcbd56"></a>
### FCRMSettings.remove forecasting section

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_customer_relationship_settings_remove_forecasting_section`

**Inputs** self, layout\_type.

**Record and data access** read “CRM Fields Layout” via exists · resolve a document from “CRM Fields Layout” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- Set layout\_name from formatted text CRM Deal-{layout\_type}.
- If not Platform.db.exists(“CRM Fields Layout”, layout\_name).
  - Return no value.
- Set doc from Platform.get\_doc(“CRM Fields Layout”, layout\_name).
- Set layout from json.loads(doc.layout) when doc.layout, otherwise list().
  - Value choice on doc.layout — true gives json.loads(doc.layout), false gives list().
- Set has\_tabs from any(generator of “sections” belongs to item for item drawn from layout).
  - Draw item from layout.
- If has\_tabs.
  - For each tab in layout.
    - Set tab at “sections” from list of section for section drawn from tab.get(“sections”, list()) where section.get(“name”) differs from “forecasted\_sales\_section”.
      - Draw section from tab.get(“sections”, list()), keep a combination only if (section.get(“name”) differs from “forecasted\_sales\_section”).
- Otherwise.
  - Set layout from list of section for section drawn from layout where section.get(“name”) differs from “forecasted\_sales\_section”.
    - Draw section from layout, keep a combination only if (section.get(“name”) differs from “forecasted\_sales\_section”).
- Set doc.layout from json.dumps(layout).
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L1202) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1223) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1199)

<a id="op-a51f3382dc9ed9"></a>
### Get standard dropdown items

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_get_standard_dropdown_items`

**Inputs** no declared parameters.

**Explicit results** list of item.get(“name1”) for item drawn from Platform.get\_hooks(“standard\_dropdown\_items”).

**Local steps**

- Return list of item.get(“name1”) for item drawn from Platform.get\_hooks(“standard\_dropdown\_items”).
  - Draw item from Platform.get\_hooks(“standard\_dropdown\_items”).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“standard\_dropdown\_items”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L1710) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1229) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1205)

<a id="op-a0fa6e28a1457b"></a>
### After migrate

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_after_migrate`

**Inputs** no declared parameters.

**Local steps**

- Evaluate sync\_table(“dropdown\_items”, “standard\_dropdown\_items”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L1798) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1218) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1194)

<a id="op-fc8ce32530125e"></a>
### Sync table

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_sync_table`

**Inputs** key, hook.

**State and service calls** call save on crm\_settings.

**Local steps**

- Set crm\_settings from FCRMSettings(“FCRM Settings”).
- Set existing\_items from mapping of d.name1 → d for d drawn from crm\_settings.get(key).
  - Draw d from crm\_settings.get(key).
- Set new\_standard\_items from mapping().
- Set count from 0.
- For each item in Platform.get\_hooks(hook).
  - If item.get(“name1”) does not belong to existing\_items.
    - Evaluate crm\_settings.append(key, item, count).
  - Set new\_standard\_items at item.get(“name1”) from true.
  - Update count using + 1.
- Set items from crm\_settings.get(key).
- Set items from list of item for item drawn from items where not (item.is\_standard and item.name1 does not belong to new\_standard\_items).
  - Draw item from items, keep a combination only if (not (item.is\_standard and item.name1 does not belong to new\_standard\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_standard → item.name1 does not belong to new\_standard\_items.
- Evaluate crm\_settings.set(key, items).
- Evaluate crm\_settings.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L1851) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1230) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1206)

<a id="op-41777f6c2d50ce"></a>
### Create forecasting script

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_create_forecasting_script`

**Inputs** no declared parameters.

**Record and data access** read “CRM Form Script” via exists · resolve a document from mapping(“doctype” → “CRM Form Script”, “name” → “Forecasting Script”, “dt” → “CRM Deal”, “view” → “Form”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Form Script”, “name” → “Forecasting Script”, “dt” → “CRM Deal”, “view” → “Form”, …)).

**Local steps**

- If not Platform.db.exists(“CRM Form Script”, “Forecasting Script”).
  - Set script from get\_forecasting\_script().
  - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Form Script”, “name” → “Forecasting Script”, “dt” → “CRM Deal”, “view” → “Form”, …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L2307) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1219) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1195)

<a id="op-c87df4fcb58a2a"></a>
### Get forecasting script

`operation_relationships_fcrm_record_definitions_fcrm_settings_business_behavior_get_forecasting_script`

**Inputs** no declared parameters.

**Explicit results** multiline text in the contract.

**Local steps**

- Return multiline text in the contract.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L2553) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1228) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1204)

## Service · Utils

<a id="op-7cdc80331b18e3"></a>
### Add or remove lost reason section in sidepanel

`operation_relationships_fcrm_record_definitions_utils_business_behavior_add_or_remove_lost_reason_section_in_sidepanel`

**Inputs** doc.

**Record and data access** read status\_doctype via get\_value · resolve a document from “CRM Fields Layout” via get\_doc.

**State and service calls** call save on layout\_doc.

**Explicit results** no value.

**Local steps**

- Set doctype from doc.doctype.
- If doctype does not belong to tuple(“CRM Deal”, “CRM Lead”).
  - Return no value.
- Set status\_doctype from “CRM Deal Status” when doctype equals “CRM Deal”, otherwise “CRM Lead Status”.
  - Value choice on doctype equals “CRM Deal” — true gives “CRM Deal Status”, false gives “CRM Lead Status”.
- Set status from no value.
- If getattr(doc, “status”, no value).
  - Set status from Platform.db.get\_value(status\_doctype, doc.status, “type”).
- Set is\_lost from (status and status equals “Lost”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status → status equals “Lost”.
- Set layout\_doc from Platform.get\_doc(“CRM Fields Layout”, formatted text {doctype}-Side Panel).
- Set sections from json.loads(layout\_doc.layout).
- Set lost\_reason\_section from mapping(“name” → “lost\_reason\_section”, “label” → “Lost Reason”, “opened” → true, “columns” → list(mapping(“name” → “lost\_reason\_column”, “fields” → list(“lost\_reason”, “lost\_notes”)))).
- Set section\_exists from any(generator of section.get(“name”) equals “lost\_reason\_section” for section drawn from sections).
  - Draw section from sections.
- If (is\_lost and not section\_exists).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_lost → not section\_exists.
  - If (sections and sections at 0.get(“name”) equals “contacts\_section”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sections → sections at 0.get(“name”) equals “contacts\_section”.
    - Set sections from list(expanded sections at slice no value to 1, lost\_reason\_section, expanded sections at slice 1 to no value).
  - Otherwise.
    - Set sections from list(lost\_reason\_section, expanded sections).
  - Set layout\_doc.layout from json.dumps(sections).
  - Evaluate layout\_doc.save(ignore\_permissions = true).
- Otherwise.
  - If (not is\_lost and section\_exists).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_lost → section\_exists.
    - Set sections from list of section for section drawn from sections where section.get(“name”) differs from “lost\_reason\_section”.
      - Draw section from sections, keep a combination only if (section.get(“name”) differs from “lost\_reason\_section”).
    - Set layout\_doc.layout from json.dumps(sections).
    - Evaluate layout\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, “status”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0048.json#L5202) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1240) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1216)
