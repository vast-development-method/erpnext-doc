# Employment and attendance · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank details change request

<a id="op-ec088aacbc1f40"></a>
### Bank Details Change Request.update employee

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_update_employee`

**Inputs** self.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on employee.

**Local steps**

- Set employee from Platform.get\_doc(“Employee”, self.employee).
- Set employee.salary\_mode from “Bank”.
- Set employee.bank\_name from self.bank\_name.
- Set employee.bank\_ac\_no from self.bank\_ac\_no.
- Set employee.iban from self.iban.
- If employee.meta.has\_field(“ifsc\_code”).
  - Set employee.ifsc\_code from self.ifsc\_code.
- Evaluate employee.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L48) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L99) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L99)

## Service · Bank details change request decided

<a id="op-5ef142f0425beb"></a>
### Get context

`operation_workforce_binding_workforce_hr_notification_bank_details_change_request_decided_bank_details_change_request_decided_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L88) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L139) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L139)

## Record · Compensatory leave request

[Record definition](../../../../data/record-types/compensatory_leave_request.json)

<a id="op-fd3a8d4dffc6ea"></a>
### Compensatory Leave Request.validate

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Half Day Date is mandatory” · validation helper — translated “Half Day Date should be in between Work From Date and Work End Date” · validation helper — translated “Leave Type is mandatory”.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate validate\_dates(self, self.work\_from\_date, self.work\_end\_date).
- If self.half\_day.
  - If not self.half\_day\_date.
    - Call the validation error handler Platform.throw(translated “Half Day Date is mandatory”).
  - If not getdate(self.work\_from\_date) ≤ getdate(self.half\_day\_date) ≤ getdate(self.work\_end\_date).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.work\_from\_date) ≤ getdate(self.half\_day\_date) ≤ getdate(self.work\_end\_date).
    - Call the validation error handler Platform.throw(translated “Half Day Date should be in between Work From Date and Work End Date”).
- Evaluate validate\_overlap(self, self.work\_from\_date, self.work\_end\_date).
- Evaluate self.validate\_holidays().
- Evaluate self.validate\_attendance().
- If not self.leave\_type.
  - Call the validation error handler Platform.throw(translated “Leave Type is mandatory”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate holidays](operations-006.md#op-82c557a6cf8af3), [validate attendance](operations-006.md#op-8a67f614f15222).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L2376) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L446) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L442)

<a id="op-8a67f614f15222"></a>
### Compensatory Leave Request.validate attendance

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_validate_attendance`

**Inputs** self.

**Record and data access** read “Attendance” via get\_all.

**Explicit failure paths** validation helper — translated “You were only present for Half Day on {}. Cannot apply for a full day compensatory leave”.format(“, ”.join(list of Platform.bold(format\_date(half\_day)) for half\_day drawn from half\_days)) · validation helper — translated “You are not present all day(s) between compensatory leave request days”.

**Local steps**

- Set attendance\_records from Platform.get\_all(“Attendance”, filters = list(list(“attendance\_date”, “between”, list(self.work\_from\_date, self.work\_end\_date)), list(“status”, “in”, list(“Present”, “Work From Home”, “Half Day”)), list(“d ….
- Set half\_days from list of entry.attendance\_date for entry drawn from attendance\_records where entry.status equals “Half Day”.
  - Draw entry from attendance\_records, keep a combination only if (entry.status equals “Half Day”).
- If (half\_days and (not self.half\_day or getdate(self.half\_day\_date) does not belong to half\_days)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in half\_days → (not self.half\_day or getdate(self.half\_day\_date) does not belong to half\_days).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.half\_day → getdate(self.half\_day\_date) does not belong to half\_days.
  - Call the validation error handler Platform.throw(translated “You were only present for Half Day on {}. Cannot apply for a full day compensatory leave”.format(“, ”.join(list of Platform.bold(format\_date(half\_day)) for half\_day drawn from half\_days))).
    - Draw half\_day from half\_days.
- If len(attendance\_records) &lt; (date\_diff(self.work\_end\_date, self.work\_from\_date) + 1).
  - Call the validation error handler Platform.throw(translated “You are not present all day(s) between compensatory leave request days”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L2794) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L447) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L443)

<a id="op-82c557a6cf8af3"></a>
### Compensatory Leave Request.validate holidays

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_validate_holidays`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set holidays from get\_holiday\_dates\_for\_employee(self.employee, self.work\_from\_date, self.work\_end\_date).
- If len(holidays) &lt; (date\_diff(self.work\_end\_date, self.work\_from\_date) + 1).
  - If date\_diff(self.work\_end\_date, self.work\_from\_date).
    - Set msg from translated “The days between {0} to {1} are not valid holidays.”.format(Platform.bold(format\_date(self.work\_from\_date)), Platform.bold(format\_date(self.work\_end\_date))).
  - Otherwise.
    - Set msg from translated “{0} is not a holiday.”.format(Platform.bold(format\_date(self.work\_from\_date))).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L3373) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L448) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L444)

