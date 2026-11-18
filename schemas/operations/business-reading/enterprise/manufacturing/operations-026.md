# Production · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Master production schedule

[Record definition](../../../../data/record-types/master_production_schedule.json)

<a id="op-59607021ee8fb7"></a>
### Master Production Schedule.get item wise mps data

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_item_wise_master_production_schedule_data`

**Inputs** self, data.

**Explicit results** item\_wise\_data.

**Local steps**

- Set item\_wise\_data from Platform.\_dict(mapping()).
- For each item in data.
  - Set key from tuple(item.item\_code, item.delivery\_date, item.warehouse).
  - If key does not belong to item\_wise\_data.
    - Set item\_wise\_data at key from Platform.\_dict(mapping(“item\_code” → item.item\_code, “delivery\_date” → item.delivery\_date, “warehouse” → item.warehouse, “stock\_uom” → item.stock\_uom, …)).
  - Set item\_details from item\_wise\_data at key.
  - Update item\_details.qty using + item.qty.
- Return item\_wise\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L546)

<a id="op-9b86be180ee0f4"></a>
### Master Production Schedule.add mps data

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_add_master_production_schedule_data`

**Inputs** self, data.

**Local steps**

- Set data from Platform.\_dict(sorted(data.items(), key = deferred anonymous expression)).
- For each key in data.
  - Set row from data at key.
  - Set row.cumulative\_lead\_time from math.ceil(row.cumulative\_lead\_time).
  - Set row.order\_release\_date from add\_days(row.delivery\_date, negative row.cumulative\_lead\_time).
  - Set row.planned\_qty from row.qty.
  - Set row.uom from row.stock\_uom.
  - Set row.warehouse from (row.warehouse or self.parent\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.warehouse → self.parent\_warehouse.
  - Evaluate self.append(“items”, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L4306) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L537)

<a id="op-d7e0f4168c1766"></a>
### Master Production Schedule.get distinct items

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_distinct_items`

**Inputs** self, data.

**Explicit results** items.

**Local steps**

- Set items from list().
- For each item in data.
  - If item.item\_code does not belong to items.
    - Evaluate items.append(item.item\_code).
- Return items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L4677) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L544)

<a id="op-27d0739bfbfb40"></a>
### Master Production Schedule.fetch materials requests

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_fetch_materials_remote_requests`

**Inputs** self, remaining named values data.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “No open Material Requests found for the given criteria.” · call save on self.

**Explicit results** no value.

**Local steps**

- If isinstance(data, str).
  - Set data from parse\_json(data).
- Evaluate self.set(“material\_requests”, list()).
- Set materials\_requests from self.get\_material\_requests(data).
- If not materials\_requests.
  - Evaluate Platform.msgprint(translated “No open Material Requests found for the given criteria.”, alert = true).
  - Return no value.
- For each row in materials\_requests.
  - Evaluate self.append(“material\_requests”, mapping(“material\_request” → row.name, “material\_request\_date” → row.transaction\_date)).
