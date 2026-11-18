# Regional rules and controller overrides · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Appraisal

<a id="op-0be3f3ec1195e0"></a>
### Appraisal Mixin.validate total weightage

`operation_workforce_mixins_appraisal_business_behavior_appraisal_mixin_validate_total_weightage`

**Inputs** self, table\_name, table\_label.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Total weightage for all {0} must add up to 100. Currently, it is {1}%”.format(Platform.bold(translated table\_label), total\_weightage).

**Local steps**

- If not self.get(table\_name).
  - Return no value.
- Set total\_weightage from sum(generator of flt(d.per\_weightage) for d drawn from self.get(table\_name)).
  - Draw d from self.get(table\_name).
- If flt(total\_weightage, 2) differs from 100.0.
  - Call the validation error handler Platform.throw(translated “Total weightage for all {0} must add up to 100. Currently, it is {1}%”.format(Platform.bold(translated table\_label), total\_weightage), title = translated “Incorrect Weightage Allocation”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L2929) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L183) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L532)

## Service · Company

<a id="op-6d867a9a7961d4"></a>
### Make company fixtures

`operation_workforce_overrides_company_business_behavior_make_company_fixtures`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If not Platform.flags.country\_change.
  - Return no value.
- Evaluate run\_regional\_setup(doc.country).
- Evaluate make\_salary\_components(doc.country).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L4632) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L197) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L546)

<a id="op-5692d797386c37"></a>
### Delete company fixtures

`operation_workforce_overrides_company_business_behavior_delete_company_fixtures`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_all.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set countries from Platform.get\_all(“Company”, distinct = “True”, pluck = “country”).
- For each country in countries.
  - Attempt the following.
    - Set module\_name from formatted text Workforce.regional.{Platform.scrub(country)}.setup.uninstall.
    - Evaluate Platform.get\_attr(module\_name)().
  - On failure (tuple(ImportError, AttributeError)).
    - Take no action here.
  - On failure (Exception) bound to e.
    - Evaluate Platform.log\_error(“Unable to delete country fixtures for Platform HR”).
    - Set msg from translated “Failed to delete defaults for country {0}.”.format(Platform.bold(country)).
    - Update msg using + (text in the contract + translated “{0}: {1}”.format(Platform.bold(translated “Error”), get\_error\_message(e))).
    - Call the validation error handler Platform.throw(msg, title = translated “Country Fixture Deletion Failed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(module\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L4751) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L191) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L540)

<a id="op-11b5975fae9f63"></a>
### Run regional setup

`operation_workforce_overrides_company_business_behavior_run_regional_setup`

**Inputs** country.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Attempt the following.
  - Set module\_name from formatted text Workforce.regional.{Platform.scrub(country)}.setup.setup.
  - Evaluate Platform.get\_attr(module\_name)().
- On failure (ImportError).
  - Take no action here.
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(“Unable to setup country fixtures for Platform HR”).
  - Set msg from translated “Failed to setup defaults for country {0}.”.format(Platform.bold(country)).
  - Update msg using + (text in the contract + translated “{0}: {1}”.format(Platform.bold(translated “Error”), get\_error\_message(e))).
  - Call the validation error handler Platform.throw(msg, title = translated “Country Setup failed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(module\_name).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L5207) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L200) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L549)

<a id="op-b28b2f590b6beb"></a>
### Get error message

`operation_workforce_overrides_company_business_behavior_get_error_message`

**Inputs** error.

**Declared result** str.

**Explicit results** error\_message.

**Local steps**

- Attempt the following.
  - Set message\_log from Platform.message\_log.pop() when Platform.message\_log, otherwise str(error).
    - Value choice on Platform.message\_log — true gives Platform.message\_log.pop(), false gives str(error).
  - If isinstance(message\_log, str).
    - Set error\_message from json.loads(message\_log).get(“message”).
  - Otherwise.
    - Set error\_message from message\_log.get(“message”).
- On failure (Exception).
  - Set error\_message from message\_log.
- Return error\_message.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L5587) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L193) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L542)

<a id="op-257a8ba61099aa"></a>
### Make salary components

`operation_workforce_overrides_company_business_behavior_make_salary_components`

**Inputs** country.

**Record and data access** read “Salary Component” via exists · resolve a document from d via get\_doc.

**State and service calls** call insert on doc.

**Local steps**

