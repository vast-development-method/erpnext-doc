# Regional rules and controller overrides · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Employee master

<a id="op-b6b3e2688a57b4"></a>
### Get linked job offer

`operation_workforce_overrides_employee_master_business_behavior_get_linked_job_offer`

**Inputs** doc, job\_applicant.

**Record and data access** read “Job Offer” via get\_value · resolve a document from “Job Offer” via get\_doc.

**Explicit results** no value · no value when job\_offer.docstatus equals 2, otherwise job\_offer.

**Local steps**

- Set offer\_name from doc.get(“job\_offer”).
- If (not offer\_name and job\_applicant).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not offer\_name → job\_applicant.
  - Set offer\_name from Platform.db.get\_value(“Job Offer”, mapping(“job\_applicant” → job\_applicant, “docstatus” → list(“!=”, 2)), “name”, order\_by = “creation desc”).
- If not offer\_name.
  - Return no value.
- Set job\_offer from Platform.get\_doc(“Job Offer”, offer\_name).
- Return no value when job\_offer.docstatus equals 2, otherwise job\_offer.
  - Value choice on job\_offer.docstatus equals 2 — true gives no value, false gives job\_offer.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L90) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L211) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L560)

<a id="op-5b63805c63390e"></a>
### Update approver role

`operation_workforce_overrides_employee_master_business_behavior_update_approver_role`

**Inputs** doc, method = no value.

**Record and data access** resolve a document from “User” via get\_doc.

**Local steps**

- If doc.leave\_approver.
  - Set user from Platform.get\_doc(“User”, doc.leave\_approver).
  - Set user.flags.ignore\_permissions from true.
  - Evaluate user.add\_roles(“Leave Approver”).
- If doc.expense\_approver.
  - Set user from Platform.get\_doc(“User”, doc.expense\_approver).
  - Set user.flags.ignore\_permissions from true.
  - Evaluate user.add\_roles(“Expense Approver”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L5794) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L215) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L564)

<a id="op-42193fd38212c4"></a>
### Update approver user roles

`operation_workforce_overrides_employee_master_business_behavior_update_approver_user_roles`

**Inputs** doc, method = no value.

**Record and data access** read “Employee” via exists.

**Local steps**

- Set approver\_roles from set().
- If Platform.db.exists(“Employee”, mapping(“leave\_approver” → doc.name)).
  - Evaluate approver\_roles.add(“Leave Approver”).
- If Platform.db.exists(“Employee”, mapping(“expense\_approver” → doc.name)).
  - Evaluate approver\_roles.add(“Expense Approver”).
- If approver\_roles.
  - Evaluate doc.append\_roles(expanded approver\_roles).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L6033) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L216) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L565)

<a id="op-db6da6c1cfa2d7"></a>
### Update employee transfer

`operation_workforce_overrides_employee_master_business_behavior_update_employee_transfer`

**Inputs** doc, method = no value.

**Record and data access** read “Employee Transfer” via exists · resolve a document from “Employee Transfer” via get\_doc.

**State and service calls** call db\_set on emp\_transfer.

**Local steps**

- If Platform.db.exists(“Employee Transfer”, mapping(“new\_employee\_id” → doc.name, “docstatus” → 1)).
  - Set emp\_transfer from Platform.get\_doc(“Employee Transfer”, mapping(“new\_employee\_id” → doc.name, “docstatus” → 1)).
  - Evaluate emp\_transfer.db\_set(“new\_employee\_id”, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L6298) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L217) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L566)

<a id="op-c890ec556c5621"></a>
### Get timeline data

`operation_workforce_overrides_employee_master_business_behavior_get_timeline_data`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** out.

**Explicit failure paths** validation helper — translated “Timeline data is only available for Employee”.

**Local steps**

- Bind dependencies get\_open\_count.
- If doctype differs from “Employee”.
  - Call the validation error handler Platform.throw(translated “Timeline data is only available for Employee”).
