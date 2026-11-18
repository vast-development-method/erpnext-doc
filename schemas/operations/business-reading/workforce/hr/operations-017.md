# Employment and attendance · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Expense claim

[Record definition](../../../../data/record-types/expense_claim.json)

<a id="op-9a37ba116c77de"></a>
### Get default payable account

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_default_payable_account`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** (Platform.get\_cached\_value(“Company”, company, “default\_expense\_claim\_payable\_account”) or Platform.get\_cached\_value(“Company”, company, “default\_payroll\_payable\_account”)).

**Local steps**

- Evaluate Platform.has\_permission(“Company”, “read”, company, throw = true).
- Return (Platform.get\_cached\_value(“Company”, company, “default\_expense\_claim\_payable\_account”) or Platform.get\_cached\_value(“Company”, company, “default\_payroll\_payable\_account”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Company”, company, “default\_expense\_claim\_payable\_account”) → Platform.get\_cached\_value(“Company”, company, “default\_payroll\_payable\_account”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, company, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_expense\_claim\_payable\_account”), Platform.get\_cached\_value(“Company”, company, “default\_payroll\_payable\_account”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0028.json#L6006) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L721) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L701)

<a id="op-9f02c40f1b9677"></a>
### Get expense claim advances

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_expense_claim_advances`

**Inputs** expense\_claim, employee\_advance.

**Record and data access** read “Advance Payment Ledger Entry” via get\_all.

**Explicit results** no value.

**Local steps**

- Set advance\_payments from Platform.get\_all(“Advance Payment Ledger Entry”, filters = mapping(“company” → expense\_claim.company, “against\_voucher\_type” → “Employee Advance”, “against\_voucher\_no” → employee\_advance.name, “event” → “S ….
- If not advance\_payments.
  - Return no value.
- Evaluate advance\_payments.sort(key = deferred anonymous expression).
- Set advance\_payment\_voucher\_nos from list of payment at “voucher\_no” for payment drawn from advance\_payments.
  - Draw payment from advance\_payments.
- Set claimed\_payments from Platform.get\_all(“Advance Payment Ledger Entry”, filters = mapping(“company” → expense\_claim.company, “event” → “Adjustment”, “against\_voucher\_no” → list(“in”, advance\_payment\_voucher\_nos), “delinked” → fa ….
- Set adjustment\_map from mapping().
- For each adjustment\_entry in claimed\_payments.
  - Set payment\_reference from tuple(adjustment\_entry at “against\_voucher\_type”, adjustment\_entry at “against\_voucher\_no”).
  - Set adjustment\_map at payment\_reference from (adjustment\_map.get(payment\_reference, 0) + abs(adjustment\_entry at “amount”)).
- For each advance in advance\_payments.
  - Set paid\_amount from flt(advance at “amount”).
  - Set claimed\_amount from adjustment\_map.get(tuple(advance at “voucher\_type”, advance at “voucher\_no”), 0).
  - Set unclaimed\_amount from (paid\_amount − claimed\_amount).
  - Set return\_amount from flt(employee\_advance.return\_amount).
  - Set allocated\_amount from get\_allocation\_amount(paid\_amount = paid\_amount, claimed\_amount = claimed\_amount, return\_amount = return\_amount).
  - Evaluate expense\_claim.append(“advances”, mapping(“advance\_account” → employee\_advance.advance\_account, “employee\_advance” → employee\_advance.name, “posting\_date” → employee\_advance.posting\_date, “advance\_paid” → p ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L725) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L705)

<a id="op-bdc06509347767"></a>
### Update payment for expense claim

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_update_payment_for_expense_claim`

**Inputs** doc, method = no value.

**Record and data access** resolve a document from “Expense Claim” via get\_doc.

**Explicit results** no value.

**Local steps**

- If (doc.doctype equals “Payment Entry” and not (doc.payment\_type equals “Pay” and doc.party)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Payment Entry” → not (doc.payment\_type equals “Pay” and doc.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.payment\_type equals “Pay” → doc.party.
  - Return no value.
- Set doctype\_field\_map from mapping(“Journal Entry” → list(“accounts”, “reference\_type”), “Payment Entry” → list(“references”, “reference\_doctype”), “Unreconcile Payment” → list(“allocations”, “reference\_doctype”)).
- Set tuple(payment\_table, doctype\_field) from doctype\_field\_map at doc.doctype.
- For each d in doc.get(payment\_table).
  - If (d.get(doctype\_field) equals “Expense Claim” and d.reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(doctype\_field) equals “Expense Claim” → d.reference\_name.
    - Set expense\_claim from Platform.get\_doc(“Expense Claim”, d.reference\_name).
    - Evaluate update\_reimbursed\_amount(expense\_claim).
    - If doc.doctype equals “Payment Entry”.
      - Evaluate update\_outstanding\_amount\_in\_payment\_entry(expense\_claim, d.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L1207) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L730) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L710)

<a id="op-5d0a1380f32909"></a>
### Update outstanding amount in payment entry

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_update_outstanding_amount_in_payment_entry`

**Inputs** expense\_claim, pe\_reference.

**State and service calls** request set\_value on “Payment Entry Reference”.

**Local steps**

- Set outstanding\_amount from get\_outstanding\_amount\_for\_claim(expense\_claim).
- Evaluate Platform.db.set\_value(“Payment Entry Reference”, pe\_reference, “outstanding\_amount”, outstanding\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L1695) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L729) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L709)

<a id="op-b9bd0c42eedcda"></a>
### Validate expense claim in jv

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_validate_expense_claim_in_journal_voucher`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row No {0}: Amount cannot be greater than the Outstanding Amount against Expense Claim {1}. Outstanding Amou …”.format(d.idx, d.reference\_name, outstanding\_amt).

**Local steps**

- If doc.voucher\_type equals “Exchange Gain Or Loss”.
  - Return no value.
- For each d in doc.accounts.
  - If d.reference\_type equals “Expense Claim”.
    - Set outstanding\_amt from get\_outstanding\_amount\_for\_claim(d.reference\_name).
    - If (d.debit and d.debit &gt; outstanding\_amt).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.debit → d.debit &gt; outstanding\_amt.
      - Call the validation error handler Platform.throw(translated “Row No {0}: Amount cannot be greater than the Outstanding Amount against Expense Claim {1}. Outstanding Amou …”.format(d.idx, d.reference\_name, outstanding\_amt)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L1820) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L733) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L713)

<a id="op-34be8445328134"></a>
### Make expense claim for delivery trip

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_make_expense_claim_for_delivery_trip`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Explicit results** doc.

**Local steps**

- Set doc from get\_mapped\_doc(“Delivery Trip”, source\_name, mapping(“Delivery Trip” → mapping(“doctype” → “Expense Claim”, “field\_map” → mapping(“name” → “delivery\_trip”))), target\_doc).
- Return doc.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L2088) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L728) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L708)

