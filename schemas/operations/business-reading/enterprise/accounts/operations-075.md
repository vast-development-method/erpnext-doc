# Accounting and settlement · operations 75

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment request

[Record definition](../../../../data/record-types/payment_request.json)

<a id="op-e8d1e9c34188e8"></a>
### Make payment order

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_make_payment_order`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind dependencies get\_mapped\_doc.
- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Payment Request”, source\_name, mapping(“Payment Request” → mapping(“doctype” → “Payment Order”, “field\_no\_map” → list(“company”) when target\_doc, otherwise list())), target\_doc, …).
  - Value choice on target\_doc — true gives list(“company”), false gives list().
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L347)

<a id="op-5849102eeb8740"></a>
### Make payment order.set missing values

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_make_payment_order_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.payment\_order\_type from “Payment Request”.
- Set target.company from (target.company or source.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target.company → source.company.
- Evaluate target.append(“references”, mapping(“reference\_doctype” → source.reference\_doctype, “reference\_name” → source.reference\_name, “amount” → source.outstanding\_amount, “supplier” → source.party, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L348)

<a id="op-1b9f37b7576b21"></a>
### Validate payment

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_validate_payment`

**Inputs** doc, method = no value.

**Record and data access** read doc.reference\_doctype via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The Payment Request {0} is already paid, cannot process payment twice”.format(doc.reference\_docname).

**Local steps**

