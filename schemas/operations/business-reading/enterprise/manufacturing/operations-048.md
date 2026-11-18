# Production · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workstation

[Record definition](../../../../data/record-types/workstation.json)

<a id="op-ae77b13977cf3b"></a>
### Workstation.validate overlap for operation timings

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_validate_overlap_for_operation_timings`

**Inputs** self.

**Explicit failure paths** validation helper with OverlapError — translated “Row #{0}: Timings conflicts with row {1}”.format(d.idx, comma\_and(existing)).

**Local steps**

- For each d in self.get(“working\_hours”).
  - If not d.enabled.
    - Continue with the next iteration or loop test.
  - Set wh from Platform.qb.DocType(“Workstation Working Hour”).
  - Set existing from nested operand in the contract(nested operand in the contract).select(wh.idx).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ….
  - If existing.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Timings conflicts with row {1}”.format(d.idx, comma\_and(existing)), OverlapError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1001)

<a id="op-18119b76125b05"></a>
### Workstation.update bom operation

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_update_bill_of_materials_operation`

**Inputs** self.

**Record and data access** execute query text (SELECT, BOM Operation).

**State and service calls** execute a supplied database query.

**Local steps**

- Set bom\_list from Platform.db.sql(query text (SELECT, BOM Operation), self.name).
- For each bom\_no in bom\_list.
  - Evaluate Platform.db.sql(“update ′tabBOM Operation′\\n\\t\\t\\t\\tset hour\_rate = %s, operating\_cost = %s \* time\_in\_mins / 60\\n\\t\\t\\t\\twher …”, tuple(self.hour\_rate, self.hour\_rate, bom\_no at 0, self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L79) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L998)

<a id="op-45cd0de80d990e"></a>
### Workstation.validate workstation holiday

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_validate_workstation_holiday`

**Inputs** self, schedule\_date, skip\_holiday\_list\_check = false.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** schedule\_date · self.validate\_workstation\_holiday(schedule\_date, skip\_holiday\_list\_check = true).

**Local steps**

- If (not skip\_holiday\_list\_check and (not self.holiday\_list or cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_production\_on\_holidays”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not skip\_holiday\_list\_check → (not self.holiday\_list or cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_production\_on\_holidays”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.holiday\_list → cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_production\_on\_holidays”)).
  - Return schedule\_date.
- If schedule\_date belongs to tuple(get\_holidays(self.holiday\_list)).
  - Set schedule\_date from add\_days(schedule\_date, 1).
  - Return self.validate\_workstation\_holiday(schedule\_date, skip\_holiday\_list\_check = true).
- Return schedule\_date.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_production\_on\_holidays”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L863) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1003)

<a id="op-cb581083a44382"></a>
### Workstation.start job

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_start_job`

**Inputs** self, job\_card, from\_time, employee.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call save on doc.

**Explicit results** doc.

**Local steps**

- Set doc from self.get\_open\_job\_card(job\_card, “write”).
- Evaluate doc.append(“time\_logs”, mapping(“from\_time” → from\_time, “employee” → employee)).
- Evaluate doc.save().
- Return doc.

**Methods declared on this owner** [get open job card](operations-048.md#op-ed7796f4a0b5e0).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L997)

<a id="op-1586c745fae8a3"></a>
### Workstation.complete job

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_workstation_complete_job`

**Inputs** self, job\_card, qty, to\_time.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call save on doc · call submit on doc.

**Explicit results** doc.

**Local steps**

- Set doc from self.get\_open\_job\_card(job\_card, “submit”).
- Set pending\_qty from flt(qty).
- For each row in doc.time\_logs.
  - If not row.to\_time.
    - Set row.to\_time from to\_time.
    - Set row.completed\_qty from pending\_qty.
    - Set pending\_qty from 0.
- Evaluate doc.save().
- Evaluate doc.submit().
- Return doc.

**Methods declared on this owner** [get open job card](operations-048.md#op-ed7796f4a0b5e0).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L990)

<a id="op-ed7796f4a0b5e0"></a>
### Workstation.get open job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_workstation_workstation_get_open_job_card`

**Inputs** self, job\_card, ptype.

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Job Card {0} is not open”.format(get\_link\_to\_form(“Job Card”, doc.name)) · validation helper — translated “Job Card {0} is not for workstation {1}”.format(get\_link\_to\_form(“Job Card”, doc.name), Platform.bold(self.name)).

**Local steps**

- Set doc from Platform.get\_doc(“Job Card”, job\_card).
- Evaluate doc.check\_permission(ptype).
- <a id="op-ed7796f4a0b5e0-guard-5"></a>If doc.docstatus differs from 0.
  - Call the validation error handler Platform.throw(translated “Job Card {0} is not open”.format(get\_link\_to\_form(“Job Card”, doc.name))).
- If doc.workstation differs from self.name.
  - Call the validation error handler Platform.throw(translated “Job Card {0} is not for workstation {1}”.format(get\_link\_to\_form(“Job Card”, doc.name), Platform.bold(self.name))).
- Return doc.

**Derived branch illustrations**

- At the comparison doc.docstatus differs from 0, doc.docstatus = 1 (submitted) selects the branch that calls the validation-error handler with translated “Job Card {0} is not open”.format(get\_link\_to\_form(“Job Card”, doc.name)). With doc.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ed7796f4a0b5e0-guard-5)

