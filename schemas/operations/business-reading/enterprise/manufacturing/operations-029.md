# Production · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Material requirements planning report

<a id="op-cb7fd88df16d1f"></a>
### Make work orders

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_make_work_orders`

**Inputs** work\_orders, company, warehouse = no value, mps = no value.

**State and service calls** request new\_doc for “Work Order” · call insert on wo · msgprint with translated “Work Order {0} created”.format(Platform.bold(wo.name)).

**Local steps**

- For each item in work\_orders.
  - Set uom from get\_item\_uom(item.item\_code).stock\_uom.
  - If is\_whole\_number(uom).
    - Set item.required\_qty from math.ceil(flt(item.required\_qty, Platform.get\_precision(“Work Order”, “qty”))).
  - Set wo from Platform.new\_doc(“Work Order”).
  - Set wo.production\_item from item.item\_code.
  - Set wo.bom\_no from item.bom\_no.
  - Set wo.company from company.
  - Set wo.qty from item.required\_qty.
  - Set wo.mps from mps.
  - Set wo.stock\_uom from uom.
  - Set wo.wip\_warehouse from item.default\_warehouse.
  - Set wo.fg\_warehouse from (warehouse or item.default\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → item.default\_warehouse.
  - Set wo.planned\_start\_date from item.release\_date when item.release\_date, otherwise today().
    - Value choice on item.release\_date — true gives item.release\_date, false gives today().
  - Set wo.planned\_end\_date from item.delivery\_date when item.delivery\_date, otherwise today().
    - Value choice on item.delivery\_date — true gives item.delivery\_date, false gives today().
  - Set wo.flags.ignore\_mandatory from true.
  - Evaluate wo.insert().
  - Evaluate Platform.msgprint(translated “Work Order {0} created”.format(Platform.bold(wo.name)), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1116)

<a id="op-6f1fbe89a0eba5"></a>
### Get item uom

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_get_item_unit_of_measure`

**Inputs** item\_code.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Item”, item\_code, list(“stock\_uom”, “purchase\_uom”), as\_dict = true).

**Local steps**

- Return Platform.get\_cached\_value(“Item”, item\_code, list(“stock\_uom”, “purchase\_uom”), as\_dict = true).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“stock\_uom”, “purchase\_uom”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0551.json#L1475) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1112)

<a id="op-ef1a0147c216f4"></a>
### Get uom conversion factor

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_uom_conversion_factor`

**Inputs** item\_code, uom.

**Wrappers, in declaration order** Platform.request\_cache.

**Explicit results** get\_conversion\_factor(item\_code, uom).get(“conversion\_factor”).

**Local steps**

- Return get\_conversion\_factor(item\_code, uom).get(“conversion\_factor”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1139)

<a id="op-b9ea52672d007b"></a>
### Is whole number

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_is_whole_number`

**Inputs** uom.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).

**Local steps**

- Return Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0551.json#L1580) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1113)

<a id="op-a63ea44b8f34a7"></a>
### Split forecast qty

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_split_forecast_qty`

**Inputs** rows, qty.

**Local steps**

- Set total\_planned\_qty from sum(generator of flt(d.planned\_qty) for d drawn from rows).
  - Draw d from rows.
- Set shares from list of ((qty × flt(d.planned\_qty)) ÷ total\_planned\_qty) when total\_planned\_qty, otherwise qty when idx equals 0, otherwise 0 for tuple(idx, d) drawn from enumerate(rows).
  - Draw tuple(idx, d) from enumerate(rows).
  - Value choice on total\_planned\_qty — true gives ((qty × flt(d.planned\_qty)) ÷ total\_planned\_qty), false gives qty when idx equals 0, otherwise 0.
  - Value choice on idx equals 0 — true gives qty, false gives 0.
- If (flt(qty) equals round(qty) and is\_whole\_number\_item(rows at 0.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(qty) equals round(qty) → is\_whole\_number\_item(rows at 0.item\_code).
  - Set shares from round\_shares\_keeping\_total(shares, round(qty)).
- For each tuple(d, share) in zip(rows, shares, strict = true).
  - Update d.sales\_forecast\_qty using + share.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1145)

<a id="op-e2cf9e53c8ce77"></a>
### Is whole number item

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_is_whole_number_item`

