# Supporting services · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Telemetry

<a id="op-d69bdbd31a2f2c"></a>
### Should skip

`operation_workforce_binding_workforce_telemetry_should_skip`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** (\_skip\_context() or not is\_enabled()).

**Local steps**

- Return (\_skip\_context() or not is\_enabled()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_skip\_context() → not is\_enabled().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L195) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L246) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L246)

<a id="op-f65918524d2ff5"></a>
### Sanitize properties

`operation_workforce_binding_workforce_telemetry_sanitize_properties`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** properties.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L194) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L245) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L245)

<a id="op-357b581c48a33c"></a>
### Capture

`operation_workforce_telemetry_business_behavior_capture`

**Inputs** event, properties = no value.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If \_should\_skip().
  - Return no value.
- Evaluate \_capture(event, APP, properties = sanitize\_properties(properties)).
- Evaluate \_track\_conversion().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L19) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1127) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L74)

<a id="op-0e0de9d2b0a359"></a>
### Claim milestone

`operation_workforce_telemetry_business_behavior_claim_milestone`

**Inputs** event.

**Declared result** bool.

**Record and data access** resolve a document from mapping(“doctype” → MILESTONE\_DOCTYPE, “event” → event) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → MILESTONE\_DOCTYPE, “event” → event)).

**Explicit results** claimed.

**Local steps**

- Set claimed from false.
- Set mute\_messages from Platform.flags.mute\_messages.
- Set Platform.flags.mute\_messages from true.
- Attempt the following.
  - Within savepoint(catch = Exception).
    - Evaluate Platform.get\_doc(mapping(“doctype” → MILESTONE\_DOCTYPE, “event” → event)).insert(ignore\_permissions = true).
    - Set claimed from true.
- On exit, including pending return or failure.
  - Set Platform.flags.mute\_messages from mute\_messages.
- Return claimed.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L22) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1131) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L78)

<a id="op-987ddbfdc7a8a3"></a>
### Capture first

`operation_workforce_telemetry_business_behavior_capture_first`

**Inputs** event, properties = no value.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If \_should\_skip().
  - Return no value.
- Set age from site\_age().
- If (not age or age &gt; ACTIVATION\_WINDOW\_DAYS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not age → age &gt; ACTIVATION\_WINDOW\_DAYS.
  - Return no value.
- If not \_claim\_milestone(event).
  - Return no value.
- Evaluate capture(event, mapping(“day\_since\_install” → age, expand (properties or mapping()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in properties → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L21) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1130) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L77)

<a id="op-09e9ebe7dbc175"></a>
### Track conversion

`operation_workforce_telemetry_business_behavior_track_conversion`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read MILESTONE\_DOCTYPE via exists · read MILESTONE\_DOCTYPE via get\_value.

**Explicit results** no value.

**Local steps**

- If Platform.db.exists(MILESTONE\_DOCTYPE, CONVERSION\_EVENT).
  - Return no value.
- Set first\_capture from Platform.db.get\_value(MILESTONE\_DOCTYPE, FIRST\_CAPTURE\_MILESTONE, “creation”).
- If not first\_capture.
  - Evaluate \_claim\_milestone(FIRST\_CAPTURE\_MILESTONE).
  - Return no value.
- Set days\_since\_first\_capture from date\_diff(today(), first\_capture).
- If days\_since\_first\_capture ≤ CONVERSION\_WINDOW\_DAYS.
  - Return no value.
- If \_claim\_milestone(CONVERSION\_EVENT).
  - Evaluate \_capture(CONVERSION\_EVENT, APP, properties = mapping(“days\_since\_first\_capture” → days\_since\_first\_capture, “day\_since\_install” → site\_age())).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L1315) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1145) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L92)

<a id="op-46b8b36b57cddc"></a>
### Duration days

`operation_workforce_telemetry_business_behavior_duration_days`

**Inputs** from\_date, to\_date.

**Declared result** (int bitwise or no value).

**Explicit results** no value · (date\_diff(to\_date, from\_date) + 1).

**Local steps**

- If not (from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date.
  - Return no value.
- Return (date\_diff(to\_date, from\_date) + 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L1624) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1132) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L79)

<a id="op-ca0375d28491ae"></a>
### On leave application submit

`operation_workforce_telemetry_business_behavior_on_leave_application_submit`

**Inputs** doc, method = no value.

**Record and data access** read “Leave Type” via get\_value.

**Local steps**

