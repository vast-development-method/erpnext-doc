# Production · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom update log

<a id="op-5c58bdc5c3d945"></a>
### Generate dependence map

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_generate_dependence_map`

**Inputs** no declared parameters.

**Declared result** defaultdict.

**Explicit results** tuple(child\_parent\_map, parent\_child\_map).

**Local steps**

- Set bom from Platform.qb.DocType(“BOM”).
- Set bom\_item from Platform.qb.DocType(“BOM Item”).
- Set child\_bom from Platform.qb.DocType(“BOM”).as\_(“child\_bom”).
- Set bom\_items from nested operand in the contract(nested operand in the contract).select(bom\_item.bom\_no, bom\_item.parent).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nest ….
- Set child\_parent\_map from defaultdict(list).
- Set parent\_child\_map from defaultdict(list).
- For each row in bom\_items.
  - Evaluate child\_parent\_map at row.bom\_no.append(row.parent).
  - Evaluate parent\_child\_map at row.parent.append(row.bom\_no).
- Return tuple(child\_parent\_map, parent\_child\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L296)

<a id="op-442075c0180ce6"></a>
### Set values in log

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_set_values_in_log`

**Inputs** log\_name, values, commit = false.

**Declared result** no value.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- If not values.
  - Return no value.
- Set bom\_update\_log from Platform.qb.DocType(“BOM Update Log”).
- Set query from Platform.qb.update(bom\_update\_log).where(bom\_update\_log.name equals log\_name).
- For each tuple(key, value) in values.items().
  - Set query from query.set(key, value).
- Evaluate query.run().
- If (commit and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in commit → not Platform.in\_test.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L4142) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L303)

<a id="op-454c03e0b70a86"></a>
### Handle exception

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_handle_exception`

**Inputs** doc.

**Declared result** no value.

**State and service calls** rollback.

**Local steps**

- Evaluate Platform.db.rollback().
- Set error\_log from doc.log\_error(“BOM Update Tool Error”).
- Evaluate set\_values\_in\_log(doc.name, mapping(“status” → “Failed”, “error\_log” → error\_log.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L4482) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L301)

## Record · Bom update tool

<a id="op-52c859e4905afe"></a>
### Enqueue replace bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_tool_business_behavior_enqueue_replace_bill_of_materials`

**Inputs** boms = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** “BOMUpdateLog”.

**Explicit results** update\_log.

**Explicit failure paths** validation helper with BOMMissingError.

**Local steps**

- Bind dependencies BOMMissingError.
- Set boms from (boms or args).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in boms → args.
- If isinstance(boms, str).
  - Set boms from json.loads(boms).
