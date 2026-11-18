# Employment and attendance · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job offer

[Record definition](../../../../data/record-types/job_offer.json)

<a id="op-d32a1914e8aea1"></a>
### Job Offer.validate duplicate job offer

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_validate_duplicate_job_offer`

**Inputs** self.

**Record and data access** read “Job Offer” via exists.

**Explicit failure paths** validation helper — translated “Job Offer {0} already exists for {1}”.format(get\_link\_to\_form(“Job Offer”, duplicate), Platform.bold(self.applicant\_email)).

**Local steps**

- Set duplicate from Platform.db.exists(“Job Offer”, mapping(“applicant\_email” → self.applicant\_email, “docstatus” → list(“!=”, 2), “status” → list(“not in”, list(“Rejected”, “Cancelled”)), “name” → list(“!=”, self.name))).
- If duplicate.
  - Call the validation error handler Platform.throw(translated “Job Offer {0} already exists for {1}”.format(get\_link\_to\_form(“Job Offer”, duplicate), Platform.bold(self.applicant\_email))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L5698) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L930) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L910)

<a id="op-138b65c5b06d29"></a>
### Job Offer.set compensation

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_set_compensation`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.salary\_structure or not self.calculate\_component\_amount\_from).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.salary\_structure → not self.calculate\_component\_amount\_from.
  - If self.salary\_structure.
    - Set self.ctc from 0.
  - Set self.gross from 0.
  - Evaluate self.set(“ctc\_breakup”, list()).
  - Return no value.
- If not self.compensation\_inputs\_changed().
  - Return no value.
- Set details from compute\_compensation(self).
- Set self.base from details at “base”.
- Set self.ctc from details at “ctc”.
- Set self.gross from details at “gross”.
- Evaluate self.set(“ctc\_breakup”, details at “components”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [compensation inputs changed](operations-022.md#op-c83483a560de47).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L79) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L130) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L130)

<a id="op-c83483a560de47"></a>
### Job Offer.compensation inputs changed

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_compensation_inputs_changed`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · any(generator of not \_same\_input(self.get(f), previous.get(f)) for f drawn from fieldnames).

**Local steps**

- If not self.ctc\_breakup.
  - Return true.
- Set previous from self.doc\_before\_save().
- If not previous.
  - Return true.
- Set driver from “ctc” when self.calculate\_component\_amount\_from equals “CTC”, otherwise “base”.
  - Value choice on self.calculate\_component\_amount\_from equals “CTC” — true gives “ctc”, false gives “base”.
- Set fieldnames from tuple(expanded COMPENSATION\_INPUTS, driver, expanded shared\_regional\_fieldnames(self)).
- Return any(generator of not \_same\_input(self.get(f), previous.get(f)) for f drawn from fieldnames).
  - Draw f from fieldnames.

**Methods declared on this owner** [doc before save](operations-022.md#op-fed3df8ef76c73).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L74) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L125) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L125)

<a id="op-fed3df8ef76c73"></a>
### Job Offer.doc before save

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_doc_before_save`

**Inputs** self.

**Explicit results** previous.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Evaluate self.load\_doc\_before\_save().
  - Set previous from self.get\_doc\_before\_save().
- Return previous.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L75) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L126) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L126)

<a id="op-d266fd1390f97c"></a>
### Job Offer.validate vacancies

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_validate_vacancies`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single.

**Explicit failure paths** validation helper — translated “There are no vacancies under staffing plan {0}”.format(error\_variable).

**Local steps**

- Set staffing\_plan from get\_staffing\_plan\_detail(self.designation, self.company, self.offer\_date).
- Set check\_vacancies from Platform.get\_single(“HR Settings”).check\_vacancies.
- If (staffing\_plan and check\_vacancies).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in staffing\_plan → check\_vacancies.
  - Set job\_offers from self.get\_job\_offer(staffing\_plan.from\_date, staffing\_plan.to\_date).
  - If (not staffing\_plan.get(“vacancies”) or (cint(staffing\_plan.vacancies) − len(job\_offers)) ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not staffing\_plan.get(“vacancies”) → (cint(staffing\_plan.vacancies) − len(job\_offers)) ≤ 0.
    - Set error\_variable from (“for ” + Platform.bold(self.designation)).
    - If staffing\_plan.get(“parent”).
      - Set error\_variable from Platform.bold(get\_link\_to\_form(“Staffing Plan”, staffing\_plan.parent)).
    - Call the validation error handler Platform.throw(translated “There are no vacancies under staffing plan {0}”.format(error\_variable)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get job offer](operations-022.md#op-5d90e40da107dd).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L5997) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L931) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L911)

<a id="op-4af139a956fa8e"></a>
### Job Offer.on change

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_on_change`