**Inputs** item\_code.

**Record and data access** read “Item” via get\_cached\_value · read “UOM” via get\_cached\_value.

**Explicit results** bool((stock\_uom and Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”))).

**Local steps**

- Set stock\_uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
- Return bool((stock\_uom and Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_uom → Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”), Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1140)

<a id="op-964ee6fd024317"></a>
### Round shares keeping total

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_round_shares_keeping_total`

**Inputs** shares, total.

**Explicit results** rounded.

**Local steps**

- Set rounded from list of math.floor(share) for share drawn from shares.
  - Draw share from shares.
- Set by\_remainder from sorted(range(len(shares)), key = deferred anonymous expression, reverse = true).
- For each idx in by\_remainder at slice no value to max((total − sum(rounded)), 0).
  - Update rounded at idx using + 1.
- Return rounded.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1144)

## Record · Operation

[Record definition](../../../../data/record-types/operation.json)

<a id="op-3f2938e6752efd"></a>
### Operation.validate

`operation_enterprise_manufacturing_record_definitions_operation_business_behavior_operation_validate`

**Inputs** self.

**Local steps**

- If not self.description.
  - Set self.description from self.name.
- Evaluate self.duplicate\_sub\_operation().
- Evaluate self.set\_total\_time().

If control reaches the end, it returns no value.

**Methods declared on this owner** [duplicate sub operation](operations-029.md#op-913dc8dd85e2ad), [set total time](operations-029.md#op-8cb87671df916b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L765) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L562)

<a id="op-913dc8dd85e2ad"></a>
### Operation.duplicate sub operation

`operation_enterprise_manufacturing_record_definitions_operation_business_behavior_operation_duplicate_subordinate_operation`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The operation {0} can not add multiple times”.format(Platform.bold(row.operation)) · validation helper — translated “The operation {0} can not be the sub operation”.format(Platform.bold(row.operation)).

**Local steps**

- Set operation\_list from list().
- For each row in self.sub\_operations.
  - If row.operation belongs to operation\_list.
    - Call the validation error handler Platform.throw(translated “The operation {0} can not add multiple times”.format(Platform.bold(row.operation))).
  - If self.name equals row.operation.
    - Call the validation error handler Platform.throw(translated “The operation {0} can not be the sub operation”.format(Platform.bold(row.operation))).
  - Evaluate operation\_list.append(row.operation).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L560)

<a id="op-8cb87671df916b"></a>
### Operation.set total time

`operation_enterprise_manufacturing_record_definitions_operation_business_behavior_operation_set_total_time`

**Inputs** self.

**Local steps**

- Set self.total\_operation\_time from 0.0.
- For each row in self.sub\_operations.
  - Update self.total\_operation\_time using + row.time\_in\_mins.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L1178) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L561)

<a id="op-f7900ca2aa0df5"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_operation_operation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “operation”, “transactions” → list(mapping(“label” → translated “Manufacture”, “items” → list(“BOM”, “Work Order”, “Job Card”)))).

**Local steps**

- Return mapping(“fieldname” → “operation”, “transactions” → list(mapping(“label” → translated “Manufacture”, “items” → list(“BOM”, “Work Order”, “Job Card”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L1266) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L563)

## Record · Plant floor

[Record definition](../../../../data/record-types/plant_floor.json)

<a id="op-6187352b8e822c"></a>
### Plant Floor.validate

`operation_enterprise_binding_enterprise_manufacturing_doctype_plant_floor_plant_floor_plantfloor_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_warehouse().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate warehouse](operations-029.md#op-a0c50cc58980c4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L893)

<a id="op-a0c50cc58980c4"></a>
### Plant Floor.validate warehouse

`operation_enterprise_binding_enterprise_manufacturing_doctype_plant_floor_plant_floor_plantfloor_validate_warehouse`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Warehouse {0} is a group warehouse”.format(Platform.bold(self.warehouse)) · validation helper — translated “Warehouse {0} does not belong to company {1}”.format(Platform.bold(self.warehouse), Platform.bold(self.company)).

**Local steps**

- If not self.warehouse.
  - Return no value.
- Set warehouse from Platform.get\_cached\_value(“Warehouse”, self.warehouse, list(“is\_group”, “company”), as\_dict = true).
- If warehouse.is\_group.
  - Call the validation error handler Platform.throw(translated “Warehouse {0} is a group warehouse”.format(Platform.bold(self.warehouse))).
- If (self.company and warehouse.company differs from self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → warehouse.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Warehouse {0} does not belong to company {1}”.format(Platform.bold(self.warehouse), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, self.warehouse, list(“is\_group”, “company”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L894)

<a id="op-7b8d46966d84e8"></a>
### Plant Floor.make stock entry

`operation_enterprise_manufacturing_record_definitions_plant_floor_business_behavior_plant_floor_make_stock_entry`

**Inputs** self, kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Stock Entry”.

**Explicit results** stock\_entry.

**Local steps**

- If isinstance(kwargs, str).
  - Set kwargs from Platform.parse\_json(kwargs).
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Set stock\_entry from Platform.new\_doc(“Stock Entry”).
- Evaluate stock\_entry.update(mapping(“company” → kwargs.company, “from\_warehouse” → kwargs.from\_warehouse, “to\_warehouse” → kwargs.to\_warehouse, “purpose” → kwargs.purpose, …)).
- Evaluate stock\_entry.set\_missing\_values().
- Return stock\_entry.

**Methods declared on this owner** [get item details](operations-029.md#op-95312b25cdeab4).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L568)

<a id="op-95312b25cdeab4"></a>
### Plant Floor.get item details

`operation_enterprise_manufacturing_record_definitions_plant_floor_business_behavior_plant_floor_get_item_details`

**Inputs** self, kwargs.

**Declared result** list at dict.

**Record and data access** read “Item” via get\_value.

**Explicit results** list(item\_details).

**Local steps**

- Set item\_details from Platform.db.get\_value(“Item”, kwargs.item\_code, list(“item\_name”, “stock\_uom”, “item\_group”, “description”), as\_dict = true).
- Evaluate item\_details.update(mapping(“qty” → kwargs.qty, “uom” → item\_details.stock\_uom, “item\_code” → kwargs.item\_code, “conversion\_factor” → 1, …)).
- Return list(item\_details).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L2188) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L567)

<a id="op-ec8ebae6b06955"></a>
### Get stock summary

`operation_enterprise_manufacturing_record_definitions_plant_floor_business_behavior_get_stock_summary`

**Inputs** warehouse, start = 0, item\_code = no value, item\_group = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** stock\_details.

**Local steps**

- Evaluate Platform.has\_permission(“Warehouse”, doc = warehouse, throw = true).
- If item\_code.
  - Evaluate Platform.has\_permission(“Item”, doc = item\_code, throw = true).
- If item\_group.
  - Evaluate Platform.has\_permission(“Item Group”, doc = item\_group, throw = true).
- Set stock\_details from get\_stock\_details(warehouse, start = start, item\_code = item\_code, item\_group = item\_group).
- Set max\_count from 0.0.
- For each d in stock\_details.
  - Set d.actual\_or\_pending from (((d.projected\_qty + d.reserved\_qty) + d.reserved\_qty\_for\_production) + d.reserved\_qty\_for\_sub\_contract).
  - Set d.pending\_qty from 0.
  - Set d.total\_reserved from ((d.reserved\_qty + d.reserved\_qty\_for\_production) + d.reserved\_qty\_for\_sub\_contract).
  - If d.actual\_or\_pending &gt; d.actual\_qty.
    - Set d.pending\_qty from (d.actual\_or\_pending − d.actual\_qty).
  - Set d.max\_count from max(d.actual\_or\_pending, d.actual\_qty, d.total\_reserved, max\_count).
  - Set max\_count from d.max\_count.
  - Set d.item\_link from get\_link\_to\_form(“Item”, d.item\_code).
- Return stock\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Warehouse”, doc = warehouse, throw = true), Platform.has\_permission(“Item”, doc = item\_code, throw = true) and 1 further calls.

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L566)

