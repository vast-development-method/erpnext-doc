# Company and master data · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee

[Record definition](../../../../data/record-types/employee.json)

<a id="op-c6e69f8b83af25"></a>
### Create user

`operation_enterprise_setup_record_definitions_employee_business_behavior_create_user`

**Inputs** employee, email = no value, create\_user\_permission = 0.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** request new\_doc for “User” · call db\_set on emp · call insert on user · call save on emp.

**Explicit results** user.name.

**Explicit failure paths** validation helper — translated “Employee {0} already has a linked user”.format(emp.name) · validation helper — translated “Email is required to create a user”.

**Local steps**

- Set emp from Platform.get\_doc(“Employee”, employee).
- Evaluate emp.check\_permission(“write”).
- If emp.user\_id.
  - Call the validation error handler Platform.throw(translated “Employee {0} already has a linked user”.format(emp.name)).
- If not email.
  - Call the validation error handler Platform.throw(translated “Email is required to create a user”).
- Set email from validate\_email\_address(email, true).
- Set employee\_name from emp.employee\_name.split(one space).
- Set first\_name from employee\_name at 0.
- Set middle\_name, last\_name from empty text.
- If len(employee\_name) ≥ 3.
  - Set last\_name from one space.join(employee\_name at slice 2 to no value).
  - Set middle\_name from employee\_name at 1.
- Otherwise.
  - If len(employee\_name) equals 2.
    - Set last\_name from employee\_name at 1.
- Set user from Platform.new\_doc(“User”).
- Evaluate user.update(mapping(“email” → email, “enabled” → 1, “first\_name” → first\_name, “middle\_name” → middle\_name, …)).
- Evaluate emp.db\_set(“user\_id”, email).
- Evaluate user.append\_roles(“Employee”).
- Evaluate user.insert().
- Set emp.user\_id from user.name.
- Set emp.create\_user\_permission from cint(create\_user\_permission).
- Evaluate emp.save().
- If cint(create\_user\_permission).
  - Evaluate add\_user\_permission(“Employee”, emp.name, user.name).
  - Evaluate add\_user\_permission(“Company”, emp.company, user.name).
- Return user.name.

**Values supplied outside this operation** effective access from emp.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L5472) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L420)

<a id="op-0bca952f3c4c4d"></a>
### Get all employee emails

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_all_employee_emails`

**Inputs** company.

**Record and data access** read “Employee” via get\_all · read “Employee” via get\_value.

**Explicit results** employee\_emails.

**Local steps**

- Set employee\_list from Platform.get\_all(“Employee”, fields = list(“name”, “employee\_name”), filters = mapping(“status” → “Active”, “company” → company)).
- Set employee\_emails from list().
- For each employee in employee\_list.
  - If not employee.
    - Continue with the next iteration or loop test.
  - Set tuple(user, company\_email, personal\_email) from Platform.db.get\_value(“Employee”, employee, list(“user\_id”, “company\_email”, “personal\_email”)).
  - Set email from (user or company\_email or personal\_email).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → company\_email → personal\_email.
  - If email.
    - Evaluate employee\_emails.append(email).
- Return employee\_emails.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L6523) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L445)

<a id="op-c4ff545ced92b1"></a>
### Get employee emails

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_employee_emails`

**Inputs** employee\_list.

**Record and data access** read “Employee” via get\_value.

**Explicit results** employee\_emails.

**Local steps**

- Set employee\_emails from list().
- For each employee in employee\_list.
  - If not employee.
    - Continue with the next iteration or loop test.
  - Set tuple(user, company\_email, personal\_email) from Platform.db.get\_value(“Employee”, employee, list(“user\_id”, “company\_email”, “personal\_email”)).
  - Set email from (user or company\_email or personal\_email).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → company\_email → personal\_email.
  - If email.
    - Evaluate employee\_emails.append(email).
- Return employee\_emails.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0691.json#L6861) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L450)

<a id="op-2add7bea0601f3"></a>
### Get children

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_children`

**Inputs** doctype, parent = no value, company = no value, is\_root = false, is\_tree = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list · read doctype via get\_all.

**Explicit results** employees.

**Local steps**

- Set filters from list(list(“status”, “=”, “Active”)).
- If (company and company differs from “All Companies”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → company differs from “All Companies”.
  - Evaluate filters.append(list(“company”, “=”, company)).
- Set fields from list(“name as value”, “employee\_name as title”).
- If is\_root.
  - Set parent from empty text.
- If (parent and company and parent differs from company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → company → parent differs from company.
  - Evaluate filters.append(list(“reports\_to”, “=”, parent)).
- Otherwise.
  - Evaluate filters.append(list(“reports\_to”, “=”, empty text)).
- Set employees from Platform.get\_list(doctype, fields = fields, filters = filters, order\_by = “name”).
- For each employee in employees.
  - Set is\_expandable from Platform.get\_all(doctype, filters = list(list(“reports\_to”, “=”, employee.get(“value”)))).
  - Set employee.expandable from 1 when is\_expandable, otherwise 0.
    - Value choice on is\_expandable — true gives 1, false gives 0.
- Return employees.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L446)

<a id="op-8cbf51adfca73b"></a>
### On doctype update

`operation_enterprise_setup_record_definitions_employee_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Employee”.

