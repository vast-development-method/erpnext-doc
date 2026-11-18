# Production · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Work order stock report

<a id="op-971aef8b03b7a8"></a>
### Get bom descriptions

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_bom_descriptions`

**Inputs** wo\_list.

**Record and data access** read “BOM” via get\_all.

**Explicit results** dict(Platform.get\_all(“BOM”, filters = mapping(“name” → list(“in”, boms)), fields = list(“name”, “description”), as\_list = true)).

**Local steps**

- Set boms from list(set of d.bom\_no for d drawn from wo\_list where d.bom\_no).
  - Draw d from wo\_list, keep a combination only if (d.bom\_no).
- Return dict(Platform.get\_all(“BOM”, filters = mapping(“name” → list(“in”, boms)), fields = list(“name”, “description”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1156)

<a id="op-44cc564c00cc25"></a>
### Get work order items

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_work_order_items`

**Inputs** wo\_list.

**Record and data access** read “Work Order Item” via get\_all.

**Explicit results** items\_by\_order.

**Local steps**

- Set items\_by\_order from mapping().
- For each row in Platform.get\_all(“Work Order Item”, filters = mapping(“parent” → list(“in”, list of d.name for d drawn from wo\_list), “parenttype” → “Work Order”), fields = list(“parent”, “item\_code”, “source\_warehouse”,  ….
  - Draw d from wo\_list.
  - Evaluate items\_by\_order.setdefault(row.parent, list()).append(row).
- Return items\_by\_order.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1161)

<a id="op-b70ecf81de922e"></a>
### Get stock

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_stock`

**Inputs** items\_by\_order, filters.

**Record and data access** read “Bin” via get\_all.

**Explicit results** mapping() · stock.

**Local steps**

- Set rows from list of row for items drawn from items\_by\_order.values(), then row drawn from items.
  - Draw items from items\_by\_order.values().
  - Draw row from items.
- Set warehouses from (set of (row.source\_warehouse or filters.get(“warehouse”)) for row drawn from rows − set(no value, empty text)).
  - Draw row from rows.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.source\_warehouse → filters.get(“warehouse”).
- If (not rows or not warehouses).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not rows → not warehouses.
  - Return mapping().
- Set stock from mapping().
- For each d in Platform.get\_all(“Bin”, filters = mapping(“item\_code” → list(“in”, list(set of row.item\_code for row drawn from rows)), “warehouse” → list(“in”, list(warehouses))), fields = list(“item\_code”, “warehouse”,  ….
  - Draw row from rows.
  - Set stock at tuple(d.item\_code, d.warehouse) from flt(d.actual\_qty).
- Return stock.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1159)

<a id="op-be716d95d13fc9"></a>
### Get work orders

`operation_enterprise_manufacturing_report_work_order_stock_report_business_behavior_get_work_orders`

**Inputs** no declared parameters.

**Record and data access** read “Work Order” via get\_all.

**Explicit results** out.

**Local steps**

- Set out from Platform.get\_all(“Work Order”, filters = mapping(“docstatus” → 1, “status” → tuple(“in”, list(“Not Started”, “In Process”, “Stock Reserved”, “Stock Partially Reserved”))), fields = list(“name”, “status”, “ ….
- Return out.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1234)

<a id="op-85dd118dc80fc0"></a>
### Get columns

`operation_enterprise_manufacturing_report_work_order_stock_report_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “work\_order”, “label” → translated “Work Order”, “fieldtype” → “Link”, “options” → “Work Order”, …), mapping(“fieldname” → “bom\_no”, “label” → translated “BOM”, “fieldtype” → “Li ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0557.json#L1473) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1232)

## Report · Work order summary

<a id="op-f79dafc1779eb4"></a>
### Execute

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- If not filters.get(“age”).
  - Set filters at “age” from 0.
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Set chart\_data from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1235)

<a id="op-0089b265791a6a"></a>
### Get data

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Work Order” via get\_list.

**Explicit results** res.

**Local steps**

- Set query\_filters from mapping(“docstatus” → tuple(“&lt;”, 2)).
- Set fields from list(“name”, “status”, “sales\_order”, “production\_item”, …).
- For each field in list(“sales\_order”, “production\_item”).
  - If filters.get(field).
    - Set query\_filters at field from tuple(“in”, filters.get(field)).
