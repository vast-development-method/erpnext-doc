# Production · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Production plan

[Record definition](../../../../data/record-types/production_plan.json)

<a id="op-e7c3f31fe94e36"></a>
### Get remaining reserved qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_remaining_reserved_qty`

**Inputs** plan\_qty\_by\_warehouse, work\_order\_qty\_by\_warehouse, warehouse.

**Explicit results** 0.0 · (remaining\_qty − ((remaining\_qty × unmatched\_qty) ÷ total\_remaining\_qty)).

**Local steps**

- Set remaining\_qty\_by\_warehouse from mapping of plan\_warehouse → max((qty − work\_order\_qty\_by\_warehouse.get(plan\_warehouse, 0.0)), 0.0) for tuple(plan\_warehouse, qty) drawn from plan\_qty\_by\_warehouse.items().
  - Draw tuple(plan\_warehouse, qty) from plan\_qty\_by\_warehouse.items().
- Set total\_remaining\_qty from sum(remaining\_qty\_by\_warehouse.values()).
- If not total\_remaining\_qty.
  - Return 0.0.
- Set matched\_qty from (sum(plan\_qty\_by\_warehouse.values()) − total\_remaining\_qty).
- Set unmatched\_qty from min((sum(work\_order\_qty\_by\_warehouse.values()) − matched\_qty), total\_remaining\_qty).
- Set remaining\_qty from remaining\_qty\_by\_warehouse.get(warehouse, 0.0).
- Return (remaining\_qty − ((remaining\_qty × unmatched\_qty) ÷ total\_remaining\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L926)

<a id="op-7798f85c139a8f"></a>
### Get plan reservations

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_plan_reservations`

**Inputs** item\_code.

**Explicit results** \_group\_by\_plan\_and\_warehouse(\_get\_material\_request\_plan\_query(item\_code), \_get\_sub\_assembly\_plan\_query(item\_code)).

**Local steps**

- Return \_group\_by\_plan\_and\_warehouse(\_get\_material\_request\_plan\_query(item\_code), \_get\_sub\_assembly\_plan\_query(item\_code)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L916)

<a id="op-1d481d1181274b"></a>
### Get material request plan query

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_material_request_plan_query`

**Inputs** item\_code.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“production\_plan”), child.warehouse, nested operand in the contract.as\_(“reserved\_qty”)).where((\_is\_ ….

**Local steps**

- Set table from Platform.qb.DocType(“Production Plan”).
- Set child from Platform.qb.DocType(“Material Request Plan Item”).
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“production\_plan”), child.warehouse, nested operand in the contract.as\_(“reserved\_qty”)).where((\_is\_ ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L910)

<a id="op-eb581b6846e508"></a>
### Get sub assembly plan query

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_sub_assembly_plan_query`

**Inputs** item\_code.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“production\_plan”), nested operand in the contract.as\_(“warehouse”), nested operand in the contract. ….

**Local steps**

- Set table from Platform.qb.DocType(“Production Plan”).
- Set child from Platform.qb.DocType(“Production Plan Sub Assembly Item”).
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“production\_plan”), nested operand in the contract.as\_(“warehouse”), nested operand in the contract. ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L933)

<a id="op-f02dd2a99604ee"></a>
### Is open plan

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_is_open_plan`

**Inputs** table.

**Explicit results** (table.docstatus equals 1 bitwise and table.status.notin(list(“Completed”, “Closed”))).

**Local steps**

- Return (table.docstatus equals 1 bitwise and table.status.notin(list(“Completed”, “Closed”))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L940)

<a id="op-a93314a7556d3c"></a>
### Get work order reservations

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_work_order_reservations`

**Inputs** item\_code, plan\_names.

**Explicit results** \_group\_by\_plan\_and\_warehouse(query).

**Local steps**

- Set work\_order from Platform.qb.DocType(“Work Order”).
- Set work\_order\_item from Platform.qb.DocType(“Work Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(work\_order.production\_plan, nested operand in the contract.as\_(“warehouse”), nested operand in the contract.as\_(“reserved\_qty”)).where( ….
- Return \_group\_by\_plan\_and\_warehouse(query).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L938)

<a id="op-0945eedf78e451"></a>
### Group by plan and warehouse

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_group_by_plan_and_warehouse`

**Inputs** remaining positional values queries.

**Explicit results** reservations.

**Local steps**

- Set reservations from defaultdict(deferred anonymous expression).
- For each query in queries.
  - For each row in query.run(as\_dict = true).
    - Update reservations at row.production\_plan at row.warehouse using + flt(row.reserved\_qty).
- Return reservations.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L939)