<a id="op-b505d911336e0e"></a>
### Get allocation amount

`operation_workforce_human_resources_record_definitions_expense_claim_business_behavior_get_allocation_amount`

**Inputs** paid\_amount = no value, claimed\_amount = no value, return\_amount = no value, unclaimed\_amount = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (float bitwise or no value).

**Explicit results** (flt(unclaimed\_amount) − flt(return\_amount)) · (flt(paid\_amount) − (flt(claimed\_amount) + flt(return\_amount))).

**Explicit failure paths** validation helper — translated “Invalid parameters provided. Please pass the required arguments.”.

**Local steps**

- If (unclaimed\_amount is distinct from no value and return\_amount is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in unclaimed\_amount is distinct from no value → return\_amount is distinct from no value.
  - Return (flt(unclaimed\_amount) − flt(return\_amount)).
- Otherwise.
  - If (paid\_amount is distinct from no value and claimed\_amount is distinct from no value and return\_amount is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in paid\_amount is distinct from no value → claimed\_amount is distinct from no value → return\_amount is distinct from no value.
    - Return (flt(paid\_amount) − (flt(claimed\_amount) + flt(return\_amount))).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid parameters provided. Please pass the required arguments.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L2300) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L720) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L700)

<a id="op-eabb09ed10dde2"></a>
### Get data

