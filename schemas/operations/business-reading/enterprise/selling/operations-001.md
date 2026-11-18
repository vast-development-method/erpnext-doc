# Sales · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Address and contacts

<a id="op-82c66a5ef6a644"></a>
### Execute

`operation_enterprise_selling_report_address_and_contacts_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(get\_columns(filters), get\_data(filters)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0660.json#L5869) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1511)

<a id="op-614f9241ccd0bd"></a>
### Get columns

`operation_enterprise_selling_report_address_and_contacts_business_behavior_get_columns`

**Inputs** filters.

**State and service calls** call insert on columns.

**Explicit results** columns.

**Local steps**

- Set party\_type from filters.get(“party\_type”).
- Set party\_type\_value from get\_party\_group(party\_type).
- Set columns from list(formatted text {party\_type}:Link/{party\_type}, formatted text {Platform.unscrub(str(party\_type\_value))}::150, mapping(“label” → translated “Address”, “fieldtype” → “Link”, “options” → “Address”, “hidd ….
- If should\_add\_party\_name(party\_type).
  - Evaluate columns.insert(2, formatted text {party\_type} Name:Data:150).
- Return columns.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1512)

<a id="op-dfa7dca10e0291"></a>
### Get data

`operation_enterprise_selling_report_address_and_contacts_business_behavior_get_data`

**Inputs** filters.

**Explicit results** get\_party\_addresses\_and\_contact(party\_type, party, party\_group, filters).

**Local steps**

- Set party\_type from filters.get(“party\_type”).
- Set party from filters.get(“party\_name”).
- Set party\_group from get\_party\_group(party\_type).
- Return get\_party\_addresses\_and\_contact(party\_type, party, party\_group, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0660.json#L6482) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1513)

<a id="op-9da70e06b352b7"></a>
### Get party addresses and contact

`operation_enterprise_selling_report_address_and_contacts_business_behavior_get_party_addresses_and_contact`

**Inputs** party\_type, party, party\_group, filters.

**Record and data access** read party\_type via get\_list.

**Explicit results** list() · data.

**Local steps**

- Set data from list().
- Set query\_filters from no value.
- Set party\_details from Platform.\_dict().
- If not party\_type.
  - Return list().
- If party.
  - Set query\_filters from mapping(“name” → party).
- Set field from get\_party\_name\_field(party\_type).
- Set fetch\_party\_list from Platform.get\_list(party\_type, filters = query\_filters, fields = list(“name”, party\_group, field), as\_list = true).
- Set party\_list from list of d at 0 for d drawn from fetch\_party\_list.
  - Draw d from fetch\_party\_list.
- Set party\_groups from mapping().
- Set party\_name\_map from mapping().
- For each d in fetch\_party\_list.
  - Set party\_groups at d at 0 from d at 1.
  - Set party\_name\_map at d at 0 from d at 2.
- For each d in party\_list.
  - Evaluate party\_details.setdefault(d, Platform.\_dict()).
- Set party\_details from get\_party\_details(party\_type, party\_list, “Address”, party\_details).
- Set party\_details from get\_party\_details(party\_type, party\_list, “Contact”, party\_details).
- Set add\_party\_name from should\_add\_party\_name(party\_type).
- For each tuple(party, details) in party\_details.items().
  - Set addresses from details.get(“address”, list()).
  - Set contacts from details.get(“contact”, list()).
  - If not any(list(addresses, contacts)).
    - Set result from list(party).
    - Evaluate result.append(party\_groups at party).
    - If add\_party\_name.
      - Evaluate result.append(party\_name\_map at party).
    - Evaluate result.extend(add\_blank\_columns\_for(“Contact”)).
    - Evaluate result.extend(add\_blank\_columns\_for(“Address”)).
    - Evaluate data.append(result).
  - Otherwise.
    - Set addresses from list(map(list, addresses)).
    - Set contacts from list(map(list, contacts)).
    - Set max\_length from max(len(addresses), len(contacts)).
    - For each idx in range(0, max\_length).
      - Set result from list(party).
      - Evaluate result.append(party\_groups at party).
      - If add\_party\_name.
        - Evaluate result.append(party\_name\_map at party).
      - Set address from addresses at idx when idx &lt; len(addresses), otherwise add\_blank\_columns\_for(“Address”).
        - Value choice on idx &lt; len(addresses) — true gives addresses at idx, false gives add\_blank\_columns\_for(“Address”).
      - Set contact from contacts at idx when idx &lt; len(contacts), otherwise add\_blank\_columns\_for(“Contact”).
        - Value choice on idx &lt; len(contacts) — true gives contacts at idx, false gives add\_blank\_columns\_for(“Contact”).
      - Evaluate result.extend(address).
      - Evaluate result.extend(contact).
      - Evaluate data.append(result).
- Return data.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1514)

<a id="op-3dda06a4a71899"></a>
### Get party details

`operation_enterprise_selling_report_address_and_contacts_business_behavior_get_party_details`

**Inputs** party\_type, party\_list, doctype, party\_details.

**Record and data access** read doctype via get\_list.

**Explicit results** party\_details.

**Local steps**

- Set filters from list(list(“Dynamic Link”, “link\_doctype”, “=”, party\_type), list(“Dynamic Link”, “link\_name”, “in”, party\_list)).
- Set fields from list(“′tabDynamic Link′.link\_name”, expanded field\_map.get(doctype, list())).
- Set records from Platform.get\_list(doctype, filters = filters, fields = fields, as\_list = true).
- For each d in records.
  - Set details from party\_details.get(d at 0).
  - Evaluate details.setdefault(Platform.scrub(doctype), list()).append(d at slice 1 to no value).
- Return party\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L1501) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1515)

<a id="op-96daea6741549d"></a>
### Add blank columns for

`operation_enterprise_selling_report_address_and_contacts_business_behavior_add_blank_columns_for`

**Inputs** doctype.

**Explicit results** list of empty text for field drawn from field\_map.get(doctype, list()).

**Local steps**

- Return list of empty text for field drawn from field\_map.get(doctype, list()).
  - Draw field from field\_map.get(doctype, list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L1869) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1510)

<a id="op-2690a611ab6c3e"></a>
### Get party name field

`operation_enterprise_binding_enterprise_selling_report_address_and_contacts_address_and_contacts_get_party_name_field`

**Inputs** party\_type.

**Explicit results** field at party\_type.

**Local steps**

- Set field from mapping(“Customer” → “customer\_name”, “Supplier” → “supplier\_name”, “Sales Partner” → “partner\_name”, “Lead” → “lead\_name”).
- Return field at party\_type.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L94)

<a id="op-ba95617f8db007"></a>
### Get party group

`operation_enterprise_selling_report_address_and_contacts_business_behavior_get_party_group`

**Inputs** party\_type.

**Explicit results** no value · group at party\_type.

**Local steps**

- If not party\_type.
  - Return no value.
- Set group from mapping(“Customer” → “customer\_group”, “Supplier” → “supplier\_group”, “Sales Partner” → “partner\_type”, “Lead” → “status”).
- Return group at party\_type.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L1945) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1516)

<a id="op-5113c9225844dd"></a>
### Should add party name

`operation_enterprise_selling_report_address_and_contacts_business_behavior_should_add_party_name`

**Inputs** party\_type.

**Record and data access** read doctype via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(doctype, fieldname) belongs to list(“Naming Series”, “Auto Name”) · false.

**Local steps**

- Set settings\_map from mapping(“Supplier” → tuple(“Buying Settings”, “supp\_master\_name”), “Customer” → tuple(“Selling Settings”, “cust\_master\_name”)).
- If party\_type belongs to settings\_map.
  - Set tuple(doctype, fieldname) from settings\_map.get(party\_type).
  - Return Platform.db.get\_single\_value(doctype, fieldname) belongs to list(“Naming Series”, “Auto Name”).
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(doctype, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L2107) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1517)

## Report · Available stock for packing items

<a id="op-a487f80e25566a"></a>
### Execute

`operation_enterprise_selling_report_available_stock_for_packing_items_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns().
- Set iwq\_map from get\_item\_warehouse\_quantity\_map().
- Set item\_map from get\_item\_details(list(iwq\_map.keys())).
- Set data from list().
- For each tuple(sbom, warehouse) in iwq\_map.items().
  - Set total from 0.
  - Set total\_qty from 0.
  - For each tuple(wh, item\_qty) in warehouse.items().
    - Update total using + 1.
    - If item\_map.get(sbom).
      - Set row from list(sbom, item\_map.get(sbom).item\_name, item\_map.get(sbom).description, item\_map.get(sbom).stock\_uom, …).
      - Set available\_qty from item\_qty.
      - Update total\_qty using + flt(available\_qty).
      - Update row using + list(available\_qty).
      - If available\_qty.
        - Evaluate data.append(row).
        - If total equals len(warehouse).
          - Set row from list(empty text, empty text, “Total”, empty text, …).
          - Evaluate data.append(row).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L2341) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1518)

