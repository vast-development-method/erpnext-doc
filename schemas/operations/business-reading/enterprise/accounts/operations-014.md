# Accounting and settlement · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank reconciliation tool

[Record definition](../../../../data/record-types/bank_reconciliation_tool.json)

<a id="op-b79b5349b1786a"></a>
### Update clearance date

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_update_clearance_date`

**Inputs** payment\_document, payment\_entry, account, clearance\_date.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Account” via get\_doc · resolve a document from payment\_document via get\_doc.

**State and service calls** request set\_value on “Sales Invoice Payment” · request set\_value on payment\_document.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “{0} cannot be cleared against a bank statement”.format(payment\_document).

**Local steps**

- If not clearance\_date.
  - Set clearance\_date from no value.
- Evaluate Platform.has\_permission(“Bank Clearance”, ptype = “write”, throw = true).
- If payment\_document does not belong to get\_doctypes\_for\_bank\_reconciliation().
  - Call the validation error handler Platform.throw(translated “{0} cannot be cleared against a bank statement”.format(payment\_document), Platform.PermissionError).
- Set payment\_entry from cstr(payment\_entry).
- If (not payment\_entry or not Platform.has\_permission(payment\_document, “write”, doc = payment\_entry)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not payment\_entry → not Platform.has\_permission(payment\_document, “write”, doc = payment\_entry).
  - Evaluate \_refuse().
- Evaluate Platform.get\_doc(“Account”, account).check\_permission(“read”).
- Set voucher from Platform.get\_doc(payment\_document, payment\_entry).
- Evaluate validate\_clearance\_date(voucher, clearance\_date, account).
- If payment\_document equals “Sales Invoice”.
  - Evaluate Platform.db.set\_value(“Sales Invoice Payment”, mapping(“parent” → payment\_entry, “account” → account, “amount” → list(“!=”, 0)), “clearance\_date”, clearance\_date).
- Otherwise.
  - Evaluate Platform.db.set\_value(payment\_document, payment\_entry, “clearance\_date”, clearance\_date).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Clearance”, ptype = “write”, throw = true), Platform.has\_permission(payment\_document, “write”, doc = payment\_entry).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L298)

<a id="op-77dc5ec43ee4e9"></a>
### Clear clearing date

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_clear_clearing_date`

**Inputs** voucher\_type, voucher\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from voucher\_type via get\_doc.

**State and service calls** request set\_value on “Sales Invoice Payment” · call db\_set on payment\_entry.

**Explicit failure paths** validation helper — translated “{0} is not a voucher this tool can clear”.format(voucher\_type).

**Local steps**

- Evaluate Platform.has\_permission(“Bank Clearance”, ptype = “write”, throw = true).
- If voucher\_type does not belong to get\_doctypes\_for\_bank\_reconciliation().
  - Call the validation error handler Platform.throw(translated “{0} is not a voucher this tool can clear”.format(voucher\_type), title = translated “Invalid Voucher”).
- Set payment\_entry from Platform.get\_doc(voucher\_type, voucher\_name).
- Evaluate validate\_clearance\_date(payment\_entry, no value, no value).
- If voucher\_type equals “Sales Invoice”.
  - Evaluate Platform.db.set\_value(“Sales Invoice Payment”, mapping(“parent” → voucher\_name, “amount” → list(“!=”, 0)), “clearance\_date”, no value).
- Otherwise.
  - Evaluate payment\_entry.db\_set(“clearance\_date”, no value).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Clearance”, ptype = “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L271)

<a id="op-734dfe280d9b13"></a>
### Create bulk internal transfer

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_bulk_internal_transfer`

**Inputs** bank\_transaction\_names, bank\_account.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Transaction” via get\_value · read “Bank Account” via get\_cached\_value.

**Explicit results** output.

**Local steps**

- Set normalised\_names from list().
- For each name in bank\_transaction\_names.
  - Set name from cstr(name).
  - If (not name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = name).
    - Evaluate \_refuse().
  - Evaluate normalised\_names.append(name).
- Set bank\_transaction\_names from normalised\_names.
- Set output from list().
- For each bank\_transaction\_name in bank\_transaction\_names.
  - Set bank\_transaction from Platform.db.get\_value(“Bank Transaction”, bank\_transaction\_name, list(“name”, “withdrawal”, “bank\_account”, “date”, …), as\_dict = true).
  - Set transaction\_account from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).
  - Set is\_withdrawal from bank\_transaction.withdrawal &gt; 0.0.
  - If is\_withdrawal.
    - Set paid\_from from transaction\_account.
    - Set paid\_to from bank\_account.
  - Otherwise.
    - Set paid\_from from bank\_account.
    - Set paid\_to from transaction\_account.
  - Set reference\_no from (bank\_transaction.reference\_number or bank\_transaction.description or empty text) at slice no value to 140.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bank\_transaction.reference\_number → bank\_transaction.description → empty text.
  - Set final\_transaction from create\_internal\_transfer(bank\_transaction\_name = bank\_transaction.name, posting\_date = bank\_transaction.date, reference\_date = bank\_transaction.date, reference\_no = reference\_no, …).
  - Evaluate output.append(final\_transaction).
- Return output.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = name) · configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L274)

<a id="op-1f3921ecda4e19"></a>
### Create internal transfer

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_internal_transfer`

