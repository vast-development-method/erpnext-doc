# Production · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-485abc9bbc6102"></a>
### Get timer rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_timer_rows`

**Inputs** filters, or\_filters = no value, start = 0, page\_length = 1.

**Declared result** list at dict.

**Explicit results** list of timer.as\_list\_row(can\_write = can\_write(timer)) for timer drawn from timers.

**Local steps**

- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set job\_cards from nested operand in the contract(nested operand in the contract, fields = nested operand in the contract, filters = nested operand in the contract, or\_filters = nested operand in the contract, offset = neste ….
- Evaluate attach\_timer\_summary(job\_cards).
- Set timers from list of JobCardTimer(job\_card) for job\_card drawn from job\_cards.
  - Draw job\_card from job\_cards.
- Return list of timer.as\_list\_row(can\_write = can\_write(timer)) for timer drawn from timers.
  - Draw timer from timers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L866)

<a id="op-7ee929bc1672ab"></a>
### Can write

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_can_write`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** timer.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L859)

<a id="op-3b71877fd598af"></a>
### Attach timer summary

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_attach_timer_summary`

**Inputs** job\_cards.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set names from list of job\_card.name for job\_card drawn from job\_cards.
  - Draw job\_card from job\_cards.
- If not names.
  - Return no value.
- Set item from Platform.qb.DocType(“Job Card Item”).
- Set time\_log\_summary from get\_time\_log\_summary(names).
- Set open\_logs from get\_open\_time\_logs(names).
- Set employees from get\_assigned\_employees(names).
- Set pending\_transfer from get\_parents\_with\_rows(“Job Card Item”, “items”, names, IfNull(item.transferred\_qty, 0) &lt; item.required\_qty).
- Set with\_sub\_operations from get\_parents\_with\_rows(“Job Card Operation”, “sub\_operations”, names).
- Set work\_order\_statuses from get\_work\_order\_statuses(job\_cards).
- For each job\_card in job\_cards.
  - Set summary from time\_log\_summary.get(job\_card.name).
  - Set card\_open\_logs from open\_logs at job\_card.name.
  - Evaluate job\_card.update(has\_time\_logs = summary is distinct from no value, logged\_minutes = summary.logged\_minutes when summary, otherwise 0, open\_log\_starts = list of log.from\_time for log drawn from card\_open\_lo ….
    - Value choice on summary — true gives summary.logged\_minutes, false gives 0.
    - Draw log from card\_open\_logs.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(summary) → any(generator of log.idx equals summary.last\_idx for log drawn from card\_open\_logs).
    - Draw log from card\_open\_logs.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L858)

<a id="op-5eefa9d00a9312"></a>
### Get time log summary

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_time_log_summary`

**Inputs** names.

**Declared result** dict at tuple(str, Platform.\_dict).

**Explicit results** mapping of row.parent → row for row drawn from rows.

**Local steps**

- Set time\_log from Platform.qb.DocType(“Job Card Time Log”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(child\_rows\_criterion(time\_log, “time\_logs”, names)).groupby(time\_log.par ….
- Return mapping of row.parent → row for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L865)

<a id="op-a49cd1788c2905"></a>
### Get open time logs

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_open_time_logs`

**Inputs** names.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** group\_by\_parent(rows).

**Local steps**

- Set time\_log from Platform.qb.DocType(“Job Card Time Log”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract, nested o ….
- Return group\_by\_parent(rows).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L863)

<a id="op-0adb6430913b8d"></a>
### Get assigned employees

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_assigned_employees`

**Inputs** names.

**Declared result** dict at tuple(str, list at str).

**Explicit results** mapping of parent → list of row.employee for row drawn from rows for tuple(parent, rows) drawn from group\_by\_parent(rows).items().

**Local steps**

- Set time\_log from Platform.qb.DocType(“Job Card Time Log”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract, nested operand in the contract, nested o ….
- Return mapping of parent → list of row.employee for row drawn from rows for tuple(parent, rows) drawn from group\_by\_parent(rows).items().
  - Draw tuple(parent, rows) from group\_by\_parent(rows).items().
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L861)

<a id="op-9268eddb78aac4"></a>
### Group by parent

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_group_by_parent`

**Inputs** rows.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** grouped.

**Local steps**