**Inputs** self.

**Local steps**

- Evaluate update\_job\_applicant(self.status, self.job\_applicant).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L6459) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L926) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L906)

<a id="op-5d90e40da107dd"></a>
### Job Offer.get job offer

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_get_job_offer`

**Inputs** self, from\_date, to\_date.

**Record and data access** read “Job Offer” via get\_all.

**Explicit results** Platform.get\_all(“Job Offer”, filters = mapping(“offer\_date” → list(“between”, tuple(from\_date, to\_date)), “designation” → self.designation, “company” → self.company, “docstatus” → 1), fields = list(“name”)).

**Local steps**

- Return Platform.get\_all(“Job Offer”, filters = mapping(“offer\_date” → list(“between”, tuple(from\_date, to\_date)), “designation” → self.designation, “company” → self.company, “docstatus” → 1), fields = list(“name”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L6523) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L925) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L905)

<a id="op-31a0fe8f3ba2bd"></a>
### Job Offer.on discard

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L6718) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L927) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L907)

<a id="op-dbfefe7f56b1c3"></a>
### Update job applicant

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_update_job_applicant`

**Inputs** status, job\_applicant.

**Local steps**

- If (job\_applicant and status belongs to tuple(“Accepted”, “Rejected”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_applicant → status belongs to tuple(“Accepted”, “Rejected”).
  - Evaluate Platform.set\_value(“Job Applicant”, job\_applicant, “status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L6781) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L934) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L914)

<a id="op-c8083bb0e8134f"></a>
### Get staffing plan detail

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_get_staffing_plan_detail`

**Inputs** designation, company, offer\_date.

**Explicit results** Platform.\_dict(detail at 0) when (detail and detail at 0.parent), otherwise no value.

**Local steps**

- Set spd from Platform.qb.DocType(“Staffing Plan Detail”).
- Set sp from Platform.qb.DocType(“Staffing Plan”).
- Set detail from nested operand in the contract().where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≤ nested operand in the contract)).groupby(spd ….
- Return Platform.\_dict(detail at 0) when (detail and detail at 0.parent), otherwise no value.
  - Value choice on (detail and detail at 0.parent) — true gives Platform.\_dict(detail at 0), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in detail → detail at 0.parent.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L924) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L904)

<a id="op-5699f23158c33f"></a>
### Make employee

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_make_employee`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doc from get\_mapped\_doc(“Job Offer”, source\_name, mapping(“Job Offer” → mapping(“doctype” → “Employee”, “field\_map” → mapping(“applicant\_name” → “employee\_name”, “offer\_date” → “scheduled\_confirmation\_date”))), tar ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L633) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L932) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L912)

<a id="op-13c04d39aae91c"></a>
### Make employee.set missing values

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_make_employee_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.personal\_email from source.applicant\_email.
- Set target.first\_name from source.applicant\_name.
- Set target.job\_offer from source.name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L957) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L933) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L913)

