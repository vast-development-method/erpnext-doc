# Company and master data · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee

[Record definition](../../../../data/record-types/employee.json)

<a id="op-0d8af1db55ac89"></a>
### Employee.update nsm model

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_update_nested_set_model_model`

**Inputs** self.

**Local steps**

- Evaluate Platform.utils.nestedset.update\_nsm(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L6986) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L431)

<a id="op-52a87b290e8e30"></a>
### Employee.on update

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_nsm\_model().
- Evaluate Platform.clear\_cache().
- If self.user\_id.
  - Evaluate self.update\_user().
  - Evaluate self.update\_user\_permissions().
  - Evaluate self.update\_user\_status().
- Evaluate self.reset\_employee\_emails\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update nsm model](operations-008.md#op-0d8af1db55ac89), [update user](operations-008.md#op-f75d4952d3d3af), [update user permissions](operations-008.md#op-8d4564bb5b4d78), [update user status](operations-008.md#op-8a4e279482b18f), [reset employee emails cache](operations-008.md#op-c817ff9fb3d36e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L7050) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L427)

<a id="op-ac3792f383be44"></a>
### Employee.before insert

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_auto\_user\_creation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate auto user creation](operations-007.md#op-6a0daaee810b1d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L7214) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L425)

<a id="op-fac774300d7fd5"></a>
### Employee.after insert

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_after_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.create\_user\_automatically.
  - Return no value.
- If self.user\_id.
  - Return no value.
- Evaluate create\_user(employee = self.name, email = (self.prefered\_email or self.company\_email or self.personal\_email), create\_user\_permission = self.create\_user\_permission).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.prefered\_email → self.company\_email → self.personal\_email.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L7265) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L422)

<a id="op-8d4564bb5b4d78"></a>
### Employee.update user permissions

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_update_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L433)

<a id="op-f75d4952d3d3af"></a>
### Employee.update user

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_update_user`

**Inputs** self.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Local steps**

- Set user from Platform.get\_doc(“User”, self.user\_id).
- Set user.flags.ignore\_permissions from true.
- If “Employee” does not belong to user.get(“roles”).
  - Evaluate user.append\_roles(“Employee”).
