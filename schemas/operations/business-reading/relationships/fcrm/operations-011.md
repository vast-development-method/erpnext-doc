# Lead and deal records · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Enterprise crm settings

<a id="op-973ee3a3913d25"></a>
### Get product sync status

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_product_sync_status`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping() · mapping(“products” → \_get\_products(), “items” → \_get\_synced\_items(), “failed” → get\_open\_sync\_issues(), “unsynced” → \_get\_unsynced\_counts()).

**Local steps**

- If not Platform.has\_permission(“CRM Product”, “read”).
  - Return mapping().
- Return mapping(“products” → \_get\_products(), “items” → \_get\_synced\_items(), “failed” → get\_open\_sync\_issues(), “unsynced” → \_get\_unsynced\_counts()).

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Product”, “read”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L3705) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1208) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1184)

<a id="op-f4894833f84055"></a>
### Get unsynced counts

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_unsynced_counts`

**Inputs** no declared parameters.

**Record and data access** read “Enterprise CRM Settings” via get\_single · read “CRM Product” via count.

**Explicit results** mapping(“items” → items, “products” → Platform.db.count(“CRM Product”, filters = mapping(“Enterprise\_item\_code” → list(“is”, “not set”))), “sync\_products” → bool(settings.sync\_products)).

**Local steps**

- Set settings from Platform.get\_single(“Enterprise CRM Settings”).
- Set items from \_count\_linked(“Item”, “crm\_product\_code”, is\_set = false) when \_can\_read\_items(), otherwise 0.
  - Value choice on \_can\_read\_items() — true gives \_count\_linked(“Item”, “crm\_product\_code”, is\_set = false), false gives 0.
- Return mapping(“items” → items, “products” → Platform.db.count(“CRM Product”, filters = mapping(“Enterprise\_item\_code” → list(“is”, “not set”))), “sync\_products” → bool(settings.sync\_products)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L3902) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1212) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1188)

<a id="op-eef0fc6af37b19"></a>
### Get products

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_products`

**Inputs** no declared parameters.

**Record and data access** read “CRM Product” via get\_all · read “CRM Product” via count.

**Explicit results** mapping(“count” → Platform.db.count(“CRM Product”), “rows” → rows).

**Local steps**

- Set rows from Platform.get\_all(“CRM Product”, fields = list(“name”, “product\_code”, “product\_name”, “Enterprise\_item\_code”), limit = 20, order\_by = “modified desc”).
- Evaluate \_set\_product\_item\_groups(rows).
- Return mapping(“count” → Platform.db.count(“CRM Product”), “rows” → rows).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L4155) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1209) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1185)

<a id="op-12124381b1fef7"></a>
### Get synced items

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_synced_items`

**Inputs** no declared parameters.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping(“count” → 0, “rows” → list()) · mapping(“count” → \_count\_linked(“Item”, “crm\_product\_code”), “rows” → Platform.get\_all(“Item”, fields = list(“name”, “item\_code”, “item\_name”, “item\_group”, …), filters = mapping(“crm\_product\_code” → list( ….

**Local steps**

- If not \_can\_read\_items().
  - Return mapping(“count” → 0, “rows” → list()).
- Return mapping(“count” → \_count\_linked(“Item”, “crm\_product\_code”), “rows” → Platform.get\_all(“Item”, fields = list(“name”, “item\_code”, “item\_name”, “item\_group”, …), filters = mapping(“crm\_product\_code” → list( ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L4361) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1211) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1187)

<a id="op-8b16012eb082f2"></a>
### Set product item groups

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_set_product_item_groups`

**Inputs** rows.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value.

**Local steps**

- Set item\_codes from list of row.Enterprise\_item\_code for row drawn from rows where row.Enterprise\_item\_code.
  - Draw row from rows, keep a combination only if (row.Enterprise\_item\_code).
- If (not item\_codes or not \_can\_read\_items()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_codes → not \_can\_read\_items().
  - Return no value.
- Set item\_groups from Platform.get\_all(“Item”, fields = list(“name”, “item\_group”), filters = mapping(“name” → list(“in”, item\_codes))).
- Set item\_groups from mapping of row.name → row.item\_group for row drawn from item\_groups.
  - Draw row from item\_groups.
- For each row in rows.
  - Set row at “item\_group” from item\_groups.get(row.Enterprise\_item\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L4632) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1216) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1192)

<a id="op-b7dd6d4ecf0d12"></a>
### Count linked

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_count_linked`

**Inputs** doctype, fieldname, is\_set = true.

**Record and data access** read doctype via count.

**Explicit results** 0 · Platform.db.count(doctype, filters = mapping(fieldname → list(“is”, operator))).

**Local steps**

- If not Platform.db.has\_column(doctype, fieldname).
  - Return 0.
- Set operator from “set” when is\_set, otherwise “not set”.
  - Value choice on is\_set — true gives “set”, false gives “not set”.
- Return Platform.db.count(doctype, filters = mapping(fieldname → list(“is”, operator))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L4956) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1180) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1156)

<a id="op-860e162f73967b"></a>
### Can read items

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_can_read_items`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L5147) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1177) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1153)

<a id="op-707b0fae9d9be4"></a>
### Get Enterprise site client

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_enterprise_site_client`

**Inputs** Enterprise\_crm\_settings.

**Explicit results** PlatformClient(site\_url, api\_key = api\_key, api\_secret = api\_secret).

**Local steps**

- Set site\_url from Enterprise\_crm\_settings.Enterprise\_site\_url.
- Set api\_key from Enterprise\_crm\_settings.api\_key.
- Set api\_secret from Enterprise\_crm\_settings.get\_password(“api\_secret”, raise\_exception = false).
- Return PlatformClient(site\_url, api\_key = api\_key, api\_secret = api\_secret).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L5254) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1203) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1179)