- Set requested from (boms or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in boms → mapping().
- If (not requested.get(“current\_bom”) or not requested.get(“new\_bom”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not requested.get(“current\_bom”) → not requested.get(“new\_bom”).
  - Call the validation error handler Platform.throw(msg = translated “Please mention the Current and New BOM for replacement.”, title = translated “Mandatory”, exc = BOMMissingError).
- Set boms at “current\_bom” from cstr(boms.get(“current\_bom”)).
- Set boms at “new\_bom” from cstr(boms.get(“new\_bom”)).
- If not Platform.has\_permission(“BOM”, “write”, doc = boms at “current\_bom”).
  - Evaluate \_refuse().
- If not Platform.has\_permission(“BOM”, “read”, doc = boms at “new\_bom”).
  - Evaluate \_refuse().
- Bind dependencies get\_ancestor\_boms.
- Set rewritten\_boms from sorted(((set(get\_ancestor\_boms(boms at “current\_bom”)) bitwise or set(get\_ancestor\_boms(boms at “new\_bom”))) − set(boms at “current\_bom”, boms at “new\_bom”))).
- For each parent in rewritten\_boms.
  - Evaluate require\_permission(“BOM”, parent, “write”).
- Set update\_log from create\_bom\_update\_log(boms = boms).
- Return update\_log.

**Values supplied outside this operation** effective access from Platform.has\_permission(“BOM”, “write”, doc = boms at “current\_bom”), Platform.has\_permission(“BOM”, “read”, doc = boms at “new\_bom”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L328)

<a id="op-0fb2a6a05d2558"></a>
### Enqueue update cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_tool_business_behavior_enqueue_update_cost`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** “BOMUpdateLog”.

**Explicit results** update\_log.

**Local steps**

- Set update\_log from create\_bom\_update\_log(update\_type = “Update Cost”).
- Return update\_log.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L6774) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L329)

<a id="op-bd3deb8b9985c2"></a>
### Auto update latest price in all boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_tool_business_behavior_auto_update_latest_price_in_all_bills_of_materials`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read “Manufacturing Settings” via get\_single\_value · read “BOM Update Log” via get\_all.

**Local steps**

- If Platform.db.get\_single\_value(“Manufacturing Settings”, “update\_bom\_costs\_automatically”).
  - Set wip\_log from Platform.get\_all(“BOM Update Log”, fields = list(“creation”, “status”), filters = mapping(“update\_type” → “Update Cost”, “status” → list(“in”, list(“Queued”, “In Progress”))), limit\_page\_length = 1, order\_ ….
  - If (not wip\_log or is\_older\_log(wip\_log at 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not wip\_log → is\_older\_log(wip\_log at 0).
    - Evaluate create\_bom\_update\_log(update\_type = “Update Cost”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “update\_bom\_costs\_automatically”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L6860) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L326)

<a id="op-cfd02b6158b7df"></a>
### Is older log

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_tool_business_behavior_is_older_log`

**Inputs** log.

**Declared result** bool.

**Explicit results** no\_of\_days &gt; 10.

**Local steps**

- Set no\_of\_days from date\_diff(get\_datetime(now()), get\_datetime(log.creation)).
- Return no\_of\_days &gt; 10.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L7143) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L330)

<a id="op-642e598f6124ff"></a>
### Create bom update log

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_tool_business_behavior_create_bill_of_materials_update_log`

**Inputs** boms = no value, update\_type = “Replace BOM”.

**Declared result** “BOMUpdateLog”.

**Record and data access** resolve a document from mapping(“doctype” → “BOM Update Log”, “current\_bom” → current\_bom, “new\_bom” → new\_bom, “update\_type” → update\_type) via get\_doc.

**State and service calls** call submit on Platform.get\_doc(mapping(“doctype” → “BOM Update Log”, “current\_bom” → current\_bom, “new\_bom” → new\_bom, “update\_type” → update\_type)).

**Explicit results** Platform.get\_doc(mapping(“doctype” → “BOM Update Log”, “current\_bom” → current\_bom, “new\_bom” → new\_bom, “update\_type” → update\_type)).submit().

**Local steps**

- Set boms from (boms or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in boms → mapping().
- Set current\_bom from boms.get(“current\_bom”).
- Set new\_bom from boms.get(“new\_bom”).
- Return Platform.get\_doc(mapping(“doctype” → “BOM Update Log”, “current\_bom” → current\_bom, “new\_bom” → new\_bom, “update\_type” → update\_type)).submit().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L327)

## Report · Bom variance report

<a id="op-306601daedfa1d"></a>
### Execute

`operation_enterprise_manufacturing_report_bill_of_materials_variance_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0543.json#L2809) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1054)

<a id="op-863f13fd5a6358"></a>
### Get columns

`operation_enterprise_manufacturing_report_bill_of_materials_variance_report_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Work Order”, “fieldname” → “work\_order”, “fieldtype” → “Link”, “options” → “Work Order”, …)).
- If not filters.get(“bom\_no”).
  - Evaluate columns.extend(list(mapping(“label” → translated “BOM No”, “fieldname” → “bom\_no”, “fieldtype” → “Link”, “options” → “BOM”, …))).
- Evaluate columns.extend(list(mapping(“label” → translated “Finished Good”, “fieldname” → “production\_item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Ordered Qty”, “fieldname” → “q ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0543.json#L2944) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1055)

<a id="op-51d4bf626d735a"></a>
### Get data

`operation_enterprise_manufacturing_report_bill_of_materials_variance_report_business_behavior_get_data`

**Inputs** filters.

**Explicit results** results.

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set query from get\_work\_order\_query(list(“name as work\_order”, “qty”, “produced\_qty”, “production\_item”, …)).
- If (filters.get(“bom\_no”) and not filters.get(“work\_order”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“bom\_no”) → not filters.get(“work\_order”).
  - Set query from query.where(wo.bom\_no equals filters.get(“bom\_no”)).
- If filters.get(“work\_order”).
  - Set query from query.where(wo.name equals filters.get(“work\_order”)).
- Set work\_orders from query.run(as\_dict = true).
- Set materials from get\_materials\_by\_work\_order(list of d.work\_order for d drawn from work\_orders).
  - Draw d from work\_orders.
- Set planned\_loss from get\_planned\_loss\_percentage(set of d.bom\_no for d drawn from work\_orders).
  - Draw d from work\_orders.
- Set results from list().
- For each d in work\_orders.
  - Evaluate results.append(d).
  - Set expected\_output from (flt(d.qty) × (1 − (flt(planned\_loss.get(d.bom\_no)) ÷ 100))).
  - For each data in materials.get(d.work\_order, list()).
    - Set data.required\_qty from ((flt(data.required\_qty) × flt(d.produced\_qty)) ÷ (expected\_output or flt(d.qty))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in expected\_output → flt(d.qty).
    - Evaluate results.append(data).
- Return results.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1056)

<a id="op-a50f806157993b"></a>
### Get planned loss percentage

`operation_enterprise_binding_enterprise_manufacturing_report_bom_variance_report_bom_variance_report_get_planned_loss_percentage`

**Inputs** boms.

**Record and data access** read “BOM” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“in”, list(boms))), fields = list(“name”, “process\_loss\_percentage”), as\_list = true)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“in”, list(boms))), fields = list(“name”, “process\_loss\_percentage”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1125)

