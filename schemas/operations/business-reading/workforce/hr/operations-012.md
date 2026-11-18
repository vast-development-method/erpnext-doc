# Employment and attendance · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Workspace · Employee profile

<a id="op-4c640f785647e5"></a>
### Get birthday

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_birthday`

**Inputs** date\_of\_birth.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“month” → day.month, “day” → day.day).

**Local steps**

- If not date\_of\_birth.
  - Return no value.
- Set day from getdate(date\_of\_birth).
- Return mapping(“month” → day.month, “day” → day.day).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L100) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L151) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L151)

<a id="op-3bea67002d034b"></a>
### Get sections

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_sections`

**Inputs** employee.

**Declared result** list at dict.

**Record and data access** read “Employee Profile Section” via get\_all.

**Explicit results** list of mapping(“type” → row.section\_type, “title” → row.title, “content” → parse\_content(row)) for row drawn from Platform.get\_all(“Employee Profile Section”, filters = mapping(“parent” → employee, “paren ….

**Local steps**

- Return list of mapping(“type” → row.section\_type, “title” → row.title, “content” → parse\_content(row)) for row drawn from Platform.get\_all(“Employee Profile Section”, filters = mapping(“parent” → employee, “paren ….
  - Draw row from Platform.get\_all(“Employee Profile Section”, filters = mapping(“parent” → employee, “parenttype” → “Employee”, “parentfield” → “profile\_sections”), fields = list(“section\_type”, “title”, “content”), order\_ ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L114) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L165) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L165)

<a id="op-8be5e367531012"></a>
### Parse content

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_parse_content`

**Inputs** row.

**Explicit results** list of tag.strip() for tag drawn from (row.content or empty text).splitlines() where tag.strip() · list() · items when isinstance(items, list), otherwise list() · (row.content or empty text).

**Local steps**

- If row.section\_type equals “Tags”.
  - Return list of tag.strip() for tag drawn from (row.content or empty text).splitlines() where tag.strip().
    - Draw tag from (row.content or empty text).splitlines(), keep a combination only if (tag.strip()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.content → empty text.
- If row.section\_type belongs to tuple(“Photos”, “Links”).
  - Attempt the following.
    - Set items from json.loads((row.content or “&#91;&#93;”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.content → “&#91;&#93;”.
  - On failure (ValueError).
    - Return list().
  - Return items when isinstance(items, list), otherwise list().
    - Value choice on isinstance(items, list) — true gives items, false gives list().
- Return (row.content or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.content → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L118) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L169) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L169)

<a id="op-fb766b65f69487"></a>
### Get private

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_private`

**Inputs** employee.

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** mapping(“personal” → pick(PERSONAL\_FIELDS), “contact” → pick(CONTACT\_FIELDS), “emergency” → pick(EMERGENCY\_FIELDS), “employment” → mapping(expand pick(list(expanded EMPLOYMENT\_FIELDS, “department”, “branch ….

**Local steps**

- Set bank\_fields from get\_bank\_fields().
- Set values from Platform.db.get\_value(“Employee”, employee, list(expanded PERSONAL\_FIELDS, expanded CONTACT\_FIELDS, expanded EMERGENCY\_FIELDS, expanded EMPLOYMENT\_FIELDS, …), as\_dict = true).
- Set pick from deferred anonymous expression.
- Set bank from pick(bank\_fields).
- Set bank at “bank\_ac\_no” from mask(bank at “bank\_ac\_no”).
- Set bank at “iban” from mask(bank at “iban”).
- Return mapping(“personal” → pick(PERSONAL\_FIELDS), “contact” → pick(CONTACT\_FIELDS), “emergency” → pick(EMERGENCY\_FIELDS), “employment” → mapping(expand pick(list(expanded EMPLOYMENT\_FIELDS, “department”, “branch ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L111) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L162) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L162)

<a id="op-476662867551fc"></a>
### Get asset requests

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_asset_requests`

**Inputs** employee.

**Declared result** list at dict.

**Record and data access** read “Asset Request” via get\_all · read “Asset Movement” via get\_all.

**Explicit results** (requests + rejected).

**Local steps**

- Set fields from list(“name”, “request\_type”, “status”, “asset\_category”, …).
- Set requests from Platform.get\_all(“Asset Request”, filters = mapping(“employee” → employee, “docstatus” → 0), fields = fields, order\_by = “creation desc”).
- Set approved from Platform.get\_all(“Asset Request”, filters = mapping(“employee” → employee, “docstatus” → 1, “status” → “Approved”), fields = fields, order\_by = “creation desc”, limit = 20).
- Set rejected from get\_rejected(“Asset Request”, employee, fields).
- If not approved.
  - Return (requests + rejected).
- Set movements from mapping().
- For each movement in Platform.get\_all(“Asset Movement”, filters = mapping(“reference\_doctype” → “Asset Request”, “reference\_name” → list(“in”, list of request.name for request drawn from approved), “docstatus” → list(“!=”, 2)) ….
  - Draw request from approved.
  - Set movements at movement.reference\_name from movement.
- For each request in approved.
  - Set movement from movements.get(request.name).
  - If (movement and movement.docstatus equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in movement → movement.docstatus equals 1.
    - Continue with the next iteration or loop test.
  - Set request.asset\_movement from movement.name when movement, otherwise no value.
    - Value choice on movement — true gives movement.name, false gives no value.
  - Evaluate requests.append(request).
- Return (requests + rejected).

**Values supplied outside this operation** service or queued work from requests.append(request).

**Boundaries to resolve** stored data, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L96) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L147) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L147)

<a id="op-0afb3540779ccf"></a>
### Get rejected

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_rejected`

**Inputs** doctype, employee, fields, limit = 20.

**Declared result** list at dict.

**Record and data access** read doctype via get\_all.

**Explicit results** Platform.get\_all(doctype, filters = mapping(“employee” → employee, “docstatus” → 1, “status” → “Rejected”, “modified” → list(“&gt;=”, add\_days(now\_datetime(), negative DECIDED\_DAYS))), fields = fields, order\_ ….

**Local steps**

- Return Platform.get\_all(doctype, filters = mapping(“employee” → employee, “docstatus” → 1, “status” → “Rejected”, “modified” → list(“&gt;=”, add\_days(now\_datetime(), negative DECIDED\_DAYS))), fields = fields, order\_ ….

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L113) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L164) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L164)

<a id="op-e81bedbf8001e7"></a>
### Get bank fields

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_bank_fields`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list(expanded BANK\_FIELDS, “ifsc\_code”) when Platform.get\_meta(“Employee”).has\_field(“ifsc\_code”), otherwise BANK\_FIELDS.

**Local steps**

- Return list(expanded BANK\_FIELDS, “ifsc\_code”) when Platform.get\_meta(“Employee”).has\_field(“ifsc\_code”), otherwise BANK\_FIELDS.
  - Value choice on Platform.get\_meta(“Employee”).has\_field(“ifsc\_code”) — true gives list(expanded BANK\_FIELDS, “ifsc\_code”), false gives BANK\_FIELDS.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L98) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L149) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L149)

<a id="op-b14c8bcb80c446"></a>
### Get open bank request

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_open_bank_request`

**Inputs** employee.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Bank Details Change Request” via get\_value.

**Explicit results** prepare\_bank\_request(request) when request, otherwise no value.

**Local steps**

- Set request from Platform.db.get\_value(“Bank Details Change Request”, mapping(“employee” → employee, “docstatus” → 0), BANK\_REQUEST\_FIELDS, as\_dict = true).
- Return prepare\_bank\_request(request) when request, otherwise no value.
  - Value choice on request — true gives prepare\_bank\_request(request), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L105) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L156) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L156)

<a id="op-a0cf4706ebb668"></a>
### Get decided bank request

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_decided_bank_request`

**Inputs** employee.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Bank Details Change Request” via exists · read “Bank Details Change Request” via get\_all.

**Explicit results** no value · request.

**Local steps**

- If Platform.db.exists(“Bank Details Change Request”, mapping(“employee” → employee, “docstatus” → 0)).
  - Return no value.
- Set decided from Platform.get\_all(“Bank Details Change Request”, filters = mapping(“employee” → employee, “docstatus” → 1, “modified” → list(“&gt;=”, add\_days(now\_datetime(), negative DECIDED\_DAYS))), fields = BANK\_REQUEST\_FI ….
- If not decided.
  - Return no value.
- Set decided\_by from get\_fullname(decided at 0.modified\_by).
- Set request from prepare\_bank\_request(decided at 0).
- Set request.decided\_by from decided\_by.
- Return request.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L102) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L153) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L153)

<a id="op-e3ab8550628102"></a>
### Prepare bank request

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_prepare_bank_request`

**Inputs** request.

**Declared result** Platform.\_dict.

**Record and data access** read “File” via get\_value.

**Explicit results** request.

**Local steps**

- Set request.bank\_ac\_no from mask(request.bank\_ac\_no).
- Set request.iban from mask(request.iban).
- Set request.proof\_name from Platform.db.get\_value(“File”, mapping(“file\_url” → request.proof, “attached\_to\_doctype” → “Bank Details Change Request”, “attached\_to\_name” → request.name), “file\_name”).
- Evaluate request.pop(“modified\_by”, no value).
- Return request.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L119) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L170) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L170)