- Set grouped from defaultdict(list).
- For each row in rows.
  - Evaluate grouped at row.parent.append(row).
- Return grouped.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L869)

<a id="op-74e37a3242d492"></a>
### Get parents with rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_parents_with_rows`

**Inputs** child\_doctype, parentfield, names, condition = no value.

**Declared result** set at str.

**Explicit results** set(query.run(pluck = true)).

**Local steps**

- Set child from Platform.qb.DocType(child\_doctype).
- Set query from nested operand in the contract(nested operand in the contract).select(child.parent).distinct().where(child\_rows\_criterion(child, parentfield, names)).
- If condition is distinct from no value.
  - Set query from query.where(condition).
- Return set(query.run(pluck = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L864)

<a id="op-e979249ae45cb9"></a>
### Child rows criterion

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_child_rows_criterion`

**Inputs** child, parentfield, names.

**Declared result** Criterion.

**Explicit results** ((child.parenttype equals “Job Card” bitwise and child.parentfield equals parentfield) bitwise and child.parent.isin(names)).

**Local steps**

- Return ((child.parenttype equals “Job Card” bitwise and child.parentfield equals parentfield) bitwise and child.parent.isin(names)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L860)

<a id="op-8656006069df20"></a>
### Get work order statuses

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_get_work_order_statuses`

**Inputs** job\_cards.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Work Order” via get\_all.

**Explicit results** mapping() · mapping of row.name → row.status for row drawn from rows.

**Local steps**

- Set work\_orders from set of job\_card.work\_order for job\_card drawn from job\_cards where job\_card.work\_order.
  - Draw job\_card from job\_cards, keep a combination only if (job\_card.work\_order).
- If not work\_orders.
  - Return mapping().
- Set rows from Platform.get\_all(“Work Order”, filters = mapping(“name” → tuple(“in”, list(work\_orders))), fields = list(“name”, “status”)).
- Return mapping of row.name → row.status for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L868)

<a id="op-d0c6f8964585b3"></a>
### Job Card Timer.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_init`

**Inputs** self, job\_card.

**Declared result** no value.

**Local steps**

- Set self.job\_card from job\_card.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L875)

<a id="op-02dcd2e51a2170"></a>
### Job Card Timer.as list row

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_as_list_row`

**Inputs** self, can\_write.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set row from mapping of fieldname → self.job\_card.get(fieldname) for fieldname drawn from LIST\_FIELDS.
  - Draw fieldname from LIST\_FIELDS.
- Evaluate row.update(elapsed\_seconds = self.get\_elapsed\_seconds(), is\_running = self.is\_running(), open\_log\_count = len(self.job\_card.open\_log\_starts), timer\_action = self.get\_action() when can\_write, otherwise no value, …).
  - Value choice on can\_write — true gives self.get\_action(), false gives no value.
- Return row.

**Methods declared on this owner** [get elapsed seconds](operations-024.md#op-3730d4a81feec4), [is running](operations-024.md#op-5521a73955ba13), [get action](operations-024.md#op-31c95ade68d025).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L870)

<a id="op-3730d4a81feec4"></a>
### Job Card Timer.get elapsed seconds

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_get_elapsed_seconds`

**Inputs** self.

**Declared result** int.

**Explicit results** int(((flt(self.job\_card.logged\_minutes) × 60) + open\_seconds)).

**Local steps**

- Set now from now\_datetime().
- Set open\_seconds from sum(generator of time\_diff\_in\_seconds(now, start) for start drawn from self.job\_card.open\_log\_starts).
  - Draw start from self.job\_card.open\_log\_starts.
- Return int(((flt(self.job\_card.logged\_minutes) × 60) + open\_seconds)).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L873)

<a id="op-5521a73955ba13"></a>
### Job Card Timer.is running

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_is_running`

**Inputs** self.

**Declared result** bool.

**Explicit results** (self.job\_card.last\_log\_open and not self.job\_card.is\_paused).

**Local steps**

- Return (self.job\_card.last\_log\_open and not self.job\_card.is\_paused).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.job\_card.last\_log\_open → not self.job\_card.is\_paused.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L876)

<a id="op-31c95ade68d025"></a>
### Job Card Timer.get action

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_get_action`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** no value · “resume” · “start” · “pause”.

