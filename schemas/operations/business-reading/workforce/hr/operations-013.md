# Employment and attendance · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Workspace · Employee profile

<a id="op-dca0796827ca4d"></a>
### Attach file

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_attach_file`

**Inputs** file, doctype, name, field = no value.

**State and service calls** request set\_value on “File”.

**Local steps**

- Evaluate Platform.db.set\_value(“File”, file, mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → name, “attached\_to\_field” → field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L89) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L140) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L140)

<a id="op-ba6d0a638366d9"></a>
### Request bank details change

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_request_bank_details_change`

**Inputs** values, name = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from mapping(“doctype” → “Bank Details Change Request”, “employee” → employee) via get\_doc.

**State and service calls** call save on request.

**Explicit results** get\_private(employee).

**Explicit failure paths** validation helper — translated “Bank details must be a set of fields”.

**Local steps**

- Set employee from get\_own\_employee().
- Set values from Platform.parse\_json(values).
- If not isinstance(values, dict).
  - Call the validation error handler Platform.throw(translated “Bank details must be a set of fields”).
- If name.
  - Set request from get\_own\_open\_request(“Bank Details Change Request”, name, employee).
- Otherwise.
  - Set request from Platform.get\_doc(mapping(“doctype” → “Bank Details Change Request”, “employee” → employee)).
- For each field in tuple(“bank\_name”, “bank\_ac\_no”, “ifsc\_code”, “iban”).
  - Set value from (str((nested operand in the contract(nested operand in the contract) or empty text)).strip() at slice no value to MAX\_TITLE or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((nested operand in the contract.get(field) or empty text)).strip() at slice no value to MAX\_TITLE → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.get(field) → empty text.
  - If (value or not name or field does not belong to tuple(“bank\_ac\_no”, “iban”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → not name → field does not belong to tuple(“bank\_ac\_no”, “iban”).
    - Evaluate request.set(field, value).
- Set request.reason from (str((nested operand in the contract(nested operand in the contract) or empty text)).strip() at slice no value to MAX\_TEXT or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((nested operand in the contract.get(“reason”) or empty text)).strip() at slice no value to MAX\_TEXT → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.get(“reason”) → empty text.
- Set proof from no value.
- If (not name or values.get(“proof”) differs from request.proof).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → values.get(“proof”) differs from request.proof.
  - Set proof from get\_own\_upload(values.get(“proof”)).
  - Set request.proof from values.get(“proof”).
- Evaluate request.save().
- If proof.
  - Evaluate attach\_file(proof, request.doctype, request.name, “proof”).
- Return get\_private(employee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L122) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L173) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L173)

<a id="op-e64932a5b24596"></a>
### Request asset

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_request_asset`

**Inputs** values, name = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from mapping(“doctype” → “Asset Request”, “employee” → employee, “request\_type” → values at “request\_type”, “asset” → no value when is\_issue, otherwise (str((nested operand in the contract.get(“asset”) or empty … via get\_doc.

**State and service calls** call save on request.

**Explicit results** get\_private(employee).

**Explicit failure paths** validation helper — translated “Asset request must be a set of fields” · validation helper — translated “Choose whether to request or return an asset”.

**Local steps**

- Set employee from get\_own\_employee().
- Set values from Platform.parse\_json(values).
- If not isinstance(values, dict).
  - Call the validation error handler Platform.throw(translated “Asset request must be a set of fields”).
- If name.
  - Set request from get\_own\_open\_request(“Asset Request”, name, employee).
- Otherwise.
  - If values.get(“request\_type”) belongs to tuple(“Issue”, “Return”).
    - Set is\_issue from values at “request\_type” equals “Issue”.
    - Set request from Platform.get\_doc(mapping(“doctype” → “Asset Request”, “employee” → employee, “request\_type” → values at “request\_type”, “asset” → no value when is\_issue, otherwise (str((nested operand in the contract(nest ….
      - Value choice on is\_issue — true gives no value, false gives (str((values.get(“asset”) or empty text)) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((values.get(“asset”) or empty text)) → no value.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.get(“asset”) → empty text.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Choose whether to request or return an asset”).
- If request.request\_type equals “Issue”.
  - Set request.asset\_category from (str((values.get(“asset\_category”) or empty text)) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((values.get(“asset\_category”) or empty text)) → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.get(“asset\_category”) → empty text.
  - Set request.required\_by from getdate(values at “required\_by”) when values.get(“required\_by”), otherwise no value.
    - Value choice on values.get(“required\_by”) — true gives getdate(values at “required\_by”), false gives no value.
- Set request.reason from (str((nested operand in the contract(nested operand in the contract) or empty text)).strip() at slice no value to MAX\_TEXT or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((nested operand in the contract.get(“reason”) or empty text)).strip() at slice no value to MAX\_TEXT → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.get(“reason”) → empty text.
- Evaluate request.save().
- Return get\_private(employee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L121) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L172) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L172)

<a id="op-ef4543b9b3e31f"></a>
### Withdraw request

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_withdraw_request`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** get\_private(employee).

**Explicit failure paths** validation helper — translated “Only bank details and asset requests can be withdrawn here”.

**Local steps**

- If doctype does not belong to REQUESTS.
  - Call the validation error handler Platform.throw(translated “Only bank details and asset requests can be withdrawn here”).
- Set employee from get\_own\_employee().
- Evaluate get\_own\_open\_request(doctype, name, employee).discard().
- Return get\_private(employee).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L129) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L180) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L180)