- Set docs from list().
- Set file\_name from “salary\_components.json”.
- If not Platform.db.exists(“Salary Component”, “Basic”).
  - Set file\_path from Platform.get\_app\_path(“Workforce”, “payroll”, “data”, file\_name).
  - Evaluate docs.extend(json.loads(read\_data\_file(file\_path))).
- Set file\_path from Platform.get\_app\_path(“Workforce”, “regional”, Platform.scrub(country), “data”, …).
- Evaluate docs.extend(json.loads(read\_data\_file(file\_path))).
- For each d in docs.
  - Attempt the following.
    - Set doc from Platform.get\_doc(d).
    - Set doc.flags.ignore\_permissions from true.
    - Set doc.flags.ignore\_mandatory from true.
    - Evaluate doc.insert(ignore\_if\_duplicate = true).
  - On failure (Exception) bound to e.
    - Evaluate Platform.error\_log(“Error occurred while creating Salary Component”, e).
  - On exit, including pending return or failure.
    - Evaluate Platform.clear\_messages().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L5826) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L198) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L547)

<a id="op-ab80436789a2b5"></a>
### Read data file

`operation_workforce_overrides_company_business_behavior_read_data_file`

**Inputs** file\_path.

**Explicit results** f.read() · “{}”.

**Local steps**

- Attempt the following.
  - Within open(file\_path) bound as f.
    - Return f.read().
- On failure (OSError).
  - Return “{}”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L6330) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L199) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L548)

<a id="op-51885555f9ba01"></a>
### Set default hr accounts

`operation_workforce_overrides_company_business_behavior_set_default_human_resources_accounts`

**Inputs** doc, method = no value.

**Record and data access** read “Account” via get\_value.

**State and service calls** call db\_set on doc.

**Explicit results** no value.

**Local steps**

- If Platform.local.flags.ignore\_chart\_of\_accounts.
  - Return no value.
- If not doc.default\_payroll\_payable\_account.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Payroll Payable”, “company” → doc.name, “is\_group” → 0)).
  - Evaluate doc.db\_set(“default\_payroll\_payable\_account”, payroll\_payable\_account).
- If not doc.default\_employee\_advance\_account.
  - Set employe\_advance\_account from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Employee Advances”, “company” → doc.name, “is\_group” → 0)).
  - Evaluate doc.db\_set(“default\_employee\_advance\_account”, employe\_advance\_account).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L6436) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L201) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L550)

<a id="op-35603f58da5948"></a>
### Set expense claim type accounts

`operation_workforce_overrides_company_business_behavior_set_expense_claim_type_accounts`

**Inputs** doc, method = no value.

**Record and data access** read “Expense Claim Type” via get\_all · read “Expense Claim Account” via exists · resolve a document from “Expense Claim Type” via get\_doc.

**State and service calls** call save on claim\_type\_doc.

**Explicit results** no value.

**Local steps**

- If Platform.local.flags.ignore\_chart\_of\_accounts.
  - Return no value.
- Set expense\_account from no value.
- For each claim\_type in Platform.get\_all(“Expense Claim Type”, pluck = “name”).
  - If Platform.db.exists(“Expense Claim Account”, mapping(“parent” → claim\_type, “company” → doc.name)).
    - Continue with the next iteration or loop test.
  - If not expense\_account.
    - Set expense\_account from get\_or\_create\_expense\_claim\_account(doc).
    - If not expense\_account.
      - Return no value.
  - Set claim\_type\_doc from Platform.get\_doc(“Expense Claim Type”, claim\_type).
  - Evaluate claim\_type\_doc.append(“accounts”, mapping(“company” → doc.name, “default\_account” → expense\_account)).
  - Evaluate claim\_type\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L6815) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L202) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L551)

<a id="op-62cc3e4f7debaf"></a>
### Get or create expense claim account

`operation_workforce_overrides_company_business_behavior_get_or_create_expense_claim_account`

**Inputs** doc.

**Declared result** (str bitwise or no value).

**Record and data access** read “Account” via get\_value · resolve a document from mapping(“doctype” → “Account”, “account\_name” → translated “Expense Claims”, “company” → doc.name, “parent\_account” → parent\_account, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → translated “Expense Claims”, “company” → doc.name, “parent\_account” → parent\_account, …)).

