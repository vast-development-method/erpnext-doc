# Subcontracting · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting inward order

[Record definition](../../../../data/record-types/subcontracting_inward_order.json)

<a id="op-93f6025ddd3188"></a>
### Get data

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_subcontracting_inward_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “subcontracting\_inward\_order”, “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Stock Entry”)), mapping(“label” → translated “Manufacturing”, “items” ….

**Local steps**

- Return mapping(“fieldname” → “subcontracting\_inward\_order”, “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Stock Entry”)), mapping(“label” → translated “Manufacturing”, “items” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0951.json#L367) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L954)

## Record · Subcontracting inward order item

[Record definition](../../../../data/record-types/subcontracting_inward_order_item.json)

<a id="op-a2f44c0df9a448"></a>
### Subcontracting Inward Order Item.update manufacturing qty fields

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_item_business_behavior_subcontracting_inward_order_item_update_manufacturing_quantity_fields`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set table from Platform.qb.DocType(“Work Order”).
- Set query from nested operand in the contract.qb.from\_(table).select(Sum(nested operand in the contract.produced\_qty).as\_(“produced\_qty”), Sum(nested operand in the contract.process\_loss\_qty).as\_(“process\_loss\_qty”)).whe ….
- Set result from query.run(as\_dict = true) at 0.
- Evaluate self.db\_set(“produced\_qty”, result.produced\_qty).
- Evaluate self.db\_set(“process\_loss\_qty”, result.process\_loss\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0952.json#L6671) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L953)

## Report · Subcontracting inward order summary

<a id="op-f6755d9c25b52e"></a>
### Execute

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracting_inward_order_summary_subcontracting_inward_order_summary_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1242)

<a id="op-8dc05671c2586e"></a>
### Get data

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracting_inward_order_summary_subcontracting_inward_order_summary_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set finished\_goods from get\_finished\_goods(filters).
- Set raw\_materials from get\_raw\_materials(set of row.subcontracting\_inward\_order for row drawn from finished\_goods).
  - Draw row from finished\_goods.
- Set data from list().
- For each finished\_good in finished\_goods.
  - Evaluate data.extend(get\_finished\_good\_rows(finished\_good, raw\_materials.get(finished\_good.order\_item, list()))).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1244)

<a id="op-41d75102710f31"></a>
### Get finished goods

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracting_inward_order_summary_subcontracting_inward_order_summary_get_finished_goods`

**Inputs** filters.

**Record and data access** read “Subcontracting Inward Order” via get\_list.

**Explicit results** Platform.get\_list(“Subcontracting Inward Order”, fields = list(“name as subcontracting\_inward\_order”, “transaction\_date”, “customer”, “status”, …), filters = order\_filters, order\_by = “transaction\_date, na ….

**Local steps**

- Set order\_filters from get\_inward\_order\_filters(filters).
- If filters.get(“subcontracting\_inward\_order”).
  - Evaluate order\_filters.append(list(“name”, “=”, filters.subcontracting\_inward\_order)).
- Return Platform.get\_list(“Subcontracting Inward Order”, fields = list(“name as subcontracting\_inward\_order”, “transaction\_date”, “customer”, “status”, …), filters = order\_filters, order\_by = “transaction\_date, na ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1246)

<a id="op-ac12b4b8f8b5f1"></a>
### Get raw materials

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracting_inward_order_summary_subcontracting_inward_order_summary_get_raw_materials`

**Inputs** orders.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_all.

**Explicit results** mapping() · raw\_materials.

**Local steps**

- If not orders.
  - Return mapping().
- Set raw\_materials from mapping().
- For each row in Platform.get\_all(“Subcontracting Inward Order Received Item”, fields = list(“reference\_name”, “rm\_item\_code”, “stock\_uom as rm\_stock\_uom”, “required\_qty”, …), filters = mapping(“parent” → list(“in”, list(o ….
  - Evaluate raw\_materials.setdefault(row.reference\_name, list()).append(row).
- Return raw\_materials.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1247)

<a id="op-a9e86d78548213"></a>
### Get finished good rows

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracting_inward_order_summary_subcontracting_inward_order_summary_get_finished_good_rows`

**Inputs** finished\_good, raw\_materials.

**Explicit results** rows.

**Local steps**

- Set rows from list().
- For each tuple(index, raw\_material) in enumerate((raw\_materials or list(mapping()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in raw\_materials → list(mapping()).
  - Set finished\_good\_columns from finished\_good when index equals 0, otherwise dict.fromkeys(finished\_good).
    - Value choice on index equals 0 — true gives finished\_good, false gives dict.fromkeys(finished\_good).
  - Evaluate rows.append(mapping(expand finished\_good\_columns, expand raw\_material)).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1245)

<a id="op-dbdd4655f6e1e4"></a>
### Get columns

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracting_inward_order_summary_subcontracting_inward_order_summary_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(expanded get\_inward\_order\_columns(), mapping(“label” → translated “Status”, “fieldname” → “status”, “fieldtype” → “Data”, “width” → 100), mapping(“label” → translated “Finished Good”, “fieldname” → “i ….

**Local steps**

- Return list(expanded get\_inward\_order\_columns(), mapping(“label” → translated “Status”, “fieldname” → “status”, “fieldtype” → “Data”, “width” → 100), mapping(“label” → translated “Finished Good”, “fieldname” → “i ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1243)

## Record · Subcontracting order

[Record definition](../../../../data/record-types/subcontracting_order.json)

<a id="op-770345e95bc84a"></a>
### Subcontracting Order.onload

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_onload`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Stock Settings” via get\_single\_value.

**Local steps**

- Evaluate self.set\_onload(“over\_transfer\_allowance”, Platform.db.get\_single\_value(“Buying Settings”, “over\_transfer\_allowance”)).
- Evaluate self.set\_onload(“over\_delivery\_receipt\_allowance”, Platform.get\_single\_value(“Stock Settings”, “over\_delivery\_receipt\_allowance”)).
- Evaluate self.set\_onload(“backflush\_based\_on”, Platform.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”)).
- If self.reserve\_stock.
  - If self.has\_unreserved\_stock().
    - Evaluate self.set\_onload(“has\_unreserved\_stock”, true).
  - If has\_reserved\_stock(self.doctype, self.name).
    - Evaluate self.set\_onload(“has\_reserved\_stock”, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has unreserved stock](operations-004.md#op-fa00f4a1605fa4).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “over\_transfer\_allowance”), Platform.get\_single\_value(“Stock Settings”, “over\_delivery\_receipt\_allowance”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0952.json#L7039) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L989)

<a id="op-e6f73244ddf184"></a>
### Subcontracting Order.before validate

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_before_validate`

**Inputs** self.

**Local steps**

- Evaluate super().before\_validate().
- Evaluate self.set\_subcontracting\_conversion\_factor().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set subcontracting conversion factor](operations-003.md#op-48708f9a9065ce).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L981)

<a id="op-8d4300e7dcf23c"></a>
### Subcontracting Order.validate

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “qty”, “Subcontracting Order Item”).
- Evaluate self.validate\_item\_stock\_uom\_is\_integer(“item\_code”, “qty”, “Subcontracting Order Item”).
- Evaluate self.validate\_purchase\_order\_for\_subcontracting().
- Evaluate self.validate\_items().
- Evaluate self.validate\_service\_items().
- Evaluate self.validate\_header\_with\_purchase\_order().
- Evaluate self.validate\_rows\_with\_purchase\_order().
- Evaluate self.validate\_supplied\_items().
- Evaluate self.set\_missing\_values().
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate clear\_reserve\_stock\_if\_disabled(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate purchase order for subcontracting](operations-003.md#op-5793e3f03f588a), [validate service items](operations-003.md#op-d356a222d6ea21), [validate header with purchase order](operations-003.md#op-bff11e73efb9ae), [validate rows with purchase order](operations-003.md#op-5642db9b6e31b0), [validate supplied items](operations-003.md#op-898f2a66f3e425), [set missing values](operations-003.md#op-5938df9ae3f4ae), [validate with previous doc](operations-003.md#op-edef732b6a47f0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L997)

<a id="op-725f6a978f7014"></a>
### Subcontracting Order.on submit

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.update\_subcontracted\_quantity\_in\_po().
- Evaluate self.make\_raw\_material\_reservations().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-004.md#op-80d00c8ebd7843), [update subcontracted quantity in po](operations-004.md#op-7d9fc48e248f3a), [make raw material reservations](operations-004.md#op-c93f24abf6101f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L988)

<a id="op-882ae163d972df"></a>
### Subcontracting Order.on cancel

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.update\_subcontracted\_quantity\_in\_po().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-004.md#op-80d00c8ebd7843), [update subcontracted quantity in po](operations-004.md#op-7d9fc48e248f3a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L987)

<a id="op-edef732b6a47f0"></a>
### Subcontracting Order.validate with previous doc

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_validate_with_previous_doc`

**Inputs** self.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Purchase Order Item” → mapping(“ref\_dn\_field” → “purchase\_order\_item”, “compare\_fields” → list(list(“project”, “=”)), “is\_child\_table” → true))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1194)

<a id="op-f084a5dff800a3"></a>
### Subcontracting Order.get purchase order items

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_get_purchase_order_items`

**Inputs** self.

**Record and data access** read “Purchase Order Item” via get\_all.

**Explicit results** mapping of d.name → d for d drawn from Platform.get\_all(“Purchase Order Item”, filters = mapping(“parent” → self.purchase\_order), fields = list(“name”, “item\_code”, “rate”, “qty”, …)).

**Local steps**

- Return mapping of d.name → d for d drawn from Platform.get\_all(“Purchase Order Item”, filters = mapping(“parent” → self.purchase\_order), fields = list(“name”, “item\_code”, “rate”, “qty”, …)).
  - Draw d from Platform.get\_all(“Purchase Order Item”, filters = mapping(“parent” → self.purchase\_order), fields = list(“name”, “item\_code”, “rate”, “qty”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1185)

<a id="op-48708f9a9065ce"></a>
### Subcontracting Order.set subcontracting conversion factor

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_set_subcontracting_conversion_factor`

**Inputs** self.

**Local steps**

- Set conversion\_factors from mapping of d.name → (flt(d.qty) ÷ flt(d.fg\_item\_qty)) for d drawn from self.get\_purchase\_order\_items().values() where flt(d.fg\_item\_qty).
  - Draw d from self.get\_purchase\_order\_items().values(), keep a combination only if (flt(d.fg\_item\_qty)).
- For each item in self.items.
  - If item.purchase\_order\_item belongs to conversion\_factors.
    - Set item.subcontracting\_conversion\_factor from conversion\_factors at item.purchase\_order\_item.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get purchase order items](operations-003.md#op-f084a5dff800a3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1190)

<a id="op-5793e3f03f588a"></a>
### Subcontracting Order.validate purchase order for subcontracting

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_validate_purchase_order_for_subcontracting`

**Inputs** self.

**Record and data access** resolve a document from “Purchase Order” via get\_doc.

**Explicit failure paths** validation helper — translated “Please select a valid Purchase Order that is configured for Subcontracting.” · validation helper — translated “Please select a valid Purchase Order that has Service Items.” · validation helper — translated msg · validation helper — translated “Cannot create a Subcontracting Order against Purchase Order {0} because it is {1}.”.format(po.name, translated po.status) · validation helper — translated “Please select a Subcontracting Purchase Order.”.

**Local steps**

- If self.purchase\_order.
  - Set po from Platform.get\_doc(“Purchase Order”, self.purchase\_order).
  - If not po.is\_subcontracted.
    - Call the validation error handler Platform.throw(translated “Please select a valid Purchase Order that is configured for Subcontracting.”).
  - If po.is\_old\_subcontracting\_flow.
    - Call the validation error handler Platform.throw(translated “Please select a valid Purchase Order that has Service Items.”).
  - If po.docstatus differs from 1.
    - Set msg from formatted text Please submit Purchase Order {po.name} before proceeding..
    - Call the validation error handler Platform.throw(translated msg).
  - If po.status belongs to tuple(“Closed”, “On Hold”).
    - Call the validation error handler Platform.throw(translated “Cannot create a Subcontracting Order against Purchase Order {0} because it is {1}.”.format(po.name, translated po.status)).
  - If po.per\_received equals 100.
    - Set msg from formatted text Cannot create more Subcontracting Orders against the Purchase Order {po.name}..
    - Call the validation error handler Platform.throw(translated msg).
- Otherwise.
  - Set self.service\_items, self.items, self.supplied\_items from no value.
  - Call the validation error handler Platform.throw(translated “Please select a Subcontracting Purchase Order.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L998)

<a id="op-d356a222d6ea21"></a>
### Subcontracting Order.validate service items

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_validate_service_items`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Service Item {0} must be a non-stock item.”.format(service\_item.item\_code).

**Local steps**

- Set purchase\_order\_items from list of item.purchase\_order\_item for item drawn from self.items.
  - Draw item from self.items.
- Set self.service\_items from list of service\_item for service\_item drawn from self.service\_items where service\_item.purchase\_order\_item belongs to purchase\_order\_items.
  - Draw service\_item from self.service\_items, keep a combination only if (service\_item.purchase\_order\_item belongs to purchase\_order\_items).
- For each service\_item in self.service\_items.
  - If Platform.get\_value(“Item”, service\_item.item\_code, “is\_stock\_item”).
    - Call the validation error handler Platform.throw(translated “Service Item {0} must be a non-stock item.”.format(service\_item.item\_code)).
  - Set item from next(generator of item for item drawn from self.items where item.purchase\_order\_item equals service\_item.purchase\_order\_item).
    - Draw item from self.items, keep a combination only if (item.purchase\_order\_item equals service\_item.purchase\_order\_item).
  - Set service\_item.qty from (item.qty × item.subcontracting\_conversion\_factor).
  - Set service\_item.fg\_item\_qty from item.qty.
  - Set service\_item.amount from (service\_item.qty × service\_item.rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0953.json#L565) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L999)

<a id="op-bff11e73efb9ae"></a>
### Subcontracting Order.validate header with purchase order

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_validate_header_with_purchase_order`

**Inputs** self.

**Record and data access** read “Purchase Order” via get\_value.

**Explicit failure paths** validation helper — translated “{0} must be the same as in Purchase Order {1}.”.format(translated self.meta.get\_label(fieldname), self.purchase\_order).

**Local steps**

- Set po from Platform.db.get\_value(“Purchase Order”, self.purchase\_order, list(“supplier”, “company”), as\_dict = true).
- For each fieldname in tuple(“supplier”, “company”).
  - If self.get(fieldname) differs from po.get(fieldname).
    - Call the validation error handler Platform.throw(translated “{0} must be the same as in Purchase Order {1}.”.format(translated self.meta.get\_label(fieldname), self.purchase\_order)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1192)

<a id="op-5642db9b6e31b0"></a>
### Subcontracting Order.validate rows with purchase order

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_validate_rows_with_purchase_order`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Item {1} is not the Finished Good of Purchase Order {2}.”.format(item.idx, item.item\_code, self.purchase\_order) · validation helper — translated “Row {0}: Service Item {1} and its rate must match Purchase Order {2}.”.format(service\_item.idx, service\_item.item\_code, self.purchase\_order).

**Local steps**

- Set po\_items from self.get\_purchase\_order\_items().
- For each item in self.items.
  - Set po\_item from po\_items.get(item.purchase\_order\_item).
  - If (not po\_item or item.item\_code differs from po\_item.fg\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not po\_item → item.item\_code differs from po\_item.fg\_item.
    - Call the validation error handler Platform.throw(translated “Row {0}: Item {1} is not the Finished Good of Purchase Order {2}.”.format(item.idx, item.item\_code, self.purchase\_order)).
- For each service\_item in self.service\_items.
  - Set po\_item from po\_items.get(service\_item.purchase\_order\_item).
  - Set precision from service\_item.precision(“rate”).
  - If (not po\_item or service\_item.item\_code differs from po\_item.item\_code or flt(service\_item.rate, precision) differs from flt(po\_item.rate, precision)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not po\_item → service\_item.item\_code differs from po\_item.item\_code → flt(service\_item.rate, precision) differs from flt(po\_item.rate, precision).
    - Call the validation error handler Platform.throw(translated “Row {0}: Service Item {1} and its rate must match Purchase Order {2}.”.format(service\_item.idx, service\_item.item\_code, self.purchase\_order)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get purchase order items](operations-003.md#op-f084a5dff800a3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1193)

<a id="op-898f2a66f3e425"></a>
### Subcontracting Order.validate supplied items

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_validate_supplied_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- If self.supplier\_warehouse.
  - For each item in self.supplied\_items.
    - If self.supplier\_warehouse equals item.reserve\_warehouse.
      - Set msg from formatted text Reserve Warehouse must be different from Supplier Warehouse for Supplied Item {item.main\_item\_code}..
      - Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1000)

<a id="op-5938df9ae3f4ae"></a>
### Subcontracting Order.set missing values

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_set_missing_values`

**Inputs** self.

**Local steps**

- Evaluate self.calculate\_additional\_costs().
- Evaluate self.calculate\_service\_costs().
- Evaluate self.calculate\_supplied\_items\_qty\_and\_amount().
- Evaluate self.calculate\_items\_qty\_and\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate service costs](operations-003.md#op-fbac1bb2bcc644), [calculate supplied items qty and amount](operations-004.md#op-54e3ec1464b022), [calculate items qty and amount](operations-004.md#op-8a96182a967d4c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0953.json#L1163) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L992)

<a id="op-3569ccf340e38a"></a>
### Subcontracting Order.set service item base amounts

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_set_service_item_base_amounts`

**Inputs** self.

**Local steps**

- Set conversion\_rate from (flt(self.conversion\_rate) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.conversion\_rate) → 1.0.
- For each item in self.get(“service\_items”).
  - Set item.base\_rate from flt((item.rate × conversion\_rate), item.precision(“base\_rate”)).
  - Set item.base\_amount from flt((item.amount × conversion\_rate), item.precision(“base\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1189)

<a id="op-fbac1bb2bcc644"></a>
### Subcontracting Order.calculate service costs

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_calculate_service_costs`

**Inputs** self.

**Local steps**

- Evaluate self.set\_service\_item\_base\_amounts().
- Set service\_amount\_by\_po\_item from mapping of service\_item.purchase\_order\_item → service\_item.base\_amount for service\_item drawn from self.get(“service\_items”).
  - Draw service\_item from self.get(“service\_items”).
- For each item in self.items.
  - Set service\_amount from flt(service\_amount\_by\_po\_item.get(item.purchase\_order\_item)).
  - Set item.service\_cost\_per\_qty from (service\_amount ÷ item.qty) when item.qty, otherwise 0.
    - Value choice on item.qty — true gives (service\_amount ÷ item.qty), false gives 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set service item base amounts](operations-003.md#op-3569ccf340e38a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L983)
