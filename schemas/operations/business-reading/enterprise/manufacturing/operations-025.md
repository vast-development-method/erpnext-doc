# Production · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Manufacturing settings

[Record definition](../../../../data/record-types/manufacturing_settings.json)

<a id="op-3c61c67014b259"></a>
### Manufacturing Settings.before save

`operation_enterprise_manufacturing_record_definitions_manufacturing_settings_business_behavior_manufacturing_settings_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.reset\_values().
- Set self.capacity\_planning\_for\_days from (cint(self.capacity\_planning\_for\_days) or DEFAULT\_CAPACITY\_PLANNING\_DAYS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(self.capacity\_planning\_for\_days) → DEFAULT\_CAPACITY\_PLANNING\_DAYS.

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset values](operations-025.md#op-58d0868705003f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L534)

<a id="op-58d0868705003f"></a>
### Manufacturing Settings.reset values

`operation_enterprise_manufacturing_record_definitions_manufacturing_settings_business_behavior_manufacturing_settings_reset_values`

**Inputs** self.

**Local steps**

- If (self.backflush\_raw\_materials\_based\_on differs from “BOM” and self.validate\_components\_quantities\_per\_bom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.backflush\_raw\_materials\_based\_on differs from “BOM” → self.validate\_components\_quantities\_per\_bom.
  - Set self.validate\_components\_quantities\_per\_bom from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0484.json#L7507) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L535)

<a id="op-4f51d02dd45e78"></a>
### Get mins between operations

`operation_enterprise_manufacturing_record_definitions_manufacturing_settings_business_behavior_get_mins_between_operations`

**Inputs** no declared parameters.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** relativedelta(minutes = cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “mins\_between\_operations”))).

**Local steps**

- Return relativedelta(minutes = cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “mins\_between\_operations”))).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “mins\_between\_operations”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L532)

<a id="op-9613af6d53373f"></a>
### Get capacity planning days

`operation_enterprise_binding_enterprise_manufacturing_doctype_manufacturing_settings_manufacturing_settings_get_capacity_planning_days`

**Inputs** no declared parameters.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** (cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “capacity\_planning\_for\_days”)) or DEFAULT\_CAPACITY\_PLANNING\_DAYS).

**Local steps**

- Return (cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “capacity\_planning\_for\_days”)) or DEFAULT\_CAPACITY\_PLANNING\_DAYS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “capacity\_planning\_for\_days”)) → DEFAULT\_CAPACITY\_PLANNING\_DAYS.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “capacity\_planning\_for\_days”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L879)

<a id="op-37374dc7b5af04"></a>
### Is material consumption enabled

`operation_enterprise_manufacturing_record_definitions_manufacturing_settings_business_behavior_is_material_consumption_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** Platform.local.material\_consumption.

**Local steps**

- If not hasattr(Platform.local, “material\_consumption”).
  - Set Platform.local.material\_consumption from cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “material\_consumption”)).
- Return Platform.local.material\_consumption.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “material\_consumption”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0484.json#L7705) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L533)

## Record · Master production schedule

[Record definition](../../../../data/record-types/master_production_schedule.json)

<a id="op-3b485854bbcc05"></a>
### Master Production Schedule.get actual demand

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_actual_demand`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** list().

**Local steps**

- Evaluate self.set(“items”, list()).
- Set actual\_demand\_data from self.get\_demand\_data().
- Set item\_wise\_data from self.get\_item\_wise\_mps\_data(actual\_demand\_data).
- If not item\_wise\_data.
  - Return list().
- Evaluate self.update\_item\_details(item\_wise\_data).
- Evaluate self.add\_mps\_data(item\_wise\_data).
- If not self.is\_new().
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get demand data](operations-025.md#op-3b09b40f8ebca5), [get item wise mps data](operations-026.md#op-59607021ee8fb7), [update item details](operations-025.md#op-28269b4ddafb1d), [add mps data](operations-026.md#op-9b86be180ee0f4).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L541)

<a id="op-42345db6d179f3"></a>
### Master Production Schedule.validate

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_to\_date().
- Evaluate self.validate\_company().
- Evaluate self.validate\_sales\_forecast\_not\_used().
- Evaluate self.validate\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set to date](operations-025.md#op-75efc0aa978d80), [validate company](operations-025.md#op-07e740b54184a4), [validate sales forecast not used](operations-025.md#op-4b8706537f783c), [validate items](operations-025.md#op-9813971c92eda2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L558)

<a id="op-9813971c92eda2"></a>
### Master Production Schedule.validate items

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_validate_items`