**Explicit results** account · no value · Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → translated “Expense Claims”, “company” → doc.name, “parent\_account” → parent\_account, …)).insert(ignore\_permissions = true).name.

**Local steps**

- Set account from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Expense Claims”, “company” → doc.name, “is\_group” → 0)).
- If account.
  - Return account.
- Set parent\_account from (Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Indirect Expenses”, “company” → doc.name, “is\_group” → 1)) or Platform.db.get\_value(“Account”, mapping(“root\_type” → “Expense”, “compa ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Indirect Expenses”, “company” → doc.name, “is\_group” → 1)) → Platform.db.get\_value(“Account”, mapping(“root\_type” → “Expense”, “company” → doc.name, “is\_group” → 1), order\_by = “lft”).
- If not parent\_account.
  - Return no value.
- Return Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → translated “Expense Claims”, “company” → doc.name, “parent\_account” → parent\_account, …)).insert(ignore\_permissions = true).name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L194) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L543)

<a id="op-fe118240735b6d"></a>
### Validate default accounts

`operation_workforce_overrides_company_business_behavior_validate_default_accounts`

**Inputs** doc, method = no value.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Account {0} does not belong to company: {1}”.format(doc.default\_payroll\_payable\_account, doc.name) · validation helper — translated “The currency of {0} should be same as the company's default currency. Please select another account.”.format(Platform.bold(translated “Default Payroll Payable Account”)).

**Local steps**

- If doc.default\_payroll\_payable\_account.
  - Set for\_company from Platform.db.get\_value(“Account”, doc.default\_payroll\_payable\_account, “company”).
  - If for\_company differs from doc.name.
    - Call the validation error handler Platform.throw(translated “Account {0} does not belong to company: {1}”.format(doc.default\_payroll\_payable\_account, doc.name)).
  - If get\_account\_currency(doc.default\_payroll\_payable\_account) differs from doc.default\_currency.
    - Call the validation error handler Platform.throw(translated “The currency of {0} should be same as the company's default currency. Please select another account.”.format(Platform.bold(translated “Default Payroll Payable Account”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L584) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L203) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L552)

<a id="op-7dc54a3eb12a29"></a>
### Handle linked docs

`operation_workforce_overrides_company_business_behavior_handle_linked_records`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate delete\_docs\_with\_company\_field(doc).
- Evaluate clear\_company\_field\_for\_single\_doctypes(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L919) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L196) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L545)

<a id="op-08b3ba29c90744"></a>
### Delete docs with company field

`operation_workforce_overrides_company_business_behavior_delete_records_with_company_field`

**Inputs** doc, method = no value.

**Record and data access** read doctype via get\_all.

**State and service calls** request delete on doctype.

**Local steps**

- Set company\_data\_to\_be\_ignored from (Platform.get\_hooks(“company\_data\_to\_be\_ignored”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“company\_data\_to\_be\_ignored”) → list().
- For each doctype in company\_data\_to\_be\_ignored.
  - Set records\_to\_delete from Platform.get\_all(doctype, filters = mapping(“company” → doc.name), pluck = “name”).
  - If records\_to\_delete.
    - Evaluate Platform.db.delete(doctype, mapping(“name” → list(“in”, records\_to\_delete))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“company\_data\_to\_be\_ignored”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L1002) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L192) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L541)

<a id="op-db376c091230ad"></a>
### Clear company field for single doctypes

`operation_workforce_overrides_company_business_behavior_clear_company_field_for_single_record_types`

**Inputs** doc.

**Local steps**

- Set single\_docs from get\_single\_doctypes\_with\_company\_field().
- Set singles from Platform.qb.DocType(“Singles”).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.field equals “company”).where(singles.value equals doc.name).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L1245) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L190) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L539)

<a id="op-dc35a6e934088e"></a>
### Get single doctypes with company field

`operation_workforce_overrides_company_business_behavior_get_single_record_types_with_company_field`

**Inputs** no declared parameters.