<a id="op-30a2f807901068"></a>
### Get own open request

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_own_open_request`

**Inputs** doctype, name, employee.

**Declared result** Document.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** request.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Only your own open requests can be changed”.

**Local steps**

- Set request from Platform.get\_doc(doctype, name).
- If (request.employee differs from employee or not request.docstatus.is\_draft() or request.status differs from “Open”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.employee differs from employee → not request.docstatus.is\_draft() → request.status differs from “Open”.
  - Call the validation error handler Platform.throw(translated “Only your own open requests can be changed”, Platform.PermissionError).
- Return request.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L108) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L159) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L159)

<a id="op-a23e34bfa0dade"></a>
### Review request

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_review_request`

**Inputs** doctype, name, status, reason = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call submit on request.

**Explicit results** get\_private(request.employee).

**Explicit failure paths** validation helper — translated “Only bank details and asset requests can be approved or rejected here” · validation helper — translated “{0} is no longer open”.format(Platform.bold(request.name)) · validation helper with Platform.PermissionError — translated “You cannot approve or reject your own request” · validation helper — translated “Say why the request is rejected, so {0} knows”.format(request.employee\_name).

**Local steps**

- If (doctype does not belong to REQUESTS or status does not belong to tuple(“Approved”, “Rejected”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype does not belong to REQUESTS → status does not belong to tuple(“Approved”, “Rejected”).
  - Call the validation error handler Platform.throw(translated “Only bank details and asset requests can be approved or rejected here”).
- Set request from Platform.get\_doc(doctype, name).
- Evaluate request.check\_permission(“submit”).
- If (request.docstatus differs from 0 or request.status differs from “Open”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.docstatus differs from 0 → request.status differs from “Open”.
  - Call the validation error handler Platform.throw(translated “{0} is no longer open”.format(Platform.bold(request.name)), title = translated “Request Closed”).
- If request.employee equals get\_user\_employee().
  - Call the validation error handler Platform.throw(translated “You cannot approve or reject your own request”, Platform.PermissionError).
- Set request.status from status.
- If status equals “Rejected”.
  - Set request.rejection\_reason from (str((reason or empty text)).strip() at slice no value to MAX\_TEXT or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((reason or empty text)).strip() at slice no value to MAX\_TEXT → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reason → empty text.
  - If not request.rejection\_reason.
    - Call the validation error handler Platform.throw(translated “Say why the request is rejected, so {0} knows”.format(request.employee\_name)).
- Evaluate request.submit().
- Return get\_private(request.employee).

**Values supplied outside this operation** effective access from request.check\_permission(“submit”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L125) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L176) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L176)

<a id="op-81b3cf23fca623"></a>
### Upload document

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_upload_document`

**Inputs** document\_type, file\_url, document\_number = no value, expiry\_date = no value, employee = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from “Employee Document Type” via get\_cached\_doc · resolve a document from “Employee” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_private(employee).

**Local steps**

- Set employee from (employee or get\_user\_employee()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee → get\_user\_employee().
- Set can\_manage from can\_manage\_employee(employee).
- Set document from Platform.get\_cached\_doc(“Employee Document Type”, document\_type).
- Set file from get\_own\_upload(file\_url).
- Set doc from Platform.get\_doc(“Employee”, employee).
- Set row from (get\_document\_row(doc, document.name) or doc.append(“documents”, mapping(“document\_type” → document.name))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_document\_row(doc, document.name) → doc.append(“documents”, mapping(“document\_type” → document.name)).
- Set row.attachment from file\_url.
- Set row.document\_number from (str((nested operand in the contract or nested operand in the contract)).strip() at slice no value to MAX\_TITLE or no value) when document.has\_number, otherwise no value.
  - Value choice on document.has\_number — true gives (str((document\_number or empty text)).strip() at slice no value to MAX\_TITLE or no value), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((document\_number or empty text)).strip() at slice no value to MAX\_TITLE → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in document\_number → empty text.
- Set row.expiry\_date from getdate(expiry\_date) when (expiry\_date and document.has\_expiry), otherwise no value.
  - Value choice on (expiry\_date and document.has\_expiry) — true gives getdate(expiry\_date), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expiry\_date → document.has\_expiry.
- Set row.status from “Verified” when (can\_manage and employee differs from get\_user\_employee()), otherwise “Submitted”.
  - Value choice on (can\_manage and employee differs from get\_user\_employee()) — true gives “Verified”, false gives “Submitted”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_manage → employee differs from get\_user\_employee().
- If row.status equals “Verified”.
  - Set row.verified\_on from today().
- Set row.remarks from no value.
- If can\_manage.
  - Evaluate doc.save().
- Otherwise.
  - Evaluate doc.save(ignore\_permissions = true).
- Evaluate attach\_file(file, “Employee”, employee, “documents”).
- Return get\_private(employee).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Employee Document Type”, document\_type) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L128) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L179) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L179)

<a id="op-c69b0586e28a08"></a>
### Review document

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_review_document`

**Inputs** employee, document\_type, status, remarks = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_private(employee).

**Explicit failure paths** validation helper — translated “A document can only be verified or rejected” · validation helper with Platform.PermissionError — translated “You cannot verify your own documents” · validation helper — translated “{0} has not uploaded {1}”.format(Platform.bold(doc.employee\_name), Platform.bold(document\_type)).

**Local steps**

- If status does not belong to tuple(“Verified”, “Rejected”).
  - Call the validation error handler Platform.throw(translated “A document can only be verified or rejected”).
- Set doc from Platform.get\_doc(“Employee”, employee).
- Evaluate doc.check\_permission(“write”).
- If employee equals get\_user\_employee().
  - Call the validation error handler Platform.throw(translated “You cannot verify your own documents”, Platform.PermissionError).
- Set row from get\_document\_row(doc, document\_type).
- If (not row or not row.attachment).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row → not row.attachment.
  - Call the validation error handler Platform.throw(translated “{0} has not uploaded {1}”.format(Platform.bold(doc.employee\_name), Platform.bold(document\_type))).
- Set row.status from status.
- If status equals “Verified”.
  - Set row.verified\_on from today().
- Set row.remarks from (str((remarks or empty text)).strip() at slice no value to MAX\_TEXT or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in str((remarks or empty text)).strip() at slice no value to MAX\_TEXT → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in remarks → empty text.
- Evaluate doc.save().
- Return get\_private(employee).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L124) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L175) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L175)

