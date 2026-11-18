# Employment and attendance · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Expense claim

[Record definition](../../../../data/record-types/expense_claim.json)

<a id="op-47869cd80267a5"></a>
### Expense Claim.make gl entries

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_make_general_ledger_entries`

**Inputs** self, cancel = false.

**Local steps**

- If flt(self.total\_sanctioned\_amount) &gt; 0.
  - Set gl\_entries from self.get\_gl\_entries().
  - Evaluate make\_gl\_entries(gl\_entries, cancel).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries](operations-016.md#op-cab17b977bd758).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L2777) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L698) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L678)

<a id="op-cab17b977bd758"></a>
### Expense Claim.get gl entries

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_get_general_ledger_entries`

**Inputs** self.

**Explicit results** gl\_entry.

**Local steps**

- Set gl\_entry from list().
- Evaluate self.validate\_account\_details().
- If self.grand\_total.
  - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → self.payable\_account, “credit” → self.base\_grand\_total, “credit\_in\_account\_currency” → self.grand\_total, “credit\_in\_transaction\_currency” → self.grand\_t ….
    - Draw d from self.expenses.
- For each data in self.expenses.
  - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → data.default\_account, “debit” → data.base\_sanctioned\_amount, “debit\_in\_account\_currency” → data.sanctioned\_amount, “debit\_in\_transaction\_currency” → dat ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.cost\_center → self.cost\_center.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.project → self.project.
- For each data in self.advances.
  - If data.allocated\_amount.
    - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → data.advance\_account, “credit” → data.base\_allocated\_amount, “credit\_in\_account\_currency” → data.allocated\_amount, “credit\_in\_transaction\_currency” → da ….
      - Draw d from self.expenses.
- Evaluate self.add\_tax\_gl\_entries(gl\_entry).
- If (self.is\_paid and self.grand\_total).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_paid → self.grand\_total.
  - Set payment\_account from get\_bank\_cash\_account(self.mode\_of\_payment, self.company).get(“account”).
  - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → payment\_account, “credit” → self.base\_grand\_total, “credit\_in\_account\_currency” → self.grand\_total, “credit\_in\_transaction\_currency” → self.grand\_total, ….
  - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → self.payable\_account, “party\_type” → “Employee”, “party” → self.employee, “against” → payment\_account, …), account\_currency = self.currency, item = self)).
- Return gl\_entry.

**Methods declared on this owner** [validate account details](operations-016.md#op-e166d0d59ab241), [add tax gl entries](operations-016.md#op-068615063ce093).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L2909) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L696) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L676)

<a id="op-068615063ce093"></a>
### Expense Claim.add tax gl entries

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_add_tax_general_ledger_entries`

**Inputs** self, gl\_entries.

**Local steps**

- For each tax in self.get(“taxes”).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → tax.account\_head, “debit” → tax.base\_tax\_amount, “debit\_in\_account\_currency” → tax.tax\_amount, “debit\_in\_transaction\_currency” → tax.tax\_amount, …), a ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax.cost\_center → self.cost\_center.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax.project → self.project.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L4640) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L689) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L669)

<a id="op-26b98990fb58ed"></a>
### Expense Claim.set default accounting dimension

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_set_default_accounting_dimension`

**Inputs** self.

**Local steps**

- Bind dependencies get\_checks\_for\_pl\_and\_bs\_accounts.
- For each dim in get\_checks\_for\_pl\_and\_bs\_accounts().
  - If dim.company differs from self.company.
    - Continue with the next iteration or loop test.
  - Set field from Platform.scrub(dim.fieldname).
  - If self.meta.get\_field(field).
    - If (not self.get(field) and dim.mandatory\_for\_bs).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(field) → dim.mandatory\_for\_bs.
      - Evaluate self.set(field, dim.default\_dimension).
  - For each row in (self.get(“expenses”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“expenses”) → list().
    - If row.meta.get\_field(field).
      - If (not row.get(field) and dim.mandatory\_for\_pl).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.get(field) → dim.mandatory\_for\_pl.
        - Evaluate row.set(field, dim.default\_dimension).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L5007) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L708) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L688)

