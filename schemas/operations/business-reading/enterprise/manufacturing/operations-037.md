# Production · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Quality inspection summary

<a id="op-a023e06a5cef62"></a>
### Get chart data

`operation_enterprise_manufacturing_report_quality_inspection_summary_business_behavior_get_chart_data`

**Inputs** periodic\_data, columns.

**Explicit results** chart.

**Local steps**

- Set labels from list(translated “Rejected”, translated “Accepted”).
- Set status\_wise\_data from mapping(“Accepted” → 0, “Rejected” → 0).
- Set datasets from list().
- For each d in periodic\_data.
  - If d.status belongs to status\_wise\_data.
    - Update status\_wise\_data at d.status using + 1.
- Evaluate datasets.append(mapping(“name” → translated “Qty Wise Chart”, “values” → list(status\_wise\_data.get(“Rejected”), status\_wise\_data.get(“Accepted”)))).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “donut”, “height” → 300).
- Return chart.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1214)

<a id="op-69522379017024"></a>
### Get columns

`operation_enterprise_manufacturing_report_quality_inspection_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Quality Inspection”, …), mapping(“label” → translated “Report Date”, “fieldname” → “report\_date”, “fieldtype ….
- If not filters.get(“status”).
  - Evaluate columns.append(mapping(“label” → translated “Status”, “fieldname” → “status”, “width” → 100)).
- Evaluate columns.extend(list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “ ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1215)

## Record · Routing

[Record definition](../../../../data/record-types/routing.json)

<a id="op-9ff1c63bd63f9b"></a>
### Routing.validate

`operation_enterprise_manufacturing_record_definitions_routing_business_behavior_routing_validate`

**Inputs** self.

**Local steps**

- Evaluate self.calculate\_operating\_cost().
- Evaluate self.set\_routing\_id().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate operating cost](operations-037.md#op-74635602e458ff), [set routing id](operations-037.md#op-1b3c332897ecae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L1584) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L759)

<a id="op-a74f1191acdd6e"></a>
### Routing.on update

`operation_enterprise_manufacturing_record_definitions_routing_business_behavior_routing_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.calculate\_operating\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate operating cost](operations-037.md#op-74635602e458ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L1655) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L757)

<a id="op-74635602e458ff"></a>
### Routing.calculate operating cost

`operation_enterprise_manufacturing_record_definitions_routing_business_behavior_routing_calculate_operating_cost`

**Inputs** self.

**Local steps**

- Evaluate self.set\_workstation\_hour\_rates().
- For each operation in self.operations.
  - Set operation.operating\_cost from flt(((flt(operation.hour\_rate) × flt(operation.time\_in\_mins)) ÷ 60), operation.precision(“operating\_cost”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set workstation hour rates](operations-037.md#op-0c896668af66f4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L756)

<a id="op-0c896668af66f4"></a>
### Routing.set workstation hour rates

`operation_enterprise_binding_enterprise_manufacturing_doctype_routing_routing_routing_set_workstation_hour_rates`

**Inputs** self.

**Record and data access** read “Workstation” via get\_all.

**Explicit results** no value.

**Local steps**

- Set rows from self.get\_rows\_without\_workstation\_rate().
- Set workstations from list(set of row.workstation for row drawn from rows where row.workstation).
  - Draw row from rows, keep a combination only if (row.workstation).
- If not workstations.
  - Return no value.
- Set hour\_rates from dict(Platform.get\_all(“Workstation”, filters = mapping(“name” → list(“in”, workstations)), fields = list(“name”, “hour\_rate”), as\_list = true)).
- For each row in rows.
  - If row.workstation belongs to hour\_rates.
    - Set row.hour\_rate from hour\_rates at row.workstation.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows without workstation rate](operations-037.md#op-87c1d6449b6e24).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L981)

<a id="op-87c1d6449b6e24"></a>
### Routing.get rows without workstation rate

`operation_enterprise_binding_enterprise_manufacturing_doctype_routing_routing_routing_get_rows_without_workstation_rate`

**Inputs** self.

**Explicit results** rows.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- Set previous\_rows from mapping of row.name → row for row drawn from previous.operations when previous, otherwise mapping().
  - Value choice on previous — true gives mapping of row.name → row for row drawn from previous.operations, false gives mapping().
  - Draw row from previous.operations.
- Set rows from list().
- For each row in self.operations.
  - Set old from previous\_rows.get(row.name).
  - If (not row.hour\_rate or (old and old.workstation differs from row.workstation and flt(old.hour\_rate) equals flt(row.hour\_rate))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.hour\_rate → (old and old.workstation differs from row.workstation and flt(old.hour\_rate) equals flt(row.hour\_rate)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in old → old.workstation differs from row.workstation → flt(old.hour\_rate) equals flt(row.hour\_rate).
    - Evaluate rows.append(row).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L980)

<a id="op-1b3c332897ecae"></a>
### Routing.set routing id

`operation_enterprise_manufacturing_record_definitions_routing_business_behavior_routing_set_routing_identifier`

**Inputs** self.

**Explicit failure paths** validation helper — translated “At row #{0}: the sequence id {1} cannot be less than previous row sequence id {2}”.format(row.idx, row.sequence\_id, sequence\_id).

**Local steps**

- Set sequence\_id from 0.
- For each row in self.operations.
  - If not row.sequence\_id.
    - Set row.sequence\_id from (sequence\_id + 1).
  - Otherwise.
    - If (sequence\_id and row.sequence\_id and cint(sequence\_id) &gt; cint(row.sequence\_id)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sequence\_id → row.sequence\_id → cint(sequence\_id) &gt; cint(row.sequence\_id).
      - Call the validation error handler Platform.throw(translated “At row #{0}: the sequence id {1} cannot be less than previous row sequence id {2}”.format(row.idx, row.sequence\_id, sequence\_id)).
  - Set sequence\_id from row.sequence\_id.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L1933) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L758)

<a id="op-22235c0b5572c0"></a>
### Get operations

`operation_enterprise_manufacturing_record_definitions_routing_business_behavior_get_operations`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Routing” via exists · read parenttype via get\_list · read “BOM Operation” via get\_all.

**Explicit results** list() · Platform.get\_all(“BOM Operation”, fields = list(“operation”), filters = query\_filters, start = start, page\_length = page\_len, …).

**Local steps**

- Set query\_filters from mapping().
- If txt.
  - Set query\_filters from mapping(“operation” → list(“like”, formatted text %{txt}%)).
- If routing bound to filters.get(“routing”).
  - If not Platform.db.exists(“Routing”, routing).
    - Return list().
  - Set ptype from “select” when Platform.only\_has\_select\_perm(“Routing”), otherwise “read”.
    - Value choice on Platform.only\_has\_select\_perm(“Routing”) — true gives “select”, false gives “read”.
  - Evaluate Platform.has\_permission(“Routing”, ptype, doc = routing, throw = true).
  - Set query\_filters at “parent” from routing.
  - Set query\_filters at “parenttype” from “Routing”.
- Otherwise.
  - Set parents from list().
  - For each parenttype in tuple(“Routing”, “BOM”).
    - Set ptype from “select” when Platform.only\_has\_select\_perm(parenttype), otherwise “read”.
      - Value choice on Platform.only\_has\_select\_perm(parenttype) — true gives “select”, false gives “read”.
    - If Platform.has\_permission(parenttype, ptype).
      - Update parents using + Platform.get\_list(parenttype, pluck = “name”).
  - If not parents.
    - Return list().
  - Set query\_filters at “parent” from list(“in”, parents).
- Return Platform.get\_all(“BOM Operation”, fields = list(“operation”), filters = query\_filters, start = start, page\_length = page\_len, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Routing”, ptype, doc = routing, throw = true), Platform.has\_permission(parenttype, ptype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L755)

<a id="op-7662231e7bd389"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_routing_routing_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “routing”, “transactions” → list(mapping(“items” → list(“BOM”)))).

**Local steps**

- Return mapping(“fieldname” → “routing”, “transactions” → list(mapping(“items” → list(“BOM”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L2569) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L760)

## Record · Sales forecast

[Record definition](../../../../data/record-types/sales_forecast.json)

<a id="op-f2e4771e09de87"></a>
### Sales Forecast.validate

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_salesforecast_validate`

**Inputs** self.

**Local steps**

- If self.is\_new().
  - Set self.status from “Planned”.
- Evaluate self.validate\_demand\_qty().
- Evaluate self.validate\_parent\_warehouse().
- Evaluate self.validate\_periods\_and\_dates().
- Evaluate self.validate\_stock\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate demand qty](operations-037.md#op-72d09514dfd683), [validate parent warehouse](operations-037.md#op-e764d99707d56e), [validate periods and dates](operations-037.md#op-79067d115a9ed5), [validate stock items](operations-037.md#op-433b01e35b49a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L983)

<a id="op-e764d99707d56e"></a>
### Sales Forecast.validate parent warehouse

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_salesforecast_validate_parent_warehouse`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Parent Warehouse {0} must be a group warehouse of company {1}”.format(Platform.bold(self.parent\_warehouse), Platform.bold(self.company)).

**Local steps**

- Set warehouse from Platform.get\_cached\_value(“Warehouse”, self.parent\_warehouse, list(“is\_group”, “company”), as\_dict = true).
- If (warehouse and (not warehouse.is\_group or warehouse.company differs from self.company)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → (not warehouse.is\_group or warehouse.company differs from self.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not warehouse.is\_group → warehouse.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Parent Warehouse {0} must be a group warehouse of company {1}”.format(Platform.bold(self.parent\_warehouse), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, self.parent\_warehouse, list(“is\_group”, “company”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L985)

<a id="op-79067d115a9ed5"></a>
### Sales Forecast.validate periods and dates

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_salesforecast_validate_periods_and_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Number of periods must be greater than zero” · validation helper — translated “Row #{0}: Delivery Date {1} cannot be before From Date {2}”.format(row.idx, formatdate(row.delivery\_date), formatdate(self.from\_date)).

**Local steps**

- If cint(self.demand\_number) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Number of periods must be greater than zero”).
- For each row in self.items.
  - If (row.delivery\_date and getdate(row.delivery\_date) &lt; getdate(self.from\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.delivery\_date → getdate(row.delivery\_date) &lt; getdate(self.from\_date).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Date {1} cannot be before From Date {2}”.format(row.idx, formatdate(row.delivery\_date), formatdate(self.from\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L986)

<a id="op-433b01e35b49a3"></a>
### Sales Forecast.validate stock items

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_salesforecast_validate_stock_items`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only stock items can be forecast: {0}”.format(“, ”.join(generator of Platform.bold(item) for item drawn from non\_stock\_items)).

**Local steps**

- Set item\_codes from set of row.item\_code for row drawn from (self.items + self.selected\_items) where row.item\_code.
  - Draw row from (self.items + self.selected\_items), keep a combination only if (row.item\_code).
- If not item\_codes.
  - Return no value.
- Set non\_stock\_items from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list(item\_codes)), “is\_stock\_item” → 0), pluck = “name”).
- If non\_stock\_items.
  - Call the validation error handler Platform.throw(translated “Only stock items can be forecast: {0}”.format(“, ”.join(generator of Platform.bold(item) for item drawn from non\_stock\_items))).
    - Draw item from non\_stock\_items.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L987)

<a id="op-72d09514dfd683"></a>
### Sales Forecast.validate demand qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_salesforecast_validate_demand_qty`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Row #{0}: Demand Qty is mandatory”.format(row.idx).

**Local steps**

- For each row in self.items.
  - If row.get(“demand\_qty”) belongs to tuple(no value, empty text).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Demand Qty is mandatory”.format(row.idx), Platform.MandatoryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L984)

<a id="op-694cced6df10ca"></a>
### Sales Forecast.on discard

`operation_enterprise_manufacturing_record_definitions_sales_forecast_business_behavior_sales_forecast_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L5435) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L771)

<a id="op-d505378452a808"></a>
### Sales Forecast.on cancel

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_salesforecast_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L982)

<a id="op-6160ed4fb2c3ae"></a>
### Sales Forecast.generate manual demand

`operation_enterprise_manufacturing_record_definitions_sales_forecast_business_behavior_sales_forecast_generate_manual_demand`

**Inputs** self.

**Record and data access** read “Item” via get\_all · read “Item” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.selected\_items.
  - Return no value.
- Set item\_details\_by\_code from mapping of item.name → item for item drawn from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list of row.item\_code for row drawn from self.selected\_items)), fields = list(“name”, “item\_na ….
  - Draw item from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list of row.item\_code for row drawn from self.selected\_items)), fields = list(“name”, “item\_name”, “stock\_uom as uom”)).
  - Draw row from self.selected\_items.
- Set ascii\_items\_by\_lowercase\_code from mapping().
- If Platform.db.db\_type equals “mariadb”.
  - Set ascii\_items\_by\_lowercase\_code from mapping of code.lower() → item for tuple(code, item) drawn from item\_details\_by\_code.items() where code.isascii().
    - Draw tuple(code, item) from item\_details\_by\_code.items(), keep a combination only if (code.isascii()).
- Set forecast\_demand from list().
- For each row in self.selected\_items.
  - If row.item\_code does not belong to item\_details\_by\_code.
    - Set matching\_item from no value.
    - If row.item\_code.isascii().
      - Set matching\_item from ascii\_items\_by\_lowercase\_code.get(row.item\_code.lower()).
    - Set item\_details\_by\_code at row.item\_code from (matching\_item or Platform.db.get\_value(“Item”, row.item\_code, list(“item\_name”, “stock\_uom as uom”), as\_dict = true)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in matching\_item → Platform.db.get\_value(“Item”, row.item\_code, list(“item\_name”, “stock\_uom as uom”), as\_dict = true).
  - Set item\_details from item\_details\_by\_code at row.item\_code.
  - For each index in range(self.demand\_number).
    - If self.frequency equals “Monthly”.
      - Set delivery\_date from add\_to\_date(self.from\_date, months = index).
    - Otherwise.
      - Set delivery\_date from add\_to\_date(self.from\_date, weeks = index).
    - Evaluate forecast\_demand.append(mapping(“item\_code” → row.item\_code, “delivery\_date” → delivery\_date, “item\_name” → item\_details.item\_name, “uom” → item\_details.uom, …)).
- For each demand in forecast\_demand.
  - Evaluate self.append(“items”, demand).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L770)

<a id="op-e71c103efc8ace"></a>
### Sales Forecast.generate demand

`operation_enterprise_manufacturing_record_definitions_sales_forecast_business_behavior_sales_forecast_generate_demand`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set(“items”, list()).
- Evaluate self.generate\_manual\_demand().

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate manual demand](operations-037.md#op-6160ed4fb2c3ae).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L5949) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L769)

<a id="op-21bab0adac07df"></a>
### Create mps

`operation_enterprise_manufacturing_record_definitions_sales_forecast_business_behavior_create_master_production_schedule`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Bind local operation postprocess for subsequent calls.
- Set doc from get\_mapped\_doc(“Sales Forecast”, source\_name, mapping(“Sales Forecast” → mapping(“doctype” → “Master Production Schedule”, “validation” → mapping(“docstatus” → list(“=”, 1), “status” → list(“=”, “Planned”) ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L767)

<a id="op-b9ca2fa9b4498c"></a>
### Create mps.postprocess

`operation_enterprise_manufacturing_record_definitions_sales_forecast_business_behavior_create_master_production_schedule_postprocess`

**Inputs** source, doc.

**State and service calls** msgprint with translated “No open Sales Orders found for this Sales Forecast's items. Use {0} to see the forecasted demand.”.format(bold(translated “View MRP”)).

**Local steps**

- Set doc.naming\_series from “MPS.YY.-.######”.
- For each item\_code in dict.fromkeys(generator of d.item\_code for d drawn from source.items).
  - Draw d from source.items.
  - Evaluate doc.append(“select\_items”, mapping(“item\_code” → item\_code)).
- Evaluate doc.set\_to\_date().
- Evaluate doc.get\_actual\_demand().
- If not doc.items.
  - Evaluate Platform.msgprint(translated “No open Sales Orders found for this Sales Forecast's items. Use {0} to see the forecasted demand.”.format(bold(translated “View MRP”)), alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L768)

<a id="op-0368fb97de579d"></a>
### Update sales forecast status

`operation_enterprise_binding_enterprise_manufacturing_doctype_sales_forecast_sales_forecast_update_sales_forecast_status`

**Inputs** sales\_forecast.

**Record and data access** read “Sales Forecast” via get\_value · read “Master Production Schedule” via exists.

**State and service calls** request set\_value on “Sales Forecast”.

**Explicit results** no value.

**Local steps**

- If (not sales\_forecast or Platform.db.get\_value(“Sales Forecast”, sales\_forecast, “docstatus”) differs from 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not sales\_forecast → Platform.db.get\_value(“Sales Forecast”, sales\_forecast, “docstatus”) differs from 1.
  - Return no value.
- Set status from “MPS Generated” when Platform.db.exists(“Master Production Schedule”, mapping(“sales\_forecast” → sales\_forecast)), otherwise “Planned”.
  - Value choice on Platform.db.exists(“Master Production Schedule”, mapping(“sales\_forecast” → sales\_forecast)) — true gives “MPS Generated”, false gives “Planned”.
- Evaluate Platform.db.set\_value(“Sales Forecast”, sales\_forecast, “status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L988)

<a id="op-4bf3474564afab"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_sales_forecast_sales_forecast_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “sales\_forecast”, “transactions” → list(mapping(“label” → translated “MPS”, “items” → list(“Master Production Schedule”)))).

**Local steps**

- Return mapping(“fieldname” → “sales\_forecast”, “transactions” → list(mapping(“label” → translated “MPS”, “items” → list(“Master Production Schedule”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0509.json#L6428) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L772)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-b3edddb66dd7c1"></a>
### Work Order.onload

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_onload`

**Inputs** self.

**Record and data access** resolve a document from “Manufacturing Settings” via get\_doc · read “Stock Settings” via get\_single\_value · read “BOM” via get\_cached\_value.

**Local steps**

- Set ms from Platform.get\_doc(“Manufacturing Settings”).
- Evaluate self.set\_onload(“allow\_editing\_items”, ms.allow\_editing\_of\_items\_and\_quantities\_in\_work\_order).
- Evaluate self.set\_onload(“material\_consumption”, ms.material\_consumption).
- Evaluate self.set\_onload(“backflush\_raw\_materials\_based\_on”, ms.backflush\_raw\_materials\_based\_on).
- Evaluate self.set\_onload(“overproduction\_percentage”, ms.overproduction\_percentage\_for\_work\_order).
- Evaluate self.set\_onload(“transfer\_extra\_materials\_percentage”, ms.transfer\_extra\_materials\_percentage).
- Evaluate self.set\_onload(“show\_create\_job\_card\_button”, self.show\_create\_job\_card\_button()).
- Evaluate self.set\_onload(“operation\_target\_qty”, mapping of d.name → get\_operation\_target\_qty(self, d) for d drawn from self.operations).
  - Draw d from self.operations.
- Evaluate self.set\_onload(“upstream\_process\_loss”, get\_upstream\_process\_loss(self)).
- Evaluate self.set\_onload(“enable\_stock\_reservation”, Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”)).
- If self.bom\_no.
  - If based\_on bound to Platform.get\_cached\_value(“BOM”, self.bom\_no, “backflush\_based\_on”).
    - Evaluate self.set\_onload(“backflush\_raw\_materials\_based\_on”, based\_on).

If control reaches the end, it returns no value.

**Methods declared on this owner** [show create job card button](operations-038.md#op-c1fdc1c8276bf3).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”), Platform.get\_cached\_value(“BOM”, self.bom\_no, “backflush\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L805)