**Inputs** bank\_transaction\_name, posting\_date, reference\_date, reference\_no, paid\_from, paid\_to, custom\_remarks = false, remarks = no value, mirror\_transaction\_name = no value, dimensions = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Transaction” via get\_doc · read “Bank Account” via get\_cached\_value · read “Account” via get\_cached\_value.

**State and service calls** request new\_doc for “Payment Entry” · call insert on pe · call submit on pe.

**Explicit results** mapping(“transaction” → transaction\_id, “payment\_entry” → pe).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- If mirror\_transaction\_name.
  - Set mirror\_transaction\_name from cstr(mirror\_transaction\_name).
  - If (not mirror\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = mirror\_transaction\_name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not mirror\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = mirror\_transaction\_name).
    - Evaluate \_refuse().
- If dimensions.
  - Set allowed\_dimensions from list().
  - For each dimension in get\_dimensions(with\_cost\_center\_and\_project = true) at 0.
    - Evaluate allowed\_dimensions.append(dimension.fieldname).
  - For each fieldname in dimensions.
    - If fieldname does not belong to allowed\_dimensions.
      - Evaluate \_refuse().
- Set bank\_transaction from Platform.get\_doc(“Bank Transaction”, bank\_transaction\_name).
- Set bank\_account from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).
- Set company from Platform.get\_cached\_value(“Account”, bank\_account, “company”).
- Set is\_withdrawal from bank\_transaction.withdrawal &gt; 0.0.
- Set paid\_from from cstr(paid\_from).
- Set paid\_to from cstr(paid\_to).
- Set counterpart\_account from paid\_to when is\_withdrawal, otherwise paid\_from.
  - Value choice on is\_withdrawal — true gives paid\_to, false gives paid\_from.
- If (not counterpart\_account or not Platform.has\_permission(“Account”, “select”, doc = counterpart\_account)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not counterpart\_account → not Platform.has\_permission(“Account”, “select”, doc = counterpart\_account).
  - Evaluate \_refuse().
- Set pe from Platform.new\_doc(“Payment Entry”).
- Set pe.company from company.
- Set pe.payment\_type from “Internal Transfer”.
- Set pe.posting\_date from posting\_date.
- Set pe.reference\_date from reference\_date.
- Set pe.reference\_no from reference\_no.
- Set pe.custom\_remarks from custom\_remarks.
- Set pe.paid\_amount from bank\_transaction.unallocated\_amount.
- Set pe.received\_amount from bank\_transaction.unallocated\_amount.
- Set pe.target\_exchange\_rate from 1.0.
- If custom\_remarks.
  - Set pe.remarks from remarks.
- If dimensions.
  - Evaluate pe.update(dimensions).
- If is\_withdrawal.
  - Set pe.paid\_to from paid\_to.
  - Set pe.paid\_from from bank\_account.
- Otherwise.
  - Set pe.paid\_from from paid\_from.
  - Set pe.paid\_to from bank\_account.
- Evaluate pe.insert().
- Evaluate pe.submit().
- Set vouchers from json.dumps(list(mapping(“payment\_doctype” → “Payment Entry”, “payment\_name” → pe.name, “amount” → bank\_transaction.unallocated\_amount))).
- Set transaction\_id from \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = true).
- If mirror\_transaction\_name.
  - Evaluate \_reconcile\_vouchers(mirror\_transaction\_name, vouchers, is\_new\_voucher = false).
- Return mapping(“transaction” → transaction\_id, “payment\_entry” → pe).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name), Platform.has\_permission(“Bank Transaction”, “write”, doc = mirror\_transaction\_name) and 1 further calls · configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”), Platform.get\_cached\_value(“Account”, bank\_account, “company”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L276)