**Local steps**

- If (self.job\_card.docstatus differs from 0 or self.job\_card.is\_subcontracted).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.job\_card.docstatus differs from 0 → self.job\_card.is\_subcontracted.
  - Return no value.
- If self.job\_card.work\_order\_status belongs to CLOSED\_WORK\_ORDER\_STATUSES.
  - Return no value.
- If (not self.has\_remaining\_qty() or not self.materials\_ready()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.has\_remaining\_qty() → not self.materials\_ready().
  - Return no value.
- If self.job\_card.is\_paused.
  - Return “resume”.
- If self.can\_start().
  - Return “start”.
- If self.qty\_yet\_to\_manufacture() &gt; 0.
  - Return “pause”.
- Return no value.

**Methods declared on this owner** [has remaining qty](operations-024.md#op-a55f47ff9e7abf), [materials ready](operations-024.md#op-8b2cfb1f36c599), [can start](operations-024.md#op-403f3a0c079d6d), [qty yet to manufacture](operations-024.md#op-01c29d9552c423).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L872)

<a id="op-a55f47ff9e7abf"></a>
### Job Card Timer.has remaining qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_has_remaining_qty`

**Inputs** self.

**Declared result** bool.

**Explicit results** (flt(job\_card.for\_quantity) + flt(job\_card.process\_loss\_qty)) &gt; flt(job\_card.total\_completed\_qty).

**Local steps**

- Set job\_card from self.job\_card.
- Return (flt(job\_card.for\_quantity) + flt(job\_card.process\_loss\_qty)) &gt; flt(job\_card.total\_completed\_qty).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L874)

<a id="op-8b2cfb1f36c599"></a>
### Job Card Timer.materials ready

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_materials_ready`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · not self.job\_card.has\_pending\_transfer.

**Local steps**

- If (self.job\_card.skip\_material\_transfer or self.job\_card.is\_corrective\_job\_card).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.job\_card.skip\_material\_transfer → self.job\_card.is\_corrective\_job\_card.
  - Return true.
- Return not self.job\_card.has\_pending\_transfer.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L877)

<a id="op-403f3a0c079d6d"></a>
### Job Card Timer.can start

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_can_start`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · (has\_cycles and not self.job\_card.last\_log\_open).

**Local steps**

- If not self.job\_card.has\_time\_logs.
  - Return true.
- Set has\_cycles from (flt(self.job\_card.pending\_qty) &gt; 0 or self.job\_card.has\_sub\_operations).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.job\_card.pending\_qty) &gt; 0 → self.job\_card.has\_sub\_operations.
- Return (has\_cycles and not self.job\_card.last\_log\_open).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_cycles → not self.job\_card.last\_log\_open.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L871)

<a id="op-01c29d9552c423"></a>
### Job Card Timer.qty yet to manufacture

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_timer_jobcardtimer_qty_yet_to_manufacture`

**Inputs** self.

**Declared result** float.

**Explicit results** (flt(job\_card.for\_quantity) − (manufactured\_qty + flt(job\_card.process\_loss\_qty))).

**Local steps**

- Set job\_card from self.job\_card.
- Set manufactured\_qty from (flt(job\_card.manufactured\_qty) or flt(job\_card.total\_completed\_qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(job\_card.manufactured\_qty) → flt(job\_card.total\_completed\_qty).
- Return (flt(job\_card.for\_quantity) − (manufactured\_qty + flt(job\_card.process\_loss\_qty))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L878)

## Report · Job card summary

<a id="op-09a45da70107d0"></a>
### Execute

`operation_enterprise_manufacturing_report_job_card_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Set chart\_data from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1095)

<a id="op-112283fb0b87c8"></a>
### Get data