<a id="op-bdcd233089060d"></a>
### Get columns

`operation_enterprise_selling_report_available_stock_for_packing_items_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(“Item Code:Link/Item:100”, “Item Name::100”, “Description::120”, “UOM:Link/UOM:80”, …).
- Return columns.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L2932) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1519)

<a id="op-bfcca0ec4de0a2"></a>
### Get item details

`operation_enterprise_selling_report_available_stock_for_packing_items_business_behavior_get_item_details`

**Inputs** item\_codes.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · item\_map.

**Local steps**

- If not item\_codes.
  - Return mapping().
- Set item\_map from mapping().
- For each item in Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, item\_codes)), fields = list(“name”, “item\_name”, “description”, “stock\_uom”)).
  - Evaluate item\_map.setdefault(item.name, item).
- Return item\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0661.json#L2999) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1520)

<a id="op-cb28d33f3194f7"></a>
### Get item warehouse quantity map

`operation_enterprise_selling_report_available_stock_for_packing_items_business_behavior_get_item_warehouse_quantity_map`

**Inputs** no declared parameters.

**Explicit results** mapping() · sbom\_map.

**Local steps**

- Set pb from Platform.qb.DocType(“Product Bundle”).
- Set pbi from Platform.qb.DocType(“Product Bundle Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“parent”), pbi.item\_code, nested operand in the contract.as\_(“qty”)).where(pb.disabled equals 0).gro ….
- If condition bound to get\_allowed\_masters\_condition(pb.new\_item\_code, “Item”).
  - Set query from query.where(condition).
- Set bundle\_components from query.run(as\_dict = true).
- If not bundle\_components.
  - Return mapping().
- Set component\_items from list(set of c.item\_code for c drawn from bundle\_components).
  - Draw c from bundle\_components.
- Set bin\_projected from mapping of tuple(b.item\_code, b.warehouse) → flt(b.projected\_qty) for b drawn from get\_component\_bins(component\_items).
  - Draw b from get\_component\_bins(component\_items).
- Set bin\_warehouses from set of wh for tuple(\_, wh) drawn from bin\_projected.
  - Draw tuple(\_, wh) from bin\_projected.
- Set packable\_qty from mapping().
- For each component in bundle\_components.
  - If not component.qty.
    - Continue with the next iteration or loop test.
  - For each warehouse in bin\_warehouses.
    - Set qty from (bin\_projected.get(tuple(component.item\_code, warehouse), 0) ÷ flt(component.qty)).
    - Set key from tuple(component.parent, warehouse).
    - Set packable\_qty at key from min(packable\_qty at key, qty) when key belongs to packable\_qty, otherwise qty.
      - Value choice on key belongs to packable\_qty — true gives min(packable\_qty at key, qty), false gives qty.
- Set sbom\_map from mapping().
- For each tuple(tuple(parent, warehouse), qty) in packable\_qty.items().
  - Set bundles from max(0, floor(flt(qty, 9))).
  - If bundles.
    - Set sbom\_map.setdefault(parent, mapping()) at warehouse from bundles.
- Return sbom\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1521)

<a id="op-f1874111ff2ad2"></a>
### Get component bins

`operation_enterprise_binding_enterprise_selling_report_available_stock_for_packing_items_available_stock_for_packing_items_get_component_bins`

**Inputs** component\_items.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set bin\_table from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract.qb.from\_(bin\_table).select(bin\_table.item\_code, bin\_table.warehouse, bin\_table.projected\_qty).where(bin\_table.item\_code.isin(component\_items)).
- If warehouses bound to get\_user\_permitted\_warehouses().
  - Set query from query.where(bin\_table.warehouse.isin(warehouses)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L95)

<a id="op-e123d1d2ada1f9"></a>
### Get user permitted warehouses

`operation_enterprise_binding_enterprise_selling_report_available_stock_for_packing_items_available_stock_for_packing_items_get_user_permitted_warehouses`

**Inputs** no declared parameters.

**Explicit results** get\_allowed\_docs\_for\_doctype(warehouse\_permissions, “Bin”).

**Local steps**

- Set warehouse\_permissions from (get\_user\_permissions(Platform.session.user).get(“Warehouse”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_user\_permissions(Platform.session.user).get(“Warehouse”) → list().
- Return get\_allowed\_docs\_for\_doctype(warehouse\_permissions, “Bin”).

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L96)

## Record · Customer

[Record definition](../../../../data/record-types/customer.json)

<a id="op-8e18bf23d2dcdd"></a>
### Customer.onload

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).
- Evaluate self.load\_dashboard\_info().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load dashboard info](operations-001.md#op-2cf8f896533b00).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L1453) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1144)

<a id="op-2cf8f896533b00"></a>
### Customer.load dashboard info

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_load_dashboard_info`

