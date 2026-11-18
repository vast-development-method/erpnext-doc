# Accounting and settlement · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Bank clearance summary

<a id="op-fc10c6baf92168"></a>
### Get entries for bank clearance summary

`operation_enterprise_accounts_report_bank_clearance_summary_business_behavior_get_entries_for_bank_clearance_summary`

**Inputs** filters.

**Explicit results** entries.

**Local steps**

- Set entries from list().
- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Set journal\_entries from nested operand in the contract(nested operand in the contract).orderby(je.posting\_date, order = Order.desc).orderby(je.name, order = Order.desc).run(as\_list = true).
- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set payment\_entries from nested operand in the contract(nested operand in the contract).orderby(pe.posting\_date, order = Order.desc).orderby(pe.name, order = Order.desc).run(as\_list = true).
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set purchase\_invoices from nested operand in the contract(nested operand in the contract).orderby(pi.posting\_date, order = Order.desc).orderby(pi.name, order = Order.desc).run(as\_list = true).
- Set entries from (((journal\_entries + payment\_entries) + purchase\_invoices) + get\_pos\_entries(filters)).
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L676)

<a id="op-b2809e8a7820e9"></a>
### Get pos entries

`operation_enterprise_binding_enterprise_accounts_report_bank_clearance_summary_bank_clearance_summary_get_pos_entries`

**Inputs** filters.

**Declared result** list.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(si.posting\_date, order = Order.desc).orderby(si.name, order = Order.desc).run(as\_list = true).

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set si\_payment from Platform.qb.DocType(“Sales Invoice Payment”).
- Return nested operand in the contract(nested operand in the contract).orderby(si.posting\_date, order = Order.desc).orderby(si.name, order = Order.desc).run(as\_list = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1130)

<a id="op-807d5d2c4f7c77"></a>
### Get amount in bank currency

`operation_enterprise_binding_enterprise_accounts_report_bank_clearance_summary_bank_clearance_summary_get_amount_in_bank_currency`

**Inputs** bank\_account, invoice, amount, base\_amount.

**Declared result** Case.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** Case().when(invoice.currency equals bank\_currency, amount).else\_(base\_amount).

**Local steps**

- Set bank\_currency from Platform.get\_cached\_value(“Account”, bank\_account, “account\_currency”).
- Return Case().when(invoice.currency equals bank\_currency, amount).else\_(base\_amount).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, bank\_account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1129)

## Record · Bank guarantee

[Record definition](../../../../data/record-types/bank_guarantee.json)

<a id="op-99df2499740dce"></a>
### Bank Guarantee.validate

`operation_enterprise_accounts_record_definitions_bank_guarantee_business_behavior_bank_guarantee_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Select the customer or supplier.”.

**Local steps**

- If not (self.customer or self.supplier).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.customer → self.supplier.
  - Call the validation error handler Platform.throw(translated “Select the customer or supplier.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0016.json#L1461) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L267)

<a id="op-73f3323d9e011f"></a>
### Bank Guarantee.on submit

`operation_enterprise_accounts_record_definitions_bank_guarantee_business_behavior_bank_guarantee_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enter the Bank Guarantee Number before submitting.” · validation helper — translated “Enter the name of the Beneficiary before submitting.” · validation helper — translated “Enter the name of the bank or lending institution before submitting.”.

**Local steps**

- If not self.bank\_guarantee\_number.
  - Call the validation error handler Platform.throw(translated “Enter the Bank Guarantee Number before submitting.”).
- If not self.name\_of\_beneficiary.
  - Call the validation error handler Platform.throw(translated “Enter the name of the Beneficiary before submitting.”).