**Local steps**

- Evaluate Platform.db.add\_index(“Employee”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L609) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L455)

<a id="op-c6404e59d4d7db"></a>
### Has user permission for employee

`operation_enterprise_setup_record_definitions_employee_business_behavior_has_user_permission_for_employee`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user\_name, employee\_name.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L687) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L453)

<a id="op-16f8063ba58d8b"></a>
### Has upload permission

`operation_enterprise_setup_record_definitions_employee_business_behavior_has_upload_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, a comparison result.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L827) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L452)

<a id="op-80908d19ca3b5d"></a>
### Get contact details

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_contact_details`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** \_get\_contact\_details(employee).

**Explicit failure paths** validation helper.

**Local steps**

- If not employee.
  - Call the validation error handler Platform.throw(msg = translated “Employee is required”, title = translated “Missing Parameter”).
- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Return \_get\_contact\_details(employee).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L1011) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L447)

<a id="op-0d07ef966fae59"></a>
### Get contact details

`operation_enterprise_setup_record_definitions_employee_business_behavior_get_contact_details_2`

**Inputs** employee.

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** mapping(“contact\_display” → contact\_data.get(“employee\_name”), “contact\_email” → employee\_email, “contact\_mobile” → contact\_data.get(“cell\_number”), “contact\_designation” → contact\_data.get(“designation”), …).

**Explicit failure paths** validation helper.

**Local steps**

- Set contact\_data from Platform.db.get\_value(“Employee”, employee, list(“employee\_name”, “prefered\_email”, “company\_email”, “personal\_email”, …), as\_dict = true).
- If not contact\_data.
  - Call the validation error handler Platform.throw(msg = translated “Employee {0} not found”.format(employee), title = translated “Not Found”).