`operation_enterprise_manufacturing_report_job_card_summary_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Job Card” via get\_list · read “Job Card Time Log” via get\_all.

**Explicit results** list() · res.

**Local steps**

- Set query\_filters from mapping(“docstatus” → tuple(“&lt;”, 2), “posting\_date” → tuple(“between”, list(filters.from\_date, filters.to\_date))).
- Set fields from list(“name”, “status”, “work\_order”, “production\_item”, …).
- For each field in list(“work\_order”, “production\_item”).
  - If filters.get(field).
    - Set query\_filters at field from tuple(“in”, filters.get(field)).
- For each field in list(“workstation”, “operation”, “status”, “company”).
  - If filters.get(field).
    - Set query\_filters at field from filters.get(field).
- Set data from Platform.get\_list(“Job Card”, fields = fields, filters = query\_filters).
- If not data.
  - Return list().
- Set job\_cards from list of d.name for d drawn from data.
  - Draw d from data.
- Set job\_card\_time\_filter from mapping(“docstatus” → tuple(“&lt;”, 2), “parent” → tuple(“in”, job\_cards)).
- Set job\_card\_time\_details from mapping().
- For each job\_card\_data in Platform.get\_all(“Job Card Time Log”, fields = list(mapping(“MIN” → “from\_time”, “as” → “from\_time”), mapping(“MAX” → “to\_time”, “as” → “to\_time”), “parent”), filters = job\_card\_time\_filter, group\_by = “parent”).
  - Set job\_card\_time\_details at job\_card\_data.parent from job\_card\_data.
- Set res from list().
- For each d in data.
  - If job\_card\_time\_details.get(d.name).
    - Set d.from\_time from job\_card\_time\_details.get(d.name).from\_time.
    - Set d.to\_time from job\_card\_time\_details.get(d.name).to\_time.
  - Evaluate res.append(d).
- Return res.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1098)

<a id="op-df7d8d1f24b23e"></a>
### Get chart data

`operation_enterprise_manufacturing_report_job_card_summary_business_behavior_get_chart_data`

**Inputs** job\_card\_details, filters.

**Explicit results** chart.

**Local steps**

- Set tuple(labels, periodic\_data) from prepare\_chart\_data(job\_card\_details, filters).
- Set tuple(open\_job\_cards, completed) from tuple(list(), list()).
- Set datasets from list().
- For each d in labels.
  - Evaluate open\_job\_cards.append(periodic\_data.get(“Open”).get(d)).
  - Evaluate completed.append(periodic\_data.get(“Completed”).get(d)).
- Evaluate datasets.append(mapping(“name” → translated “Open”, “values” → open\_job\_cards)).
- Evaluate datasets.append(mapping(“name” → translated “Completed”, “values” → completed)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “bar”).
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0546.json#L3885) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1096)

<a id="op-76ea6f7864c99c"></a>
### Prepare chart data

`operation_enterprise_manufacturing_report_job_card_summary_business_behavior_prepare_chart_data`

**Inputs** job\_card\_details, filters.

**Explicit results** tuple(labels, periodic\_data).

**Local steps**

- Set labels from list().
- Set periodic\_data from mapping(“Open” → mapping(), “Completed” → mapping()).
- Set filters.range from “Monthly”.
- Set ranges from get\_period\_date\_ranges(filters).
- For each tuple(from\_date, end\_date) in ranges.
  - Set period from get\_period(end\_date, filters).
  - If period does not belong to labels.
    - Evaluate labels.append(period).
    - For each status in periodic\_data.
      - Set periodic\_data at status at period from 0.
  - For each d in job\_card\_details.
    - If from\_date ≤ getdate(d.posting\_date) ≤ end\_date.
      - Compare adjacent operands in order, stopping at the first false comparison in from\_date ≤ getdate(d.posting\_date) ≤ end\_date.
      - Set status from “Completed” when d.status equals “Completed”, otherwise “Open”.
        - Value choice on d.status equals “Completed” — true gives “Completed”, false gives “Open”.
      - Update periodic\_data at status at period using + 1.
- Return tuple(labels, periodic\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1099)

<a id="op-c0954fc01b21a2"></a>
### Get columns

`operation_enterprise_manufacturing_report_job_card_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Job Card”, …), mapping(“label” → translated “Posting Date”, “fieldname” → “posting\_date”, “fieldtype” → “Dat ….
- If not filters.get(“status”).
  - Evaluate columns.append(mapping(“label” → translated “Status”, “fieldname” → “status”, “width” → 100)).
- Evaluate columns.extend(list(mapping(“label” → translated “Work Order”, “fieldname” → “work\_order”, “fieldtype” → “Link”, “options” → “Work Order”, …), mapping(“label” → translated “Production Item”, “fieldname” →  ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0546.json#L4813) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1097)