<a id="op-1528c6c4efe708"></a>
### Build prospective assignment

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_build_prospective_assignment`

**Inputs** offer.

**Record and data access** read “Salary Structure” via get\_cached\_value.

**State and service calls** request new\_doc for “Employee” · request new\_doc for “Salary Structure Assignment”.

**Explicit results** assignment.

**Local steps**

- Set structure\_currency from Platform.get\_cached\_value(“Salary Structure”, offer.salary\_structure, “currency”).
- Set from\_date from (offer.date\_of\_joining or offer.offer\_date or nowdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in offer.date\_of\_joining → offer.offer\_date → nowdate().
- Set prospective\_employee from Platform.new\_doc(“Employee”).
- Set prospective\_employee.company from offer.company.
- Set prospective\_employee.department from offer.department.
- Set prospective\_employee.designation from offer.designation.
- Set prospective\_employee.grade from offer.grade.
- Set prospective\_employee.branch from offer.branch.
- Set prospective\_employee.employment\_type from offer.employment\_type.
- Set prospective\_employee.date\_of\_joining from from\_date.
- Set assignment from Platform.new\_doc(“Salary Structure Assignment”).
- Set assignment.employee from prospective\_employee.
- Set assignment.salary\_structure from offer.salary\_structure.
- Set assignment.company from offer.company.
- Set assignment.currency from (offer.currency or structure\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in offer.currency → structure\_currency.
- Set assignment.variable from flt(offer.variable).
- Set assignment.from\_date from from\_date.
- Set assignment.department from offer.department.
- Set assignment.designation from offer.designation.
- Set assignment.grade from offer.grade.
- Evaluate copy\_regional\_config(offer, assignment).
- Return assignment.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Structure”, offer.salary\_structure, “currency”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L64) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L115) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L115)

<a id="op-1e67d31d7f0adb"></a>
### Same input

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_same_input`

**Inputs** current, previous.

**Declared result** bool.

**Explicit results** flt(current) equals flt(previous) · str((current or empty text)) equals str((previous or empty text)).

**Local steps**

- If (isinstance(current, (int bitwise or float)) or isinstance(previous, (int bitwise or float))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(current, (int bitwise or float)) → isinstance(previous, (int bitwise or float)).
  - Return flt(current) equals flt(previous).
- Return str((current or empty text)) equals str((previous or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in current → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L83) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L134) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L134)

<a id="op-93fdacd7aa6d22"></a>
### Shared regional fieldnames

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_shared_regional_fieldnames`

**Inputs** offer.

**Declared result** list at str.

**Explicit results** list of df.fieldname for df drawn from Platform.get\_meta(“Salary Structure Assignment”).get(“fields”, mapping(“is\_custom\_field” → 1)) where (df.fieldtype does not belong to Platform.model.no\_value\_fields a ….

**Local steps**

- Set offer\_fieldnames from set of df.fieldname for df drawn from offer.meta.fields.
  - Draw df from offer.meta.fields.
- Return list of df.fieldname for df drawn from Platform.get\_meta(“Salary Structure Assignment”).get(“fields”, mapping(“is\_custom\_field” → 1)) where (df.fieldtype does not belong to Platform.model.no\_value\_fields a ….
  - Draw df from Platform.get\_meta(“Salary Structure Assignment”).get(“fields”, mapping(“is\_custom\_field” → 1)), keep a combination only if ((df.fieldtype does not belong to Platform.model.no\_value\_fields and df.fieldname belongs to offer\_fieldnames)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to Platform.model.no\_value\_fields → df.fieldname belongs to offer\_fieldnames.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L84) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L135) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L135)

<a id="op-719fa71ff9dd62"></a>
### Copy regional config

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_copy_regional_config`

**Inputs** offer, assignment.

**Declared result** no value.

**Local steps**

- For each fieldname in shared\_regional\_fieldnames(offer).
  - Evaluate assignment.set(fieldname, offer.get(fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L66) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L117) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L117)

<a id="op-ebcb61c7d4cad2"></a>
### Get components left out of offer

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_components_left_out_of_offer`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Workforce.allow\_regional.

**Declared result** tuple at tuple(str, ellipsis).

**Explicit results** tuple().

**Local steps**

- Return tuple().

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L71) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L122) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L122)

<a id="op-aa594a6e069270"></a>
### Get breakup rows

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_breakup_rows`

**Inputs** assignment, periods, total\_ctc.

**Declared result** list at dict.

**Explicit results** list() · breakup.

**Local steps**

