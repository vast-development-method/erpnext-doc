# Regional rules and controller overrides · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Employee overview

<a id="op-b985c40d8a844e"></a>
### Row outstanding

`operation_workforce_binding_workforce_overrides_employee_overview_row_outstanding`

**Inputs** doctype, row.

**Explicit results** ((flt(row.grand\_total) − flt(row.total\_amount\_reimbursed)) × flt((row.exchange\_rate or 1))) · ((flt(row.paid\_amount) − flt(row.claimed\_amount)) − flt(row.return\_amount)) · no value.

**Local steps**

- If (doctype equals “Expense Claim” and row.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Expense Claim” → row.docstatus equals 1.
  - Return ((flt(row.grand\_total) − flt(row.total\_amount\_reimbursed)) × flt((row.exchange\_rate or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.exchange\_rate → 1.
- If doctype equals “Employee Advance”.
  - Return ((flt(row.paid\_amount) − flt(row.claimed\_amount)) − flt(row.return\_amount)).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L170) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L221) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L221)

<a id="op-e31417bf7b9bb6"></a>
### Has activity

`operation_workforce_binding_workforce_overrides_employee_overview_has_activity`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** any(generator of (Platform.has\_permission(doctype, “read”) and Platform.get\_list(doctype, filters = mapping(“employee” → employee, “docstatus” → list(“!=”, 2)), limit = 1)) for doctype drawn from tuple(expande …).

**Local steps**

- Evaluate check\_access(employee).
- Return any(generator of (Platform.has\_permission(doctype, “read”) and Platform.get\_list(doctype, filters = mapping(“employee” → employee, “docstatus” → list(“!=”, 2)), limit = 1)) for doctype drawn from tuple(expande …).
  - Draw doctype from tuple(expanded TRANSACTION\_TYPES, “Attendance”, “Leave Allocation”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(doctype, “read”) → Platform.get\_list(doctype, filters = mapping(“employee” → employee, “docstatus” → list(“!=”, 2)), limit = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L162) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L213) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L213)

## Service · Employee payment entry

<a id="op-4a8da36b9c0fc0"></a>
### Employee Payment Entry.get valid reference doctypes

`operation_workforce_overrides_employee_payment_entry_business_behavior_employee_payment_entry_get_valid_reference_record_types`

**Inputs** self.

**Explicit results** tuple(“Sales Order”, “Sales Invoice”, “Journal Entry”, “Dunning”, …) · tuple(“Purchase Order”, “Purchase Invoice”, “Journal Entry”, “Payment Entry”) · tuple(“Journal Entry”) · tuple(“Expense Claim”, “Journal Entry”, “Employee Advance”, “Leave Encashment”, …).

**Local steps**

- If self.party\_type equals “Customer”.
  - Return tuple(“Sales Order”, “Sales Invoice”, “Journal Entry”, “Dunning”, …).
- Otherwise.
  - If self.party\_type equals “Supplier”.
    - Return tuple(“Purchase Order”, “Purchase Invoice”, “Journal Entry”, “Payment Entry”).
  - Otherwise.
    - If self.party\_type equals “Shareholder”.
      - Return tuple(“Journal Entry”).
    - Otherwise.
      - If self.party\_type equals “Employee”.
        - Return tuple(“Expense Claim”, “Journal Entry”, “Employee Advance”, “Leave Encashment”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L1170) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L220) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L569)

<a id="op-1caf419fef6e95"></a>
### Employee Payment Entry.set missing ref details

`operation_workforce_overrides_employee_payment_entry_business_behavior_employee_payment_entry_set_missing_reference_details`

**Inputs** self, force = false, update\_ref\_details\_only\_for = no value, reference\_exchange\_details = no value.

**Declared result** no value.

**State and service calls** call db\_set on d.

**Local steps**