**Inputs** self.

**Local steps**

- For each tuple(item\_code, uom) in set of tuple(row.item\_code, row.uom) for row drawn from self.items where (row.item\_code and row.uom).
  - Draw row from self.items, keep a combination only if ((row.item\_code and row.uom)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → row.uom.
  - Evaluate get\_conversion\_factor(item\_code, uom, throw\_if\_missing = true).
- For each tuple(item\_code, bom\_no) in set of tuple(row.item\_code, row.bom\_no) for row drawn from self.items where row.bom\_no.
  - Draw row from self.items, keep a combination only if (row.bom\_no).
  - Evaluate validate\_production\_bom(item\_code, bom\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L891)

<a id="op-4b8706537f783c"></a>
### Master Production Schedule.validate sales forecast not used

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_validate_sales_forecast_not_used`

**Inputs** self.

**Record and data access** read “Sales Forecast” via get\_value · read “Master Production Schedule” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Sales Forecast {0} already has Master Production Schedule {1}”.format(bold(self.sales\_forecast), get\_link\_to\_form(“Master Production Schedule”, existing)).

**Local steps**

- If not self.sales\_forecast.
  - Return no value.
- Evaluate Platform.db.get\_value(“Sales Forecast”, self.sales\_forecast, “name”, for\_update = true).
- Set existing from Platform.db.get\_value(“Master Production Schedule”, mapping(“sales\_forecast” → self.sales\_forecast, “name” → tuple(“!=”, (self.name or empty text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- If existing.
  - Call the validation error handler Platform.throw(translated “Sales Forecast {0} already has Master Production Schedule {1}”.format(bold(self.sales\_forecast), get\_link\_to\_form(“Master Production Schedule”, existing))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L892)

<a id="op-07e740b54184a4"></a>
### Master Production Schedule.validate company

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_validate_company`

**Inputs** self.

**Record and data access** read “Sales Forecast” via get\_value.

**Explicit failure paths** validation helper — translated “The Company {0} of Sales Forecast {1} does not match with the Company {2} of Master Production Schedule {3}.”.format(bold(sales\_forecast\_company), bold(self.sales\_forecast), bold(self.company), ….

**Local steps**

- If self.sales\_forecast.
  - Set sales\_forecast\_company from Platform.db.get\_value(“Sales Forecast”, self.sales\_forecast, “company”).
  - If sales\_forecast\_company differs from self.company.
    - Call the validation error handler Platform.throw(translated “The Company {0} of Sales Forecast {1} does not match with the Company {2} of Master Production Schedule {3}.”.format(bold(sales\_forecast\_company), bold(self.sales\_forecast), bold ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L330) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L559)

<a id="op-75efc0aa978d80"></a>
### Master Production Schedule.set to date

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_set_to_date`

**Inputs** self.

**Local steps**

- Set dates from list of row.delivery\_date for row drawn from self.items where row.delivery\_date.
  - Draw row from self.items, keep a combination only if (row.delivery\_date).
- If self.to\_date.
  - Evaluate dates.append(self.to\_date).
- Otherwise.
  - Evaluate dates.extend(self.get\_sales\_forecast\_data()).
- If dates.
  - Set self.to\_date from max(generator of getdate(date) for date drawn from dates).
    - Draw date from dates.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales forecast data](operations-025.md#op-03171eaeb3d426).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L556)

<a id="op-03171eaeb3d426"></a>
### Master Production Schedule.get sales forecast data

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_sales_forecast_data`

**Inputs** self.

**Record and data access** read “Sales Forecast Item” via get\_all.

**Explicit results** list() · Platform.get\_all(“Sales Forecast Item”, filters = filters, pluck = “delivery\_date”, order\_by = “delivery\_date asc”).

**Local steps**

- If not self.sales\_forecast.
  - Return list().
- Set filters from mapping(“parent” → self.sales\_forecast).
- If self.select\_items.
  - Set items from list of d.item\_code for d drawn from self.select\_items where d.item\_code.
    - Draw d from self.select\_items, keep a combination only if (d.item\_code).
  - Set filters at “item\_code” from tuple(“in”, items).
- Return Platform.get\_all(“Sales Forecast Item”, filters = filters, pluck = “delivery\_date”, order\_by = “delivery\_date asc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L881) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L551)

<a id="op-28269b4ddafb1d"></a>
### Master Production Schedule.update item details

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_update_item_details`

**Inputs** self, data.

**Local steps**

- Set items from list of item at 0 for item drawn from data where item at 0.
  - Draw item from data, keep a combination only if (item at 0).
- Set item\_details from self.get\_item\_details(items).
- Evaluate self.load\_lead\_times(list of tuple(row.item\_code, row.bom\_no) for row drawn from item\_details.values()).
  - Draw row from item\_details.values().
- For each key in data.
  - Set item\_data from data at key.
  - Set item\_code from key at 0.
  - If item\_code belongs to item\_details.
    - Evaluate item\_data.update(item\_details at item\_code).
    - Set item\_data.cumulative\_lead\_time from self.get\_cumulative\_lead\_time(item\_code, item\_data.bom\_no, flt(item\_data.qty)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item details](operations-025.md#op-cf6a9f8c2ce736), [load lead times](operations-025.md#op-31a288a8897044), [get cumulative lead time](operations-025.md#op-0e3223effceeab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L557)

<a id="op-cf6a9f8c2ce736"></a>
### Master Production Schedule.get item details

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_item_details`

**Inputs** self, items.

**Explicit results** Platform.\_dict(mapping of row.item\_code → row for row drawn from query.run(as\_dict = true)).

**Local steps**

- Set doctype from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(doctype).select(doctype.name.as\_(“item\_code”), doctype.default\_bom.as\_(“bom\_no”), doctype.item\_name).where(doctype.name.isin(items)).
- Return Platform.\_dict(mapping of row.item\_code → row for row drawn from query.run(as\_dict = true)).
  - Draw row from query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L545)