- For each field in list(“status”, “company”).
  - If filters.get(field).
    - Set query\_filters at field from filters.get(field).
- If filters.get(“based\_on”) equals “Planned Date”.
  - Set query\_filters at “planned\_start\_date” from tuple(“&gt;=”, filters.get(“from\_date”)).
  - Set query\_filters at “planned\_end\_date” from tuple(“&lt;”, add\_days(filters.get(“to\_date”), 1)).
- Otherwise.
  - If filters.get(“based\_on”) equals “Actual Date”.
    - Set query\_filters at “actual\_start\_date” from tuple(“&gt;=”, filters.get(“from\_date”)).
    - Set query\_filters at “actual\_end\_date” from tuple(“&lt;”, add\_days(filters.get(“to\_date”), 1)).
  - Otherwise.
    - Set query\_filters at “creation” from tuple(“between”, list(filters.get(“from\_date”), filters.get(“to\_date”))).
- Set data from Platform.get\_list(“Work Order”, fields = fields, filters = query\_filters, order\_by = “planned\_start\_date asc”).
- Set res from list().
- For each d in data.
  - Set start\_date from (d.actual\_start\_date or d.planned\_start\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.actual\_start\_date → d.planned\_start\_date.
  - Set d.age from 0.
  - If d.status differs from “Completed”.
    - Set d.age from max(date\_diff(today(), start\_date), 0).
  - If filters.get(“age”) ≤ d.age.
    - Evaluate res.append(d).
- Return res.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1241)

<a id="op-382347b84f3af4"></a>
### Get chart data

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_get_chart_data`

**Inputs** data, filters.

**Explicit results** get\_chart\_based\_on\_status(data) · get\_chart\_based\_on\_age(data) · get\_chart\_based\_on\_qty(data, filters).

**Local steps**

- If filters.get(“charts\_based\_on”) equals “Status”.
  - Return get\_chart\_based\_on\_status(data).
- Otherwise.
  - If filters.get(“charts\_based\_on”) equals “Age”.
    - Return get\_chart\_based\_on\_age(data).
  - Otherwise.
    - Return get\_chart\_based\_on\_qty(data, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0557.json#L6291) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1239)

<a id="op-a747c75639bc59"></a>
### Get chart based on status

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_get_chart_based_on_status`

**Inputs** data.

**Explicit results** chart.

**Local steps**

- Set labels from Platform.get\_meta(“Work Order”).get\_options(“status”).split(whitespace '\\n').
- If empty text belongs to labels.
  - Evaluate labels.remove(empty text).
- Set status\_wise\_data from defaultdict(int).
- For each d in data.
  - Update status\_wise\_data at d.status using + 1.
- Set labels from list of translated label for label drawn from labels.
  - Draw label from labels.
- Set values from list of status\_wise\_data at label for label drawn from labels.
  - Draw label from labels.
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Qty Wise Chart”, “values” → values))), “type” → “donut”, “height” → 300).
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0557.json#L6474) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1238)

<a id="op-ead14be445650b"></a>
### Get chart based on age

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_get_chart_based_on_age`

**Inputs** data.

**Explicit results** chart.

**Local steps**

- Set labels from list(translated “0-30 Days”, translated “30-60 Days”, translated “60-90 Days”, translated “90 Above”).
- Set age\_wise\_data from mapping(“0-30 Days” → 0, “30-60 Days” → 0, “60-90 Days” → 0, “90 Above” → 0).
- For each d in data.
  - If d.status equals “Completed”.
    - Continue with the next iteration or loop test.
  - If d.age ≤ 30.
    - Update age\_wise\_data at “0-30 Days” using + 1.
  - Otherwise.
    - If (d.age &gt; 30 and d.age ≤ 60).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.age &gt; 30 → d.age ≤ 60.
      - Update age\_wise\_data at “30-60 Days” using + 1.
    - Otherwise.
      - If (d.age &gt; 60 and d.age ≤ 90).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.age &gt; 60 → d.age ≤ 90.
        - Update age\_wise\_data at “60-90 Days” using + 1.
      - Otherwise.
        - Update age\_wise\_data at “90 Above” using + 1.
- Set values from list(age\_wise\_data at “0-30 Days”, age\_wise\_data at “30-60 Days”, age\_wise\_data at “60-90 Days”, age\_wise\_data at “90 Above”).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Qty Wise Chart”, “values” → values))), “type” → “donut”, “height” → 300).
- Return chart.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1236)

<a id="op-ef5ece46237189"></a>
### Get chart based on qty

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_get_chart_based_on_quantity`

