# Production · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Production analytics

<a id="op-e7bfaa1a95a825"></a>
### Get columns

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_get_columns`

**Inputs** period\_columns.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Status”, “fieldname” → “status”, “fieldtype” → “Data”, “width” → 140)).
- Evaluate columns.extend(period\_columns).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0552.json#L4506) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1179)

<a id="op-ad06944c4396a8"></a>
### Get work orders

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_get_work_orders`

**Inputs** filters.

**Explicit results** nested operand in the contract.qb.get\_query(“Work Order”, fields = list(“creation”, “actual\_end\_date”, “planned\_end\_date”, “status”), filters = mapping(“docstatus” → 1, “company” → nested operand in the co ….

**Local steps**

- Set from\_date from filters.get(“from\_date”).
- Set to\_date from get\_datetime(filters.get(“to\_date”)).replace(hour = 23, minute = 59, second = 59).
- Set WorkOrder from Platform.qb.DocType(“Work Order”).
- Return nested operand in the contract.qb.get\_query(“Work Order”, fields = list(“creation”, “actual\_end\_date”, “planned\_end\_date”, “status”), filters = mapping(“docstatus” → 1, “company” → nested operand in the co ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1182)

<a id="op-445d94ed796e6b"></a>
### Get data

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_get_data`

**Inputs** filters, period\_columns.

**Explicit results** tuple(data, chart).

**Local steps**

- Set ranges from build\_ranges(filters).
- Set period\_labels from list of scrub(pd) for tuple(\_fd, \_td, pd) drawn from ranges.
  - Draw tuple(\_fd, \_td, pd) from ranges.
- Set periodic\_data from mapping of status → mapping of pd → 0 for pd drawn from period\_labels for status drawn from WORK\_ORDER\_STATUS\_LIST.
  - Draw status from WORK\_ORDER\_STATUS\_LIST.
  - Draw pd from period\_labels.
- Set entries from get\_work\_orders(filters).
- For each d in entries.
  - If d.status equals “Completed”.
    - If not d.actual\_end\_date.
      - Continue with the next iteration or loop test.
    - If period bound to scrub(get\_period\_for\_date(getdate(d.actual\_end\_date), ranges)).
      - Update periodic\_data at “Completed” at period using + 1.
    - Continue with the next iteration or loop test.
  - Set creation\_date from getdate(d.creation).
  - Set period from scrub(get\_period\_for\_date(creation\_date, ranges)).
  - If not period.
    - Continue with the next iteration or loop test.
  - If d.status belongs to tuple(“Not Started”, “Closed”, “Stopped”).
    - Update periodic\_data at d.status at period using + 1.
  - Otherwise.
    - If (d.planned\_end\_date and getdate(today()) &gt; getdate(d.planned\_end\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.planned\_end\_date → getdate(today()) &gt; getdate(d.planned\_end\_date).
      - Update periodic\_data at “Overdue” at period using + 1.
    - Otherwise.
      - Update periodic\_data at “Pending” at period using + 1.
- Set data from list().
- For each status in WORK\_ORDER\_STATUS\_LIST.
  - Set row from mapping(“status” → translated status).
  - For each tuple(\_fd, \_td, period) in ranges.
    - Set row at scrub(period) from periodic\_data at status.get(scrub(period), 0).
  - Evaluate data.append(row).
- Set chart from get\_chart\_data(periodic\_data, period\_columns).
- Return tuple(data, chart).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0552.json#L5096) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1180)

<a id="op-52c1633768b144"></a>
### Get period for date

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_get_period_for_date`

**Inputs** date, ranges.

**Explicit results** period · no value.

**Local steps**

- For each tuple(from\_date, to\_date, period) in ranges.
  - If from\_date ≤ date ≤ to\_date.
    - Compare adjacent operands in order, stopping at the first false comparison in from\_date ≤ date ≤ to\_date.
    - Return period.
- Return no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0552.json#L5994) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1181)

<a id="op-5f961852ae6ad4"></a>
### Build ranges

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_build_ranges`

**Inputs** filters.

**Explicit results** ranges.

**Local steps**

- Set ranges from list().
- For each tuple(from\_date, end\_date) in get\_period\_date\_ranges(filters).
  - Set period from get\_period(end\_date, filters).
  - Evaluate ranges.append(tuple(getdate(from\_date), getdate(end\_date), period)).
- Return ranges.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0552.json#L6101) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1176)

<a id="op-0e3b30d610b4da"></a>
### Get chart data

`operation_enterprise_manufacturing_report_production_analytics_business_behavior_get_chart_data`

**Inputs** periodic\_data, period\_columns.

**Explicit results** mapping(“data” → mapping(“labels” → period\_labels, “datasets” → datasets), “type” → “line”).

**Local steps**

- Set period\_labels from list of col.get(“label”) for col drawn from period\_columns.
  - Draw col from period\_columns.
- Set period\_fieldnames from list of col.get(“fieldname”) for col drawn from period\_columns.
  - Draw col from period\_columns.
- Set datasets from list().
- For each status in WORK\_ORDER\_STATUS\_LIST.
  - Set values from list of periodic\_data.get(status, mapping()).get(fieldname, 0) for fieldname drawn from period\_fieldnames.
    - Draw fieldname from period\_fieldnames.
  - Evaluate datasets.append(mapping(“name” → translated status, “values” → values)).
- Return mapping(“data” → mapping(“labels” → period\_labels, “datasets” → datasets), “type” → “line”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0552.json#L6285) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1178)

## Record · Production plan

[Record definition](../../../../data/record-types/production_plan.json)

<a id="op-7ce5599be221b7"></a>
### Production Plan.onload

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_onload`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- Evaluate self.set\_onload(“enable\_stock\_reservation”, Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”)).
- If self.docstatus equals 1.
  - Evaluate self.set\_onload(“pending\_work\_order\_qty”, ProductionPlanWorkOrderQuantities(self.name).get\_pending\_quantities(self)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L5088) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L971) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L600)

