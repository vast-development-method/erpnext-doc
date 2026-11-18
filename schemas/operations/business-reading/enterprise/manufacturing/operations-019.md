# Production · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-ecc98152945d87"></a>
### Job Card.get overlap for

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_overlap_for`

**Inputs** self, args, open\_job\_cards = no value.

**Explicit results** mapping() · time\_logs at 0.

**Local steps**

- Set time\_logs from self.get\_overlapping\_time\_logs(args, open\_job\_cards).
- If not time\_logs.
  - Return mapping().
- Set time\_logs from sorted(time\_logs, key = deferred anonymous expression).
- If not self.has\_overlap(self.get\_production\_capacity(), time\_logs).
  - Return mapping().
- If (not self.workstation and self.workstation\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.workstation → self.workstation\_type.
  - If workstation bound to self.get\_free\_workstation(time\_logs).
    - Set self.workstation from workstation.
    - Return mapping().
- Return time\_logs at 0.

**Methods declared on this owner** [get overlapping time logs](operations-019.md#op-169e1236e1d8bf), [has overlap](operations-019.md#op-d3244e0e4b198e), [get production capacity](operations-019.md#op-8c935b2768fd25), [get free workstation](operations-019.md#op-70cffcffb5189d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L402)

<a id="op-169e1236e1d8bf"></a>
### Job Card.get overlapping time logs

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_overlapping_time_logs`

**Inputs** self, args, open\_job\_cards = no value.

**Explicit results** time\_logs.

**Local steps**

- Set time\_logs from list().
- Evaluate time\_logs.extend(self.get\_time\_logs(args, “Job Card Time Log”)).
- Evaluate time\_logs.extend(self.get\_time\_logs(args, “Job Card Scheduled Time”, open\_job\_cards = open\_job\_cards)).
- Return time\_logs.