- If not self.bank.
  - Call the validation error handler Platform.throw(translated “Enter the name of the bank or lending institution before submitting.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0016.json#L1563) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L266)

<a id="op-4065510b7818bc"></a>
### Get voucher details

`operation_enterprise_accounts_record_definitions_bank_guarantee_business_behavior_get_voucher_details`

**Inputs** bank\_guarantee\_type, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_value.

**Explicit results** Platform.db.get\_value(doctype, reference\_name, fields\_to\_fetch, as\_dict = true).

**Explicit failure paths** TypeError(“reference\_name must be a string”).

**Local steps**

- If not isinstance(reference\_name, str).
  - Raise TypeError(“reference\_name must be a string”).
- Evaluate Platform.has\_permission(“Bank Guarantee”, throw = true).
- Set fields\_to\_fetch from list(“grand\_total”).
- If bank\_guarantee\_type equals “Receiving”.
  - Set doctype from “Sales Order”.
  - Evaluate fields\_to\_fetch.append(“customer”).
  - Evaluate fields\_to\_fetch.append(“project”).
- Otherwise.
  - Set doctype from “Purchase Order”.
  - Evaluate fields\_to\_fetch.append(“supplier”).
- Return Platform.db.get\_value(doctype, reference\_name, fields\_to\_fetch, as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Guarantee”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L268)

## Report · Bank reconciliation statement

<a id="op-26c7b308f99cc3"></a>
### Execute

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** tuple(columns, list()) · tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns().
- If not filters.get(“account”).
  - Return tuple(columns, list()).
- Set account\_currency from Platform.get\_cached\_value(“Account”, filters.account, “account\_currency”).
- Set data from get\_entries(filters).
- Set balance\_as\_per\_system from get\_balance\_on(filters at “account”, filters at “report\_date”, company = filters at “company”).
- Set tuple(total\_debit, total\_credit) from tuple(0, 0).
- For each d in data.
  - Update total\_debit using + flt(d.debit).
  - Update total\_credit using + flt(d.credit).
- Set amounts\_not\_reflected\_in\_system from get\_amounts\_not\_reflected\_in\_system(filters).
- Set bank\_bal from (((flt(balance\_as\_per\_system) − flt(total\_debit)) + flt(total\_credit)) + amounts\_not\_reflected\_in\_system).
- Update data using + list(get\_balance\_row(translated “Bank Statement balance as per General Ledger”, balance\_as\_per\_system, account\_currency), mapping(), mapping(“payment\_entry” → translated “Outstanding Cheques and Deposits t ….
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, filters.account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L679)

<a id="op-05df4465d38291"></a>
### Get columns

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “posting\_date”, “label” → translated “Posting Date”, “fieldtype” → “Date”, “width” → 90), mapping(“fieldname” → “payment\_document”, “label” → translated “Payment Document Type”,  ….

**Local steps**

- Return list(mapping(“fieldname” → “posting\_date”, “label” → translated “Posting Date”, “fieldtype” → “Date”, “width” → 90), mapping(“fieldname” → “payment\_document”, “label” → translated “Payment Document Type”,  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L683)

<a id="op-725965280f20ee"></a>
### Get entries

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_entries`

**Inputs** filters.

**Explicit results** sorted(entries, key = deferred anonymous expression).

**Local steps**

- Set entries from list().
- For each method\_name in Platform.get\_hooks(“get\_entries\_for\_bank\_reconciliation\_statement”).
  - Update entries using + (Platform.get\_attr(method\_name)(filters) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method\_name)(filters) → list().
- Return sorted(entries, key = deferred anonymous expression).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_entries\_for\_bank\_reconciliation\_statement”), Platform.get\_attr(method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0230.json#L6169) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L684)

<a id="op-bdba4fb4645543"></a>
### Get entries for bank reconciliation statement

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_entries_for_bank_reconciliation_statement`

**Inputs** filters.

**Explicit results** (((list(journal\_entries) + list(payment\_entries)) + list(pos\_entries)) + list(purchase\_invoices)).

**Local steps**

- Set journal\_entries from get\_journal\_entries(filters).
- Set payment\_entries from get\_payment\_entries(filters).
- Set purchase\_invoices from get\_purchase\_invoices(filters).
- Set pos\_entries from list().
- If filters.include\_pos\_transactions.
  - Set pos\_entries from get\_pos\_entries(filters).
- Return (((list(journal\_entries) + list(payment\_entries)) + list(pos\_entries)) + list(purchase\_invoices)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0230.json#L6364) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L685)

<a id="op-f0d8485f2ff7c4"></a>
### Get journal entries

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_journal_entries`

**Inputs** filters.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(je.posting\_date).orderby(je.name, order = Order.desc).run(as\_dict = true).

**Local steps**

- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Return nested operand in the contract(nested operand in the contract).orderby(je.posting\_date).orderby(je.name, order = Order.desc).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L686)

<a id="op-f01df46519d005"></a>
### Get payment entries

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_payment_entries`

**Inputs** filters.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(pe.posting\_date).orderby(pe.name, order = Order.desc).run(as\_dict = true).

**Local steps**

- Set pe from Platform.qb.DocType(“Payment Entry”).
- Return nested operand in the contract(nested operand in the contract).orderby(pe.posting\_date).orderby(pe.name, order = Order.desc).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0231.json#L713) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L687)

<a id="op-d6fc2deaf41edf"></a>
### Get purchase invoices

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_purchase_invoices`

**Inputs** filters.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(pi.posting\_date).orderby(pi.name, order = Order.desc).run(as\_dict = true).

**Local steps**

- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set acc from Platform.qb.DocType(“Account”).
- Set paid\_amount from get\_amount\_in\_bank\_currency(filters, pi.paid\_amount, pi.base\_paid\_amount).
- Return nested operand in the contract(nested operand in the contract).orderby(pi.posting\_date).orderby(pi.name, order = Order.desc).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L689)

<a id="op-f54ee98f299548"></a>
### Get pos entries

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_point_of_sale_entries`

**Inputs** filters.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(si.posting\_date).orderby(si\_payment.name, order = Order.desc).run(as\_dict = true).

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set si\_payment from Platform.qb.DocType(“Sales Invoice Payment”).
- Set acc from Platform.qb.DocType(“Account”).
- Return nested operand in the contract(nested operand in the contract).orderby(si.posting\_date).orderby(si\_payment.name, order = Order.desc).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L688)

<a id="op-1975065d198ccd"></a>
### Get amounts not reflected in system

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_amounts_not_reflected_in_system`

**Inputs** filters.

**Explicit results** amount.

**Local steps**

- Set amount from 0.0.
- For each method\_name in Platform.get\_hooks(“get\_amounts\_not\_reflected\_in\_system\_for\_bank\_reconciliation\_statement”).
  - Update amount using + (Platform.get\_attr(method\_name)(filters) or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method\_name)(filters) → 0.0.
- Return amount.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_amounts\_not\_reflected\_in\_system\_for\_bank\_reconciliation\_statement”), Platform.get\_attr(method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0231.json#L3168) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L680)

<a id="op-422841d59c4cd8"></a>
### Get amounts not reflected in system for bank reconciliation statement

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_amounts_not_reflected_in_system_for_bank_reconciliation_statement`

**Inputs** filters.

**Explicit results** ((je\_amount + pe\_amount) + pi\_amount).

**Local steps**

- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Set je\_amount from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“amount”)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitw ….
- Set je\_amount from flt(je\_amount at 0.amount) when je\_amount, otherwise 0.0.
  - Value choice on je\_amount — true gives flt(je\_amount at 0.amount), false gives 0.0.
- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set pe\_amount from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“amount”)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitw ….
- Set pe\_amount from flt(pe\_amount at 0.amount) when pe\_amount, otherwise 0.0.
  - Value choice on pe\_amount — true gives flt(pe\_amount at 0.amount), false gives 0.0.
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pi\_amount from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“amount”)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitw ….
- Set pi\_amount from flt(pi\_amount at 0.amount) when pi\_amount, otherwise 0.0.
  - Value choice on pi\_amount — true gives flt(pi\_amount at 0.amount), false gives 0.0.