<a id="op-bec0f1dfc824f2"></a>
### Compensatory Leave Request.on submit

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_on_submit`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**State and service calls** call db\_set on leave\_allocation · call db\_set on self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set company from Platform.db.get\_value(“Employee”, self.employee, “company”).
- Set date\_difference from (date\_diff(self.work\_end\_date, self.work\_from\_date) + 1).
- If self.half\_day.
  - Update date\_difference using − 0.5.
- Set comp\_leave\_valid\_from from add\_days(self.work\_end\_date, 1).
- Set leave\_period from get\_leave\_period(comp\_leave\_valid\_from, comp\_leave\_valid\_from, company).
- If leave\_period.
  - Set leave\_allocation from self.get\_existing\_allocation(comp\_leave\_valid\_from).
  - If leave\_allocation.
    - Update leave\_allocation.new\_leaves\_allocated using + date\_difference.
    - Evaluate leave\_allocation.validate().
    - Evaluate leave\_allocation.db\_set(“new\_leaves\_allocated”, leave\_allocation.total\_leaves\_allocated).
    - Evaluate leave\_allocation.db\_set(“total\_leaves\_allocated”, leave\_allocation.total\_leaves\_allocated).
    - Evaluate create\_additional\_leave\_ledger\_entry(leave\_allocation, date\_difference, comp\_leave\_valid\_from).
  - Otherwise.
    - Set leave\_allocation from self.create\_leave\_allocation(leave\_period, date\_difference).
  - Evaluate self.db\_set(“leave\_allocation”, leave\_allocation.name).
- Otherwise.
  - Set comp\_leave\_valid\_from from Platform.bold(format\_date(comp\_leave\_valid\_from)).
  - Set msg from translated “This compensatory leave will be applicable from {0}.”.format(comp\_leave\_valid\_from).
  - Update msg using + (one space + translated “Currently, there is no {0} leave period for this date to create/update leave allocation.”.format(Platform.bold(translated “active”))).
  - Update msg using + (text in the contract + translated “Please create a new {0} for the date {1} first.”.format(formatted text &lt;a href='{get\_url\_to\_list(“Leave Period”)}'&gt;Leave Period&lt;/a&gt;, comp\_leave\_valid\_from)).
  - Call the validation error handler Platform.throw(msg, title = translated “No Leave Period Found”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing allocation](operations-006.md#op-0d9b600234680b), [create leave allocation](operations-006.md#op-4499f197c95182).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L3773) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L445) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L441)

<a id="op-ca801a6c8e556b"></a>
### Compensatory Leave Request.on cancel

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Leave Allocation” via get\_doc.

**State and service calls** call db\_set on leave\_allocation.

**Local steps**

- If self.leave\_allocation.
  - Set date\_difference from (date\_diff(self.work\_end\_date, self.work\_from\_date) + 1).
  - If self.half\_day.
    - Update date\_difference using − 0.5.
  - Set leave\_allocation from Platform.get\_doc(“Leave Allocation”, self.leave\_allocation).
  - If leave\_allocation.
    - Update leave\_allocation.new\_leaves\_allocated using − date\_difference.
    - If leave\_allocation.new\_leaves\_allocated &lt; 0.
      - Set leave\_allocation.new\_leaves\_allocated from 0.
    - Evaluate leave\_allocation.validate().
    - Evaluate leave\_allocation.db\_set(“new\_leaves\_allocated”, leave\_allocation.total\_leaves\_allocated).
    - Evaluate leave\_allocation.db\_set(“total\_leaves\_allocated”, leave\_allocation.total\_leaves\_allocated).
    - Evaluate create\_additional\_leave\_ledger\_entry(leave\_allocation, (date\_difference × negative 1), add\_days(self.work\_end\_date, 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L4569) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L444) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L440)

<a id="op-0d9b600234680b"></a>
### Compensatory Leave Request.get existing allocation

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_get_existing_allocation`