- If not self.is\_new().
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get material requests](operations-026.md#op-daed11aa03bdff).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L4803) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L539)

<a id="op-daed11aa03bdff"></a>
### Master Production Schedule.get material requests

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_material_remote_requests`

**Inputs** self, data.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Material Request”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.name, doctype.transaction\_date).where((doctype.docstatus equals 1 bitwise and nested operand in the contract.status.notin(list( ….
- If data.get(“material\_request\_type”).
  - Set query from query.where(doctype.material\_request\_type equals data.get(“material\_request\_type”)).
- If data.get(“from\_date”).
  - Set query from query.where(doctype.transaction\_date ≥ data.get(“from\_date”)).
- If data.get(“to\_date”).
  - Set query from query.where(doctype.transaction\_date ≤ data.get(“to\_date”)).
- If self.from\_date.
  - Set query from query.where(doctype.schedule\_date ≥ self.from\_date).
- If self.to\_date.
  - Set query from query.where(doctype.schedule\_date ≤ self.to\_date).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L5179) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L549)

<a id="op-9cf11133382c09"></a>
### Master Production Schedule.fetch sales orders

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_fetch_sales_orders`

**Inputs** self, remaining named values data.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** no value.

**Local steps**

- If isinstance(data, str).
  - Set data from parse\_json(data).
- Evaluate self.set(“sales\_orders”, list()).
- Set sales\_orders from self.get\_sales\_orders(data).
- If not sales\_orders.
  - Return no value.
- For each row in sales\_orders.
  - Evaluate self.append(“sales\_orders”, mapping(“sales\_order” → row.name, “sales\_order\_date” → row.transaction\_date, “delivery\_date” → row.delivery\_date, “customer” → row.customer, …)).
- If not self.is\_new().
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales orders](operations-026.md#op-d3db248d25ce27).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L5843) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L540)

<a id="op-d3db248d25ce27"></a>
### Master Production Schedule.get sales orders

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_sales_orders`

**Inputs** self, kwargs.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Sales Order”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.name, doctype.transaction\_date, doctype.delivery\_date, doctype.customer, …).where((doctype.docstatus equals 1 bitwise and neste ….
- If kwargs.get(“customer”).
  - Set query from query.where(doctype.customer equals kwargs.get(“customer”)).
- If kwargs.get(“from\_date”).
  - Set query from query.where(doctype.transaction\_date ≥ kwargs.get(“from\_date”)).
- If kwargs.get(“to\_date”).
  - Set query from query.where(doctype.transaction\_date ≤ kwargs.get(“to\_date”)).
- If kwargs.get(“delivery\_from\_date”).
  - Set query from query.where(doctype.delivery\_date ≥ kwargs.get(“delivery\_from\_date”)).
- If kwargs.get(“delivery\_to\_date”).
  - Set query from query.where(doctype.delivery\_date ≤ kwargs.get(“delivery\_to\_date”)).
- If items bound to self.get\_items\_for\_mps().
  - Set doctype\_item from Platform.qb.DocType(“Sales Order Item”).
  - Set query from query.join(doctype\_item).on(doctype\_item.parent equals doctype.name).
  - Set query from query.where(doctype\_item.item\_code.isin(items)).
- Return query.run(as\_dict = true).

**Methods declared on this owner** [get items for mps](operations-026.md#op-b27eb3cf9b15ac).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L553)

<a id="op-b27eb3cf9b15ac"></a>
### Master Production Schedule.get items for mps

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_items_for_master_production_schedule`

**Inputs** self.

**Explicit results** no value · list of d.item\_code for d drawn from self.select\_items where d.item\_code.

**Local steps**

- If not self.select\_items.
  - Return no value.
- Return list of d.item\_code for d drawn from self.select\_items where d.item\_code.
  - Draw d from self.select\_items, keep a combination only if (d.item\_code).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L7177) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L547)

<a id="op-edb9bd3995d08e"></a>
### Master Production Schedule.on update

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_on_update`

**Inputs** self.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If (previous and previous.sales\_forecast differs from self.sales\_forecast).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.sales\_forecast differs from self.sales\_forecast.
  - Evaluate update\_sales\_forecast\_status(previous.sales\_forecast).
- Evaluate update\_sales\_forecast\_status(self.sales\_forecast).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L890)

<a id="op-276d7f629050c2"></a>
### Master Production Schedule.after delete

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_after_delete`

**Inputs** self.

**Local steps**

- Evaluate update\_sales\_forecast\_status(self.sales\_forecast).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L885)