- Return ((je\_amount + pe\_amount) + pi\_amount).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L681)

<a id="op-852f1c7eeaea63"></a>
### Get amount in bank currency

`operation_enterprise_binding_enterprise_accounts_report_bank_reconciliation_statement_bank_reconciliation_statement_get_amount_in_bank_currency`

**Inputs** filters, amount, base\_amount.

**Declared result** Field.

**Record and data access** read “Account” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** base\_amount when bank\_currency equals company\_currency, otherwise amount.

**Local steps**

- Set bank\_currency from Platform.get\_cached\_value(“Account”, filters.account, “account\_currency”).
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Return base\_amount when bank\_currency equals company\_currency, otherwise amount.
  - Value choice on bank\_currency equals company\_currency — true gives base\_amount, false gives amount.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, filters.account, “account\_currency”), Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1131)

<a id="op-f73a13a578b90e"></a>
### Get balance row

`operation_enterprise_accounts_report_bank_reconciliation_statement_business_behavior_get_balance_row`

**Inputs** label, amount, account\_currency.

**Explicit results** mapping(“payment\_entry” → label, “debit” → amount, “credit” → 0, “account\_currency” → account\_currency) · mapping(“payment\_entry” → label, “debit” → 0, “credit” → abs(amount), “account\_currency” → account\_currency).