**Inputs** self, comp\_leave\_valid\_from.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Leave Allocation” via get\_all · resolve a document from “Leave Allocation” via get\_doc.

**Explicit results** Platform.get\_doc(“Leave Allocation”, leave\_allocation at 0.name).

**Local steps**

- Set leave\_allocation from Platform.db.get\_all(“Leave Allocation”, filters = mapping(“employee” → self.employee, “leave\_type” → self.leave\_type, “from\_date” → tuple(“&lt;=”, comp\_leave\_valid\_from), “to\_date” → tuple(“&gt;=”, comp\_leave\_va ….
- If leave\_allocation.
  - Return Platform.get\_doc(“Leave Allocation”, leave\_allocation at 0.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L4951) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L443) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L439)

<a id="op-4499f197c95182"></a>
### Compensatory Leave Request.create leave allocation

`operation_workforce_human_resources_record_definitions_compensatory_leave_request_business_behavior_compensatory_leave_request_create_leave_allocation`

**Inputs** self, leave\_period, date\_difference.

**Record and data access** read “Leave Type” via get\_value · resolve a document from dict(doctype = “Leave Allocation”, employee = self.employee, employee\_name = self.employee\_name, leave\_type = self.leave\_type, …) via get\_doc.

**State and service calls** call insert on allocation · call submit on allocation.

**Explicit results** allocation.

**Local steps**

- Set is\_carry\_forward from Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_carry\_forward”).
- Set allocation from Platform.get\_doc(dict(doctype = “Leave Allocation”, employee = self.employee, employee\_name = self.employee\_name, leave\_type = self.leave\_type, …)).
- Evaluate allocation.insert(ignore\_permissions = true).
- Evaluate allocation.submit().
- Return allocation.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0013.json#L5223) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L442) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L438)

## Record · Department approver

[Record definition](../../../../data/record-types/department_approver.json)

<a id="op-81eea584736308"></a>
### Get approvers

`operation_workforce_human_resources_record_definitions_department_approver_business_behavior_get_approvers`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Employee” via get\_value · read “Department” via get\_value · read “User” via get\_value.

**Explicit results** set(generator of tuple(approver) for approver drawn from approvers).

**Explicit failure paths** validation helper — translated “Please select Employee first.” · validation helper with Platform.DoesNotExistError — translated “Employee {0} not found”.format(filters.get(“employee”)) · validation helper — error\_msg.

**Local steps**

- If not filters.get(“employee”).
  - Call the validation error handler Platform.throw(translated “Please select Employee first.”).
- Set approvers from list().
- Set department\_details from mapping().
- Set department\_list from list().
- Set employee from Platform.get\_value(“Employee”, filters.get(“employee”), list(“employee\_name”, “department”, “user\_id”, “leave\_approver”, …), as\_dict = true).
- If not employee.
  - Call the validation error handler Platform.throw(translated “Employee {0} not found”.format(filters.get(“employee”)), Platform.DoesNotExistError).
