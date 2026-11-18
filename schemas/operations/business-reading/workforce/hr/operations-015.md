# Employment and attendance · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Exit interview

[Record definition](../../../../data/record-types/exit_interview.json)

<a id="op-ef0a6bdc8a0882"></a>
### Send exit questionnaire

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_send_exit_questionnaire`

**Inputs** interviews.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Exit Interview” via get\_doc · resolve a document from “Employee” via get\_doc · read “HR Settings” via get\_single\_value · resolve a document from “Email Template” via get\_doc.

**State and service calls** sendmail · call db\_set on interview.

**Local steps**

- Set interviews from get\_interviews(interviews).
- For each exit\_interview in interviews.
  - Evaluate Platform.has\_permission(“Exit Interview”, ptype = “write”, doc = exit\_interview.get(“name”), throw = true).
- Evaluate validate\_questionnaire\_settings().
- Set email\_success from list().
- Set email\_failure from list().
- For each exit\_interview in interviews.
  - Set interview from Platform.get\_doc(“Exit Interview”, exit\_interview.get(“name”)).
  - If interview.get(“questionnaire\_email\_sent”).
    - Continue with the next iteration or loop test.
  - Set employee from Platform.get\_doc(“Employee”, interview.employee).
  - Set email from get\_employee\_email(employee).
  - Set context from interview.as\_dict().
  - Evaluate context.update(employee.as\_dict()).
  - Set template\_name from Platform.db.get\_single\_value(“HR Settings”, “exit\_questionnaire\_notification\_template”).
  - Set template from Platform.get\_doc(“Email Template”, template\_name).
  - If email.
    - Evaluate Platform.sendmail(recipients = email, subject = template.subject, message = Platform.render\_template(template.response, context), reference\_doctype = interview.doctype, …).
    - Evaluate interview.db\_set(“questionnaire\_email\_sent”, 1).
    - Evaluate interview.notify\_update().
    - Evaluate email\_success.append(email).
  - Otherwise.
    - Evaluate email\_failure.append(get\_link\_to\_form(“Employee”, employee.name)).
- Evaluate show\_email\_summary(email\_success, email\_failure).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Exit Interview”, ptype = “write”, doc = exit\_interview.get(“name”), throw = true) · configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “exit\_questionnaire\_notification\_template”) · service or queued work from Platform.sendmail(recipients = email, subject = template.subject, message = Platform.render\_template(template.response, context), reference\_doctype = interview.doctype, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L20) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L679) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L659)

<a id="op-a60656fa7968ca"></a>
### Get interviews

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_get_interviews`

**Inputs** interviews.

**Explicit results** interviews.

**Explicit failure paths** validation helper — translated “At least one interview has to be selected.”.

**Local steps**

- Bind dependencies json.
- If isinstance(interviews, str).
  - Set interviews from json.loads(interviews).
- If not len(interviews).
  - Call the validation error handler Platform.throw(translated “At least one interview has to be selected.”).
- Return interviews.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L3304) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L678) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L658)

<a id="op-755bc846195be6"></a>
### Validate questionnaire settings

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_validate_questionnaire_settings`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_value.

**Explicit failure paths** validation helper — translated “Please set {0} and {1} in {2}.”.format(Platform.bold(translated “Exit Questionnaire Web Form”), Platform.bold(translated “Notification Template”), get\_link\_to\_form(“HR Settings”, “HR Settings”)).

**Local steps**

- Set settings from Platform.db.get\_value(“HR Settings”, “HR Settings”, list(“exit\_questionnaire\_web\_form”, “exit\_questionnaire\_notification\_template”), as\_dict = true).
- If (not settings.exit\_questionnaire\_web\_form or not settings.exit\_questionnaire\_notification\_template).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not settings.exit\_questionnaire\_web\_form → not settings.exit\_questionnaire\_notification\_template.
  - Call the validation error handler Platform.throw(translated “Please set {0} and {1} in {2}.”.format(Platform.bold(translated “Exit Questionnaire Web Form”), Platform.bold(translated “Notification Template”), get\_link\_to\_form(“HR Settings”, ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L3473) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L681) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L661)

<a id="op-a7988d94330006"></a>
### Show email summary

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_show_email_summary`

**Inputs** email\_success, email\_failure.

**State and service calls** msgprint with message.

**Local steps**

- Set message from empty text.
- If email\_success.
  - Update message using + translated “Sent Successfully: {0}”.format(“, ”.join(email\_success)).
- If (message and email\_failure).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in message → email\_failure.
  - Update message using + text in the contract.