**Explicit results** nested operand in the contract(nested operand in the contract).select(DocField.parent).where(((nested operand in the contract.fieldtype equals “Link” bitwise and nested operand in the contract.options equa ….

**Local steps**

- Set DocType from Platform.qb.DocType(“DocType”).
- Set DocField from Platform.qb.DocType(“DocField”).
- Return nested operand in the contract(nested operand in the contract).select(DocField.parent).where(((nested operand in the contract.fieldtype equals “Link” bitwise and nested operand in the contract.options equa ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L1503) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L195) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L544)

## Service · Dashboard overrides

<a id="op-20910bc37e8b09"></a>
### Get dashboard for employee

`operation_workforce_overrides_dashboard_overrides_business_behavior_get_dashboard_for_employee`

**Inputs** data.

**Explicit results** data.

**Local steps**

- Evaluate data at “transactions”.extend(list(mapping(“label” → translated “Attendance”, “items” → list(“Attendance”, “Attendance Request”, “Employee Checkin”)), mapping(“label” → translated “Leave”, “items” → list(“ ….
- Evaluate data at “non\_standard\_fieldnames”.update(mapping(“Bank Account” → “party”, “Contract” → “party\_name”, “Employee Grievance” → “raised\_by”, “Holiday List Assignment” → “assigned\_to”)).
- If not data.get(“dynamic\_links”).
  - Set data at “dynamic\_links” from mapping().
- Set data at “dynamic\_links” at “assigned\_to” from list(“Employee”, “applicable\_for”).
- Set data at “dynamic\_links” at “party\_name” from list(“Employee”, “party\_type”).
- Evaluate data.update(mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on the attendance of this Employee”, “fieldname” → “employee”, “method” → “Workforce.overrides.employee\_master.get\_timeline\_data”)).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L1870) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L205) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L554)

<a id="op-fe901533212412"></a>
### Get dashboard for holiday list

`operation_workforce_overrides_dashboard_overrides_business_behavior_get_dashboard_for_holiday_list`

**Inputs** data.

**Explicit results** data.

**Local steps**

- Evaluate data at “non\_standard\_fieldnames”.update(mapping(“Leave Period” → “optional\_holiday\_list”)).
- Evaluate data at “transactions”.append(mapping(“items” → list(“Leave Period”, “Shift Type”, “Holiday List Assignment”))).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L88) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L206) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L555)

<a id="op-97a6c3ee914b3d"></a>
### Get dashboard for timesheet

`operation_workforce_overrides_dashboard_overrides_business_behavior_get_dashboard_for_timesheet`

**Inputs** data.

**Explicit results** data.

**Local steps**

- Evaluate data at “transactions”.append(mapping(“label” → translated “Payroll”, “items” → list(“Salary Slip”))).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L3418) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L208) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L557)

<a id="op-405796bc200b8c"></a>
### Get dashboard for project

`operation_workforce_overrides_dashboard_overrides_business_behavior_get_dashboard_for_project`

**Inputs** data.

**Explicit results** data.

**Local steps**

- Evaluate data at “transactions”.append(mapping(“label” → translated “Claims”, “items” → list(“Expense Claim”))).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L3544) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L207) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L556)

<a id="op-1ecc9a885af3be"></a>
### Get dashboard for bank account

`operation_workforce_overrides_dashboard_overrides_business_behavior_get_dashboard_for_bank_account`

**Inputs** data.

**Explicit results** data.

**Local steps**

- For each section in data at “transactions”.
  - If section.get(“label”) equals “Transactions”.
    - Evaluate section at “items”.append(“Payroll Entry”).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L3670) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L204) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L553)

## Service · Employee master

<a id="op-a6e812e3901a7e"></a>
### Employee Master.autoname

`operation_workforce_overrides_employee_master_business_behavior_employee_master_autoname`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Please setup Employee Naming System in Human Resource &gt; HR Settings”.

**Local steps**

- Set naming\_method from Platform.db.get\_single\_value(“HR Settings”, “emp\_created\_by”).
- If not naming\_method.
  - Call the validation error handler Platform.throw(translated “Please setup Employee Naming System in Human Resource &gt; HR Settings”).
- Otherwise.
  - If naming\_method equals “Naming Series”.
    - Evaluate set\_name\_by\_naming\_series(self).
  - Otherwise.
    - If naming\_method equals “Employee Number”.
      - Set self.name from self.employee\_number.
    - Otherwise.
      - If naming\_method equals “Full Name”.
        - Evaluate self.set\_employee\_name().
        - Set self.name from self.employee\_name.
- Set self.employee from self.name.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “emp\_created\_by”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L3816) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L209) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L558)

<a id="op-cf2f8b3167c87c"></a>
### Validate onboarding process