<a id="op-835248af996e8b"></a>
### Expense Claim.create exchange gain loss je

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_create_exchange_gain_loss_je`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** call db\_set on advance · call db\_set on self · msgprint with translated “All Exchange Gain/Loss amount of {0} has been booked through {1}”.format(self.name, get\_link\_to\_form(“Journal Entry”, je)).

**Explicit results** no value.

**Local steps**

- If not self.advances.
  - Return no value.
- Set per\_advance\_gain\_loss from 0.
- Set total\_advance\_exchange\_gain\_loss from 0.
- For each advance in self.advances.
  - If (advance.exchange\_rate and advance.base\_allocated\_amount and self.base\_total\_advance\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in advance.exchange\_rate → advance.base\_allocated\_amount → self.base\_total\_advance\_amount.
    - Set allocated\_amount\_in\_adv\_exchange\_rate from (flt(advance.allocated\_amount) × flt(advance.exchange\_rate)).
    - Update per\_advance\_gain\_loss using + flt((advance.base\_allocated\_amount − allocated\_amount\_in\_adv\_exchange\_rate), self.precision(“total\_exchange\_gain\_loss”)).
    - If per\_advance\_gain\_loss.
      - Evaluate advance.db\_set(“exchange\_gain\_loss”, per\_advance\_gain\_loss).
      - Update total\_advance\_exchange\_gain\_loss using + per\_advance\_gain\_loss.
- If total\_advance\_exchange\_gain\_loss.
  - Set gain\_loss\_account from Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”).
  - Evaluate self.db\_set(mapping(“total\_exchange\_gain\_loss” → total\_advance\_exchange\_gain\_loss, “gain\_loss\_account” → gain\_loss\_account)).
  - Set dr\_or\_cr from “credit” when self.total\_exchange\_gain\_loss &gt; 0, otherwise “debit”.
    - Value choice on self.total\_exchange\_gain\_loss &gt; 0 — true gives “credit”, false gives “debit”.
  - Set reverse\_dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
    - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
  - Set je from create\_gain\_loss\_journal(company = self.company, posting\_date = today(), party\_type = “Employee”, party = self.employee, …).
  - Evaluate Platform.msgprint(translated “All Exchange Gain/Loss amount of {0} has been booked through {1}”.format(self.name, get\_link\_to\_form(“Journal Entry”, je))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L5398) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L695) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L675)

<a id="op-e166d0d59ab241"></a>
### Expense Claim.validate account details

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_validate_account_details`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: {1} is required in the expenses table to book an expense claim.”.format(data.idx, Platform.bold(translated “Cost Center”)) · validation helper — translated “Mode of payment is required to make a payment”.format(self.employee).

**Local steps**

- For each data in self.expenses.
  - If not data.cost\_center.
    - Call the validation error handler Platform.throw(translated “Row {0}: {1} is required in the expenses table to book an expense claim.”.format(data.idx, Platform.bold(translated “Cost Center”))).
- For each data in self.advances.
  - Evaluate self.validate\_advance\_linkage(data).