- For each d in self.get(“references”).
  - If d.allocated\_amount.
    - If (update\_ref\_details\_only\_for and tuple(d.reference\_doctype, d.reference\_name) does not belong to update\_ref\_details\_only\_for).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_ref\_details\_only\_for → tuple(d.reference\_doctype, d.reference\_name) does not belong to update\_ref\_details\_only\_for.
      - Continue with the next iteration or loop test.
    - Set ref\_details from get\_payment\_reference\_details(d.reference\_doctype, d.reference\_name, self.party\_account\_currency, self.party\_type, …).
    - If (reference\_exchange\_details and d.reference\_doctype equals reference\_exchange\_details.reference\_doctype and d.reference\_name equals reference\_exchange\_details.reference\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_exchange\_details → d.reference\_doctype equals reference\_exchange\_details.reference\_doctype → d.reference\_name equals reference\_exchange\_details.reference\_name.
      - Evaluate ref\_details.update(mapping(“exchange\_rate” → reference\_exchange\_details.exchange\_rate)).
    - For each tuple(field, value) in ref\_details.items().
      - If d.exchange\_gain\_loss.
        - Continue with the next iteration or loop test.
      - If (field equals “exchange\_rate” or not d.get(field) or force).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in field equals “exchange\_rate” → not d.get(field) → force.
        - If self.get(“\_action”) belongs to tuple(“submit”, “cancel”).
          - Evaluate d.db\_set(field, value).
        - Otherwise.
          - Evaluate d.set(field, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L1494) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L221) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L570)

<a id="op-5de5634d388236"></a>
### Get payment entry for employee

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_payment_entry_for_employee`

**Inputs** dt, dn, party\_amount = no value, bank\_account = no value, bank\_amount = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from dt via get\_doc.

**State and service calls** request new\_doc for “Payment Entry”.

**Explicit results** pe.

**Explicit failure paths** validation helper — translated “Please set a {0} on this document, or a Default Bank/Cash Account in the Company {1}”.format(get\_link\_to\_form(dt, (dn + “#mode\_of\_payment”), translated “Mode of Payment”), company\_link) · validation helper — translated “Please set a Default Bank/Cash Account in the Company {0}”.format(company\_link).

**Local steps**

- Evaluate Platform.has\_permission(dt, “read”, dn, throw = true).
- Set doc from Platform.get\_doc(dt, dn).
- Set party\_account from get\_party\_account(doc).
- Set party\_account\_currency from get\_account\_currency(party\_account).
- Set payment\_type from “Pay”.
- Set tuple(grand\_total, outstanding\_amount) from get\_grand\_total\_and\_outstanding\_amount(doc, party\_amount, party\_account\_currency).
- Set bank from get\_bank\_cash\_account(doc, bank\_account).
- If not bank.get(“account”).
  - Set company\_link from get\_link\_to\_form(“Company”, (doc.company + “#accounts\_tab”), translated “here”).
  - If Platform.get\_meta(dt).has\_field(“mode\_of\_payment”).
    - Call the validation error handler Platform.throw(translated “Please set a {0} on this document, or a Default Bank/Cash Account in the Company {1}”.format(get\_link\_to\_form(dt, (dn + “#mode\_of\_payment”), translated “Mode of Payment”), compan ….
  - Call the validation error handler Platform.throw(translated “Please set a Default Bank/Cash Account in the Company {0}”.format(company\_link), title = translated “Bank/Cash Account Required”).
- Set pe from Platform.new\_doc(“Payment Entry”).
- Set pe.payment\_type from payment\_type.
- Set pe.company from doc.company.
- Set pe.cost\_center from doc.get(“cost\_center”).
- Set pe.posting\_date from nowdate().
- Set pe.mode\_of\_payment from doc.get(“mode\_of\_payment”).
- Set pe.party\_type from “Employee”.
- Set pe.party from doc.get(“employee”).
- Set pe.contact\_person from doc.get(“contact\_person”).
- Set pe.contact\_email from doc.get(“contact\_email”).
- Set pe.letter\_head from doc.get(“letter\_head”).
- Set pe.paid\_from from bank.account.
- Set pe.paid\_to from party\_account.
- Set pe.paid\_from\_account\_currency from bank.account\_currency.
- Set pe.paid\_to\_account\_currency from party\_account\_currency.
- Evaluate pe.append(“references”, mapping(“reference\_doctype” → dt, “reference\_name” → dn, “bill\_no” → doc.get(“bill\_no”), “due\_date” → doc.get(“due\_date”), …)).
- Evaluate pe.setup\_party\_account\_field().
- Evaluate pe.set\_missing\_values().
- Evaluate pe.set\_missing\_ref\_details().
- Set current\_exchange\_rate from get\_exchange\_rate(pe.paid\_to\_account\_currency, pe.paid\_from\_account\_currency, pe.posting\_date).
- Set tuple(paid\_amount, received\_amount) from get\_paid\_amount\_and\_received\_amount(doc, party\_account\_currency, bank, outstanding\_amount, …).
- Set pe.paid\_amount from paid\_amount.
- Set pe.received\_amount from received\_amount.
- If (party\_account and bank).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account → bank.
  - Evaluate pe.set\_exchange\_rate().
  - If (dt equals “Employee Advance” and pe.paid\_to\_account\_currency differs from pe.paid\_from\_account\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Employee Advance” → pe.paid\_to\_account\_currency differs from pe.paid\_from\_account\_currency.
    - Set pe.target\_exchange\_rate from current\_exchange\_rate.
  - Evaluate pe.set\_amounts().
- Return pe.

**Values supplied outside this operation** effective access from Platform.has\_permission(dt, “read”, dn, throw = true) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L92) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L225) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L574)

<a id="op-f29c4e83cdc92d"></a>
### Get party account

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_party_account`