- If (self.employee\_name and not (user.first\_name and user.last\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.employee\_name → not (user.first\_name and user.last\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user.first\_name → user.last\_name.
  - Set employee\_name from self.employee\_name.split(one space).
  - If len(employee\_name) ≥ 3.
    - Set user.last\_name from one space.join(employee\_name at slice 2 to no value).
    - Set user.middle\_name from employee\_name at 1.
  - Otherwise.
    - If len(employee\_name) equals 2.
      - Set user.last\_name from employee\_name at 1.
  - Set user.first\_name from employee\_name at 0.
- If self.date\_of\_birth.
  - Set user.birth\_date from self.date\_of\_birth.
- If self.gender.
  - Set user.gender from self.gender.
- If self.image.
  - If (not user.user\_image or self.has\_value\_changed(“image”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not user.user\_image → self.has\_value\_changed(“image”).
    - Set user.user\_image from self.image.
- Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L432)

<a id="op-cb276baeca2d1a"></a>
### Employee.validate date

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_date`

**Inputs** self.

**Local steps**

- If (self.date\_of\_birth and getdate(self.date\_of\_birth) &gt; getdate(today())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.date\_of\_birth → getdate(self.date\_of\_birth) &gt; getdate(today()).
  - Evaluate throw(translated “Date of Birth cannot be greater than today.”).
- Evaluate self.validate\_from\_to\_dates(“date\_of\_birth”, “date\_of\_joining”).
- Evaluate self.validate\_from\_to\_dates(“date\_of\_joining”, “date\_of\_retirement”).
- Evaluate self.validate\_from\_to\_dates(“date\_of\_joining”, “relieving\_date”).
- Evaluate self.validate\_from\_to\_dates(“date\_of\_joining”, “contract\_end\_date”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L1253) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L887) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L437)

<a id="op-8ee8916428e0db"></a>
### Employee.validate email

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_email`

**Inputs** self.

**Local steps**

- If self.company\_email.
  - Evaluate validate\_email\_address(self.company\_email, true).
- If self.personal\_email.
  - Evaluate validate\_email\_address(self.personal\_email, true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L1541) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L439)

<a id="op-fa68abe542f7bb"></a>
### Employee.set preferred email

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_set_preferred_email`

**Inputs** self.

**Local steps**

- Set preferred\_email\_field from Platform.scrub(self.prefered\_contact\_email).
- Set self.prefered\_email from self.get(preferred\_email\_field) when preferred\_email\_field, otherwise no value.
  - Value choice on preferred\_email\_field — true gives self.get(preferred\_email\_field), false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L1657) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L430)

<a id="op-20eecc13c89699"></a>
### Employee.validate status

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_status`

**Inputs** self.

**Record and data access** read “Employee” via get\_all.

**Local steps**

- If self.status equals “Left”.
  - Set reports\_to from Platform.db.get\_all(“Employee”, filters = mapping(“reports\_to” → self.name, “status” → “Active”), fields = list(“name”, “employee\_name”)).
  - If reports\_to.
    - Set link\_to\_employees from list of Platform.utils.get\_link\_to\_form(“Employee”, employee.name, label = employee.employee\_name) for employee drawn from reports\_to.
      - Draw employee from reports\_to.
    - Set message from translated “The following employees are currently still reporting to {0}:”.format(Platform.bold(self.employee\_name)).
    - Update message using + (text in the contract + “&lt;/li&gt;&lt;li&gt;”.join(link\_to\_employees)).
    - Update message using + “&lt;/li&gt;&lt;/ul&gt;&lt;br&gt;”.
    - Update message using + translated “Please make sure the employees above report to another Active employee.”.
    - Evaluate throw(message, InactiveEmployeeStatusError, translated “Cannot Relieve Employee”).
  - If not self.relieving\_date.
    - Evaluate throw(translated “Please enter relieving date.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L1767) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L443)

<a id="op-238bb28a9aa90e"></a>
### Employee.validate for enabled user id

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_for_enabled_user_identifier`

**Inputs** self.

**Record and data access** read “User” via exists.

**Explicit failure paths** validation helper — translated “User {0} does not exist”.format(self.user\_id).

**Local steps**

- If not Platform.db.exists(“User”, self.user\_id).
  - Call the validation error handler Platform.throw(translated “User {0} does not exist”.format(self.user\_id)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L2264) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L440)

<a id="op-8a4e279482b18f"></a>
### Employee.update user status

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_update_user_status`

**Inputs** self.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** msgprint with translated “User {0} is disabled. Only a user who can edit Users can enable it.”.format(Platform.bold(self.user\_id)) · call save on user.

**Explicit results** no value.

**Local steps**

- If not self.user\_id.
  - Return no value.
- If (not self.has\_value\_changed(“status”) and not self.has\_value\_changed(“user\_id”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_value\_changed(“status”) → not self.has\_value\_changed(“user\_id”).
  - Return no value.
- Set user from Platform.get\_doc(“User”, self.user\_id).
- Set enable from self.status equals “Active”.
- If user.enabled equals enable.
  - Return no value.
- If (enable and not self.can\_reenable\_user(user)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enable → not self.can\_reenable\_user(user).
  - Evaluate Platform.msgprint(translated “User {0} is disabled. Only a user who can edit Users can enable it.”.format(Platform.bold(self.user\_id))).
  - Return no value.
- Set user.enabled from enable.
- Evaluate user.save(ignore\_permissions = true, ignore\_version = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can reenable user](operations-008.md#op-81b0d21f90140b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L434)

<a id="op-81b0d21f90140b"></a>
### Employee.can reenable user

`operation_enterprise_binding_enterprise_setup_doctype_employee_employee_employee_can_reenable_user`

**Inputs** self, user.

**Record and data access** read “Version” via get\_all.

**Explicit results** true · (bool(last\_change) and not Platform.has\_permission(“User”, “write”, user = last\_change at 0, ignore\_share\_permissions = true)).

**Local steps**

- If Platform.has\_permission(“User”, “write”, user).
  - Return true.
- Set last\_change from Platform.get\_all(“Version”, filters = mapping(“ref\_doctype” → “User”, “docname” → user.name, “data” → tuple(“like”, “%&#91;"enabled",%”)), pluck = “owner”, order\_by = “creation desc”, limit = 1).
- Return (bool(last\_change) and not Platform.has\_permission(“User”, “write”, user = last\_change at 0, ignore\_share\_permissions = true)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(last\_change) → not Platform.has\_permission(“User”, “write”, user = last\_change at 0, ignore\_share\_permissions = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“User”, “write”, user), Platform.has\_permission(“User”, “write”, user = last\_change at 0, ignore\_share\_permissions = true).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L153)

<a id="op-2a81d536c2c19b"></a>
### Employee.validate duplicate user id

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_duplicate_user_identifier`

**Inputs** self.

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set employee from nested operand in the contract(nested operand in the contract).select(Employee.name).where(((nested operand in the contract.user\_id equals nested operand in the contract.user\_id bitwise and nested operand  ….run().
- If employee.
  - Evaluate throw(translated “User {0} is already assigned to Employee {1}”.format(self.user\_id, employee at 0 at 0), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L2724) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L438)

<a id="op-8acf6b3c1b7133"></a>
### Employee.validate reports to

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_reports_to`

**Inputs** self.

**Local steps**

- If self.reports\_to equals self.name.
  - Evaluate throw(translated “Employee cannot report to himself.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L3043) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L442)

<a id="op-4201344b904d3d"></a>
### Employee.on trash

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.update\_nsm\_model().
- Evaluate delete\_events(self.doctype, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update nsm model](operations-008.md#op-0d8af1db55ac89).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L3141) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L426)

<a id="op-09421b0c790141"></a>
### Employee.validate preferred email

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_preferred_email`

**Inputs** self.

**State and service calls** msgprint with translated “Please enter {0}”.format(self.prefered\_contact\_email).

**Local steps**

- If (self.prefered\_contact\_email and not self.get(scrub(self.prefered\_contact\_email))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.prefered\_contact\_email → not self.get(scrub(self.prefered\_contact\_email)).
  - Evaluate Platform.msgprint(translated “Please enter {0}”.format(self.prefered\_contact\_email)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L3227) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L441)

<a id="op-c817ff9fb3d36e"></a>
### Employee.reset employee emails cache

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_reset_employee_emails_cache`

**Inputs** self.

**Local steps**

- Set prev\_doc from (self.get\_doc\_before\_save() or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_doc\_before\_save() → mapping().
- Set cell\_number from cstr(self.get(“cell\_number”)).
- Set prev\_number from cstr(prev\_doc.get(“cell\_number”)).
- If (cell\_number differs from prev\_number or self.get(“user\_id”) differs from prev\_doc.get(“user\_id”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cell\_number differs from prev\_number → self.get(“user\_id”) differs from prev\_doc.get(“user\_id”).
  - Evaluate Platform.cache().hdel(“employees\_with\_number”, cell\_number).
  - Evaluate Platform.cache().hdel(“employees\_with\_number”, prev\_number).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L3380) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L428)

<a id="op-12dc8b1d0c82cf"></a>
### Get admin roles

`operation_enterprise_binding_enterprise_setup_doctype_employee_employee_get_admin_roles`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** roles.

**Local steps**

- Set roles from set(“Administrator”, “System Manager”).
- For each doctype in tuple(“User”, “Role”).
  - Evaluate roles.update(generator of perm.role for perm drawn from Platform.get\_meta(doctype).permissions where (perm.write and not perm.permlevel)).
    - Draw perm from Platform.get\_meta(doctype).permissions, keep a combination only if ((perm.write and not perm.permlevel)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.write → not perm.permlevel.
- Return roles.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L155)

<a id="op-445b5f3d2f3fc2"></a>
### Validate employee role

`operation_enterprise_setup_record_definitions_employee_business_behavior_validate_employee_role`

**Inputs** doc, method = no value, ignore\_emp\_check = false.

**Record and data access** read “Employee” via get\_value.

**State and service calls** msgprint with translated “User {0}: Removed Employee role as there is no mapped employee.”.format(doc.name) · msgprint with translated “User {0}: Removed Employee Self Service role as there is no mapped employee.”.format(doc.name).

**Explicit results** no value.

**Local steps**

- If not ignore\_emp\_check.
  - If Platform.db.get\_value(“Employee”, mapping(“user\_id” → doc.name)).
    - Return no value.
- Set user\_roles from list of d.role for d drawn from doc.get(“roles”).
  - Draw d from doc.get(“roles”).
- If “Employee” belongs to user\_roles.
  - Evaluate Platform.msgprint(translated “User {0}: Removed Employee role as there is no mapped employee.”.format(doc.name)).
  - Evaluate doc.get(“roles”).remove(doc.get(“roles”, mapping(“role” → “Employee”)) at 0).
- If “Employee Self Service” belongs to user\_roles.
  - Evaluate Platform.msgprint(translated “User {0}: Removed Employee Self Service role as there is no mapped employee.”.format(doc.name)).
  - Evaluate doc.get(“roles”).remove(doc.get(“roles”, mapping(“role” → “Employee Self Service”)) at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L3699) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L456)

<a id="op-36b11724a78299"></a>
### Get employee email

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_employee_email`

**Inputs** employee\_doc.

**Explicit results** (employee\_doc.get(“user\_id”) or employee\_doc.get(“personal\_email”) or employee\_doc.get(“company\_email”)).

**Local steps**

- Return (employee\_doc.get(“user\_id”) or employee\_doc.get(“personal\_email”) or employee\_doc.get(“company\_email”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_doc.get(“user\_id”) → employee\_doc.get(“personal\_email”) → employee\_doc.get(“company\_email”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L4244) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L449)

<a id="op-653e4b424f97fa"></a>
### Get holiday list for employee

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_holiday_list_for_employee`

**Inputs** employee, raise\_exception = true, as\_on = no value.

**Record and data access** read “Employee” via get\_cached\_value · read “Global Defaults” via get\_single\_value · read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_attr(Workforce\_override at negative 1)(employee, raise\_exception, as\_on) · holiday\_list.

**Explicit failure paths** validation helper — translated “Please set a default Holiday List for Employee {0} or Company {1}”.format(employee, company).

**Local steps**

- Set Workforce\_override from Platform.get\_hooks(“employee\_holiday\_list”).
- If Workforce\_override.
  - Return Platform.get\_attr(Workforce\_override at negative 1)(employee, raise\_exception, as\_on).
- If employee.
  - Set tuple(holiday\_list, company) from Platform.get\_cached\_value(“Employee”, employee, list(“holiday\_list”, “company”)).
- Otherwise.
  - Set holiday\_list from empty text.
  - Set company from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).
- If not holiday\_list.
  - Set holiday\_list from Platform.get\_cached\_value(“Company”, company, “default\_holiday\_list”).
- If (not holiday\_list and raise\_exception).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not holiday\_list → raise\_exception.
  - Call the validation error handler Platform.throw(translated “Please set a default Holiday List for Employee {0} or Company {1}”.format(employee, company)).
- Return holiday\_list.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“employee\_holiday\_list”), Platform.get\_attr(Workforce\_override at negative 1) · configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“holiday\_list”, “company”)), Platform.db.get\_single\_value(“Global Defaults”, “default\_company”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L4357) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L451)

<a id="op-0e9fb1d3a9d735"></a>
### Is holiday

`operation_enterprise_setup_record_definitions_employee_business_behavior_is_holiday`

**Inputs** employee, date = no value, raise\_exception = true, only\_non\_weekly = false, with\_description = false.

**Record and data access** read “Holiday” via get\_all.

**Explicit results** false · tuple(len(holidays) &gt; 0, holidays) · len(holidays) &gt; 0.

**Local steps**

- If not date.
  - Set date from today().
- Set holiday\_list from get\_holiday\_list\_for\_employee(employee, raise\_exception, as\_on = date).
- If not holiday\_list.
  - Return false.
- Set filters from mapping(“parent” → holiday\_list, “holiday\_date” → date).
- If only\_non\_weekly.
  - Set filters at “weekly\_off” from false.
- Set holidays from Platform.get\_all(“Holiday”, fields = list(“description”), filters = filters, pluck = “description”).
- If with\_description.
  - Return tuple(len(holidays) &gt; 0, holidays).
- Return len(holidays) &gt; 0.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L454)

<a id="op-b5d7b55a3cf1f8"></a>
### Deactivate sales person

`operation_enterprise_setup_record_definitions_employee_business_behavior_deactivate_sales_person`

**Inputs** status = no value, employee = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Person” via get\_value.

**State and service calls** request set\_value on “Sales Person”.

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, doc = employee, ptype = “write”, throw = true).
- If status equals “Left”.
  - Set sales\_person from Platform.db.get\_value(“Sales Person”, mapping(“Employee” → employee)).
  - If sales\_person.
    - Evaluate Platform.db.set\_value(“Sales Person”, sales\_person, “enabled”, 0).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, doc = employee, ptype = “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L421)