- If self.is\_paid.
  - If not self.mode\_of\_payment.
    - Call the validation error handler Platform.throw(translated “Mode of payment is required to make a payment”.format(self.employee)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate advance linkage](operations-016.md#op-b790783ceac202).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L22) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L714) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L694)

<a id="op-f57aae3813a761"></a>
### Expense Claim.set company currency if multi currency disabled

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_set_company_currency_if_multi_currency_disabled`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If Platform.db.get\_single\_value(“HR Settings”, “enable\_multi\_currency\_expense\_claim”).
  - Return no value.
- Set self.currency from Enterprise.get\_company\_currency(self.company).
- Set self.exchange\_rate from 1.0.
- For each advance in self.get(“advances”).
  - Set advance.exchange\_rate from 1.0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “enable\_multi\_currency\_expense\_claim”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0027.json#L6516) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L707) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L687)

<a id="op-b2f7843b631e96"></a>
### Expense Claim.calculate total amount

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_calculate_total_amount`

**Inputs** self.

**Local steps**

- Set self.total\_claimed\_amount from 0.
- Set self.total\_sanctioned\_amount from 0.
- For each d in self.get(“expenses”).
  - Evaluate self.round\_floats\_in(d).
  - If self.approval\_status equals “Rejected”.
    - Set d.sanctioned\_amount from 0.0.
  - Update self.total\_claimed\_amount using + flt(d.amount).
  - Update self.total\_sanctioned\_amount using + flt(d.sanctioned\_amount).
  - Evaluate self.set\_base\_fields\_amount(d, list(“amount”, “sanctioned\_amount”)).
- Evaluate self.set\_base\_fields\_amount(self, list(“total\_sanctioned\_amount”, “total\_claimed\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set base fields amount](operations-016.md#op-048deebb7407bb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L694) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L674)

<a id="op-048deebb7407bb"></a>
### Expense Claim.set base fields amount

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_set_base_fields_amount`

**Inputs** self, doc, fields, exchange\_rate = no value.

**Local steps**

- For each f in fields.
  - Set val from flt((flt(doc.get(f), doc.precision(f)) × flt(exchange\_rate when exchange\_rate, otherwise self.exchange\_rate)), doc.precision((“base\_” + f))).
    - Value choice on exchange\_rate — true gives exchange\_rate, false gives self.exchange\_rate.
  - Evaluate doc.set((“base\_” + f), val).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L332) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L706) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L686)

<a id="op-1da6ab118df7b2"></a>
### Expense Claim.calculate taxes

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_calculate_taxes`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set self.total\_taxes\_and\_charges from 0.
- For each tax in self.taxes.
  - Evaluate self.round\_floats\_in(tax).
  - If tax.rate.
    - Set tax.tax\_amount from flt((flt(self.total\_sanctioned\_amount) × flt((flt(tax.rate) ÷ 100))), tax.precision(“tax\_amount”)).
  - Set tax.total from (flt(tax.tax\_amount) + flt(self.total\_sanctioned\_amount)).
  - Update self.total\_taxes\_and\_charges using + flt(tax.tax\_amount).
  - Evaluate self.set\_base\_fields\_amount(tax, list(“tax\_amount”, “total”)).
- Evaluate self.round\_floats\_in(self, list(“total\_taxes\_and\_charges”)).
- Set self.grand\_total from ((flt(self.total\_sanctioned\_amount) + flt(self.total\_taxes\_and\_charges)) − flt(self.total\_advance\_amount)).
- Evaluate self.round\_floats\_in(self, list(“grand\_total”)).
- Evaluate self.set\_base\_fields\_amount(self, list(“grand\_total”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set base fields amount](operations-016.md#op-048deebb7407bb).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L570) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L693) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L673)

<a id="op-9fe56a156c3569"></a>
### Expense Claim.validate advances

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_validate_advances`

**Inputs** self.

**Local steps**

- Set self.total\_advance\_amount from 0.
- Set precision from self.precision(“total\_advance\_amount”).
- For each d in self.get(“advances”).
  - Evaluate self.validate\_advance\_row(d, precision).
  - Update self.total\_advance\_amount using + flt(d.allocated\_amount).
  - Evaluate self.set\_base\_fields\_amount(d, list(“advance\_paid”, “unclaimed\_amount”), d.exchange\_rate).
  - Evaluate self.set\_base\_fields\_amount(d, list(“allocated\_amount”)).
- If self.total\_advance\_amount.
  - Evaluate self.validate\_total\_advance\_amount(precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate advance row](operations-016.md#op-8294191a8428ef), [set base fields amount](operations-016.md#op-048deebb7407bb), [validate total advance amount](operations-016.md#op-cb81b54603ca25).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L23) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L715) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L695)

<a id="op-8294191a8428ef"></a>
### Expense Claim.validate advance row

`operation_workforce_binding_workforce_hr_doctype_expense_claim_expense_claim_expenseclaim_validate_advance_row`

**Inputs** self, d, precision.

**Record and data access** read “Employee Advance” via get\_value.

**Explicit failure paths** validation helper — translated “Selected employee advance is not of employee {}”.format(self.employee) · validation helper — translated “Row {0}# Allocated amount {1} cannot be greater than unclaimed amount {2}”.format(d.idx, d.allocated\_amount, d.unclaimed\_amount).

**Local steps**

- Set advance\_details from Platform.db.get\_value(“Employee Advance”, d.employee\_advance, list(“employee”, “currency”, “advance\_account”, “paid\_amount”), as\_dict = true).
- If (not advance\_details or self.employee differs from advance\_details.employee).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not advance\_details → self.employee differs from advance\_details.employee.
  - Call the validation error handler Platform.throw(translated “Selected employee advance is not of employee {}”.format(self.employee)).
- Evaluate validate\_employee\_advance\_currency\_and\_account(self, d.employee\_advance, advance\_details).
- Evaluate self.validate\_advance\_linkage(d).
- Evaluate self.round\_floats\_in(d).
- If (d.allocated\_amount and flt(d.allocated\_amount) &gt; flt((flt(d.unclaimed\_amount) − flt(d.return\_amount)), precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.allocated\_amount → flt(d.allocated\_amount) &gt; flt((flt(d.unclaimed\_amount) − flt(d.return\_amount)), precision).
  - Call the validation error handler Platform.throw(translated “Row {0}# Allocated amount {1} cannot be greater than unclaimed amount {2}”.format(d.idx, d.allocated\_amount, d.unclaimed\_amount)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate advance linkage](operations-016.md#op-b790783ceac202).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L57) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L108) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L108)

<a id="op-b790783ceac202"></a>
### Expense Claim.validate advance linkage

`operation_workforce_binding_workforce_hr_doctype_expense_claim_expense_claim_expenseclaim_validate_advance_linkage`

**Inputs** self, d.

**Explicit failure paths** validation helper — translated “Row {0}: {1}, {2} and {3} are required against advance {4}.”.format(d.idx, Platform.bold(translated “Advance Account”), Platform.bold(translated “Reference Type”), Platform.bold(translated “Ref ….

**Local steps**

- If (d.allocated\_amount and not (d.advance\_account and d.reference\_type and d.reference\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.allocated\_amount → not (d.advance\_account and d.reference\_type and d.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.advance\_account → d.reference\_type → d.reference\_name.
  - Call the validation error handler Platform.throw(translated “Row {0}: {1}, {2} and {3} are required against advance {4}.”.format(d.idx, Platform.bold(translated “Advance Account”), Platform.bold(translated “Reference Type”), Platform.bold( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L56) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L107) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L107)

<a id="op-cb81b54603ca25"></a>
### Expense Claim.validate total advance amount

`operation_workforce_binding_workforce_hr_doctype_expense_claim_expense_claim_expenseclaim_validate_total_advance_amount`

**Inputs** self, precision.

**Explicit failure paths** validation helper — translated “Total advance amount cannot be greater than total sanctioned amount”.

**Local steps**

- Evaluate self.round\_floats\_in(self, list(“total\_advance\_amount”)).
- Set amount\_with\_taxes from flt((flt(self.total\_sanctioned\_amount, precision) + flt(self.total\_taxes\_and\_charges, precision)), precision).
- Evaluate self.set\_base\_fields\_amount(self, list(“total\_advance\_amount”)).
- If flt(self.total\_advance\_amount, precision) &gt; amount\_with\_taxes.
  - Call the validation error handler Platform.throw(translated “Total advance amount cannot be greater than total sanctioned amount”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set base fields amount](operations-016.md#op-048deebb7407bb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L59) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L110) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L110)

<a id="op-b4b05bbea02d5d"></a>
### Expense Claim.validate sanctioned amount

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_validate_sanctioned_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Sanctioned Amount cannot be greater than Claim Amount in Row {0}.”.format(d.idx).

**Local steps**

- For each d in self.get(“expenses”).
  - If flt(d.sanctioned\_amount) &gt; flt(d.amount).
    - Call the validation error handler Platform.throw(translated “Sanctioned Amount cannot be greater than Claim Amount in Row {0}.”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L2045) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L718) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L698)

<a id="op-163bc2cec64851"></a>
### Expense Claim.set expense account

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_expense_claim_set_expense_account`

**Inputs** self, validate = false.

**Local steps**

- For each expense in self.expenses.
  - If (not expense.default\_account or not validate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not expense.default\_account → not validate.
    - Set expense.default\_account from get\_expense\_claim\_account(expense.expense\_type, self.company) at “account”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L2227) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L709) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L689)

<a id="op-9d748d9691a927"></a>
### Update reimbursed amount

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_update_reimbursed_amount`

**Inputs** doc.

**State and service calls** request set\_value on “Expense Claim”.

**Local steps**

- Set total\_amount\_reimbursed from get\_total\_reimbursed\_amount(doc).
- Set doc.total\_amount\_reimbursed from total\_amount\_reimbursed.
- Evaluate Platform.db.set\_value(“Expense Claim”, doc.name, “total\_amount\_reimbursed”, total\_amount\_reimbursed).
- Evaluate doc.set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L2375) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L731) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L711)

<a id="op-6283531f0ead78"></a>
### Get total reimbursed amount

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_total_reimbursed_amount`

**Inputs** doc.

**Record and data access** read “Journal Entry Account” via get\_value · read “Payment Entry Reference” via get\_value.

**Explicit results** doc.grand\_total · (flt(amount\_via\_jv) + flt(amount\_via\_payment\_entry)).

**Local steps**

- If doc.is\_paid.
  - Return doc.grand\_total.
- Otherwise.
  - Set JournalEntryAccount from Platform.qb.DocType(“Journal Entry Account”).
  - Set amount\_via\_jv from Platform.db.get\_value(“Journal Entry Account”, mapping(“reference\_name” → doc.name, “docstatus” → 1), Sum((JournalEntryAccount.debit\_in\_account\_currency − JournalEntryAccount.credit\_in\_account\_currency))).
  - Set amount\_via\_payment\_entry from Platform.db.get\_value(“Payment Entry Reference”, mapping(“reference\_name” → doc.name, “advance\_voucher\_type” → no value, “docstatus” → 1), list(mapping(“SUM” → “allocated\_amount”))).
  - Return (flt(amount\_via\_jv) + flt(amount\_via\_payment\_entry)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L2534) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L727) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L707)

<a id="op-9a371b755bdc04"></a>
### Get outstanding amount for claim

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_outstanding_amount_for_claim`

**Inputs** claim.

**Record and data access** read “Expense Claim” via get\_value.

**Explicit results** flt(outstanding\_amt, precision).

**Local steps**

- Set precision from Platform.get\_precision(“Expense Claim”, “grand\_total”).
- If isinstance(claim, str).
  - Set claim from Platform.db.get\_value(“Expense Claim”, claim, tuple(“total\_sanctioned\_amount”, “total\_taxes\_and\_charges”, “total\_amount\_reimbursed”, “total\_advance\_amount”), as\_dict = true).
- Set outstanding\_amt from (((flt(claim.total\_sanctioned\_amount) + flt(claim.total\_taxes\_and\_charges)) − flt(claim.total\_amount\_reimbursed)) − flt(claim.total\_advance\_amount)).
- Return flt(outstanding\_amt, precision).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L2901) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L726) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L706)

<a id="op-3f2a5521cd73bb"></a>
### Get expense claim account and cost center

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_expense_claim_account_and_cost_center`

**Inputs** expense\_claim\_type, company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“account” → data.get(“account”), “cost\_center” → cost\_center).