**Inputs** doc.

**Explicit results** party\_account.

**Local steps**

- Set party\_account from no value.
- If doc.doctype equals “Employee Advance”.
  - Set party\_account from doc.advance\_account.
- Otherwise.
  - If doc.doctype belongs to tuple(“Expense Claim”, “Gratuity”, “Leave Encashment”).
    - Set party\_account from doc.payable\_account.
- Return party\_account.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L3381) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L224) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L573)

<a id="op-f93f97f3c127c6"></a>
### Get grand total and outstanding amount

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_grand_total_and_outstanding_amount`

**Inputs** doc, party\_amount, party\_account\_currency.

**Explicit results** tuple(grand\_total, outstanding\_amount).

**Local steps**

- Set grand\_total, outstanding\_amount from 0.
- If party\_amount.
  - Set grand\_total, outstanding\_amount from party\_amount.
- Otherwise.
  - If doc.doctype equals “Expense Claim”.
    - Set grand\_total from (flt(doc.total\_sanctioned\_amount) + flt(doc.total\_taxes\_and\_charges)).
    - Set outstanding\_amount from get\_outstanding\_amount\_for\_claim(doc.name).
  - Otherwise.
    - If doc.doctype equals “Employee Advance”.
      - Set grand\_total from flt(doc.advance\_amount).
      - Set outstanding\_amount from (flt(doc.advance\_amount) − flt(doc.paid\_amount)).
      - If party\_account\_currency differs from doc.currency.
        - Set grand\_total from (flt(doc.advance\_amount) × flt(doc.exchange\_rate)).
        - Set outstanding\_amount from ((flt(doc.advance\_amount) − flt(doc.paid\_amount)) × flt(doc.exchange\_rate)).
    - Otherwise.
      - If doc.doctype equals “Gratuity”.
        - Set grand\_total from doc.amount.
        - Set outstanding\_amount from (flt(doc.amount) − flt(doc.paid\_amount)).
      - Otherwise.
        - If doc.doctype equals “Leave Encashment”.
          - Set grand\_total from doc.encashment\_amount.
          - Set outstanding\_amount from (flt(doc.encashment\_amount) − flt(doc.paid\_amount)).
        - Otherwise.
          - If party\_account\_currency equals doc.company\_currency.
            - Set grand\_total from flt((doc.get(“base\_rounded\_total”) or doc.base\_grand\_total)).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“base\_rounded\_total”) → doc.base\_grand\_total.
          - Otherwise.
            - Set grand\_total from flt((doc.get(“rounded\_total”) or doc.grand\_total)).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“rounded\_total”) → doc.grand\_total.
          - Set outstanding\_amount from (grand\_total − flt(doc.advance\_paid)).
- Return tuple(grand\_total, outstanding\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L3550) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L222) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L571)

<a id="op-eba373e2a834d8"></a>
### Get paid amount and received amount

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_paid_amount_and_received_amount`

