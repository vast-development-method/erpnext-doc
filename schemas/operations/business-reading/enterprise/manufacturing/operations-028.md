# Production · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Material requirements planning report

<a id="op-d705395a0498e2"></a>
### Material Requirements Planning Report.update rm details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_update_raw_material_details`

**Inputs** self, raw\_materials, delivery\_date, planned\_qty, bom\_no, data.

**Local steps**

- For each material in raw\_materials.
  - Set row from Platform.\_dict(mapping(“item\_code” → material.item\_code, “item\_name” → material.item\_name, “default\_warehouse” → material.default\_warehouse, “default\_supplier” → material.default\_supplier, …)).
  - Set row.capacity from 0.
  - Set row.type\_of\_material from get\_type\_of\_material(material.get(“is\_purchase\_item”), material.bom\_no).
  - If material.raw\_materials.
    - Set row.capacity from get\_item\_capacity(material.item\_code, self.filters.bucket\_size).
  - Evaluate self.update\_required\_qty(row).
  - Evaluate self.set\_lead\_time(row).
  - Evaluate data.append(row).
  - If material.raw\_materials.
    - Evaluate self.update\_rm\_details(material.raw\_materials, row.release\_date, row.required\_qty, material.bom\_no, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update required qty](operations-027.md#op-7a54863a60e811), [set lead time](operations-027.md#op-dfe7d81510b786).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1149)

<a id="op-2adea26878c589"></a>
### Material Requirements Planning Report.get mps data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_master_production_schedule_data`

**Inputs** self.

**Explicit results** rows.

**Local steps**

- Set doctype from Platform.qb.DocType(“Master Production Schedule”).
- Set child\_doctype from Platform.qb.DocType(“Master Production Schedule Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(child\_doctype.item\_code, child\_doctype.delivery\_date, doctype.parent\_warehouse, child\_doctype.name, …).where(child\_doctype.parentfield  ….
- If self.filters.get(“from\_date”).
  - Set query from query.where(child\_doctype.delivery\_date ≥ self.filters.from\_date).
- If self.filters.get(“to\_date”).
  - Set query from query.where(child\_doctype.delivery\_date ≤ self.filters.to\_date).
- Set fields from mapping(“parent\_warehouse” → self.filters.get(“warehouse”), “name” → self.filters.get(“mps”), “item\_code” → self.filters.get(“item\_code”)).
- For each tuple(field, value) in fields.items().
  - If not value.
    - Continue with the next iteration or loop test.
  - If field equals “item\_code”.
    - Set query from query.where(child\_doctype at field equals value).
  - Otherwise.
    - Set query from query.where(doctype at field equals value).
- Set rows from query.run(as\_dict = true).
- For each row in rows.
  - Update row.planned\_qty using × get\_uom\_conversion\_factor(row.item\_code, row.uom).
- Return rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1136)

<a id="op-ebf8db9b5cf280"></a>
### Material Requirements Planning Report.get items from mps

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_items_from_master_production_schedule`

**Inputs** self, mps\_data.

**Record and data access** read “Master Production Schedule” via get\_all · read “Sales Forecast Item” via get\_all.

**Explicit results** items.

**Local steps**

- Set items from list().
- For each row in mps\_data.
  - If row.item\_code does not belong to items.
    - Evaluate items.append(row.item\_code).
- If self.filters.mps.
  - Set sales\_forecasts from Platform.get\_all(“Master Production Schedule”, filters = mapping(“name” → self.filters.mps), pluck = “sales\_forecast”).
  - If sales\_forecasts.
    - Set sales\_forecast\_items from Platform.get\_all(“Sales Forecast Item”, filters = mapping(“parent” → tuple(“in”, sales\_forecasts)), pluck = “item\_code”).
    - If sales\_forecast\_items.
      - Evaluate items.extend(sales\_forecast\_items).
- Return items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0549.json#L5349) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1134)

<a id="op-03f4bdbf05e57f"></a>
### Material Requirements Planning Report.get raw materials data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_raw_materials_data`

**Inputs** self, items.

**Record and data access** read “Item” via get\_value.

**Explicit results** item\_wise\_rm\_details.

**Local steps**

- Set item\_wise\_rm\_details from Platform.\_dict().
- For each item\_code in items.
  - If item\_code does not belong to item\_wise\_rm\_details.
    - Set item\_wise\_rm\_details at item\_code from Platform.db.get\_value(“Item”, item\_code, list(“default\_bom as bom\_no”, “safety\_stock”, “min\_order\_qty”, “purchase\_uom”, …), as\_dict = true).
  - Set item\_data from item\_wise\_rm\_details at item\_code.
  - If details bound to get\_item\_details(item\_code, self.filters.get(“company”)).
    - Evaluate item\_data.update(details).
  - If item\_code does not belong to self.fg\_items.
    - Evaluate self.fg\_items.append(item\_code).
  - If item\_data.bom\_no.
    - Set item\_data.raw\_materials from self.get\_raw\_materials(item\_data.bom\_no, indent = 0).
- For each row in self.mps\_data.
  - Set key from tuple(row.item\_code, row.get(“bom\_no”)).
  - If (not row.get(“bom\_no”) or key belongs to item\_wise\_rm\_details).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.get(“bom\_no”) → key belongs to item\_wise\_rm\_details.
    - Continue with the next iteration or loop test.
  - Set item\_data from item\_wise\_rm\_details at row.item\_code.
  - If row.bom\_no differs from item\_data.bom\_no.
    - Set item\_wise\_rm\_details at key from Platform.\_dict(item\_data, bom\_no = row.bom\_no, raw\_materials = self.get\_raw\_materials(row.bom\_no)).
- Return item\_wise\_rm\_details.

**Methods declared on this owner** [get raw materials](operations-028.md#op-c0863f145963d1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1142)

<a id="op-c0863f145963d1"></a>
### Material Requirements Planning Report.get raw materials

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_raw_materials`

**Inputs** self, bom\_no, indent = 0.

**Record and data access** read “BOM” via get\_all.

**Explicit results** raw\_materials.

**Local steps**

- Set company from self.filters.get(“company”).
- Set raw\_materials from Platform.get\_all(“BOM”, filters = list(list(“BOM Item”, “parent”, “=”, bom\_no), list(“BOM”, “docstatus”, “=”, 1)), fields = list(“′tabBOM Item′.′item\_code′”, “′tabBOM Item′.′stock\_qty′”, “′tabBOM′.quantity ….
- For each material in raw\_materials.
  - Set material.indent from indent.
  - Set material.qty from flt((material.stock\_qty ÷ material.parent\_qty)).
  - If details bound to get\_item\_details(material.item\_code, company).
    - Evaluate material.update(details).
  - If material.item\_code does not belong to self.rm\_items.
    - Evaluate self.rm\_items.append(material.item\_code).
  - If material.bom\_no.
    - Set material.raw\_materials from self.get\_raw\_materials(material.bom\_no, (indent + 1)).
- Return raw\_materials.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1141)

<a id="op-3b81038a215cce"></a>
### Material Requirements Planning Report.get columns

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_columns`

**Inputs** self.

**Explicit results** columns.

**Local steps**

- If self.filters.show\_in\_bucket\_view.
  - Set columns from list(mapping(“fieldname” → “item\_code”, “label” → translated “Item Code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “item\_name”, “label” → translated “Item Name”, “fieldtype” → “Data”)).
  - Set label from (((translated “Capacity” + “ (”) + translated self.filters.bucket\_size) + “)”).
  - Evaluate columns.append(mapping(“fieldname” → “capacity”, “label” → translated label, “fieldtype” → “Int”)).
  - For each date in self.dates.
    - Evaluate columns.append(mapping(“fieldname” → date at “from\_date”, “label” → date at “label”, “fieldtype” → “Float”, “width” → 135)).
  - Return columns.
- Set columns from list(mapping(“fieldname” → “item\_code”, “label” → translated “Item Code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “item\_name”, “label” → translated “Item Name”, “fieldtype” → “D ….
- Update columns using + list(mapping(“fieldname” → “demand\_qty”, “label” → translated “Demand Qty”, “fieldtype” → “Float”, “width” → 120), mapping(“fieldname” → “adhoc\_qty”, “label” → translated “Ad-hoc Qty”, “fieldtype” → “Float ….
- Update columns using + list(mapping(“fieldname” → “planned\_qty”, “label” → translated “Planned Qty”, “fieldtype” → “Float”, “width” → 120), mapping(“fieldname” → “in\_hand\_qty”, “label” → translated “On Hand”, “fieldtype” → “Floa ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0550.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1127)

<a id="op-23b5a7d0e99e41"></a>
### Material Requirements Planning Report.get dates

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_dates`

**Inputs** self.

**Explicit results** dates\_list.

**Local steps**

- Set bucket\_size from self.filters.bucket\_size.
- Set from\_date from self.filters.from\_date.
- If bucket\_size equals “Weekly”.
  - Set from\_date from self.get\_first\_date\_of\_week(from\_date).
- Otherwise.
  - If bucket\_size equals “Monthly”.
    - Set from\_date from get\_first\_day(from\_date).
- Set dates\_list from list().
- While getdate(from\_date) ≤ getdate(self.filters.to\_date).
  - Set args from mapping(“from\_date” → from\_date).
  - Set days from 1 when bucket\_size equals “Daily”, otherwise 7.
    - Value choice on bucket\_size equals “Daily” — true gives 1, false gives 7.
  - If bucket\_size equals “Monthly”.
    - Set from\_date from add\_months(from\_date, 1).
  - Otherwise.
    - Set from\_date from add\_days(from\_date, days).
  - Set args at “to\_date” from add\_days(from\_date, negative 1).
  - If bucket\_size equals “Monthly”.
    - Set args at “label” from formatdate(args at “from\_date”, “MMM YYYY”).
  - Otherwise.
    - If bucket\_size equals “Weekly”.
      - Set args at “label” from ((formatdate(args at “from\_date”, “dd MMM”) + “ - ”) + formatdate(args at “to\_date”, “dd MMM”)).
    - Otherwise.
      - Set args at “label” from formatdate(args at “to\_date”, “dd MMM”).
  - Evaluate dates\_list.append(args).
- Return dates\_list.

**Methods declared on this owner** [get first date of week](operations-028.md#op-21340cb4eaeeff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1128)

<a id="op-21340cb4eaeeff"></a>
### Material Requirements Planning Report.get first date of week

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_first_date_of_week`

**Inputs** self, input\_date.

**Explicit results** start\_of\_week.strftime(“%Y-%m-%d”).

**Local steps**

- If isinstance(input\_date, str).
  - Set input\_date from datetime.strptime(input\_date, “%Y-%m-%d”).
- Set start\_of\_week from (input\_date − timedelta(days = input\_date.weekday())).
- Return start\_of\_week.strftime(“%Y-%m-%d”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0550.json#L2691) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1132)

<a id="op-b88db9125241ca"></a>
### Material Requirements Planning Report.get last date of week

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_last_date_of_week`

**Inputs** self, input\_date.

**Explicit results** end\_of\_week.strftime(“%Y-%m-%d”).

**Local steps**

- If isinstance(input\_date, str).
  - Set input\_date from datetime.strptime(input\_date, “%Y-%m-%d”).
- Set end\_of\_week from (input\_date + timedelta(days = (6 − input\_date.weekday()))).
- Return end\_of\_week.strftime(“%Y-%m-%d”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0550.json#L2860) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1135)

<a id="op-adb3bf8e6e8309"></a>
### Material Requirements Planning Report.get sales forecast data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_sales_forecast_data`

**Inputs** self.

**Record and data access** read “Master Production Schedule” via get\_value · read “Warehouse” via get\_value.

**Explicit results** convert\_to\_daily\_bucket\_data(sales\_data).

**Local steps**

- Set forecast\_doc from Platform.qb.DocType(“Sales Forecast”).
- Set doctype from Platform.qb.DocType(“Sales Forecast Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(forecast\_doc.frequency, doctype.item\_code, doctype.delivery\_date, nested operand in the contract.as\_(“sales\_forecast”), …).where((forec ….
- If self.filters.mps.
  - Set forecast from Platform.db.get\_value(“Master Production Schedule”, self.filters.mps, “sales\_forecast”).
  - Set query from query.where(forecast\_doc.name equals forecast).
- If self.filters.from\_date.
  - Set query from query.where(doctype.delivery\_date ≥ self.filters.from\_date).
- If self.filters.to\_date.
  - Set query from query.where(doctype.delivery\_date ≤ self.filters.to\_date).
- If self.filters.warehouse.
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
    - Evaluate warehouses.append(self.filters.get(“warehouse”)).
  - Set query from query.where(forecast\_doc.parent\_warehouse.isin(warehouses)).
- If self.filters.item\_code.
  - Set query from query.where(doctype.item\_code equals self.filters.item\_code).
- Set sales\_data from query.run(as\_dict = true).
- Return convert\_to\_daily\_bucket\_data(sales\_data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0550.json#L3037) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1143)

<a id="op-824ddf9fefcb45"></a>
### Get stock reserved for work orders

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_stock_reserved_for_work_orders`

**Inputs** items, warehouses = no value.

**Explicit results** overlap.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sre.item\_code, sre.warehouse, Sum((nested operand in the contract − nested operand in the contract))).where((((nested operand in the co ….
- If warehouses.
  - Set query from query.where(sre.warehouse.isin(warehouses)).
- Set reserved\_for\_production from get\_reserved\_for\_production\_by\_warehouse(items, warehouses).
- Set overlap from mapping().
- For each tuple(item\_code, warehouse, qty) in query.run().
  - Set counted from min(flt(qty), reserved\_for\_production.get(tuple(item\_code, warehouse), 0.0)).
  - Set overlap at item\_code from (overlap.get(item\_code, 0.0) + max(counted, 0.0)).
- Return overlap.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1137)

<a id="op-ebe1066cfba77a"></a>
### Get reserved for production by warehouse

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_reserved_for_production_by_warehouse`

**Inputs** items, warehouses = no value.

**Record and data access** read “Bin” via get\_all.

**Explicit results** mapping of tuple(row.item\_code, row.warehouse) → flt(row.reserved\_qty\_for\_production) for row drawn from Platform.get\_all(“Bin”, filters = filters, fields = list(“item\_code”, “warehouse”, “reserved\_qty\_for ….

**Local steps**

- Set filters from mapping(“item\_code” → tuple(“in”, items)).
- If warehouses.
  - Set filters at “warehouse” from tuple(“in”, warehouses).
- Return mapping of tuple(row.item\_code, row.warehouse) → flt(row.reserved\_qty\_for\_production) for row drawn from Platform.get\_all(“Bin”, filters = filters, fields = list(“item\_code”, “warehouse”, “reserved\_qty\_for ….
  - Draw row from Platform.get\_all(“Bin”, filters = filters, fields = list(“item\_code”, “warehouse”, “reserved\_qty\_for\_production”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1136)

<a id="op-f2b77a91d74c54"></a>
### Apply dated supply

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_apply_dated_supply`

**Inputs** row, supply\_details.

**Explicit results** supplied\_qty.

**Local steps**

- Set supplied\_qty from 0.0.
- If (row.required\_qty ≤ 0 or not supply\_details).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.required\_qty ≤ 0 → not supply\_details.
  - Return supplied\_qty.
- Set keys from list of key for key drawn from supply\_details where key at 0 equals row.item\_code.
  - Draw key from supply\_details, keep a combination only if (key at 0 equals row.item\_code).
- For each key in sorted(keys, key = deferred anonymous expression).
  - Set covered\_qty from cover\_demand(row, flt(supply\_details at key.qty), getdate(key at 1)).
  - Update supplied\_qty using + covered\_qty.
  - Set supply\_details at key.qty from (flt(supply\_details at key.qty) − covered\_qty).
  - If supply\_details at key.qty ≤ 0.
    - Remove supply\_details at key.
  - <a id="op-f2b77a91d74c54-guard-14"></a>If row.required\_qty ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return supplied\_qty.

**Derived branch illustrations**

- At the comparison row.required\_qty ≤ 0, row.required\_qty = 0 selects the branch that exits the enclosing loop. With row.required\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f2b77a91d74c54-guard-14)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1131)

<a id="op-a8778f15955cc8"></a>
### Cover demand

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_cover_demand`

**Inputs** row, qty, supply\_date = no value.

**Explicit results** covered\_qty.

**Local steps**

- Set covered\_qty from 0.0.
- For each part in row.demand\_parts.
  - <a id="op-a8778f15955cc8-guard-4"></a>If qty ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If (part at 1 ≤ 0 or (supply\_date and part at 0 &lt; supply\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in part at 1 ≤ 0 → (supply\_date and part at 0 &lt; supply\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in supply\_date → part at 0 &lt; supply\_date.
    - Continue with the next iteration or loop test.
  - Set covered from min(part at 1, qty).
  - Update part at 1 using − covered.
  - Update qty using − covered.
  - Update covered\_qty using + covered.
- Set row.required\_qty from (flt(row.required\_qty) − covered\_qty).
- Return covered\_qty.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a8778f15955cc8-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1132)

<a id="op-16b47cb72da19e"></a>
### Get free stock

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_free_stock`

**Inputs** bin\_details.

**Explicit results** (flt(bin\_details.get(“actual\_qty”)) − sum(generator of flt(bin\_details.get(field)) for field drawn from tuple(“reserved\_stock”, “reserved\_qty\_for\_production”, “reserved\_qty\_for\_sub\_contract”, “reserved\_qty ….

**Local steps**

- Return (flt(bin\_details.get(“actual\_qty”)) − sum(generator of flt(bin\_details.get(field)) for field drawn from tuple(“reserved\_stock”, “reserved\_qty\_for\_production”, “reserved\_qty\_for\_sub\_contract”, “reserved\_qty ….
  - Draw field from tuple(“reserved\_stock”, “reserved\_qty\_for\_production”, “reserved\_qty\_for\_sub\_contract”, “reserved\_qty\_for\_production\_plan”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1133)

<a id="op-3ff65f20578fab"></a>
### Get type of material

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_type_of_material`

**Inputs** is\_purchase\_item, bom\_no.

**Explicit results** “Purchase” when (is\_purchase\_item and not bom\_no), otherwise “Manufacture”.

**Local steps**

- Return “Purchase” when (is\_purchase\_item and not bom\_no), otherwise “Manufacture”.
  - Value choice on (is\_purchase\_item and not bom\_no) — true gives “Purchase”, false gives “Manufacture”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_purchase\_item → not bom\_no.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1138)

<a id="op-9465a78e45021f"></a>
### Get item details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_get_item_details`

**Inputs** item\_code, company.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Item” via get\_value · read “Item Default” via get\_value.

**Explicit results** data.

**Local steps**

- Set data from (Platform.db.get\_value(“Item”, item\_code, list(“safety\_stock”, “min\_order\_qty”, “purchase\_uom”, “is\_purchase\_item”), as\_dict = true) or Platform.\_dict(mapping(“safety\_stock” → 0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Item”, item\_code, list(“safety\_stock”, “min\_order\_qty”, “purchase\_uom”, “is\_purchase\_item”), as\_dict = true) → Platform.\_dict(mapping(“safety\_stock” → 0)).
- Set default\_data from Platform.db.get\_value(“Item Default”, mapping(“parent” → item\_code, “company” → company), list(“default\_warehouse”, “default\_supplier”), as\_dict = true).
- If default\_data.
  - Evaluate data.update(default\_data).
- If not data.get(“default\_supplier”).
  - Set item\_group from Platform.db.get\_value(“Item”, item\_code, “item\_group”).
  - Set data.default\_supplier from Platform.db.get\_value(“Item Default”, mapping(“parent” → item\_group, “company” → company), “default\_supplier”).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1110)

<a id="op-4074f5ef2ae2fc"></a>
### Get item lead time

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_get_item_lead_time`

**Inputs** item\_code, type\_of\_material, qty = 1.

**Explicit results** 0 · (time\_in\_days + flt(details.buffer\_time)).

**Local steps**

- Set details from get\_item\_lead\_time\_details(item\_code).
- If type\_of\_material equals “Manufacture”.
  - <a id="op-4074f5ef2ae2fc-guard-5"></a>If qty ≤ 0.
    - Return 0.
  - Set time\_in\_days from ((max(flt(details.manufacturing\_time\_in\_mins), 0) × qty) ÷ 1440.0).
- Otherwise.
  - If details.purchase\_time is identical to no value.
    - Return 0.
  - Set time\_in\_days from flt(details.purchase\_time).
- Return (time\_in\_days + flt(details.buffer\_time)).

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that returns 0. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4074f5ef2ae2fc-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1111)

<a id="op-6de9db6cd903ba"></a>
### Get item lead time details

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_item_lead_time_details`

**Inputs** item\_code.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Item Lead Time” via get\_value.

**Explicit results** (Platform.db.get\_value(“Item Lead Time”, mapping(“item\_code” → item\_code), list(“manufacturing\_time\_in\_mins”, “purchase\_time”, “buffer\_time”), as\_dict = true) or Platform.\_dict()).

**Local steps**

- Return (Platform.db.get\_value(“Item Lead Time”, mapping(“item\_code” → item\_code), list(“manufacturing\_time\_in\_mins”, “purchase\_time”, “buffer\_time”), as\_dict = true) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Item Lead Time”, mapping(“item\_code” → item\_code), list(“manufacturing\_time\_in\_mins”, “purchase\_time”, “buffer\_time”), as\_dict = true) → Platform.\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1134)

<a id="op-0d781923adbb5c"></a>
### Convert to daily bucket data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_convert_to_daily_bucket_data`

**Inputs** data.

**Explicit results** bucketed\_data.

**Local steps**

- Set bucketed\_data from list().
- For each row in data.
  - If row.frequency equals “Monthly”.
    - Set start\_date from get\_first\_day(row.delivery\_date).
    - Set no\_of\_days from days\_diff(add\_months(start\_date, 1), start\_date).
    - For each i in range(no\_of\_days).
      - Evaluate bucketed\_data.append(Platform.\_dict(mapping(“frequency” → “Daily”, “item\_code” → row.item\_code, “delivery\_date” → add\_days(start\_date, i), “sales\_forecast” → row.sales\_forecast, …))).
  - Otherwise.
    - If row.frequency equals “Weekly”.
      - Set start\_date from getdate(row.delivery\_date).
      - For each i in range(7).
        - Evaluate bucketed\_data.append(Platform.\_dict(mapping(“frequency” → “Daily”, “item\_code” → row.item\_code, “delivery\_date” → add\_days(start\_date, i), “sales\_forecast” → row.sales\_forecast, …))).
- Return bucketed\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0550.json#L4956) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1107)

<a id="op-7c0822df0f24f6"></a>
### Get item capacity

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_get_item_capacity`

**Inputs** item\_code, bucket\_size.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Item Lead Time” via get\_value.

**Explicit results** 0.0 · math.ceil((cint(capacity) × no\_of\_days)).

**Local steps**

- Set capacity from Platform.db.get\_value(“Item Lead Time”, mapping(“item\_code” → item\_code), “capacity\_per\_day”).
- If not capacity.
  - Return 0.0.
- Set no\_of\_days from 7 when bucket\_size equals “Weekly”, otherwise 30.
  - Value choice on bucket\_size equals “Weekly” — true gives 7, false gives 30.
- If bucket\_size equals “Daily”.
  - Set no\_of\_days from 1.
- Return math.ceil((cint(capacity) × no\_of\_days)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1109)

<a id="op-afc9492c330ccd"></a>
### Make order

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_make_order`

**Inputs** selected\_rows, company, warehouse = no value, mps = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via exists.

**State and service calls** msgprint with translated “Nothing to order, the selected rows are already covered by stock or existing orders” when covered\_rows, otherwise translated “Nothing to order from the selected rows”.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted to make Purchase Orders” · validation helper — translated “Company {0} does not exist”.format(company) · validation helper — translated “Default BOM for {0} not found”.format(“, ”.join(missing\_bom)) · validation helper — translated “Default Supplier for {0} not found”.format(“, ”.join(missing\_supplier)).

**Local steps**

- If not Platform.has\_permission(“Purchase Order”, “create”).
  - Call the validation error handler Platform.throw(translated “Not permitted to make Purchase Orders”, Platform.PermissionError).
- If isinstance(selected\_rows, str).
  - Set selected\_rows from parse\_json(selected\_rows).
- If not Platform.db.exists(“Company”, company).
  - Call the validation error handler Platform.throw(translated “Company {0} does not exist”.format(company)).
- Set qty\_precision from Platform.get\_precision(“Purchase Order Item”, “qty”).
- Set purchase\_orders from mapping().
- Set work\_orders from list().
- Set covered\_rows from 0.
- Set missing\_bom from list().
- Set missing\_supplier from list().
- For each row in selected\_rows.
  - Set row from Platform.\_dict(row).
  - If flt(row.required\_qty, qty\_precision) ≤ 0.
    - Update covered\_rows using + 1.
    - Continue with the next iteration or loop test.
  - If row.type\_of\_material equals “Purchase”.
    - If row.default\_supplier.
      - Evaluate purchase\_orders.setdefault(tuple(row.default\_supplier, row.release\_date), list()).append(row).
    - Otherwise.
      - If row.item\_code does not belong to missing\_supplier.
        - Evaluate missing\_supplier.append(row.item\_code).
  - If row.type\_of\_material equals “Manufacture”.
    - If row.bom\_no.
      - Evaluate work\_orders.append(row).
    - Otherwise.
      - If row.item\_code does not belong to missing\_bom.
        - Evaluate missing\_bom.append(row.item\_code).
- If missing\_bom.
  - Call the validation error handler Platform.throw(translated “Default BOM for {0} not found”.format(“, ”.join(missing\_bom))).
- If missing\_supplier.
  - Call the validation error handler Platform.throw(translated “Default Supplier for {0} not found”.format(“, ”.join(missing\_supplier))).
- If (not purchase\_orders and not work\_orders).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not purchase\_orders → not work\_orders.
  - Evaluate Platform.msgprint(translated “Nothing to order, the selected rows are already covered by stock or existing orders” when covered\_rows, otherwise translated “Nothing to order from the selected rows”).
    - Value choice on covered\_rows — true gives translated “Nothing to order, the selected rows are already covered by stock or existing orders”, false gives translated “Nothing to order from the selected rows”.
  - Return no value.
- If purchase\_orders.
  - Evaluate make\_purchase\_orders(purchase\_orders, company, warehouse = warehouse, mps = mps).
- If work\_orders.
  - Evaluate make\_work\_orders(work\_orders, company, warehouse = warehouse, mps = mps).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Order”, “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1114)

<a id="op-1e50ea9e2a92d6"></a>
### Make purchase orders

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_make_purchase_orders`

**Inputs** purchase\_orders, company, warehouse = no value, mps = no value.

**State and service calls** request new\_doc for “Purchase Order” · call insert on po · msgprint with translated “Purchase Order {0} created”.format(Platform.bold(po.name)).

**Local steps**

- For each tuple(tuple(supplier, release\_date), items) in purchase\_orders.items().
  - Set po\_items from list of get\_purchase\_order\_item(item, warehouse) for item drawn from items.
    - Draw item from items.
  - If not po\_items.
    - Continue with the next iteration or loop test.
  - Set po from Platform.new\_doc(“Purchase Order”).
  - Set po.supplier from supplier.
  - Set po.company from company.
  - Set po.mps from mps.
  - Set po.transaction\_date from release\_date.
  - Evaluate po.set(“items”, po\_items).
  - Evaluate po.run\_method(“set\_missing\_values”).
  - Evaluate po.insert().
  - Evaluate Platform.msgprint(translated “Purchase Order {0} created”.format(Platform.bold(po.name)), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from po.run\_method(“set\_missing\_values”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1115)

<a id="op-c837dd4263bcec"></a>
### Get purchase order item

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_get_purchase_order_item`

**Inputs** item, warehouse = no value.

**Explicit results** mapping(“item\_code” → item.item\_code, “qty” → qty, “uom” → uom, “conversion\_factor” → conversion\_factor, …).

**Local steps**

- Set uom from (item.purchase\_uom or item.uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.purchase\_uom → item.uom.
- If not uom.
  - Set uom\_details from get\_item\_uom(item.item\_code).
  - Set uom from (uom\_details.purchase\_uom or uom\_details.stock\_uom).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in uom\_details.purchase\_uom → uom\_details.stock\_uom.
- Set conversion\_factor from (flt(get\_conversion\_factor(item.item\_code, uom).get(“conversion\_factor”)) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(get\_conversion\_factor(item.item\_code, uom).get(“conversion\_factor”)) → 1.0.
- Set stock\_qty from max(flt(item.required\_qty), flt(item.min\_order\_qty)).
- Set qty from (stock\_qty ÷ conversion\_factor).
- If is\_whole\_number(uom).
  - Set qty from math.ceil(qty).
  - Set precision from Platform.get\_precision(“Purchase Order Item”, “stock\_qty”).
  - If flt((((qty − 1) × conversion\_factor) − stock\_qty), precision) ≥ 0.
    - Update qty using − 1.
- Return mapping(“item\_code” → item.item\_code, “qty” → qty, “uom” → uom, “conversion\_factor” → conversion\_factor, …).
  - Value choice on item.delivery\_date — true gives item.delivery\_date, false gives today().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → item.default\_warehouse.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1135)