<a id="op-013fc23e1f59cb"></a>
### Get local customer

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_local_customer`

**Inputs** crm\_deal.

**Record and data access** read “Customer” via exists · read “CRM Deal” via get\_value.

**Explicit results** customer.

**Local steps**

- Set customer from Platform.db.exists(“Customer”, mapping(“crm\_deal” → crm\_deal)).
- If not customer.
  - Set customer from Platform.db.get\_value(“CRM Deal”, crm\_deal, “Enterprise\_customer”).
- Return customer.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L5405) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1204) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1180)

<a id="op-422f76ac1ac2f2"></a>
### Get customer link

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_customer_link`

**Inputs** crm\_deal.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Deal” via get\_value.

**Explicit results** get\_url\_to\_form(“Customer”, customer) when customer, otherwise empty text · formatted text {Enterprise\_crm\_settings.Enterprise\_site\_url}/app/customer/{customer} · empty text.

**Local steps**

- Set Enterprise\_crm\_settings from \_get\_enabled\_settings().
- If not Enterprise\_crm\_settings.is\_Enterprise\_in\_different\_site.
  - Set customer from get\_local\_customer(crm\_deal).
  - Return get\_url\_to\_form(“Customer”, customer) when customer, otherwise empty text.
    - Value choice on customer — true gives get\_url\_to\_form(“Customer”, customer), false gives empty text.
- Set client from get\_Enterprise\_site\_client(Enterprise\_crm\_settings).
- Attempt the following.
  - Set customer from client.get\_list(“Customer”, filters = mapping(“crm\_deal” → crm\_deal)).
  - Set customer from customer at 0.get(“name”) when customer, otherwise no value.
    - Value choice on customer — true gives customer at 0.get(“name”), false gives no value.
  - If not customer.
    - Set customer from Platform.db.get\_value(“CRM Deal”, crm\_deal, “Enterprise\_customer”).
  - If customer.
    - Return formatted text {Enterprise\_crm\_settings.Enterprise\_site\_url}/app/customer/{customer}.
  - Return empty text.