- Set rows\_by\_type from assignment.get\_evaluated\_components().
- Bind local operation row for subsequent calls.
- Bind local operation payable for subsequent calls.
- Set earnings from payable(“earnings”).
- Set left\_out from set(get\_components\_left\_out\_of\_offer()).
- Set employer\_contributions from payable(“employer\_contributions”).
- Set shown\_contributions from list of r for r drawn from employer\_contributions where r.salary\_component does not belong to left\_out.
  - Draw r from employer\_contributions, keep a combination only if (r.salary\_component does not belong to left\_out).
- If (not earnings and not employer\_contributions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not earnings → not employer\_contributions.
  - Return list().
- Set gross from (flt(assignment.annual\_gross\_earning) ÷ periods).
- Set deductions from sum(generator of flt(r.default\_amount) for r drawn from payable(“deductions”) where not r.do\_not\_include\_in\_total).
  - Draw r from payable(“deductions”), keep a combination only if (not r.do\_not\_include\_in\_total).
- Set breakup from list of row(r.salary\_component, flt(r.default\_amount), 0) for r drawn from earnings.
  - Draw r from earnings.
- Evaluate breakup.append(row(translated “Gross Pay”, gross, 1)).
- Update breakup using + list of row(r.salary\_component, flt(r.default\_amount), 0) for r drawn from shown\_contributions.
  - Draw r from shown\_contributions.
- Set ctc\_label from translated “Total Cost to Company (CTC)\* (Includes Statutory Contributions)” when len(shown\_contributions) &lt; len(employer\_contributions), otherwise translated “Total Cost to Company (CTC)”.
  - Value choice on len(shown\_contributions) &lt; len(employer\_contributions) — true gives translated “Total Cost to Company (CTC)\* (Includes Statutory Contributions)”, false gives translated “Total Cost to Company (CTC)”.
- Evaluate breakup.append(row(ctc\_label, (flt(total\_ctc) ÷ periods), 1)).
- Evaluate breakup.append(row(translated “Take Home\* (Income Tax applicable as per IT Act)”, (gross − deductions), 1)).
- Return breakup.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L67) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L118) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L118)

<a id="op-1a65ce9097ccd9"></a>
### Get breakup rows.row

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_breakup_rows_row`

**Inputs** label, per\_cycle, is\_summary.

**Declared result** dict.

**Explicit results** mapping(“fixed\_components” → label, “per\_cycle” → flt(per\_cycle), “yearly” → flt((per\_cycle × periods)), “currency” → assignment.currency, …).

**Local steps**

- Return mapping(“fixed\_components” → label, “per\_cycle” → flt(per\_cycle), “yearly” → flt((per\_cycle × periods)), “currency” → assignment.currency, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L69) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L120) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L120)

<a id="op-1a9ed5d01feb7c"></a>
### Get breakup rows.payable

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_breakup_rows_payable`

**Inputs** component\_type.

**Declared result** list.

**Explicit results** list of r for r drawn from rows\_by\_type at component\_type where (not r.statistical\_component and flt(r.default\_amount)).

**Local steps**

- Return list of r for r drawn from rows\_by\_type at component\_type where (not r.statistical\_component and flt(r.default\_amount)).
  - Draw r from rows\_by\_type at component\_type, keep a combination only if ((not r.statistical\_component and flt(r.default\_amount))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not r.statistical\_component → flt(r.default\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L68) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L119) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L119)