**Inputs** doc, party\_account\_currency, bank, outstanding\_amount, payment\_type, bank\_amount, exchange\_rate.

**Explicit results** tuple(paid\_amount, received\_amount).

**Local steps**

- Set paid\_amount, received\_amount from 0.
- If party\_account\_currency equals bank.account\_currency.
  - Set paid\_amount, received\_amount from abs(outstanding\_amount).
- Otherwise.
  - If payment\_type equals “Receive”.
    - Set paid\_amount from abs(outstanding\_amount).
    - If bank\_amount.
      - Set received\_amount from bank\_amount.
    - Otherwise.
      - Set received\_amount from (paid\_amount × doc.get(“conversion\_rate”, 1)).
      - If doc.doctype equals “Employee Advance”.
        - Set received\_amount from (paid\_amount × doc.get(“exchange\_rate”, 1)).
  - Otherwise.
    - Set received\_amount from abs(outstanding\_amount).
    - If bank\_amount.
      - Set paid\_amount from bank\_amount.
    - Otherwise.
      - Set paid\_amount from (received\_amount × doc.get(“conversion\_rate”, 1)).
      - If doc.doctype equals “Employee Advance”.
        - Set paid\_amount from (received\_amount × exchange\_rate).
- Return tuple(paid\_amount, received\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L4416) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L223) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L572)

<a id="op-3ad3aff38f6cbc"></a>
### Get payment reference details

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_payment_reference_details`

**Inputs** reference\_doctype, reference\_name, party\_account\_currency, party\_type = no value, party = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_reference\_details\_for\_employee(reference\_doctype, reference\_name, party\_account\_currency) · get\_reference\_details(reference\_doctype, reference\_name, party\_account\_currency, party\_type, …).

**Local steps**

- Evaluate Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).
- If reference\_doctype belongs to tuple(“Expense Claim”, “Employee Advance”, “Gratuity”, “Leave Encashment”).
  - Return get\_reference\_details\_for\_employee(reference\_doctype, reference\_name, party\_account\_currency).
- Otherwise.
  - Return get\_reference\_details(reference\_doctype, reference\_name, party\_account\_currency, party\_type, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L4916) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L226) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L575)

<a id="op-b07d84621c19a8"></a>
### Get reference details for employee

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_reference_details_for_employee`

**Inputs** reference\_doctype, reference\_name, party\_account\_currency.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from reference\_doctype via get\_doc.

**Explicit results** Platform.\_dict(mapping(“due\_date” → ref\_doc.get(“due\_date”), “total\_amount” → flt(total\_amount), “outstanding\_amount” → flt(outstanding\_amount), “exchange\_rate” → flt(exchange\_rate))).

**Local steps**

- Evaluate Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).
- Set total\_amount, outstanding\_amount, exchange\_rate from no value.
- Set ref\_doc from Platform.get\_doc(reference\_doctype, reference\_name).
- Set company\_currency from (ref\_doc.get(“company\_currency”) or Enterprise.get\_company\_currency(ref\_doc.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“company\_currency”) → Enterprise.get\_company\_currency(ref\_doc.company).
- Set tuple(total\_amount, exchange\_rate) from get\_total\_amount\_and\_exchange\_rate(ref\_doc, party\_account\_currency, company\_currency).
- If reference\_doctype equals “Expense Claim”.
  - Set outstanding\_amount from get\_outstanding\_amount\_for\_claim(ref\_doc).
- Otherwise.
  - If reference\_doctype equals “Employee Advance”.
    - Set outstanding\_amount from (flt(ref\_doc.advance\_amount) − flt(ref\_doc.paid\_amount)).
    - If party\_account\_currency differs from ref\_doc.currency.
      - Set outstanding\_amount from (flt(outstanding\_amount) × flt(exchange\_rate)).
  - Otherwise.
    - If reference\_doctype equals “Gratuity”.
      - Set outstanding\_amount from (ref\_doc.amount − flt(ref\_doc.paid\_amount)).
    - Otherwise.
      - If reference\_doctype equals “Leave Encashment”.
        - Set outstanding\_amount from (ref\_doc.encashment\_amount − flt(ref\_doc.paid\_amount)).
      - Otherwise.
        - Set outstanding\_amount from (flt(total\_amount) − flt(ref\_doc.advance\_paid)).
- Return Platform.\_dict(mapping(“due\_date” → ref\_doc.get(“due\_date”), “total\_amount” → flt(total\_amount), “outstanding\_amount” → flt(outstanding\_amount), “exchange\_rate” → flt(exchange\_rate))).

**Values supplied outside this operation** effective access from Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L5215) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L227) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L576)

