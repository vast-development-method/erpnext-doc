# Production · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Material requirements planning report

<a id="op-b4baa2b776c2e3"></a>
### Material Requirements Planning Report.get orders to skip

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_orders_to_skip`

**Inputs** self.

**Record and data access** read “Production Plan Sales Order” via get\_all.

**Explicit results** Platform.get\_all(“Production Plan Sales Order”, filters = mapping(“parent” → self.filters.mps), pluck = “sales\_order”).

**Local steps**

- Return Platform.get\_all(“Production Plan Sales Order”, filters = mapping(“parent” → self.filters.mps), pluck = “sales\_order”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0547.json#L2715) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1138)

<a id="op-803a75d10335e6"></a>
### Material Requirements Planning Report.get item wise bin details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_item_wise_bin_details`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** mapping() · \_bin\_details.

**Local steps**

- Set items from (self.fg\_items + self.rm\_items).
- If not items.
  - Return mapping().
- Set \_bin\_details from Platform.\_dict(mapping()).
- Set doctype from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.item\_code, nested operand in the contract.as\_(“actual\_qty”), nested operand in the contract.as\_(“reserved\_stock”), nested opera ….
- Set warehouses from no value.
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(doctype.warehouse.isin(warehouses)).
- Set bin\_data from query.run(as\_dict = true).
- Set work\_order\_reserved from get\_stock\_reserved\_for\_work\_orders(items, warehouses).
- For each row in bin\_data.
  - Set row.reserved\_stock from max((flt(row.reserved\_stock) − work\_order\_reserved.get(row.item\_code, 0.0)), 0.0).
  - If row.item\_code does not belong to \_bin\_details.
    - Set \_bin\_details at row.item\_code from row.
- Evaluate self.update\_mps\_data\_with\_bin\_details(\_bin\_details).
- Return \_bin\_details.

**Methods declared on this owner** [update mps data with bin details](operations-027.md#op-52f1b923cac20b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1133)

<a id="op-52f1b923cac20b"></a>
### Material Requirements Planning Report.update mps data with bin details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_update_master_production_schedule_data_with_bin_details`

**Inputs** self, bin\_details.

**Record and data access** read “Production Plan Sales Order” via get\_all · read “Sales Order Item” via get\_all.

**Explicit results** no value.

**Local steps**

- If not self.filters.mps.
  - Return no value.
- Set items from (self.fg\_items + self.rm\_items).
- If not items.
  - Return no value.
- Set sales\_orders from Platform.get\_all(“Production Plan Sales Order”, filters = mapping(“parent” → self.filters.mps), pluck = “sales\_order”).
- If not sales\_orders.
  - Return no value.
- Set sales\_order\_items from Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → list(“in”, sales\_orders), “docstatus” → 1, “item\_code” → list(“in”, items)), fields = list(“item\_code”, “qty”, “delivered\_qty”, “conversion\_factor”)).
- If not sales\_order\_items.
  - Return no value.
- For each row in sales\_order\_items.
  - Set reserved\_qty from (flt((flt(row.qty) − flt(row.delivered\_qty))) × flt(row.conversion\_factor)).
  - <a id="op-52f1b923cac20b-guard-30"></a>If reserved\_qty ≤ 0.
    - Continue with the next iteration or loop test.
  - If details bound to bin\_details.get(row.item\_code, mapping()).
    - Update details.reserved\_qty using − reserved\_qty.
    - Update details.projected\_qty using + reserved\_qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison reserved\_qty ≤ 0, reserved\_qty = 0 selects the branch that continues with the next loop iteration. With reserved\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-52f1b923cac20b-guard-30)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0547.json#L3790) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1148)

<a id="op-3556ef3df7fc48"></a>
### Material Requirements Planning Report.update sales forecast data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_update_sales_forecast_data`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set sales\_forecast\_data from self.get\_sales\_forecast\_data().
- If not sales\_forecast\_data.
  - Return no value.
