# Payroll and benefits · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary slip

[Record definition](../../../../data/record-types/salary_slip.json)

<a id="op-0bdc1824e63688"></a>
### Unlink ref doc from salary slip

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_unlink_reference_record_from_salary_slip`

**Inputs** doc, method = no value.

**Record and data access** read “Salary Slip” via get\_all · resolve a document from “Salary Slip” via get\_doc.

**State and service calls** request set\_value on “Salary Slip”.

**Local steps**

- Set linked\_ss from Platform.get\_all(“Salary Slip”, filters = mapping(“journal\_entry” → doc.name, “docstatus” → list(“&lt;”, 2)), pluck = “name”).
- If linked\_ss.
  - For each ss in linked\_ss.
    - Set ss\_doc from Platform.get\_doc(“Salary Slip”, ss).
    - Evaluate Platform.db.set\_value(“Salary Slip”, ss\_doc.name, “journal\_entry”, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L5542) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L738) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1085)

<a id="op-c3f9bf35c2d23c"></a>
### System Formatted Date.str

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_system_formatted_date_text`

**Inputs** self.

**Explicit results** formatdate(datetime.date(self.year, self.month, self.day)).

**Local steps**

- Return formatdate(datetime.date(self.year, self.month, self.day)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L5810) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L736) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1083)

<a id="op-15581155ddfe48"></a>
### System Formatted Datetime.str

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_system_formatted_datetime_text`

**Inputs** self.

**Explicit results** format\_datetime(datetime.datetime(self.year, self.month, self.day, self.hour, …)).

**Local steps**

- Return format\_datetime(datetime.datetime(self.year, self.month, self.day, self.hour, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L5896) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L737) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1084)

<a id="op-efc6da5f3cdd9c"></a>
### Format dates in system format

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_format_dates_in_system_format`

**Inputs** value.

**Explicit results** SystemFormattedDatetime(value.year, value.month, value.day, value.hour, …) · SystemFormattedDate(value.year, value.month, value.day) · value.

**Local steps**

- If isinstance(value, datetime.datetime).
  - Return SystemFormattedDatetime(value.year, value.month, value.day, value.hour, …).
- If isinstance(value, datetime.date).
  - Return SystemFormattedDate(value.year, value.month, value.day).
- Return value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L6017) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L618) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L965)

<a id="op-b9279ddc148a0b"></a>
### Generate password for pdf

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_generate_password_for_portable_document`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** policy\_template, employee.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L6224) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L619) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L966)

<a id="op-48197b14c5ee1e"></a>
### Get salary component data

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_get_salary_component_data`

**Inputs** component.

**Record and data access** read “Salary Component” via get\_value.

**Explicit results** Platform.db.get\_value(“Salary Component”, component, tuple(“name as salary\_component”, “depends\_on\_payment\_days”, “salary\_component\_abbr as abbr”, “do\_not\_include\_in\_total”, …), as\_dict = 1, cache = true).

**Local steps**

- Return Platform.db.get\_value(“Salary Component”, component, tuple(“name as salary\_component”, “depends\_on\_payment\_days”, “salary\_component\_abbr as abbr”, “do\_not\_include\_in\_total”, …), as\_dict = 1, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L6408) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L623) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L970)

<a id="op-8c1a821fa223ea"></a>
### Get payroll payable account

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_get_payroll_payable_account`

**Inputs** company, payroll\_entry.

**Record and data access** read “Payroll Entry” via get\_value · read “Company” via get\_value.

**Explicit results** payroll\_payable\_account.

**Local steps**

- If payroll\_entry.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Payroll Entry”, payroll\_entry, “payroll\_payable\_account”, cache = true).
- Otherwise.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Company”, company, “default\_payroll\_payable\_account”, cache = true).
- Return payroll\_payable\_account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L6579) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L622) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L969)

<a id="op-985e9b133ae3d4"></a>
### Get lwp or ppl for date range

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_get_leave_without_pay_or_partially_paid_leave_for_date_range`