<a id="op-9dd8763ec5dc1e"></a>
### Get total amount and exchange rate

`operation_workforce_overrides_employee_payment_entry_business_behavior_get_total_amount_and_exchange_rate`

**Inputs** ref\_doc, party\_account\_currency, company\_currency.

**Explicit results** tuple(total\_amount, exchange\_rate).

**Local steps**

- Set total\_amount, exchange\_rate from no value.
- If ref\_doc.doctype equals “Expense Claim”.
  - Set total\_amount from (flt(ref\_doc.total\_sanctioned\_amount) + flt(ref\_doc.total\_taxes\_and\_charges)).
- Otherwise.
  - If ref\_doc.doctype equals “Employee Advance”.
    - Set total\_amount from ref\_doc.advance\_amount.
    - Set exchange\_rate from ref\_doc.get(“exchange\_rate”).
    - If party\_account\_currency differs from ref\_doc.currency.
      - Set total\_amount from (flt(total\_amount) × flt(exchange\_rate)).
    - If (party\_account\_currency equals company\_currency and party\_account\_currency equals ref\_doc.currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account\_currency equals company\_currency → party\_account\_currency equals ref\_doc.currency.
      - Set exchange\_rate from 1.
  - Otherwise.
    - If ref\_doc.doctype equals “Leave Encashment”.
      - Set total\_amount from ref\_doc.encashment\_amount.
    - Otherwise.
      - If ref\_doc.doctype equals “Gratuity”.
        - Set total\_amount from ref\_doc.amount.
- If not total\_amount.
  - If party\_account\_currency equals company\_currency.
    - Set total\_amount from ref\_doc.base\_grand\_total.
    - Set exchange\_rate from 1.
  - Otherwise.
    - Set total\_amount from ref\_doc.grand\_total.
- If not exchange\_rate.
  - Set exchange\_rate from (ref\_doc.get(“conversion\_rate”) or get\_exchange\_rate(party\_account\_currency, company\_currency, ref\_doc.posting\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“conversion\_rate”) → get\_exchange\_rate(party\_account\_currency, company\_currency, ref\_doc.posting\_date).
- Return tuple(total\_amount, exchange\_rate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L6029) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L228) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L577)

<a id="op-3a3e5b94d76dfb"></a>
### Set exchange rate in advance

`operation_workforce_overrides_employee_payment_entry_business_behavior_set_exchange_rate_in_advance`

**Inputs** doc, method = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** request set\_value on “Employee Advance”.

**Local steps**

- If doc.references.
  - For each reference\_doc in doc.references.
    - If (reference\_doc.reference\_doctype equals “Employee Advance” and doc.target\_exchange\_rate).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doc.reference\_doctype equals “Employee Advance” → doc.target\_exchange\_rate.
      - Evaluate Platform.has\_permission(“Employee Advance”, “write”, reference\_doc.reference\_name, throw = true).
      - Evaluate Platform.db.set\_value(“Employee Advance”, reference\_doc.reference\_name, “exchange\_rate”, doc.target\_exchange\_rate, update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee Advance”, “write”, reference\_doc.reference\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L6668) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L229) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L578)

## Service · Employee project

<a id="op-ca929a7c6851de"></a>
### Employee Project.calculate gross margin

`operation_workforce_overrides_employee_project_business_behavior_employee_project_calculate_gross_margin`

**Inputs** self.

**Local steps**

- Set expense\_amount from (((flt(self.total\_costing\_amount) + flt(self.total\_expense\_claim)) + flt(self.total\_purchase\_cost)) + flt(self.get(“total\_consumed\_material\_cost”, 0))).
- Set self.gross\_margin from (flt(self.total\_billed\_amount) − expense\_amount).
- If self.total\_billed\_amount.
  - Set self.per\_gross\_margin from ((self.gross\_margin ÷ flt(self.total\_billed\_amount)) × 100).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0100.json#L6955) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L230) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L579)