- Set employee\_department from (filters.get(“department”) or employee.department).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“department”) → employee.department.
- If employee\_department.
  - Set department\_details from Platform.db.get\_value(“Department”, mapping(“name” → employee\_department), list(“lft”, “rgt”), as\_dict = true).
- If department\_details.
  - Set Department from Platform.qb.DocType(“Department”).
  - Set department\_list from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….
- If (filters.get(“doctype”) equals “Leave Application” and employee.leave\_approver).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“doctype”) equals “Leave Application” → employee.leave\_approver.
  - Set approver from Platform.db.get\_value(“User”, mapping(“name” → employee.leave\_approver, “enabled” → 1), list(“name”, “first\_name”, “last\_name”)).
  - If approver.
    - Evaluate approvers.append(approver).
- If (filters.get(“doctype”) equals “Expense Claim” and employee.expense\_approver).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“doctype”) equals “Expense Claim” → employee.expense\_approver.
  - Set approver from Platform.db.get\_value(“User”, mapping(“name” → employee.expense\_approver, “enabled” → 1), list(“name”, “first\_name”, “last\_name”)).
  - If approver.
    - Evaluate approvers.append(approver).
- If (filters.get(“doctype”) equals “Shift Request” and employee.shift\_request\_approver).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“doctype”) equals “Shift Request” → employee.shift\_request\_approver.
  - Set approver from Platform.db.get\_value(“User”, mapping(“name” → employee.shift\_request\_approver, “enabled” → 1), list(“name”, “first\_name”, “last\_name”)).
  - If approver.
    - Evaluate approvers.append(approver).
- If filters.get(“doctype”) equals “Leave Application”.
  - Set parentfield from “leave\_approvers”.
  - Set field\_name from “Leave Approver”.
- Otherwise.
  - If filters.get(“doctype”) equals “Expense Claim”.
    - Set parentfield from “expense\_approvers”.
    - Set field\_name from “Expense Approver”.
  - Otherwise.
    - If filters.get(“doctype”) equals “Shift Request”.
      - Set parentfield from “shift\_request\_approver”.
      - Set field\_name from “Shift Request Approver”.
- If department\_list.
  - Set User from Platform.qb.DocType(“User”).
  - Set DeptApprover from Platform.qb.DocType(“Department Approver”).
  - For each d in department\_list.
    - Update approvers using + nested operand in the contract(nested operand in the contract).select(User.name, User.first\_name, User.last\_name).where((((nested operand in the contract equals nested operand in the contract bitwise and n ….
- Evaluate validate\_approver\_access(filters.get(“employee”), employee, approvers).
- If len(approvers) equals 0.
  - Set error\_msg from translated “Please set {0} for the Employee: {1}”.format(Platform.bold(translated field\_name), get\_link\_to\_form(“Employee”, filters.get(“employee”), employee.employee\_name)).
  - If department\_list.
    - Update error\_msg using + (one space + translated “or for the Employee's Department: {0}”.format(get\_link\_to\_form(“Department”, employee\_department))).
  - Call the validation error handler Platform.throw(error\_msg, title = translated “{0} Missing”.format(translated field\_name)).
- Return set(generator of tuple(approver) for approver drawn from approvers).
  - Draw approver from approvers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L15) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L475) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L456)

<a id="op-b34afdd7653ec3"></a>
### Validate approver access

`operation_workforce_binding_workforce_hr_doctype_department_approver_department_approver_validate_approver_access`

**Inputs** employee\_id, employee, approvers.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Set user from Platform.session.user.
- If (user equals employee.user\_id or Platform.has\_permission(“Employee”, “read”, employee\_id)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user equals employee.user\_id → Platform.has\_permission(“Employee”, “read”, employee\_id).
  - Return no value.
- Set employee\_approvers from set(employee.leave\_approver, employee.expense\_approver, employee.shift\_request\_approver).
- If (user belongs to employee\_approvers or user belongs to set of approver at 0 for approver drawn from approvers).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user belongs to employee\_approvers → user belongs to set of approver at 0 for approver drawn from approvers.
  - Draw approver from approvers.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee\_id).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L52) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L103) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L103)