<a id="op-1942c17d54cf72"></a>
### Production Plan.on discard

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L5271) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L969) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L598)

<a id="op-6dc313be47d88b"></a>
### Production Plan.validate

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_pending\_qty\_in\_row\_without\_reference().
- Evaluate self.set\_process\_loss\_percentage().
- Evaluate self.calculate\_total\_planned\_qty().
- Evaluate self.set\_status().
- Evaluate self.\_rename\_temporary\_references().
- Evaluate validate\_uom\_is\_integer(self, “stock\_uom”, “planned\_qty”).
- Evaluate self.validate\_data().
- Evaluate self.validate\_sales\_orders().
- Evaluate self.validate\_material\_request\_type().
- Evaluate self.validate\_raw\_material\_group\_warehouse().
- Evaluate self.validate\_warehouse\_belongs\_to\_company().
- Evaluate clear\_reserve\_stock\_if\_disabled(self).
- Evaluate self.enable\_auto\_reserve\_stock().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pending qty in row without reference](operations-030.md#op-64b9ed184659f1), [set process loss percentage](operations-030.md#op-de0cbd9e75489d), [calculate total planned qty](operations-030.md#op-e5caff857b0d05), [set status](operations-031.md#op-1e85174448a70e), [rename temporary references](operations-030.md#op-5a70ce7d30b78b), [validate data](operations-030.md#op-f7cba36e58776d), [validate sales orders](operations-030.md#op-34984ae6d057e0), [validate material request type](operations-030.md#op-fad55fccebdfbf), [validate raw material group warehouse](operations-030.md#op-c1f21e54184e89), [validate warehouse belongs to company](operations-030.md#op-90755be000fedd), [enable auto reserve stock](operations-030.md#op-ea91f87365cdbc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L614)

<a id="op-90755be000fedd"></a>
### Production Plan.validate warehouse belongs to company

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_validate_warehouse_belongs_to_company`

**Inputs** self.

**Local steps**

- Set warehouses from set(self.for\_warehouse, self.sub\_assembly\_warehouse).
- Evaluate warehouses.update(generator of row.warehouse for row drawn from self.po\_items).
  - Draw row from self.po\_items.
- Evaluate warehouses.update(generator of row.fg\_warehouse for row drawn from self.sub\_assembly\_items).
  - Draw row from self.sub\_assembly\_items.
- For each row in self.mr\_items.
  - Evaluate warehouses.update(tuple(row.warehouse, row.from\_warehouse)).
- For each warehouse in warehouses.
  - If warehouse.
    - Evaluate validate\_warehouse\_company(warehouse, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L956)

<a id="op-c1f21e54184e89"></a>
### Production Plan.validate raw material group warehouse

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_validate_raw_material_group_warehouse`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value · read “Warehouse” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} must be a group warehouse of company {1}.”.format(Platform.bold(translated “Raw Material Group Warehouse”), Platform.bold(self.company)) · validation helper — translated “For Warehouse {0} must be a non-group warehouse under {1}.”.format(Platform.bold(self.for\_warehouse), Platform.bold(self.raw\_material\_group\_warehouse)).

**Local steps**

- If not self.raw\_material\_group\_warehouse.
  - Return no value.
