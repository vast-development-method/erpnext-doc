# Employment and attendance · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Full and final statement

[Record definition](../../../../data/record-types/full_and_final_statement.json)

<a id="op-25265f89ef1eb3"></a>
### Fulland Final Statement.add withheld salary slips

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_add_withheld_salary_slips`

**Inputs** self.

**Record and data access** read “Salary Slip” via get\_all.

**Local steps**

- Set salary\_slips from Platform.get\_all(“Salary Slip”, filters = mapping(“employee” → self.employee, “status” → “Withheld”, “docstatus” → tuple(“!=”, 2)), fields = list(“name”, “net\_pay”)).
- For each slip in salary\_slips.
  - Evaluate self.append(“payables”, mapping(“status” → “Unsettled”, “component” → “Salary Slip”, “reference\_document\_type” → “Salary Slip”, “reference\_document” → slip.name, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L5652) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L781) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L761)

<a id="op-7cb40b1036f35c"></a>
### Fulland Final Statement.add outstanding employee advances

`operation_workforce_binding_workforce_hr_doctype_full_and_final_statement_full_and_final_statement_fullandfinalstatement_add_outstanding_employee_advances`

**Inputs** self.

**Record and data access** read “Employee Advance” via get\_all.

**Local steps**

- Set advances from Platform.get\_all(“Employee Advance”, filters = mapping(“employee” → self.employee, “docstatus” → 1), fields = list(“name”, “advance\_account”, “paid\_amount”, “claimed\_amount”, …)).
- Set outstanding\_advances from mapping().
- For each advance in advances.
  - Set advance.outstanding from ((flt(advance.paid\_amount) − flt(advance.claimed\_amount)) − flt(advance.return\_amount)).
  - If advance.outstanding &gt; 0.
    - Set outstanding\_advances at advance.name from advance.
- Set self.receivables from list of row for row drawn from self.receivables where (row.component differs from “Employee Advance” or row.reference\_document belongs to outstanding\_advances or (not row.reference\_document and not outstan ….
  - Draw row from self.receivables, keep a combination only if ((row.component differs from “Employee Advance” or row.reference\_document belongs to outstanding\_advances or (not row.reference\_document and not outstanding\_advances))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.component differs from “Employee Advance” → row.reference\_document belongs to outstanding\_advances → (not row.reference\_document and not outstanding\_advances).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.reference\_document → not outstanding\_advances.
- Set referenced\_advances from set().
- For each row in self.receivables.
  - Set advance from outstanding\_advances.get(row.reference\_document).
  - If not advance.
    - Continue with the next iteration or loop test.
  - Evaluate referenced\_advances.add(advance.name).
  - If row.status differs from “Settled”.
    - Set row.account from advance.advance\_account.
    - Set row.amount from advance.outstanding.
- For each advance in outstanding\_advances.values().
  - If advance.name belongs to referenced\_advances.
    - Continue with the next iteration or loop test.
  - Evaluate self.append(“receivables”, mapping(“status” → “Unsettled”, “component” → “Employee Advance”, “reference\_document\_type” → “Employee Advance”, “reference\_document” → advance.name, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L60) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L111) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L111)

<a id="op-77aa664332b342"></a>
### Fulland Final Statement.create component row

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_create_component_row`

**Inputs** self, components, component\_type.

**Local steps**

- Set existing\_components from set of row.component for row drawn from self.get(component\_type).
  - Draw row from self.get(component\_type).
- For each component in components.
  - If component belongs to existing\_components.
    - Continue with the next iteration or loop test.
  - Evaluate self.append(component\_type, mapping(“status” → “Unsettled”, “reference\_document\_type” → component when component differs from “Bonus”, otherwise “Additional Salary”, “component” → component)).
    - Value choice on component differs from “Bonus” — true gives component, false gives “Additional Salary”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L24) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L784) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L764)

<a id="op-2a13f221c00cdb"></a>
### Fulland Final Statement.get payable component

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_get_payable_component`

**Inputs** self.

**Explicit results** list(“Gratuity”, “Expense Claim”, “Bonus”, “Leave Encashment”).

**Local steps**

- Return list(“Gratuity”, “Expense Claim”, “Bonus”, “Leave Encashment”).

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L6148) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L789) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L769)

<a id="op-3fa345ff7f5eae"></a>
### Fulland Final Statement.get receivable component

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_get_receivable_component`

