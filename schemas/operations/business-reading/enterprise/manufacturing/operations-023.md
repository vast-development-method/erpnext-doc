# Production · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-c90c5d1c183ad1"></a>
### Make subcontracting po.set missing values

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_subcontracting_po_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set \_item\_details from get\_subcontracting\_boms\_for\_finished\_goods(source.finished\_good).
- Set pending\_qty from (source.for\_quantity − source.manufactured\_qty).
- Set service\_item\_qty from (flt(\_item\_details.service\_item\_qty) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(\_item\_details.service\_item\_qty) → 1.0.
- Set fg\_item\_qty from (flt(\_item\_details.finished\_good\_qty) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(\_item\_details.finished\_good\_qty) → 1.0.
- Set target.is\_subcontracted from 1.
- Set target.supplier\_warehouse from source.wip\_warehouse.
- Evaluate target.append(“items”, mapping(“item\_code” → \_item\_details.service\_item, “fg\_item” → source.finished\_good, “uom” → \_item\_details.service\_item\_uom, “stock\_uom” → \_item\_details.service\_item\_uom, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_item\_details.conversion\_factor → 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L855)

<a id="op-4daba8c4f176c3"></a>
### Merge time logs per job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_merge_time_logs_per_job_card`

**Inputs** time\_logs.

**Explicit results** merged.

**Local steps**

- Set time\_logs from list of Platform.\_dict(log) for log drawn from time\_logs.
  - Draw log from time\_logs.
- Set merged from list of log for log drawn from time\_logs where not log.name.
  - Draw log from time\_logs, keep a combination only if (not log.name).
- For each name in dict.fromkeys(generator of log.name for log drawn from time\_logs where log.name).
  - Draw log from time\_logs, keep a combination only if (log.name).
  - For each log in sorted(generator of log for log drawn from time\_logs where log.name equals name, key = deferred anonymous expression).
    - Draw log from time\_logs, keep a combination only if (log.name equals name).
    - If (merged and merged at negative 1.name equals name and log.from\_time &lt; merged at negative 1.to\_time).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in merged → merged at negative 1.name equals name → log.from\_time &lt; merged at negative 1.to\_time.
      - Set merged at negative 1.to\_time from max(merged at negative 1.to\_time, log.to\_time).
    - Otherwise.
      - Evaluate merged.append(log).
- Return merged.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L856)

<a id="op-cba42268f42d66"></a>
### Get workstation minutes

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_get_workstation_minutes`

**Inputs** time\_logs.

**Explicit results** minutes.

**Local steps**

- Set tuple(intervals, minutes) from tuple(list(), 0.0).
- For each row in time\_logs.
  - If (row.from\_time and (row.to\_time or flt(row.time\_in\_mins))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.from\_time → (row.to\_time or flt(row.time\_in\_mins)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.to\_time → flt(row.time\_in\_mins).
    - Set start from get\_datetime(row.from\_time).
    - Set end from get\_datetime(row.to\_time) when row.to\_time, otherwise add\_to\_date(start, minutes = flt(row.time\_in\_mins)).
      - Value choice on row.to\_time — true gives get\_datetime(row.to\_time), false gives add\_to\_date(start, minutes = flt(row.time\_in\_mins)).
    - Evaluate intervals.append(tuple(start, end)).
  - Otherwise.
    - Update minutes using + flt(row.time\_in\_mins).
- Set current\_start, current\_end from no value.
- For each tuple(start, end) in sorted(intervals).
  - If (current\_end and start ≤ current\_end).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_end → start ≤ current\_end.
    - Set current\_end from max(current\_end, end).
    - Continue with the next iteration or loop test.
  - If current\_end.
    - Update minutes using + time\_diff\_in\_minutes(current\_end, current\_start).
  - Set tuple(current\_start, current\_end) from tuple(start, end).
- If current\_end.
  - Update minutes using + time\_diff\_in\_minutes(current\_end, current\_start).
- Return minutes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L810)

<a id="op-b1b3dbc7779d02"></a>
### Validate job card submitted for manufacture

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_validate_job_card_submitted_for_manufacture`

**Inputs** job\_card.

**Explicit failure paths** validation helper — translated “Submit Job Card {0} before making its Manufacture entry”.format(get\_link\_to\_form(“Job Card”, job\_card.name)).

**Local steps**

- <a id="op-b1b3dbc7779d02-guard-2"></a>If job\_card.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Submit Job Card {0} before making its Manufacture entry”.format(get\_link\_to\_form(“Job Card”, job\_card.name))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison job\_card.docstatus differs from 1, job\_card.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Submit Job Card {0} before making its Manufacture entry”.format(get\_link\_to\_form(“Job Card”, job\_card.name)). With job\_card.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b1b3dbc7779d02-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L857)

<a id="op-2a77311f532fc8"></a>
### Get sorted working hours

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_get_sorted_working_hours`

**Inputs** workstation\_doc.

**Explicit results** sorted(generator of row for row drawn from workstation\_doc.working\_hours where row.enabled, key = deferred anonymous expression).

**Local steps**

- Return sorted(generator of row for row drawn from workstation\_doc.working\_hours where row.enabled, key = deferred anonymous expression).
  - Draw row from workstation\_doc.working\_hours, keep a combination only if (row.enabled).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L809)

<a id="op-f90e53beb8d96e"></a>
### Make time log

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_make_time_log`

**Inputs** kwargs.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Local steps**

- If isinstance(kwargs, str).
  - Set kwargs from json.loads(kwargs).
- Set kwargs from Platform.\_dict(kwargs).
- Set doc from Platform.get\_doc(“Job Card”, kwargs.job\_card\_id).
- Evaluate Platform.has\_permission(“Job Card”, “write”, doc = doc, throw = true).
- Evaluate doc.validate\_docstatus().
- Evaluate doc.validate\_sequence\_id().
- Evaluate doc.add\_time\_log(kwargs).
- Evaluate doc.set\_status(update\_status = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “write”, doc = doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L470)

<a id="op-d2ccc6c7144e38"></a>
### Get operation details

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_get_operation_details`

**Inputs** work\_order, operation.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Work Order Operation” via get\_all.

**Explicit results** Platform.get\_all(“Work Order Operation”, fields = list(“name”, “idx”), filters = mapping(“parent” → work\_order, “operation” → operation)).

**Local steps**

- Evaluate Platform.has\_permission(“Work Order”, “read”, doc = work\_order, throw = true).
- If (work\_order and operation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order → operation.
  - Return Platform.get\_all(“Work Order Operation”, fields = list(“name”, “idx”), filters = mapping(“parent” → work\_order, “operation” → operation)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “read”, doc = work\_order, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L380)

<a id="op-dbad5809afb8c6"></a>
### Get operations

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_get_operations`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Work Order Operation” via get\_all.

**State and service calls** msgprint with translated “Please select a Work Order first.”.

**Explicit results** list() · Platform.get\_all(“Work Order Operation”, filters = args, fields = list(“operation”), limit\_start = start, limit\_page\_length = page\_len, …).

**Local steps**

- If not filters.get(“work\_order”).
  - Evaluate Platform.msgprint(translated “Please select a Work Order first.”).
  - Return list().
- Evaluate Platform.has\_permission(“Work Order”, “read”, doc = filters.get(“work\_order”), throw = true).
- Set args from mapping(“parent” → filters.get(“work\_order”)).
- If txt.
  - Set args at “operation” from tuple(“like”, formatted text %{txt}%).
- Return Platform.get\_all(“Work Order Operation”, filters = args, fields = list(“operation”), limit\_start = start, limit\_page\_length = page\_len, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “read”, doc = filters.get(“work\_order”), throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L381)

<a id="op-4d9d37be5bb45b"></a>
### Make material request

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_material_request`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** doclist.

**Local steps**

- Set shortages from get\_shortages\_to\_request(source\_name).
- Set pending from get\_pending\_qty\_to\_request(source\_name).
- Set allow\_excess\_transfer from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).
- Bind local operation update\_item for subsequent calls.
- Bind local operation can\_request for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Job Card”, source\_name, mapping(“Job Card” → mapping(“doctype” → “Material Request”, “field\_map” → mapping(“name” → “job\_card”)), “Job Card Item” → mapping(“doctype” → “Material Request Ite ….
- Return doclist.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L847)

<a id="op-7c4f618c412b9a"></a>
### Make material request.update item

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_material_request_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set target.warehouse from source\_parent.wip\_warehouse.
- If shortages is distinct from no value.
  - Set target.qty from shortages at obj.name.
- If pending at obj.name &gt; 0.
  - Set target.qty from min(flt(target.qty), pending at obj.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L850)

<a id="op-9a372db8de65d9"></a>
### Make material request.can request

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_material_request_can_request`

**Inputs** row.

**Explicit results** false · (allow\_excess\_transfer or pending at row.name &gt; 0).

**Local steps**

- If (shortages is distinct from no value and row.name does not belong to shortages).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shortages is distinct from no value → row.name does not belong to shortages.
  - Return false.
- Return (allow\_excess\_transfer or pending at row.name &gt; 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in allow\_excess\_transfer → pending at row.name &gt; 0.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L848)

<a id="op-c6051515bb1b12"></a>
### Make material request.set missing values

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_material_request_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.material\_request\_type from “Material Transfer”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L849)