**Values supplied outside this operation** effective access from doc.check\_permission(ptype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1119)

<a id="op-424f92dc6eefd4"></a>
### Get job cards

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_workstation_get_job_cards`

**Inputs** workstation.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Job Card” via get\_list · read “Manufacturing Settings” via get\_single\_value · read “Employee” via get\_value · read “Item” via get\_cached\_value.

**Explicit results** jc\_data.

**Local steps**

- If Platform.has\_permission(“Job Card”, “read”).
  - Set jc\_data from Platform.get\_list(“Job Card”, fields = list(“name”, “production\_item”, “work\_order”, “operation”, …), filters = mapping(“workstation” → workstation, “is\_subcontracted” → 0, “docstatus” → tuple(“&lt;”, 2), “st ….
  - Set job\_cards from list of row.name for row drawn from jc\_data.
    - Draw row from jc\_data.
  - Set time\_logs from get\_time\_logs(job\_cards).
  - Set allow\_excess\_transfer from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).
  - Set user\_employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user), “name”).
  - For each row in jc\_data.
    - If row.status equals “Open”.
      - Set row.status from “Not Started”.
    - Set item\_code from (row.finished\_good or row.production\_item).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.finished\_good → row.production\_item.
    - Set row.fg\_uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
    - Set row.status\_colour from get\_status\_color(row.status).
    - Set row.job\_card\_link from formatted text   &lt;a class="ellipsis" data-doctype="Job Card" data-name="{row.name}" href="/app/job-card/{row.name}" title="" data-original-title="{row.name}"&gt;{ro.
    - Set row.operation\_link from formatted text   &lt;a class="ellipsis" data-doctype="Operation" data-name="{row.operation}" href="/app/operation/{row.operation}" title="" data-original-title="{ro.
    - Set row.work\_order\_link from get\_link\_to\_form(“Work Order”, row.work\_order).
    - Set row.time\_logs from time\_logs.get(row.name, list()).
    - Set row.make\_material\_request from false.
    - If (row.for\_quantity &gt; row.transferred\_qty or allow\_excess\_transfer).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.for\_quantity &gt; row.transferred\_qty → allow\_excess\_transfer.
      - Set row.make\_material\_request from true.
    - Set row.user\_employee from user\_employee.
  - Return jc\_data.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “read”) · configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”), Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1118)

<a id="op-b93437cb501ffc"></a>
### Get status color

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_get_status_color`

**Inputs** status.

**Explicit results** color\_map.get(status, “blue”).

**Local steps**

- Set color\_map from mapping(“Pending” → “blue”, “In Process” → “yellow”, “Submitted” → “blue”, “Open” → “gray”, …).
- Return color\_map.get(status, “blue”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L983)