## Record · Employee advance

[Record definition](../../../../data/record-types/employee_advance.json)

<a id="op-bb51f7ae7ce776"></a>
### Employee Advance.validate

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_advance\_amount().
- Evaluate self.validate\_advance\_account\_currency().
- Evaluate self.validate\_advance\_account\_type().
- Evaluate self.set\_status().
- Evaluate self.set\_pending\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate advance amount](operations-006.md#op-a082c80d6a1e17), [validate advance account currency](operations-006.md#op-a9796181e31924), [validate advance account type](operations-006.md#op-bd42ef007aeed6), [set status](operations-006.md#op-07752577dec9ae), [set pending amount](operations-007.md#op-8f2f49f5756329).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L16) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L488) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L469)

<a id="op-da96d2983d9446"></a>
### Employee Advance.before submit

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_before_submit`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please set the Advance Account {0} or in {1}”.format(get\_link\_to\_form(“Employee Advance”, (self.name + “#advance\_account”), translated “here”), get\_link\_to\_form(“Employee”, (self.employee + “#s … · validation helper — translated “Advance Account is mandatory. Please set the {0} in the Company {1} and submit this document.”.format(get\_link\_to\_form(“Company”, (self.company + “#hr\_and\_payroll\_tab”), “Default Employee Advan ….

**Local steps**

- If not self.get(“advance\_account”).
  - Set default\_advance\_account from Platform.db.get\_value(“Company”, self.company, “default\_employee\_advance\_account”).
  - Set same\_currency from self.currency equals Enterprise.get\_company\_currency(self.company).
  - If (default\_advance\_account and same\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_advance\_account → same\_currency.
    - Set self.advance\_account from default\_advance\_account.
    - Return no value.
  - If not same\_currency.
    - Call the validation error handler Platform.throw(translated “Please set the Advance Account {0} or in {1}”.format(get\_link\_to\_form(“Employee Advance”, (self.name + “#advance\_account”), translated “here”), get\_link\_to\_form(“Employee”, (self ….
  - Call the validation error handler Platform.throw(translated “Advance Account is mandatory. Please set the {0} in the Company {1} and submit this document.”.format(get\_link\_to\_form(“Company”, (self.company + “#hr\_and\_payroll\_tab”), “Default ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L4216) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L478) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L459)

<a id="op-524197b0a59072"></a>
### Employee Advance.on cancel

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Payment Ledger Entry”, “Advance Payment Ledger Entry”).
- Evaluate self.check\_linked\_payment\_entry().
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check linked payment entry](operations-007.md#op-132d8f64a30394), [set status](operations-006.md#op-07752577dec9ae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L4760) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L480) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L461)

<a id="op-0112845e128404"></a>
### Employee Advance.on update

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-006.md#op-e89150554b929e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L4887) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L482) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L463)

<a id="op-5eec94a48ddb99"></a>
### Employee Advance.after delete

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-006.md#op-e89150554b929e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L4938) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L477) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L458)

<a id="op-e89150554b929e"></a>
### Employee Advance.publish update

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Workforce.refetch\_resource(“Workforce:employee\_advance\_balance”, employee\_user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L4989) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L483) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L464)

<a id="op-a082c80d6a1e17"></a>
### Employee Advance.validate advance amount

`operation_workforce_binding_workforce_hr_doctype_employee_advance_employee_advance_employeeadvance_validate_advance_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Advance Amount must be greater than zero.”.

**Local steps**

- If flt(self.advance\_amount) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Advance Amount must be greater than zero.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L53) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L104) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L104)