<a id="op-03c1b6ffc933d3"></a>
### Employee Project.update costing

`operation_workforce_overrides_employee_project_business_behavior_employee_project_update_costing`

**Inputs** self.

**Local steps**

- Set ExpenseClaim from Platform.qb.DocType(“Expense Claim”).
- Set ExpenseClaimDetail from Platform.qb.DocType(“Expense Claim Detail”).
- Set self.total\_expense\_claim from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0.
- Set TimesheetDetail from Platform.qb.DocType(“Timesheet Detail”).
- Set from\_time\_sheet from nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract), nested operand in the contract(nested o … at 0.
- Set self.actual\_start\_date from from\_time\_sheet.start\_date.
- Set self.actual\_end\_date from from\_time\_sheet.end\_date.
- Set self.total\_costing\_amount from from\_time\_sheet.costing\_amount.
- Set self.total\_billable\_amount from from\_time\_sheet.billing\_amount.
- Set self.actual\_time from from\_time\_sheet.time.
- Evaluate self.update\_purchase\_costing().
- Evaluate self.update\_sales\_amount().
- Evaluate self.update\_billed\_amount().
- Evaluate self.calculate\_gross\_margin().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate gross margin](operations-003.md#op-ca929a7c6851de).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0101.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L231) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L580)

## Service · Employee timesheet

<a id="op-d539d7627ed0a0"></a>
### Employee Timesheet.set status

`operation_workforce_overrides_employee_timesheet_business_behavior_employee_timesheet_set_status`

**Inputs** self.

**Local steps**

- Set self.status from mapping(“0” → “Draft”, “1” → “Submitted”, “2” → “Cancelled”) at str((self.docstatus or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus → 0.
- If flt(self.per\_billed, self.precision(“per\_billed”)) ≥ 100.0.
  - Set self.status from “Billed”.
- If 0.0 &lt; flt(self.per\_billed, self.precision(“per\_billed”)) &lt; 100.0.
  - Compare adjacent operands in order, stopping at the first false comparison in 0.0 &lt; flt(self.per\_billed, self.precision(“per\_billed”)) &lt; 100.0.
  - Set self.status from “Partially Billed”.
- If self.salary\_slip.
  - Set self.status from “Payslip”.
- If (self.sales\_invoice and self.salary\_slip).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sales\_invoice → self.salary\_slip.
  - Set self.status from “Completed”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0101.json#L906) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L232) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L581)

## Service · Pwa notifications

<a id="op-0669a173c98215"></a>
### PWANotifications Mixin.notify approval status

`operation_workforce_mixins_pwa_notifications_business_behavior_progressive_web_application_notifications_mixin_notify_approval_status`

**Inputs** self.

**State and service calls** request new\_doc for “PWA Notification” · call insert on notification.

**Explicit results** no value.

**Local steps**

- Set status\_field from self.\_get\_doc\_status\_field().
- Set status from self.get(status\_field).
- If (self.has\_value\_changed(status\_field) and status belongs to list(“Approved”, “Rejected”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(status\_field) → status belongs to list(“Approved”, “Rejected”).
  - Set from\_user from Platform.session.user.
  - Set from\_user\_name from self.\_get\_user\_name(from\_user).
  - Set to\_user from self.\_get\_employee\_user().
  - If from\_user equals to\_user.
    - Return no value.
  - Set notification from Platform.new\_doc(“PWA Notification”).
  - Set notification.from\_user from from\_user.
  - Set notification.to\_user from to\_user.
  - Set notification.message from formatted text {bold(“Your”)} {bold(self.doctype)} {self.name} has been {bold(status)} by {bold(from\_user\_name)}.
  - Set notification.reference\_document\_type from self.doctype.
  - Set notification.reference\_document\_name from self.name.
  - Evaluate notification.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doc status field](operations-003.md#op-0dd4f8f4009f05), [get user name](operations-003.md#op-5fe1c5c9d395a1), [get employee user](operations-003.md#op-6fac2cc138826d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L3248) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L188) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L537)

<a id="op-9ba96b3655a73d"></a>
### PWANotifications Mixin.notify approver

`operation_workforce_mixins_pwa_notifications_business_behavior_progressive_web_application_notifications_mixin_notify_approver`

**Inputs** self.

**State and service calls** request new\_doc for “PWA Notification” · call insert on notification.

**Explicit results** no value.

**Local steps**

- Set from\_user from self.\_get\_employee\_user().
- Set to\_user from self.\_get\_doc\_approver().
- If (not to\_user or from\_user equals to\_user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not to\_user → from\_user equals to\_user.
  - Return no value.
- Set notification from Platform.new\_doc(“PWA Notification”).
- Set notification.message from formatted text {bold(self.employee\_name)} raised a new {bold(self.doctype)} for approval: {self.name}.
- Set notification.from\_user from from\_user.
- Set notification.to\_user from to\_user.
- Set notification.reference\_document\_type from self.doctype.
- Set notification.reference\_document\_name from self.name.
- Evaluate notification.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get employee user](operations-003.md#op-6fac2cc138826d), [get doc approver](operations-003.md#op-241507780b803d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L3790) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L189) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L538)

<a id="op-0dd4f8f4009f05"></a>
### PWANotifications Mixin.get doc status field

`operation_workforce_mixins_pwa_notifications_business_behavior_progressive_web_application_notifications_mixin_get_record_status_field`

**Inputs** self.

**Declared result** str.

**Explicit results** APPROVAL\_STATUS\_FIELD at self.doctype.

**Local steps**

- Set APPROVAL\_STATUS\_FIELD from mapping(“Leave Application” → “status”, “Expense Claim” → “approval\_status”, “Shift Request” → “status”).
- Return APPROVAL\_STATUS\_FIELD at self.doctype.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L4161) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L186) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L535)

<a id="op-241507780b803d"></a>
### PWANotifications Mixin.get doc approver

`operation_workforce_mixins_pwa_notifications_business_behavior_progressive_web_application_notifications_mixin_get_record_approver`

**Inputs** self.

**Declared result** str.

**Explicit results** self.get(approver\_field).

**Local steps**

- Set APPROVER\_FIELD from mapping(“Leave Application” → “leave\_approver”, “Expense Claim” → “expense\_approver”, “Shift Request” → “approver”).
- Set approver\_field from APPROVER\_FIELD at self.doctype.
- Return self.get(approver\_field).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L4288) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L185) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L534)