**Inputs** data, filters.

**Explicit results** chart.

**Local steps**

- Set tuple(labels, periodic\_data) from prepare\_chart\_data(data, filters).
- Set tuple(pending, completed) from tuple(list(), list()).
- Set datasets from list().
- For each d in labels.
  - Evaluate pending.append(periodic\_data.get(“Pending”).get(d)).
  - Evaluate completed.append(periodic\_data.get(“Completed”).get(d)).
- Evaluate datasets.append(mapping(“name” → translated “Pending”, “values” → pending)).
- Evaluate datasets.append(mapping(“name” → translated “Completed”, “values” → completed)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “bar”, “barOptions” → mapping(“stacked” → 1)).
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0558.json#L611) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1237)

<a id="op-a1cf242cd35c4c"></a>
### Prepare chart data

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_prepare_chart_data`

**Inputs** data, filters.

**Explicit results** tuple(labels, periodic\_data).

**Local steps**

- Set labels from list().
- Set periodic\_data from mapping(“Pending” → mapping(), “Completed” → mapping()).
- Set filters.range from “Monthly”.
- Set ranges from get\_period\_date\_ranges(filters).
- For each tuple(from\_date, end\_date) in ranges.
  - Set period from get\_period(end\_date, filters).
  - If period does not belong to labels.
    - Evaluate labels.append(period).
  - If period does not belong to periodic\_data at “Pending”.
    - Set periodic\_data at “Pending” at period from 0.
  - If period does not belong to periodic\_data at “Completed”.
    - Set periodic\_data at “Completed” at period from 0.
  - For each d in data.
    - If (getdate(d.planned\_start\_date) ≥ from\_date and getdate(d.planned\_start\_date) ≤ end\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(d.planned\_start\_date) ≥ from\_date → getdate(d.planned\_start\_date) ≤ end\_date.
      - Update periodic\_data at “Pending” at period using + get\_pending\_qty(d).
      - Update periodic\_data at “Completed” at period using + flt(d.produced\_qty).
- Return tuple(labels, periodic\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1242)

<a id="op-a1f8838af893ef"></a>
### Get pending qty

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_summary_work_order_summary_get_pending_qty`

**Inputs** work\_order.

**Explicit results** 0.0 · ((flt(work\_order.qty) − flt(work\_order.produced\_qty)) − flt(work\_order.process\_loss\_qty)).

**Local steps**

- If work\_order.status belongs to tuple(“Completed”, “Closed”, “Stopped”).
  - Return 0.0.
- Return ((flt(work\_order.qty) − flt(work\_order.produced\_qty)) − flt(work\_order.process\_loss\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1164)

<a id="op-215d30d3741274"></a>
### Get columns

`operation_enterprise_manufacturing_report_work_order_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Work Order”, …)).
- If not filters.get(“status”).
  - Evaluate columns.append(mapping(“label” → translated “Status”, “fieldname” → “status”, “width” → 100)).
- Evaluate columns.extend(list(mapping(“label” → translated “Production Item”, “fieldname” → “production\_item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Produce Qty”, “fieldname” →  ….
- If filters.get(“status”) differs from “Not Started”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Actual Start Date”, “fieldname” → “actual\_start\_date”, “fieldtype” → “Date”, “width” → 100), mapping(“label” → translated “Actual End Date”, “fieldname” →  ….
- If filters.get(“status”) equals “Completed”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Lead Time (in mins)”, “fieldname” → “lead\_time”, “fieldtype” → “Float”, “width” → 110))).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1240)

## Record · Workstation

[Record definition](../../../../data/record-types/workstation.json)

<a id="op-8231bdd2ea09e0"></a>
### Workstation.validate

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_operating\_component().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate operating component](operations-047.md#op-33824a78b0c099).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L4750) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L999)

<a id="op-33824a78b0c099"></a>
### Workstation.validate duplicate operating component

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_validate_duplicate_operating_component`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Duplicate Operating Component {0} found in Operating Components”.format(bold(row.operating\_component)).

**Local steps**

- Set components from list().
- For each row in self.workstation\_costs.
  - If row.operating\_component does not belong to components.
    - Evaluate components.append(row.operating\_component).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Duplicate Operating Component {0} found in Operating Components”.format(bold(row.operating\_component))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L4801) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L81) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1000)