- On failure (Exception).
  - Evaluate \_log\_and\_throw(“Error while fetching customer in Enterprise, check error log for more details”, formatted text Error while fetching customer in remote site: {Enterprise\_crm\_settings.Enterprise\_site\_url}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0046.json#L5562) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1199) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1175)

<a id="op-9721eda88f89f2"></a>
### Quotation permission

`operation_relationships_binding_crm_fcrm_doctype_enterprise_crm_settings_enterprise_crm_settings_quotation_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** ptype.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L205) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L361) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L342)

<a id="op-70d363a548d511"></a>
### Can view quotations

`operation_relationships_binding_crm_fcrm_doctype_enterprise_crm_settings_enterprise_crm_settings_can_view_quotations`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_quotation\_permission(“read”).

**Local steps**

- Return \_quotation\_permission(“read”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L202) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L358) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L339)

<a id="op-622bba653efd46"></a>
### Can create quotations

`operation_relationships_binding_crm_fcrm_doctype_enterprise_crm_settings_enterprise_crm_settings_can_create_quotations`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_quotation\_permission(“create”).

**Local steps**

- Return \_quotation\_permission(“create”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L201) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L357) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L338)

<a id="op-9c149d0c297e1a"></a>
### Get deal quotations

`operation_relationships_binding_crm_fcrm_doctype_enterprise_crm_settings_enterprise_crm_settings_get_deal_quotations`

**Inputs** crm\_deal.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Enterprise CRM Settings” via get\_single · read “Quotation” via get\_list.

**Explicit results** list() · rows.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid deal” · validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not isinstance(crm\_deal, str).
  - Call the validation error handler Platform.throw(translated “Invalid deal”, Platform.ValidationError).
- Set settings from Platform.get\_single(“Enterprise CRM Settings”).
- If not settings.enabled.
  - Return list().
- If not Platform.has\_permission(“CRM Deal”, doc = crm\_deal).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- If (not settings.is\_Enterprise\_in\_different\_site and not Platform.has\_permission(“Quotation”, ptype = “read”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not settings.is\_Enterprise\_in\_different\_site → not Platform.has\_permission(“Quotation”, ptype = “read”).
  - Return list().
- If not settings.is\_Enterprise\_in\_different\_site.
  - Set rows from Platform.get\_list(“Quotation”, filters = mapping(“crm\_deal” → crm\_deal), fields = QUOTATION\_LIST\_FIELDS, order\_by = “modified desc”, limit\_page\_length = 0).
  - For each row in rows.
    - Set row at “url” from get\_url\_to\_form(“Quotation”, row at “name”).
  - Return rows.
- Set client from get\_Enterprise\_site\_client(settings).
- Attempt the following.
  - Set rows from client.get\_list(“Quotation”, filters = mapping(“crm\_deal” → crm\_deal), fields = QUOTATION\_LIST\_FIELDS, order\_by = “modified desc”, limit\_page\_length = 0).
- On failure (Exception).
  - Evaluate \_log\_and\_throw(“Error while fetching quotations in Enterprise, check error log for more details”, formatted text Error while fetching quotations in remote site: {settings.Enterprise\_site\_url}).
- For each row in rows.
  - Set row at “url” from formatted text {settings.Enterprise\_site\_url}/app/quotation/{row at “name”}.
- Return rows.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, doc = crm\_deal), Platform.has\_permission(“Quotation”, ptype = “read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L203) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L359) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L340)

<a id="op-0106a4485ce807"></a>
### Notify deal quotation change

`operation_relationships_binding_crm_fcrm_doctype_enterprise_crm_settings_enterprise_crm_settings_notify_deal_quotation_change`

**Inputs** doc, method = no value.

**State and service calls** publish realtime with “crm\_quotation\_update”.

**Local steps**

- Set crm\_deal from doc.get(“crm\_deal”).
- If crm\_deal.
  - Evaluate Platform.publish\_realtime(“crm\_quotation\_update”, mapping(“crm\_deal” → crm\_deal), doctype = “CRM Deal”, docname = crm\_deal, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“crm\_quotation\_update”, mapping(“crm\_deal” → crm\_deal), doctype = “CRM Deal”, docname = crm\_deal, after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L204) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L360) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L341)

<a id="op-79420f129302a7"></a>
### Get quotation url

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_quotation_resource_address`

**Inputs** crm\_deal, organization = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** formatted text {base\_url}?{query\_string}.

**Local steps**

- Set Enterprise\_crm\_settings from \_get\_enabled\_settings().
- Set contact from get\_primary\_contact(crm\_deal).
- Set address from get\_organization\_address(organization).
- Set address\_name from address.get(“name”) when address, otherwise no value.
  - Value choice on address — true gives address.get(“name”), false gives no value.
- If not Enterprise\_crm\_settings.is\_Enterprise\_in\_different\_site.
  - Set customer from get\_local\_customer(crm\_deal).
  - Set base\_url from formatted text {get\_url\_to\_list(“Quotation”)}/new.
  - Set params from mapping(“quotation\_to” → “Customer” when customer, otherwise “CRM Deal”, “crm\_deal” → crm\_deal, “party\_name” → (customer or crm\_deal), “company” → Enterprise\_crm\_settings.Enterprise\_company, …).
    - Value choice on customer — true gives “Customer”, false gives “CRM Deal”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer → crm\_deal.
- Otherwise.
  - Set site\_url from Enterprise\_crm\_settings.get(“Enterprise\_site\_url”).
  - Set base\_url from formatted text {site\_url}/app/quotation/new.
  - Set prospect from create\_prospect\_in\_remote\_site(crm\_deal, Enterprise\_crm\_settings).
  - Set params from mapping(“quotation\_to” → “Prospect”, “crm\_deal” → crm\_deal, “party\_name” → prospect, “company” → Enterprise\_crm\_settings.Enterprise\_company, …).
- Set query\_string from “&amp;”.join(generator of formatted text {key}={value} for tuple(key, value) drawn from params.items() where value is distinct from no value).
  - Draw tuple(key, value) from params.items(), keep a combination only if (value is distinct from no value).
- Return formatted text {base\_url}?{query\_string}.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1210) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1186)