**Local steps**

- If amount &gt; 0.
  - Return mapping(“payment\_entry” → label, “debit” → amount, “credit” → 0, “account\_currency” → account\_currency).
- Otherwise.
  - Return mapping(“payment\_entry” → label, “debit” → 0, “credit” → abs(amount), “account\_currency” → account\_currency).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0231.json#L4620) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L682)

## Record · Bank reconciliation tool

[Record definition](../../../../data/record-types/bank_reconciliation_tool.json)

<a id="op-cfae8e4f0a26d9"></a>
### Get bank transactions

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_bank_transactions`

**Inputs** bank\_account, from\_date = no value, to\_date = no value, all\_transactions = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Bank Transaction” via get\_list.

**Explicit results** transactions.

**Local steps**

- Evaluate validate\_date\_range(from\_date, to\_date).
- Set filters from list().
- Evaluate filters.append(list(“bank\_account”, “=”, bank\_account)).
- Evaluate filters.append(list(“docstatus”, “=”, 1)).
- If not all\_transactions.
  - Evaluate filters.append(list(“unallocated\_amount”, “&gt;”, 0.0)).
- If to\_date.
  - Evaluate filters.append(list(“date”, “&lt;=”, to\_date)).
- If from\_date.
  - Evaluate filters.append(list(“date”, “&gt;=”, from\_date)).
- Set transactions from Platform.get\_list(“Bank Transaction”, fields = list(“date”, “deposit”, “withdrawal”, “currency”, …), filters = filters, order\_by = “date”).
- Return transactions.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L283)

<a id="op-d89c338a7e7d86"></a>
### Get account balance

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_account_balance`

**Inputs** bank\_account, till\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Bank Account” via get\_value.

**Explicit results** (((flt(balance\_as\_per\_system) − flt(total\_debit)) + flt(total\_credit)) + amounts\_not\_reflected\_in\_system).

**Local steps**

- Evaluate Platform.has\_permission(“Bank Account”, “read”, bank\_account, throw = true).
- Set account from Platform.db.get\_value(“Bank Account”, bank\_account, “account”).
- Set filters from Platform.\_dict(mapping(“account” → account, “report\_date” → till\_date, “include\_pos\_transactions” → 1, “company” → company)).
- Set data from get\_entries(filters).
- Set balance\_as\_per\_system from get\_balance\_on(filters at “account”, filters at “report\_date”, company = filters at “company”).
- Set tuple(total\_debit, total\_credit) from tuple(0.0, 0.0).
- For each d in data.
  - Update total\_debit using + flt(d.debit).
  - Update total\_credit using + flt(d.credit).
- Set amounts\_not\_reflected\_in\_system from get\_amounts\_not\_reflected\_in\_system(filters).
- Return (((flt(balance\_as\_per\_system) − flt(total\_debit)) + flt(total\_credit)) + amounts\_not\_reflected\_in\_system).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Account”, “read”, bank\_account, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L280)