- Set flags from (Platform.db.get\_value(“Leave Type”, doc.leave\_type, LEAVE\_TYPE\_FLAGS, as\_dict = true) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Leave Type”, doc.leave\_type, LEAVE\_TYPE\_FLAGS, as\_dict = true) → mapping().
- Evaluate capture(“leave\_application\_submitted”, mapping(expand mapping of flag → bool(flags.get(flag)) for flag drawn from LEAVE\_TYPE\_FLAGS, “total\_leave\_days” → doc.total\_leave\_days, “half\_day” → bool(doc.half\_day ….
  - Draw flag from LEAVE\_TYPE\_FLAGS.
- Evaluate capture\_first(“first\_leave\_applied”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L27) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1139) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L86)

<a id="op-52114204e7691c"></a>
### On expense claim submit

`operation_workforce_telemetry_business_behavior_on_expense_claim_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“expense\_claim\_submitted”, mapping(“expense\_count” → len((doc.expenses or list())), “is\_paid” → bool(doc.is\_paid), “has\_advances” → bool(doc.get(“advances”)), “has\_taxes” → bool(doc.get(“taxes”)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.expenses → list().
- Evaluate capture\_first(“first\_expense\_claimed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L25) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1136) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L83)

<a id="op-bd8c61f820d277"></a>
### On attendance request submit

`operation_workforce_telemetry_business_behavior_on_attendance_request_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“attendance\_request\_submitted”, mapping(“reason” → doc.reason, “half\_day” → bool(doc.half\_day), “include\_holidays” → bool(doc.include\_holidays), “days” → \_duration\_days(doc.from\_date, doc.to\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L24) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1134) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L81)

<a id="op-88e822a4268725"></a>
### On shift request submit

`operation_workforce_telemetry_business_behavior_on_shift_request_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“shift\_request\_submitted”, mapping(“has\_approver” → bool(doc.approver), “days” → \_duration\_days(doc.from\_date, doc.to\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L28) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1143) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L90)

<a id="op-be9994d92f89c9"></a>
### On employee checkin

`operation_workforce_telemetry_business_behavior_on_employee_checkin`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“employee\_checkin”, mapping(“log\_type” → doc.log\_type, “has\_shift” → bool(doc.shift), “has\_geolocation” → bool((doc.latitude and doc.longitude)), “via\_device” → bool(doc.device\_id))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.latitude → doc.longitude.
- Evaluate capture\_first(“first\_attendance\_marked”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L2548) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1135) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L82)

<a id="op-2ab695069c4816"></a>
### On milestone insert

`operation_workforce_telemetry_business_behavior_on_milestone_insert`

**Inputs** doc, method = no value.

**Local steps**

- Set event from CREATION\_MILESTONES.get(doc.doctype).
- If event.
  - Evaluate capture\_first(event).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L2750) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1140) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L87)

<a id="op-79d026f78915a7"></a>
### On milestone submit

`operation_workforce_telemetry_business_behavior_on_milestone_submit`

**Inputs** doc, method = no value.

**Local steps**

- Set event from SUBMISSION\_MILESTONES.get(doc.doctype).
- If event.
  - Evaluate capture\_first(event).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L2856) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1141) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L88)

<a id="op-1b6bf039440b17"></a>
### On payroll entry submit

`operation_workforce_telemetry_business_behavior_on_payroll_entry_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“payroll\_entry\_submitted”, mapping(“payroll\_frequency” → doc.payroll\_frequency, “employee\_count” → (doc.number\_of\_employees or len((doc.employees or list()))), “validate\_attendance” → bool(doc.vali ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.number\_of\_employees → len((doc.employees or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.employees → list().
- Evaluate capture\_first(“first\_payroll\_run”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L2962) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1142) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L89)

<a id="op-4b8df61d0f1656"></a>
### On job offer submit

`operation_workforce_telemetry_business_behavior_on_job_offer_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“job\_offer\_made”, mapping(“compensation\_mode” → doc.calculate\_component\_amount\_from, “has\_salary\_structure” → bool(doc.salary\_structure), “component\_count” → len(list of row for row drawn from (nes ….
  - Draw row from (doc.get(“ctc\_breakup”) or list()), keep a combination only if (not row.get(“is\_summary”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“ctc\_breakup”) → list().
- Evaluate capture\_first(“first\_job\_offer\_made”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L26) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1138) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L85)

<a id="op-4d9d573ba25179"></a>
### On job offer change

`operation_workforce_binding_workforce_telemetry_on_job_offer_change`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- Set previous from doc.get\_doc\_before\_save().
- If (not previous or previous.status equals doc.status).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous → previous.status equals doc.status.
  - Return no value.
- Evaluate capture(“job\_offer\_status\_changed”, mapping(“from\_status” → previous.status, “to\_status” → doc.status, “days\_since\_offer” → \_days\_since(doc.offer\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L193) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L244) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L244)

<a id="op-203b86f4b0139a"></a>
### On employee from job offer

`operation_workforce_binding_workforce_telemetry_on_employee_from_job_offer`

**Inputs** doc, method = no value.

**Record and data access** read “Job Offer” via get\_value.

**Explicit results** no value.

**Local steps**

- If not doc.get(“job\_offer”).
  - Return no value.
- Set offer\_date from Platform.db.get\_value(“Job Offer”, doc.job\_offer, “offer\_date”).
- Evaluate capture(“employee\_created\_from\_job\_offer”, mapping(“days\_since\_offer” → \_days\_since(offer\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L192) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L243) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L243)

<a id="op-bed688b4ef4502"></a>
### Days since

`operation_workforce_binding_workforce_telemetry_days_since`

**Inputs** date.

**Declared result** (int bitwise or no value).

**Explicit results** date\_diff(today(), date) when date, otherwise no value.

**Local steps**

- Return date\_diff(today(), date) when date, otherwise no value.
  - Value choice on date — true gives date\_diff(today(), date), false gives no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L191) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L242) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L242)

<a id="op-437629198e3e25"></a>
### On appraisal submit

`operation_workforce_telemetry_business_behavior_on_appraisal_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“appraisal\_submitted”, mapping(“has\_cycle” → bool(doc.appraisal\_cycle), “goal\_count” → len((doc.get(“goals”) or list())), “kra\_count” → len((doc.get(“appraisal\_kra”) or list())), “rated\_manually” → ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“goals”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“appraisal\_kra”) → list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L23) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1133) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L80)