<a id="op-5e35dcb39fd6cc"></a>
### Create prospect in remote site

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_create_prospect_in_remote_site`

**Inputs** crm\_deal, Enterprise\_crm\_settings.

**Record and data access** resolve a document from “CRM Deal” via get\_cached\_doc.

**Explicit results** client.post\_api(“Enterprise.crm.Platform\_crm\_api.create\_prospect\_against\_crm\_deal”, mapping(“organization” → doc.organization, “lead\_name” → doc.lead\_name, “no\_of\_employees” → doc.no\_of\_employees, “deal\_ow ….

**Local steps**

- Attempt the following.
  - Set client from get\_Enterprise\_site\_client(Enterprise\_crm\_settings).
  - Set doc from Platform.get\_cached\_doc(“CRM Deal”, crm\_deal).
  - Set contacts from get\_contacts(doc).
  - Set address from (get\_organization\_address(doc.organization) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_organization\_address(doc.organization) → no value.
  - If (address and not isinstance(address, dict)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in address → not isinstance(address, dict).
    - Set address from address.as\_dict().
  - Return client.post\_api(“Enterprise.crm.Platform\_crm\_api.create\_prospect\_against\_crm\_deal”, mapping(“organization” → doc.organization, “lead\_name” → doc.lead\_name, “no\_of\_employees” → doc.no\_of\_employees, “deal\_ow ….
    - Value choice on contacts — true gives json.dumps(contacts), false gives no value.
    - Value choice on address — true gives json.dumps(address), false gives no value.
- On failure (Exception).
  - Evaluate \_log\_and\_throw(“Error while creating prospect in Enterprise, check error log for more details”, formatted text Error while creating prospect in remote site: {Enterprise\_crm\_settings.Enterprise\_site\_url}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, crm\_deal).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L796) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1184) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1160)

<a id="op-3c0f2dc42e00af"></a>
### Prefill quotation items

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_prefill_quotation_items`

**Inputs** crm\_deal.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Deal” via exists · resolve a document from “CRM Deal” via get\_doc · read “CRM Product” via get\_value.

**Explicit results** list() · items.

**Local steps**

- If not Platform.db.exists(“CRM Deal”, crm\_deal).
  - Return list().
- Set deal from Platform.get\_doc(“CRM Deal”, crm\_deal).
- Set items from list().
- For each row in deal.products.
  - Set item\_code from Platform.db.get\_value(“CRM Product”, row.product\_code, “Enterprise\_item\_code”).
  - If not item\_code.
    - Continue with the next iteration or loop test.
  - Evaluate items.append(mapping(“item\_code” → item\_code, “qty” → (row.qty or 1), “price\_list\_rate” → (row.rate or 0), “discount\_percentage” → (row.discount\_percentage or 0))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.qty → 1.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.rate → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.discount\_percentage → 0.
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L1455) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1215) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1191)

<a id="op-47ca6f8afbd4a9"></a>
### Get primary contact

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_primary_contact`

**Inputs** crm\_deal.

**Record and data access** resolve a document from “CRM Deal” via get\_cached\_doc.

**Explicit results** c.contact · no value.

**Local steps**

- Set doc from Platform.get\_cached\_doc(“CRM Deal”, crm\_deal).
- For each c in doc.contacts.
  - If c.is\_primary.
    - Return c.contact.
- Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, crm\_deal).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L1840) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1207) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1183)

<a id="op-a5acdce5b72796"></a>
### Get contacts

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_contacts`