<a id="op-aaa85e4c1db150"></a>
### Get bank number

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_bank_number`

**Inputs** employee, request = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from “Bank Details Change Request” via get\_doc · read “Employee” via get\_value.

**Explicit results** values.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “{0} is not a request of {1}”.format(request, employee) · validation helper with Platform.PermissionError — translated “Not permitted to see this bank account”.

**Local steps**

- If request.
  - Set doc from Platform.get\_doc(“Bank Details Change Request”, request).
  - Evaluate doc.check\_permission(“read”).
  - If doc.employee differs from employee.
    - Call the validation error handler Platform.throw(translated “{0} is not a request of {1}”.format(request, employee), Platform.PermissionError).
  - Set values from mapping(“bank\_ac\_no” → doc.bank\_ac\_no, “iban” → doc.iban).
  - Evaluate make\_access\_log(doctype = doc.doctype, document = doc.name, method = “get\_bank\_number”).
- Otherwise.
  - If not Platform.has\_permission(“Employee”, “read”, doc = employee).
    - Call the validation error handler Platform.throw(translated “Not permitted to see this bank account”, Platform.PermissionError).
  - Set values from Platform.db.get\_value(“Employee”, employee, list(“bank\_ac\_no”, “iban”), as\_dict = true).
  - Evaluate make\_access\_log(doctype = “Employee”, document = employee, method = “get\_bank\_number”).
- Return values.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”), Platform.has\_permission(“Employee”, “read”, doc = employee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L99) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L150) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L150)

<a id="op-fc22e8fc286f8d"></a>
### Get assets

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_assets`