<a id="op-8b6c642c9bb8e8"></a>
### Get raw materials

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_get_raw_materials`

**Inputs** job\_card.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Job Card” via get\_all · read “Bin” via get\_value.

**Explicit results** raw\_materials.

**Explicit failure paths** validation helper — translated “This Job Card has no raw materials to transfer.”.

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “read”, doc = job\_card, throw = true).
- Set raw\_materials from Platform.get\_all(“Job Card”, fields = list(“′tabJob Card′.′skip\_material\_transfer′”, “′tabJob Card′.′backflush\_from\_wip\_warehouse′”, “′tabJob Card′.′wip\_warehouse′”, “′tabJob Card Item′.′parent′”, …), filt ….
- If (not raw\_materials or not raw\_materials at 0.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not raw\_materials → not raw\_materials at 0.item\_code.
  - Call the validation error handler Platform.throw(translated “This Job Card has no raw materials to transfer.”).
- For each row in raw\_materials.
  - Set warehouse from row.source\_warehouse.
  - If (row.skip\_material\_transfer and row.backflush\_from\_wip\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.skip\_material\_transfer → row.backflush\_from\_wip\_warehouse.
    - Set warehouse from row.wip\_warehouse.
  - Set row.stock\_qty from (Platform.db.get\_value(“Bin”, mapping(“item\_code” → row.item\_code, “warehouse” → warehouse), “actual\_qty”) or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Bin”, mapping(“item\_code” → row.item\_code, “warehouse” → warehouse), “actual\_qty”) → 0.0.
  - Set row.warehouse from warehouse.
  - Set row.material\_availability\_status from 0.
  - If (row.skip\_material\_transfer and row.stock\_qty ≥ row.required\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.skip\_material\_transfer → row.stock\_qty ≥ row.required\_qty.
    - Set row.material\_availability\_status from 1.
  - Otherwise.
    - If row.transferred\_qty ≥ row.required\_qty.
      - Set row.material\_availability\_status from 1.
- Return raw\_materials.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “read”, doc = job\_card, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L1836) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L982)

<a id="op-2702744ec4a509"></a>
### Get time logs

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_get_time_logs`

**Inputs** job\_cards.

**Record and data access** read “Job Card Time Log” via get\_all.

**Explicit results** time\_logs.

**Local steps**

- Set time\_logs from mapping().
- Set data from Platform.get\_all(“Job Card Time Log”, fields = list(“parent”, “name”, “employee”, “from\_time”, …), filters = mapping(“parent” → list(“in”, job\_cards), “parentfield” → “time\_logs”), order\_by = “parent, idx”).
- For each row in data.
  - Evaluate time\_logs.setdefault(row.parent, list()).append(row).
- Return time\_logs.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L2479) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L984)

<a id="op-ee9f87cb71735b"></a>
### Get default holiday list

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_get_default_holiday_list`

**Inputs** company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via exists · read “Company” via get\_cached\_value.

**Explicit results** list() · Platform.get\_cached\_value(“Company”, company, “default\_holiday\_list”).

**Local steps**

- If company.
  - If not Platform.has\_permission(“Company”, “read”).
    - Return list().
  - If not Platform.db.exists(“Company”, company).
    - Return list().
- If not company.
  - Set company from Platform.defaults.get\_user\_default(“Company”).
- Return Platform.get\_cached\_value(“Company”, company, “default\_holiday\_list”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_holiday\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L981)

<a id="op-79695bdf5d12ee"></a>
### Check if within operating hours

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_check_if_within_operating_hours`

**Inputs** workstation, operation, from\_datetime, to\_datetime.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Local steps**

- If (from\_datetime and to\_datetime).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_datetime → to\_datetime.
  - If not Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_production\_on\_holidays”).
    - Evaluate check\_workstation\_for\_holiday(workstation, from\_datetime, to\_datetime).
  - If not cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_overtime”)).
    - Evaluate is\_within\_operating\_hours(workstation, operation, from\_datetime, to\_datetime).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_production\_on\_holidays”), Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_overtime”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L3035) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L978)

<a id="op-e4d78b4a170abb"></a>
### Is within operating hours

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_is_within_operating_hours`

**Inputs** workstation, operation, from\_datetime, to\_datetime.

**Record and data access** resolve a document from “Workstation” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper with NotInWorkingHoursError — translated “Operation {0} longer than any available working hours in workstation {1}, break down the operation into mult …”.format(operation, workstation.name).

**Local steps**

- Set operation\_length from time\_diff\_in\_seconds(to\_datetime, from\_datetime).
- Set workstation from Platform.get\_doc(“Workstation”, workstation).
- If not workstation.working\_hours.
  - Return no value.
- For each working\_hour in workstation.working\_hours.
  - If (working\_hour.start\_time and working\_hour.end\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in working\_hour.start\_time → working\_hour.end\_time.
    - Set slot\_length from (to\_timedelta((working\_hour.end\_time or empty text)) − to\_timedelta((working\_hour.start\_time or empty text))).total\_seconds().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in working\_hour.end\_time → empty text.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in working\_hour.start\_time → empty text.
    - If slot\_length ≥ operation\_length.
      - Return no value.
- Call the validation error handler Platform.throw(translated “Operation {0} longer than any available working hours in workstation {1}, break down the operation into mult …”.format(operation, workstation.name), NotInWorkingHoursError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L986)

<a id="op-4f9190b23e49cd"></a>
### Check workstation for holiday

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_check_workstation_for_holiday`

**Inputs** workstation, from\_datetime, to\_datetime.