<a id="op-bd42ef007aeed6"></a>
### Employee Advance.validate advance account type

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_validate_advance_account_type`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Employee advance account {0} should be of type {1}.”.format(get\_link\_to\_form(“Account”, self.advance\_account), Platform.bold(translated “Receivable”)).

**Local steps**

- If not self.advance\_account.
  - Return no value.
- Set account\_type from Platform.db.get\_value(“Account”, self.advance\_account, “account\_type”).
- If (not account\_type or account\_type differs from “Receivable”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not account\_type → account\_type differs from “Receivable”.
  - Call the validation error handler Platform.throw(translated “Employee advance account {0} should be of type {1}.”.format(get\_link\_to\_form(“Account”, self.advance\_account), Platform.bold(translated “Receivable”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L5115) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L490) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L471)

<a id="op-a9796181e31924"></a>
### Employee Advance.validate advance account currency

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_validate_advance_account_currency`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Advance Account {} currency should be same as Salary Currency of Employee {}. Please select same currency Ad …”.format(Platform.bold(self.advance\_account), Platform.bold(self.employee)).

**Local steps**

- If (self.currency and self.advance\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency → self.advance\_account.
  - Set account\_currency from Platform.db.get\_value(“Account”, self.advance\_account, “account\_currency”).
  - If self.currency differs from account\_currency.
    - Call the validation error handler Platform.throw(translated “Advance Account {} currency should be same as Salary Currency of Employee {}. Please select same currency Ad …”.format(Platform.bold(self.advance\_account), Platform.bold(self.employee))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L5379) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L489) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L470)

<a id="op-07752577dec9ae"></a>
### Employee Advance.set status

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_set_status`

**Inputs** self, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set precision from self.precision(“paid\_amount”).
- Set total\_amount from flt((flt(self.claimed\_amount) + flt(self.return\_amount)), precision).
- Set status from no value.
- If self.docstatus equals 0.
  - Set status from “Draft”.
- Otherwise.
  - If self.docstatus equals 1.
    - If (flt(self.claimed\_amount) &gt; 0 and flt(self.claimed\_amount, precision) equals flt(self.paid\_amount, precision)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.claimed\_amount) &gt; 0 → flt(self.claimed\_amount, precision) equals flt(self.paid\_amount, precision).
      - Set status from “Claimed”.
    - Otherwise.
      - If (flt(self.return\_amount) &gt; 0 and flt(self.return\_amount, precision) equals flt(self.paid\_amount, precision)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.return\_amount) &gt; 0 → flt(self.return\_amount, precision) equals flt(self.paid\_amount, precision).
        - Set status from “Returned”.
      - Otherwise.
        - If (flt(self.claimed\_amount) &gt; 0 and flt(self.return\_amount) &gt; 0 and total\_amount equals flt(self.paid\_amount, precision)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.claimed\_amount) &gt; 0 → flt(self.return\_amount) &gt; 0 → total\_amount equals flt(self.paid\_amount, precision).
          - Set status from “Partly Claimed and Returned”.
        - Otherwise.
          - If (flt(self.paid\_amount) &gt; 0 and flt(self.advance\_amount, precision) equals flt(self.paid\_amount, precision)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.paid\_amount) &gt; 0 → flt(self.advance\_amount, precision) equals flt(self.paid\_amount, precision).
            - Set status from “Paid”.
          - Otherwise.
            - If flt(self.paid\_amount) &gt; 0.
              - Set status from “Partially Paid”.
            - Otherwise.
              - Set status from “Unpaid”.
  - Otherwise.
    - If self.docstatus equals 2.
      - Set status from “Cancelled”.
- If update.
  - Evaluate self.db\_set(“status”, status).
  - Evaluate self.publish\_update().
  - Evaluate self.notify\_update().
- Otherwise.
  - Set self.status from status.

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-006.md#op-e89150554b929e).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L5622) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L485) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L466)

<a id="op-3f4907299b1127"></a>
### Employee Advance.on discard

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0015.json#L6502) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L481) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L462)

<a id="op-6d7616d4a8b49b"></a>
### Employee Advance.set total advance paid

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_set_total_advance_paid`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Employee advance account {0} should be of type {1}.”.format(get\_link\_to\_form(“Account”, self.advance\_account), Platform.bold(translated “Receivable”)) · validation helper with EmployeeAdvanceOverPayment — translated “Row {0}# Paid Amount cannot be greater than requested advance amount” · validation helper — translated “Return amount cannot be greater than unclaimed amount”.