**Inputs** employee.

**Declared result** list at dict.

**Record and data access** read “Asset” via get\_all.

**Explicit results** list() · sorted(assets, key = deferred anonymous expression, reverse = true).

**Local steps**

- Set assets from Platform.get\_all(“Asset”, filters = mapping(“custodian” → employee, “docstatus” → 1), fields = list(“name”, “asset\_name”, “item\_name”, “asset\_category”), limit = 50).
- If not assets.
  - Return list().
- Set movement from Platform.qb.DocType(“Asset Movement”).
- Set item from Platform.qb.DocType(“Asset Movement Item”).
- Set since from dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(item.asset).run()).
  - Draw asset from assets.
- For each asset in assets.
  - Set asset.since from since.get(asset.name).
- Return sorted(assets, key = deferred anonymous expression, reverse = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L97) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L148) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L148)

<a id="op-acb9293aac5f7b"></a>
### Get documents

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_documents`

**Inputs** employee.

**Declared result** list at dict.

**Record and data access** read “Employee Document Type” via get\_all · read “Employee Document” via get\_all.

**Explicit results** documents.

**Local steps**

- Set types from mapping of document.name → document for document drawn from Platform.get\_all(“Employee Document Type”, fields = list(“name”, “is\_required”, “has\_number”, “has\_expiry”)).
  - Draw document from Platform.get\_all(“Employee Document Type”, fields = list(“name”, “is\_required”, “has\_number”, “has\_expiry”)).
- Set documents from Platform.get\_all(“Employee Document”, filters = mapping(“parent” → employee, “parenttype” → “Employee”, “parentfield” → “documents”), fields = list(“document\_type”, “attachment”, “document\_number”, “expiry ….
- Set given from set of document.document\_type for document drawn from documents.
  - Draw document from documents.
- Update documents using + list of mapping(“document\_type” → name, “status” → “Missing”) for tuple(name, document) drawn from types.items() where (document.is\_required and name does not belong to given).
  - Draw tuple(name, document) from types.items(), keep a combination only if ((document.is\_required and name does not belong to given)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in document.is\_required → name does not belong to given.
- For each document in documents.
  - Set kind from (types.get(document at “document\_type”) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in types.get(document at “document\_type”) → mapping().
  - Set document at “has\_number” from kind.get(“has\_number”).
  - Set document at “has\_expiry” from kind.get(“has\_expiry”).
- Return documents.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L104) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L155) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L155)

<a id="op-684d6d54204060"></a>
### Mask

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_mask`