<a id="op-6fac2cc138826d"></a>
### PWANotifications Mixin.get employee user

`operation_workforce_mixins_pwa_notifications_business_behavior_progressive_web_application_notifications_mixin_get_employee_user`

**Inputs** self.

**Declared result** str.

**Record and data access** read “Employee” via get\_value.

**Explicit results** Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).

**Local steps**

- Return Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L4445) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L184) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L533)

<a id="op-5fe1c5c9d395a1"></a>
### PWANotifications Mixin.get user name

`operation_workforce_mixins_pwa_notifications_business_behavior_progressive_web_application_notifications_mixin_get_user_name`

**Inputs** self, user.

**Declared result** str.

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.db.get\_value(“User”, user, “full\_name”, cache = true).

**Local steps**

- Return Platform.db.get\_value(“User”, user, “full\_name”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L4537) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L187) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L536)

## Service · Utils

<a id="op-1ff41c6e2e9272"></a>
### Calculate annual eligible hra exemption

`operation_workforce_regional_india_utils_business_behavior_calculate_annual_eligible_hra_exemption`

**Inputs** doc.

**Record and data access** read “Company” via get\_value · read “Payroll Period” via get\_value · read “Salary Structure” via get\_value.

**Explicit results** Platform.\_dict(mapping(“hra\_amount” → hra\_amount, “annual\_exemption” → annual\_exemption, “monthly\_exemption” → monthly\_exemption)).

**Explicit failure paths** validation helper — translated “Please set Basic and HRA component in Company {0}”.format(get\_link\_to\_form(“Company”, doc.company)) · validation helper — translated “Salary Structure must be submitted before submission of {0}”.format(doc.doctype).

**Local steps**