<a id="op-31a288a8897044"></a>
### Master Production Schedule.load lead times

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_load_lead_times`

**Inputs** self, roots.

**Record and data access** read “Item Lead Time” via get\_all.

**Local steps**

- Set self.\_bom\_materials from mapping().
- Set tuple(items, visited, stack) from tuple(set(), set(), list(roots)).
- While stack.
  - Set tuple(item\_code, bom\_no) from stack.pop().
  - Evaluate items.add(item\_code).
  - If (bom\_no and bom\_no does not belong to visited).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bom\_no → bom\_no does not belong to visited.
    - Evaluate visited.add(bom\_no).
    - Evaluate stack.extend(generator of tuple(row.item\_code, row.bom\_no) for row drawn from self.get\_bom\_materials(bom\_no)).
      - Draw row from self.get\_bom\_materials(bom\_no).
- Set self.\_lead\_times from mapping of row.item\_code → row for row drawn from Platform.get\_all(“Item Lead Time”, filters = mapping(“item\_code” → tuple(“in”, (list(items) or list(empty text)))), fields = list(“item\_code”, “capacity\_pe ….
  - Draw row from Platform.get\_all(“Item Lead Time”, filters = mapping(“item\_code” → tuple(“in”, (list(items) or list(empty text)))), fields = list(“item\_code”, “capacity\_per\_day”, “manufacturing\_time\_in\_mins”, “no\_of\_shift”, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list(items) → list(empty text).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bom materials](operations-025.md#op-647b27cd75fe12).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L889)

<a id="op-647b27cd75fe12"></a>
### Master Production Schedule.get bom materials

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_get_bom_materials`

**Inputs** self, bom\_no.