- If email\_failure.
  - Update message using + translated “Sending Failed due to missing email information for employee(s): {1}”.format(“, ”.join(email\_failure)).
- Evaluate Platform.msgprint(message, title = translated “Exit Questionnaire”, indicator = “blue”, is\_minimizable = true, wide = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L3789) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L680) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L660)

## Service · Exit interview scheduled

<a id="op-1f1af687a97882"></a>
### Get context

`operation_workforce_human_resources_notification_exit_interview_scheduled_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1954) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L303) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L303)

## Record · Expense claim

[Record definition](../../../../data/record-types/expense_claim.json)

<a id="op-0943b657a0597e"></a>
### Expense Claim.onload

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_onload`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Local steps**

- Evaluate self.set\_onload(“self\_expense\_approval\_not\_allowed”, Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_expense\_approval”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_expense\_approval”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L6358) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L704) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L684)

<a id="op-9bf344dcc87aed"></a>
### Expense Claim.after insert

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.notify\_approver().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L6450) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L691) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L671)

<a id="op-fbd203d0473587"></a>
### Expense Claim.validate

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_validate`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_employee\_scope().
- Evaluate set\_employee\_name(self).
- Evaluate self.set\_company\_currency\_if\_multi\_currency\_disabled().
- Evaluate self.validate\_sanctioned\_amount().
- Evaluate self.calculate\_total\_amount().
- Evaluate self.validate\_advances().
- Evaluate self.set\_expense\_account(validate = true).
- Evaluate self.set\_default\_accounting\_dimension().
- Evaluate self.calculate\_taxes().
- Evaluate self.set\_status().
- Evaluate self.validate\_company\_and\_department().
- If (self.task and not self.project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.task → not self.project.
  - Set self.project from Platform.db.get\_value(“Task”, self.task, “project”).
- If (flt(self.grand\_total) &gt; 0 and self.total\_advance\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.grand\_total) &gt; 0 → self.total\_advance\_amount.
  - Set self.is\_paid from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate employee scope](operations-015.md#op-815dad16d2e5d0), [set company currency if multi currency disabled](operations-016.md#op-f57aae3813a761), [validate sanctioned amount](operations-016.md#op-b4b05bbea02d5d), [calculate total amount](operations-016.md#op-b2f7843b631e96), [validate advances](operations-016.md#op-9fe56a156c3569), [set expense account](operations-016.md#op-163bc2cec64851), [set default accounting dimension](operations-016.md#op-26b98990fb58ed), [calculate taxes](operations-016.md#op-1da6ab118df7b2), [set status](operations-015.md#op-220573ab77fd7b), [validate company and department](operations-015.md#op-d6985948861b27).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L21) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L713) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L693)

<a id="op-220573ab77fd7b"></a>
### Expense Claim.set status

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_set_status`