- Set tuple(basic\_component, hra\_component) from Platform.db.get\_value(“Company”, doc.company, list(“basic\_component”, “hra\_component”)).
- If not (basic\_component and hra\_component).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in basic\_component → hra\_component.
  - Call the validation error handler Platform.throw(translated “Please set Basic and HRA component in Company {0}”.format(get\_link\_to\_form(“Company”, doc.company))).
- Set annual\_exemption, monthly\_exemption, hra\_amount, basic\_amount from 0.
- If (hra\_component and basic\_component).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hra\_component → basic\_component.
  - Set assignments from get\_salary\_assignments(doc.employee, doc.payroll\_period).
  - If (not assignments and doc.docstatus equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not assignments → doc.docstatus equals 1.
    - Call the validation error handler Platform.throw(translated “Salary Structure must be submitted before submission of {0}”.format(doc.doctype)).
  - Set period\_start\_date from Platform.db.get\_value(“Payroll Period”, doc.payroll\_period, “start\_date”).
  - Set assignment\_dates from list().
  - For each assignment in assignments.
    - Set assignment.from\_date from max(assignment.from\_date, period\_start\_date).
    - Evaluate assignment\_dates.append(assignment.from\_date).
  - For each tuple(idx, assignment) in enumerate(assignments).
    - If has\_hra\_component(assignment.salary\_structure, hra\_component).
      - Set tuple(basic\_salary\_amt, hra\_salary\_amt) from get\_component\_amt\_from\_salary\_slip(doc.employee, assignment.salary\_structure, basic\_component, hra\_component, …).
      - Set to\_date from get\_end\_date\_for\_assignment(assignment\_dates, idx, doc.payroll\_period).
      - Set frequency from Platform.get\_value(“Salary Structure”, assignment.salary\_structure, “payroll\_frequency”).
      - Update basic\_amount using + get\_component\_pay(frequency, basic\_salary\_amt, assignment.from\_date, to\_date).
      - Update hra\_amount using + get\_component\_pay(frequency, hra\_salary\_amt, assignment.from\_date, to\_date).
  - If hra\_amount.
    - If doc.monthly\_house\_rent.
      - Set annual\_exemption from calculate\_hra\_exemption(assignment.salary\_structure, basic\_amount, hra\_amount, doc.monthly\_house\_rent, …).
      - If annual\_exemption &gt; 0.
        - Set monthly\_exemption from (annual\_exemption ÷ 12).
      - Otherwise.
        - Set annual\_exemption from 0.
- Return Platform.\_dict(mapping(“hra\_amount” → hra\_amount, “annual\_exemption” → annual\_exemption, “monthly\_exemption” → monthly\_exemption)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1068) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L19)

<a id="op-6c5c53d95ff6b5"></a>
### Has hra component

`operation_workforce_regional_india_utils_business_behavior_has_hra_component`

**Inputs** salary\_structure, hra\_component.

**Record and data access** read “Salary Detail” via exists.

**Explicit results** Platform.db.exists(“Salary Detail”, mapping(“parent” → salary\_structure, “salary\_component” → hra\_component, “parentfield” → “earnings”, “parenttype” → “Salary Structure”)).

**Local steps**

- Return Platform.db.exists(“Salary Detail”, mapping(“parent” → salary\_structure, “salary\_component” → hra\_component, “parentfield” → “earnings”, “parenttype” → “Salary Structure”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L1038) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1075) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L26)

<a id="op-94033f4ecca847"></a>
### Get end date for assignment

`operation_workforce_regional_india_utils_business_behavior_get_end_date_for_assignment`

**Inputs** assignment\_dates, idx, payroll\_period.

**Record and data access** read “Payroll Period” via get\_value.

**Explicit results** end\_date.

**Local steps**

- Set end\_date from no value.
- Attempt the following.
  - Set end\_date from assignment\_dates at (idx + 1).
  - Set end\_date from add\_days(end\_date, negative 1).
- On failure (IndexError).
  - Take no action here.
- If not end\_date.
  - Set end\_date from Platform.db.get\_value(“Payroll Period”, payroll\_period, “end\_date”).
- Return end\_date.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L1187) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1074) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L25)