**Local steps**

- Set data from get\_expense\_claim\_account(expense\_claim\_type, company).
- Set cost\_center from Enterprise.get\_default\_cost\_center(company).
- Return mapping(“account” → data.get(“account”), “cost\_center” → cost\_center).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L3217) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L724) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L704)

<a id="op-43fe916834db31"></a>
### Get expense claim account

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_expense_claim_account`

**Inputs** expense\_claim\_type, company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Expense Claim Account” via get\_value.

**Explicit results** mapping(“account” → account).

**Explicit failure paths** validation helper — translated “Set the default account for the {0} {1}”.format(Platform.bold(translated “Expense Claim Type”), get\_link\_to\_form(“Expense Claim Type”, expense\_claim\_type)).

**Local steps**

- Set account from Platform.db.get\_value(“Expense Claim Account”, mapping(“parent” → expense\_claim\_type, “company” → company), “default\_account”).
- If not account.
  - Call the validation error handler Platform.throw(translated “Set the default account for the {0} {1}”.format(Platform.bold(translated “Expense Claim Type”), get\_link\_to\_form(“Expense Claim Type”, expense\_claim\_type))).
- Return mapping(“account” → account).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L3409) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L723) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L703)

<a id="op-fc0c55c9ff1f77"></a>
### Validate employee advance currency and account

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_validate_employee_advance_currency_and_account`