`operation_workforce_human_resources_record_definitions_expense_claim_expense_claim_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “reference\_name”, “internal\_links” → mapping(“Employee Advance” → list(“advances”, “employee\_advance”)), “transactions” → list(mapping(“label” → translated “Payment”, “items” → list(“ ….

**Local steps**

- Return mapping(“fieldname” → “reference\_name”, “internal\_links” → mapping(“Employee Advance” → list(“advances”, “employee\_advance”)), “transactions” → list(mapping(“label” → translated “Payment”, “items” → list(“ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0029.json#L2719) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L734) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L714)

## Record · Expense claim type

[Record definition](../../../../data/record-types/expense_claim_type.json)

<a id="op-94177caceffd26"></a>
### Expense Claim Type.validate

`operation_workforce_human_resources_record_definitions_expense_claim_type_business_behavior_expense_claim_type_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_accounts().
- Evaluate self.validate\_repeating\_companies().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate accounts](operations-017.md#op-d93edfefa2b135), [validate repeating companies](operations-017.md#op-794e83801670b2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L2964) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L778) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L758)

<a id="op-794e83801670b2"></a>
### Expense Claim Type.validate repeating companies

`operation_workforce_human_resources_record_definitions_expense_claim_type_business_behavior_expense_claim_type_validate_repeating_companies`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Same Company is entered more than once”.

**Local steps**

- Set accounts\_list from list().
- For each entry in self.accounts.
  - Evaluate accounts\_list.append(entry.company).
- If len(accounts\_list) differs from len(set(accounts\_list)).
  - Call the validation error handler Platform.throw(translated “Same Company is entered more than once”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3035) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L780) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L760)

<a id="op-d93edfefa2b135"></a>
### Expense Claim Type.validate accounts

`operation_workforce_human_resources_record_definitions_expense_claim_type_business_behavior_expense_claim_type_validate_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Account {0} does not match with Company {1}”.format(entry.default\_account, entry.company).

**Local steps**

- For each entry in self.accounts.
  - If Platform.db.get\_value(“Account”, entry.default\_account, “company”) differs from entry.company.
    - Call the validation error handler Platform.throw(translated “Account {0} does not match with Company {1}”.format(entry.default\_account, entry.company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3222) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L779) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L759)

## Record · Full and final statement

[Record definition](../../../../data/record-types/full_and_final_statement.json)

<a id="op-bc0e420f0f6bd8"></a>
### Fulland Final Statement.before insert

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_before_insert`

**Inputs** self.

**Local steps**

- Set self.status from “Unpaid”.
- Evaluate self.get\_outstanding\_statements().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get outstanding statements](operations-017.md#op-053e66db2a7d34).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3408) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L782) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L762)

<a id="op-f0aaaabd28dd97"></a>
### Fulland Final Statement.validate

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_relieving\_date().
- Evaluate self.get\_assets\_statements().
- Evaluate self.set\_total\_asset\_recovery\_cost().
- Evaluate self.set\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate relieving date](operations-017.md#op-c26108ec927805), [get assets statements](operations-017.md#op-101daa9f722c0f), [set total asset recovery cost](operations-017.md#op-bbd229e211c071), [set totals](operations-017.md#op-2a0ee0a051810d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3476) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L798) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L778)

<a id="op-36fb494c45eed5"></a>
### Fulland Final Statement.before submit

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_settlement(“payables”).
- Evaluate self.validate\_settlement(“receivables”).
- Evaluate self.validate\_assets().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate settlement](operations-017.md#op-164eddb059e0af), [validate assets](operations-017.md#op-edfb12185b5f19).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3587) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L783) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L763)

<a id="op-b36bc14374a964"></a>
### Fulland Final Statement.on submit

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_on_submit`

**Inputs** self.

**Local steps**

- Evaluate process\_loan\_accrual(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3697) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L793) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L773)

<a id="op-0fff385e477004"></a>
### Fulland Final Statement.on cancel

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”).
- Evaluate cancel\_loan\_repayment(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3749) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L791) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L771)

<a id="op-3eceaff90ee51d"></a>
### Fulland Final Statement.on discard

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3828) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L792) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L772)

<a id="op-c26108ec927805"></a>
### Fulland Final Statement.validate relieving date

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_validate_relieving_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please set {0} for Employee {1}”.format(Platform.bold(translated “Relieving Date”), get\_link\_to\_form(“Employee”, self.employee)).

**Local steps**

- If not self.relieving\_date.
  - Call the validation error handler Platform.throw(translated “Please set {0} for Employee {1}”.format(Platform.bold(translated “Relieving Date”), get\_link\_to\_form(“Employee”, self.employee)), title = translated “Missing Relieving Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L3891) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L800) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L780)

<a id="op-164eddb059e0af"></a>
### Fulland Final Statement.validate settlement

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_validate_settlement`

**Inputs** self, component\_type.

**Explicit failure paths** validation helper — translated “Settle all Payables and Receivables before submission”.

**Local steps**

- For each data in self.get(component\_type, list()).
  - If data.status equals “Unsettled”.
    - Call the validation error handler Platform.throw(translated “Settle all Payables and Receivables before submission”, title = translated “Unsettled Transactions”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L4082) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L801) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L781)