<a id="op-3c9454b15a5e12"></a>
### Get non completed production plans

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_non_completed_production_plans`

**Inputs** no declared parameters.

**Explicit results** nested operand in the contract(nested operand in the contract).distinct().where((table.docstatus equals 1 bitwise and nested operand in the contract.status.notin(list(“Completed”, “Closed”)))).run(pluck = “name”).

**Local steps**

- Set table from Platform.qb.DocType(“Production Plan”).
- Return nested operand in the contract(nested operand in the contract).distinct().where((table.docstatus equals 1 bitwise and nested operand in the contract.status.notin(list(“Completed”, “Closed”)))).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L914)

<a id="op-0466876b37bd22"></a>
### Get raw materials of sub assembly items

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_raw_materials_of_sub_assembly_items`

**Inputs** existing\_sub\_assembly\_items, item\_details, company, bom\_no, include\_non\_stock\_items, sub\_assembly\_items, planned\_qty = 1.

**Explicit results** item\_details.

**Local steps**

- Set bei from Platform.qb.DocType(“BOM Item”).
- Set bom from Platform.qb.DocType(“BOM”).
- Set item from Platform.qb.DocType(“Item”).
- Set item\_default from Platform.qb.DocType(“Item Default”).
- Set item\_uom from Platform.qb.DocType(“UOM Conversion Detail”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“qty”), item.item\_name, nested operand in the contract.as\_(“item\_code”), bei.description, …).where(( ….
  - Value choice on include\_non\_stock\_items — true gives item.is\_stock\_item.isin(list(0, 1)), false gives item.is\_stock\_item equals 1.
- For each item in query.run(as\_dict = true).
  - Set key from tuple(item.item\_code, item.bom\_no).
  - Set existing\_key from tuple(item.item\_code, (item.bom\_no or item.main\_bom)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.bom\_no → item.main\_bom.
  - If (item.bom\_no and not item.is\_phantom\_item and key does not belong to sub\_assembly\_items).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.bom\_no → not item.is\_phantom\_item → key does not belong to sub\_assembly\_items.
    - Continue with the next iteration or loop test.
  - If (not item.is\_phantom\_item and existing\_key belongs to existing\_sub\_assembly\_items).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.is\_phantom\_item → existing\_key belongs to existing\_sub\_assembly\_items.
    - Continue with the next iteration or loop test.
  - If item.bom\_no.
    - Set recursion\_qty from flt(item.get(“qty”)) when item.is\_phantom\_item, otherwise flt(sub\_assembly\_items at key).
      - Value choice on item.is\_phantom\_item — true gives flt(item.get(“qty”)), false gives flt(sub\_assembly\_items at key).
    - Evaluate get\_raw\_materials\_of\_sub\_assembly\_items(existing\_sub\_assembly\_items, item\_details, company, item.bom\_no, planned\_qty = recursion\_qty, …).
    - If not item.is\_phantom\_item.
      - Evaluate existing\_sub\_assembly\_items.add(existing\_key).
  - Otherwise.
    - If (not item.conversion\_factor and item.purchase\_uom).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.conversion\_factor → item.purchase\_uom.
      - Set item.conversion\_factor from get\_uom\_conversion\_factor(item.item\_code, item.purchase\_uom).
    - If details bound to item\_details.get(tuple(item.get(“item\_code”), item.get(“main\_bom”))).
      - Update details.qty using + item.get(“qty”).
    - Otherwise.
      - Evaluate item\_details.setdefault(tuple(item.get(“item\_code”), item.get(“main\_bom”)), item).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L925)

<a id="op-b55d5d2007c500"></a>
### Sales order query

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_sales_order_query`

**Inputs** doctype = no value, txt = no value, searchfield = no value, start = no value, page\_len = no value, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** query.run().

**Local steps**

- Evaluate Platform.has\_permission(“Production Plan”, throw = true).
- If not filters.
  - Set filters from mapping().
- Set so\_table from Platform.qb.DocType(“Sales Order”).
- Set table from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(table.parent).distinct().where((table.stock\_qty &gt; table.production\_plan\_qty bitwise and table.docstatus equals 1)).
- If filters.get(“company”).
  - Set query from query.where(so\_table.company equals filters.get(“company”)).
- If filters.get(“sales\_orders”).
  - Set query from query.where(so\_table.name.isin(filters.get(“sales\_orders”))).
- If filters.get(“item\_code”).
  - Set query from query.where(table.item\_code equals filters.get(“item\_code”)).
- If txt.
  - Set query from query.where(table.parent.like(formatted text %{txt}%)).
- For each condition in get\_user\_permission\_conditions\_qb(“Sales Order”, so\_table).
  - Set query from query.where(condition).
- If page\_len.
  - Set query from query.limit(page\_len).
- If start.
  - Set query from query.offset(start).
- Return query.run().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L964)

<a id="op-67be180cd9c03f"></a>
### Get reserved qty for sub assembly

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_reserved_qty_for_sub_assembly`

**Inputs** item\_code, warehouse.

**Wrappers, in declaration order** record a compatibility advisory for the invoked interface.

**Explicit results** get\_reserved\_qty\_for\_production\_plan(item\_code, warehouse).

**Local steps**

- Return get\_reserved\_qty\_for\_production\_plan(item\_code, warehouse).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L929)

<a id="op-a8e19669686e21"></a>
### Make stock reservation entries

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_make_stock_reservation_entries`

**Inputs** doc, items = no value, table\_name = no value, notify = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Production Plan” via get\_doc.

**Local steps**

- If isinstance(doc, str).
  - Set doc from parse\_json(doc).
  - Set doc from Platform.get\_doc(“Production Plan”, doc.get(“name”)).
- Evaluate Platform.has\_permission(“Production Plan”, “write”, doc = doc, throw = true).
- Evaluate reserve\_stock\_for\_production\_plan(doc, items, table\_name, notify).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, “write”, doc = doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L943)

<a id="op-675cbbd17bd59f"></a>
### Reserve stock for production plan

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_reserve_stock_for_production_plan`

**Inputs** doc, items = no value, table\_name = no value, notify = false.

**State and service calls** msgprint with translated “Stock Reservation Entries Created”.

**Local steps**

- If (items and isinstance(items, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in items → isinstance(items, str).
  - Set items from parse\_json(items).
- Set mapper from mapping(“sub\_assembly\_items” → mapping(“table\_name” → “sub\_assembly\_items”, “qty\_field” → “required\_qty”, “warehouse\_field” → “fg\_warehouse”), “mr\_items” → mapping(“table\_name” → “mr\_items”, “qty\_field” →  ….
- For each child\_table\_name in mapper.
  - If (table\_name and table\_name differs from child\_table\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_name → table\_name differs from child\_table\_name.
    - Continue with the next iteration or loop test.
  - Set sre from StockReservation(doc, items = items, kwargs = mapper at child\_table\_name).
  - If doc.docstatus equals 1.
    - Set sre\_created from sre.make\_stock\_reservation\_entries().
    - If sre\_created.
      - Evaluate Platform.msgprint(translated “Stock Reservation Entries Created”, alert = true).
  - Otherwise.
    - If doc.docstatus equals 2.
      - Evaluate sre.cancel\_stock\_reservation\_entries().
- Evaluate doc.reload().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L960)

<a id="op-87b003788869e6"></a>
### Cancel stock reservation entries

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_cancel_stock_reservation_entries`

**Inputs** doc, sre\_list.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Production Plan” via get\_doc.

**Local steps**

- If isinstance(doc, str).
  - Set doc from parse\_json(doc).
  - Set doc from Platform.get\_doc(“Production Plan”, doc.get(“name”)).
- Evaluate Platform.has\_permission(“Production Plan”, “write”, doc = doc, throw = true).
- Set sre from StockReservation(doc).
- Evaluate sre.cancel\_stock\_reservation\_entries(sre\_list).
- Evaluate doc.reload().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, “write”, doc = doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L900)

<a id="op-ca9bb944e504d2"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_production_plan_production_plan_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “production\_plan”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “voucher\_no”), “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Wo ….

**Local steps**

- Return mapping(“fieldname” → “production\_plan”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “voucher\_no”), “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Wo ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L620)

<a id="op-16bd991433d2b9"></a>
### Production Plan Work Order Quantities.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_init`

**Inputs** self, production\_plan.

**Local steps**

- Set self.production\_plan from production\_plan.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L977)

<a id="op-cb4b387c276256"></a>
### Production Plan Work Order Quantities.validate work order

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_validate_work_order`

**Inputs** self, work\_order, process\_loss\_qty (named only, default 0).

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit failure paths** validation helper with OverProductionError — translated “Row {0} in {1} {2}: Work Order quantity after process loss {3} exceeds the remaining allowed quantity {4}.”.format(row.idx, translated row.doctype, get\_link\_to\_form(“Production Plan”, self.prod ….

**Local steps**

- Bind dependencies round\_up\_to\_whole\_unit.
- Bind dependencies OverProductionError.
- Set row from self.lock\_plan\_row(work\_order).
- Set committed from self.get\_committed\_quantities(exclude\_work\_order = work\_order.name, reference\_field = row.reference\_field, reference\_name = row.name, for\_update = true) at row.reference\_field.get(row.name, 0).
- Set allowance from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
- Set precision from work\_order.precision(“qty”).
- Set maximum\_qty from flt(round\_up\_to\_whole\_unit(((row.order\_qty × (1 + (allowance ÷ 100))) − committed), row.stock\_uom), precision).
- Set committed\_qty from flt(self.\_get\_committed\_qty(work\_order, process\_loss\_qty, row.process\_loss\_percentage), precision).
- If committed\_qty &gt; maximum\_qty.
  - Call the validation error handler Platform.throw(translated “Row {0} in {1} {2}: Work Order quantity after process loss {3} exceeds the remaining allowed quantity {4}.”.format(row.idx, translated row.doctype, get\_link\_to\_form(“Production P ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [lock plan row](operations-035.md#op-525c9355fd9b85), [get committed quantities](operations-035.md#op-8a47c207d1e24f), [get committed qty](operations-035.md#op-a7b2c5f09c223e).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L979)

<a id="op-525c9355fd9b85"></a>
### Production Plan Work Order Quantities.lock plan row

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_lock_plan_row`

**Inputs** self, work\_order.

**Record and data access** read row\_doctype via get\_value.

**Explicit results** row.

**Explicit failure paths** validation helper — translated “Work Order must reference only one Production Plan row.” · validation helper — translated “Work Order must reference a row in Production Plan {0}.”.format(get\_link\_to\_form(“Production Plan”, self.production\_plan)).

**Local steps**

- If (work\_order.production\_plan\_item and work\_order.production\_plan\_sub\_assembly\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.production\_plan\_item → work\_order.production\_plan\_sub\_assembly\_item.
  - Call the validation error handler Platform.throw(translated “Work Order must reference only one Production Plan row.”).
- If work\_order.production\_plan\_sub\_assembly\_item.
  - Set reference\_field from “production\_plan\_sub\_assembly\_item”.
  - Set row\_doctype from “Production Plan Sub Assembly Item”.
- Otherwise.
  - Set reference\_field from “production\_plan\_item”.
  - Set row\_doctype from “Production Plan Item”.
- Set reference\_name from work\_order.get(reference\_field).
- Set row from Platform.db.get\_value(row\_doctype, mapping(“name” → reference\_name, “parent” → self.production\_plan), list(“name”, “idx”, QTY\_FIELDS at reference\_field, “process\_loss\_percentage”, …), as\_dict = true, for\_u ….
  - Value choice on reference\_name — true gives Platform.db.get\_value(row\_doctype, mapping(“name” → reference\_name, “parent” → self.production\_plan), list(“name”, “idx”, QTY\_FIELDS at reference\_field, “process\_loss\_percentage”, …), as\_dict = true, for\_u …, false gives no value.
- If not row.
  - Call the validation error handler Platform.throw(translated “Work Order must reference a row in Production Plan {0}.”.format(get\_link\_to\_form(“Production Plan”, self.production\_plan))).
- Set row.reference\_field from reference\_field.
- Set row.doctype from row\_doctype.
- Set row.order\_qty from self.get\_order\_qty(row, reference\_field).
- Return row.

**Methods declared on this owner** [get order qty](operations-035.md#op-6747cf17834441).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L978)

<a id="op-6747cf17834441"></a>
### Production Plan Work Order Quantities.get order qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_get_order_qty`

**Inputs** row, reference\_field.

**Wrappers, in declaration order** staticmethod.

**Explicit results** get\_qty\_before\_process\_loss(row.get(QTY\_FIELDS at reference\_field), row.process\_loss\_percentage, row.stock\_uom).

**Local steps**

- Bind dependencies get\_qty\_before\_process\_loss.
- Return get\_qty\_before\_process\_loss(row.get(QTY\_FIELDS at reference\_field), row.process\_loss\_percentage, row.stock\_uom).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L974)

<a id="op-a97af9e8c46af5"></a>
### Production Plan Work Order Quantities.get pending quantities

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_get_pending_quantities`

**Inputs** self, plan.

**Explicit results** pending.

**Local steps**

- Bind dependencies round\_up\_to\_whole\_unit.
- Set committed from self.get\_committed\_quantities(include\_drafts = true).
- Set precision from Platform.get\_precision(“Work Order”, “qty”).
- Set pending from mapping().
- For each tuple(table, reference\_field) in tuple(tuple(“po\_items”, “production\_plan\_item”), tuple(“sub\_assembly\_items”, “production\_plan\_sub\_assembly\_item”)).
  - Set pending at reference\_field from mapping of row.name → max(0, flt(round\_up\_to\_whole\_unit((nested operand in the contract.get\_order\_qty(row, reference\_field) − nested operand in the contract.get(nested operand in the contract.name, 0)), ro ….
    - Draw row from plan.get(table), keep a combination only if ((table equals “po\_items” or row.type\_of\_manufacturing equals “In House”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in table equals “po\_items” → row.type\_of\_manufacturing equals “In House”.
- Return pending.

**Methods declared on this owner** [get committed quantities](operations-035.md#op-8a47c207d1e24f), [get order qty](operations-035.md#op-6747cf17834441).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L975)

<a id="op-8a47c207d1e24f"></a>
### Production Plan Work Order Quantities.get committed quantities

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_get_committed_quantities`

**Inputs** self, exclude\_work\_order = no value, reference\_field = no value, reference\_name = no value, for\_update = false, include\_drafts = false.

**Explicit results** quantities.

**Local steps**

- Set table from Platform.qb.DocType(“Work Order”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.produc ….
  - Value choice on include\_drafts — true gives table.docstatus &lt; 2, false gives table.docstatus equals 1.
- If exclude\_work\_order.
  - Set query from query.where(table.name differs from exclude\_work\_order).
- If reference\_field.
  - Set query from query.where(table at reference\_field equals reference\_name).
- If for\_update.
  - Set query from query.for\_update().
- Set work\_orders from query.run(as\_dict = true).
- Set loss\_percentages from self.get\_planned\_loss\_percentages().
- Set quantities from mapping(“production\_plan\_item” → defaultdict(float), “production\_plan\_sub\_assembly\_item” → defaultdict(float)).
- For each work\_order in work\_orders.
  - Set field from “production\_plan\_sub\_assembly\_item” when work\_order.production\_plan\_sub\_assembly\_item, otherwise “production\_plan\_item”.
    - Value choice on work\_order.production\_plan\_sub\_assembly\_item — true gives “production\_plan\_sub\_assembly\_item”, false gives “production\_plan\_item”.
  - If work\_order.get(field).
    - Update quantities at field at work\_order at field using + self.\_get\_committed\_qty(work\_order, work\_order.process\_loss\_qty, loss\_percentages.get(work\_order at field)).
- Return quantities.

**Methods declared on this owner** [get planned loss percentages](operations-035.md#op-16e168e272b668), [get committed qty](operations-035.md#op-a7b2c5f09c223e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L973)

<a id="op-16e168e272b668"></a>
### Production Plan Work Order Quantities.get planned loss percentages

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_get_planned_loss_percentages`

**Inputs** self.

**Record and data access** read doctype via get\_all.

**Explicit results** loss\_percentages.

**Local steps**

- Set loss\_percentages from mapping().
- For each doctype in tuple(“Production Plan Item”, “Production Plan Sub Assembly Item”).
  - Evaluate loss\_percentages.update(Platform.get\_all(doctype, filters = mapping(“parent” → self.production\_plan, “process\_loss\_percentage” → tuple(“&gt;”, 0)), fields = list(“name”, “process\_loss\_percentage”), as\_list = true)).
- Return loss\_percentages.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L976)

<a id="op-a7b2c5f09c223e"></a>
### Production Plan Work Order Quantities.get committed qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_work_order_quantities_productionplanworkorderquantities_get_committed_qty`

**Inputs** self, work\_order, process\_loss\_qty, planned\_loss\_percentage.

**Explicit results** max(0, flt(work\_order.produced\_qty), committed\_qty).

**Local steps**

- Bind dependencies get\_planned\_loss\_percentage.
- Set loss\_percentage from get\_planned\_loss\_percentage(planned\_loss\_percentage).
- Set good\_qty from (flt(work\_order.qty) − max(flt(process\_loss\_qty), ((flt(work\_order.qty) × loss\_percentage) ÷ 100))).
- Set committed\_qty from (good\_qty ÷ (1 − (loss\_percentage ÷ 100))).
- Return max(0, flt(work\_order.produced\_qty), committed\_qty).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L972)

## Report · Production plan summary

<a id="op-40bebee66eccac"></a>
### Execute

`operation_enterprise_manufacturing_report_production_plan_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set data from get\_data(filters).
- Set columns from get\_column(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1187)