**Explicit results** self.\_bom\_materials at bom\_no.

**Local steps**

- If bom\_no does not belong to self.\_bom\_materials.
  - Set bom from Platform.qb.DocType(“BOM”).
  - Set bom\_item from Platform.qb.DocType(“BOM Item”).
  - Set self.\_bom\_materials at bom\_no from nested operand in the contract(nested operand in the contract).select(bom\_item.item\_code, bom\_item.bom\_no, nested operand in the contract.as\_(“qty\_per\_unit”)).where(((nested operand in the contract.parent  ….
- Return self.\_bom\_materials at bom\_no.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L887)

<a id="op-0e3223effceeab"></a>
### Master Production Schedule.get cumulative lead time

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_cumulative_lead_time`

**Inputs** self, item\_code, bom\_no, qty.

**Explicit results** own\_time · (own\_time + max(component\_times, default = 0)).

**Local steps**

- Set own\_time from get\_own\_lead\_time(self.\_lead\_times.get(item\_code), qty, bool(bom\_no)).
- If not bom\_no.
  - Return own\_time.
- Set component\_times from list of self.get\_cumulative\_lead\_time(row.item\_code, row.bom\_no, (qty × flt(row.qty\_per\_unit))) for row drawn from self.get\_bom\_materials(bom\_no).
  - Draw row from self.get\_bom\_materials(bom\_no).
- Return (own\_time + max(component\_times, default = 0)).

**Methods declared on this owner** [get bom materials](operations-025.md#op-647b27cd75fe12).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L542)

<a id="op-3b09b40f8ebca5"></a>
### Master Production Schedule.get demand data

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_demand_data`

**Inputs** self.

**Explicit results** (sales\_order\_data + material\_request\_data).

**Local steps**

- Set sales\_order\_data from self.get\_sales\_orders\_data().
- Set material\_request\_data from self.get\_material\_requests\_data().
- Return (sales\_order\_data + material\_request\_data).

**Methods declared on this owner** [get sales orders data](operations-025.md#op-56c0f8e96fd691), [get material requests data](operations-025.md#op-7169f4d28d0aa2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0485.json#L2109) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L543)

<a id="op-7169f4d28d0aa2"></a>
### Master Production Schedule.get material requests data

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_material_remote_requests_data`

**Inputs** self.

**Explicit results** list() · self.filter\_selected\_items(query, doctype).run(as\_dict = true).

**Local steps**

- Set material\_requests from list of m.material\_request for m drawn from self.material\_requests where m.material\_request.
  - Draw m from self.material\_requests, keep a combination only if (m.material\_request).
- If not material\_requests.
  - Return list().
- Set doctype from Platform.qb.DocType(“Material Request Item”).
- Set parent from Platform.qb.DocType(“Material Request”).
- Set pending\_qty from (doctype.stock\_qty − IfNull(doctype.ordered\_qty, 0)).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.item\_code, doctype.warehouse, doctype.stock\_uom, nested operand in the contract.as\_(“delivery\_date”), …).where(((((nested opera ….
- If self.from\_date.
  - Set query from query.where(doctype.schedule\_date ≥ self.from\_date).
- If self.to\_date.
  - Set query from query.where(doctype.schedule\_date ≤ self.to\_date).
- Return self.filter\_selected\_items(query, doctype).run(as\_dict = true).

**Methods declared on this owner** [filter selected items](operations-025.md#op-b5c023838e6388).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L550)

<a id="op-b5c023838e6388"></a>
### Master Production Schedule.filter selected items

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_filter_selected_items`

**Inputs** self, query, doctype.

**Explicit results** query.

**Local steps**

- If items bound to self.get\_items\_for\_mps().
  - Set query from query.where(doctype.item\_code.isin(items)).
- Return query.

**Methods declared on this owner** [get items for mps](operations-026.md#op-b27eb3cf9b15ac).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L886)

<a id="op-56c0f8e96fd691"></a>
### Master Production Schedule.get sales orders data

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_sales_orders_data`

**Inputs** self.

**Explicit results** (self.get\_items\_from\_sales\_orders(scheduled\_rows) + sales\_order\_schedules).

**Local steps**

- Set schedules from self.get\_sales\_order\_schedules().
- Set scheduled\_rows from list(set of row.sales\_order\_item for row drawn from schedules where row.sales\_order\_item).
  - Draw row from schedules, keep a combination only if (row.sales\_order\_item).
- Set sales\_order\_schedules from list of row for row drawn from deduct\_delivered\_qty(schedules) where self.is\_in\_date\_range(row.delivery\_date).
  - Draw row from deduct\_delivered\_qty(schedules), keep a combination only if (self.is\_in\_date\_range(row.delivery\_date)).
- Return (self.get\_items\_from\_sales\_orders(scheduled\_rows) + sales\_order\_schedules).

**Methods declared on this owner** [get sales order schedules](operations-025.md#op-06de2d61ae700a), [is in date range](operations-025.md#op-4f4b4706229474), [get items from sales orders](operations-025.md#op-6876ef4f146da7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L554)

<a id="op-6876ef4f146da7"></a>
### Master Production Schedule.get items from sales orders

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_items_from_sales_orders`

**Inputs** self, ignore\_orders = no value.

**Explicit results** list() · self.filter\_selected\_items(query, doctype).run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Sales Order Item”).
- Set parent from Platform.qb.DocType(“Sales Order”).
- Set pending\_qty from ((doctype.qty − IfNull(doctype.delivered\_qty, 0)) × doctype.conversion\_factor).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.item\_code, doctype.warehouse, doctype.stock\_uom, doctype.delivery\_date, …).where((((nested operand in the contract equals neste ….
- If self.from\_date.
  - Set query from query.where(doctype.delivery\_date ≥ self.from\_date).
- If self.to\_date.
  - Set query from query.where(doctype.delivery\_date ≤ self.to\_date).
- If self.sales\_orders.
  - Set names from list of s.sales\_order for s drawn from self.sales\_orders where s.sales\_order.
    - Draw s from self.sales\_orders, keep a combination only if (s.sales\_order).
  - If not names.
    - Return list().
  - Set query from query.where(doctype.parent.isin(names)).
- If ignore\_orders.
  - Set query from query.where(doctype.name.notin(ignore\_orders)).
- Return self.filter\_selected\_items(query, doctype).run(as\_dict = true).

**Methods declared on this owner** [filter selected items](operations-025.md#op-b5c023838e6388).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L548)

<a id="op-06de2d61ae700a"></a>
### Master Production Schedule.get sales order schedules

`operation_enterprise_manufacturing_record_definitions_master_production_schedule_business_behavior_master_production_schedule_get_sales_order_schedules`

**Inputs** self.

**Explicit results** self.filter\_selected\_items(query, doctype).run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Delivery Schedule Item”).
- Set parent from Platform.qb.DocType(“Sales Order”).
- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If self.sales\_orders.
  - Set names from list of s.sales\_order for s drawn from self.sales\_orders where s.sales\_order.
    - Draw s from self.sales\_orders, keep a combination only if (s.sales\_order).
  - Set query from query.where(doctype.sales\_order.isin(names)).
- Return self.filter\_selected\_items(query, doctype).run(as\_dict = true).

**Methods declared on this owner** [filter selected items](operations-025.md#op-b5c023838e6388).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L552)

<a id="op-4f4b4706229474"></a>
### Master Production Schedule.is in date range

`operation_enterprise_binding_enterprise_manufacturing_doctype_master_production_schedule_master_production_schedule_masterproductionschedule_is_in_date_range`

**Inputs** self, delivery\_date.

**Explicit results** false · not (self.to\_date and getdate(delivery\_date) &gt; getdate(self.to\_date)).

**Local steps**

- If (self.from\_date and getdate(delivery\_date) &lt; getdate(self.from\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → getdate(delivery\_date) &lt; getdate(self.from\_date).
  - Return false.
- Return not (self.to\_date and getdate(delivery\_date) &gt; getdate(self.to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.to\_date → getdate(delivery\_date) &gt; getdate(self.to\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L888)