<a id="op-5c887e38c0e2b2"></a>
### Create bulk bank entry and reconcile

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_bulk_bank_entry_and_reconcile`

**Inputs** bank\_transactions, account.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Transaction” via get\_value · read “Bank Account” via get\_cached\_value.

**Explicit results** output.

**Local steps**

- Set normalised\_names from list().
- For each name in bank\_transactions.
  - Set name from cstr(name).
  - If (not name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = name).
    - Evaluate \_refuse().
  - Evaluate normalised\_names.append(name).
- Set bank\_transactions from normalised\_names.
- Set output from list().
- For each bank\_transaction in bank\_transactions.
  - Set transactions\_details from Platform.db.get\_value(“Bank Transaction”, bank\_transaction, list(“name”, “deposit”, “withdrawal”, “bank\_account”, …), as\_dict = true).
  - Set is\_credit\_card from Platform.get\_cached\_value(“Bank Account”, transactions\_details.bank\_account, “is\_credit\_card”).
  - Set cheque\_no from (transactions\_details.reference\_number or transactions\_details.description or empty text) at slice no value to 140.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transactions\_details.reference\_number → transactions\_details.description → empty text.
  - Set is\_withdrawal from transactions\_details.withdrawal &gt; 0.0.
  - Set entries from list().
  - Set gl\_account from Platform.get\_cached\_value(“Bank Account”, transactions\_details.bank\_account, “account”).
  - If is\_withdrawal.
    - Evaluate entries.append(mapping(“account” → gl\_account, “bank\_account” → transactions\_details.bank\_account, “credit\_in\_account\_currency” → transactions\_details.unallocated\_amount, “credit” → transactions\_details.un ….
    - Evaluate entries.append(mapping(“account” → account, “credit” → 0, “debit” → transactions\_details.unallocated\_amount)).
  - Otherwise.
    - Evaluate entries.append(mapping(“account” → gl\_account, “bank\_account” → transactions\_details.bank\_account, “debit\_in\_account\_currency” → transactions\_details.unallocated\_amount, “debit” → transactions\_details.unal ….
    - Evaluate entries.append(mapping(“account” → account, “debit” → 0, “credit” → transactions\_details.unallocated\_amount)).
  - Set final\_transaction from create\_bank\_entry\_and\_reconcile(bank\_transaction\_name = bank\_transaction, cheque\_date = transactions\_details.date, posting\_date = transactions\_details.date, cheque\_no = cheque\_no, …).
    - Value choice on is\_credit\_card — true gives “Credit Card Entry”, false gives “Bank Entry”.
  - Evaluate output.append(final\_transaction).
- Return output.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = name) · configured or stored value from Platform.get\_cached\_value(“Bank Account”, transactions\_details.bank\_account, “is\_credit\_card”), Platform.get\_cached\_value(“Bank Account”, transactions\_details.bank\_account, “account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L273)

<a id="op-21a6f363a424dd"></a>
### Create bank entry and reconcile

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_bank_entry_and_reconcile`

**Inputs** bank\_transaction\_name, cheque\_date, posting\_date, cheque\_no, entries, user\_remark = no value, voucher\_type = “Bank Entry”, dimensions = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Transaction” via get\_values · read “Bank Account” via get\_cached\_value · read “Account” via get\_cached\_value · resolve a document from mapping(“doctype” → “Journal Entry”, “voucher\_type” → voucher\_type, “company” → company, “cheque\_date” → cheque\_date, …) via get\_doc.

**State and service calls** call insert on bank\_entry · call submit on bank\_entry.

**Explicit results** mapping(“transaction” → transaction, “journal\_entry” → bank\_entry).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- For each entry in entries.
  - If entry.get(“party”).
    - Set entry at “party” from cstr(entry at “party”).
  - Evaluate require\_party\_permission(entry.get(“party\_type”), entry.get(“party”)).
- Set bank\_transaction from Platform.db.get\_values(“Bank Transaction”, bank\_transaction\_name, fieldname = list(“name”, “deposit”, “withdrawal”, “bank\_account”, …), as\_dict = true) at 0.
- Set bank\_account from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).
- Set company from Platform.get\_cached\_value(“Account”, bank\_account, “company”).
- Set default\_cost\_center from get\_default\_cost\_center(company).
- Set bank\_entry from Platform.get\_doc(mapping(“doctype” → “Journal Entry”, “voucher\_type” → voucher\_type, “company” → company, “cheque\_date” → cheque\_date, …)).
- If not dimensions.
  - Set dimensions from mapping().
- For each entry in entries.
  - Set cost\_center from entry.get(“cost\_center”).
  - If not cost\_center.
    - Set report\_type from Platform.get\_cached\_value(“Account”, entry at “account”, “report\_type”).
    - If report\_type equals “Profit and Loss”.
      - Set cost\_center from default\_cost\_center.
  - Evaluate bank\_entry.append(“accounts”, mapping(“account” → entry at “account”, “debit\_in\_account\_currency” → entry.get(“debit”), “credit\_in\_account\_currency” → entry.get(“credit”), “debit” → entry.get(“debit”), …)).
    - Value choice on entry.get(“party”) — true gives entry.get(“party\_type”), false gives no value.
- Evaluate bank\_entry.insert().
- Evaluate bank\_entry.submit().
- If bank\_transaction.deposit &gt; 0.0.
  - Set paid\_amount from bank\_transaction.deposit.
- Otherwise.
  - Set paid\_amount from bank\_transaction.withdrawal.