- If (doc.reference\_doctype differs from “Payment Request” or Platform.db.get\_value(doc.reference\_doctype, doc.reference\_docname, “status”) differs from “Paid”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.reference\_doctype differs from “Payment Request” → Platform.db.get\_value(doc.reference\_doctype, doc.reference\_docname, “status”) differs from “Paid”.
  - Return no value.
- Call the validation error handler Platform.throw(translated “The Payment Request {0} is already paid, cannot process payment twice”.format(doc.reference\_docname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L3649) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L381)

<a id="op-d24f96c1fd1f72"></a>
### Get bank account query

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_bank_account_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list() · nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run(as\_list = true).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If (not filters.company and not (filters.party\_type and filters.party)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.company → not (filters.party\_type and filters.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.party\_type → filters.party.
  - Return list().
- Set bank\_account from Platform.qb.DocType(“Bank Account”).
- Set ownership from bank\_account.name equals empty text.
- If filters.company.
  - Set ownership from (bank\_account.is\_company\_account equals 1 bitwise and bank\_account.company equals filters.company).
- If (filters.party\_type and filters.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.party\_type → filters.party.
  - Update ownership using bitwise or ((bank\_account.is\_company\_account equals 0 bitwise and bank\_account.party\_type equals filters.party\_type) bitwise and bank\_account.party equals filters.party).
- Return nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run(as\_list = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L853)

<a id="op-227b0dfccafd6a"></a>
### Get open payment requests query

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_open_payment_remote_requests_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Payment Request” via get\_list.

**Explicit results** list() · list of tuple(pr.name, translated text in the contract.format(pr.grand\_total), translated text in the contract.format(pr.outstanding\_amount)) for pr drawn from open\_payment\_requests.

**Local steps**

- Set filters from Platform.\_dict(filters).
- If (not filters.reference\_doctype or not filters.reference\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.reference\_doctype → not filters.reference\_name.
  - Return list().
- If txt.
  - Set filters.name from list(“like”, formatted text %{txt}%).
- Set open\_payment\_requests from Platform.get\_list(“Payment Request”, filters = filters, fields = list(“name”, “grand\_total”, “outstanding\_amount”), order\_by = “transaction\_date ASC,creation ASC”).
- Return list of tuple(pr.name, translated text in the contract.format(pr.grand\_total), translated text in the contract.format(pr.outstanding\_amount)) for pr drawn from open\_payment\_requests.
  - Draw pr from open\_payment\_requests.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L341)

<a id="op-4928cfb03ac01c"></a>
### Get irequests of payment request

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_irequests_of_payment_request`

**Inputs** doc = no value.

**Declared result** list.

**Record and data access** read “Integration Request” via get\_all.

**Explicit results** res.

**Local steps**

- Set res from list().
- If doc.
  - Set res from Platform.db.get\_all(“Integration Request”, mapping(“reference\_doctype” → “Payment Request”, “reference\_docname” → doc, “status” → “Queued”)).
- Return res.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L4353) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L340)

<a id="op-183450553244af"></a>
### Get available payment schedules

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_available_payment_schedules`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from reference\_doctype via get\_doc.

**Explicit results** list() · list of r for r drawn from ref\_doc.payment\_schedule where r.name does not belong to existing\_ids.

**Local steps**

- Set ref\_doc from Platform.get\_doc(reference\_doctype, reference\_name).
- Evaluate ref\_doc.check\_permission().
- If (not hasattr(ref\_doc, “payment\_schedule”) or not ref\_doc.payment\_schedule).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(ref\_doc, “payment\_schedule”) → not ref\_doc.payment\_schedule.
  - Return list().
- If get\_existing\_payment\_entry(reference\_name).
  - Return list().
- Set existing\_refs from get\_existing\_payment\_references(reference\_name).
- Set existing\_ids from set of r at “payment\_schedule” for r drawn from existing\_refs where r.get(“payment\_schedule”).
  - Draw r from existing\_refs, keep a combination only if (r.get(“payment\_schedule”)).
- Return list of r for r drawn from ref\_doc.payment\_schedule where r.name does not belong to existing\_ids.
  - Draw r from ref\_doc.payment\_schedule, keep a combination only if (r.name does not belong to existing\_ids).

**Values supplied outside this operation** effective access from ref\_doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L333)

<a id="op-97468dd1f2cc95"></a>
### Get existing payment references

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_existing_payment_references`

**Inputs** reference\_name.

**Explicit results** result.

**Local steps**

- Set PR from Platform.qb.DocType(“Payment Request”).
- Set PRF from Platform.qb.DocType(“Payment Reference”).
- Set result from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus &lt; 2).where(PR.status.isin(list(“Draft”, “Requested”, “Initiated”, “Partially Paid”, …))).run(as ….
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L4885) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L336)

<a id="op-eba60fdd7e721a"></a>
### Get data

`operation_enterprise_accounts_record_definitions_payment_request_payment_request_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payment\_request”, “internal\_links” → mapping(“Payment Entry” → list(“references”, “payment\_request”), “Payment Order” → list(“references”, “payment\_order”)), “transactions” → list(ma ….

**Local steps**

- Return mapping(“fieldname” → “payment\_request”, “internal\_links” → mapping(“Payment Entry” → list(“references”, “payment\_request”), “Payment Order” → list(“references”, “payment\_order”)), “transactions” → list(ma ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L5306) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L382)

## Record · Payment term

[Record definition](../../../../data/record-types/payment_term.json)

<a id="op-8635adccde4a76"></a>
### Get data

`operation_enterprise_accounts_record_definitions_payment_term_payment_term_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payment\_term”, “transactions” → list(mapping(“label” → translated “Sales”, “items” → list(“Sales Invoice”, “Sales Order”, “Quotation”)), mapping(“label” → translated “Purchase”, “ite ….

**Local steps**

- Return mapping(“fieldname” → “payment\_term”, “transactions” → list(mapping(“label” → translated “Sales”, “items” → list(“Sales Invoice”, “Sales Order”, “Quotation”)), mapping(“label” → translated “Purchase”, “ite ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L406)

## Record · Payment terms template

[Record definition](../../../../data/record-types/payment_terms_template.json)

<a id="op-0e869b95c96ffd"></a>
### Payment Terms Template.validate

`operation_enterprise_accounts_record_definitions_payment_terms_template_business_behavior_payment_terms_template_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_invoice\_portion().
- Evaluate self.validate\_terms().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate invoice portion](operations-075.md#op-f2b8bc33210422), [validate terms](operations-075.md#op-6c62ddc5e04afc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L249) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L407)

<a id="op-f2b8bc33210422"></a>
### Payment Terms Template.validate invoice portion

`operation_enterprise_accounts_record_definitions_payment_terms_template_business_behavior_payment_terms_template_validate_invoice_portion`

**Inputs** self.

**State and service calls** msgprint with translated “Combined invoice portion must equal 100%”.

**Local steps**

- Set total\_portion from 0.
- For each term in self.terms.
  - Update total\_portion using + flt(term.get(“invoice\_portion”, 0)).
- If flt(total\_portion, 2) differs from 100.0.
  - Evaluate Platform.msgprint(translated “Combined invoice portion must equal 100%”, raise\_exception = 1, indicator = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L320) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L408)

<a id="op-6c62ddc5e04afc"></a>
### Payment Terms Template.validate terms

`operation_enterprise_accounts_record_definitions_payment_terms_template_business_behavior_payment_terms_template_validate_terms`

**Inputs** self.

**State and service calls** msgprint with translated “The Payment Term at row {0} is possibly a duplicate.”.format(term.idx).

**Explicit failure paths** validation helper — translated “Row {0}: Payment Term is mandatory”.format(term.idx).

**Local steps**

- Set terms from list().
- For each term in self.terms.
  - If (self.allocate\_payment\_based\_on\_payment\_terms and not term.payment\_term).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.allocate\_payment\_based\_on\_payment\_terms → not term.payment\_term.
    - Call the validation error handler Platform.throw(translated “Row {0}: Payment Term is mandatory”.format(term.idx)).
  - Set term\_info from tuple(term.payment\_term, term.credit\_days, term.credit\_months, term.due\_date\_based\_on).
  - If term\_info belongs to terms.
    - Evaluate Platform.msgprint(translated “The Payment Term at row {0} is possibly a duplicate.”.format(term.idx), raise\_exception = 1, indicator = “red”).
  - Otherwise.
    - Evaluate terms.append(term\_info).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L530) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L409)

<a id="op-ef871cc37dd51e"></a>
### Get data

`operation_enterprise_accounts_record_definitions_payment_terms_template_payment_terms_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payment\_terms\_template”, “non\_standard\_fieldnames” → mapping(“Customer Group” → “payment\_terms”, “Supplier Group” → “payment\_terms”, “Supplier” → “payment\_terms”, “Customer” → “payme ….

**Local steps**

- Return mapping(“fieldname” → “payment\_terms\_template”, “non\_standard\_fieldnames” → mapping(“Customer Group” → “payment\_terms”, “Supplier Group” → “payment\_terms”, “Supplier” → “payment\_terms”, “Customer” → “payme ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L859) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L410)

## Record · Period closing voucher

[Record definition](../../../../data/record-types/period_closing_voucher.json)

<a id="op-50689433187825"></a>
### Period Closing Voucher.validate

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_start\_and\_end\_date().
- Evaluate self.check\_if\_previous\_period\_closed().
- Evaluate self.block\_if\_future\_closing\_voucher\_exists().
- Evaluate self.check\_closing\_account().
- Evaluate self.check\_closing\_account\_currency().
- Evaluate self.validate\_accounts\_not\_frozen().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate start and end date](operations-075.md#op-c108b80576d98f), [check if previous period closed](operations-075.md#op-fd6fb6ab4996a4), [block if future closing voucher exists](operations-075.md#op-71a42a9e4d5e37), [check closing account](operations-075.md#op-c65af36dc5b025), [check closing account currency](operations-075.md#op-285f21612ec4eb), [validate accounts not frozen](operations-075.md#op-03ce049e2176ce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L447)

<a id="op-03ce049e2176ce"></a>
### Period Closing Voucher.validate accounts not frozen

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_validate_accounts_not_frozen`

**Inputs** self.

**Local steps**

- Evaluate check\_freezing\_date(self.period\_end\_date, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L448)

<a id="op-c108b80576d98f"></a>
### Period Closing Voucher.validate start and end date

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_validate_start_and_end_date`

**Inputs** self.

**Record and data access** read “Fiscal Year” via get\_value.

**Explicit failure paths** validation helper — translated “Period Start Date must be {0}”.format(formatdate(valid\_start\_date)) · validation helper — translated “Period Start Date cannot be greater than Period End Date” · validation helper — translated “Period End Date cannot be greater than Fiscal Year End Date”.

**Local steps**

- Set tuple(self.fy\_start\_date, self.fy\_end\_date) from Platform.db.get\_value(“Fiscal Year”, self.fiscal\_year, list(“year\_start\_date”, “year\_end\_date”)).
- Set prev\_closed\_period\_end\_date from get\_previous\_closed\_period\_in\_current\_year(self.fiscal\_year, self.company).
- Set valid\_start\_date from add\_days(prev\_closed\_period\_end\_date, 1) when prev\_closed\_period\_end\_date, otherwise self.fy\_start\_date.
  - Value choice on prev\_closed\_period\_end\_date — true gives add\_days(prev\_closed\_period\_end\_date, 1), false gives self.fy\_start\_date.
- If getdate(self.period\_start\_date) differs from getdate(valid\_start\_date).
  - Call the validation error handler Platform.throw(translated “Period Start Date must be {0}”.format(formatdate(valid\_start\_date))).
- If getdate(self.period\_start\_date) &gt; getdate(self.period\_end\_date).
  - Call the validation error handler Platform.throw(translated “Period Start Date cannot be greater than Period End Date”).
- If getdate(self.period\_end\_date) &gt; getdate(self.fy\_end\_date).
  - Call the validation error handler Platform.throw(translated “Period End Date cannot be greater than Fiscal Year End Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L3228) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L449)

<a id="op-fd6fb6ab4996a4"></a>
### Period Closing Voucher.check if previous period closed

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_check_if_previous_period_closed`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Period Closing Voucher {0} has GL Entry Processing Status {1}. Complete or cancel it before closing the next …”.format(get\_link\_to\_form(self.doctype, last\_closing.name), translated last\_closing … · validation helper — translated “Previous period is not closed. Close the period from {0} first.”.format(Platform.bold(formatdate(open\_from))).

**Local steps**

- Set last\_closing from self.get\_last\_closing().
- If (last\_closing and last\_closing.gle\_processing\_status differs from “Completed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_closing → last\_closing.gle\_processing\_status differs from “Completed”.
  - Call the validation error handler Platform.throw(translated “Period Closing Voucher {0} has GL Entry Processing Status {1}. Complete or cancel it before closing the next …”.format(get\_link\_to\_form(self.doctype, last\_closing.name), translat ….
- Set last\_closed\_date from last\_closing.period\_end\_date when last\_closing, otherwise no value.
  - Value choice on last\_closing — true gives last\_closing.period\_end\_date, false gives no value.
- If (last\_closed\_date and getdate(add\_days(last\_closed\_date, 1)) equals getdate(self.period\_start\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_closed\_date → getdate(add\_days(last\_closed\_date, 1)) equals getdate(self.period\_start\_date).
  - Return no value.
- Set first\_unclosed\_date from self.get\_first\_unclosed\_date(last\_closed\_date).
- If first\_unclosed\_date.
  - Set open\_from from add\_days(last\_closed\_date, 1) when last\_closed\_date, otherwise first\_unclosed\_date.
    - Value choice on last\_closed\_date — true gives add\_days(last\_closed\_date, 1), false gives first\_unclosed\_date.
  - Call the validation error handler Platform.throw(translated “Previous period is not closed. Close the period from {0} first.”.format(Platform.bold(formatdate(open\_from)))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last closing](operations-075.md#op-41d060100fb4c6), [get first unclosed date](operations-075.md#op-2638d8511cc0b8).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L871)

<a id="op-41d060100fb4c6"></a>
### Period Closing Voucher.get last closing

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_get_last_closing`

**Inputs** self.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit results** Platform.db.get\_value(“Period Closing Voucher”, mapping(“company” → self.company, “docstatus” → 1, “period\_end\_date” → tuple(“&lt;”, self.period\_start\_date)), list(“name”, “period\_end\_date”, “gle\_processing\_s ….

**Local steps**

- Return Platform.db.get\_value(“Period Closing Voucher”, mapping(“company” → self.company, “docstatus” → 1, “period\_end\_date” → tuple(“&lt;”, self.period\_start\_date)), list(“name”, “period\_end\_date”, “gle\_processing\_s ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L873)

<a id="op-2638d8511cc0b8"></a>
### Period Closing Voucher.get first unclosed date

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_get_first_unclosed_date`

**Inputs** self, last\_closed\_date.

**Record and data access** read “GL Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“GL Entry”, mapping(“company” → self.company, “posting\_date” → posting\_date, “is\_cancelled” → 0, “is\_opening” → “No”, …), “posting\_date”, order\_by = “posting\_date asc”).

**Local steps**

- Set posting\_date from tuple(“&lt;”, self.period\_start\_date).
- If last\_closed\_date.
  - Set posting\_date from tuple(“between”, list(add\_days(last\_closed\_date, 1), add\_days(self.period\_start\_date, negative 1))).
- Return Platform.db.get\_value(“GL Entry”, mapping(“company” → self.company, “posting\_date” → posting\_date, “is\_cancelled” → 0, “is\_opening” → “No”, …), “posting\_date”, order\_by = “posting\_date asc”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L872)

<a id="op-71a42a9e4d5e37"></a>
### Period Closing Voucher.block if future closing voucher exists

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_block_if_future_closing_voucher_exists`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You cannot {0} this document because another Period Closing Entry {1} exists after {2}”.format(action, future\_closing\_voucher, self.period\_end\_date).

**Local steps**

- Set future\_closing\_voucher from self.get\_future\_closing\_voucher().
- If future\_closing\_voucher.
  - Set action from “cancel” when self.docstatus equals 2, otherwise “create”.
    - Value choice on self.docstatus equals 2 — true gives “cancel”, false gives “create”.
  - Call the validation error handler Platform.throw(translated “You cannot {0} this document because another Period Closing Entry {1} exists after {2}”.format(action, future\_closing\_voucher, self.period\_end\_date)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get future closing voucher](operations-075.md#op-8a2f2a5d997d64).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L420)

<a id="op-8a2f2a5d997d64"></a>
### Period Closing Voucher.get future closing voucher

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_future_closing_voucher`

**Inputs** self.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit results** Platform.db.get\_value(“Period Closing Voucher”, mapping(“period\_end\_date” → tuple(“&gt;”, self.period\_end\_date), “docstatus” → 1, “company” → self.company), “name”).

**Local steps**

- Return Platform.db.get\_value(“Period Closing Voucher”, mapping(“period\_end\_date” → tuple(“&gt;”, self.period\_end\_date), “docstatus” → 1, “company” → self.company), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L4423) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L431)

<a id="op-c65af36dc5b025"></a>
### Period Closing Voucher.check closing account

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_check_closing_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Closing Account {0} must be of type Liability / Equity”.format(self.closing\_account\_head) · validation helper — translated “Closing Account {0} does not belong to Company {1}”.format(self.closing\_account\_head, self.company) · validation helper — translated “Closing Account {0} cannot be a group account”.format(self.closing\_account\_head) · validation helper — translated “Closing Account {0} is disabled”.format(self.closing\_account\_head).

**Local steps**

- Set account from Platform.get\_cached\_value(“Account”, self.closing\_account\_head, list(“root\_type”, “company”, “is\_group”, “disabled”), as\_dict = true).
- If account.root\_type does not belong to list(“Liability”, “Equity”).
  - Call the validation error handler Platform.throw(translated “Closing Account {0} must be of type Liability / Equity”.format(self.closing\_account\_head)).
- If account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Closing Account {0} does not belong to Company {1}”.format(self.closing\_account\_head, self.company)).
- If account.is\_group.
  - Call the validation error handler Platform.throw(translated “Closing Account {0} cannot be a group account”.format(self.closing\_account\_head)).
- If account.disabled.
  - Call the validation error handler Platform.throw(translated “Closing Account {0} is disabled”.format(self.closing\_account\_head)).
- Evaluate validate\_frozen\_account(self.company, self.closing\_account\_head).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.closing\_account\_head, list(“root\_type”, “company”, “is\_group”, “disabled”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L870)

<a id="op-285f21612ec4eb"></a>
### Period Closing Voucher.check closing account currency

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_check_closing_account_currency`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Currency of the Closing Account must be {0}”.format(company\_currency).

**Local steps**

- Set account\_currency from get\_account\_currency(self.closing\_account\_head).
- Set company\_currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
- If account\_currency differs from company\_currency.
  - Call the validation error handler Platform.throw(translated “Currency of the Closing Account must be {0}”.format(company\_currency)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L4738) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L423)