**Inputs** self, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set status from mapping(“0” → “Draft”, “1” → “Submitted”, “2” → “Cancelled”) at cstr((self.docstatus or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus → 0.
- Set precision from self.precision(“grand\_total”).
- If self.docstatus equals 1.
  - If self.approval\_status equals “Approved”.
    - If (self.is\_paid or (flt(self.total\_sanctioned\_amount) &gt; 0 and (flt(self.grand\_total, precision) equals flt(self.total\_amount\_reimbursed, precision) or flt(self.grand\_total, precision) equals 0))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_paid → (flt(self.total\_sanctioned\_amount) &gt; 0 and (flt(self.grand\_total, precision) equals flt(self.total\_amount\_reimbursed, precision) or flt(self.grand\_total, precision) equals 0)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.total\_sanctioned\_amount) &gt; 0 → (flt(self.grand\_total, precision) equals flt(self.total\_amount\_reimbursed, precision) or flt(self.grand\_total, precision) equals 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.grand\_total, precision) equals flt(self.total\_amount\_reimbursed, precision) → flt(self.grand\_total, precision) equals 0.
      - Set status from “Paid”.
    - Otherwise.
      - If flt(self.total\_sanctioned\_amount) &gt; 0.
        - If flt(self.total\_amount\_reimbursed, precision) &gt; 0.
          - Set status from “Partially Paid”.
        - Otherwise.
          - Set status from “Unpaid”.
  - Otherwise.
    - If self.approval\_status equals “Rejected”.
      - Set status from “Rejected”.
- If update.
  - Evaluate self.db\_set(“status”, status).
  - Evaluate self.publish\_update().
  - Evaluate self.notify\_update().
- Otherwise.
  - Set self.status from status.

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-015.md#op-1c977e17320607).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L710) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L690)

<a id="op-815dad16d2e5d0"></a>
### Expense Claim.validate employee scope

`operation_workforce_binding_workforce_hr_doctype_expense_claim_expense_claim_expenseclaim_validate_employee_scope`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with MismatchError — translated “Employee {0} does not belong to company: {1}”.format(self.employee, self.company) · validation helper with Platform.PermissionError — translated “You are not allowed to create or modify an Expense Claim for Employee {0}”.format(self.employee).

**Local steps**

- If not self.employee.
  - Return no value.
- Set tuple(employee\_company, employee\_user) from Platform.db.get\_value(“Employee”, self.employee, list(“company”, “user\_id”)).
- If not self.company.
  - Set self.company from employee\_company.
- Otherwise.
  - If self.company differs from employee\_company.
    - Call the validation error handler Platform.throw(translated “Employee {0} does not belong to company: {1}”.format(self.employee, self.company), exc = MismatchError).
- If self.flags.ignore\_permissions.
  - Return no value.
- If (employee\_user differs from Platform.session.user and not self.can\_claim\_for\_others()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee\_user differs from Platform.session.user → not self.can\_claim\_for\_others().
  - Call the validation error handler Platform.throw(translated “You are not allowed to create or modify an Expense Claim for Employee {0}”.format(self.employee), Platform.PermissionError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can claim for others](operations-015.md#op-24824090316474).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L58) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L109) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L109)

<a id="op-24824090316474"></a>
### Expense Claim.can claim for others

`operation_workforce_binding_workforce_hr_doctype_expense_claim_expense_claim_expenseclaim_can_claim_for_others`

**Inputs** self.

**Explicit results** bool(((roles\_with\_write − SELF\_SERVICE\_ROLES) bitwise and set(Platform.get\_roles()))).

**Local steps**

- Set roles\_with\_write from set of perm.role for perm drawn from Platform.get\_meta(self.doctype).permissions where (perm.write and not perm.permlevel).
  - Draw perm from Platform.get\_meta(self.doctype).permissions, keep a combination only if ((perm.write and not perm.permlevel)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.write → not perm.permlevel.
- Return bool(((roles\_with\_write − SELF\_SERVICE\_ROLES) bitwise and set(Platform.get\_roles()))).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L55) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L106) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L106)

<a id="op-d6985948861b27"></a>
### Expense Claim.validate company and department

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_validate_company_and_department`

**Inputs** self.

**Record and data access** read “Department” via get\_value.

**Explicit failure paths** validation helper with MismatchError — translated “Department {0} does not belong to company: {1}”.format(self.department, self.company).

**Local steps**

- If self.department.
  - Set company from Platform.db.get\_value(“Department”, self.department, “company”).
  - If (company and self.company differs from company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → self.company differs from company.
    - Call the validation error handler Platform.throw(translated “Department {0} does not belong to company: {1}”.format(self.department, self.company), exc = MismatchError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L627) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L716) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L696)

<a id="op-c94caa762886be"></a>
### Expense Claim.validate for self approval

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_validate_for_self_approval`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Self-approval for Expense Claims is not allowed”.

**Local steps**

- Set self\_expense\_approval\_not\_allowed from Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_expense\_approval”).
- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”).
- If (self\_expense\_approval\_not\_allowed and employee\_user equals Platform.session.user and not get\_workflow\_name(“Expense Claim”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self\_expense\_approval\_not\_allowed → employee\_user equals Platform.session.user → not get\_workflow\_name(“Expense Claim”).
  - Call the validation error handler Platform.throw(translated “Self-approval for Expense Claims is not allowed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_expense\_approval”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L842) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L717) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L697)

<a id="op-1b0b10f57eec90"></a>
### Expense Claim.on update

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_on_update`

**Inputs** self.

**Local steps**

- Evaluate share\_doc\_with\_approver(self, self.expense\_approver).
- Evaluate self.publish\_update().
- Evaluate self.notify\_approval\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-015.md#op-1c977e17320607).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1082) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L702) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L682)

<a id="op-113bff950bc054"></a>
### Expense Claim.after delete

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-015.md#op-1c977e17320607).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1181) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L690) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L670)

<a id="op-345164912a722d"></a>
### Expense Claim.on discard

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.db\_set(“approval\_status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1232) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L700) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L680)

<a id="op-af3326f085098d"></a>
### Expense Claim.before submit

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_for\_self\_approval().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for self approval](operations-015.md#op-c94caa762886be).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1326) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L692) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L672)

<a id="op-1c977e17320607"></a>
### Expense Claim.publish update

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Workforce.refetch\_resource(“Workforce:my\_claims”, employee\_user).
- Evaluate Workforce.refetch\_resource(“Workforce:team\_claims”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1377) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L705) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L685)

<a id="op-e67f9cd693b60d"></a>
### Expense Claim.on submit

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Approval Status must be 'Approved' or 'Rejected'”.

**Local steps**

- <a id="op-e67f9cd693b60d-guard-2"></a>If self.approval\_status equals “Draft”.
  - Call the validation error handler Platform.throw(translated “Approval Status must be 'Approved' or 'Rejected'”).
- Evaluate self.update\_task\_and\_project().
- Evaluate self.make\_gl\_entries().
- Evaluate update\_reimbursed\_amount(self).
- Evaluate self.update\_claimed\_amount\_in\_employee\_advance().
- Evaluate self.create\_exchange\_gain\_loss\_je().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.approval\_status equals “Draft”, self.approval\_status = “Draft” selects the branch that calls the validation-error handler with translated “Approval Status must be 'Approved' or 'Rejected'”. With self.approval\_status = “Approved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e67f9cd693b60d-guard-2)

**Methods declared on this owner** [update task and project](operations-015.md#op-1c119a8a58c275), [make gl entries](operations-016.md#op-47869cd80267a5), [update claimed amount in employee advance](operations-015.md#op-e15fe109f4446e), [create exchange gain loss je](operations-016.md#op-835248af996e8b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1527) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L701) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L681)

<a id="op-0ee1005729ccb6"></a>
### Expense Claim.on update after submit

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_on_update_after_submit`

**Inputs** self.

**Local steps**

- If self.check\_if\_fields\_updated(list(), mapping(“taxes” → tuple(“account\_head”), “expenses” → tuple())).
  - Evaluate validate\_docs\_for\_voucher\_types(list(“Expense Claim”)).
  - Evaluate self.repost\_accounting\_entries().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1724) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L703) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L683)