**Methods declared on this owner** [get time logs](operations-019.md#op-ee40206b64102c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L6763) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L403)

<a id="op-8c935b2768fd25"></a>
### Job Card.get production capacity

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_production_capacity`

**Inputs** self, workstation = no value.

**Record and data access** read “Workstation” via get\_cached\_value.

**Explicit results** (Platform.get\_cached\_value(“Workstation”, workstation, “production\_capacity”) or 1) · 1.

**Local steps**

- Set workstation from (workstation or self.workstation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in workstation → self.workstation.
- If workstation.
  - Return (Platform.get\_cached\_value(“Workstation”, workstation, “production\_capacity”) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Workstation”, workstation, “production\_capacity”) → 1.
- Return 1.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Workstation”, workstation, “production\_capacity”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L405)

<a id="op-d3244e0e4b198e"></a>
### Job Card.has overlap

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_has_overlap`

**Inputs** self, production\_capacity, time\_logs.

**Explicit results** true · false · len(alloted\_capacity) ≥ production\_capacity.

**Local steps**

- If (production\_capacity equals 1 and len(time\_logs) ≥ 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in production\_capacity equals 1 → len(time\_logs) ≥ 1.
  - Return true.
- If not len(time\_logs).
  - Return false.
- Set alloted\_capacity from self.get\_alloted\_capacity(merge\_time\_logs\_per\_job\_card(time\_logs)).
- Return len(alloted\_capacity) ≥ production\_capacity.

**Methods declared on this owner** [get alloted capacity](operations-019.md#op-9e81f1ea6168d2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L410)

<a id="op-9e81f1ea6168d2"></a>
### Job Card.get alloted capacity

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_alloted_capacity`

**Inputs** self, time\_logs.

**Explicit results** alloted\_capacity.

**Local steps**

- Set time\_logs from sorted(time\_logs, key = deferred anonymous expression).
- Set alloted\_capacity from mapping(1 → time\_logs at 0 at “to\_time”).
- For each i in range(1, len(time\_logs)).
  - Set sequential\_job\_card\_found from false.
  - For each key in alloted\_capacity.keys().
    - If alloted\_capacity at key ≤ time\_logs at i at “from\_time”.
      - Set alloted\_capacity at key from time\_logs at i at “to\_time”.
      - Set sequential\_job\_card\_found from true.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If not sequential\_job\_card\_found.
    - Set key from (key + 1).
    - Set alloted\_capacity at key from time\_logs at i at “to\_time”.
- Return alloted\_capacity.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L394)

<a id="op-ee40206b64102c"></a>
### Job Card.get time logs

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_time_logs`

**Inputs** self, args, doctype, open\_job\_cards = no value.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If (args.get(“remaining\_time\_in\_mins”) and get\_datetime(args.from\_time) ≥ get\_datetime(args.to\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“remaining\_time\_in\_mins”) → get\_datetime(args.from\_time) ≥ get\_datetime(args.to\_time).
  - Set args.to\_time from add\_to\_date(args.from\_time, minutes = args.get(“remaining\_time\_in\_mins”)).
- If (args.get(“employee”) and not open\_job\_cards and doctype equals “Job Card Scheduled Time”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“employee”) → not open\_job\_cards → doctype equals “Job Card Scheduled Time”.
  - Return list().
- Set jc from Platform.qb.DocType(“Job Card”).
- Set jctl from Platform.qb.DocType(doctype).
- Set query from self.get\_base\_overlap\_query(jc, jctl, args).
- Set query from self.apply\_workstation\_filters(query, jc).
- Set query from self.apply\_employee\_filters(query, jc, jctl, args, …).
- Set query from self.apply\_docstatus\_filters(query, jc, doctype).
- Return query.run(as\_dict = true).

**Methods declared on this owner** [get base overlap query](operations-019.md#op-a2093c28cdd059), [apply workstation filters](operations-019.md#op-2e03b77a7740ed), [apply employee filters](operations-019.md#op-12dcf65363c8cf), [apply docstatus filters](operations-019.md#op-47a4986b71fcfa).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L624) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L409)

<a id="op-a2093c28cdd059"></a>
### Job Card.get base overlap query

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_base_overlap_query`

**Inputs** self, jc, jctl, args.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“name”), nested operand in the contract.as\_(“row\_name”), jctl.from\_time, jctl.to\_time, …).where((((( ….

**Local steps**

- Set time\_conditions from list((jctl.from\_time &lt; args.from\_time bitwise and jctl.to\_time &gt; args.from\_time), (jctl.from\_time &lt; args.to\_time bitwise and jctl.to\_time &gt; args.to\_time), (jctl.from\_time ≥ args.from\_time bitwise and jctl. ….
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“name”), nested operand in the contract.as\_(“row\_name”), jctl.from\_time, jctl.to\_time, …).where((((( ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.name → “No Name”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.parent → “No Name”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L1155) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L395)

<a id="op-2e03b77a7740ed"></a>
### Job Card.apply workstation filters

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_apply_workstation_filters`

**Inputs** self, query, jc.

**Explicit results** query.where(jc.workstation equals self.workstation) · query.where(jc.workstation.isin(workstations)) · query.where(jc.workstation\_type equals self.workstation\_type) · query.

**Local steps**

- If self.workstation.
  - Return query.where(jc.workstation equals self.workstation).
- If self.workstation\_type.
  - If workstations bound to get\_workstations(self.workstation\_type).
    - Return query.where(jc.workstation.isin(workstations)).
  - Return query.where(jc.workstation\_type equals self.workstation\_type).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L389)

<a id="op-12dcf65363c8cf"></a>
### Job Card.apply employee filters

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_apply_employee_filters`

**Inputs** self, query, jc, jctl, args, doctype, open\_job\_cards.

**Explicit results** query.

**Local steps**

- If (args.get(“employee”) and doctype equals “Job Card Scheduled Time”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“employee”) → doctype equals “Job Card Scheduled Time”.
  - Set query from query.where(jc.name.isin(open\_job\_cards)).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L387)

<a id="op-47a4986b71fcfa"></a>
### Job Card.apply docstatus filters

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_apply_record_state_filters`

**Inputs** self, query, jc, doctype.

**Explicit results** query.

**Local steps**

- If doctype equals “Job Card Time Log”.
  - Set query from query.where(jc.docstatus &lt; 2).
- Otherwise.
  - Set query from query.where((jc.docstatus equals 0 bitwise and jc.total\_time\_in\_mins equals 0)).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L2173) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L388)

<a id="op-9a1a52d2462a8e"></a>
### Job Card.get open job cards

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_open_job_cards`

**Inputs** self, employee, workstation = no value.

**Explicit results** list of job.get(“name”) for job drawn from jobs when jobs, otherwise list().

**Local steps**

- Set jc from Platform.qb.DocType(“Job Card”).
- Set jctl from Platform.qb.DocType(“Job Card Time Log”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(jc.name).where((((jctl.parent equals jc.name bitwi ….
- If workstation.
  - Set query from query.where(jc.workstation equals workstation).
- Set jobs from query.run(as\_dict = true).
- Return list of job.get(“name”) for job drawn from jobs when jobs, otherwise list().
  - Value choice on jobs — true gives list of job.get(“name”) for job drawn from jobs, false gives list().
  - Draw job from jobs.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L2373) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L401)

<a id="op-70cffcffb5189d"></a>
### Job Card.get free workstation

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_free_workstation`

**Inputs** self, overlapping\_time\_logs.

**Explicit results** workstation.

**Local steps**

- For each workstation in get\_workstations(self.workstation\_type).
  - Set time\_logs from list of row for row drawn from overlapping\_time\_logs where row.workstation equals workstation.
    - Draw row from overlapping\_time\_logs, keep a combination only if (row.workstation equals workstation).
  - If (not time\_logs or not self.has\_overlap(self.get\_production\_capacity(workstation), time\_logs)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not time\_logs → not self.has\_overlap(self.get\_production\_capacity(workstation), time\_logs).
    - Return workstation.

If control reaches the end, it returns no value.

**Methods declared on this owner** [has overlap](operations-019.md#op-d3244e0e4b198e), [get production capacity](operations-019.md#op-8c935b2768fd25).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L816)

<a id="op-d0728e633cece9"></a>
### Job Card.schedule time logs

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_schedule_time_logs`

**Inputs** self, row.

**Local steps**

- Set row.remaining\_time\_in\_mins from row.time\_in\_mins.
- While row.remaining\_time\_in\_mins &gt; 0.
  - Set slot\_end from self.place\_row\_start(row).
  - If not slot\_end.
    - Evaluate self.schedule\_without\_working\_hours(row).
    - Continue with the next iteration or loop test.
  - Evaluate self.consume\_working\_hour\_slot(row, slot\_end).
  - If row.remaining\_time\_in\_mins &gt; 0.
    - Set row.planned\_start\_time from row.planned\_end\_time.

If control reaches the end, it returns no value.

**Methods declared on this owner** [place row start](operations-019.md#op-a6fbb106f3064d), [schedule without working hours](operations-019.md#op-5d07c61e6b807e), [consume working hour slot](operations-019.md#op-5189999ef7fd76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L422)

<a id="op-a6fbb106f3064d"></a>
### Job Card.place row start

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_place_row_start`

**Inputs** self, row.

**Explicit results** slot\_end.

**Local steps**

- While true.
  - Set start from get\_datetime(row.planned\_start\_time).
  - Set args from Platform.\_dict(mapping(“from\_time” → row.planned\_start\_time, “to\_time” → add\_to\_date(row.planned\_start\_time, minutes = row.remaining\_time\_in\_mins), “remaining\_time\_in\_mins” → row.remaining\_time\_in\_mins)).
  - Evaluate self.validate\_overlap\_for\_workstation(args, row).
  - Set slot\_end from self.align\_start\_to\_working\_time(row).
  - If get\_datetime(row.planned\_start\_time) equals start.
    - Return slot\_end.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap for workstation](operations-019.md#op-7cd0c95608d5ae), [align start to working time](operations-019.md#op-a015464838e306).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L830)

<a id="op-a015464838e306"></a>
### Job Card.align start to working time

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_align_start_to_working_time`

**Inputs** self, row.

**Record and data access** resolve a document from “Workstation” via get\_cached\_doc · read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value · slot\_end.

**Local steps**

- Set workstation\_doc from Platform.get\_cached\_doc(“Workstation”, self.workstation).
- Set working\_hours from get\_sorted\_working\_hours(workstation\_doc).
- Set allow\_overtime from cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_overtime”)).
- For each \_day in range(366).
  - Set start\_date from self.adjust\_start\_date\_for\_holiday(workstation\_doc, row).
  - If (not working\_hours or allow\_overtime).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not working\_hours → allow\_overtime.
    - Return no value.
  - If slot\_end bound to self.move\_start\_into\_working\_slot(working\_hours, row, start\_date).
    - Return slot\_end.
  - Set row.planned\_start\_time from datetime.datetime.combine(add\_days(start\_date, 1), get\_time(working\_hours at 0.start\_time)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [adjust start date for holiday](operations-019.md#op-b7a4f22b2c463a), [move start into working slot](operations-019.md#op-e70cf7791bdd1d).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Workstation”, self.workstation), Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_overtime”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L811)

<a id="op-e70cf7791bdd1d"></a>
### Job Card.move start into working slot

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_move_start_into_working_slot`

**Inputs** working\_hours, row, start\_date.

**Wrappers, in declaration order** staticmethod.

**Explicit results** slot\_end.

**Local steps**

- For each time\_slot in working\_hours.
  - Set slot\_start from datetime.datetime.combine(start\_date, get\_time(time\_slot.start\_time)).
  - Set slot\_end from datetime.datetime.combine(start\_date, get\_time(time\_slot.end\_time)).
  - If get\_datetime(row.planned\_start\_time) &lt; slot\_end.
    - Set row.planned\_start\_time from max(get\_datetime(row.planned\_start\_time), slot\_start).
    - Return slot\_end.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L829)

<a id="op-7cd0c95608d5ae"></a>
### Job Card.validate overlap for workstation

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_overlap_for_workstation`

**Inputs** self, args, row.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Workstation Type {0} has no enabled Workstation”.format(bold(self.workstation\_type)).

**Local steps**

- Set data from self.get\_overlap\_for(args).
- If not self.workstation.
  - Set workstations from get\_workstations(self.workstation\_type).
  - If not workstations.
    - Call the validation error handler Platform.throw(translated “Workstation Type {0} has no enabled Workstation”.format(bold(self.workstation\_type))).
  - Set self.workstation from workstations at 0.
- If not data.
  - Set row.planned\_start\_time from args.from\_time.
  - Return no value.
- If data.
  - Set args.planned\_start\_time from get\_datetime((data.to\_time + get\_mins\_between\_operations())).
  - Set args.from\_time from args.planned\_start\_time.
  - Set args.to\_time from add\_to\_date(args.planned\_start\_time, minutes = row.remaining\_time\_in\_mins).
  - Evaluate self.validate\_overlap\_for\_workstation(args, row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get overlap for](operations-019.md#op-ecc98152945d87).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L795) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L458)

<a id="op-5d07c61e6b807e"></a>
### Job Card.schedule without working hours

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_schedule_without_working_hours`

**Inputs** self, row.

**Local steps**

- If get\_datetime(row.planned\_end\_time) ≤ get\_datetime(row.planned\_start\_time).
  - Set row.planned\_end\_time from add\_to\_date(row.planned\_start\_time, minutes = row.time\_in\_mins).
  - Set row.remaining\_time\_in\_mins from 0.0.
- Otherwise.
  - Update row.remaining\_time\_in\_mins using − time\_diff\_in\_minutes(row.planned\_end\_time, row.planned\_start\_time).
- Evaluate self.update\_time\_logs(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update time logs](operations-019.md#op-e8aa4f9825c3b1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L4497) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L423)

<a id="op-b7a4f22b2c463a"></a>
### Job Card.adjust start date for holiday

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_adjust_start_date_for_holiday`

**Inputs** self, workstation\_doc, row.

**Explicit results** start\_date.

**Local steps**

- Set start\_date from getdate(row.planned\_start\_time).
- Set start\_time from get\_time(row.planned\_start\_time).
- Set new\_start\_date from workstation\_doc.validate\_workstation\_holiday(start\_date).
- If new\_start\_date differs from start\_date.
  - Set row.planned\_start\_time from datetime.datetime.combine(new\_start\_date, start\_time).
  - Set start\_date from new\_start\_date.
- Return start\_date.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L4725) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L386)

<a id="op-5189999ef7fd76"></a>
### Job Card.consume working hour slot

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_consume_working_hour_slot`

**Inputs** self, row, workstation\_end\_time.

**Local steps**

- Set time\_in\_mins from time\_diff\_in\_minutes(workstation\_end\_time, row.planned\_start\_time).
- If time\_in\_mins &gt; row.remaining\_time\_in\_mins.
  - Set row.planned\_end\_time from add\_to\_date(row.planned\_start\_time, minutes = row.remaining\_time\_in\_mins).
  - Set row.remaining\_time\_in\_mins from 0.
- Otherwise.
  - Set row.planned\_end\_time from add\_to\_date(row.planned\_start\_time, minutes = time\_in\_mins).
  - Update row.remaining\_time\_in\_mins using − time\_in\_mins.
- Evaluate self.update\_time\_logs(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update time logs](operations-019.md#op-e8aa4f9825c3b1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L5429) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L393)

<a id="op-1f1c4681044455"></a>
### Job Card.add time log

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_add_time_log`

**Inputs** self, args.

**State and service calls** call db\_set on row.

**Local steps**

- Set last\_row from list().
- Set employees from args.employees.
- If isinstance(employees, str).
  - Set employees from json.loads(employees).
- If (self.time\_logs and len(self.time\_logs) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.time\_logs → len(self.time\_logs) &gt; 0.
  - Set last\_row from self.time\_logs at negative 1.
- If (last\_row and args.get(“complete\_time”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_row → args.get(“complete\_time”).
  - For each row in self.time\_logs.
    - If not row.to\_time.
      - Set to\_time from get\_datetime(args.get(“complete\_time”)).
      - Evaluate row.db\_set(mapping(“to\_time” → to\_time, “time\_in\_mins” → time\_diff\_in\_minutes(to\_time, row.from\_time), “operation” → args.get(“sub\_operation”), “completed\_qty” → args.get(“completed\_qty”) when last\_row.idx ….
        - Value choice on last\_row.idx equals row.idx — true gives args.get(“completed\_qty”), false gives 0.0.
- Otherwise.
  - If args.get(“start\_time”).
    - Set new\_args from Platform.\_dict(mapping(“from\_time” → get\_datetime(args.get(“start\_time”)), “operation” → args.get(“sub\_operation”), “completed\_qty” → 0.0)).
    - If employees.
      - For each name in employees.
        - Set new\_args.employee from name.get(“employee”).
        - Evaluate self.add\_start\_time\_log(new\_args).
    - Otherwise.
      - Evaluate self.add\_start\_time\_log(new\_args).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add start time log](operations-019.md#op-11b7b5aa355ecc).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L383)

<a id="op-11b7b5aa355ecc"></a>
### Job Card.add start time log

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_add_start_time_log`

**Inputs** self, args.

**State and service calls** call db\_update on row.

**Local steps**

- If (args.from\_time and args.to\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.from\_time → args.to\_time.
  - Set args.time\_in\_mins from time\_diff\_in\_minutes(args.to\_time, args.from\_time).
- Set row from self.append(“time\_logs”, args).
- Evaluate row.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0471.json#L6604) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L382)

<a id="op-e0cc6f4811d94f"></a>
### Job Card.update sub operation status

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_subordinate_operation_status`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.sub\_operations.
  - Return no value.
- Set operation\_wise\_completed\_time from mapping().
- For each time\_log in self.time\_logs.
  - If time\_log.operation does not belong to operation\_wise\_completed\_time.
    - Evaluate operation\_wise\_completed\_time.setdefault(time\_log.operation, Platform.\_dict(mapping(“status” → “Pending”, “completed\_qty” → 0.0, “process\_loss\_qty” → 0.0, “completed\_time” → 0.0, …))).
  - Set op\_row from operation\_wise\_completed\_time at time\_log.operation.
  - Set op\_row.status from “Work In Progress” when not time\_log.time\_in\_mins, otherwise “Complete”.
    - Value choice on not time\_log.time\_in\_mins — true gives “Work In Progress”, false gives “Complete”.
  - If self.status equals “On Hold”.
    - Set op\_row.status from “Pause”.
  - Evaluate op\_row.employee.append(time\_log.employee).
  - If time\_log.time\_in\_mins.
    - Update op\_row.completed\_time using + time\_log.time\_in\_mins.
    - Update op\_row.completed\_qty using + flt(time\_log.completed\_qty).
    - Update op\_row.process\_loss\_qty using + flt(time\_log.process\_loss\_qty).
- For each row in self.sub\_operations.
  - Set operation\_deatils from operation\_wise\_completed\_time.get(row.sub\_operation).
  - If operation\_deatils.
    - If row.status differs from “Complete”.
      - Set row.status from operation\_deatils.status.
    - Set row.completed\_time from operation\_deatils.completed\_time.
    - If operation\_deatils.employee.
      - Set row.completed\_time from (row.completed\_time ÷ len(set(operation\_deatils.employee))).
    - If operation\_deatils.completed\_qty.
      - Set row.completed\_qty from operation\_deatils.completed\_qty.
    - Set row.process\_loss\_qty from flt(operation\_deatils.process\_loss\_qty, row.precision(“process\_loss\_qty”)).
  - Otherwise.
    - Set row.status from “Pending”.
    - Set row.completed\_time from 0.0.
    - Set row.completed\_qty from 0.0.
    - Set row.process\_loss\_qty from 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L778) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L445)

<a id="op-e8aa4f9825c3b1"></a>
### Job Card.update time logs

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_time_logs`

**Inputs** self, row.

**Local steps**

- Evaluate self.append(“scheduled\_time\_logs”, mapping(“from\_time” → row.planned\_start\_time, “to\_time” → row.planned\_end\_time, “completed\_qty” → 0, “time\_in\_mins” → time\_diff\_in\_minutes(row.planned\_end\_time, row.plann ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0472.json#L259) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L446)