<a id="op-123fed36f51403"></a>
### Master Production Schedule.on submit

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.enqueue\_mrp\_creation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [enqueue mrp creation](operations-026.md#op-4d635f9d5d3a12).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L7273) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L555)

<a id="op-4d635f9d5d3a12"></a>
### Master Production Schedule.enqueue mrp creation

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_enqueue_material_requirements_planning_creation`

**Inputs** self.

**State and service calls** enqueue doc with “Master Production Schedule” · msgprint with translated “MRP Log documents are being created in the background.”.

**Local steps**

- Evaluate Platform.enqueue\_doc(“Master Production Schedule”, self.name, “make\_mrp”, queue = “long”, timeout = 1800, enqueue\_after\_commit = true).
- Evaluate Platform.msgprint(translated “MRP Log documents are being created in the background.”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue\_doc(“Master Production Schedule”, self.name, “make\_mrp”, queue = “long”, timeout = 1800, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L538)

<a id="op-f20aee3b029805"></a>
### Get own lead time

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_get_own_lead_time`

**Inputs** lead\_time, qty, is\_manufactured.

**Explicit results** 0 · (days + flt(lead\_time.buffer\_time)).

**Local steps**

- If not lead\_time.
  - Return 0.
- If is\_manufactured.
  - Set days from get\_days\_needed(lead\_time, qty, 0).
- Otherwise.
  - Set days from flt(lead\_time.purchase\_time).
- Return (days + flt(lead\_time.buffer\_time)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L884)

<a id="op-151e5c41c9a34c"></a>
### Get days needed

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_get_days_needed`

**Inputs** lead\_time, qty, no\_of\_shifts.

**Explicit results** (qty ÷ capacity) · ((cint(lead\_time.manufacturing\_time\_in\_mins) × qty) ÷ minutes\_per\_day) · 0.

**Local steps**

- Set capacity from get\_daily\_capacity(lead\_time, no\_of\_shifts).
- If capacity.
  - Return (qty ÷ capacity).
- If lead\_time.manufacturing\_time\_in\_mins.
  - Set minutes\_per\_day from (get\_daily\_working\_mins(lead\_time, no\_of\_shifts) × (cint(lead\_time.no\_of\_workstations) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(lead\_time.no\_of\_workstations) → 1.
  - Return ((cint(lead\_time.manufacturing\_time\_in\_mins) × qty) ÷ minutes\_per\_day).
- Return 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L883)

<a id="op-36f3df6cead445"></a>
### Get daily working mins

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_get_daily_working_mins`

**Inputs** lead\_time, no\_of\_shifts.

**Explicit results** (((no\_of\_shifts or cint(lead\_time.no\_of\_shift) or 1) × (cint(lead\_time.shift\_time\_in\_hours) or 8)) × 60.0).

**Local steps**

- Return (((no\_of\_shifts or cint(lead\_time.no\_of\_shift) or 1) × (cint(lead\_time.shift\_time\_in\_hours) or 8)) × 60.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in no\_of\_shifts → cint(lead\_time.no\_of\_shift) → 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(lead\_time.shift\_time\_in\_hours) → 8.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L882)

<a id="op-16f92e14d106d2"></a>
### Get daily capacity

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_get_daily_capacity`

**Inputs** lead\_time, no\_of\_shifts.

**Explicit results** capacity.

**Local steps**

- Set capacity from flt(lead\_time.capacity\_per\_day).
- If (capacity and no\_of\_shifts).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in capacity → no\_of\_shifts.
  - Set capacity from ((capacity × no\_of\_shifts) ÷ (cint(lead\_time.no\_of\_shift) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(lead\_time.no\_of\_shift) → 1.
- Return capacity.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L881)

<a id="op-30fe21a6982bbc"></a>
### Get mps details

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_get_master_production_schedule_details`

**Inputs** mps.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Master Production Schedule” via get\_value.

**Explicit results** Platform.db.get\_value(“Master Production Schedule”, mps, list(“name”, “from\_date”, “to\_date”, “company”, …), as\_dict = true).

**Local steps**

- Evaluate Platform.has\_permission(“Master Production Schedule”, “read”, doc = mps, throw = true).
- Return Platform.db.get\_value(“Master Production Schedule”, mps, list(“name”, “from\_date”, “to\_date”, “company”, …), as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Master Production Schedule”, “read”, doc = mps, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L536)

<a id="op-715bf592d8656e"></a>
### Deduct delivered qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_deduct_delivered_qty`

**Inputs** schedules.

**Explicit results** pending.

**Local steps**

- Set delivered\_by\_row from mapping().
- Set pending from list().
- For each row in schedules.
  - Set delivered from delivered\_by\_row.setdefault(row.sales\_order\_item, flt(row.delivered\_qty)).
  - Set covered from min(delivered, flt(row.qty)).
  - Set delivered\_by\_row at row.sales\_order\_item from (delivered − covered).
  - Set row.qty from (flt(row.qty) − covered).
  - If row.qty &gt; 0.
    - Evaluate pending.append(row).
- Return pending.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L880)

## Service · Material request receipt notification

<a id="op-6507cb0b7c8df9"></a>
### Get context

`operation_enterprise_manufacturing_notification_material_request_receipt_notification_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L7066) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L144)

## Report · Material requirements planning report

<a id="op-53ab7fb104101c"></a>
### Execute

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set obj from MaterialRequirementsPlanningReport(filters).
- Set tuple(data, chart) from obj.generate\_mrp().
- Set columns from obj.get\_columns().
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1108)

<a id="op-ca41e0513cb2db"></a>
### Material Requirements Planning Report.initialize

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_initialize`

**Inputs** self, filters.

**Local steps**

- Set self.filters from filters.
- Set self.qty\_precision from Platform.get\_precision(“Master Production Schedule Item”, “planned\_qty”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1147)