**Inputs** employee, start\_date, end\_date.

**Explicit results** leave\_date\_mapper.

**Local steps**

- Set LeaveApplication from Platform.qb.DocType(“Leave Application”).
- Set LeaveType from Platform.qb.DocType(“Leave Type”).
- Set leaves from nested operand in the contract(nested operand in the contract).select(LeaveApplication.name, LeaveType.is\_ppl, LeaveType.fraction\_of\_daily\_salary\_per\_leave, LeaveType.include\_holiday, …).where(((((nested o ….
- Set leave\_date\_mapper from Platform.\_dict().
- For each leave in leaves.
  - If leave.from\_date equals leave.to\_date.
    - Set leave\_date\_mapper at leave.from\_date from leave.
  - Otherwise.
    - Set date\_diff from (getdate(leave.to\_date) − getdate(leave.from\_date)).days.
    - For each i in range((date\_diff + 1)).
      - Set date from add\_days(leave.from\_date, i).
      - Set leave\_date\_mapper at date from leave.
- Return leave\_date\_mapper.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L621) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L968)

<a id="op-71d903b9727950"></a>
### Make salary slip from timesheet

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_make_salary_slip_from_timesheet`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** read “Salary Structure” via get\_cached\_value.

**State and service calls** request new\_doc for “Salary Slip”.

**Explicit results** target.

**Explicit failure paths** validation helper — translated “Cannot create Salary Slip: no active Salary Structure is assigned to employee {0}.”.format(Platform.bold(target.employee\_name)) · validation helper — translated “The Assigned Salary Structure {0} for the employee {1} is not configured for Salary Slip based on Timesheet.”.format(Platform.bold(target.salary\_structure), Platform.bold(target.employee\_name)) · validation helper — translated “The Assigned Salary Structure {0} for the employee {1} does not have a Salary Component configured for Salar …”.format(Platform.bold(target.salary\_structure), Platform.bold(target.employee\_name)).

**Local steps**

- Evaluate Platform.has\_permission(“Timesheet”, “read”, source\_name, throw = true).
- Set target from Platform.new\_doc(“Salary Slip”).
- Evaluate set\_missing\_values(source\_name, target).
- If not target.check\_sal\_struct().
  - Call the validation error handler Platform.throw(translated “Cannot create Salary Slip: no active Salary Structure is assigned to employee {0}.”.format(Platform.bold(target.employee\_name))).
- Set timesheet\_config from Platform.get\_cached\_value(“Salary Structure”, target.salary\_structure, list(“salary\_slip\_based\_on\_timesheet”, “salary\_component”), as\_dict = true).
- If (not timesheet\_config or not timesheet\_config.salary\_slip\_based\_on\_timesheet).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not timesheet\_config → not timesheet\_config.salary\_slip\_based\_on\_timesheet.
  - Call the validation error handler Platform.throw(translated “The Assigned Salary Structure {0} for the employee {1} is not configured for Salary Slip based on Timesheet.”.format(Platform.bold(target.salary\_structure), Platform.bold(target. ….
- If not timesheet\_config.salary\_component.
  - Call the validation error handler Platform.throw(translated “The Assigned Salary Structure {0} for the employee {1} does not have a Salary Component configured for Salar …”.format(Platform.bold(target.salary\_structure), Platform.bold(targe ….
- Evaluate target.run\_method(“get\_emp\_and\_working\_day\_details”).
- Return target.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Timesheet”, “read”, source\_name, throw = true) · configured or stored value from Platform.get\_cached\_value(“Salary Structure”, target.salary\_structure, list(“salary\_slip\_based\_on\_timesheet”, “salary\_component”), as\_dict = true) · selected callable from target.run\_method(“get\_emp\_and\_working\_day\_details”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L791) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L624) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L971)

<a id="op-3397d4c6040659"></a>
### Set missing values

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_set_missing_values`

**Inputs** time\_sheet, target.

**Record and data access** resolve a document from “Timesheet” via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(“Timesheet”, time\_sheet).
- Set target.employee from doc.employee.
- Set target.employee\_name from doc.employee\_name.
- Set target.salary\_slip\_based\_on\_timesheet from 1.
- Set target.start\_date from doc.start\_date.
- Set target.end\_date from doc.end\_date.
- Set target.posting\_date from doc.modified.
- Set target.total\_working\_hours from doc.total\_hours.
- Evaluate target.append(“timesheets”, mapping(“time\_sheet” → doc.name, “working\_hours” → doc.total\_hours)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L1447) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L735) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1082)

<a id="op-dbbb3e51ae5473"></a>
### Verify lwp days corrected

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_verify_leave_without_pay_days_corrected`

**Inputs** employee, start\_date, end\_date, lwp\_days\_corrected.

**Explicit results** true.

**Explicit failure paths** validation helper — translated “LWP Days Reversed ({0}) does not match actual Payroll Corrections total ({1}) for employee {2} from {3} to {4}”.format(lwp\_days\_corrected, actual\_total, employee, start\_date, …).

**Local steps**

- Set PayrollCorrection from Platform.qb.DocType(“Payroll Correction”).
- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set actual\_days\_reversed from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“total\_days”)).where((((nested operand in the contract equals nested operand in the contract bitwise ….
- Set actual\_total from (actual\_days\_reversed at 0 or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in actual\_days\_reversed at 0 → 0.0.
- If lwp\_days\_corrected differs from actual\_total.
  - Call the validation error handler Platform.throw(translated “LWP Days Reversed ({0}) does not match actual Payroll Corrections total ({1}) for employee {2} from {3} to {4}”.format(lwp\_days\_corrected, actual\_total, employee, start\_date, …), ….
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L1743) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L739) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1086)

<a id="op-a2dfc40a998001"></a>
### On doctype update

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Salary Slip”.

**Local steps**

- Evaluate Platform.db.add\_index(“Salary Slip”, list(“employee”, “start\_date”, “end\_date”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L2285) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L625) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L972)

<a id="op-db811d33033db6"></a>
### Enqueue email salary slips

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_enqueue_email_salary_slips`

**Inputs** names.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** enqueue with “Workforce.payroll.doctype.salary\_slip.salary\_slip.email\_salary\_slips” · msgprint with translated “Salary slip emails have been enqueued for sending. Check {0} for status.”.format(formatted text &lt;a href='{Platform.utils.get\_url\_to\_list(“Email Queue”)}' target='blank'&gt;Email Queue&lt;/a&gt;).

**Local steps**

- Bind dependencies json.
- If isinstance(names, str).
  - Set names from json.loads(names).
- For each name in names.
  - Evaluate Platform.has\_permission(“Salary Slip”, “read”, name, throw = true).
- Evaluate Platform.enqueue(“Workforce.payroll.doctype.salary\_slip.salary\_slip.email\_salary\_slips”, names = names).
- Evaluate Platform.msgprint(translated “Salary slip emails have been enqueued for sending. Check {0} for status.”.format(formatted text &lt;a href='{Platform.utils.get\_url\_to\_list(“Email Queue”)}' target='blank'&gt;Email  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Salary Slip”, “read”, name, throw = true) · service or queued work from Platform.enqueue(“Workforce.payroll.doctype.salary\_slip.salary\_slip.email\_salary\_slips”, names = names).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L2372) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L617) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L964)