- Set group from Platform.db.get\_value(“Warehouse”, mapping(“name” → self.raw\_material\_group\_warehouse, “is\_group” → 1, “company” → self.company), list(“lft”, “rgt”), as\_dict = true).
- If not group.
  - Call the validation error handler Platform.throw(translated “{0} must be a group warehouse of company {1}.”.format(Platform.bold(translated “Raw Material Group Warehouse”), Platform.bold(self.company))).
- If (self.for\_warehouse and not Platform.db.exists(“Warehouse”, mapping(“name” → self.for\_warehouse, “is\_group” → 0, “lft” → tuple(“&gt;”, group.lft), “rgt” → tuple(“&lt;”, group.rgt)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.for\_warehouse → not Platform.db.exists(“Warehouse”, mapping(“name” → self.for\_warehouse, “is\_group” → 0, “lft” → tuple(“&gt;”, group.lft), “rgt” → tuple(“&lt;”, group.rgt))).
  - Call the validation error handler Platform.throw(translated “For Warehouse {0} must be a non-group warehouse under {1}.”.format(Platform.bold(self.for\_warehouse), Platform.bold(self.raw\_material\_group\_warehouse))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L989) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L618)

<a id="op-ea91f87365cdbc"></a>
### Production Plan.enable auto reserve stock

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_enable_auto_reserve_stock`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (self.is\_new() and Platform.db.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → Platform.db.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).
  - Set self.reserve\_stock from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L6074) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L581)

<a id="op-fad55fccebdfbf"></a>
### Production Plan.validate material request type

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_validate_material_request_type`

**Inputs** self.

**Local steps**

- For each row in self.get(“mr\_items”).
  - If (row.from\_warehouse and row.material\_request\_type differs from “Material Transfer”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.from\_warehouse → row.material\_request\_type differs from “Material Transfer”.
    - Set row.from\_warehouse from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L6187) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L617)

<a id="op-34984ae6d057e0"></a>
### Production Plan.validate sales orders

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_validate_sales_orders`

**Inputs** self, sales\_order = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — msg · validation helper — translated “No items are available in the sales order {0} for production”.format(sales\_order).

**Local steps**

- Set sales\_orders from list().
- If sales\_order.
  - Evaluate sales\_orders.append(sales\_order).
- Otherwise.
  - Set sales\_orders from list of row.sales\_order for row drawn from self.sales\_orders where row.sales\_order.
    - Draw row from self.sales\_orders, keep a combination only if (row.sales\_order).
- Set data from sales\_order\_query(filters = mapping(“company” → self.company, “sales\_orders” → sales\_orders)).
- Set title from translated “Production Plan Already Submitted”.
- If (not data and sales\_orders).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not data → sales\_orders.
  - Set msg from translated “No items are available in the sales order {0} for production”.format(sales\_orders at 0).
  - If len(sales\_orders) &gt; 1.
    - Set sales\_orders from “, ”.join(sales\_orders).
    - Set msg from translated “No items are available in sales orders {0} for production”.format(sales\_orders).
  - Call the validation error handler Platform.throw(msg, title = title).
- Set data from list of d at 0 for d drawn from data.
  - Draw d from data.
- For each sales\_order in sales\_orders.
  - If sales\_order does not belong to data.
    - Call the validation error handler Platform.throw(translated “No items are available in the sales order {0} for production”.format(sales\_order), title = title).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L619)

<a id="op-64b9ed184659f1"></a>
### Production Plan.set pending qty in row without reference

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_set_pending_quantity_in_row_without_reference`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-64b9ed184659f1-guard-3"></a>If self.docstatus &gt; 0.
  - Return no value.
- For each item in self.po\_items.
  - If (not item.get(“sales\_order”) or not item.get(“material\_request”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(“sales\_order”) → not item.get(“material\_request”).
    - Set item.pending\_qty from item.planned\_qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus &gt; 0, self.docstatus = 1 (submitted) selects the branch that returns no value. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-64b9ed184659f1-guard-3)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L6927) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L604)

<a id="op-de0cbd9e75489d"></a>
### Production Plan.set process loss percentage

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_set_process_loss_percentage`

**Inputs** self.

**Local steps**

- For each item in self.po\_items.
  - Set item.process\_loss\_percentage from get\_plan\_process\_loss\_percentage(self, item.bom\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L951)

<a id="op-e5caff857b0d05"></a>
### Production Plan.calculate total planned qty

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_calculate_total_planned_quantity`

**Inputs** self.

**Local steps**