- Set transaction from \_reconcile\_vouchers(bank\_transaction\_name, json.dumps(list(mapping(“payment\_doctype” → “Journal Entry”, “payment\_name” → bank\_entry.name, “amount” → paid\_amount))), is\_new\_voucher = true).
- Return mapping(“transaction” → transaction, “journal\_entry” → bank\_entry).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name) · configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”), Platform.get\_cached\_value(“Account”, bank\_account, “company”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L272)

<a id="op-d5e4bcea5d7484"></a>
### Create bulk payment entry and reconcile

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_bulk_payment_entry_and_reconcile`

**Inputs** bank\_transaction\_names, party\_type, party, account, mode\_of\_payment = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Transaction” via get\_value · read “Bank Account” via get\_cached\_value · resolve a document from mapping(“doctype” → “Payment Entry”, “payment\_type” → “Pay” when is\_withdrawal, otherwise “Receive”, “bank\_account” → bank\_transaction.bank\_account, “company” → bank\_transaction.company, …) via get\_doc.

**State and service calls** call insert on payment\_entry\_doc · call submit on payment\_entry\_doc.

**Explicit results** output.

**Local steps**

- Set normalised\_names from list().
- For each name in bank\_transaction\_names.
  - Set name from cstr(name).
  - If (not name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = name).
    - Evaluate \_refuse().
  - Evaluate normalised\_names.append(name).
- Set bank\_transaction\_names from normalised\_names.
- If party.
  - Set party from cstr(party).
- Evaluate require\_party\_permission(party\_type, party).
- Set output from list().
- For each bank\_transaction\_name in bank\_transaction\_names.
  - Set bank\_transaction from Platform.db.get\_value(“Bank Transaction”, bank\_transaction\_name, list(“name”, “deposit”, “withdrawal”, “bank\_account”, …), as\_dict = true).
  - Set transaction\_account from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).
  - Set is\_withdrawal from bank\_transaction.withdrawal &gt; 0.0.
  - If is\_withdrawal.
    - Set paid\_from from transaction\_account.
    - Set paid\_to from account.
  - Otherwise.
    - Set paid\_from from account.
    - Set paid\_to from transaction\_account.
  - Set payment\_entry\_doc from Platform.get\_doc(mapping(“doctype” → “Payment Entry”, “payment\_type” → “Pay” when is\_withdrawal, otherwise “Receive”, “bank\_account” → bank\_transaction.bank\_account, “company” → bank\_transaction.company, …)).
    - Value choice on is\_withdrawal — true gives “Pay”, false gives “Receive”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bank\_transaction.reference\_number → bank\_transaction.description → empty text.
  - Evaluate set\_multi\_currency\_amounts(payment\_entry\_doc).
  - Evaluate payment\_entry\_doc.insert().
  - Evaluate payment\_entry\_doc.submit().
  - Set final\_transaction from \_reconcile\_vouchers(bank\_transaction\_name, json.dumps(list(mapping(“payment\_doctype” → “Payment Entry”, “payment\_name” → payment\_entry\_doc.name, “amount” → payment\_entry\_doc.paid\_amount))), is\_new\_voucher = true).
  - Evaluate output.append(mapping(“transaction” → final\_transaction, “payment\_entry” → payment\_entry\_doc)).
- Return output.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = name) · configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_transaction.bank\_account, “account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L275)

<a id="op-154453b8e76891"></a>
### Create payment entry and reconcile

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_create_payment_entry_and_reconcile`

**Inputs** bank\_transaction\_name, payment\_entry\_doc.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(expand payment\_entry\_doc, “doctype” → “Payment Entry”) via get\_doc.

**State and service calls** call insert on payment\_entry · call submit on payment\_entry.

**Explicit results** mapping(“transaction” → transaction, “payment\_entry” → payment\_entry).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- If payment\_entry\_doc.get(“party”).
  - Set payment\_entry\_doc at “party” from cstr(payment\_entry\_doc at “party”).
- Evaluate require\_party\_permission(payment\_entry\_doc.get(“party\_type”), payment\_entry\_doc.get(“party”)).
- Set payment\_entry from Platform.get\_doc(mapping(expand payment\_entry\_doc, “doctype” → “Payment Entry”)).
- Evaluate set\_multi\_currency\_amounts(payment\_entry).
- Evaluate payment\_entry.insert().
- Evaluate payment\_entry.submit().
- Set transaction from \_reconcile\_vouchers(bank\_transaction\_name, json.dumps(list(mapping(“payment\_doctype” → “Payment Entry”, “payment\_name” → payment\_entry.name, “amount” → payment\_entry.paid\_amount))), is\_new\_voucher = true).
- Return mapping(“transaction” → transaction, “payment\_entry” → payment\_entry).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L278)

<a id="op-4da5d976daf097"></a>
### Set multi currency amounts

`operation_enterprise_binding_enterprise_accounts_doctype_bank_reconciliation_tool_bank_reconciliation_tool_set_multi_currency_amounts`