<a id="op-1fd03121f62e64"></a>
### Request document

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_request_document`

**Inputs** employee, document\_type, due\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from “Employee” via get\_doc · resolve a document from “Employee Document Type” via get\_cached\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_private(employee).

**Local steps**

- Set doc from Platform.get\_doc(“Employee”, employee).
- Evaluate doc.check\_permission(“write”).
- Set document from Platform.get\_cached\_doc(“Employee Document Type”, document\_type).
- Set row from (get\_document\_row(doc, document.name) or doc.append(“documents”, mapping(“document\_type” → document.name))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_document\_row(doc, document.name) → doc.append(“documents”, mapping(“document\_type” → document.name)).
- Set row.status from “Pending”.
- Set row.due\_date from getdate(due\_date) when due\_date, otherwise no value.
  - Value choice on due\_date — true gives getdate(due\_date), false gives no value.
- Set row.remarks from no value.
- Evaluate doc.save().
- Return get\_private(employee).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”) · configured or stored value from Platform.get\_cached\_doc(“Employee Document Type”, document\_type).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L123) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L174) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L174)

<a id="op-73d41d30f626f2"></a>
### Remove document

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_remove_document`

**Inputs** document\_type, employee = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_private(employee).

**Explicit failure paths** validation helper — translated “{0} is not on the record”.format(Platform.bold(document\_type)) · validation helper with Platform.PermissionError — translated “HR has verified {0}. Ask HR to remove it.”.format(Platform.bold(document\_type)).