**Inputs** number.

**Declared result** (str bitwise or no value).

**Explicit results** formatted text ••••{number at slice negative 4 to no value} when number, otherwise no value.

**Local steps**

- Return formatted text ••••{number at slice negative 4 to no value} when number, otherwise no value.
  - Value choice on number — true gives formatted text ••••{number at slice negative 4 to no value}, false gives no value.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L117) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L168) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L168)

<a id="op-687deba1d65c15"></a>
### Get user employee

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_user_employee`

**Inputs** no declared parameters.

**Declared result** (str bitwise or no value).

**Record and data access** read “Employee” via get\_value.

**Explicit results** Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user, “status” → “Active”), “name”).

**Local steps**

- Return Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user, “status” → “Active”), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L116) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L167) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L167)

<a id="op-0ac835c19669c4"></a>
### Get own employee

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_own_employee`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** employee.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have an employee record”.

**Local steps**

- Set employee from get\_user\_employee().
- If not employee.
  - Call the validation error handler Platform.throw(translated “You do not have an employee record”, Platform.PermissionError).
- Return employee.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L107) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L158) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L158)

<a id="op-476f9e67dfdf7c"></a>
### Can manage employee

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_can_manage_employee`

**Inputs** employee.

**Declared result** bool.

**Explicit results** can\_manage.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have an employee record” · validation helper with Platform.PermissionError — translated “You cannot change this employee's details”.

**Local steps**

- If not employee.
  - Call the validation error handler Platform.throw(translated “You do not have an employee record”, Platform.PermissionError).
- Set can\_manage from Platform.has\_permission(“Employee”, “write”, doc = employee).
- If (not can\_manage and employee differs from get\_user\_employee()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not can\_manage → employee differs from get\_user\_employee().
  - Call the validation error handler Platform.throw(translated “You cannot change this employee's details”, Platform.PermissionError).
- Return can\_manage.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “write”, doc = employee).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L90) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L141) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L141)

<a id="op-d24055ddae6255"></a>
### Save details

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_save_details`

**Inputs** values, employee = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** mapping(“private” → get\_private(employee), “card” → get\_card(get\_person(employee), true)).

**Explicit failure paths** validation helper — translated “Details must be a set of fields” · validation helper — translated “You cannot change {0} here”.format(“, ”.join(sorted(unknown))) · validation helper — translated “You cannot change {0} here”.format(field).

**Local steps**

- Set employee from (employee or get\_user\_employee()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee → get\_user\_employee().
- Set can\_manage from can\_manage\_employee(employee).
- Set values from Platform.parse\_json(values).
- If not isinstance(values, dict).
  - Call the validation error handler Platform.throw(translated “Details must be a set of fields”).
- Set unknown from (set(values) − set((SELF\_EDITABLE + HR\_EDITABLE) when can\_manage, otherwise SELF\_EDITABLE)).
  - Value choice on can\_manage — true gives (SELF\_EDITABLE + HR\_EDITABLE), false gives SELF\_EDITABLE.
- If unknown.
  - Call the validation error handler Platform.throw(translated “You cannot change {0} here”.format(“, ”.join(sorted(unknown)))).
- Set doc from Platform.get\_doc(“Employee”, employee).
- Set meta from Platform.get\_meta(“Employee”).
- For each tuple(field, value) in values.items().
  - Set df from meta.get\_field(field).
  - If not df.
    - Call the validation error handler Platform.throw(translated “You cannot change {0} here”.format(field)).
  - Evaluate doc.set(field, clean\_value(doc, df, value)).
- If values.get(“bank\_ac\_no”).
  - Set doc.salary\_mode from “Bank”.
- If can\_manage.
  - Evaluate doc.save().
- Otherwise.
  - Evaluate doc.save(ignore\_permissions = true).
- Return mapping(“private” → get\_private(employee), “card” → get\_card(get\_person(employee), true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L126) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L177) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L177)