<a id="op-b86ddf26fe3f00"></a>
### Get work order query

`operation_enterprise_binding_enterprise_manufacturing_report_bom_variance_report_bom_variance_report_get_work_order_query`

**Inputs** fields.

**Explicit results** Platform.qb.get\_query(“Work Order”, fields = fields, filters = mapping(“docstatus” → 1, “produced\_qty” → list(“&gt;”, 0)), ignore\_permissions = false).

**Local steps**

- Return Platform.qb.get\_query(“Work Order”, fields = fields, filters = mapping(“docstatus” → 1, “produced\_qty” → list(“&gt;”, 0)), ignore\_permissions = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1126)

<a id="op-0fdbcbeba7d060"></a>
### Get materials by work order

`operation_enterprise_binding_enterprise_manufacturing_report_bom_variance_report_bom_variance_report_get_materials_by_work_order`

**Inputs** work\_orders.

**Record and data access** read “Work Order Item” via get\_all.

**Explicit results** mapping() · materials.

**Local steps**

- If not work\_orders.
  - Return mapping().
- Set materials from mapping().
- For each row in Platform.get\_all(“Work Order Item”, fields = list(“parent”, “item\_code as raw\_material\_code”, “required\_qty”, “consumed\_qty”), filters = mapping(“parent” → list(“in”, work\_orders), “parenttype” → “Work Ord ….
  - Evaluate materials.setdefault(row.pop(“parent”), list()).append(row).
- Return materials.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1124)

<a id="op-7be7da9f69dea7"></a>
### Get work orders

`operation_enterprise_manufacturing_report_bill_of_materials_variance_report_business_behavior_get_work_orders`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** query.run(as\_list = true).

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set query from nested operand in the contract(nested operand in the contract).orderby(wo.name).limit(page\_len).offset(start).
- If filters.get(“bom\_no”).
  - Set query from query.where(wo.bom\_no equals filters.get(“bom\_no”)).
- Return query.run(as\_list = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1057)

## Report · Cost of poor quality report

<a id="op-8e8a0f0c28ad68"></a>
### Execute

`operation_enterprise_manufacturing_report_cost_of_poor_quality_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(filters), get\_data(filters)).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return tuple(get\_columns(filters), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1063)

<a id="op-5f1e45acafd654"></a>
### Get data

`operation_enterprise_manufacturing_report_cost_of_poor_quality_report_business_behavior_get_data`

**Inputs** report\_filters.

**Record and data access** read “Operation” via get\_all.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set operations from Platform.get\_all(“Operation”, filters = mapping(“is\_corrective\_operation” → 1)).
- If operations.
  - If report\_filters.get(“operation”).
    - Set operations from list(report\_filters.get(“operation”)).
  - Otherwise.
    - Set operations from list of d.name for d drawn from operations.
      - Draw d from operations.
  - Set job\_card from Platform.qb.DocType(“Job Card”).
  - Set operating\_cost from ((job\_card.hour\_rate × job\_card.total\_time\_in\_mins) ÷ 60.0).as\_(“operating\_cost”).
  - Set item\_code from job\_card.production\_item.as\_(“item\_code”).
  - Set query from nested operand in the contract.qb.from\_(job\_card).select(job\_card.name, job\_card.work\_order, item\_code, job\_card.item\_name, …).where((job\_card.docstatus equals 1 bitwise and job\_card.is\_corrective\_job\_card ….
  - Set query from append\_filters(query, report\_filters, operations, job\_card).
  - Set data from query.run(as\_dict = true).
  - If report\_filters.get(“serial\_no”).
    - Set data from keep\_exact\_serial\_no(data, report\_filters.get(“serial\_no”)).
  - If (report\_filters.get(“from\_date”) or report\_filters.get(“to\_date”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in report\_filters.get(“from\_date”) → report\_filters.get(“to\_date”).
    - Evaluate clip\_to\_date\_range(data, report\_filters).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1065)

<a id="op-670863216a97ee"></a>
### Append filters

`operation_enterprise_manufacturing_report_cost_of_poor_quality_report_business_behavior_append_filters`

**Inputs** query, report\_filters, operations, job\_card.

**Explicit results** query.

**Local steps**

- For each field in tuple(“name”, “work\_order”, “operation”, “workstation”, …).
  - If report\_filters.get(field).
    - If field equals “serial\_no”.
      - Set query from query.where(Locate(report\_filters.get(field), job\_card at field) &gt; 0).
    - Otherwise.
      - If field equals “operation”.
        - Set query from query.where(job\_card at field.isin(operations)).
      - Otherwise.
        - Set query from query.where(job\_card at field equals report\_filters.get(field)).
- If (report\_filters.get(“from\_date”) or report\_filters.get(“to\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in report\_filters.get(“from\_date”) → report\_filters.get(“to\_date”).
  - Set query from query.where(ExistsCriterion(get\_overlapping\_time\_logs(report\_filters, job\_card))).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1062)

<a id="op-cd01e7461c299e"></a>
### Get overlapping time logs

`operation_enterprise_binding_enterprise_manufacturing_report_cost_of_poor_quality_report_cost_of_poor_quality_report_get_overlapping_time_logs`

**Inputs** report\_filters, job\_card.

**Explicit results** query.

**Local steps**

- Set time\_log from Platform.qb.DocType(“Job Card Time Log”).
- Set query from nested operand in the contract.qb.from\_(time\_log).select(time\_log.name).where((time\_log.parent equals job\_card.name bitwise and time\_log.parenttype equals “Job Card”)).
- If report\_filters.get(“from\_date”).
  - Set query from query.where(time\_log.to\_time &gt; report\_filters.get(“from\_date”)).
- If report\_filters.get(“to\_date”).
  - Set query from query.where(time\_log.from\_time &lt; report\_filters.get(“to\_date”)).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1129)

<a id="op-96d7d9773a7954"></a>
### Clip to date range

`operation_enterprise_binding_enterprise_manufacturing_report_cost_of_poor_quality_report_cost_of_poor_quality_report_clip_to_date_range`

**Inputs** data, report\_filters.

**Record and data access** read “Job Card Time Log” via get\_all.

**Explicit results** no value.

**Local steps**

- If not data.
  - Return no value.
- Set start from get\_datetime(report\_filters.get(“from\_date”)) when report\_filters.get(“from\_date”), otherwise no value.
  - Value choice on report\_filters.get(“from\_date”) — true gives get\_datetime(report\_filters.get(“from\_date”)), false gives no value.
- Set end from get\_datetime(report\_filters.get(“to\_date”)) when report\_filters.get(“to\_date”), otherwise no value.
  - Value choice on report\_filters.get(“to\_date”) — true gives get\_datetime(report\_filters.get(“to\_date”)), false gives no value.
- Set minutes from defaultdict(float).
- For each log in Platform.get\_all(“Job Card Time Log”, filters = mapping(“parent” → list(“in”, list of row.name for row drawn from data), “parenttype” → “Job Card”), fields = list(“parent”, “from\_time”, “to\_time”, “time\_in\_mins”)).
  - Draw row from data.
  - Update minutes at log.parent using + get\_minutes\_in\_range(log, start, end).
- For each row in data.
  - Set row.total\_time\_in\_mins from flt(minutes at row.name, 2).
  - Set row.operating\_cost from ((flt(row.hour\_rate) × minutes at row.name) ÷ 60.0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1127)

<a id="op-afe713d4868ac3"></a>
### Get minutes in range

`operation_enterprise_binding_enterprise_manufacturing_report_cost_of_poor_quality_report_cost_of_poor_quality_report_get_minutes_in_range`

**Inputs** log, start, end.

**Explicit results** 0 · ((flt(log.time\_in\_mins) × max(overlap, 0)) ÷ duration).

**Local steps**

- Set tuple(log\_start, log\_end) from tuple(get\_datetime(log.from\_time), get\_datetime(log.to\_time)).
- Set duration from (log\_end − log\_start).total\_seconds().
- <a id="op-afe713d4868ac3-guard-4"></a>If duration ≤ 0.
  - Return 0.
- Set overlap from (min(log\_end, (end or log\_end)) − max(log\_start, (start or log\_start))).total\_seconds().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in end → log\_end.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in start → log\_start.
- Return ((flt(log.time\_in\_mins) × max(overlap, 0)) ÷ duration).

**Derived branch illustrations**

- At the comparison duration ≤ 0, duration = 0 selects the branch that returns 0. With duration = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-afe713d4868ac3-guard-4)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1128)

<a id="op-5249b1fe7b20c4"></a>
### Keep exact serial no

`operation_enterprise_binding_enterprise_manufacturing_report_cost_of_poor_quality_report_cost_of_poor_quality_report_keep_exact_serial_no`

**Inputs** data, serial\_no.

**Explicit results** list of row for row drawn from data where serial\_no belongs to get\_serial\_nos(row.serial\_no).

**Local steps**

- Return list of row for row drawn from data where serial\_no belongs to get\_serial\_nos(row.serial\_no).
  - Draw row from data, keep a combination only if (serial\_no belongs to get\_serial\_nos(row.serial\_no)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1130)

<a id="op-e909e7186ccc89"></a>
### Get columns

`operation_enterprise_manufacturing_report_cost_of_poor_quality_report_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Job Card”, “fieldtype” → “Link”, “fieldname” → “name”, “options” → “Job Card”, …), mapping(“label” → translated “Work Order”, “fieldtype” → “Link”, “fieldname” → “work\_or ….

**Local steps**

- Return list(mapping(“label” → translated “Job Card”, “fieldtype” → “Link”, “fieldname” → “name”, “options” → “Job Card”, …), mapping(“label” → translated “Work Order”, “fieldtype” → “Link”, “fieldname” → “work\_or ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1064)

## Service · Dashboard fixtures

<a id="op-53aab65769630b"></a>
### Get data

`operation_enterprise_manufacturing_dashboard_fixtures_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(mapping(“dashboards” → get\_dashboards(), “charts” → get\_charts(), “number\_cards” → get\_number\_cards())).

**Local steps**

- Return Platform.\_dict(mapping(“dashboards” → get\_dashboards(), “charts” → get\_charts(), “number\_cards” → get\_number\_cards())).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L294) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L142)