- Set rows\_by\_key from mapping().
- For each d in self.mps\_data.
  - Set d.sales\_forecast\_qty from flt(d.sales\_forecast\_qty).
  - Evaluate rows\_by\_key.setdefault(tuple(d.item\_code, getdate(d.delivery\_date)), list()).append(d).
- Set forecast\_by\_key from mapping().
- For each row in sales\_forecast\_data.
  - Set key from tuple(row.item\_code, getdate(row.delivery\_date)).
  - If key belongs to forecast\_by\_key.
    - Set forecast\_by\_key at key.qty from (flt(forecast\_by\_key at key.qty) + flt(row.qty)).
  - Otherwise.
    - Set forecast\_by\_key at key from Platform.\_dict(row).
- For each tuple(key, row) in forecast\_by\_key.items().
  - If rows bound to rows\_by\_key.get(key).
    - Evaluate split\_forecast\_qty(rows, flt(row.qty)).
    - Continue with the next iteration or loop test.
  - Set new\_row from Platform.\_dict(mapping(“item\_code” → row.item\_code, “item\_name” → row.item\_code, “delivery\_date” → row.delivery\_date, “projected\_qty” → 0, …)).
  - Evaluate self.mps\_data.append(new\_row).
  - Set rows\_by\_key at key from list(new\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales forecast data](operations-028.md#op-adb3bf8e6e8309).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1151)

<a id="op-c736ef641b1122"></a>
### Material Requirements Planning Report.get mrp data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_material_requirements_planning_data`

**Inputs** self.

**Explicit results** tuple(self.get\_bucket\_view\_data(data), chart) · tuple(data, chart).

**Local steps**

- Set data from self.get\_detailed\_view\_data().
- Set data from self.filter\_based\_on\_type\_of\_materials(data).
- Set chart from (self.get\_chart\_data(data) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_chart\_data(data) → mapping().
- If self.filters.show\_in\_bucket\_view.
  - Return tuple(self.get\_bucket\_view\_data(data), chart).
- Return tuple(data, chart).

**Methods declared on this owner** [get detailed view data](operations-027.md#op-dbad7cc5edbfe2), [filter based on type of materials](operations-027.md#op-6b658a729cb46b), [get chart data](operations-027.md#op-eef4cbcc460786), [get bucket view data](operations-027.md#op-386cb40e9b48bf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0547.json#L4880) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1137)

<a id="op-6b658a729cb46b"></a>
### Material Requirements Planning Report.filter based on type of materials

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_filter_based_on_type_of_materials`

**Inputs** self, data.

**Explicit results** data · new\_data.

**Local steps**

- Set new\_data from list().
- If self.filters.type\_of\_material equals “All”.
  - Return data.
- Set mapper from mapping(“Finished Goods” → “Manufacture”, “Raw Materials” → “Purchase”).get(self.filters.type\_of\_material).
- For each row in data.
  - If row.type\_of\_material equals mapper.
    - Set row.indent from 0.
    - Evaluate new\_data.append(row).
- Return new\_data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0547.json#L5077) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1122)

<a id="op-eef4cbcc460786"></a>
### Material Requirements Planning Report.get chart data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_chart_data`

**Inputs** self, data.

**Explicit results** self.get\_bucket\_view\_chart\_data(data) · self.get\_detailed\_view\_chart\_data(data).

**Local steps**

- If self.filters.get(“show\_in\_bucket\_view”).
  - Return self.get\_bucket\_view\_chart\_data(data).
- Otherwise.
  - Return self.get\_detailed\_view\_chart\_data(data).

**Methods declared on this owner** [get bucket view chart data](operations-027.md#op-6b74dd5912f411), [get detailed view chart data](operations-027.md#op-34cb0104b04fd5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0547.json#L5313) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1126)

<a id="op-34cb0104b04fd5"></a>
### Material Requirements Planning Report.get detailed view chart data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_detailed_view_chart_data`

**Inputs** self, data.

**Explicit results** mapping(“data” → mapping(“labels” → self.get\_detailed\_chart\_labels(delivery\_dates), “datasets” → list(mapping(“name” → translated “Demand”, “values” → demand\_data), mapping(“name” → translated “Supply”, “v ….

**Local steps**

- Set chart\_data from Platform.\_dict(mapping()).
- Set sorted\_data from sorted(data, key = deferred anonymous expression).
- For each row in sorted\_data.
  - If not row.delivery\_date.
    - Continue with the next iteration or loop test.
  - If getdate(row.delivery\_date) &lt; getdate(today()).
    - Continue with the next iteration or loop test.
  - Set delivery\_date from getdate(row.delivery\_date).
  - If delivery\_date does not belong to chart\_data.
    - Set chart\_data at delivery\_date from Platform.\_dict(mapping(“demand” → 0.0, “supply” → 0.0)).
  - Set demand\_supply\_data from chart\_data at delivery\_date.
  - Update demand\_supply\_data.demand using + math.ceil(flt(row.planned\_qty, self.qty\_precision)).
  - Update demand\_supply\_data.supply using + ((flt(row.in\_hand\_qty) + flt(row.po\_ordered\_qty)) + flt(row.wo\_ordered\_qty)).
- Set demand\_data from list().
- Set supply\_data from list().
- Set delivery\_dates from list(chart\_data).
- For each row in chart\_data.
  - Set value from chart\_data at row.
  - Evaluate demand\_data.append(math.ceil(flt(value.demand))).
  - Evaluate supply\_data.append(math.ceil(flt(value.supply, self.qty\_precision))).
- Return mapping(“data” → mapping(“labels” → self.get\_detailed\_chart\_labels(delivery\_dates), “datasets” → list(mapping(“name” → translated “Demand”, “values” → demand\_data), mapping(“name” → translated “Supply”, “v ….

**Methods declared on this owner** [get detailed chart labels](operations-027.md#op-1c7223339a3b07).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1130)

<a id="op-1c7223339a3b07"></a>
### Material Requirements Planning Report.get detailed chart labels

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_detailed_chart_labels`

**Inputs** self, delivery\_dates.

**Explicit results** list of formatdate(date, date\_format) for date drawn from delivery\_dates.

**Local steps**

- Set date\_format from “dd MMM yyyy” when len(set of date.year for date drawn from delivery\_dates) &gt; 1, otherwise “dd MMM”.
  - Value choice on len(set of date.year for date drawn from delivery\_dates) &gt; 1 — true gives “dd MMM yyyy”, false gives “dd MMM”.
  - Draw date from delivery\_dates.
- Return list of formatdate(date, date\_format) for date drawn from delivery\_dates.
  - Draw date from delivery\_dates.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0547.json#L6368) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1129)

<a id="op-6b74dd5912f411"></a>
### Material Requirements Planning Report.get bucket view chart data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_bucket_view_chart_data`

**Inputs** self, data.

**Explicit results** mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Demand”, “values” → demand\_data), mapping(“name” → translated “Supply”, “values” → supply\_data))), “type” → “bar”, ….

**Local steps**

- Set chart\_data from Platform.\_dict(mapping()).
- Set labels from list().
- Set i from 0.
- For each row in self.dates.
  - If (self.filters.bucket\_size equals “Daily” and i equals 15).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.bucket\_size equals “Daily” → i equals 15.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If (self.filters.bucket\_size equals “Weekly” and i equals 12).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.bucket\_size equals “Weekly” → i equals 12.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set row from Platform.\_dict(row).
  - For each d in data.
    - If (getdate(d.delivery\_date) ≥ getdate(row.from\_date) and getdate(d.delivery\_date) ≤ getdate(row.to\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(d.delivery\_date) ≥ getdate(row.from\_date) → getdate(d.delivery\_date) ≤ getdate(row.to\_date).
      - If row.from\_date does not belong to chart\_data.
        - Update i using + 1.
        - Set label from row.label.
        - If self.filters.bucket\_size equals “Weekly”.
          - Set label from ((formatdate(row.from\_date, “dd”) + “-”) + formatdate(row.to\_date, “dd MMM”)).
        - Evaluate labels.append(label).
        - Set chart\_data at row.from\_date from Platform.\_dict(mapping(“demand” → 0.0, “supply” → 0.0)).
      - Set demand\_supply\_data from chart\_data at row.from\_date.
      - Update demand\_supply\_data.demand using + math.ceil(flt(d.planned\_qty, self.qty\_precision)).
      - Update demand\_supply\_data.supply using + ((flt(d.in\_hand\_qty) + flt(d.po\_ordered\_qty)) + flt(d.wo\_ordered\_qty)).
- Set demand\_data from list().
- Set supply\_data from list().
- For each row in chart\_data.
  - Set value from chart\_data at row.
  - Evaluate demand\_data.append(math.ceil(flt(value.demand))).
  - Evaluate supply\_data.append(math.ceil(flt(value.supply, self.qty\_precision))).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Demand”, “values” → demand\_data), mapping(“name” → translated “Supply”, “values” → supply\_data))), “type” → “bar”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1124)

<a id="op-386cb40e9b48bf"></a>
### Material Requirements Planning Report.get bucket view data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_bucket_view_data`

**Inputs** self, data.

**Explicit results** new\_data.

**Local steps**

- Set new\_data from list().
- Set item\_wise\_data from Platform.\_dict(mapping()).
- For each item in data.
  - If item.item\_code does not belong to item\_wise\_data.
    - Set item\_wise\_data at item.item\_code from Platform.\_dict(mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “lead\_time” → item.lead\_time, “parents\_bom” → item.parent\_bom, …)).
  - Set item\_data from item\_wise\_data at item.item\_code.
  - For each date in self.dates.
    - Set date from Platform.\_dict(date).
    - If date at “from\_date” does not belong to item\_data.
      - Set item\_data at date at “from\_date” from 0.0.
    - If self.filters.bucket\_view equals “Delivery Date”.
      - If (getdate(item.delivery\_date) ≥ getdate(date.from\_date) and getdate(item.delivery\_date) ≤ getdate(date.to\_date)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(item.delivery\_date) ≥ getdate(date.from\_date) → getdate(item.delivery\_date) ≤ getdate(date.to\_date).
        - Update item\_data at date at “from\_date” using + flt(item.required\_qty).
    - Otherwise.
      - If (getdate(item.release\_date) ≥ getdate(date.from\_date) and getdate(item.release\_date) ≤ getdate(date.to\_date)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(item.release\_date) ≥ getdate(date.from\_date) → getdate(item.release\_date) ≤ getdate(date.to\_date).
        - Update item\_data at date at “from\_date” using + flt(item.required\_qty).
- For each row in item\_wise\_data.
  - Evaluate new\_data.append(Platform.\_dict(item\_wise\_data at row)).
- Return new\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0548.json#L1159) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1125)

<a id="op-dbad7cc5edbfe2"></a>
### Material Requirements Planning Report.get detailed view data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_detailed_view_data`

**Inputs** self.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set i from 0.
- Set sorted\_data from sorted(self.mps\_data, key = deferred anonymous expression).
- For each row in sorted\_data.
  - Set rm\_details from (self.item\_rm\_details.get(tuple(row.item\_code, row.get(“bom\_no”))) or self.item\_rm\_details.get(row.item\_code) or Platform.\_dict(mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.item\_rm\_details.get(tuple(row.item\_code, row.get(“bom\_no”))) → self.item\_rm\_details.get(row.item\_code) → Platform.\_dict(mapping()).
  - Set row.indent from 0.
  - Set row.bom\_no from rm\_details.get(“bom\_no”).
  - If not row.sales\_forecast\_qty.
    - Set row.sales\_forecast\_qty from 0.
  - Set row.demand\_qty from max(flt(row.planned\_qty), flt(row.sales\_forecast\_qty)).
  - Set row.planned\_qty from max(flt(row.planned\_qty), flt(row.sales\_forecast\_qty)).
  - If row.get(“is\_adhoc”).
    - Update row.planned\_qty using + row.adhoc\_qty.
  - For each field in tuple(“min\_order\_qty”, “purchase\_uom”, “safety\_stock”, “default\_supplier”).
    - If rm\_details.get(field).
      - Set row at field from rm\_details.get(field).
  - Evaluate self.update\_required\_qty(row).
  - If i differs from 0.
    - Evaluate data.append(Platform.\_dict(mapping())).
  - Update i using + 1.
  - Set row.capacity from 0.
  - Set row.type\_of\_material from get\_type\_of\_material(rm\_details.get(“is\_purchase\_item”), row.bom\_no).
  - If rm\_details.raw\_materials.
    - Set row.capacity from get\_item\_capacity(row.item\_code, self.filters.bucket\_size).
  - Evaluate self.set\_lead\_time(row).
  - Evaluate data.append(row).
  - If rm\_details.raw\_materials.
    - Evaluate self.update\_rm\_details(rm\_details.raw\_materials, row.release\_date, row.required\_qty, rm\_details.bom\_no, …).
- Return data.

**Methods declared on this owner** [update required qty](operations-027.md#op-7a54863a60e811), [set lead time](operations-027.md#op-dfe7d81510b786), [update rm details](operations-028.md#op-d705395a0498e2).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1131)

<a id="op-dfe7d81510b786"></a>
### Material Requirements Planning Report.set lead time

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_materialrequirementsplanningreport_set_lead_time`

**Inputs** self, row.

**Local steps**

- Set lead\_time from get\_item\_lead\_time(row.item\_code, row.type\_of\_material, flt(row.required\_qty, self.qty\_precision)).
- Set row.lead\_time from math.ceil(lead\_time).
- Set row.release\_date from add\_days(row.delivery\_date, negative row.lead\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1143)

<a id="op-68d2ed4aad886c"></a>
### Material Requirements Planning Report.add non planned so

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_add_non_planned_sales_order`

**Inputs** self, row.

**Explicit results** no value.

**Local steps**

- If row.demand\_parts is identical to no value.
  - Set row.demand\_parts from list(list(getdate(row.delivery\_date), flt(row.planned\_qty))).
- Set keys from list of key for key drawn from self.\_so\_details where (key at 0 equals row.item\_code and getdate(key at 1) ≤ getdate(row.delivery\_date)).
  - Draw key from self.\_so\_details, keep a combination only if ((key at 0 equals row.item\_code and getdate(key at 1) ≤ getdate(row.delivery\_date))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key at 0 equals row.item\_code → getdate(key at 1) ≤ getdate(row.delivery\_date).
- If not keys.
  - Return no value.
- For each key in keys.
  - Set qty from flt(self.\_so\_details.pop(key).qty).
  - Set row.adhoc\_qty from (flt(row.adhoc\_qty) + qty).
  - Set row.planned\_qty from (flt(row.planned\_qty) + qty).
  - Evaluate row.demand\_parts.append(list(getdate(key at 1), qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1119)

<a id="op-8b59099ef634fe"></a>
### Material Requirements Planning Report.add bin details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_add_bin_details`

**Inputs** self, row.

**Local steps**

- If bin\_details bound to self.\_bin\_details.get(row.item\_code).
  - Set current\_qty from get\_free\_stock(bin\_details).
  - If current\_qty &gt; 0.
    - Set covered\_qty from cover\_demand(row, current\_qty).
    - Set row.in\_hand\_qty from covered\_qty.
    - Set bin\_details at “actual\_qty” from (flt(bin\_details at “actual\_qty”) − covered\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1117)

<a id="op-6ba97a1803a850"></a>
### Material Requirements Planning Report.add po details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_add_purchase_order_details`

**Inputs** self, row.

**Local steps**

- Set row.po\_ordered\_qty from (flt(row.po\_ordered\_qty) + apply\_dated\_supply(row, self.\_po\_details)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1120)

<a id="op-7fdffba20dca15"></a>
### Material Requirements Planning Report.add wo details

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_add_work_order_details`

**Inputs** self, row.

**Local steps**

- Set row.wo\_ordered\_qty from (flt(row.wo\_ordered\_qty) + apply\_dated\_supply(row, self.\_wo\_details)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1121)

<a id="op-7a54863a60e811"></a>
### Material Requirements Planning Report.update required qty

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_update_required_quantity`

**Inputs** self, row.

**Local steps**

- Set row.demand\_parts from no value.
- Evaluate self.add\_non\_planned\_so(row).
- Evaluate row.demand\_parts.sort(key = deferred anonymous expression).
- Set row.required\_qty from flt(row.planned\_qty).
- Set row.in\_hand\_qty from 0.0.
- Evaluate self.reserve\_safety\_stock(row).
- Evaluate self.add\_bin\_details(row).
- Evaluate self.add\_po\_details(row).
- Evaluate self.add\_wo\_details(row).
- Evaluate row.pop(“demand\_parts”, no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add non planned so](operations-027.md#op-68d2ed4aad886c), [reserve safety stock](operations-027.md#op-c2ee2b3341ff22), [add bin details](operations-027.md#op-8b59099ef634fe), [add po details](operations-027.md#op-6ba97a1803a850), [add wo details](operations-027.md#op-7fdffba20dca15).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1150)

<a id="op-c2ee2b3341ff22"></a>
### Material Requirements Planning Report.reserve safety stock

`operation_enterprise_binding_enterprise_manufacturing_report_material_requirements_planning_report_material_requirements_planning_report_materialrequirementsplanningreport_reserve_safety_stock`

**Inputs** self, row.

**State and service calls** call insert on row.demand\_parts.

**Explicit results** no value.

**Local steps**

- If (not self.filters.add\_safety\_stock or not flt(row.safety\_stock)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.filters.add\_safety\_stock → not flt(row.safety\_stock).
  - Return no value.
- If row.item\_code belongs to self.\_safety\_stock\_reserved.
  - Return no value.
- Evaluate self.\_safety\_stock\_reserved.add(row.item\_code).
- Set bin\_details from self.\_bin\_details.setdefault(row.item\_code, Platform.\_dict(mapping(“actual\_qty” → 0.0, “reserved\_stock” → 0.0))).
- Set available from max(get\_free\_stock(bin\_details), 0.0).
- Set reserved from min(flt(row.safety\_stock), available).
- Set bin\_details.actual\_qty from (flt(bin\_details.actual\_qty) − reserved).
- Update row.required\_qty using + (flt(row.safety\_stock) − reserved).
- Evaluate row.demand\_parts.insert(0, list(row.demand\_parts at 0 at 0, (flt(row.safety\_stock) − reserved))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1142)

<a id="op-07d6f23091eb9f"></a>
### Material Requirements Planning Report.get work order data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_work_order_data`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** wo\_details.

**Local steps**

- Set wo\_details from Platform.\_dict(mapping()).
- Set doctype from Platform.qb.DocType(“Work Order”).
- Set query from nested operand in the contract.qb.from\_(doctype).select((nested operand in the contract.qty − nested operand in the contract.produced\_qty).as\_(“qty”), doctype.production\_item.as\_(“item\_code”), doctype.plan ….
- Set items from (self.fg\_items + self.rm\_items).
- If items.
  - Set query from query.where(doctype.production\_item.isin(items)).
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(doctype.fg\_warehouse.isin(warehouses)).
- Set data from query.run(as\_dict = true).
- For each row in data.
  - Set key from tuple(row.item\_code, row.delivery\_date).
  - If key does not belong to wo\_details.
    - Set wo\_details at key from row.
  - Otherwise.
    - Update wo\_details at key.qty using + row.qty.
- Return wo\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0548.json#L5446) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1146)

<a id="op-55c2a8c07c3f45"></a>
### Material Requirements Planning Report.get purchase order data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_purchase_order_data`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** po\_details.

**Local steps**

- Set po\_details from Platform.\_dict(mapping()).
- Set parent\_doctype from Platform.qb.DocType(“Purchase Order”).
- Set doctype from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(((nested operand in the contract − nested operand  ….
- Set items from (self.fg\_items + self.rm\_items).
- If items.
  - Set query from query.where(doctype.item\_code.isin(items)).
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(doctype.warehouse.isin(warehouses)).
- Set data from query.run(as\_dict = true).
- For each row in data.
  - Set key from tuple(row.item\_code, row.delivery\_date).
  - If key does not belong to po\_details.
    - Set po\_details at key from row.
  - Otherwise.
    - Update po\_details at key.qty using + row.qty.
- If sco bound to self.get\_subcontracted\_data().
  - For each row in sco.
    - Set key from tuple(row.item\_code, row.delivery\_date).
    - If key does not belong to po\_details.
      - Set po\_details at key from row.
    - Otherwise.
      - Update po\_details at key.qty using + row.qty.
- Return po\_details.

**Methods declared on this owner** [get subcontracted data](operations-027.md#op-eea6b3fe691907).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0549.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1140)

<a id="op-d7b8f695c6c980"></a>
### Material Requirements Planning Report.get sales order data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_sales_order_data`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** Platform.\_dict(mapping()) · so\_details.

**Local steps**

- If not self.rm\_items.
  - Return Platform.\_dict(mapping()).
- Set items from list of item for item drawn from self.rm\_items where item does not belong to self.fg\_items.
  - Draw item from self.rm\_items, keep a combination only if (item does not belong to self.fg\_items).
- Set so\_details from Platform.\_dict(mapping()).
- Set parent\_doctype from Platform.qb.DocType(“Sales Order”).
- Set doctype from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(((nested operand in the contract − nested operand  ….
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(doctype.warehouse.isin(warehouses)).
- Set data from query.where(nested operand in the contract.item\_code.isin(items)).run(as\_dict = true) when items, otherwise list().
  - Value choice on items — true gives query.where(doctype.item\_code.isin(items)).run(as\_dict = true), false gives list().
- For each row in data.
  - Set key from tuple(row.item\_code, row.delivery\_date).
  - If key does not belong to so\_details.
    - Set so\_details at key from row.
  - Otherwise.
    - Update so\_details at key.qty using + row.qty.
- If packed\_items bound to self.get\_packed\_items\_sales\_order().
  - For each row in packed\_items.
    - Set key from tuple(row.item\_code, row.delivery\_date).
    - If key does not belong to so\_details.
      - Set so\_details at key from row.
    - Otherwise.
      - Update so\_details at key.qty using + row.qty.
- Return so\_details.

**Methods declared on this owner** [get packed items sales order](operations-027.md#op-3feedbdd672d09).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1144)

<a id="op-3feedbdd672d09"></a>
### Material Requirements Planning Report.get packed items sales order

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_packed_items_sales_order`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set parent\_doctype from Platform.qb.DocType(“Sales Order”).
- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set doctype from Platform.qb.DocType(“Packed Item”).
- Set pending\_qty from (so\_item.qty − so\_item.delivered\_qty).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent\_detail\_docname).select(((nested operand in the contract ×  ….
- If self.rm\_items.
  - Set query from query.where(doctype.item\_code.isin(self.rm\_items)).
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(doctype.warehouse.isin(warehouses)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1139)

<a id="op-eea6b3fe691907"></a>
### Material Requirements Planning Report.get subcontracted data

`operation_enterprise_manufacturing_report_material_requirements_planning_report_business_behavior_material_requirements_planning_report_get_subcontracted_data`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set parent\_doctype from Platform.qb.DocType(“Subcontracting Order”).
- Set doctype from Platform.qb.DocType(“Subcontracting Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select((nested operand in the contract.qty − nested opera ….
- Set items from (self.fg\_items + self.rm\_items).
- If items.
  - Set query from query.where(doctype.item\_code.isin(items)).
- If self.filters.get(“warehouse”).
  - Set warehouses from list(self.filters.get(“warehouse”)).
  - If Platform.db.get\_value(“Warehouse”, self.filters.get(“warehouse”), “is\_group”).
    - Set warehouses from get\_descendants\_of(“Warehouse”, self.filters.get(“warehouse”)).
  - Set query from query.where(doctype.warehouse.isin(warehouses)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0549.json#L3045) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1145)