**Inputs** self.

**Explicit results** receivables.

**Local steps**

- Set receivables from list(“Employee Advance”).
- If “lending” belongs to Platform.get\_installed\_apps().
  - Evaluate receivables.append(“Loan”).
- Return receivables.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L6217) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L790) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L770)

<a id="op-735b7e11eee3ac"></a>
### Fulland Final Statement.get assets movement

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_get_assets_movement`

**Inputs** self.

**Record and data access** read “Asset Movement Item” via get\_all · read “Asset” via get\_value · read “Asset Movement” via get\_value.

**Explicit results** data.

**Local steps**

- Set asset\_movements from Platform.get\_all(“Asset Movement Item”, filters = mapping(“docstatus” → 1), fields = list(“asset”, “from\_employee”, “to\_employee”, “parent”, …), or\_filters = mapping(“from\_employee” → self.employee, “to\_em ….
- Set data from list().
- Set inward\_movements from list().
- Set outward\_movements from list().
- For each movement in asset\_movements.
  - If (movement.to\_employee and movement.to\_employee equals self.employee).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in movement.to\_employee → movement.to\_employee equals self.employee.
    - Evaluate inward\_movements.append(movement).
  - If (movement.from\_employee and movement.from\_employee equals self.employee).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in movement.from\_employee → movement.from\_employee equals self.employee.
    - Evaluate outward\_movements.append(movement).
- For each movement in inward\_movements.
  - Set outwards\_count from list of movement.asset for movement drawn from outward\_movements.count(movement.asset).
    - Draw movement from outward\_movements.
  - Set inwards\_counts from list of movement.asset for movement drawn from inward\_movements.count(movement.asset).
    - Draw movement from inward\_movements.
  - If inwards\_counts &gt; outwards\_count.
    - Set cost from Platform.db.get\_value(“Asset”, movement.asset, “total\_asset\_cost”).
    - Evaluate data.append(mapping(“reference” → movement.parent, “asset\_name” → movement.asset\_name, “date” → Platform.db.get\_value(“Asset Movement”, movement.parent, “transaction\_date”), “actual\_cost” → cost, …)).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0032.json#L6334) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L786) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L766)

<a id="op-73aadd43576ed9"></a>
### Fulland Final Statement.create journal entry

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_create_journal_entry`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** jv.

**Local steps**

- Set precision from Platform.get\_precision(“Journal Entry Account”, “debit\_in\_account\_currency”).
- Set jv from Platform.new\_doc(“Journal Entry”).
- Set jv.company from self.company.
- Set jv.voucher\_type from “Bank Entry”.
- Set jv.posting\_date from today().
- Set difference from (self.total\_payable\_amount − self.total\_receivable\_amount).
- For each data in self.payables.
  - If (flt(data.amount) &gt; 0 and not data.paid\_via\_salary\_slip).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(data.amount) &gt; 0 → not data.paid\_via\_salary\_slip.
    - Set account\_dict from mapping(“account” → data.account, “debit\_in\_account\_currency” → flt(data.amount, precision), “user\_remark” → data.remark).
    - If (data.reference\_document\_type belongs to list(“Expense Claim”, “Gratuity”, “Leave Encashment”) or is\_party\_account(data.account)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.reference\_document\_type belongs to list(“Expense Claim”, “Gratuity”, “Leave Encashment”) → is\_party\_account(data.account).
      - Set account\_dict at “party\_type” from “Employee”.
      - Set account\_dict at “party” from self.employee.
    - Evaluate jv.append(“accounts”, account\_dict).
- For each data in self.receivables.
  - If flt(data.amount) &gt; 0.
    - Set account\_dict from mapping(“account” → data.account, “credit\_in\_account\_currency” → flt(data.amount, precision), “user\_remark” → data.remark).
    - If data.reference\_document\_type equals “Employee Advance”.
      - Evaluate account\_dict.update(mapping(“party\_type” → “Employee”, “party” → self.employee, “reference\_type” → “Employee Advance”, “reference\_name” → data.reference\_document, …)).
    - Otherwise.
      - If is\_party\_account(data.account).
        - Set account\_dict at “party\_type” from “Employee”.
        - Set account\_dict at “party” from self.employee.
    - Evaluate jv.append(“accounts”, account\_dict).
- For each data in self.assets\_allocated.
  - If data.action equals “Recover Cost”.
    - Evaluate jv.append(“accounts”, mapping(“account” → data.account, “credit\_in\_account\_currency” → flt(data.cost, precision), “party\_type” → “Employee”, “party” → self.employee, …)).
- Evaluate jv.append(“accounts”, mapping(“credit\_in\_account\_currency” → difference when difference &gt; 0, otherwise 0, “debit\_in\_account\_currency” → negative difference when difference &lt; 0, otherwise 0, “reference\_type ….
  - Value choice on difference &gt; 0 — true gives difference, false gives 0.
  - Value choice on difference &lt; 0 — true gives negative difference, false gives 0.
- Return jv.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L25) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L785) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L765)