**Local steps**

- Set own from get\_user\_employee().
- Set employee from (employee or get\_own\_employee()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee → get\_own\_employee().
- Set doc from Platform.get\_doc(“Employee”, employee).
- If employee differs from own.
  - Evaluate doc.check\_permission(“write”).
- Set row from get\_document\_row(doc, document\_type).
- If not row.
  - Call the validation error handler Platform.throw(translated “{0} is not on the record”.format(Platform.bold(document\_type))).
- If employee differs from own.
  - Evaluate doc.remove(row).
  - Evaluate doc.save().
  - Return get\_private(employee).
- If (row.status does not belong to tuple(“Submitted”, “Rejected”) or row.verified\_on).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.status does not belong to tuple(“Submitted”, “Rejected”) → row.verified\_on.
  - Call the validation error handler Platform.throw(translated “HR has verified {0}. Ask HR to remove it.”.format(Platform.bold(document\_type)), Platform.PermissionError).
- If row.due\_date.
  - Evaluate row.update(mapping(“attachment” → no value, “document\_number” → no value, “expiry\_date” → no value, “status” → “Pending”, …)).
- Otherwise.
  - Evaluate doc.remove(row).
- Evaluate doc.save(ignore\_permissions = true).
- Return get\_private(employee).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L120) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L171) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L171)

<a id="op-454a60a6fda865"></a>
### Get document row

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_document_row`

**Inputs** doc, document\_type.

**Explicit results** next(generator of row for row drawn from doc.documents where row.document\_type equals document\_type, no value).

**Local steps**

- Return next(generator of row for row drawn from doc.documents where row.document\_type equals document\_type, no value).
  - Draw row from doc.documents, keep a combination only if (row.document\_type equals document\_type).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L103) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L154) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L154)

## Record · Employee promotion

[Record definition](../../../../data/record-types/employee_promotion.json)

<a id="op-f2aa35d9b631c0"></a>
### Employee Promotion.validate

`operation_workforce_human_resources_record_definitions_employee_promotion_business_behavior_employee_promotion_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L6587) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L636) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L616)