- Set out from mapping().
- Evaluate Platform.has\_permission(“Employee”, “read”, name, throw = true).
- Evaluate Platform.has\_permission(“Attendance”, “read”, throw = true).
- Set open\_count from get\_open\_count(doctype, name).
- Set out at “count” from open\_count at “count”.
- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set timeline\_data from dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(Attendance.attendance\_date).run()).
- Set out at “timeline\_data” from timeline\_data.
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, name, throw = true), Platform.has\_permission(“Attendance”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L91) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L213) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L562)

<a id="op-c24572c4ad6978"></a>
### Get assignable masters

`operation_workforce_overrides_employee_master_business_behavior_get_assignable_masters`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, bool).

**Record and data access** read doctype via get\_list.

**Explicit results** mapping of doctype → (Platform.has\_permission(doctype, “select”) and bool(Platform.get\_list(doctype, filters = filters, limit = 1, pluck = “name”))) for tuple(doctype, filters) drawn from masters.items().

**Local steps**

- Set masters from mapping(“Leave Policy” → mapping(“docstatus” → 1), “Salary Structure” → mapping(“docstatus” → 1, “is\_active” → “Yes”, “company” → company), “Shift Schedule” → mapping(“docstatus” → 1)).
- Return mapping of doctype → (Platform.has\_permission(doctype, “select”) and bool(Platform.get\_list(doctype, filters = filters, limit = 1, pluck = “name”))) for tuple(doctype, filters) drawn from masters.items().
  - Draw tuple(doctype, filters) from masters.items().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(doctype, “select”) → bool(Platform.get\_list(doctype, filters = filters, limit = 1, pluck = “name”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “select”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L89) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L210) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L559)

<a id="op-d749a748589a03"></a>
### Get retirement date

`operation_workforce_overrides_employee_master_business_behavior_get_retirement_date`

**Inputs** date\_of\_birth = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** dt.strftime(“%Y-%m-%d”) · no value.

**Local steps**

- If date\_of\_birth.
  - Attempt the following.
    - Set retirement\_age from cint((Platform.db.get\_single\_value(“HR Settings”, “retirement\_age”) or 60)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“HR Settings”, “retirement\_age”) → 60.
    - Set dt from add\_years(getdate(date\_of\_birth), retirement\_age).
    - Return dt.strftime(“%Y-%m-%d”).
  - On failure (ValueError).
    - Return no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “retirement\_age”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L929) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L212) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L561)

## Service · Employee overview

<a id="op-7ed08451c7c248"></a>
### Get employee overview

`operation_workforce_binding_workforce_overrides_employee_overview_get_employee_overview`

**Inputs** employee, period = “Current Fiscal Year”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** payload.

**Local steps**

- Set company from check\_access(employee).
- If period does not belong to PERIODS.
  - Set period from “Current Fiscal Year”.
- Set as\_of from getdate(today()).
- Set tuple(from\_date, to\_date) from resolve\_period(period, company, as\_of).
- Set payload from mapping(“employee” → employee, “company” → company, “currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “period” → period, …).
- For each tuple(key, fn, args) in tuple(tuple(“pay”, pay, tuple(employee, company, from\_date, to\_date)), tuple(“attendance”, attendance, tuple(employee, from\_date, min(to\_date, as\_of))), tuple(“leave”, leave\_balances, tuple(employee, as\_of ….
  - Attempt the following.
    - Set payload at key from fn(expanded args).
  - On failure (Exception).
    - Set payload at key from no value.
    - Set payload at “errors” at key from 1.
    - Evaluate Platform.log\_error(title = (“Employee Overview: ” + key)).
- Return payload.

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L160) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L211) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L211)

<a id="op-f2ceb0c93e04d2"></a>
### Check access