<a id="op-0a270363fc8b16"></a>
### Get stock details

`operation_enterprise_manufacturing_record_definitions_plant_floor_business_behavior_get_stock_details`

**Inputs** warehouse, start = 0, item\_code = no value, item\_group = no value.

**Record and data access** read “Item Group” via get\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set item\_table from Platform.qb.DocType(“Item”).
- Set bin\_table from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract(nested operand in the contract).limit(20).offset(start).orderby(bin\_table.actual\_qty, order = Order.desc).
- If item\_code.
  - Set query from query.where(bin\_table.item\_code equals item\_code).
- If item\_group.
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Item Group”, item\_group, list(“lft”, “rgt”)).
  - Set item\_group\_table from Platform.qb.DocType(“Item Group”).
  - Set query from query.where(item\_table.item\_group.isin(nested operand in the contract(nested operand in the contract).select(item\_group\_table.name).where((item\_group\_table.lft ≥ lft bitwise and item\_group\_table.rgt ≤ rgt)))).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L565)

## Report · Process loss report

<a id="op-e0cd6f0d90460e"></a>
### Execute

`operation_enterprise_manufacturing_report_process_loss_report_business_behavior_execute`

**Inputs** filters.

**Declared result** tuple at tuple(Columns, Data).

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1165)