<a id="op-1b03fe4667e5d3"></a>
### Fulland Final Statement.update reference document payment status

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_update_reference_document_payment_status`

**Inputs** self, payable.

**Record and data access** resolve a document from payable.reference\_document\_type via get\_cached\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- Set doc from Platform.get\_cached\_doc(payable.reference\_document\_type, payable.reference\_document).
- Set amount from payable.amount when (self.docstatus equals 1 and self.status equals “Paid”), otherwise 0.
  - Value choice on (self.docstatus equals 1 and self.status equals “Paid”) — true gives payable.amount, false gives 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.status equals “Paid”.
- Evaluate doc.db\_set(“paid\_amount”, amount).
- Evaluate doc.set\_status(update = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(payable.reference\_document\_type, payable.reference\_document).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L1159) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L797) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L777)

<a id="op-bcc3cf05c72261"></a>
### Fulland Final Statement.update linked payable documents

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_fulland_final_statement_update_linked_payable_documents`

**Inputs** self.

**Local steps**

- For each payable in self.payables.
  - If (payable.reference\_document\_type belongs to list(“Gratuity”, “Leave Encashment”) and payable.reference\_document).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in payable.reference\_document\_type belongs to list(“Gratuity”, “Leave Encashment”) → payable.reference\_document.
    - Evaluate self.update\_reference\_document\_payment\_status(payable).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reference document payment status](operations-018.md#op-1b03fe4667e5d3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L27) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L796) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L776)

<a id="op-f130e25008dd44"></a>
### Get account and amount

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_get_account_and_amount`

**Inputs** ref\_doctype, ref\_document, company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (list bitwise or no value).

**Record and data access** read “Salary Slip” via get\_value · read “Payroll Entry” via get\_value · read “Gratuity” via get\_value · read “Expense Claim” via get\_value · read “Loan” via get\_value · 3 additional forms in the steps below.

**Explicit results** no value · list(payable\_account, amount) · list(payment\_account, amount).

**Local steps**

- If (not ref\_doctype or not ref\_document).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ref\_doctype → not ref\_document.
  - Return no value.
- Evaluate Platform.has\_permission(ref\_doctype, “read”, ref\_document, throw = true).
- If ref\_doctype equals “Salary Slip”.
  - Set salary\_details from Platform.db.get\_value(“Salary Slip”, ref\_document, list(“payroll\_entry”, “net\_pay”), as\_dict = 1).
  - Set amount from salary\_details.net\_pay.
  - Set payable\_account from Platform.db.get\_value(“Payroll Entry”, salary\_details.payroll\_entry, “payroll\_payable\_account”) when salary\_details.payroll\_entry, otherwise no value.
    - Value choice on salary\_details.payroll\_entry — true gives Platform.db.get\_value(“Payroll Entry”, salary\_details.payroll\_entry, “payroll\_payable\_account”), false gives no value.
  - Return list(payable\_account, amount).
- If ref\_doctype equals “Gratuity”.
  - Set tuple(payable\_account, amount) from Platform.db.get\_value(“Gratuity”, ref\_document, list(“payable\_account”, “amount”)).
  - Return list(payable\_account, amount).
- If ref\_doctype equals “Expense Claim”.
  - Set details from Platform.db.get\_value(“Expense Claim”, ref\_document, list(“payable\_account”, “grand\_total”, “total\_amount\_reimbursed”, “total\_advance\_amount”), as\_dict = true).
  - Set payable\_account from details.payable\_account.
  - Set amount from (details.grand\_total − (details.total\_amount\_reimbursed + details.total\_advance\_amount)).
  - Return list(payable\_account, amount).
- If ref\_doctype equals “Loan”.
  - Set details from Platform.db.get\_value(“Loan”, ref\_document, list(“payment\_account”, “total\_payment”, “total\_amount\_paid”), as\_dict = 1).
  - Set payment\_account from details.payment\_account.
  - Set amount from (details.total\_payment − details.total\_amount\_paid).
  - Return list(payment\_account, amount).
- If ref\_doctype equals “Employee Advance”.
  - Set details from Platform.db.get\_value(“Employee Advance”, ref\_document, list(“advance\_account”, “paid\_amount”, “claimed\_amount”, “return\_amount”), as\_dict = 1).
  - Set payment\_account from details.advance\_account.
  - Set amount from (details.paid\_amount − (details.claimed\_amount + details.return\_amount)).
  - Return list(payment\_account, amount).
- If ref\_doctype equals “Leave Encashment”.
  - Set amount from Platform.db.get\_value(“Leave Encashment”, ref\_document, “encashment\_amount”).
  - Set payable\_account from Platform.get\_cached\_value(“Company”, company, “default\_payroll\_payable\_account”).
  - Return list(payable\_account, amount).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(ref\_doctype, “read”, ref\_document, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_payroll\_payable\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L1488) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L802) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L782)

<a id="op-6025af58b9d27d"></a>
### Is party account

`operation_workforce_binding_workforce_hr_doctype_full_and_final_statement_full_and_final_statement_is_party_account`

**Inputs** account.

**Declared result** bool.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Account”, account, “account\_type”) belongs to list(“Receivable”, “Payable”).

**Local steps**

- Return Platform.get\_cached\_value(“Account”, account, “account\_type”) belongs to list(“Receivable”, “Payable”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “account\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L61) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L112) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L112)

<a id="op-760cda9b81e7c9"></a>
### Update full and final statement status

`operation_workforce_human_resources_record_definitions_full_and_final_statement_business_behavior_update_full_and_final_statement_status`

**Inputs** doc, method = no value.

**Record and data access** resolve a document from “Full and Final Statement” via get\_doc.

**State and service calls** call db\_set on fnf.

**Local steps**

- Set status from “Paid” when doc.docstatus equals 1, otherwise “Unpaid”.
  - Value choice on doc.docstatus equals 1 — true gives “Paid”, false gives “Unpaid”.
- For each entry in doc.accounts.
  - If entry.reference\_type equals “Full and Final Statement”.
    - Set fnf from Platform.get\_doc(“Full and Final Statement”, entry.reference\_name).
    - Evaluate fnf.db\_set(“status”, status).
    - Evaluate fnf.notify\_update().
    - Evaluate fnf.update\_linked\_payable\_documents().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L2657) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L803) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L783)

<a id="op-a00cd4c75e4df4"></a>
### Process loan accrual

`operation_workforce_human_resources_record_definitions_full_and_final_statement_full_and_final_statement_loan_utils_business_behavior_process_loan_accrual`

**Inputs** doc.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Record and data access** resolve a document from “Loan” via get\_doc · resolve a document from “Loan Repayment Schedule” via get\_doc.

**State and service calls** request set\_value on “Repayment Schedule” · call save on repayment\_entry · call submit on repayment\_entry.

**Local steps**

- Bind dependencies make\_loan\_interest\_accrual\_entry.
- Bind dependencies calculate\_amounts, create\_repayment\_entry, get\_pending\_principal\_amount.
- Set loan\_receivables from list().
- For each receivable in doc.receivables.
  - If receivable.component differs from “Loan”.
    - Continue with the next iteration or loop test.
  - Evaluate loan\_receivables.append(receivable.reference\_document).
- For each loan in loan\_receivables.
  - Set loan\_doc from Platform.get\_doc(“Loan”, loan).
  - Set loan\_repayment\_schedule from Platform.get\_doc(“Loan Repayment Schedule”, mapping(“loan” → loan, “docstatus” → 1)).
  - If loan\_repayment\_schedule.repayment\_schedule.
    - Set amounts from list().
    - For each repayment\_schedule in loan\_repayment\_schedule.repayment\_schedule.
      - Set amounts from calculate\_amounts(loan, doc.transaction\_date, “Normal Repayment”).
      - Set pending\_principal\_amount from get\_pending\_principal\_amount(loan\_doc).
      - If not repayment\_schedule.is\_accrued.
        - Set args from Platform.\_dict(mapping(“loan” → loan, “applicant\_type” → loan\_doc.applicant\_type, “applicant” → loan\_doc.applicant, “interest\_income\_account” → loan\_doc.interest\_income\_account, …)).
        - Evaluate make\_loan\_interest\_accrual\_entry(args).
        - Evaluate Platform.db.set\_value(“Repayment Schedule”, repayment\_schedule.name, “is\_accrued”, 1).
    - Set repayment\_entry from create\_repayment\_entry(loan, doc.employee, doc.company, doc.transaction\_date, …).
    - Evaluate repayment\_entry.save().
    - Evaluate repayment\_entry.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L2898) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L805) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L785)

<a id="op-48bf6281e67cde"></a>
### Cancel loan repayment

`operation_workforce_human_resources_record_definitions_full_and_final_statement_full_and_final_statement_loan_utils_business_behavior_cancel_loan_repayment`

**Inputs** doc.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Record and data access** resolve a document from “Loan Repayment” via get\_doc · read “Loan Interest Accrual” via get\_all · resolve a document from “Loan Interest Accrual” via get\_doc.

**State and service calls** call cancel on loan\_repayment · call cancel on Platform.get\_doc(“Loan Interest Accrual”, accrual.name).

**Local steps**

- Set loan\_receivables from list().
- For each receivable in doc.receivables.
  - If receivable.component differs from “Loan”.
    - Continue with the next iteration or loop test.
  - Evaluate loan\_receivables.append(receivable.reference\_document).
- For each loan in loan\_receivables.
  - Set posting\_date from Platform.utils.getdate(doc.transaction\_date).
  - Set loan\_repayment from Platform.get\_doc(“Loan Repayment”, mapping(“against\_loan” → loan, “docstatus” → 1, “posting\_date” → posting\_date)).
  - If loan\_repayment.
    - Evaluate loan\_repayment.cancel().
  - Set loan\_interest\_accruals from Platform.get\_all(“Loan Interest Accrual”, filters = mapping(“loan” → loan, “docstatus” → 1, “posting\_date” → posting\_date)).
  - For each accrual in loan\_interest\_accruals.
    - Evaluate Platform.get\_doc(“Loan Interest Accrual”, accrual.name).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L3759) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L804) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L784)

## Record · Goal

[Record definition](../../../../data/record-types/goal.json)

<a id="op-632fd48b302295"></a>
### Goal.before insert

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_before_insert`

**Inputs** self.

**Local steps**

- If cint(self.is\_group).
  - Set self.progress from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L6136) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L818) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L798)