`operation_workforce_binding_workforce_overrides_employee_overview_check_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** employee.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L158) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L209) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L209)

<a id="op-3874df03059174"></a>
### Payroll access

`operation_workforce_binding_workforce_overrides_employee_overview_payroll_access`

**Inputs** no declared parameters.

**Explicit results** bool(Platform.has\_permission(“Salary Slip”, “read”)).

**Local steps**

- Return bool(Platform.has\_permission(“Salary Slip”, “read”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Salary Slip”, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L166) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L217) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L217)

<a id="op-efeaac21ceedec"></a>
### Slip totals

`operation_workforce_binding_workforce_overrides_employee_overview_slip_totals`

**Inputs** employee, company, from\_date, to\_date.

**Explicit results** tuple(flt(row.gross), flt(row.net), cint(row.count)).

**Local steps**

- Set ss from DocType(“Salary Slip”).
- Set row from permitted(“Salary Slip”, slip\_filters(employee, company, from\_date, to\_date), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“gross”), Coalesce(nested operand in the c … at 0.
- Return tuple(flt(row.gross), flt(row.net), cint(row.count)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L172) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L223) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L223)

<a id="op-d4721e378adeb9"></a>
### Slip filters

`operation_workforce_binding_workforce_overrides_employee_overview_slip_filters`

**Inputs** employee, company, from\_date, to\_date.

**Explicit results** list(list(“docstatus”, “=”, 1), list(“employee”, “=”, employee), list(“company”, “=”, company), list(“start\_date”, “&gt;=”, from\_date), …).

**Local steps**

- Return list(list(“docstatus”, “=”, 1), list(“employee”, “=”, employee), list(“company”, “=”, company), list(“start\_date”, “&gt;=”, from\_date), …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L171) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L222) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L222)

<a id="op-af4c7baa4ed179"></a>
### Pay

`operation_workforce_binding_workforce_overrides_employee_overview_pay`

**Inputs** employee, company, from\_date, to\_date.

**Explicit results** no value · mapping(“gross” → mapping(“value” → gross, “count” → count, “delta” → pct\_change(gross, prev\_gross)), “net” → mapping(“value” → net, “count” → count, “delta” → pct\_change(net, prev\_net)), “points” → points).

**Local steps**

- If not payroll\_access().
  - Return no value.
- Set tuple(gross, net, count) from slip\_totals(employee, company, from\_date, to\_date).
- Set tuple(prev\_gross, prev\_net, \_count) from slip\_totals(employee, company, add\_months(from\_date, negative 12), add\_months(to\_date, negative 12)).
- Set ss from DocType(“Salary Slip”).
- Set by\_month from mapping().
- For each row in permitted(“Salary Slip”, slip\_filters(employee, company, from\_date, to\_date), list(“start\_date”, Sum(ss.base\_gross\_pay).as\_(“gross”), Sum(ss.base\_net\_pay).as\_(“net”)), group\_by = “start\_date”).
  - Set month from getdate(row.start\_date).replace(day = 1).
  - Set totals from by\_month.setdefault(month, list(0.0, 0.0)).
  - Update totals at 0 using + flt(row.gross).
  - Update totals at 1 using + flt(row.net).
- Set points from list().
- Set cursor from getdate(from\_date).replace(day = 1).
- While cursor ≤ getdate(to\_date).
  - Set tuple(gross\_pay, net\_pay) from by\_month.get(cursor, tuple(0.0, 0.0)).
  - Evaluate points.append(mapping(“label” → cursor.strftime(“%b”), “title” → cursor.strftime(“%b %Y”), “gross” → gross\_pay, “net” → net\_pay)).
  - Set cursor from add\_months(cursor, 1).
- Return mapping(“gross” → mapping(“value” → gross, “count” → count, “delta” → pct\_change(gross, prev\_gross)), “net” → mapping(“value” → net, “count” → count, “delta” → pct\_change(net, prev\_net)), “points” → points).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L165) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L216) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L216)

<a id="op-07211995482aba"></a>
### Attendance

`operation_workforce_binding_workforce_overrides_employee_overview_attendance`

**Inputs** employee, from\_date, to\_date.

**Explicit results** no value · mapping(“counts” → counts, “marked” → sum(counts.values()), “days\_worked” → worked, “rate” → flt(((worked ÷ working\_days) × 100), 1) when working\_days, otherwise no value).

**Local steps**

- If not Platform.has\_permission(“Attendance”, “read”).
  - Return no value.
- Set att from DocType(“Attendance”).
- Set counts from dict.fromkeys(ATTENDANCE\_STATUS, 0).
- Set half\_days\_absent from 0.
- For each row in permitted(“Attendance”, list(list(“docstatus”, “=”, 1), list(“employee”, “=”, employee), list(“attendance\_date”, “&gt;=”, from\_date), list(“attendance\_date”, “&lt;=”, to\_date)), list(“status”, “half\_day\_status”, ….
  - If row.status belongs to counts.
    - Update counts at row.status using + cint(row.count).
  - If (row.status equals “Half Day” and row.half\_day\_status equals “Absent”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.status equals “Half Day” → row.half\_day\_status equals “Absent”.
    - Update half\_days\_absent using + cint(row.count).
- Set worked from ((counts at “Present” + counts at “Work From Home”) + ((counts at “Half Day” − half\_days\_absent) × 0.5)).
- Set working\_days from (((counts at “Present” + counts at “Work From Home”) + counts at “Half Day”) + counts at “Absent”).
- Return mapping(“counts” → counts, “marked” → sum(counts.values()), “days\_worked” → worked, “rate” → flt(((worked ÷ working\_days) × 100), 1) when working\_days, otherwise no value).
  - Value choice on working\_days — true gives flt(((worked ÷ working\_days) × 100), 1), false gives no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Attendance”, “read”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L157) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L208) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L208)

<a id="op-74d552b3a4f949"></a>
### Leave balances

`operation_workforce_binding_workforce_overrides_employee_overview_leave_balances`

**Inputs** employee, as\_of.

**Explicit results** no value · mapping(“types” → types, “remaining” → sum(generator of t at “remaining” for t drawn from types), “pending” → sum(generator of t at “pending” for t drawn from types)).

**Local steps**

- If not Platform.has\_permission(“Leave Allocation”, “read”).
  - Return no value.
- Bind dependencies get\_leave\_details.
- Set allocations from get\_leave\_details(employee, as\_of) at “leave\_allocation”.
- Set types from list of mapping(“leave\_type” → leave\_type, “remaining” → flt(details at “remaining\_leaves”), “total” → flt(details at “total\_leaves”), “taken” → flt(details at “leaves\_taken”), …) for tuple(leave\_type, det ….
  - Draw tuple(leave\_type, details) from allocations.items().
- Evaluate types.sort(key = deferred anonymous expression, reverse = true).
- Return mapping(“types” → types, “remaining” → sum(generator of t at “remaining” for t drawn from types), “pending” → sum(generator of t at “pending” for t drawn from types)).
  - Draw t from types.
  - Draw t from types.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Leave Allocation”, “read”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L163) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L214) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L214)

<a id="op-e8ffdfeae12e3c"></a>
### Pipeline

`operation_workforce_binding_workforce_overrides_employee_overview_pipeline`

**Inputs** employee, company, currency.

**Explicit results** tiles.

**Local steps**

- Set tiles from mapping().
- If Platform.has\_permission(“Leave Application”, “read”).
  - Set tiles at “leave\_requests” from open\_leave\_requests(employee).
- If Platform.has\_permission(“Expense Claim”, “read”).
  - Evaluate tiles.update(claim\_tiles(employee, company)).
- If Platform.has\_permission(“Employee Advance”, “read”).
  - Set tiles at “advances” from advance\_tile(employee, company, currency).
- Return tiles.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Leave Application”, “read”), Platform.has\_permission(“Expense Claim”, “read”) and 1 further calls.

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L167) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L218) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L218)

<a id="op-efe2ac776d4cf3"></a>
### Advance rate

`operation_workforce_binding_workforce_overrides_employee_overview_advance_rate`

**Inputs** row, currency.

**Explicit results** 1 · (flt(row.base\_paid\_amount) ÷ paid) · flt(get\_exchange\_rate(row.currency, currency, row.posting\_date)).

**Local steps**

- If row.currency equals currency.
  - Return 1.
- Set paid from flt(row.paid\_amount).
- If (paid and flt(row.base\_paid\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in paid → flt(row.base\_paid\_amount).
  - Return (flt(row.base\_paid\_amount) ÷ paid).
- Return flt(get\_exchange\_rate(row.currency, currency, row.posting\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L155) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L206) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L206)

<a id="op-8b6eb65afdf332"></a>
### Open leave requests

`operation_workforce_binding_workforce_overrides_employee_overview_open_leave_requests`

**Inputs** employee.

**Explicit results** mapping(“value” → flt(row.days), “count” → cint(row.count), “started” → cint(row.started)).

**Local steps**

- Set la from DocType(“Leave Application”).
- Set row from permitted(“Leave Application”, mapping(“docstatus” → 0, “employee” → employee, “status” → “Open”), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“days”), Count(nested … at 0.
- Return mapping(“value” → flt(row.days), “count” → cint(row.count), “started” → cint(row.started)).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L164) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L215) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L215)

<a id="op-205115e927608b"></a>
### Claim tiles

`operation_workforce_binding_workforce_overrides_employee_overview_claim_tiles`

**Inputs** employee, company.

**Explicit results** mapping(“claims\_awaiting” → mapping(“value” → flt(awaiting.value, 2), “count” → cint(awaiting.count)), “claims\_unpaid” → mapping(“value” → flt(unpaid.value, 2), “count” → cint(unpaid.count))).

**Local steps**

- Set ec from DocType(“Expense Claim”).
- Set awaiting from permitted(“Expense Claim”, mapping(“docstatus” → 0, “employee” → employee, “company” → company, “approval\_status” → “Draft”), list(Coalesce(nested operand in the contract(nested operand in the contract), 0 … at 0.
- Set unpaid from permitted(“Expense Claim”, mapping(“docstatus” → 1, “employee” → employee, “company” → company, “approval\_status” → “Approved”, …), list(Coalesce(nested operand in the contract(nested operand in the contra … at 0.
- Return mapping(“claims\_awaiting” → mapping(“value” → flt(awaiting.value, 2), “count” → cint(awaiting.count)), “claims\_unpaid” → mapping(“value” → flt(unpaid.value, 2), “count” → cint(unpaid.count))).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L159) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L210) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L210)

<a id="op-aba844c5d67a40"></a>
### Advance tile

`operation_workforce_binding_workforce_overrides_employee_overview_advance_tile`

**Inputs** employee, company, currency.

**Explicit results** mapping(“value” → flt(to\_settle, 2), “to\_pay” → flt(to\_pay, 2), “count” → len(open\_advances)).

**Local steps**

- Set rows from permitted(“Employee Advance”, mapping(“docstatus” → 1, “employee” → employee, “company” → company), list(“name”, “posting\_date”, “status”, “currency”, …)).
- Set tuple(to\_settle, to\_pay, open\_advances) from tuple(0.0, 0.0, set()).
- For each row in rows.
  - Set paid from flt(row.paid\_amount).
  - Set rate from advance\_rate(row, currency).
  - Set unsettled from ((paid − flt(row.claimed\_amount)) − flt(row.return\_amount)).
  - If unsettled &gt; 0.
    - Update to\_settle using + (unsettled × rate).
    - Evaluate open\_advances.add(row.name).
  - If row.status belongs to UNPAID\_ADVANCE\_STATUS.
    - Update to\_pay using + ((flt(row.advance\_amount) − paid) × rate).
    - Evaluate open\_advances.add(row.name).
- Return mapping(“value” → flt(to\_settle, 2), “to\_pay” → flt(to\_pay, 2), “count” → len(open\_advances)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L156) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L207) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L207)

<a id="op-137a728b1e8826"></a>
### Get employee transactions

`operation_workforce_binding_workforce_overrides_employee_overview_get_employee_transactions`

**Inputs** employee, doc\_type = “All”, limit = 20.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** rows at slice no value to limit.

**Local steps**

- Evaluate check\_access(employee).
- Set limit from min((cint(limit) or 20), 100).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(limit) → 20.
- Set wanted from list(doc\_type) when doc\_type belongs to TRANSACTION\_TYPES, otherwise list(TRANSACTION\_TYPES).
  - Value choice on doc\_type belongs to TRANSACTION\_TYPES — true gives list(doc\_type), false gives list(TRANSACTION\_TYPES).
- Set rows from list().
- For each doctype in wanted.
  - If Platform.has\_permission(doctype, “read”).
    - Evaluate rows.extend(transaction\_rows(doctype, employee, limit)).
- Evaluate rows.sort(key = deferred anonymous expression, reverse = true).
- Return rows at slice no value to limit.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L161) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L212) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L212)

<a id="op-e134ec00f69d87"></a>
### Transaction rows

`operation_workforce_binding_workforce_overrides_employee_overview_transaction_rows`

**Inputs** doctype, employee, limit.

**Record and data access** read doctype via get\_list.

**Explicit results** list of mapping(“name” → r.name, “doctype” → doctype, “type\_label” → translated doctype, “date” → str(r.date), …) for r drawn from Platform.get\_list(doctype, filters = filters, fields = list(“name”, “statu ….

**Local steps**

- Set fields from mapping(“Salary Slip” → list(“start\_date as date”, “base\_net\_pay as amount”), “Leave Application” → list(“from\_date as date”, “total\_leave\_days as days”, “docstatus”), “Expense Claim” → list(“posting\_date  ….
- Set filters from mapping(“employee” → employee, “docstatus” → list(“!=”, 2)).
- If doctype belongs to tuple(“Salary Slip”, “Employee Advance”).
  - Set filters at “docstatus” from 1.
- Return list of mapping(“name” → r.name, “doctype” → doctype, “type\_label” → translated doctype, “date” → str(r.date), …) for r drawn from Platform.get\_list(doctype, filters = filters, fields = list(“name”, “statu ….
  - Draw r from Platform.get\_list(doctype, filters = filters, fields = list(“name”, “status”, “company”, expanded fields), order\_by = “date desc, creation desc”, limit = limit).
  - Value choice on doctype equals “Leave Application” — true gives flt(r.days), false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L173) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L224) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L224)

<a id="op-8e7c96ebcea1f8"></a>
### Row currency

`operation_workforce_binding_workforce_overrides_employee_overview_row_currency`

**Inputs** doctype, row.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** row.currency · Platform.get\_cached\_value(“Company”, row.company, “default\_currency”).

**Local steps**

- If doctype equals “Employee Advance”.
  - Return row.currency.
- Return Platform.get\_cached\_value(“Company”, row.company, “default\_currency”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, row.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L169) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L220) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L220)

<a id="op-e8f0a1ac3520f2"></a>
### Row amount

`operation_workforce_binding_workforce_overrides_employee_overview_row_amount`

**Inputs** doctype, row.

**Explicit results** flt(row.advance\_amount) · (flt(row.total\_claimed\_amount) × flt((row.exchange\_rate or 1))) · no value · flt(row.amount).

**Local steps**

- If doctype equals “Employee Advance”.
  - Return flt(row.advance\_amount).
- If doctype equals “Expense Claim”.
  - Return (flt(row.total\_claimed\_amount) × flt((row.exchange\_rate or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.exchange\_rate → 1.
- If doctype equals “Leave Application”.
  - Return no value.
- Return flt(row.amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L168) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L219) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L219)