<a id="op-bd49b860309e3b"></a>
### Get data

`operation_enterprise_manufacturing_report_process_loss_report_business_behavior_get_data`

**Inputs** filters.

**Declared result** Data.

**Explicit results** data.

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set se from Platform.qb.DocType(“Stock Entry”).
- Set finished\_items from get\_finished\_items(filters).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(get\_stock\_entry\_conditions(se, filter ….
- If filters.get(“item”).
  - Set query from query.where(wo.production\_item equals filters.item).
- If filters.get(“work\_order”).
  - Set query from query.where(wo.name equals filters.work\_order).
- Set data from query.run(as\_dict = true).
- Evaluate update\_data\_with\_total\_pl\_value(data).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1167)

<a id="op-ec3e827cf35d4c"></a>
### Get finished items

`operation_enterprise_binding_enterprise_manufacturing_report_process_loss_report_process_loss_report_get_finished_items`

**Inputs** filters.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set se from Platform.qb.DocType(“Stock Entry”).
- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set production\_item\_qty from Case().when(sed.item\_code equals wo.production\_item, sed.transfer\_qty).else\_(0).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1146)

<a id="op-44a0601fa9058c"></a>
### Get stock entry conditions

`operation_enterprise_binding_enterprise_manufacturing_report_process_loss_report_process_loss_report_get_stock_entry_conditions`

**Inputs** se, filters.

**Explicit results** (((se.company equals filters.company bitwise and se.docstatus equals 1) bitwise and se.purpose equals “Manufacture”) bitwise and se.posting\_date.between(filters.from\_date, filters.to\_date)).

**Local steps**

- Return (((se.company equals filters.company bitwise and se.docstatus equals 1) bitwise and se.purpose equals “Manufacture”) bitwise and se.posting\_date.between(filters.from\_date, filters.to\_date)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1147)

<a id="op-756c772c678396"></a>
### Get columns

`operation_enterprise_manufacturing_report_process_loss_report_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** Columns.

**Explicit results** list(mapping(“label” → translated “Work Order”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Work Order”, …), mapping(“label” → translated “Item”, “fieldname” → “production\_item”, “fieldtype” → ….

**Local steps**

- Return list(mapping(“label” → translated “Work Order”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Work Order”, …), mapping(“label” → translated “Item”, “fieldname” → “production\_item”, “fieldtype” → ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0552.json#L1325) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1166)

<a id="op-00a1df648b48c2"></a>
### Update data with total pl value

`operation_enterprise_manufacturing_report_process_loss_report_business_behavior_update_data_with_total_profit_and_loss_value`

**Inputs** data.

**Declared result** no value.

**Local steps**

- For each row in data.
  - Set processed\_qty from (row at “output\_qty” + row at “process\_loss\_qty”).
  - Set row at “total\_pl\_value” from ((row at “process\_loss\_qty” × row at “total\_fg\_value”) ÷ processed\_qty).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1168)

## Report · Production analytics

<a id="op-6ce11f3b741c44"></a>
### Execute

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set period\_columns from get\_period\_columns(filters).
- Set columns from get\_columns(period\_columns).
- Set tuple(data, chart) from get\_data(filters, period\_columns).
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1177)