- Set self.total\_planned\_qty from 0.
- For each d in self.po\_items.
  - Update self.total\_planned\_qty using + flt(d.planned\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0486.json#L7099) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L575)

<a id="op-f7cba36e58776d"></a>
### Production Plan.validate data

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_validate_data`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select BOM for Item in Row {0}”.format(d.idx) · validation helper — translated “Row #{0}: Planned Qty must be greater than 0 for Item {1}.”.format(d.idx, Platform.bold(d.item\_code)).

**Local steps**

- For each d in self.get(“po\_items”).
  - If not d.bom\_no.
    - Call the validation error handler Platform.throw(translated “Please select BOM for Item in Row {0}”.format(d.idx)).
  - If not flt(d.planned\_qty).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Planned Qty must be greater than 0 for Item {1}.”.format(d.idx, Platform.bold(d.item\_code))).
- Evaluate self.validate\_boms().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate boms](operations-030.md#op-6468625dd4808a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L615)

<a id="op-6468625dd4808a"></a>
### Production Plan.validate boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_validate_boms`

**Inputs** self.

**Local steps**

- Set boms from dict.fromkeys(generator of tuple(d.item\_code, d.bom\_no) for d drawn from self.po\_items).
  - Draw d from self.po\_items.
- Evaluate boms.update(dict.fromkeys(generator of tuple(d.production\_item, d.bom\_no) for d drawn from self.sub\_assembly\_items where d.bom\_no)).
  - Draw d from self.sub\_assembly\_items, keep a combination only if (d.bom\_no).
- For each tuple(item\_code, bom\_no) in boms.
  - Evaluate validate\_production\_bom(item\_code, bom\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L953)

<a id="op-5a70ce7d30b78b"></a>
### Production Plan.rename temporary references

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_rename_temporary_references`

**Inputs** self.

**Local steps**

- Set new\_name\_map from mapping of d.temporary\_name → d.name for d drawn from self.po\_items where d.temporary\_name.
  - Draw d from self.po\_items, keep a combination only if (d.temporary\_name).
- Set actual\_names from set of d.name for d drawn from self.po\_items.
  - Draw d from self.po\_items.
- For each sub\_assy in self.sub\_assembly\_items.
  - If sub\_assy.production\_plan\_item does not belong to actual\_names.
    - Set sub\_assy.production\_plan\_item from new\_name\_map.get(sub\_assy.production\_plan\_item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L283) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L602)

<a id="op-9dc463de82a61e"></a>
### Production Plan.get open sales orders

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_open_sales_orders`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Sales orders are not available for production”.

**Local steps**

- Set open\_so from get\_sales\_orders(self).
- If open\_so.
  - Evaluate self.add\_so\_in\_table(open\_so).
- Otherwise.
  - Evaluate Platform.msgprint(translated “Sales orders are not available for production”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add so in table](operations-030.md#op-ec208f91f722ca).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L585)

<a id="op-ec208f91f722ca"></a>
### Production Plan.add so in table

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_add_sales_order_in_table`

**Inputs** self, open\_so.

**Local steps**

- Evaluate self.set(“sales\_orders”, list()).
- For each data in open\_so.
  - Evaluate self.append(“sales\_orders”, mapping(“sales\_order” → data.name, “sales\_order\_date” → data.transaction\_date, “customer” → data.customer, “grand\_total” → data.base\_grand\_total)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L573)

<a id="op-eddd3b366b575f"></a>
### Production Plan.get pending material requests

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_pending_material_remote_requests`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set bom from Platform.qb.DocType(“BOM”).
- Set mr from Platform.qb.DocType(“Material Request”).
- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Set pending\_mr\_query from nested operand in the contract(nested operand in the contract).select(mr.name, mr.transaction\_date).distinct().where(((((((nested operand in the contract bitwise and nested operand in the contract) bitwise ….
- If self.from\_date.
  - Set pending\_mr\_query from pending\_mr\_query.where(mr.transaction\_date ≥ self.from\_date).
- If self.to\_date.
  - Set pending\_mr\_query from pending\_mr\_query.where(mr.transaction\_date ≤ self.to\_date).
- If self.warehouse.
  - Set pending\_mr\_query from pending\_mr\_query.where(mr\_item.warehouse equals self.warehouse).
- If self.item\_code.
  - Set pending\_mr\_query from pending\_mr\_query.where(mr\_item.item\_code equals self.item\_code).
- Set pending\_mr from pending\_mr\_query.run(as\_dict = true).
- Evaluate self.add\_mr\_in\_table(pending\_mr).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add mr in table](operations-030.md#op-8d0f830a8c397f).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L586)

<a id="op-8d0f830a8c397f"></a>
### Production Plan.add mr in table

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_add_material_request_in_table`

**Inputs** self, pending\_mr.

**Local steps**

- Evaluate self.set(“material\_requests”, list()).
- For each data in pending\_mr.
  - Evaluate self.append(“material\_requests”, mapping(“material\_request” → data.name, “material\_request\_date” → data.transaction\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L570)