**Inputs** self.

**Local steps**

- Set info from get\_dashboard\_info(self.doctype, self.name, self.loyalty\_program).
- Evaluate self.set\_onload(“dashboard\_info”, info).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L1525) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1141)

<a id="op-40c2a009cc889d"></a>
### Customer.before save

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_before_save`

**Inputs** self.

**Local steps**

- If not self.on\_hold.
  - Set self.release\_date from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1427)

<a id="op-f20b4323306a3a"></a>
### Customer.autoname

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_autoname`

**Inputs** self.

**Local steps**

- Set cust\_master\_name from Platform.defaults.get\_global\_default(“cust\_master\_name”).
- If cust\_master\_name equals “Customer Name”.
  - Set self.name from self.get\_customer\_name().
- Otherwise.
  - If cust\_master\_name equals “Naming Series”.
    - Evaluate set\_name\_by\_naming\_series(self).
  - Otherwise.
    - Evaluate set\_name\_from\_naming\_options(Platform.get\_meta(self.doctype).autoname, self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get customer name](operations-001.md#op-3b85254cc82721).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L1633) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1132)

<a id="op-3b85254cc82721"></a>
### Customer.get customer name

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_get_customer_name`

**Inputs** self.

**Record and data access** read “Customer” via get\_value · execute query text (SELECT, Customer).

**Explicit results** new\_customer\_name · self.customer\_name.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Customer Name is mandatory”.

**Local steps**

- Set self.customer\_name from cstr(self.customer\_name).strip().
- If not self.customer\_name.
  - Call the validation error handler Platform.throw(translated “Customer Name is mandatory”, Platform.MandatoryError).
- If (Platform.db.get\_value(“Customer”, self.customer\_name) and not Platform.flags.in\_import).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_value(“Customer”, self.customer\_name) → not Platform.flags.in\_import.
  - Set name\_prefix from formatted text {self.customer\_name} - %.
  - If Platform.db.db\_type equals “postgres”.
    - Set count from Platform.db.sql(query text (SELECT, Customer), mapping(“name\_prefix” → name\_prefix), as\_list = 1) at 0 at 0.
  - Otherwise.
    - Set count from Platform.db.sql(query text (SELECT, Customer), mapping(“name\_prefix” → name\_prefix), as\_list = 1) at 0 at 0.
  - Set count from (cint(count) + 1).
  - Set new\_customer\_name from formatted text {self.customer\_name} - {cstr(count)}.
  - Evaluate msgprint(translated “Changed customer name to '{}' as '{}' already exists.”.format(new\_customer\_name, self.customer\_name), title = translated “Note”, indicator = “yellow”, alert = true).
  - Return new\_customer\_name.
- Return self.customer\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1139)

<a id="op-4728424232336a"></a>
### Customer.after insert

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.update\_lead\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update lead status](operations-002.md#op-602c282df814a7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L2781) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1130)

<a id="op-bb4744a753e6da"></a>
### Customer.validate

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Total contribution percentage should be equal to 100”.

**Local steps**

- Set self.flags.is\_new\_doc from self.is\_new().
- Set self.flags.old\_lead from self.lead\_name.
- Evaluate self.validate\_customer\_group().
- Evaluate self.validate\_lead\_not\_converted().
- Evaluate validate\_party\_accounts(self).
- Evaluate self.validate\_duplicate\_credit\_limit\_company().
- Evaluate self.validate\_credit\_limit\_on\_change().
- Evaluate self.set\_loyalty\_program().
- Evaluate self.check\_customer\_group\_change().
- Evaluate self.validate\_default\_bank\_account().
- Evaluate self.validate\_internal\_customer().
- Evaluate self.validate\_primary\_contact\_and\_address().
- Evaluate self.validate\_prospect\_not\_converted().
- Evaluate self.add\_role\_for\_user().
- Evaluate self.validate\_currency\_for\_receivable\_payable\_and\_advance\_account().
- Evaluate validate\_default\_price\_list\_side(self.default\_price\_list, “selling”).
- If (not self.is\_new() and customer bound to self.get\_doc\_before\_save()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → customer bound to self.get\_doc\_before\_save().
  - If (self.loyalty\_program equals customer.loyalty\_program and not self.loyalty\_program\_tier).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.loyalty\_program equals customer.loyalty\_program → not self.loyalty\_program\_tier.
    - Set self.loyalty\_program\_tier from customer.loyalty\_program\_tier.
- If self.sales\_team.
  - Set total from sum(generator of flt(member.allocated\_percentage) for member drawn from self.sales\_team).
    - Draw member from self.sales\_team.
  - If flt(total, self.precision(“allocated\_percentage”, “sales\_team”)) differs from 100.
    - Call the validation error handler Platform.throw(translated “Total contribution percentage should be equal to 100”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate customer group](operations-002.md#op-62775a1a79e0ca), [validate lead not converted](operations-001.md#op-6aa5432c05fb62), [validate duplicate credit limit company](operations-002.md#op-865bd6d2ed3189), [validate credit limit on change](operations-002.md#op-e735d420c0b315), [set loyalty program](operations-002.md#op-bd2337e89eeb97), [check customer group change](operations-002.md#op-1b8f53c64c61d2), [validate default bank account](operations-002.md#op-64fd096a0bde3d), [validate internal customer](operations-002.md#op-696417dcf1e52d), [validate primary contact and address](operations-002.md#op-28182f20cf7f4c), [validate prospect not converted](operations-002.md#op-3ac6513d6e705f), [add role for user](operations-002.md#op-7611bc8595a9dc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1148)

<a id="op-6aa5432c05fb62"></a>
### Customer.validate lead not converted

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_validate_lead_not_converted`

**Inputs** self.

**Record and data access** read “Customer” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “Lead {0} is already converted to Customer {1}”.format(Platform.bold(self.lead\_name), get\_link\_to\_form(“Customer”, customer)).

**Local steps**

- If not (self.is\_new() and self.lead\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.lead\_name.
  - Return no value.
- If customer bound to Platform.db.exists(“Customer”, mapping(“lead\_name” → self.lead\_name)).
  - Call the validation error handler Platform.throw(translated “Lead {0} is already converted to Customer {1}”.format(Platform.bold(self.lead\_name), get\_link\_to\_form(“Customer”, customer)), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1432)

<a id="op-bbea22b612e77b"></a>
### Customer.get customer group details

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_get_customer_group_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Customer Group” via get\_doc.

**State and service calls** call save on self.

**Local steps**

- Set doc from Platform.get\_doc(“Customer Group”, self.customer\_group).
- Set self.accounts from list().
- Set self.credit\_limits from list().
- Set self.payment\_terms, self.default\_price\_list from empty text.
- Set tables from list(list(“accounts”, list(“account”, “advance\_account”)), list(“credit\_limits”, list(“credit\_limit”, “overdue\_billing\_threshold”, “bypass\_credit\_limit\_check”))).
- Set fields from list(“payment\_terms”, “default\_price\_list”).
- For each row in tables.
  - Set tuple(table, table\_fields) from tuple(row at 0, row at 1).
  - If not doc.get(table).
    - Continue with the next iteration or loop test.
  - For each entry in doc.get(table).
    - Set child from self.append(table).
    - Evaluate child.update(mapping(“company” → entry.company)).
    - Evaluate child.update(mapping of field → entry.get(field) for field drawn from table\_fields).
      - Draw field from table\_fields.
- For each field in fields.
  - If not doc.get(field).
    - Continue with the next iteration or loop test.
  - Evaluate self.update(mapping(field → doc.get(field))).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1138)