<a id="op-5537314e3ee90b"></a>
### Update bank transaction

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_update_bank_transaction`

**Inputs** bank\_transaction\_name, reference\_number, party\_type = no value, party = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Transaction” via get\_doc · read “Bank Transaction” via get\_all.

**State and service calls** call save on bank\_transaction.

**Explicit results** Platform.db.get\_all(“Bank Transaction”, filters = mapping(“name” → bank\_transaction\_name), fields = list(“date”, “deposit”, “withdrawal”, “currency”, …)) at 0.

**Local steps**

- Set bank\_transaction from Platform.get\_doc(“Bank Transaction”, bank\_transaction\_name).
- Set bank\_transaction.reference\_number from reference\_number.
- Set bank\_transaction.party\_type from party\_type.
- Set bank\_transaction.party from party.
- Evaluate bank\_transaction.save().
- Return Platform.db.get\_all(“Bank Transaction”, filters = mapping(“name” → bank\_transaction\_name), fields = list(“date”, “deposit”, “withdrawal”, “currency”, …)) at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L297)

<a id="op-fa603d35361714"></a>
### Create journal entry bts

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_journal_entry_bts`

**Inputs** bank\_transaction\_name, reference\_number = no value, reference\_date = no value, posting\_date = no value, entry\_type = no value, second\_account = no value, mode\_of\_payment = no value, party\_type = no value, party = no value, allow\_edit = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Transaction” via get\_values · read “Bank Account” via get\_value · read “Account” via get\_value · read “Company” via get\_cached\_value · read “Account” via get\_cached\_value.

**State and service calls** request new\_doc for “Journal Entry” · call insert on journal\_entry · call submit on journal\_entry.

**Explicit results** journal\_entry · \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = true).

**Explicit failure paths** validation helper — translated “Party Type and Party is required for Receivable / Payable account {0}”.format(second\_account).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- If party.
  - Set party from cstr(party).