<a id="op-e426e51bd5e2bf"></a>
### Material Requirements Planning Report.generate mrp

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_generate_material_requirements_planning`

**Inputs** self.

**Explicit results** tuple(data, chart).

**Local steps**

- Set self.fg\_items from list().
- Set self.rm\_items from list().
- Set self.dates from self.get\_dates().
- Set self.mps\_data from self.get\_mps\_data().
- Set items from self.get\_items\_from\_mps(self.mps\_data).
- Evaluate self.update\_sales\_forecast\_data().
- Set self.item\_rm\_details from self.get\_raw\_materials\_data(items).
- Set self.\_bin\_details from self.get\_item\_wise\_bin\_details().
- Set self.\_safety\_stock\_reserved from set().
- Evaluate self.add\_non\_planned\_orders(items).
- Set self.\_wo\_details from self.get\_work\_order\_data().
- Set self.\_po\_details from self.get\_purchase\_order\_data().
- Set self.\_so\_details from self.get\_sales\_order\_data().
- Set tuple(data, chart) from self.get\_mrp\_data().
- Return tuple(data, chart).

**Methods declared on this owner** [get dates](operations-028.md#op-23b5a7d0e99e41), [get mps data](operations-028.md#op-2adea26878c589), [get items from mps](operations-028.md#op-ebf8db9b5cf280), [update sales forecast data](operations-027.md#op-3556ef3df7fc48), [get raw materials data](operations-028.md#op-03f4bdbf05e57f), [get item wise bin details](operations-027.md#op-803a75d10335e6), [add non planned orders](operations-026.md#op-1ca067150722c9), [get work order data](operations-027.md#op-07d6f23091eb9f), [get purchase order data](operations-027.md#op-55c2a8c07c3f45), [get sales order data](operations-027.md#op-d7b8f695c6c980), [get mrp data](operations-027.md#op-c736ef641b1122).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1123)

<a id="op-1ca067150722c9"></a>
### Material Requirements Planning Report.add non planned orders

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_add_non_planned_orders`

**Inputs** self, items.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** no value.

**Local steps**

- If not items.
  - Return no value.
- Set \_adhoc\_so\_details from Platform.\_dict(mapping()).
- Set so from Platform.qb.DocType(“Sales Order”).
- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(so\_item.item\_code, so\_item.item\_name, so\_item.deli ….
- Set query from query.where(so\_item.item\_code.isin(items)).
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(so\_item.warehouse.isin(warehouses)).
- If self.filters.get(“from\_date”).
  - Set query from query.where(so\_item.delivery\_date ≥ self.filters.get(“from\_date”)).
- If self.filters.get(“to\_date”).
  - Set query from query.where(so\_item.delivery\_date ≤ self.filters.get(“to\_date”)).
- Set skipped\_data from list().
- If skip\_orders bound to self.get\_orders\_to\_skip().
  - Set skipped\_data from query.where(so.name.isin(skip\_orders)).run(as\_dict = true).
  - Set query from query.where(so.name.notin(skip\_orders)).
- Set data from query.run(as\_dict = true).
- For each row in self.get\_demand\_beyond\_mps(data, skipped\_data).
  - Evaluate self.mps\_data.append(Platform.\_dict(mapping(“item\_code” → row.item\_code, “item\_name” → row.item\_code, “delivery\_date” → row.delivery\_date, “adhoc\_qty” → row.adhoc\_qty, …))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get orders to skip](operations-027.md#op-b4baa2b776c2e3), [get demand beyond mps](operations-026.md#op-8eeff8a69c6fa9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1118)

<a id="op-8eeff8a69c6fa9"></a>
### Material Requirements Planning Report.get demand beyond mps

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_materialrequirementsplanningreport_get_demand_beyond_mps`

**Inputs** self, data, skipped\_data = no value.

**Local steps**

- Set planned from mapping().
- For each row in self.mps\_data.
  - Set key from tuple(row.item\_code, getdate(row.delivery\_date)).
  - Set planned at key from (planned.get(key, 0.0) + flt(row.planned\_qty)).
- For each row in (skipped\_data or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in skipped\_data → list().
  - Set key from tuple(row.item\_code, getdate(row.delivery\_date)).
  - Set planned at key from max((planned.get(key, 0.0) − flt(row.adhoc\_qty)), 0.0).
- Set demand from mapping().
- For each row in data.
  - Set key from tuple(row.item\_code, getdate(row.delivery\_date)).
  - If key belongs to demand.
    - Update demand at key.adhoc\_qty using + flt(row.adhoc\_qty).
  - Otherwise.
    - Set demand at key from row.
- For each tuple(key, row) in demand.items().
  - Set row.adhoc\_qty from (flt(row.adhoc\_qty) − planned.get(key, 0.0)).
  - If row.adhoc\_qty &gt; 0.
    - yield row.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1141)