**Inputs** expense\_claim, employee\_advance, advance\_details = no value.

**Declared result** no value.

**Record and data access** read “Employee Advance” via get\_value · read “Account” via get\_value · read “Advance Payment Ledger Entry” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Employee Advance {0} is in currency {1} and can only be claimed in an Expense Claim of the same currency. Th …”.format(Platform.bold(employee\_advance), Platform.bold(advance\_details.currency),  … · validation helper — translated “Employee Advance {0} is linked to account {1}, which is not of type Receivable. {2}”.format(Platform.bold(employee\_advance), Platform.bold(advance\_details.advance\_account), redo\_payment\_msg) · validation helper — translated “Employee Advance {0} is linked to account {1}, which is not of type Receivable. Please correct the account t …”.format(Platform.bold(employee\_advance), Platform.bold(advance\_details.advance\_account)) · validation helper — translated “Employee Advance {0}'s payment does not match its Receivable account. This can happen if the account's type  …”.format(Platform.bold(employee\_advance), redo\_payment\_msg).

**Local steps**

- If advance\_details is identical to no value.
  - Set advance\_details from Platform.db.get\_value(“Employee Advance”, mapping(“name” → employee\_advance, “employee” → expense\_claim.employee), list(“currency”, “advance\_account”, “paid\_amount”), as\_dict = true).
- If not advance\_details.
  - Return no value.
- If (expense\_claim.currency and advance\_details.currency differs from expense\_claim.currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expense\_claim.currency → advance\_details.currency differs from expense\_claim.currency.
  - Call the validation error handler Platform.throw(translated “Employee Advance {0} is in currency {1} and can only be claimed in an Expense Claim of the same currency. Th …”.format(Platform.bold(employee\_advance), Platform.bold(advance\_deta ….
- Set paid\_amount from flt(advance\_details.paid\_amount).
- Set redo\_payment\_msg from translated “Cancel the Payment Entry made against it, correct the advance account to be of type Receivable, and create a …”.
- Set account\_type from Platform.db.get\_value(“Account”, advance\_details.advance\_account, “account\_type”).
- If account\_type differs from “Receivable”.
  - If paid\_amount.
    - Call the validation error handler Platform.throw(translated “Employee Advance {0} is linked to account {1}, which is not of type Receivable. {2}”.format(Platform.bold(employee\_advance), Platform.bold(advance\_details.advance\_account), redo\_ ….
  - Call the validation error handler Platform.throw(translated “Employee Advance {0} is linked to account {1}, which is not of type Receivable. Please correct the account t …”.format(Platform.bold(employee\_advance), Platform.bold(advance\_deta ….
- If (paid\_amount and not Platform.db.exists(“Advance Payment Ledger Entry”, mapping(“against\_voucher\_type” → “Employee Advance”, “against\_voucher\_no” → employee\_advance, “event” → “Submit”, “delinked” → 0, …))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in paid\_amount → not Platform.db.exists(“Advance Payment Ledger Entry”, mapping(“against\_voucher\_type” → “Employee Advance”, “against\_voucher\_no” → employee\_advance, “event” → “Submit”, “delinked” → 0, …)).
  - Call the validation error handler Platform.throw(translated “Employee Advance {0}'s payment does not match its Receivable account. This can happen if the account's type  …”.format(Platform.bold(employee\_advance), redo\_payment\_msg)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L3718) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L732) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L712)

<a id="op-f813a2a8bd2f69"></a>
### Get advances

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_advances`

**Inputs** expense\_claim, advance\_id = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from expense\_claim via get\_doc.

**Explicit results** expense\_claim\_doc.advances.

**Local steps**

- Bind dependencies json.
- If isinstance(expense\_claim, str).
  - Set expense\_claim from Platform.\_dict(json.loads(expense\_claim)).
- Set expense\_claim\_doc from Platform.get\_doc(expense\_claim).
- Evaluate Platform.has\_permission(“Employee”, “read”, expense\_claim\_doc.employee, throw = true).
- Set expense\_claim\_doc.advances from list().
- Set advance from Platform.qb.DocType(“Employee Advance”).
- Set query from Platform.qb.from\_(advance).select(advance.name, advance.purpose, advance.posting\_date, advance.paid\_amount, …).
- If not advance\_id.
  - Set query from query.where((((advance.docstatus equals 1 bitwise and advance.employee equals expense\_claim\_doc.employee) bitwise and advance.paid\_amount &gt; 0) bitwise and advance.status.notin(list(“Claimed”, “Returned”, “ ….
  - If expense\_claim\_doc.currency.
    - Set query from query.where(advance.currency equals expense\_claim\_doc.currency).
- Otherwise.
  - Set query from query.where((advance.name equals advance\_id bitwise and advance.employee equals expense\_claim\_doc.employee)).
  - Evaluate validate\_employee\_advance\_currency\_and\_account(expense\_claim\_doc, advance\_id).
- Set advances from query.run(as\_dict = true).
- For each advance in advances.
  - Evaluate get\_expense\_claim\_advances(expense\_claim\_doc, advance).
- Return expense\_claim\_doc.advances.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, expense\_claim\_doc.employee, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L4673) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L719) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L699)

<a id="op-5e54b369864a9b"></a>
### Get expense claim

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_expense_claim`

**Inputs** employee\_advance.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** resolve a document from “Employee Advance” via get\_doc · read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Expense Claim”.

**Explicit results** expense\_claim.

**Local steps**

- Evaluate Platform.has\_permission(“Employee Advance”, “read”, employee\_advance, throw = true).
- If isinstance(employee\_advance, str).
  - Set employee\_advance from Platform.get\_doc(“Employee Advance”, employee\_advance).
- Set company from employee\_advance.company.
- Set default\_cost\_center from Platform.get\_cached\_value(“Company”, company, “cost\_center”).
- Set expense\_claim from Platform.new\_doc(“Expense Claim”).
- Set expense\_claim.company from company.
- Set expense\_claim.currency from employee\_advance.currency.
- Set expense\_claim.employee from employee\_advance.employee.
- Set expense\_claim.payable\_account from get\_default\_payable\_account(company) when employee\_advance.currency equals Enterprise.get\_company\_currency(company), otherwise no value.
  - Value choice on employee\_advance.currency equals Enterprise.get\_company\_currency(company) — true gives get\_default\_payable\_account(company), false gives no value.
- Set expense\_claim.cost\_center from default\_cost\_center.
- Set expense\_claim.is\_paid from 1 when flt(employee\_advance.paid\_amount), otherwise 0.
  - Value choice on flt(employee\_advance.paid\_amount) — true gives 1, false gives 0.
- Evaluate get\_expense\_claim\_advances(expense\_claim, employee\_advance).
- Return expense\_claim.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee Advance”, “read”, employee\_advance, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L5496) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L722) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L702)