**Local steps**

- Set aple from Platform.qb.DocType(“Advance Payment Ledger Entry”).
- Set account\_type from Platform.get\_value(“Account”, self.advance\_account, “account\_type”).
- If account\_type equals “Receivable”.
  - Set paid\_amount\_condition from aple.amount &gt; 0.
  - Set returned\_amount\_condition from aple.amount &lt; 0.
- Otherwise.
  - If account\_type equals “Payable”.
    - Set paid\_amount\_condition from aple.amount &lt; 0.
    - Set returned\_amount\_condition from aple.amount &gt; 0.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Employee advance account {0} should be of type {1}.”.format(get\_link\_to\_form(“Account”, self.advance\_account), Platform.bold(translated “Receivable”))).
- Set aple\_paid\_amount from (nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested o ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).where((((nested operand in the contract bitwise and nested operand in the contract) bitwise and paid\_am … at 0 → mapping().
- Set paid\_amount from (aple\_paid\_amount.get(“paid\_amount”) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in aple\_paid\_amount.get(“paid\_amount”) → 0.
- Set return\_amount from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_dict = true) at 0.return\_amount or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and returned\_amount\_condition)).run(as\_dict = true) … → 0.
- Set precision from self.precision(“paid\_amount”).
- Set paid\_amount from flt(paid\_amount, precision).
- If paid\_amount &gt; flt(self.advance\_amount, precision).
  - Call the validation error handler Platform.throw(translated “Row {0}# Paid Amount cannot be greater than requested advance amount”, EmployeeAdvanceOverPayment).
- Set precision from self.precision(“return\_amount”).
- Set return\_amount from flt(return\_amount, precision).
- If (return\_amount &gt; 0 and return\_amount &gt; flt((paid\_amount − self.claimed\_amount), precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in return\_amount &gt; 0 → return\_amount &gt; flt((paid\_amount − self.claimed\_amount), precision).
  - Call the validation error handler Platform.throw(translated “Return amount cannot be greater than unclaimed amount”).
- Evaluate self.db\_set(“paid\_amount”, paid\_amount).
- Evaluate self.db\_set(“return\_amount”, return\_amount).
- Evaluate self.set\_status(update = true).
- Evaluate self.set\_pending\_amount(update = true).
- Set base\_paid\_amount from (aple\_paid\_amount.get(“base\_paid\_amount”) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in aple\_paid\_amount.get(“base\_paid\_amount”) → 0.
- Evaluate self.db\_set(“base\_paid\_amount”, base\_paid\_amount).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-006.md#op-07752577dec9ae), [set pending amount](operations-007.md#op-8f2f49f5756329).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L486) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L467)

<a id="op-c1588a2b2bec6b"></a>
### Employee Advance.update claimed amount

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_update_claimed_amount`

**Inputs** self.

**State and service calls** request set\_value on “Employee Advance”.

**Local steps**

- Set ec from Platform.qb.DocType(“Expense Claim”).
- Set eca from Platform.qb.DocType(“Expense Claim Advance”).
- Set claimed\_amount from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0 → 0.
- Evaluate Platform.db.set\_value(“Employee Advance”, self.name, “claimed\_amount”, flt(claimed\_amount)).
- Evaluate self.reload().
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-006.md#op-07752577dec9ae).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L1600) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L487) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L468)