**Record and data access** read “Workstation” via get\_value · execute query text (SELECT, Holiday).

**Explicit failure paths** validation helper with WorkstationHolidayError — ((translated “Workstation is closed on the following dates as per Holiday List: {0}”.format(holiday\_list) + whitespace '\\n') + whitespace '\\n'.join(applicable\_holidays)).

**Local steps**

- Set holiday\_list from Platform.db.get\_value(“Workstation”, workstation, “holiday\_list”).
- If (holiday\_list and from\_datetime and to\_datetime).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in holiday\_list → from\_datetime → to\_datetime.
  - Set applicable\_holidays from list().
  - For each d in Platform.db.sql(query text (SELECT, Holiday), tuple(holiday\_list, getdate(from\_datetime), getdate(to\_datetime))).
    - Evaluate applicable\_holidays.append(formatdate(d at 0)).
  - If applicable\_holidays.
    - Call the validation error handler Platform.throw(((translated “Workstation is closed on the following dates as per Holiday List: {0}”.format(holiday\_list) + whitespace '\\n') + whitespace '\\n'.join(applicable\_holidays)), WorkstationHolidayError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L979)

<a id="op-70e087bf5f45bf"></a>
### Get workstations

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_get_workstations`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Workstation” via get\_list.

**Explicit results** list() · data.

**Local steps**

- Evaluate Platform.has\_permission(“Workstation”, “read”, throw = true).
- Set kwargs from Platform.\_dict(kwargs).
- If not kwargs.plant\_floor.
  - Return list().
- Set filters from list(list(“plant\_floor”, “=”, kwargs.plant\_floor), list(“disabled”, “=”, 0)).
- If kwargs.workstation.
  - Evaluate filters.append(list(“name”, “=”, kwargs.workstation)).
- If kwargs.workstation\_type.
  - Evaluate filters.append(list(“workstation\_type”, “=”, kwargs.workstation\_type)).
- If kwargs.workstation\_status.
  - Evaluate filters.append(list(“status”, “=”, kwargs.workstation\_status)).
- If kwargs.workstation\_name.
  - Evaluate filters.append(list(“name”, “=”, kwargs.workstation\_name)).
- Set data from Platform.get\_list(“Workstation”, filters = filters, fields = list(“name”, “description”, “status”, “on\_status\_image”, …), order\_by = “creation, workstation\_type, name”).
- Set color\_map from get\_color\_map().
- For each d in data.
  - Set d.workstation\_name from get\_link\_to\_form(“Workstation”, d.name).
  - Set d.status\_image from Platform.utils.escape\_html(d.on\_status\_image).
  - Set d.workstation\_off from empty text.
  - Set d.color from color\_map.get(d.status, “red”).
  - Set d.workstation\_link from get\_url\_to\_form(“Workstation”, d.name).
  - If d.status differs from “Production”.
    - Set d.status\_image from Platform.utils.escape\_html(d.off\_status\_image).
    - Set d.workstation\_off from “workstation-off”.
- Return data.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Workstation”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L985)

<a id="op-40166e330fcab6"></a>
### Get color map

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_get_color_map`

**Inputs** no declared parameters.

**Explicit results** mapping(“Production” → “green”, “Off” → “gray”, “Idle” → “gray”, “Problem” → “red”, …).

**Local steps**

- Return mapping(“Production” → “green”, “Off” → “gray”, “Idle” → “gray”, “Problem” → “red”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L5027) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L980)