<a id="op-874a0e4e0ce163"></a>
### On interview submit

`operation_workforce_telemetry_business_behavior_on_interview_submit`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate capture(“interview\_submitted”, mapping(“status” → doc.status, “panel\_size” → len((doc.get(“interview\_details”) or list())), “from\_job\_opening” → bool(doc.job\_opening))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“interview\_details”) → list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L3674) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1137) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L84)

<a id="op-cea3fcf2085a95"></a>
### Capture daily attendance pulse

`operation_workforce_telemetry_business_behavior_capture_daily_attendance_pulse`

**Inputs** no declared parameters.

**Record and data access** read “Employee” via count · read “Employee Checkin” via count · read “Attendance” via count.

**Explicit results** no value.

**Local steps**

- If \_should\_skip().
  - Return no value.
- Set active\_employees from Platform.db.count(“Employee”, mapping(“status” → “Active”)).
- If not active\_employees.
  - Return no value.
- Set day from add\_days(today(), negative 1).
- Set tuple(day\_start, day\_end) from tuple(formatted text {day} 00:00:00, formatted text {day} 23:59:59).
- Set checkins from Platform.db.count(“Employee Checkin”, mapping(“time” → list(“between”, list(day\_start, day\_end)))).
- Set Checkin from Platform.qb.DocType(“Employee Checkin”).
- Set employees\_checked\_in from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where((nested operand in the contract ≥ nested operand in the contract bitwise and nested operand in the contract ≤ nested operand in the cont … → 0.
- Set attendance\_marked from Platform.db.count(“Attendance”, mapping(“attendance\_date” → day, “docstatus” → 1)).
- Bind local operation rate for subsequent calls.
- Evaluate \_capture(“attendance\_daily\_summary”, APP, properties = mapping(“active\_employees” → active\_employees, “checkins” → checkins, “employees\_checked\_in” → employees\_checked\_in, “attendance\_marked” → attendance\_ ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L20) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1128) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L75)

<a id="op-8beb5e542710ed"></a>
### Capture daily attendance pulse.rate

`operation_workforce_telemetry_business_behavior_capture_daily_attendance_pulse_rate`

**Inputs** n.

**Explicit results** round((n ÷ active\_employees), 3).

**Local steps**

- Return round((n ÷ active\_employees), 3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L4686) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1129) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L76)

## Service · Uninstall

<a id="op-208c96f2ee00af"></a>
### Before uninstall

`operation_workforce_uninstall_business_behavior_before_uninstall`

**Inputs** no declared parameters.

**Explicit failure paths** e.

**Local steps**

- Attempt the following.
  - Evaluate print(“Removing customizations created by the Platform HR app...”).
  - Evaluate remove\_custom\_fields().
- On failure (Exception) bound to e.
  - Set BUG\_REPORT\_URL from text in the contract.
  - Evaluate click.secho(formatted text Removing Customizations for Platform HR failed due to an error. Please try again or report the issue on {BUG\_REPORT\_URL} if not resolved., fg = “bright\_red”).
  - Raise e.
- Evaluate click.secho(“Platform HR app customizations have been removed successfully...”, fg = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L1798) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1219) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L165)