<a id="op-3be9b8d7dc9bd2"></a>
### Clean value

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_clean_value`

**Inputs** doc, df, value.

**Record and data access** read df.options via exists · read “Department” via get\_value.

**Explicit results** 0 when df.fieldtype equals “Int”, otherwise no value · cint(value) · value.

**Explicit failure paths** validation helper — translated “{0} is not a valid {1}”.format(Platform.bold(value), translated df.label) · validation helper — translated “Department {0} is not in {1}”.format(Platform.bold(value), Platform.bold(doc.company)) · validation helper — translated “{0} must have 7 to 15 digits”.format(translated df.label) · validation helper — translated “{0} must be a whole number”.format(translated df.label).

**Local steps**

- Set value from (str((value or empty text)).strip() at slice no value to MAX\_TEXT or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((value or empty text)).strip() at slice no value to MAX\_TEXT → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
- If not value.
  - Return 0 when df.fieldtype equals “Int”, otherwise no value.
    - Value choice on df.fieldtype equals “Int” — true gives 0, false gives no value.
- If (df.fieldtype equals “Select” and value does not belong to (df.options or empty text).split(whitespace '\\n')).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Select” → value does not belong to (df.options or empty text).split(whitespace '\\n').
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.options → empty text.
  - Call the validation error handler Platform.throw(translated “{0} is not a valid {1}”.format(Platform.bold(value), translated df.label)).
- If (df.fieldtype equals “Link” and not Platform.db.exists(df.options, value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Link” → not Platform.db.exists(df.options, value).
  - Call the validation error handler Platform.throw(translated “{0} is not a valid {1}”.format(Platform.bold(value), translated df.label)).
- If (df.fieldname equals “department” and Platform.db.get\_value(“Department”, value, “company”) differs from doc.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldname equals “department” → Platform.db.get\_value(“Department”, value, “company”) differs from doc.company.
  - Call the validation error handler Platform.throw(translated “Department {0} is not in {1}”.format(Platform.bold(value), Platform.bold(doc.company))).
- If df.fieldname equals “personal\_email”.
  - Evaluate validate\_email\_address(value, throw = true).
- If df.fieldname belongs to PHONE\_FIELDS.
  - Evaluate validate\_phone\_number(value, throw = true).
  - If not 7 ≤ len(re.sub(“\\D”, empty text, value)) ≤ 15.
    - Compare adjacent operands in order, stopping at the first false comparison in 7 ≤ len(re.sub(“\\D”, empty text, value)) ≤ 15.
    - Call the validation error handler Platform.throw(translated “{0} must have 7 to 15 digits”.format(translated df.label)).
- If df.fieldtype equals “Int”.
  - If not value.isdigit().
    - Call the validation error handler Platform.throw(translated “{0} must be a whole number”.format(translated df.label)).
  - Return cint(value).
- If df.fieldtype equals “Date”.
  - Set value from getdate(value).
- If df.fieldname equals “date\_of\_birth”.
  - Set doc.date\_of\_retirement from get\_retirement\_date(str(value)).
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L95) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L146) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L146)

<a id="op-ed23f58f25fe7b"></a>
### Save sections

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_save_sections`

**Inputs** sections.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at dict.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_sections(employee).

**Explicit failure paths** validation helper — translated “Profile sections must be a list” · validation helper — translated “A profile can have at most {0} sections”.format(MAX\_SECTIONS).

**Local steps**

- Set employee from get\_own\_employee().
- Set sections from Platform.parse\_json(sections).
- If not isinstance(sections, list).
  - Call the validation error handler Platform.throw(translated “Profile sections must be a list”).
- Set rows from list of clean\_section(section, employee) for section drawn from sections at slice no value to (MAX\_SECTIONS + 1).
  - Draw section from sections at slice no value to (MAX\_SECTIONS + 1).
- If len(rows) &gt; MAX\_SECTIONS.
  - Call the validation error handler Platform.throw(translated “A profile can have at most {0} sections”.format(MAX\_SECTIONS)).
- Set doc from Platform.get\_doc(“Employee”, employee).
- Evaluate doc.set(“profile\_sections”, rows).
- Evaluate doc.save(ignore\_permissions = true).
- Return get\_sections(employee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L127) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L178) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L178)