**Inputs** pe.

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_cached\_value.

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, pe.company, “default\_currency”).
- Set pe.paid\_from\_account\_currency from Platform.get\_cached\_value(“Account”, pe.paid\_from, “account\_currency”).
- Set pe.paid\_to\_account\_currency from Platform.get\_cached\_value(“Account”, pe.paid\_to, “account\_currency”).
- Set pe.source\_exchange\_rate from 1.0 when pe.paid\_from\_account\_currency equals company\_currency, otherwise get\_exchange\_rate(pe.paid\_from\_account\_currency, company\_currency, pe.posting\_date).
  - Value choice on pe.paid\_from\_account\_currency equals company\_currency — true gives 1.0, false gives get\_exchange\_rate(pe.paid\_from\_account\_currency, company\_currency, pe.posting\_date).
- Set pe.target\_exchange\_rate from 1.0 when pe.paid\_to\_account\_currency equals company\_currency, otherwise get\_exchange\_rate(pe.paid\_to\_account\_currency, company\_currency, pe.posting\_date).
  - Value choice on pe.paid\_to\_account\_currency equals company\_currency — true gives 1.0, false gives get\_exchange\_rate(pe.paid\_to\_account\_currency, company\_currency, pe.posting\_date).
- If (pe.payment\_type equals “Receive” and pe.source\_exchange\_rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pe.payment\_type equals “Receive” → pe.source\_exchange\_rate.
  - Set base\_amount from (flt(pe.received\_amount) × pe.target\_exchange\_rate).
  - Set pe.paid\_amount from flt((base\_amount ÷ pe.source\_exchange\_rate), pe.precision(“paid\_amount”)).
- Otherwise.
  - If (pe.payment\_type equals “Pay” and pe.target\_exchange\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pe.payment\_type equals “Pay” → pe.target\_exchange\_rate.
    - Set base\_amount from (flt(pe.paid\_amount) × pe.source\_exchange\_rate).
    - Set pe.received\_amount from flt((base\_amount ÷ pe.target\_exchange\_rate), pe.precision(“received\_amount”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, pe.company, “default\_currency”), Platform.get\_cached\_value(“Account”, pe.paid\_from, “account\_currency”) and 1 further calls.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L770)

<a id="op-b50169cd229e7f"></a>
### Search for transfer transaction

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_search_for_transfer_transaction`

**Inputs** transaction\_id.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** read “Bank Transaction” via get\_value · read “Accounts Settings” via get\_single\_value · read “Bank Transaction” via get\_list · read “Bank Account” via get\_cached\_value.

**Explicit results** mapping(“name” → mirror\_tx at 0.name, “reference\_number” → mirror\_tx at 0.reference\_number, “description” → mirror\_tx at 0.description, “currency” → mirror\_tx at 0.currency, …) · no value.

**Local steps**

- Set tuple(company, withdrawal, deposit, date, …) from Platform.db.get\_value(“Bank Transaction”, transaction\_id, list(“company”, “withdrawal”, “deposit”, “date”, …)).
- Set days from Platform.db.get\_single\_value(“Accounts Settings”, “transfer\_match\_days”).
- If days is identical to no value.
  - Set days from 3.
- Set min\_date from Platform.utils.add\_days(date, negative days).
- Set max\_date from Platform.utils.add\_days(date, days).
- Set mirror\_tx from Platform.db.get\_list(“Bank Transaction”, filters = mapping(“company” → company, “date” → list(“between”, list(min\_date, max\_date)), “withdrawal” → deposit, “bank\_account” → list(“!=”, bank\_account), …), fi ….
- If len(mirror\_tx) equals 1.
  - Return mapping(“name” → mirror\_tx at 0.name, “reference\_number” → mirror\_tx at 0.reference\_number, “description” → mirror\_tx at 0.description, “currency” → mirror\_tx at 0.currency, …).
- Return no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “transfer\_match\_days”), Platform.get\_cached\_value(“Bank Account”, mirror\_tx at 0.bank\_account, “account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L294)

<a id="op-8a0306c754ea52"></a>
### Auto reconcile vouchers

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_auto_reconcile_vouchers`

**Inputs** bank\_account, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue · msgprint with translated “Auto Reconciliation has started in the background”.

**Local steps**

- Set bank\_account from cstr(bank\_account).
- If (not bank\_account or not Platform.has\_permission(“Bank Account”, “read”, doc = bank\_account)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_account → not Platform.has\_permission(“Bank Account”, “read”, doc = bank\_account).
  - Evaluate \_refuse().
- Evaluate validate\_date\_range(from\_date, to\_date, filter\_by\_reference\_date, from\_reference\_date, …).
- Set listed\_transactions from get\_bank\_transactions(bank\_account).
- Set bank\_transactions from list().
- For each transaction in listed\_transactions.
  - If \_is\_permitted(“Bank Transaction”, transaction.name, “write”).
    - Evaluate bank\_transactions.append(transaction).
- If len(bank\_transactions) &gt; 10.
  - For each bank\_transaction\_batch in create\_batch(bank\_transactions, 1000).
    - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.bank\_reconciliation\_tool.bank\_reconciliation\_tool.start\_auto\_reconcile”, queue = “long”, bank\_transactions = bank\_transaction\_batch, from\_date = from\_date, …).
  - Evaluate Platform.msgprint(translated “Auto Reconciliation has started in the background”).
- Otherwise.
  - Evaluate start\_auto\_reconcile(bank\_transactions, from\_date, to\_date, filter\_by\_reference\_date, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Account”, “read”, doc = bank\_account) · service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.bank\_reconciliation\_tool.bank\_reconciliation\_tool.start\_auto\_reconcile”, queue = “long”, bank\_transactions = bank\_transaction\_batch, from\_date = from\_date, …).

**Boundaries to resolve** external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L269)