**Inputs** doc.

**Explicit results** list of mapping(“contact” → c.contact, “full\_name” → c.full\_name, “email” → c.email, “mobile\_no” → c.mobile\_no, …) for c drawn from doc.contacts.

**Local steps**

- Return list of mapping(“contact” → c.contact, “full\_name” → c.full\_name, “email” → c.email, “mobile\_no” → c.mobile\_no, …) for c drawn from doc.contacts.
  - Draw c from doc.contacts.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L1959) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1198) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1174)

<a id="op-26580d6230db01"></a>
### Get organization address

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_get_organization_address`

**Inputs** organization = no value.

**Record and data access** read “CRM Organization” via get\_value · resolve a document from “Address” via get\_cached\_doc.

**Explicit results** no value · mapping(“name” → address.name, “address\_title” → address.address\_title, “address\_type” → address.address\_type, “address\_line1” → address.address\_line1, …).

**Local steps**

- If not organization.
  - Return no value.
- Set address from Platform.db.get\_value(“CRM Organization”, organization, “address”).
- Set address from Platform.get\_cached\_doc(“Address”, address) when address, otherwise no value.
  - Value choice on address — true gives Platform.get\_cached\_doc(“Address”, address), false gives no value.
- If not address.
  - Return no value.
- Return mapping(“name” → address.name, “address\_title” → address.address\_title, “address\_type” → address.address\_type, “address\_line1” → address.address\_line1, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Address”, address).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L2139) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1206) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1182)

<a id="op-8f940f45e210e2"></a>
### Create customer in Enterprise

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_create_customer_in_enterprise`

**Inputs** doc, method.

**Record and data access** read “Enterprise CRM Settings” via get\_single.

**Explicit results** no value.

**Local steps**

- Set Enterprise\_crm\_settings from Platform.get\_single(“Enterprise CRM Settings”).
- If (not Enterprise\_crm\_settings.enabled or not Enterprise\_crm\_settings.create\_customer\_on\_status\_change or doc.status differs from Enterprise\_crm\_settings.deal\_status).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Enterprise\_crm\_settings.enabled → not Enterprise\_crm\_settings.create\_customer\_on\_status\_change → doc.status differs from Enterprise\_crm\_settings.deal\_status.
  - Return no value.
- Evaluate create\_customer\_from\_deal(doc, Enterprise\_crm\_settings).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L2539) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1182) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1158)

<a id="op-eaefdfc43c02b7"></a>
### Create customer on sales order

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_create_customer_on_sales_order`

**Inputs** doc, method.

**Explicit results** no value.

**Local steps**

- If doc.customer.
  - Return no value.
- Set crm\_deal from get\_deal\_from\_sales\_order(doc).
- Set customer from check\_customer\_for\_deal(crm\_deal) when crm\_deal, otherwise no value.
  - Value choice on crm\_deal — true gives check\_customer\_for\_deal(crm\_deal), false gives no value.
- If customer.
  - Set doc.customer from customer.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L2703) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1183) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1159)

<a id="op-cfd9680f39693d"></a>
### Check customer for deal

`operation_relationships_fcrm_record_definitions_enterprise_application_customer_relationship_management_settings_business_behavior_check_customer_for_deal`

**Inputs** crm\_deal.

**Record and data access** read “Enterprise CRM Settings” via get\_single · read “CRM Deal” via exists · resolve a document from “CRM Deal” via get\_cached\_doc.

**Explicit results** no value · customer.

**Local steps**

- Set Enterprise\_crm\_settings from Platform.get\_single(“Enterprise CRM Settings”).
- If (not Enterprise\_crm\_settings.enabled or Enterprise\_crm\_settings.is\_Enterprise\_in\_different\_site).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Enterprise\_crm\_settings.enabled → Enterprise\_crm\_settings.is\_Enterprise\_in\_different\_site.
  - Return no value.
- If (not crm\_deal or not Platform.db.exists(“CRM Deal”, crm\_deal)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not crm\_deal → not Platform.db.exists(“CRM Deal”, crm\_deal).
  - Return no value.
- Set customer from get\_local\_customer(crm\_deal).
- If not customer.
  - Set customer from create\_customer\_from\_deal(Platform.get\_cached\_doc(“CRM Deal”, crm\_deal), Enterprise\_crm\_settings).
- Return customer.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, crm\_deal).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0047.json#L2852) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1178) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1154)