<a id="op-db0b65d27ec5f2"></a>
### Get pending qty to request

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_get_pending_qty_to_request`

**Inputs** job\_card.

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Explicit results** mapping of item.name → flt((flt(item.required\_qty) − flt(requested.get(item.name))), item.precision(“required\_qty”)) for item drawn from doc.items.

**Local steps**

- Set doc from Platform.get\_doc(“Job Card”, job\_card).
- Set requested from doc.get\_requested\_qty\_by\_item().
- Return mapping of item.name → flt((flt(item.required\_qty) − flt(requested.get(item.name))), item.precision(“required\_qty”)) for item drawn from doc.items.
  - Draw item from doc.items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L807)

<a id="op-1559fcd8a39f84"></a>
### Get shortages to request

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_get_shortages_to_request`

**Inputs** job\_card.

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Explicit results** no value · mapping of row at “name” → row at “shortage\_qty” for row drawn from shortages.

**Local steps**

- If not (Platform.flags.args or mapping()).get(“only\_shortage”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.args → mapping().
  - Return no value.
- Set shortages from Platform.get\_doc(“Job Card”, job\_card).get\_material\_shortages().
- Return mapping of row at “name” → row at “shortage\_qty” for row drawn from shortages.
  - Draw row from shortages.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L808)

<a id="op-d494d75b5a7f3d"></a>
### Make stock entry

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_stock_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** doclist.