<a id="op-c5c10a5df66b7a"></a>
### Employee Promotion.before submit

`operation_workforce_human_resources_record_definitions_employee_promotion_business_behavior_employee_promotion_before_submit`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.DocstatusTransitionError — translated “Employee Promotion cannot be submitted before Promotion Date”.

**Local steps**

- If getdate(self.promotion\_date) &gt; getdate().
  - Call the validation error handler Platform.throw(translated “Employee Promotion cannot be submitted before Promotion Date”, Platform.DocstatusTransitionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L6643) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L633) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L613)

<a id="op-64fa551e2f3300"></a>
### Employee Promotion.on submit

`operation_workforce_human_resources_record_definitions_employee_promotion_business_behavior_employee_promotion_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on employee.

**Local steps**

- Set employee from Platform.get\_doc(“Employee”, self.employee).
- Set employee from update\_employee\_work\_history(employee, self.promotion\_details, date = self.promotion\_date).
- If self.revised\_ctc.
  - Set employee.ctc from self.revised\_ctc.
- Evaluate employee.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L6769) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L635) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L615)

<a id="op-cb26e654722541"></a>
### Employee Promotion.on cancel

`operation_workforce_human_resources_record_definitions_employee_promotion_business_behavior_employee_promotion_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on employee.

**Local steps**

- Set employee from Platform.get\_doc(“Employee”, self.employee).
- Set employee from update\_employee\_work\_history(employee, self.promotion\_details, cancel = true).
- If self.revised\_ctc.
  - Set employee.ctc from self.current\_ctc.
- Evaluate employee.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L6952) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L634) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L614)

## Record · Employee referral

[Record definition](../../../../data/record-types/employee_referral.json)

<a id="op-4c548ec17da500"></a>
### Employee Referral.validate

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_employee_referral_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.referrer).
- Evaluate self.validate\_unique\_referral().
- Evaluate self.set\_full\_name().
- Evaluate self.set\_status().
- Evaluate self.set\_referral\_bonus\_payment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate unique referral](operations-013.md#op-20e909fb2591b1), [set full name](operations-013.md#op-6551c2e7053cfc), [set status](operations-013.md#op-4ca8fbc5a7b496), [set referral bonus payment status](operations-013.md#op-116540fa3dd390).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1115) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L645) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L625)

<a id="op-20e909fb2591b1"></a>
### Employee Referral.validate unique referral

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_employee_referral_validate_unique_referral`

**Inputs** self.

**Record and data access** read “Employee Referral” via exists.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “Employee Referral {0} already exists for email: {1}”.format(get\_link\_to\_form(“Employee Referral”, referral), Platform.bold(self.email)).

**Local steps**

- If referral bound to Platform.db.exists(“Employee Referral”, mapping(“name” → tuple(“!=”, self.name), “email” → self.email, “docstatus” → tuple(“!=”, 2))).
  - Call the validation error handler Platform.throw(translated “Employee Referral {0} already exists for email: {1}”.format(get\_link\_to\_form(“Employee Referral”, referral), Platform.bold(self.email)), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1251) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L646) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L626)

<a id="op-6551c2e7053cfc"></a>
### Employee Referral.set full name

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_employee_referral_set_full_name`

**Inputs** self.

**Local steps**

- Set self.full\_name from one space.join(filter(no value, list(self.first\_name, self.last\_name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1518) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L642) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L622)

<a id="op-4ca8fbc5a7b496"></a>
### Employee Referral.set status

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_employee_referral_set_status`

**Inputs** self.

**Local steps**

- Set self.status from “Pending”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1614) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L644) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L624)

<a id="op-116540fa3dd390"></a>
### Employee Referral.set referral bonus payment status

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_employee_referral_set_referral_bonus_payment_status`

**Inputs** self.

**Local steps**

- If not self.is\_applicable\_for\_referral\_bonus.
  - Set self.referral\_payment\_status from empty text.
- Otherwise.
  - If not self.referral\_payment\_status.
    - Set self.referral\_payment\_status from “Unpaid”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1661) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L643) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L623)