<a id="op-45739d9493014f"></a>
### Email salary slips

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_email_salary_slips`

**Inputs** names.

**Declared result** no value.

**Record and data access** resolve a document from “Salary Slip” via get\_doc.

**Local steps**

- For each name in names.
  - Set salary\_slip from Platform.get\_doc(“Salary Slip”, name).
  - Evaluate salary\_slip.email\_salary\_slip().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L2783) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L616) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L963)

<a id="op-5a566fe996b8f8"></a>
### If lending app installed

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_if_lending_application_installed`

**Inputs** function.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L2885) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L743) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1090)

<a id="op-a61a27ecaed21e"></a>
### If lending app installed.wrapper

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_if_lending_application_installed_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** function(expanded args, expanded names kwargs) · no value.

**Local steps**

- If “lending” belongs to Platform.get\_installed\_apps().
  - Return function(expanded args, expanded names kwargs).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L3013) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L744) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1091)

<a id="op-76a29db2d9d90c"></a>
### Set loan repayment

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_set_loan_repayment`

**Inputs** doc.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Explicit failure paths** validation helper — translated “Row {0}: Paid amount {1} is greater than pending accrued amount {2} against loan {3}”.format(payment.idx, Platform.bold(payment.total\_payment), Platform.bold(total\_amount), Platform.bold(payment.loan)).

**Local steps**

- Bind dependencies calculate\_amounts.
- Set doc.total\_loan\_repayment from 0.
- Set doc.total\_interest\_amount from 0.
- Set doc.total\_principal\_amount from 0.
- If not doc.get(“loans”, list()).
  - Set loan\_details from \_get\_loan\_details(doc).
  - For each loan in loan\_details.
    - Set amounts from calculate\_amounts(loan.name, doc.end\_date).
    - If amounts at “payable\_amount”.
      - Evaluate doc.append(“loans”, mapping(“loan” → loan.name, “total\_payment” → amounts at “payable\_amount”, “interest\_amount” → amounts at “interest\_amount”, “principal\_amount” → amounts at “payable\_principal\_amount”, …)).
- If not doc.get(“loans”).
  - Evaluate doc.set(“loans”, list()).
- For each payment in doc.get(“loans”, list()).
  - Set amounts from calculate\_amounts(payment.loan, doc.end\_date).
  - Set total\_amount from amounts at “payable\_amount”.
  - If payment.total\_payment &gt; total\_amount.
    - Call the validation error handler Platform.throw(translated “Row {0}: Paid amount {1} is greater than pending accrued amount {2} against loan {3}”.format(payment.idx, Platform.bold(payment.total\_payment), Platform.bold(total\_amount), Platf ….
  - Update doc.total\_interest\_amount using + payment.interest\_amount.
  - Update doc.total\_principal\_amount using + payment.principal\_amount.
  - Update doc.total\_loan\_repayment using + payment.total\_payment.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L3117) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L747) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1094)

<a id="op-4a70f6844a4298"></a>
### Get loan details

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_get_loan_details`