<a id="op-edfb12185b5f19"></a>
### Fulland Final Statement.validate assets

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_validate_assets`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set pending\_returns from list().
- For each data in self.assets\_allocated.
  - If data.action equals “Return”.
    - If data.status equals “Owned”.
      - Evaluate pending\_returns.append(translated “Row {0}: {1}”.format(data.idx, Platform.bold(data.asset\_name))).
  - Otherwise.
    - If data.action equals “Recover Cost”.
      - Set data.status from “Owned”.
- If pending\_returns.
  - Set msg from translated “All allocated assets should be returned before submission”.
  - Update msg using + text in the contract.
  - Update msg using + “, ”.join(generator of d for d drawn from pending\_returns).
    - Draw d from pending\_returns.
  - Call the validation error handler Platform.throw(msg, title = translated “Pending Asset Returns”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L4245) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L799) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L779)

<a id="op-053e66db2a7d34"></a>
### Fulland Final Statement.get outstanding statements

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_get_outstanding_statements`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — translated “Set Relieving Date for Employee: {0}”.format(get\_link\_to\_form(“Employee”, self.employee)).

**Local steps**

- If not self.relieving\_date.
  - Call the validation error handler Platform.throw(translated “Set Relieving Date for Employee: {0}”.format(get\_link\_to\_form(“Employee”, self.employee))).
- If not self.payables.
  - Evaluate self.add\_withheld\_salary\_slips().
  - Set components from self.get\_payable\_component().
  - Evaluate self.create\_component\_row(components, “payables”).
- Evaluate self.add\_outstanding\_employee\_advances().
- Evaluate self.create\_component\_row(self.get\_receivable\_component(), “receivables”).
- Evaluate self.get\_assets\_statements().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add withheld salary slips](operations-018.md#op-25265f89ef1eb3), [get payable component](operations-018.md#op-2a13f221c00cdb), [create component row](operations-018.md#op-77aa664332b342), [add outstanding employee advances](operations-018.md#op-7cb40b1036f35c), [get receivable component](operations-018.md#op-3fa345ff7f5eae), [get assets statements](operations-017.md#op-101daa9f722c0f).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L26) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L788) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L768)

<a id="op-101daa9f722c0f"></a>
### Fulland Final Statement.get assets statements

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_get_assets_statements`

**Inputs** self.

**Local steps**

- If not len(self.get(“assets\_allocated”, list())).
  - For each data in self.get\_assets\_movement().
    - Evaluate self.append(“assets\_allocated”, data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get assets movement](operations-018.md#op-735b7e11eee3ac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L4978) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L787) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L767)

<a id="op-bbd229e211c071"></a>
### Fulland Final Statement.set total asset recovery cost

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_set_total_asset_recovery_cost`

**Inputs** self.

**Local steps**

- Set total\_cost from 0.
- For each data in self.assets\_allocated.
  - If data.action equals “Recover Cost”.
    - If not data.description.
      - Set data.description from translated “Asset Recovery Cost for {0}: {1}”.format(data.reference, data.asset\_name).
    - Update total\_cost using + flt(data.cost).
- Set self.total\_asset\_recovery\_cost from flt(total\_cost, self.precision(“total\_asset\_recovery\_cost”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L5121) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L794) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L774)

<a id="op-2a0ee0a051810d"></a>
### Fulland Final Statement.set totals

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_set_totals`

**Inputs** self.

**Local steps**

- Set total\_payable from sum(generator of flt(row.amount) for row drawn from self.payables).
  - Draw row from self.payables.
- Set total\_receivable from sum(generator of flt(row.amount) for row drawn from self.receivables).
  - Draw row from self.receivables.
- Set self.total\_payable\_amount from flt(total\_payable, self.precision(“total\_payable\_amount”)).
- Set self.total\_receivable\_amount from flt((total\_receivable + flt(self.total\_asset\_recovery\_cost)), self.precision(“total\_receivable\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L5369) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L795) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L775)