- Evaluate require\_party\_permission(party\_type, party).
- Set bank\_transaction from Platform.db.get\_values(“Bank Transaction”, bank\_transaction\_name, fieldname = list(“name”, “deposit”, “withdrawal”, “bank\_account”, …), as\_dict = true) at 0.
- Set company\_account from Platform.get\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).
- Set account\_type from Platform.db.get\_value(“Account”, second\_account, “account\_type”).
- If account\_type belongs to list(“Receivable”, “Payable”).
  - If not (party\_type and party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
    - Call the validation error handler Platform.throw(translated “Party Type and Party is required for Receivable / Payable account {0}”.format(second\_account)).
- Set company from Platform.get\_value(“Account”, company\_account, “company”).
- Set company\_default\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set company\_account\_currency from Platform.get\_cached\_value(“Account”, company\_account, “account\_currency”).
- Set second\_account\_currency from Platform.get\_cached\_value(“Account”, second\_account, “account\_currency”).
- Set is\_multi\_currency from true when (company\_default\_currency differs from company\_account\_currency or company\_default\_currency differs from second\_account\_currency or company\_default\_currency differs from bank\_transaction.currency ….
  - Value choice on (company\_default\_currency differs from company\_account\_currency or company\_default\_currency differs from second\_account\_currency or company\_default\_currency differs from bank\_transaction.currency) — true gives true, false gives false.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_default\_currency differs from company\_account\_currency → company\_default\_currency differs from second\_account\_currency → company\_default\_currency differs from bank\_transaction.currency.
- Set accounts from list().
- Set second\_account\_dict from mapping(“account” → second\_account, “account\_currency” → second\_account\_currency, “credit\_in\_account\_currency” → bank\_transaction.deposit, “debit\_in\_account\_currency” → bank\_transaction.withdrawal, …).
- Set company\_account\_dict from mapping(“account” → company\_account, “account\_currency” → company\_account\_currency, “bank\_account” → bank\_transaction.bank\_account, “credit\_in\_account\_currency” → bank\_transaction.withdrawal, …).
- If is\_multi\_currency.
  - Set exc\_rate from get\_exchange\_rate(bank\_transaction.currency, company\_default\_currency, posting\_date).
  - Set withdrawal\_in\_company\_currency from flt((exc\_rate × abs(bank\_transaction.withdrawal))).
  - Set deposit\_in\_company\_currency from flt((exc\_rate × abs(bank\_transaction.deposit))).
- Otherwise.
  - Set withdrawal\_in\_company\_currency from bank\_transaction.withdrawal.
  - Set deposit\_in\_company\_currency from bank\_transaction.deposit.
- If second\_account\_currency differs from company\_default\_currency.
  - Set exc\_rate from get\_exchange\_rate(second\_account\_currency, company\_default\_currency, posting\_date).
  - Evaluate second\_account\_dict.update(mapping(“exchange\_rate” → exc\_rate, “credit” → deposit\_in\_company\_currency, “debit” → withdrawal\_in\_company\_currency, “credit\_in\_account\_currency” → (flt((deposit\_in\_company\_curr ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt((deposit\_in\_company\_currency ÷ exc\_rate)) → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt((withdrawal\_in\_company\_currency ÷ exc\_rate)) → 0.
- Otherwise.
  - Evaluate second\_account\_dict.update(mapping(“exchange\_rate” → 1, “credit” → deposit\_in\_company\_currency, “debit” → withdrawal\_in\_company\_currency, “credit\_in\_account\_currency” → deposit\_in\_company\_currency, …)).
- If company\_account\_currency differs from company\_default\_currency.
  - Set exc\_rate from get\_exchange\_rate(company\_account\_currency, company\_default\_currency, posting\_date).
  - Evaluate company\_account\_dict.update(mapping(“exchange\_rate” → exc\_rate, “credit” → withdrawal\_in\_company\_currency, “debit” → deposit\_in\_company\_currency)).
- Otherwise.
  - Evaluate company\_account\_dict.update(mapping(“exchange\_rate” → 1, “credit” → withdrawal\_in\_company\_currency, “debit” → deposit\_in\_company\_currency, “credit\_in\_account\_currency” → withdrawal\_in\_company\_currency, …)).
- Evaluate accounts.append(second\_account\_dict).
- Evaluate accounts.append(company\_account\_dict).
- Set journal\_entry\_dict from mapping(“voucher\_type” → entry\_type, “company” → company, “posting\_date” → posting\_date, “cheque\_date” → reference\_date, …).
- If is\_multi\_currency.
  - Evaluate journal\_entry\_dict.update(mapping(“multi\_currency” → true)).
- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Evaluate journal\_entry.update(journal\_entry\_dict).
- Evaluate journal\_entry.set(“accounts”, accounts).
- If allow\_edit.
  - Return journal\_entry.
- Evaluate journal\_entry.insert().
- Evaluate journal\_entry.submit().
- If bank\_transaction.deposit &gt; 0.0.
  - Set paid\_amount from bank\_transaction.deposit.
- Otherwise.
  - Set paid\_amount from bank\_transaction.withdrawal.
- Set vouchers from json.dumps(list(mapping(“payment\_doctype” → “Journal Entry”, “payment\_name” → journal\_entry.name, “amount” → paid\_amount))).
- Return \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”), Platform.get\_cached\_value(“Account”, company\_account, “account\_currency”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L277)

<a id="op-56325f1261175b"></a>
### Create payment entry bts

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_payment_entry_bts`

**Inputs** bank\_transaction\_name, reference\_number = no value, reference\_date = no value, party\_type = no value, party = no value, posting\_date = no value, mode\_of\_payment = no value, project = no value, cost\_center = no value, allow\_edit = no value, company\_bank\_account = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Transaction” via get\_values · read “Bank Account” via get\_cached\_value · read “Account” via get\_cached\_value.

**State and service calls** request new\_doc for “Payment Entry” · call insert on pe · call submit on pe.

**Explicit results** pe · \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = true).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- If party.
  - Set party from cstr(party).
- Evaluate require\_party\_permission(party\_type, party).
- Set bank\_transaction from Platform.db.get\_values(“Bank Transaction”, bank\_transaction\_name, fieldname = list(“name”, “unallocated\_amount”, “deposit”, “bank\_account”, …), as\_dict = true) at 0.
- Set payment\_type from “Receive” when bank\_transaction.deposit &gt; 0.0, otherwise “Pay”.
  - Value choice on bank\_transaction.deposit &gt; 0.0 — true gives “Receive”, false gives “Pay”.
- Set bank\_account from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).
- Set company from Platform.get\_cached\_value(“Account”, bank\_account, “company”).
- Set party\_account from get\_party\_account(party\_type, party, company).
- Set bank\_currency from bank\_transaction.currency.
- Set party\_currency from Platform.get\_cached\_value(“Account”, party\_account, “account\_currency”).
- Set exc\_rate from get\_exchange\_rate(bank\_currency, party\_currency, posting\_date).
- Set amt\_in\_bank\_acc\_currency from bank\_transaction.unallocated\_amount.
- Set amount\_in\_party\_currency from (bank\_transaction.unallocated\_amount × exc\_rate).
- Set pe from Platform.new\_doc(“Payment Entry”).
- Set pe.payment\_type from payment\_type.
- Set pe.company from company.
- Set pe.reference\_no from reference\_number.
- Set pe.reference\_date from reference\_date.
- Set pe.party\_type from party\_type.
- Set pe.party from party.
- Set pe.posting\_date from posting\_date.
- Set pe.paid\_from from party\_account when payment\_type equals “Receive”, otherwise bank\_account.
  - Value choice on payment\_type equals “Receive” — true gives party\_account, false gives bank\_account.
- Set pe.paid\_to from party\_account when payment\_type equals “Pay”, otherwise bank\_account.
  - Value choice on payment\_type equals “Pay” — true gives party\_account, false gives bank\_account.
- Set pe.paid\_from\_account\_currency from party\_currency when payment\_type equals “Receive”, otherwise bank\_currency.
  - Value choice on payment\_type equals “Receive” — true gives party\_currency, false gives bank\_currency.
- Set pe.paid\_to\_account\_currency from party\_currency when payment\_type equals “Pay”, otherwise bank\_currency.
  - Value choice on payment\_type equals “Pay” — true gives party\_currency, false gives bank\_currency.
- Set pe.paid\_amount from amount\_in\_party\_currency when payment\_type equals “Receive”, otherwise amt\_in\_bank\_acc\_currency.
  - Value choice on payment\_type equals “Receive” — true gives amount\_in\_party\_currency, false gives amt\_in\_bank\_acc\_currency.
- Set pe.received\_amount from amount\_in\_party\_currency when payment\_type equals “Pay”, otherwise amt\_in\_bank\_acc\_currency.
  - Value choice on payment\_type equals “Pay” — true gives amount\_in\_party\_currency, false gives amt\_in\_bank\_acc\_currency.
- Set pe.mode\_of\_payment from mode\_of\_payment.
- Set pe.project from project.
- Set pe.cost\_center from cost\_center.
- If company\_bank\_account.
  - Set pe.bank\_account from company\_bank\_account.
- Evaluate pe.validate().
- If allow\_edit.
  - Return pe.
- Evaluate pe.insert().
- Evaluate pe.submit().
- Set vouchers from json.dumps(list(mapping(“payment\_doctype” → “Payment Entry”, “payment\_name” → pe.name, “amount” → amt\_in\_bank\_acc\_currency))).
- Return \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name) · configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”), Platform.get\_cached\_value(“Account”, bank\_account, “company”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L279)

<a id="op-e30e03d8b33e94"></a>
### Get older unreconciled transactions

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_older_unreconciled_transactions`

**Inputs** bank\_account, from\_date.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** read “Bank Transaction” via count · read “Bank Transaction” via get\_list.

**Explicit results** mapping(“count” → count, “oldest\_date” → oldest\_transaction at 0.date) · mapping(“count” → 0, “oldest\_date” → no value).

**Local steps**

- Set count from Platform.db.count(“Bank Transaction”, filters = mapping(“bank\_account” → bank\_account, “date” → list(“&lt;”, from\_date), “docstatus” → 1, “unallocated\_amount” → list(“&gt;”, 0.0))).
- If count &gt; 0.
  - Set oldest\_transaction from Platform.db.get\_list(“Bank Transaction”, filters = mapping(“bank\_account” → bank\_account, “date” → list(“&lt;”, from\_date), “docstatus” → 1, “unallocated\_amount” → list(“&gt;”, 0.0)), fields = list(“date”), orde ….
  - Return mapping(“count” → count, “oldest\_date” → oldest\_transaction at 0.date).
- Return mapping(“count” → 0, “oldest\_date” → no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L288)