<a id="op-e6812e0628c2e5"></a>
### Goal.validate

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_validate`

**Inputs** self.

**Local steps**

- If self.appraisal\_cycle.
  - Evaluate validate\_active\_appraisal\_cycle(self.appraisal\_cycle).
- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_parent\_fields().
- Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- Evaluate self.validate\_progress().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent fields](operations-018.md#op-eee5bee9a4370a), [validate progress](operations-018.md#op-657f7714182de9), [set status](operations-018.md#op-97b6062f3f0f8b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L29) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L825) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L805)

<a id="op-cb267a847b10f5"></a>
### Goal.on update

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_on_update`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_update(self).
- Set doc\_before\_save from self.get\_doc\_before\_save().
- If doc\_before\_save.
  - Evaluate self.update\_kra\_in\_child\_goals(doc\_before\_save).
  - If doc\_before\_save.parent\_goal differs from self.parent\_goal.
    - Evaluate self.update\_parent\_progress(doc\_before\_save.parent\_goal).
- Evaluate self.update\_parent\_progress().
- Evaluate self.update\_goal\_progress\_in\_appraisal().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update kra in child goals](operations-018.md#op-d81abd3e336a1b), [update parent progress](operations-018.md#op-14ac724b62306f), [update goal progress in appraisal](operations-019.md#op-9eb92afba6215b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L6403) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L820) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L800)

<a id="op-8c9703f0773c6e"></a>
### Goal.on trash

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_on_trash`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_trash(self, allow\_root\_deletion = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L6615) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L819) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L799)

<a id="op-3f5b660275d7d0"></a>
### Goal.after delete

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.update\_parent\_progress().
- Evaluate self.update\_goal\_progress\_in\_appraisal().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update parent progress](operations-018.md#op-14ac724b62306f), [update goal progress in appraisal](operations-019.md#op-9eb92afba6215b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L6679) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L817) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L797)

<a id="op-eee5bee9a4370a"></a>
### Goal.validate parent fields

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_validate_parent_fields`

**Inputs** self.

**Record and data access** read “Goal” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Goal should be owned by the same employee as its parent goal.” · validation helper — translated “Goal should be aligned with the same KRA as its parent goal.” · validation helper — translated “Goal should belong to the same Appraisal Cycle as its parent goal.”.

**Local steps**

- If not self.parent\_goal.
  - Return no value.
- Set parent\_details from Platform.db.get\_value(“Goal”, self.parent\_goal, list(“employee”, “kra”, “appraisal\_cycle”), as\_dict = true).
- If not parent\_details.
  - Return no value.
- If self.employee differs from parent\_details.employee.
  - Call the validation error handler Platform.throw(translated “Goal should be owned by the same employee as its parent goal.”, title = translated “Not Allowed”).
- If self.kra differs from parent\_details.kra.
  - Call the validation error handler Platform.throw(translated “Goal should be aligned with the same KRA as its parent goal.”, title = translated “Not Allowed”).
- If self.appraisal\_cycle differs from parent\_details.appraisal\_cycle.
  - Call the validation error handler Platform.throw(translated “Goal should belong to the same Appraisal Cycle as its parent goal.”, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L6750) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L826) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L806)