<a id="op-fa45a4167e6949"></a>
### Employee Referral.on discard

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_employee_referral_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1762) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L641) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L621)

<a id="op-a2d300dd7e79dc"></a>
### Create job applicant

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_create_job_applicant`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** Document.

**Record and data access** resolve a document from “Employee Referral” via get\_doc.

**State and service calls** request new\_doc for “Job Applicant” · call save on job\_applicant · msgprint with translated “Job Applicant {0} created successfully.”.format(get\_link\_to\_form(“Job Applicant”, job\_applicant.name)) · call db\_set on emp\_ref.

**Explicit results** job\_applicant.

**Local steps**

- Set emp\_ref from Platform.get\_doc(“Employee Referral”, source\_name).
- Set status from emp\_ref.status.
- If emp\_ref.status belongs to list(“Pending”, “In process”).
  - Set status from “Open”.
- Set job\_applicant from Platform.new\_doc(“Job Applicant”).
- Set job\_applicant.source from “Employee Referral”.
- Set job\_applicant.employee\_referral from emp\_ref.name.
- Set job\_applicant.status from status.
- Set job\_applicant.designation from emp\_ref.for\_designation.
- Set job\_applicant.applicant\_name from emp\_ref.full\_name.
- Set job\_applicant.email\_id from emp\_ref.email.
- Set job\_applicant.phone\_number from emp\_ref.contact\_no.
- Set job\_applicant.resume\_attachment from emp\_ref.resume.
- Set job\_applicant.resume\_link from emp\_ref.resume\_link.
- Evaluate job\_applicant.save().
- Evaluate Platform.msgprint(translated “Job Applicant {0} created successfully.”.format(get\_link\_to\_form(“Job Applicant”, job\_applicant.name)), title = translated “Success”, indicator = “green”).
- Evaluate emp\_ref.db\_set(“status”, “In Process”).
- Return job\_applicant.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L1825) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L640) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L620)

<a id="op-4416fcb90dd66e"></a>
### Create additional salary

`operation_workforce_human_resources_record_definitions_employee_referral_business_behavior_create_additional_salary`

**Inputs** employee\_referral.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** resolve a document from “Employee Referral” via get\_doc · read “Additional Salary” via exists · read “Employee” via get\_value.

**State and service calls** request new\_doc for “Additional Salary”.

**Explicit results** additional\_salary.

**Local steps**

- Set doc from Platform.get\_doc(“Employee Referral”, employee\_referral).
- If not Platform.db.exists(“Additional Salary”, mapping(“ref\_docname” → doc.name)).
  - Set additional\_salary from Platform.new\_doc(“Additional Salary”).
  - Set additional\_salary.employee from doc.referrer.
  - Set additional\_salary.company from Platform.db.get\_value(“Employee”, doc.referrer, “company”).
  - Set additional\_salary.overwrite\_salary\_structure\_amount from 0.
  - Set additional\_salary.ref\_doctype from doc.doctype.
  - Set additional\_salary.ref\_docname from doc.name.
- Return additional\_salary.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L2431) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L639) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L619)

<a id="op-e02e2ab20b2b90"></a>
### Get data

`operation_workforce_human_resources_record_definitions_employee_referral_employee_referral_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “employee\_referral”, “non\_standard\_fieldnames” → mapping(“Additional Salary” → “ref\_docname”), “transactions” → list(mapping(“items” → list(“Job Applicant”, “Additional Salary”)))).

**Local steps**

- Return mapping(“fieldname” → “employee\_referral”, “non\_standard\_fieldnames” → mapping(“Additional Salary” → “ref\_docname”), “transactions” → list(mapping(“items” → list(“Job Applicant”, “Additional Salary”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L2774) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L647) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L627)