- Set employee\_email from (contact\_data.get(“prefered\_email”) or contact\_data.get(“company\_email”) or contact\_data.get(“personal\_email”) or contact\_data.get(“user\_id”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact\_data.get(“prefered\_email”) → contact\_data.get(“company\_email”) → contact\_data.get(“personal\_email”) → contact\_data.get(“user\_id”).
- Return mapping(“contact\_display” → contact\_data.get(“employee\_name”), “contact\_email” → employee\_email, “contact\_mobile” → contact\_data.get(“cell\_number”), “contact\_designation” → contact\_data.get(“designation”), …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L1224) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L448)

## Record · Employee group

[Record definition](../../../../data/record-types/employee_group.json)

<a id="op-c8e258ac21912d"></a>
### Employee Group.validate

`operation_enterprise_binding_enterprise_setup_doctype_employee_group_employee_group_employeegroup_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “An employee can only appear once in an Employee Group”.

**Local steps**

- Set employees from list of row.employee for row drawn from self.employee\_list where row.employee.
  - Draw row from self.employee\_list, keep a combination only if (row.employee).
- If len(employees) differs from len(set(employees)).
  - Call the validation error handler Platform.throw(translated “An employee can only appear once in an Employee Group”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L156)

## Record · Global defaults

[Record definition](../../../../data/record-types/global_defaults.json)

<a id="op-ef1b8e7bcbd906"></a>
### Global Defaults.validate

`operation_enterprise_binding_enterprise_setup_doctype_global_defaults_global_defaults_globaldefaults_validate`

**Inputs** self.

**Local steps**

- If (self.has\_value\_changed(“enable\_item\_search\_index”) and self.enable\_item\_search\_index).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“enable\_item\_search\_index”) → self.enable\_item\_search\_index.
  - Evaluate validate\_sqlite\_version().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L157)

<a id="op-fb7273db3a03d8"></a>
### Global Defaults.on update

`operation_enterprise_setup_record_definitions_global_defaults_business_behavior_global_defaults_on_update`

**Inputs** self.

**Record and data access** resolve a document from “Currency” via get\_doc.

**State and service calls** call save on currency.

**Local steps**

- For each key in keydict.
  - Evaluate Platform.db.set\_default(key, cstr(self.get(keydict at key))).
- If self.default\_currency.
  - Set currency from Platform.get\_doc(“Currency”, self.default\_currency).
  - If not currency.enabled.
    - Set currency.enabled from 1.
    - Evaluate currency.save(ignore\_permissions = true).
- Evaluate self.toggle\_rounded\_total().
- Evaluate self.toggle\_in\_words().

If control reaches the end, it returns no value.

**Methods declared on this owner** [toggle rounded total](operations-009.md#op-45e5ac1d5067a1), [toggle in words](operations-009.md#op-c58e067168c24b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L466)

<a id="op-6a613cb2dcf5cb"></a>
### Global Defaults.get defaults

`operation_enterprise_setup_record_definitions_global_defaults_business_behavior_global_defaults_get_defaults`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.defaults.get\_defaults().

**Local steps**

- Return Platform.defaults.get\_defaults().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L5587) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L465)

<a id="op-45e5ac1d5067a1"></a>
### Global Defaults.toggle rounded total

`operation_enterprise_setup_record_definitions_global_defaults_business_behavior_global_defaults_toggle_rounded_total`

**Inputs** self.

**Local steps**

- Set self.disable\_rounded\_total from cint(self.disable\_rounded\_total).
- For each doctype in tuple(“Quotation”, “Sales Order”, “Sales Invoice”, “Delivery Note”, …).
  - Evaluate make\_property\_setter(doctype, “base\_rounded\_total”, “hidden”, self.disable\_rounded\_total, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “base\_rounded\_total”, “print\_hide”, 1, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “rounded\_total”, “hidden”, self.disable\_rounded\_total, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “rounded\_total”, “print\_hide”, self.disable\_rounded\_total, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “disable\_rounded\_total”, “default”, cint(self.disable\_rounded\_total), validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L468)

<a id="op-c58e067168c24b"></a>
### Global Defaults.toggle in words

`operation_enterprise_setup_record_definitions_global_defaults_business_behavior_global_defaults_toggle_in_words`

**Inputs** self.

**Local steps**

- Set self.disable\_in\_words from cint(self.disable\_in\_words).
- For each doctype in tuple(“Quotation”, “Sales Order”, “Sales Invoice”, “Delivery Note”, …).
  - Evaluate make\_property\_setter(doctype, “in\_words”, “hidden”, self.disable\_in\_words, validate\_fields\_for\_doctype = false, …).
  - If doctype belongs to tuple(“Payment Entry”, “Subcontracting Receipt”).
    - Continue with the next iteration or loop test.
  - Evaluate make\_property\_setter(doctype, “in\_words”, “print\_hide”, self.disable\_in\_words, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L467)

## Record · Holiday list

[Record definition](../../../../data/record-types/holiday_list.json)

<a id="op-90359bfb7ae8b1"></a>
### Holiday List.validate

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_days().
- Evaluate self.update\_total\_holidays().
- Evaluate self.validate\_duplicate\_date().
- Evaluate self.sort\_holidays().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate days](operations-009.md#op-628f38e11ee158), [update total holidays](operations-009.md#op-4318fa0e456f6b), [validate duplicate date](operations-010.md#op-c8f1ce36507cac), [sort holidays](operations-009.md#op-6874bffe4e512a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L6346) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L478)

<a id="op-4318fa0e456f6b"></a>
### Holiday List.update total holidays

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_update_total_holidays`

**Inputs** self.

**Local steps**

- Set self.total\_holidays from sum(generator of 0.5 when cint(holiday.is\_half\_day), otherwise 1 for holiday drawn from self.holidays).
  - Draw holiday from self.holidays.
  - Value choice on cint(holiday.is\_half\_day) — true gives 0.5, false gives 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L6457) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L477)