**Inputs** doc.

**Declared result** dict at tuple(str, Any).

**Record and data access** read “Loan” via get\_all.

**Explicit results** loan\_details.

**Local steps**

- Set loan\_details from Platform.get\_all(“Loan”, fields = list(“name”, “interest\_income\_account”, “loan\_account”, “loan\_product”, …), filters = mapping(“applicant” → doc.employee, “docstatus” → 1, “repay\_from\_salary” → 1, “compan ….
- Return loan\_details.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L3884) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L741) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1088)

<a id="op-8814f7eb5bf73c"></a>
### Process loan interest accrual and demand

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_process_loan_interest_accrual_and_demand`

**Inputs** doc.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Record and data access** read “DocType” via exists.

**Explicit results** no value.

**Local steps**

- Set loans from \_get\_loan\_details(doc).
- If not loans.
  - Return no value.
- Set loan\_demand\_exists from Platform.db.exists(“DocType”, “Loan Demand”).
- If loan\_demand\_exists.
  - Bind dependencies process\_daily\_loan\_demands.
  - Bind dependencies process\_loan\_interest\_accrual\_for\_loans.
- Otherwise.
  - Bind dependencies process\_loan\_interest\_accrual\_for\_term\_loans.
- For each loan in loans.
  - If loan.get(“is\_term\_loan”).
    - If loan\_demand\_exists.
      - Evaluate process\_loan\_interest\_accrual\_for\_loans(doc.end\_date, loan.loan\_product, loan.name).
      - Evaluate process\_daily\_loan\_demands(doc.end\_date, loan.loan\_product, loan.name).
    - Otherwise.
      - Evaluate process\_loan\_interest\_accrual\_for\_term\_loans(posting\_date = doc.end\_date, loan\_product = loan.loan\_product, loan = loan.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L4126) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L746) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1093)

<a id="op-cf9f951f5010ea"></a>
### Make loan repayment entry

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_make_loan_repayment_entry`