`operation_workforce_overrides_employee_master_business_behavior_validate_onboarding_process`

**Inputs** doc, method = no value.

**Record and data access** read “Employee Onboarding” via get\_all · resolve a document from “Employee Onboarding” via get\_doc.

**State and service calls** call db\_set on onboarding.

**Explicit results** no value.

**Local steps**

- Set job\_applicant from doc.get(“job\_applicant”).
- Set job\_offer from doc.get(“job\_offer”).
- Set filters from mapping(“docstatus” → 1, “boarding\_status” → tuple(“!=”, “Completed”)).
- If job\_offer.
  - Set filters at “job\_offer” from job\_offer.
- Otherwise.
  - If job\_applicant.
    - Set filters at “job\_applicant” from job\_applicant.
  - Otherwise.
    - Return no value.
- Set employee\_onboarding from Platform.get\_all(“Employee Onboarding”, filters = filters).
- If employee\_onboarding.
  - Set onboarding from Platform.get\_doc(“Employee Onboarding”, employee\_onboarding at 0.name).
  - Evaluate onboarding.validate\_employee\_creation().
  - Evaluate onboarding.db\_set(“employee”, doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L4125) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L219) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L568)

<a id="op-3b9f345838dbb3"></a>
### Publish update

`operation_workforce_overrides_employee_master_business_behavior_publish_update`

**Inputs** doc, method = no value.

**Local steps**

- Bind dependencies Workforce.
- Evaluate Workforce.refetch\_resource(“Workforce:employee”, doc.user\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L4530) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L214) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L563)

<a id="op-13d04adc52faff"></a>
### Update job applicant and offer

`operation_workforce_overrides_employee_master_business_behavior_update_job_applicant_and_offer`

**Inputs** doc, method = no value.

**Record and data access** read “Job Applicant” via get\_value.

**State and service calls** msgprint with translated “Linked Job Offer {0} was {1}. Please update the Job Offer status if this hire was intended.”.format(get\_link\_to\_form(“Job Offer”, job\_offer.name), Platform.bold(translated job\_offer.status)) · request set\_value on “Job Applicant” · msgprint with translated “Updated the status of linked Job Applicant {0} to {1}”.format(get\_link\_to\_form(“Job Applicant”, job\_applicant), Platform.bold(translated “Accepted”)) · call save on job\_offer · msgprint with msg.

**Explicit results** no value.

**Local steps**

- Set job\_applicant from doc.get(“job\_applicant”).
- Set job\_offer from get\_linked\_job\_offer(doc, job\_applicant).
- If (job\_offer and job\_offer.status belongs to tuple(“Rejected”, “Cancelled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_offer → job\_offer.status belongs to tuple(“Rejected”, “Cancelled”).
  - Evaluate Platform.msgprint(translated “Linked Job Offer {0} was {1}. Please update the Job Offer status if this hire was intended.”.format(get\_link\_to\_form(“Job Offer”, job\_offer.name), Platform.bold(translated job ….
  - Return no value.
- If job\_applicant.
  - Set applicant\_status\_before\_change from Platform.db.get\_value(“Job Applicant”, job\_applicant, “status”).
  - If applicant\_status\_before\_change differs from “Accepted”.
    - Evaluate Platform.db.set\_value(“Job Applicant”, job\_applicant, “status”, “Accepted”).
    - Evaluate Platform.msgprint(translated “Updated the status of linked Job Applicant {0} to {1}”.format(get\_link\_to\_form(“Job Applicant”, job\_applicant), Platform.bold(translated “Accepted”))).
- If (not job\_offer or job\_offer.status equals “Accepted”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not job\_offer → job\_offer.status equals “Accepted”.
  - Return no value.
- Set job\_offer.status from “Accepted”.
- Set job\_offer.flags.ignore\_mandatory from true.
- Set job\_offer.flags.ignore\_permissions from true.
- Evaluate job\_offer.save().
- Set msg from translated “Updated the status of Job Offer {0} for {1} to {2}”.format(get\_link\_to\_form(“Job Offer”, job\_offer.name), Platform.bold(job\_offer.applicant\_name), Platform.bold(translated “Accepted”)).
- If job\_offer.docstatus equals 0.
  - Update msg using + (text in the contract + translated “You may add additional details, if any, and submit the offer.”).
- Evaluate Platform.msgprint(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0099.json#L4612) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L218) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L567)