**Local steps**

- Bind local operation update\_item for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Set allow\_excess\_transfer from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).
- Set doclist from get\_mapped\_doc(“Job Card”, source\_name, mapping(“Job Card” → mapping(“doctype” → “Stock Entry”, “field\_map” → mapping(“name” → “job\_card”, “for\_quantity” → “fg\_completed\_qty”)), “Job Card Item” → mapping(“ ….
- Return doclist.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L851)

<a id="op-630802bf1bb9ff"></a>
### Make stock entry.update item

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_stock_entry_update_item`

**Inputs** source, target, source\_parent.

**Local steps**

- Set target.t\_warehouse from source\_parent.wip\_warehouse.
- If not target.conversion\_factor.
  - Set target.conversion\_factor from 1.
- Set pending\_rm\_qty from (flt(source.required\_qty) − flt(source.transferred\_qty)).
- Set target.qty from pending\_rm\_qty when pending\_rm\_qty &gt; 0, otherwise flt(source.required\_qty).
  - Value choice on pending\_rm\_qty &gt; 0 — true gives pending\_rm\_qty, false gives flt(source.required\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L853)

<a id="op-91fbccb8364acf"></a>
### Make stock entry.set missing values

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_stock_entry_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Work Order” via get\_value · read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “This Job Card has no raw materials to transfer.” · validation helper — translated “Please set the Target Warehouse in the Job Card” · validation helper — translated “Please set the WIP Warehouse in the Job Card”.

**Local steps**

- If not source.items.
  - Call the validation error handler Platform.throw(translated “This Job Card has no raw materials to transfer.”).
- If (source.finished\_good and not source.target\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.finished\_good → not source.target\_warehouse.
  - Call the validation error handler Platform.throw(translated “Please set the Target Warehouse in the Job Card”).
- If (not source.skip\_material\_transfer or source.backflush\_from\_wip\_warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not source.skip\_material\_transfer → source.backflush\_from\_wip\_warehouse.
  - If not source.wip\_warehouse.
    - Call the validation error handler Platform.throw(translated “Please set the WIP Warehouse in the Job Card”).
- Set target.purpose from “Material Transfer for Manufacture”.
- Set target.from\_bom from 1.
- If source.semi\_fg\_bom.
  - Set target.bom\_no from source.semi\_fg\_bom.
- Set pending\_fg\_qty from (flt(source.get(“for\_quantity”, 0)) − flt(source.get(“transferred\_qty”, 0))).
- Set target.fg\_completed\_qty from pending\_fg\_qty when pending\_fg\_qty &gt; 0, otherwise 0.
  - Value choice on pending\_fg\_qty &gt; 0 — true gives pending\_fg\_qty, false gives 0.
- Evaluate target.set\_missing\_values().
- Evaluate target.set\_stock\_entry\_type().
- Bind dependencies set\_previous\_operation\_serial\_batch.
- Set wo\_allows\_alternate\_item from Platform.db.get\_value(“Work Order”, target.work\_order, “allow\_alternative\_item”).
- For each item in target.items.
  - Set item.allow\_alternative\_item from int((wo\_allows\_alternate\_item and Platform.get\_cached\_value(“Item”, item.item\_code, “allow\_alternative\_item”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in wo\_allows\_alternate\_item → Platform.get\_cached\_value(“Item”, item.item\_code, “allow\_alternative\_item”).
  - Evaluate set\_previous\_operation\_serial\_batch(target, item).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “allow\_alternative\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L852)

<a id="op-963dd6eb9ea9ac"></a>
### Time diff in minutes

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_time_diff_in_minutes`

**Inputs** string\_ed\_date, string\_st\_date.

**Explicit results** (time\_diff(string\_ed\_date, string\_st\_date).total\_seconds() ÷ 60).

**Local steps**

- Return (time\_diff(string\_ed\_date, string\_st\_date).total\_seconds() ÷ 60).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0475.json#L2578) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L471)

<a id="op-f31e713a38d057"></a>
### Get job details

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_get_job_details`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** execute a supplied database query.

**Explicit results** events.

**Local steps**

- Set events from list().
- Set event\_color from mapping(“Completed” → “#cdf5a6”, “Material Transferred” → “#ffdd9e”, “Partially Transferred” → “#ffe5b4”, “Work In Progress” → “#D3D3D3”).
- Bind dependencies get\_filters\_cond, get\_match\_cond.
- Set conditions from (get\_filters\_cond(“Job Card”, filters, list()) + get\_match\_cond(“Job Card”)).
- Set job\_cards from Platform.db.sql(formatted text  SELECT ′tabJob Card′.name, ′tabJob Card′.work\_order,  ′tabJob Card′.status, ifnull(′tabJob Card′.remarks, ''),  min(′tabJob Card Time Log′.from\_t, as\_dict = 1).
- For each d in job\_cards.
  - Set subject\_data from list().
  - For each field in list(“name”, “work\_order”, “remarks”).
    - If not d.get(field).
      - Continue with the next iteration or loop test.
    - Evaluate subject\_data.append(d.get(field)).
  - Set color from event\_color.get(d.status).
  - Set job\_card\_data from mapping(“from\_time” → d.from\_time, “to\_time” → d.to\_time, “name” → d.name, “subject” → whitespace '\\n'.join(subject\_data), …).
    - Value choice on color — true gives color, false gives “#89bcde”.
  - Evaluate events.append(job\_card\_data).
- Return events.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L379)

<a id="op-0337f9adf31eb9"></a>
### Make corrective job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_corrective_job_card`

**Inputs** source\_name, operation = no value, for\_operation = no value, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Job Card”, source\_name, mapping(“Job Card” → mapping(“doctype” → “Job Card”, “field\_map” → mapping(“name” → “for\_job\_card”))), target\_doc, …).
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L845)