<a id="op-1930b32e4322dd"></a>
### Expense Claim.on cancel

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_task\_and\_project().
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Payment Ledger Entry”, “Advance Payment Ledger Entry”).
- If self.payable\_account.
  - Evaluate self.make\_gl\_entries(cancel = true).
- Evaluate update\_reimbursed\_amount(self).
- Evaluate self.update\_claimed\_amount\_in\_employee\_advance().
- Evaluate self.publish\_update().
- Evaluate unlink\_ref\_doc\_from\_payment\_entries(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update task and project](operations-015.md#op-1c119a8a58c275), [make gl entries](operations-016.md#op-47869cd80267a5), [update claimed amount in employee advance](operations-015.md#op-e15fe109f4446e), [publish update](operations-015.md#op-1c977e17320607).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L1878) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L699) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L679)

<a id="op-e15fe109f4446e"></a>
### Expense Claim.update claimed amount in employee advance

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_update_claimed_amount_in_employee_advance`

**Inputs** self.

**Record and data access** resolve a document from “Employee Advance” via get\_doc.

**Local steps**

- For each d in self.get(“advances”).
  - Evaluate Platform.get\_doc(“Employee Advance”, d.employee\_advance).update\_claimed\_amount().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L2110) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L711) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L691)

<a id="op-1c119a8a58c275"></a>
### Expense Claim.update task and project

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_update_task_and_project`

**Inputs** self.

**Record and data access** resolve a document from “Task” via get\_doc · resolve a document from “Project” via get\_doc.

**State and service calls** call save on task.

**Local steps**

- If self.task.
  - Set task from Platform.get\_doc(“Task”, self.task).
  - Set ExpenseClaim from Platform.qb.DocType(“Expense Claim”).
  - Set task.total\_expense\_claim from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0.
  - Evaluate task.save().
- For each project in self.get\_linked\_projects().
  - Evaluate Platform.get\_doc(“Project”, project).update\_project().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked projects](operations-015.md#op-e3be1f8881e807).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L2224) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L712) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L692)

<a id="op-e3be1f8881e807"></a>
### Expense Claim.get linked projects

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_get_linked_projects`

**Inputs** self.

**Explicit results** projects.

**Local steps**

- Set projects from set().
- If self.project.
  - Evaluate projects.add(self.project).
- Evaluate projects.update(generator of expense.project for expense drawn from self.expenses where expense.project).
  - Draw expense from self.expenses, keep a combination only if (expense.project).
- Return projects.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L2620) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L697) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L677)