<a id="op-44e4ff506acbeb"></a>
### Update job card

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_update_job_card`

**Inputs** job\_card, method, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Method {0} is not allowed to be run on a Job Card.”.format(bold(method)).

**Local steps**

- If method does not belong to ALLOWED\_JOB\_CARD\_METHODS.
  - Call the validation error handler Platform.throw(translated “Method {0} is not allowed to be run on a Job Card.”.format(bold(method)), Platform.PermissionError, title = translated “Not Allowed”).
- Set doc from Platform.get\_doc(“Job Card”, job\_card).
- Evaluate doc.check\_permission(“write”).
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- If kwargs.get(“employees”).
  - Set kwargs.employees from Platform.parse\_json(kwargs.employees).
- If (kwargs.qty and isinstance(kwargs.qty, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.qty → isinstance(kwargs.qty, str).
  - Set kwargs.qty from flt(kwargs.qty).
- Evaluate doc.run\_method(method, expanded names kwargs).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”) · selected callable from doc.run\_method(method, expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L5123) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L987)

<a id="op-e57cb06811e1e5"></a>
### Validate job card

`operation_enterprise_manufacturing_record_definitions_workstation_business_behavior_validate_job_card`

**Inputs** job\_card, status.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Job Card” via get\_value.

**Explicit results** job\_card\_details.for\_quantity.

**Explicit failure paths** validation helper — translated “The job card {0} is in {1} state and you cannot start it again.”.format(job\_card, current\_status) · validation helper — translated “The job card {0} is in {1} state and you cannot complete.”.format(job\_card, current\_status).

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “read”, doc = job\_card, throw = true).
- Set job\_card\_details from Platform.db.get\_value(“Job Card”, job\_card, list(“status”, “for\_quantity”), as\_dict = 1).
- Set current\_status from job\_card\_details.status.
- If current\_status differs from status.
  - If status equals “Open”.
    - Call the validation error handler Platform.throw(translated “The job card {0} is in {1} state and you cannot start it again.”.format(job\_card, current\_status)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “The job card {0} is in {1} state and you cannot complete.”.format(job\_card, current\_status)).
- Return job\_card\_details.for\_quantity.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “read”, doc = job\_card, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L988)

<a id="op-c67b9b20ceaed2"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_workstation_workstation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “workstation”, “transactions” → list(mapping(“label” → translated “Master”, “items” → list(“BOM”, “Routing”, “Operation”)), mapping(“label” → translated “Transaction”, “items” → list( ….

**Local steps**

- Return mapping(“fieldname” → “workstation”, “transactions” → list(mapping(“label” → translated “Master”, “items” → list(“BOM”, “Routing”, “Operation”)), mapping(“label” → translated “Transaction”, “items” → list( ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L6029) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1016)

## Record · Workstation operating component

[Record definition](../../../../data/record-types/workstation_operating_component.json)

<a id="op-e609b2cad099bd"></a>
### Workstation Operating Component.validate

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_operating_component_workstation_operating_component_workstationoperatingcomponent_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_company().
- Evaluate self.validate\_accounts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate company](operations-048.md#op-0b16249dd027d0), [validate accounts](operations-048.md#op-1cba113b9db4de).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1111)

<a id="op-0b16249dd027d0"></a>
### Workstation Operating Component.validate duplicate company

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_operating_component_workstation_operating_component_workstationoperatingcomponent_validate_duplicate_company`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Company {1} already has an expense account”.format(row.idx, bold(row.company)).

**Local steps**

- Set companies from set().
- For each row in self.accounts.
  - If row.company belongs to companies.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Company {1} already has an expense account”.format(row.idx, bold(row.company))).
  - Evaluate companies.add(row.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1113)

<a id="op-1cba113b9db4de"></a>
### Workstation Operating Component.validate accounts

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_operating_component_workstation_operating_component_workstationoperatingcomponent_validate_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Account {1} must be an Expense ledger account of company {2}”.format(row.idx, bold(row.expense\_account), bold(row.company)).

**Local steps**

- Set names from list of row.expense\_account for row drawn from self.accounts where row.expense\_account.
  - Draw row from self.accounts, keep a combination only if (row.expense\_account).
- If not names.
  - Return no value.
- Set accounts from mapping of account.name → account for account drawn from Platform.get\_all(“Account”, filters = mapping(“name” → list(“in”, names)), fields = list(“name”, “company”, “is\_group”, “root\_type”)).
  - Draw account from Platform.get\_all(“Account”, filters = mapping(“name” → list(“in”, names)), fields = list(“name”, “company”, “is\_group”, “root\_type”)).
- For each row in self.accounts.
  - Set account from accounts.get(row.expense\_account).
  - If not account.
    - Continue with the next iteration or loop test.
  - If (account.is\_group or account.root\_type differs from “Expense” or account.company differs from row.company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.is\_group → account.root\_type differs from “Expense” → account.company differs from row.company.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Account {1} must be an Expense ledger account of company {2}”.format(row.idx, bold(row.expense\_account), bold(row.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1112)

## Record · Workstation type

[Record definition](../../../../data/record-types/workstation_type.json)

<a id="op-ea4838b86b443e"></a>
### Workstation Type.validate

`operation_enterprise_manufacturing_record_definitions_workstation_type_business_behavior_workstation_type_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_operating\_component().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate operating component](operations-048.md#op-04dd6006ac45b0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L6521) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1013)

<a id="op-04dd6006ac45b0"></a>
### Workstation Type.validate duplicate operating component

`operation_enterprise_manufacturing_record_definitions_workstation_type_business_behavior_workstation_type_validate_duplicate_operating_component`

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

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L6572) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1014)