<a id="op-a89073e54d8335"></a>
### Workstation.before save

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_before_save`

**Inputs** self.

**Local steps**

- If self.has\_value\_changed(“workstation\_type”).
  - Evaluate self.\_set\_data\_based\_on\_workstation\_type().
- Evaluate self.set\_hour\_rate().
- Evaluate self.set\_total\_working\_hours().
- Evaluate self.disabled\_workstation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set data based on workstation type](operations-047.md#op-c56d6f1b2fd9c2), [set hour rate](operations-047.md#op-d67268fb0042d1), [set total working hours](operations-047.md#op-309e08ba4dcae3), [disabled workstation](operations-047.md#op-7e6ae2c4ae9f31).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L4992) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L989)

<a id="op-7e6ae2c4ae9f31"></a>
### Workstation.disabled workstation

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_disabled_workstation`

**Inputs** self.

**Local steps**

- If self.disabled.
  - Set self.status from “Off”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L5135) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L991)

<a id="op-309e08ba4dcae3"></a>
### Workstation.set total working hours

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_set_total_working_hours`

**Inputs** self.

**Local steps**

- Set self.total\_working\_hours from 0.0.
- For each row in self.working\_hours.
  - Evaluate self.validate\_working\_hours(row).
  - If (row.start\_time and row.end\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.start\_time → row.end\_time.
    - Set row.hours from flt(time\_diff\_in\_hours(row.end\_time, row.start\_time), row.precision(“hours”)).
    - If row.enabled.
      - Update self.total\_working\_hours using + row.hours.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate working hours](operations-047.md#op-2ce5911a1c56ed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L996)

<a id="op-2ce5911a1c56ed"></a>
### Workstation.validate working hours

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_validate_working_hours`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Start Time must be before End Time”.format(row.idx).

**Local steps**

- If get\_time(row.start\_time) ≥ get\_time(row.end\_time).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Start Time must be before End Time”.format(row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L5417) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1002)

<a id="op-d67268fb0042d1"></a>
### Workstation.set hour rate

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_set_hour_rate`

**Inputs** self.

**Local steps**

- Set self.hour\_rate from 0.0.
- For each row in self.workstation\_costs.
  - If row.operating\_cost.
    - Update self.hour\_rate using + flt(row.operating\_cost).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L5574) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L995)

<a id="op-b5a250716792f8"></a>
### Workstation.set data based on workstation type

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_set_data_based_on_workstation_type`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.\_set\_data\_based\_on\_workstation\_type().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set data based on workstation type](operations-047.md#op-c56d6f1b2fd9c2).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L5687) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L993)

<a id="op-c56d6f1b2fd9c2"></a>
### Workstation.set data based on workstation type

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_set_data_based_on_workstation_type_2`

**Inputs** self.

**Record and data access** read “Workstation Cost” via get\_all.

**Local steps**

- If self.workstation\_type.
  - Set data from Platform.get\_all(“Workstation Cost”, fields = list(“operating\_component”, “operating\_cost”, “idx”), filters = mapping(“parent” → self.workstation\_type, “parenttype” → “Workstation Type”), order\_by = “idx”).
  - If data.
    - Set self.workstation\_costs from list().
  - For each row in data.
    - Evaluate self.append(“workstation\_costs”, mapping(“operating\_component” → row.operating\_component, “operating\_cost” → row.operating\_cost, “idx” → row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L5785) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L994)

<a id="op-7f23438fb8fdd4"></a>
### Workstation.on update

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_overlap\_for\_operation\_timings().
- Evaluate self.update\_bom\_operation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap for operation timings](operations-048.md#op-ae77b13977cf3b), [update bom operation](operations-048.md#op-18119b76125b05).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L992)