<a id="op-657f7714182de9"></a>
### Goal.validate progress

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_validate_progress`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Goal progress percentage cannot be more than 100.”.

**Local steps**

- If flt(self.progress) &gt; 100.
  - Call the validation error handler Platform.throw(translated “Goal progress percentage cannot be more than 100.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L7193) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L827) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L807)

<a id="op-97b6062f3f0f8b"></a>
### Goal.set status

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_set_status`

**Inputs** self, status = no value.

**Explicit results** no value.

**Local steps**

- <a id="op-97b6062f3f0f8b-guard-2"></a>If self.status belongs to list(“Archived”, “Closed”).
  - Return no value.
- If flt(self.progress) equals 0.
  - Set self.status from “Pending”.
- Otherwise.
  - If flt(self.progress) equals 100.
    - Set self.status from “Completed”.
  - Otherwise.
    - If flt(self.progress) &lt; 100.
      - Set self.status from “In Progress”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status belongs to list(“Archived”, “Closed”), self.status = “Archived” selects the branch that returns no value. With self.status = “Pending”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-97b6062f3f0f8b-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0033.json#L7302) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L821) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L801)

<a id="op-d81abd3e336a1b"></a>
### Goal.update kra in child goals

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_update_key_result_area_in_child_goals`

**Inputs** self, doc\_before\_save.

**State and service calls** msgprint with translated “KRA updated for all child goals.”.

**Local steps**

- If (doc\_before\_save.kra differs from self.kra and self.is\_group).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.kra differs from self.kra → self.is\_group.
  - Set Goal from Platform.qb.DocType(“Goal”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(Goal.kra, self.kra).where(Goal.parent\_goal equals self.name).run().
  - Evaluate Platform.msgprint(translated “KRA updated for all child goals.”, alert = true, indicator = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L823) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L803)

<a id="op-14ac724b62306f"></a>
### Goal.update parent progress

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_update_parent_progress`

**Inputs** self, old\_parent = no value.

**Record and data access** resolve a document from “Goal” via get\_doc.

**State and service calls** call save on parent\_goal\_doc.

**Explicit results** no value.

**Local steps**

- Set parent\_goal from (old\_parent or self.parent\_goal).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_parent → self.parent\_goal.
- If not parent\_goal.
  - Return no value.
- Set Goal from Platform.qb.DocType(“Goal”).
- Set avg\_goal\_completion from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract differs from nes … at 0.
- Set parent\_goal\_doc from Platform.get\_doc(“Goal”, parent\_goal).
- Set parent\_goal\_doc.progress from flt(avg\_goal\_completion, parent\_goal\_doc.precision(“progress”)).
- Set parent\_goal\_doc.ignore\_permissions from true.
- Set parent\_goal\_doc.ignore\_mandatory from true.
- Evaluate parent\_goal\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L299) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L824) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L804)