<a id="op-a158683ec922f4"></a>
### Start auto reconcile

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_start_auto_reconcile`

**Inputs** bank\_transactions, from\_date, to\_date, filter\_by\_reference\_date, from\_reference\_date, to\_reference\_date.

**State and service calls** msgprint.

**Local steps**

- Set Platform.flags.auto\_reconcile\_vouchers from true.
- Set tuple(reconciled, partially\_reconciled) from tuple(set(), set()).
- For each transaction in bank\_transactions.
  - Set linked\_payments from \_get\_linked\_payments(transaction.name, list(“payment\_entry”, “journal\_entry”, “sales\_invoice”), from\_date, to\_date, …).
  - If not linked\_payments.
    - Continue with the next iteration or loop test.
  - Set vouchers from list(map(deferred anonymous expression, linked\_payments)).
  - Set vouchers from get\_writable\_linked\_vouchers(vouchers).
  - If not vouchers.
    - Continue with the next iteration or loop test.
  - Set updated\_transaction from \_reconcile\_vouchers(transaction.name, json.dumps(vouchers)).
  - If updated\_transaction.status equals “Reconciled”.
    - Evaluate reconciled.add(updated\_transaction.name).
  - Otherwise.
    - If flt(transaction.unallocated\_amount) differs from flt(updated\_transaction.unallocated\_amount).
      - Evaluate partially\_reconciled.add(updated\_transaction.name).
- Set tuple(alert\_message, indicator) from get\_auto\_reconcile\_message(partially\_reconciled, reconciled).
- Evaluate Platform.msgprint(title = translated “Auto Reconciliation”, msg = alert\_message, indicator = indicator).
- Set Platform.flags.auto\_reconcile\_vouchers from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L295)

<a id="op-e7a4e1be2e1627"></a>
### Get auto reconcile message

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_auto_reconcile_message`

**Inputs** partially\_reconciled, reconciled.

**Explicit results** tuple(alert\_message, indicator).

**Local steps**

- Set tuple(alert\_message, indicator) from tuple(empty text, “blue”).
- If (not partially\_reconciled and not reconciled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not partially\_reconciled → not reconciled.
  - Set alert\_message from translated “No matches occurred via auto reconciliation”.
  - Return tuple(alert\_message, indicator).
- Set indicator from “green”.
- If reconciled.
  - Update alert\_message using + translated “{0} Transaction(s) Reconciled”.format(len(reconciled)).
  - Update alert\_message using + text in the contract.
- If partially\_reconciled.
  - Update alert\_message using + translated “{0} {1} Partially Reconciled”.format(len(partially\_reconciled), translated “Transactions” when len(partially\_reconciled) &gt; 1, otherwise translated “Transaction”).
    - Value choice on len(partially\_reconciled) &gt; 1 — true gives translated “Transactions”, false gives translated “Transaction”.
- Return tuple(alert\_message, indicator).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L2200) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L282)