**Inputs** doc.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**State and service calls** call save on repayment\_entry · call submit on repayment\_entry · request set\_value on “Salary Slip Loan”.

**Local steps**

- Bind dependencies create\_repayment\_entry.
- Set payroll\_payable\_account from get\_payroll\_payable\_account(doc.company, doc.payroll\_entry).
- Set process\_payroll\_accounting\_entry\_based\_on\_employee from Platform.db.get\_single\_value(“Payroll Settings”, “process\_payroll\_accounting\_entry\_based\_on\_employee”).
- If not doc.get(“loans”).
  - Evaluate doc.set(“loans”, list()).
- For each loan in doc.get(“loans”, list()).
  - If not loan.total\_payment.
    - Continue with the next iteration or loop test.
  - Set repayment\_entry from create\_repayment\_entry(loan.loan, doc.employee, doc.company, doc.posting\_date, payroll\_payable\_account = payroll\_payable\_account, process\_payroll\_accounting\_entry\_based\_on\_employee = process\_payroll\_accoun ….
  - Evaluate repayment\_entry.save().
  - If not process\_payroll\_accounting\_entry\_based\_on\_employee.
    - Set Platform.flags.party\_not\_required from true.
  - Evaluate repayment\_entry.submit().
  - Set Platform.flags.party\_not\_required from false.
  - Evaluate Platform.db.set\_value(“Salary Slip Loan”, loan.name, “loan\_repayment\_entry”, repayment\_entry.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “process\_payroll\_accounting\_entry\_based\_on\_employee”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L4491) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L745) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1092)

<a id="op-5e50981b07c631"></a>
### Cancel loan repayment entry

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_cancel_loan_repayment_entry`

**Inputs** doc.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Record and data access** resolve a document from “Loan Repayment” via get\_doc.

**State and service calls** call cancel on repayment\_entry.

**Local steps**

- If not doc.get(“loans”).
  - Evaluate doc.set(“loans”, list()).
- For each loan in doc.get(“loans”, list()).
  - If loan.loan\_repayment\_entry.
    - Set repayment\_entry from Platform.get\_doc(“Loan Repayment”, loan.loan\_repayment\_entry).
    - Evaluate repayment\_entry.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L5018) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L740) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1087)

<a id="op-a7230250af22ef"></a>
### Get payroll payable account

`operation_workforce_payroll_record_definitions_salary_slip_salary_slip_loan_utils_business_behavior_get_payroll_payable_account`

**Inputs** company, payroll\_entry.

**Record and data access** read “Payroll Entry” via get\_value · read “Company” via get\_value.

**Explicit results** payroll\_payable\_account.

**Local steps**

- If payroll\_entry.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Payroll Entry”, payroll\_entry, “payroll\_payable\_account”).
- Otherwise.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Company”, company, “default\_payroll\_payable\_account”).
- Return payroll\_payable\_account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0129.json#L5222) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L742) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1089)

## Record · Salary structure

[Record definition](../../../../data/record-types/salary_structure.json)

<a id="op-95ec801cf72160"></a>
### Salary Structure.before validate

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.sanitize\_condition\_and\_formula\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sanitize condition and formula fields](operations-019.md#op-8108baa607c6bc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L1531) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L886) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1233)

<a id="op-4c2c48ea8fd5f9"></a>
### Salary Structure.before update after submit

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.sanitize\_condition\_and\_formula\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sanitize condition and formula fields](operations-019.md#op-8108baa607c6bc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L1582) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L885) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1232)