<a id="op-9c08d8298c74a7"></a>
### Clean section

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_clean_section`

**Inputs** section, employee.

**Declared result** dict.

**Explicit results** mapping(“section\_type” → kind, “title” → title, “content” → content).

**Explicit failure paths** validation helper — translated “Unknown profile section”.

**Local steps**

- If (not isinstance(section, dict) or section.get(“type”) does not belong to SECTION\_TYPES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(section, dict) → section.get(“type”) does not belong to SECTION\_TYPES.
  - Call the validation error handler Platform.throw(translated “Unknown profile section”).
- Set kind from section at “type”.
- Set title from str((section.get(“title”) or empty text)) at slice no value to MAX\_TITLE.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“title”) → empty text.
- Set content from section.get(“content”).
- If kind equals “Cover”.
  - Set content from clean\_photo(mapping(“image” → content), employee) at “image”.
- Otherwise.
  - If kind belongs to tuple(“Headline”, “Text”).
    - Set content from str((content or empty text)) at slice no value to MAX\_TEXT.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → empty text.
  - Otherwise.
    - If kind equals “Tags”.
      - Set tags from list of str(tag).strip() at slice no value to 60 for tag drawn from (content or list()) where str(tag).strip().
        - Draw tag from (content or list()), keep a combination only if (str(tag).strip()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → list().
      - Set content from whitespace '\\n'.join(tags at slice no value to 30).
    - Otherwise.
      - If kind equals “Links”.
        - Set content from json.dumps(list of clean\_link(item) for item drawn from (content or list()) at slice no value to MAX\_ITEMS).
          - Draw item from (content or list()) at slice no value to MAX\_ITEMS.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → list().
      - Otherwise.
        - Set content from json.dumps(list of clean\_photo(item, employee) for item drawn from (content or list()) at slice no value to MAX\_ITEMS).
          - Draw item from (content or list()) at slice no value to MAX\_ITEMS.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → list().
- Return mapping(“section\_type” → kind, “title” → title, “content” → content).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L94) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L145) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L145)

<a id="op-a088628d4b3353"></a>
### Clean link

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_clean_link`

**Inputs** item.

**Declared result** dict.

**Explicit results** mapping(“title” → str((item.get(“title”) or url)) at slice no value to MAX\_TITLE, “url” → url at slice no value to 1000, “note” → str((item.get(“note”) or empty text)) at slice no value to MAX\_TITLE).

**Explicit failure paths** validation helper — translated text in the contract.

**Local steps**

- Set url from str(((nested operand in the contract or nested operand in the contract).get(“url”) or empty text)).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item or mapping()).get(“url”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item → mapping().
- If urlparse(url).scheme does not belong to tuple(“http”, “https”).
  - Call the validation error handler Platform.throw(translated text in the contract).
- Return mapping(“title” → str((item.get(“title”) or url)) at slice no value to MAX\_TITLE, “url” → url at slice no value to 1000, “note” → str((item.get(“note”) or empty text)) at slice no value to MAX\_TITLE).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“title”) → url.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“note”) → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L92) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L143) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L143)

<a id="op-168f14aa11d0cd"></a>
### Clean photo

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_clean_photo`

**Inputs** item, employee.

**Declared result** dict.

**Record and data access** read “File” via exists.

**Explicit results** mapping(“image” → image, “caption” → str((item.get(“caption”) or empty text)) at slice no value to MAX\_TITLE).

**Local steps**

- Set image from str(((item or mapping()).get(“image”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item or mapping()).get(“image”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item → mapping().
- If not Platform.db.exists(“File”, mapping(“file\_url” → image, “attached\_to\_doctype” → “Employee”, “attached\_to\_name” → employee)).
  - Evaluate attach\_file(get\_own\_upload(image), “Employee”, employee).
- Return mapping(“image” → image, “caption” → str((item.get(“caption”) or empty text)) at slice no value to MAX\_TITLE).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“caption”) → empty text.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L93) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L144) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L144)

<a id="op-6c32564251cacf"></a>
### Get own upload

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_own_upload`

**Inputs** file\_url.

**Declared result** str.

**Record and data access** read “File” via get\_value.

**Explicit results** file.

**Explicit failure paths** validation helper — translated “Files must be uploaded from your profile”.

**Local steps**

- Set file from Platform.db.get\_value(“File”, mapping(“file\_url” → str((file\_url or empty text)), “owner” → Platform.session.user, “attached\_to\_doctype” → list(“is”, “not set”), “is\_folder” → 0), “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in file\_url → empty text.
- If not file.
  - Call the validation error handler Platform.throw(translated “Files must be uploaded from your profile”).
- Return file.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L109) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L160) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L160)