<a id="op-e7e2a9dce46166"></a>
### Make corrective job card.set missing values

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_corrective_job_card_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.is\_corrective\_job\_card from 1.
- Set target.operation from operation.
- Set target.for\_operation from for\_operation.
- Set target.total\_completed\_qty from 0.
- Set target.process\_loss\_qty from 0.
- Set target.pending\_qty from 0.
- Evaluate target.set(“time\_logs”, list()).
- Evaluate target.set(“employee”, list()).
- Evaluate target.set(“items”, list()).
- Evaluate target.set(“sub\_operations”, list()).
- Evaluate target.set\_sub\_operations().
- Evaluate target.get\_required\_items().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L846)

<a id="op-44d272cd076dc1"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_job_card_job_card_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “job\_card”, “non\_standard\_fieldnames” → mapping(“Quality Inspection” → “reference\_name”), “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Material R ….

**Local steps**

- Return mapping(“fieldname” → “job\_card”, “non\_standard\_fieldnames” → mapping(“Quality Inspection” → “reference\_name”), “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Material R ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0475.json#L4739) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L472)

<a id="op-f9ee9dc92f4489"></a>
### Get work order job cards

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_work_order_job_cards`

**Inputs** work\_order, start = 0, page\_length = 20, txt = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** get\_timer\_rows(mapping(“work\_order” → work\_order), or\_filters = list of list(field, “like”, formatted text %{txt}%) for field drawn from SEARCH\_FIELDS when txt, otherwise no value, start = cint(start), pag ….

**Local steps**

- Evaluate Platform.has\_permission(“Work Order”, “read”, doc = work\_order, throw = true).
- Return get\_timer\_rows(mapping(“work\_order” → work\_order), or\_filters = list of list(field, “like”, formatted text %{txt}%) for field drawn from SEARCH\_FIELDS when txt, otherwise no value, start = cint(start), pag ….
  - Value choice on txt — true gives list of list(field, “like”, formatted text %{txt}%) for field drawn from SEARCH\_FIELDS, false gives no value.
  - Draw field from SEARCH\_FIELDS.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “read”, doc = work\_order, throw = true).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L867)

<a id="op-120291bf7d5bb6"></a>
### Get job card timer

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_job_card_timer`

**Inputs** job\_card.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** get\_timer\_rows(mapping(“name” → job\_card)) at 0.

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “read”, doc = job\_card, throw = true).
- Return get\_timer\_rows(mapping(“name” → job\_card)) at 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “read”, doc = job\_card, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L862)
