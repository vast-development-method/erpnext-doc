# Sales relationships · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Opportunity

[Record definition](../../../../data/record-types/opportunity.json)

<a id="op-14a52460e402d9"></a>
### Opportunity.validate party

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_validate_party`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If self.opportunity\_from equals “Customer”.
  - Evaluate validate\_party\_frozen\_disabled(self.company, “Customer”, self.party\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0433.json#L3132) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1248)

<a id="op-b0e118ca327853"></a>
### Opportunity.validate party contact and address

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_validate_party_contact_and_address`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} {1} is not linked to {2} {3}”.format(translated doctype, Platform.bold(value), translated self.opportunity\_from, Platform.bold(self.party\_name)).

**Local steps**

- If not self.party\_name.
  - Return no value.
- For each tuple(fieldname, doctype) in tuple(tuple(“contact\_person”, “Contact”), tuple(“customer\_address”, “Address”)).
  - Set value from self.get(fieldname).
  - If (not value or not (self.has\_value\_changed(fieldname) or self.has\_party\_changed())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not value → not (self.has\_value\_changed(fieldname) or self.has\_party\_changed()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(fieldname) → self.has\_party\_changed().
    - Continue with the next iteration or loop test.
  - If not self.is\_linked\_to\_party(doctype, value).
    - Call the validation error handler Platform.throw(translated “{0} {1} is not linked to {2} {3}”.format(translated doctype, Platform.bold(value), translated self.opportunity\_from, Platform.bold(self.party\_name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has party changed](operations-010.md#op-4dcc8450c975f6), [is linked to party](operations-010.md#op-0ece29b7cc035a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L543)

<a id="op-0ece29b7cc035a"></a>
### Opportunity.is linked to party

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_is_linked_to_party`

**Inputs** self, doctype, name.

**Declared result** bool.

**Record and data access** read “Dynamic Link” via exists.

**Explicit results** bool(Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → doctype, “parent” → name, “link\_doctype” → self.opportunity\_from, “link\_name” → self.party\_name))).

**Local steps**

- Return bool(Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → doctype, “parent” → name, “link\_doctype” → self.opportunity\_from, “link\_name” → self.party\_name))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L535)

<a id="op-49396e903fed79"></a>
### Opportunity.refresh party fields

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_refresh_party_fields`

**Inputs** self.

**Record and data access** read self.opportunity\_from via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.has\_party\_changed()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_party\_changed().
  - Return no value.
- Set previous from self.get\_doc\_before\_save().
- If (not self.has\_value\_changed(“title”) and self.title equals previous.customer\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_value\_changed(“title”) → self.title equals previous.customer\_name.
  - Set self.title from self.customer\_name.
- Set party\_meta from Platform.get\_meta(self.opportunity\_from).
- For each fieldname in PARTY\_DERIVED\_FIELDS.
  - If (party\_meta.has\_field(fieldname) and self.holds\_previous\_party\_value(previous, fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_meta.has\_field(fieldname) → self.holds\_previous\_party\_value(previous, fieldname).
    - Evaluate self.set(fieldname, Platform.db.get\_value(self.opportunity\_from, self.party\_name, fieldname)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has party changed](operations-010.md#op-4dcc8450c975f6), [holds previous party value](operations-010.md#op-a3040286a35d78).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L537)

<a id="op-a3040286a35d78"></a>
### Opportunity.holds previous party value

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_holds_previous_party_value`

**Inputs** self, previous, fieldname.

**Declared result** bool.

**Explicit results** false · self.get(fieldname) equals get\_party\_field\_value(previous, fieldname).

**Local steps**

- If self.has\_value\_changed(fieldname).
  - Return false.
- Return self.get(fieldname) equals get\_party\_field\_value(previous, fieldname).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L533)

<a id="op-4dcc8450c975f6"></a>
### Opportunity.has party changed

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_has_party_changed`

**Inputs** self.

**Declared result** bool.

**Explicit results** (self.has\_value\_changed(“party\_name”) or self.has\_value\_changed(“opportunity\_from”)).

**Local steps**

- Return (self.has\_value\_changed(“party\_name”) or self.has\_value\_changed(“opportunity\_from”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“party\_name”) → self.has\_value\_changed(“opportunity\_from”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L532)

<a id="op-532dd34b22f34f"></a>
### Opportunity.validate cust name

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_validate_customer_name`

**Inputs** self.

**Record and data access** read “Customer” via get\_value · read “Prospect Lead” via get\_value · read “Lead” via get\_value.

**Local steps**

- If self.party\_name.
  - If self.opportunity\_from equals “Customer”.
    - Set self.customer\_name from Platform.db.get\_value(“Customer”, self.party\_name, “customer\_name”).
  - Otherwise.
    - If self.opportunity\_from equals “Lead”.
      - Set customer\_name from Platform.db.get\_value(“Prospect Lead”, mapping(“lead” → self.party\_name), “parent”).
      - If not customer\_name.
        - Set tuple(lead\_name, company\_name) from Platform.db.get\_value(“Lead”, self.party\_name, list(“lead\_name”, “company\_name”)).
        - Set customer\_name from (company\_name or lead\_name).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_name → lead\_name.
      - Set self.customer\_name from customer\_name.
    - Otherwise.
      - If self.opportunity\_from equals “Prospect”.
        - Set self.customer\_name from self.party\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0433.json#L3236) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1246)

<a id="op-75c4dbb2237952"></a>
### Opportunity.validate item details

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_validate_item_details`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.get(“items”).
  - Return no value.
- Set item\_fields from tuple(“item\_name”, “description”, “item\_group”, “brand”).
- For each d in self.items.
  - If not d.item\_code.
    - Continue with the next iteration or loop test.
  - Set item from Platform.db.get\_value(“Item”, d.item\_code, item\_fields, as\_dict = true).
  - For each key in item\_fields.
    - If not d.get(key).
      - Evaluate d.set(key, item.get(key)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0433.json#L3658) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1247)

<a id="op-fe132d37654434"></a>
### Get party prospect

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_get_party_prospect`

**Inputs** opportunity\_from, party\_name.

**Declared result** (str bitwise or no value).

**Record and data access** read “Prospect Lead” via get\_value.

**Explicit results** party\_name · Platform.db.get\_value(“Prospect Lead”, mapping(“lead” → party\_name), “parent”).

**Local steps**

- If opportunity\_from equals “Prospect”.
  - Return party\_name.
- If opportunity\_from equals “Lead”.
  - Return Platform.db.get\_value(“Prospect Lead”, mapping(“lead” → party\_name), “parent”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L517)

<a id="op-73a2fbc692a914"></a>
### Get party field value

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_get_party_field_value`

**Inputs** opportunity, fieldname.

**Declared result** (str bitwise or no value).

**Record and data access** read opportunity.opportunity\_from via get\_value.

**Explicit results** no value · Platform.db.get\_value(opportunity.opportunity\_from, opportunity.party\_name, fieldname).

**Local steps**

- If (not opportunity.party\_name or not Platform.get\_meta(opportunity.opportunity\_from).has\_field(fieldname)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not opportunity.party\_name → not Platform.get\_meta(opportunity.opportunity\_from).has\_field(fieldname).
  - Return no value.
- Return Platform.db.get\_value(opportunity.opportunity\_from, opportunity.party\_name, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L516)

<a id="op-4f7866d2fd9578"></a>
### Get item details

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_get_item_details`

**Inputs** item\_code.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via exists · execute query text (SELECT, Item).

**Explicit results** mapping(“item\_name” → ((item and item at 0 at “item\_name”) or empty text), “uom” → ((item and item at 0 at “stock\_uom”) or empty text), “description” → ((item and item at 0 at “description”) or empty text) ….

**Local steps**

- If Platform.db.exists(“Item”, item\_code).
  - Evaluate Platform.has\_permission(“Item”, “read”, item\_code, throw = true).
- Set item from Platform.db.sql(query text (SELECT, Item), item\_code, as\_dict = 1).
- Return mapping(“item\_name” → ((item and item at 0 at “item\_name”) or empty text), “uom” → ((item and item at 0 at “stock\_uom”) or empty text), “description” → ((item and item at 0 at “description”) or empty text) ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and item at 0 at “item\_name”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item at 0 at “item\_name”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and item at 0 at “stock\_uom”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item at 0 at “stock\_uom”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and item at 0 at “description”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item at 0 at “description”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and item at 0 at “image”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item at 0 at “image”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and item at 0 at “item\_group”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item at 0 at “item\_group”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and item at 0 at “brand”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item at 0 at “brand”.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, item\_code, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1231)

<a id="op-84982dc491fc0a"></a>
### Make quotation

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Opportunity”, source\_name, mapping(“Opportunity” → mapping(“doctype” → “Quotation”, “field\_map” → mapping(“opportunity\_from” → “quotation\_to”, “name” → “enq\_no”)), “Opportunity Item” → mapp ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L521)

<a id="op-3c883cb4257eed"></a>
### Make quotation.set missing values

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_quotation_set_missing_values`

**Inputs** source, target.

**Record and data access** resolve a document from target via get\_doc · read “Company” via get\_cached\_value.

**Local steps**

- Bind dependencies \_get\_default\_taxes\_and\_charges.
- Set quotation from Platform.get\_doc(target).
- Set company\_currency from Platform.get\_cached\_value(“Company”, quotation.company, “default\_currency”).
- If company\_currency equals quotation.currency.
  - Set exchange\_rate from 1.
- Otherwise.
  - Set exchange\_rate from get\_exchange\_rate(quotation.currency, company\_currency, quotation.transaction\_date, args = “for\_selling”).
- Set quotation.conversion\_rate from exchange\_rate.
- Set taxes from \_get\_default\_taxes\_and\_charges(“Sales Taxes and Charges Template”, company = quotation.company).
- If taxes.get(“taxes”).
  - Evaluate quotation.update(taxes).
- Evaluate quotation.run\_method(“set\_missing\_values”).
- Evaluate quotation.run\_method(“calculate\_taxes\_and\_totals”).
- If not source.get(“items”, list()).
  - Set quotation.opportunity from source.name.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, quotation.company, “default\_currency”) · selected callable from quotation.run\_method(“set\_missing\_values”), quotation.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L522)

<a id="op-8e80ae245cb50a"></a>
### Make request for quotation

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_request_for_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation update\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Opportunity”, source\_name, mapping(“Opportunity” → mapping(“doctype” → “Request for Quotation”), “Opportunity Item” → mapping(“doctype” → “Request for Quotation Item”, “field\_map” → list(li ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L523)

<a id="op-35c2a1cdde3f4b"></a>
### Make request for quotation.update item

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_request_for_quotation_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set target.conversion\_factor from get\_conversion\_factor(obj.item\_code, obj.uom) at “conversion\_factor”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L524)

<a id="op-f69cd8bbc5e17e"></a>
### Make customer

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_customer`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Opportunity”, source\_name, mapping(“Opportunity” → mapping(“doctype” → “Customer”, “field\_map” → mapping(“currency” → “default\_currency”, “customer\_name” → “customer\_name”))), target\_doc, …).
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L518)

<a id="op-c2ecc6e3ddfc7b"></a>
### Make customer.set missing values

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_customer_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate validate\_no\_customer\_exists(source).
- Set target.opportunity\_name from source.name.
- If source.opportunity\_from equals “Lead”.
  - Set target.lead\_name from source.party\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L519)

<a id="op-99dc8496040a9a"></a>
### Validate no customer exists

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_validate_no_customer_exists`

**Inputs** opportunity.

**Record and data access** read “Customer” via get\_all.

**Explicit failure paths** validation helper — translated “Opportunity {0} is already for a Customer”.format(Platform.bold(opportunity.name)) · validation helper — translated “Customer {0} already exists for this Opportunity”.format(get\_link\_to\_form(“Customer”, customer at 0)).

**Local steps**

- If opportunity.opportunity\_from equals “Customer”.
  - Call the validation error handler Platform.throw(translated “Opportunity {0} is already for a Customer”.format(Platform.bold(opportunity.name))).
- Set or\_filters from mapping(“opportunity\_name” → opportunity.name).
- If opportunity.opportunity\_from equals “Lead”.
  - Set or\_filters at “lead\_name” from opportunity.party\_name.
- If customer bound to Platform.get\_all(“Customer”, or\_filters = or\_filters, pluck = “name”, limit = 1).
  - Call the validation error handler Platform.throw(translated “Customer {0} already exists for this Opportunity”.format(get\_link\_to\_form(“Customer”, customer at 0))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L547)

<a id="op-98897783bc2889"></a>
### Make supplier quotation

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_supplier_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Set doclist from get\_mapped\_doc(“Opportunity”, source\_name, mapping(“Opportunity” → mapping(“doctype” → “Supplier Quotation”, “field\_map” → mapping(“name” → “opportunity”)), “Opportunity Item” → mapping(“doctype” → “Suppli ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L525)

<a id="op-2343bfab52609c"></a>
### Set multiple status

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_set_multiple_status`

**Inputs** names, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Opportunity” via get\_doc.

**State and service calls** call save on opp.

**Local steps**

- Set names from json.loads(names).
- For each name in names.
  - Set opp from Platform.get\_doc(“Opportunity”, name).
  - Set opp.status from status.
  - Evaluate opp.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1250)

<a id="op-f48dbd2c680011"></a>
### Auto close opportunity

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_auto_close_opportunity`

**Inputs** no declared parameters.

**Record and data access** read “CRM Settings” via get\_single\_value.

**State and service calls** request set\_value on “Opportunity”.

**Local steps**

- Set auto\_close\_after\_days from (Platform.db.get\_single\_value(“CRM Settings”, “close\_opportunity\_after\_days”) or 15).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“CRM Settings”, “close\_opportunity\_after\_days”) → 15.
- Set table from Platform.qb.DocType(“Opportunity”).
- Set opportunities from nested operand in the contract(nested operand in the contract).select(table.name).where((table.modified &lt; (nested operand in the contract() − nested operand in the contract(days = nested operand in the con ….
- If opportunities.
  - Evaluate Platform.db.set\_value(“Opportunity”, mapping(“name” → tuple(“in”, opportunities)), “status”, “Closed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “close\_opportunity\_after\_days”) · clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1230)

<a id="op-648c4cd3927110"></a>
### Make opportunity from communication

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_make_opportunity_from_communication`

**Inputs** communication, company, ignore\_communication\_links = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Communication” via get\_doc · resolve a document from mapping(“doctype” → “Opportunity”, “company” → company, “opportunity\_from” → opportunity\_from, “party\_name” → lead) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Opportunity”, “company” → company, “opportunity\_from” → opportunity\_from, “party\_name” → lead)).

**Explicit results** doc.reference\_name · opportunity.name.

**Local steps**

- Bind dependencies make\_lead\_from\_communication.
- Evaluate Platform.has\_permission(“Communication”, doc = communication, throw = true).
- Set doc from Platform.get\_doc(“Communication”, communication).
- If (doc.reference\_doctype equals “Opportunity” and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype equals “Opportunity” → doc.reference\_name.
  - Return doc.reference\_name.
- Set lead from doc.reference\_name when doc.reference\_doctype equals “Lead”, otherwise no value.
  - Value choice on doc.reference\_doctype equals “Lead” — true gives doc.reference\_name, false gives no value.
- If not lead.
  - Set lead from make\_lead\_from\_communication(communication, ignore\_communication\_links = true).
- Set opportunity\_from from “Lead”.
- Set opportunity from Platform.get\_doc(mapping(“doctype” → “Opportunity”, “company” → company, “opportunity\_from” → opportunity\_from, “party\_name” → lead)).insert().
- Evaluate link\_communication\_to\_document(doc, “Opportunity”, opportunity.name, ignore\_communication\_links).
- Return opportunity.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Communication”, doc = communication, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L520)

<a id="op-fd2d0fe768a98b"></a>
### Get data

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_opportunity_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “opportunity”, “transactions” → list(mapping(“items” → list(“Quotation”, “Request for Quotation”, “Supplier Quotation”)))).

**Local steps**

- Return mapping(“fieldname” → “opportunity”, “transactions” → list(mapping(“items” → list(“Quotation”, “Request for Quotation”, “Supplier Quotation”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0433.json#L5106) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1251)

## Report · Opportunity summary by sales stage

<a id="op-c283c30b6551e2"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** OpportunitySummaryBySalesStage(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return OpportunitySummaryBySalesStage(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L3) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1308)