<a id="op-efae15c02a9d01"></a>
### Reconcile vouchers

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_reconcile_vouchers`

**Inputs** bank\_transaction\_name, vouchers, is\_new\_voucher = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = is\_new\_voucher).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “{0} cannot be reconciled against a Bank Transaction”.format(payment\_doctype).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- Set vouchers from json.loads(vouchers).
- Set reconcilable\_doctypes from get\_reconcilable\_doctypes().
- For each voucher in vouchers.
  - Set payment\_doctype from voucher.get(“payment\_doctype”).
  - If payment\_doctype does not belong to reconcilable\_doctypes.
    - Call the validation error handler Platform.throw(translated “{0} cannot be reconciled against a Bank Transaction”.format(payment\_doctype), Platform.PermissionError).
  - Set voucher at “payment\_name” from cstr(voucher.get(“payment\_name”)).
  - If (not voucher at “payment\_name” or not Platform.has\_permission(payment\_doctype, “write”, doc = voucher at “payment\_name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not voucher at “payment\_name” → not Platform.has\_permission(payment\_doctype, “write”, doc = voucher at “payment\_name”).
    - Evaluate \_refuse().
- Return \_reconcile\_vouchers(bank\_transaction\_name, vouchers, is\_new\_voucher = is\_new\_voucher).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”, doc = bank\_transaction\_name), Platform.has\_permission(payment\_doctype, “write”, doc = voucher at “payment\_name”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L293)

<a id="op-1bed8879e9ed8b"></a>
### Reconcile vouchers

`operation_enterprise_binding_enterprise_accounts_doctype_bank_reconciliation_tool_bank_reconciliation_tool_reconcile_vouchers`

**Inputs** bank\_transaction\_name, vouchers, is\_new\_voucher = false.

**Record and data access** resolve a document from “Bank Transaction” via get\_doc.

**State and service calls** call save on transaction.

**Explicit results** transaction.

**Local steps**

- If isinstance(vouchers, str).
  - Set vouchers from json.loads(vouchers).
- Set transaction from Platform.get\_doc(“Bank Transaction”, bank\_transaction\_name).
- Evaluate transaction.add\_payment\_entries(vouchers, is\_new\_voucher).
- Evaluate transaction.validate\_duplicate\_references().
- Evaluate transaction.allocate\_payment\_entries().
- Evaluate transaction.update\_allocated\_amount().
- Evaluate transaction.set\_status().
- Evaluate transaction.save().
- Return transaction.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L769)

<a id="op-c74bdfb144b9af"></a>
### Get linked payments

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_linked_payments`

**Inputs** bank\_transaction\_name, document\_types = no value, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list of voucher for voucher drawn from vouchers where (voucher.get(“doctype”) and \_is\_permitted(voucher at “doctype”, voucher.get(“name”), “read”)).

**Local steps**

