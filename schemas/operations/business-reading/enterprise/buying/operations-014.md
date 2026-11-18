# Purchasing · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Supplier scorecard variable

[Record definition](../../../../data/record-types/supplier_scorecard_variable.json)

<a id="op-f8bee6b47dd438"></a>
### Get total accepted amount

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_accepted_amount`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L161)

<a id="op-f29eadb3ae6614"></a>
### Get total accepted items

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_accepted_items`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L162)

<a id="op-9e78f8621057b9"></a>
### Get total shipments

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_shipments`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L170)

<a id="op-3d23d616755b13"></a>
### Get ordered qty

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_ordered_quantity`

**Inputs** scorecard.

**Explicit results** (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).

**Local steps**

- Set po from Platform.qb.DocType(“Purchase Order”).
- Return (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≤ nested operand … → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0354.json#L4289) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L155)

<a id="op-58f76add70cd08"></a>
### Get invoiced qty

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_invoiced_quantity`

**Inputs** scorecard.

**Explicit results** (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).

**Local steps**

- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Return (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≤ nested operand … → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0354.json#L4611) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L151)

<a id="op-e11a943d4c9296"></a>
### Get rfq total number

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_request_for_quotation_total_number`

**Inputs** scorecard.

**Explicit results** Platform.utils.cint(result at 0 at 0) when result, otherwise 0.

**Local steps**

- Set rfq from Platform.qb.DocType(“Request for Quotation”).
- Set rfq\_item from Platform.qb.DocType(“Request for Quotation Item”).
- Set rfq\_sup from Platform.qb.DocType(“Request for Quotation Supplier”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.supplier equals nested operand in the contract.supplier).where(rfq.transaction\_date at slice scorecard.st ….
- Set result from query.run().
- Return Platform.utils.cint(result at 0 at 0) when result, otherwise 0.
  - Value choice on result — true gives Platform.utils.cint(result at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L158)

<a id="op-8410edf286ad39"></a>
### Get rfq total items

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_request_for_quotation_total_items`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Request for Quotation Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Request for Quotation Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L157)

<a id="op-0866bf5c24048b"></a>
### Get sq total number

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_supplier_quotation_total_number`

**Inputs** scorecard.

**Explicit results** Platform.utils.cint(result at 0 at 0) when result, otherwise 0.

**Local steps**

- Set rfq from Platform.qb.DocType(“Request for Quotation”).
- Set rfq\_item from Platform.qb.DocType(“Request for Quotation Item”).
- Set rfq\_sup from Platform.qb.DocType(“Request for Quotation Supplier”).
- Set sq from Platform.qb.DocType(“Supplier Quotation”).
- Set sq\_item from Platform.qb.DocType(“Supplier Quotation Item”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.transaction\_date at slice nested operand in the contract to nested operand in the contract).where(rfq\_ite ….
- Set result from query.run().
- Return Platform.utils.cint(result at 0 at 0) when result, otherwise 0.
  - Value choice on result — true gives Platform.utils.cint(result at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L160)

<a id="op-593fad5a88e917"></a>
### Get sq total items

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_supplier_quotation_total_items`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Request for Quotation Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Request for Quotation Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L159)

<a id="op-6c0626120e0f81"></a>
### Get rfq response days

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_request_for_quotation_response_days`

**Inputs** scorecard.

**Explicit results** sum(generator of Platform.utils.cint(days) for tuple(\_rfq, \_sq, days) drawn from responses).

**Local steps**

- Set rfq from Platform.qb.DocType(“Request for Quotation”).
- Set rfq\_item from Platform.qb.DocType(“Request for Quotation Item”).
- Set rfq\_sup from Platform.qb.DocType(“Request for Quotation Supplier”).
- Set sq from Platform.qb.DocType(“Supplier Quotation”).
- Set sq\_item from Platform.qb.DocType(“Supplier Quotation Item”).
- Set responses from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(sq\_item.docstatus equals 1).run().
- Return sum(generator of Platform.utils.cint(days) for tuple(\_rfq, \_sq, days) drawn from responses).
  - Draw tuple(\_rfq, \_sq, days) from responses.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L156)

## Service · Utils

<a id="op-b99cdea184dde0"></a>
### Update last purchase rate

`operation_enterprise_buying_utils_business_behavior_update_last_purchase_rate`

**Inputs** doc, is\_submit.

**Declared result** no value.

**Record and data access** read “Buying Settings” via get\_single\_value.

**State and service calls** request set\_value on “Item”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “UOM Conversion factor is required in row {0}”.format(d.idx).

**Local steps**

- If (doc.get(“is\_internal\_supplier”) or Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“is\_internal\_supplier”) → Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”).
  - Return no value.
- Set this\_purchase\_date from getdate((doc.get(“posting\_date”) or doc.get(“transaction\_date”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“posting\_date”) → doc.get(“transaction\_date”).
- For each d in doc.get(“items”).
  - If d.get(“is\_free\_item”).
    - Continue with the next iteration or loop test.
  - Set last\_purchase\_details from get\_last\_purchase\_details(d.item\_code, doc.name).
  - Set last\_purchase\_rate from no value.
  - If (last\_purchase\_details and (doc.get(“docstatus”) equals 2 or last\_purchase\_details.purchase\_date &gt; this\_purchase\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_purchase\_details → (doc.get(“docstatus”) equals 2 or last\_purchase\_details.purchase\_date &gt; this\_purchase\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“docstatus”) equals 2 → last\_purchase\_details.purchase\_date &gt; this\_purchase\_date.
    - Set last\_purchase\_rate from last\_purchase\_details at “base\_net\_rate”.
  - Otherwise.
    - If is\_submit equals 1.
      - If flt(d.conversion\_factor).
        - Set last\_purchase\_rate from (flt(d.base\_net\_rate) ÷ flt(d.conversion\_factor)).
      - Otherwise.
        - If d.item\_code.
          - Call the validation error handler Platform.throw(translated “UOM Conversion factor is required in row {0}”.format(d.idx)).
  - Evaluate Platform.db.set\_value(“Item”, d.item\_code, “last\_purchase\_rate”, flt(last\_purchase\_rate), update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L289)

<a id="op-06e2d03d15002a"></a>
### Validate for items

`operation_enterprise_buying_utils_business_behavior_validate_for_items`

**Inputs** doc.

**Declared result** no value.

**Local steps**

- For each d in doc.get(“items”).
  - Evaluate set\_stock\_levels(row = d).
  - Set item from validate\_item\_and\_get\_basic\_data(row = d).
  - Evaluate validate\_stock\_item\_warehouse(row = d, item = item).
  - Evaluate validate\_end\_of\_life(d.item\_code, item.end\_of\_life, item.disabled).
- Evaluate validate\_duplicate\_items(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L290)

<a id="op-417af5649d3c16"></a>
### Validate duplicate items

`operation_enterprise_binding_enterprise_buying_utils_validate_duplicate_items`

**Inputs** doc.

**Declared result** no value.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Same item cannot be entered multiple times.”.

**Local steps**

- Set rows from list of tuple(row.item\_code, row.get(“purchase\_receipt”), row.get(“purchase\_order”), row.get(“material\_request”), …) for row drawn from doc.get(“items”) where row.item\_code.
  - Draw row from doc.get(“items”), keep a combination only if (row.item\_code).
- If (len(rows) differs from len(set(rows)) and not cint(Platform.db.get\_single\_value(“Buying Settings”, “allow\_multiple\_items”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(rows) differs from len(set(rows)) → not cint(Platform.db.get\_single\_value(“Buying Settings”, “allow\_multiple\_items”)).
  - Call the validation error handler Platform.throw(translated “Same item cannot be entered multiple times.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “allow\_multiple\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L236) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L138)

<a id="op-224af251c189e9"></a>
### Set stock levels

`operation_enterprise_buying_utils_business_behavior_set_stock_levels`

**Inputs** row.

**Declared result** no value.

**Record and data access** read “Bin” via get\_value.

**Local steps**

- Set projected\_qty from Platform.db.get\_value(“Bin”, mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse), “projected\_qty”).
- Set qty\_data from mapping(“projected\_qty” → flt(projected\_qty), “ordered\_qty” → 0, “received\_qty” → 0).
- If row.doctype belongs to tuple(“Purchase Receipt Item”, “Purchase Invoice Item”).
  - Evaluate qty\_data.pop(“received\_qty”).
- For each field in qty\_data.
  - If row.meta.get\_field(field).
    - Evaluate row.set(field, qty\_data at field).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0364.json#L4444) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L288)

<a id="op-c8832471966330"></a>
### Validate item and get basic data

`operation_enterprise_buying_utils_business_behavior_validate_item_and_get_basic_data`

**Inputs** row.

**Declared result** dict.

**Record and data access** read “Item” via get\_values.

**Explicit results** item at 0.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} does not exist”.format(row.idx, Platform.bold(row.item\_code)).

**Local steps**

- Set item from Platform.db.get\_values(“Item”, filters = mapping(“name” → row.item\_code), fieldname = list(“is\_stock\_item”, “is\_sub\_contracted\_item”, “end\_of\_life”, “disabled”), as\_dict = 1).
- If not item.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} does not exist”.format(row.idx, Platform.bold(row.item\_code))).
- Return item at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0364.json#L4793) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L291)

<a id="op-f4f4765e5255df"></a>
### Validate stock item warehouse

`operation_enterprise_buying_utils_business_behavior_validate_stock_item_warehouse`

**Inputs** row, item.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Row #{1}: Warehouse is mandatory for stock Item {0}”.format(Platform.bold(row.item\_code), row.idx).

**Local steps**

- If (item.is\_stock\_item equals 1 and row.qty and not row.warehouse and not row.get(“delivered\_by\_supplier”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_stock\_item equals 1 → row.qty → not row.warehouse → not row.get(“delivered\_by\_supplier”).
  - Call the validation error handler Platform.throw(translated “Row #{1}: Warehouse is mandatory for stock Item {0}”.format(Platform.bold(row.item\_code), row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0364.json#L5066) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L292)

<a id="op-13b2157a8baeb9"></a>
### Check on hold or closed status

`operation_enterprise_buying_utils_business_behavior_check_on_hold_or_closed_status`

**Inputs** doctype, docname.

**Declared result** no value.

**Record and data access** read doctype via get\_value.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “{0} {1} status is {2}.”.format(Platform.bold(translated doctype), Platform.bold(docname), Platform.bold(translated status)).

**Local steps**

- Set status from Platform.db.get\_value(doctype, docname, “status”).
- If status belongs to tuple(“Closed”, “On Hold”).
  - Call the validation error handler Platform.throw(translated “{0} {1} status is {2}.”.format(Platform.bold(translated doctype), Platform.bold(docname), Platform.bold(translated status)), Platform.InvalidStatusError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0364.json#L5279) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L286)

<a id="op-65c653bdc97ffe"></a>
### Get linked material requests

`operation_enterprise_buying_utils_business_behavior_get_linked_material_remote_requests`

**Inputs** items.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Material Request” via get\_list · execute query text (SELECT, Material Request).

**Explicit results** list() · mr\_list.

**Explicit failure paths** validation helper — translated “Items must be a list of Item codes”.

**Local steps**

- Attempt the following.
  - Set items from Platform.parse\_json(items).
- On failure (tuple(TypeError, ValueError)).
  - Call the validation error handler Platform.throw(translated “Items must be a list of Item codes”).
- If isinstance(items, str).
  - Set items from list(items).
- If (not isinstance(items, (list bitwise or tuple)) or any(generator of not isinstance(item, str) for item drawn from items)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(items, (list bitwise or tuple)) → any(generator of not isinstance(item, str) for item drawn from items).
  - Draw item from items.
  - Call the validation error handler Platform.throw(translated “Items must be a list of Item codes”).
- Set permitted\_material\_requests from Platform.get\_list(“Material Request”, filters = list(list(“material\_request\_type”, “=”, “Purchase”), list(“docstatus”, “=”, 1), list(“status”, “!=”, “Stopped”), list(“per\_ordered”, “&lt;”, 99.99), …), pluck = ….
- If not permitted\_material\_requests.
  - Return list().
- Set mr\_list from list().
- For each item in items.
  - Set material\_request from Platform.db.sql(query text (SELECT, Material Request), mapping(“item” → item, “permitted” → permitted\_material\_requests), as\_dict = 1).
  - If material\_request.
    - Evaluate mr\_list.extend(material\_request).
- Return mr\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L287)

<a id="op-0ffc9f33382cad"></a>
### Get qty to order

`operation_enterprise_binding_enterprise_buying_utils_get_qty_to_order`

**Inputs** rows, link\_field.

**Declared result** dict.

**Explicit results** mapping of row.name → flt((row.qty − (flt(nested operand in the contract.get(nested operand in the contract.name)) ÷ row.conversion\_factor)), row.precision(“qty”)) for row drawn from rows.

**Local steps**

- Set po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set ordered\_stock\_qty from dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(po\_item at link\_field).run()).
  - Draw row from rows.
- Return mapping of row.name → flt((row.qty − (flt(nested operand in the contract.get(nested operand in the contract.name)) ÷ row.conversion\_factor)), row.precision(“qty”)) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L235) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L137)