<a id="op-8d508720ee908b"></a>
### Compute compensation

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_compute_compensation`

**Inputs** offer.

**Declared result** dict.

**Record and data access** read “Salary Structure” via get\_cached\_value.

**Explicit results** empty · mapping(“base” → base, “ctc” → total\_ctc, “gross” → (flt(assignment.annual\_gross\_earning) ÷ periods), “components” → get\_breakup\_rows(assignment, periods, total\_ctc), …).

**Local steps**

- Bind dependencies PERIODS\_PER\_YEAR.
- Bind dependencies CTC\_SOLVER\_TOLERANCE.
- Set empty from mapping(“base” → flt(offer.base), “ctc” → 0.0, “gross” → 0.0, “components” → list(), …).
- If (not offer.salary\_structure or not offer.calculate\_component\_amount\_from).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not offer.salary\_structure → not offer.calculate\_component\_amount\_from.
  - Return empty.
- Set assignment from build\_prospective\_assignment(offer).
- Set ctc\_adjusted from false.
- If offer.calculate\_component\_amount\_from equals “CTC”.
  - Set target\_ctc from flt(offer.ctc).
  - If target\_ctc ≤ 0.
    - Return empty.
  - Set tuple(base, total\_ctc) from \_resolve\_base\_for\_target(assignment, flt(offer.base), target\_ctc).
  - Set ctc\_adjusted from abs((total\_ctc − target\_ctc)) &gt; CTC\_SOLVER\_TOLERANCE.
- Otherwise.
  - Set base from flt(offer.base).
  - If not base.
    - Return empty.
  - Set assignment.base from base.
  - Evaluate assignment.calculate\_ctc\_and\_gross().
  - Set total\_ctc from flt(assignment.ctc).
- Set assignment.base from base.
- Set frequency from Platform.get\_cached\_value(“Salary Structure”, offer.salary\_structure, “payroll\_frequency”).
- Set periods from PERIODS\_PER\_YEAR.get(frequency, 12).
- Return mapping(“base” → base, “ctc” → total\_ctc, “gross” → (flt(assignment.annual\_gross\_earning) ÷ periods), “components” → get\_breakup\_rows(assignment, periods, total\_ctc), …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Structure”, offer.salary\_structure, “payroll\_frequency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L65) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L116) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L116)

<a id="op-6f258dcf95a88f"></a>
### Resolve base for target

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_resolve_base_for_target`

**Inputs** assignment, base, target\_ctc.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(base, flt(assignment.ctc)) · solve\_base\_for\_ctc(assignment, target\_ctc).

**Local steps**

- Bind dependencies CTC\_SOLVER\_TOLERANCE, solve\_base\_for\_ctc.
- If base.
  - Set assignment.base from base.
  - Evaluate assignment.calculate\_ctc\_and\_gross().
  - If abs((flt(assignment.ctc) − target\_ctc)) ≤ CTC\_SOLVER\_TOLERANCE.
    - Return tuple(base, flt(assignment.ctc)).
- Return solve\_base\_for\_ctc(assignment, target\_ctc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L82) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L133) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L133)

<a id="op-c37ac57703cd99"></a>
### Get compensation details

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_compensation_details`

**Inputs** offer.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from offer via get\_doc.

**Explicit results** compute\_compensation(Platform.get\_doc(offer)).

**Local steps**

- Evaluate Platform.has\_permission(“Job Offer”, throw = true).
- Set offer from Platform.parse\_json(offer).
- Set offer at “doctype” from “Job Offer”.
- If offer.get(“salary\_structure”).
  - Evaluate Platform.has\_permission(“Salary Structure”, doc = offer at “salary\_structure”, throw = true).
- Return compute\_compensation(Platform.get\_doc(offer)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Offer”, throw = true), Platform.has\_permission(“Salary Structure”, doc = offer at “salary\_structure”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L70) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L121) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L121)

<a id="op-14891000026706"></a>
### Get offer acceptance rate

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_get_offer_acceptance_rate`

**Inputs** company = no value, department = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Job Offer” via count.

**Explicit results** mapping(“value” → ((flt(total\_accepted) ÷ flt(total\_offers)) × 100) when total\_offers, otherwise 0, “fieldtype” → “Percent”).

**Local steps**

- Evaluate Platform.has\_permission(“Job Offer”, throw = true).
- Set filters from mapping(“docstatus” → 1).
- If company.
  - Set filters at “company” from company.
- If department.
  - Set filters at “department” from department.
- Set total\_offers from Platform.db.count(“Job Offer”, filters = filters).
- Set filters at “status” from “Accepted”.
- Set total\_accepted from Platform.db.count(“Job Offer”, filters = filters).
- Return mapping(“value” → ((flt(total\_accepted) ÷ flt(total\_offers)) × 100) when total\_offers, otherwise 0, “fieldtype” → “Percent”).
  - Value choice on total\_offers — true gives ((flt(total\_accepted) ÷ flt(total\_offers)) × 100), false gives 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Offer”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L1059) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L923) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L903)