<a id="op-75a2c19492c2ca"></a>
### Holiday List.get weekly off dates

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_get_weekly_off_dates`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If not self.weekly\_off.
  - Evaluate throw(translated “Please select weekly off day”).
- Set existing\_holidays from self.get\_holidays().
- For each d in self.get\_weekly\_off\_date\_list(self.from\_date, self.to\_date).
  - If d belongs to existing\_holidays.
    - Continue with the next iteration or loop test.
  - Evaluate self.append(“holidays”, mapping(“description” → translated self.weekly\_off, “holiday\_date” → d, “weekly\_off” → 1, “is\_half\_day” → self.is\_half\_day)).
- Evaluate self.update\_total\_holidays().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get holidays](operations-009.md#op-cfb83a5d9ca07c), [get weekly off date list](operations-009.md#op-3f0bc222efb6e4), [update total holidays](operations-009.md#op-4318fa0e456f6b).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L6569) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L475)

<a id="op-de8255733971c2"></a>
### Holiday List.get supported countries

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_get_supported_countries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“countries” → countries, “subdivisions\_by\_country” → subdivisions\_by\_country).

**Local steps**

- Bind dependencies list\_supported\_countries.
- Set subdivisions\_by\_country from list\_supported\_countries().
- Set countries from list of mapping(“value” → country, “label” → local\_country\_name(country)) for country drawn from subdivisions\_by\_country.keys().
  - Draw country from subdivisions\_by\_country.keys().
- Return mapping(“countries” → countries, “subdivisions\_by\_country” → subdivisions\_by\_country).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0692.json#L6906) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L473)

<a id="op-15626b0f70af37"></a>
### Holiday List.get local holidays

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_get_local_holidays`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Bind dependencies country\_holidays.
- If not self.country.
  - Evaluate throw(translated “Please select a country”).
- Set existing\_holidays from self.get\_holidays().
- Set from\_date from getdate(self.from\_date).
- Set to\_date from getdate(self.to\_date).
- For each tuple(holiday\_date, holiday\_name) in country\_holidays(self.country, subdiv = self.subdivision, years = list(range(from\_date.year, (nested operand in the contract.year + 1))), language = Platform.local.lang).items().
  - If holiday\_date belongs to existing\_holidays.
    - Continue with the next iteration or loop test.
  - If (holiday\_date &lt; from\_date or holiday\_date &gt; to\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in holiday\_date &lt; from\_date → holiday\_date &gt; to\_date.
    - Continue with the next iteration or loop test.
  - Evaluate self.append(“holidays”, mapping(“description” → holiday\_name, “holiday\_date” → holiday\_date, “weekly\_off” → 0)).
- Evaluate self.update\_total\_holidays().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get holidays](operations-009.md#op-cfb83a5d9ca07c), [update total holidays](operations-009.md#op-4318fa0e456f6b).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L472)

<a id="op-6874bffe4e512a"></a>
### Holiday List.sort holidays

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_sort_holidays`

**Inputs** self.

**Local steps**

- Evaluate self.holidays.sort(key = deferred anonymous expression).
- For each i in range(len(self.holidays)).
  - Set self.holidays at i.idx from (i + 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L476)

<a id="op-cfb83a5d9ca07c"></a>
### Holiday List.get holidays

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_get_holidays`

**Inputs** self.

**Declared result** list at date.

**Explicit results** list of getdate(holiday.holiday\_date) for holiday drawn from self.holidays.

**Local steps**

- Return list of getdate(holiday.holiday\_date) for holiday drawn from self.holidays.
  - Draw holiday from self.holidays.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L702) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L471)

<a id="op-628f38e11ee158"></a>
### Holiday List.validate days

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_validate_days`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The holiday on {0} is not between From Date and To Date”.format(formatdate(day.holiday\_date)).

**Local steps**

- If getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Evaluate throw(translated “To Date cannot be before From Date”).
- For each day in self.get(“holidays”).
  - If not getdate(self.from\_date) ≤ getdate(day.holiday\_date) ≤ getdate(self.to\_date).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.from\_date) ≤ getdate(day.holiday\_date) ≤ getdate(self.to\_date).
    - Call the validation error handler Platform.throw(translated “The holiday on {0} is not between From Date and To Date”.format(formatdate(day.holiday\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L792) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L479)

<a id="op-3f0bc222efb6e4"></a>
### Holiday List.get weekly off date list

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_get_weekly_off_date_list`

**Inputs** self, start\_date, end\_date.

**Explicit results** date\_list.

**Local steps**

- Set tuple(start\_date, end\_date) from tuple(getdate(start\_date), getdate(end\_date)).
- Bind dependencies calendar.
- Bind dependencies timedelta.
- Bind dependencies relativedelta.
- Set date\_list from list().
- Set existing\_date\_list from list().
- Set weekday from getattr(calendar, self.weekly\_off.upper()).
- Set reference\_date from (start\_date + relativedelta.relativedelta(weekday = weekday)).
- Set existing\_date\_list from list of getdate(holiday.holiday\_date) for holiday drawn from self.get(“holidays”).
  - Draw holiday from self.get(“holidays”).
- While reference\_date ≤ end\_date.
  - If reference\_date does not belong to existing\_date\_list.
    - Evaluate date\_list.append(reference\_date).
  - Update reference\_date using + timedelta(days = 7).
- Return date\_list.

**Values supplied outside this operation** selected callable from getattr(calendar, self.weekly\_off.upper()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L1105) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L474)