- Set bank\_transaction\_name from cstr(bank\_transaction\_name).
- If (not bank\_transaction\_name or not Platform.has\_permission(“Bank Transaction”, “read”, doc = bank\_transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_transaction\_name → not Platform.has\_permission(“Bank Transaction”, “read”, doc = bank\_transaction\_name).
  - Evaluate \_refuse().
- Set vouchers from \_get\_linked\_payments(bank\_transaction\_name, document\_types, from\_date, to\_date, …).
- Return list of voucher for voucher drawn from vouchers where (voucher.get(“doctype”) and \_is\_permitted(voucher at “doctype”, voucher.get(“name”), “read”)).
  - Draw voucher from vouchers, keep a combination only if ((voucher.get(“doctype”) and \_is\_permitted(voucher at “doctype”, voucher.get(“name”), “read”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher.get(“doctype”) → \_is\_permitted(voucher at “doctype”, voucher.get(“name”), “read”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “read”, doc = bank\_transaction\_name).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L286)

<a id="op-7c7a3cb732a577"></a>
### Get linked payments

`operation_enterprise_binding_enterprise_accounts_doctype_bank_reconciliation_tool_bank_reconciliation_tool_get_linked_payments`

**Inputs** bank\_transaction\_name, document\_types = no value, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value.

**Record and data access** resolve a document from “Bank Transaction” via get\_doc · read “Bank Account” via get\_values.

**Explicit results** subtract\_allocations(gl\_account, matching).

**Local steps**

- Evaluate validate\_date\_range(from\_date, to\_date, filter\_by\_reference\_date, from\_reference\_date, …).
- Set transaction from Platform.get\_doc(“Bank Transaction”, bank\_transaction\_name).
- Set bank\_account from Platform.db.get\_values(“Bank Account”, transaction.bank\_account, list(“account”, “company”), as\_dict = true) at 0.
- Set tuple(gl\_account, company) from tuple(bank\_account.account, bank\_account.company).
- Set matching from check\_matching(gl\_account, company, transaction, document\_types, …).
- Return subtract\_allocations(gl\_account, matching).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L766)

<a id="op-159bb82feb2153"></a>
### Get writable linked vouchers

`operation_enterprise_binding_enterprise_accounts_doctype_bank_reconciliation_tool_bank_reconciliation_tool_get_writable_linked_vouchers`

**Inputs** vouchers.

**Declared result** list.

**Explicit results** writable\_vouchers.

**Local steps**

- Set reconcilable\_doctypes from get\_reconcilable\_doctypes().
- Set writable\_vouchers from list().
- For each voucher in vouchers.
  - Set payment\_doctype from voucher.get(“payment\_doctype”).
  - If payment\_doctype does not belong to reconcilable\_doctypes.
    - Continue with the next iteration or loop test.
  - If \_is\_permitted(payment\_doctype, voucher.get(“payment\_name”), “write”).
    - Evaluate writable\_vouchers.append(voucher).
- Return writable\_vouchers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L768)

<a id="op-cd5c354022e6f1"></a>
### Get reconcilable doctypes

`operation_enterprise_binding_enterprise_accounts_doctype_bank_reconciliation_tool_bank_reconciliation_tool_get_reconcilable_doctypes`

**Inputs** no declared parameters.

**Declared result** list.

**Explicit results** list(expanded get\_doctypes\_for\_bank\_reconciliation(), “Bank Transaction”).

**Local steps**

- Return list(expanded get\_doctypes\_for\_bank\_reconciliation(), “Bank Transaction”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L767)

<a id="op-5f975fef51b355"></a>
### Validate date range

`operation_enterprise_binding_enterprise_accounts_doctype_bank_reconciliation_tool_bank_reconciliation_tool_validate_date_range`

**Inputs** from\_date, to\_date, filter\_by\_reference\_date = false, from\_reference\_date = no value, to\_reference\_date = no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If cint(filter\_by\_reference\_date).
  - Set tuple(from\_date, to\_date) from tuple(from\_reference\_date, to\_reference\_date).
  - Set message from translated “From Reference Date cannot be greater than To Reference Date”.
- Otherwise.
  - Set message from translated “From Date cannot be greater than To Date”.
- If (from\_date and to\_date and getdate(from\_date) &gt; getdate(to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date → getdate(from\_date) &gt; getdate(to\_date).
  - Call the validation error handler Platform.throw(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L771)

<a id="op-99c5f8911417e6"></a>
### Subtract allocations

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_subtract_allocations`

**Inputs** gl\_account, vouchers.

**Explicit results** copied.

**Local steps**

- Set copied from list().
- Set voucher\_docs from list of tuple(voucher.get(“doctype”), voucher.get(“name”)) for voucher drawn from vouchers.
  - Draw voucher from vouchers.
- Set voucher\_allocated\_amounts from get\_total\_allocated\_amount(voucher\_docs).
- For each voucher in vouchers.
  - If amount bound to get\_allocated\_amount(voucher\_allocated\_amounts, voucher, gl\_account).
    - Update voucher at “paid\_amount” using − amount.
  - Evaluate copied.append(voucher).
- Return copied.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L3360) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L296)

<a id="op-b070a4b1bafa12"></a>
### Get allocated amount

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_allocated_amount`

**Inputs** voucher\_allocated\_amounts, voucher, gl\_account.

**Explicit results** no value · row.get(“total”).

**Local steps**

- If not voucher\_details bound to voucher\_allocated\_amounts.get(tuple(voucher.get(“doctype”), voucher.get(“name”))).
  - Return no value.
- If not row bound to voucher\_details.get(gl\_account).
  - Return no value.
- Return row.get(“total”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L3628) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L281)

<a id="op-82c65fc7e194f9"></a>
### Check matching

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_check_matching`

**Inputs** bank\_account, company, transaction, document\_types = no value, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value.

**Explicit results** sorted(matching\_vouchers, key = deferred anonymous expression, reverse = true) when matching\_vouchers, otherwise list().

**Local steps**

- Set document\_types from (document\_types or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in document\_types → list().
- Set exact\_match from true when “exact\_match” belongs to document\_types, otherwise false.
  - Value choice on “exact\_match” belongs to document\_types — true gives true, false gives false.
- Set common\_filters from Platform.\_dict(mapping(“amount” → transaction.unallocated\_amount, “payment\_type” → “Receive” when transaction.deposit &gt; 0.0, otherwise “Pay”, “reference\_no” → transaction.reference\_number, “party\_type” → t ….
  - Value choice on transaction.deposit &gt; 0.0 — true gives “Receive”, false gives “Pay”.
- Set queries from get\_queries(bank\_account, company, transaction, document\_types, …).
- Set matching\_vouchers from list().
- For each query in queries.
  - Evaluate matching\_vouchers.extend(query.run(as\_dict = true)).
- Return sorted(matching\_vouchers, key = deferred anonymous expression, reverse = true) when matching\_vouchers, otherwise list().
  - Value choice on matching\_vouchers — true gives sorted(matching\_vouchers, key = deferred anonymous expression, reverse = true), false gives list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L270)

<a id="op-7eb2a50ad210a3"></a>
### Get queries

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_queries`

**Inputs** bank\_account, company, transaction, document\_types = no value, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value, exact\_match = no value, common\_filters = no value.

**Explicit results** queries.

**Local steps**

- Set account\_from\_to from “paid\_to” when transaction.deposit &gt; 0.0, otherwise “paid\_from”.
  - Value choice on transaction.deposit &gt; 0.0 — true gives “paid\_to”, false gives “paid\_from”.
- Set queries from list().
- For each method\_name in Platform.get\_hooks(“get\_matching\_queries”).
  - Evaluate queries.extend((Platform.get\_attr(method\_name)(bank\_account, company, transaction, document\_types, …) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method\_name)(bank\_account, company, transaction, document\_types, …) → list().
- Return queries.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_matching\_queries”), Platform.get\_attr(method\_name).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L4355) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L291)
