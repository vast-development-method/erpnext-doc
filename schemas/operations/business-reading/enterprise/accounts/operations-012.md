# Accounting and settlement · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank account

[Record definition](../../../../data/record-types/bank_account.json)

<a id="op-7107f4f86c6bdf"></a>
### Bank Account.autoname

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_autoname`

**Inputs** self.

**Local steps**

- Set self.name from ((self.account\_name + “ - ”) + self.bank).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3531) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L237)

<a id="op-7f706b130489c6"></a>
### Bank Account.on trash

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_on_trash`

**Inputs** self.

**State and service calls** request delete on “Bank Account Balance”.

**Local steps**

- Evaluate delete\_contact\_and\_address(“Bank Account”, self.name).
- Evaluate Platform.db.delete(“Bank Account Balance”, filters = mapping(“bank\_account” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3604) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L238)

<a id="op-8bcd8e0644fa8e"></a>
### Bank Account.validate

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_is\_company\_account().
- Evaluate self.update\_default\_bank\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate is company account](operations-012.md#op-7f90a9caa74ef5), [update default bank account](operations-012.md#op-b180fda2e50a56).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3737) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L241)

<a id="op-7f90a9caa74ef5"></a>
### Bank Account.validate is company account

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_validate_is_company_account`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company is mandatory for company account” · validation helper — translated “Company Account is mandatory”.

**Local steps**

- If self.is\_company\_account.
  - If not self.company.
    - Call the validation error handler Platform.throw(translated “Company is mandatory for company account”).
  - If not self.account.
    - Call the validation error handler Platform.throw(translated “Company Account is mandatory”).
  - Evaluate self.validate\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account](operations-012.md#op-c44a40318d377e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3808) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L243)

<a id="op-c44a40318d377e"></a>
### Bank Account.validate account

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_validate_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · read “Bank Account” via get\_all.

**Explicit failure paths** validation helper — translated “Account {0} does not belong to Company {1}”.format(self.account, self.company) · validation helper — translated “Account {0} must be a non-group account of type Bank”.format(self.account) · validation helper — translated “'{0}' account is already used by {1}. Use another account.”.format(Platform.bold(self.account), Platform.bold(comma\_and(list of get\_link\_to\_form(self.doctype, x at 0) for x drawn from accounts))).

**Local steps**

- Set account from Platform.get\_cached\_value(“Account”, self.account, list(“company”, “account\_type”, “is\_group”), as\_dict = true).
- If account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Account {0} does not belong to Company {1}”.format(self.account, self.company)).
- If (account.is\_group or account.account\_type differs from “Bank”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.is\_group → account.account\_type differs from “Bank”.
  - Call the validation error handler Platform.throw(translated “Account {0} must be a non-group account of type Bank”.format(self.account)).
- If accounts bound to Platform.db.get\_all(“Bank Account”, filters = mapping(“account” → self.account, “name” → list(“!=”, self.name)), as\_list = 1).
  - Call the validation error handler Platform.throw(translated “'{0}' account is already used by {1}. Use another account.”.format(Platform.bold(self.account), Platform.bold(comma\_and(list of get\_link\_to\_form(nested operand in the contract.do ….
    - Draw x from accounts.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, list(“company”, “account\_type”, “is\_group”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L242)

<a id="op-b180fda2e50a56"></a>
### Bank Account.update default bank account

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_update_default_bank_account`

**Inputs** self.

**State and service calls** request set\_value on “Bank Account”.

**Local steps**

- If self.disabled.
  - Set self.is\_default from 0.
- If self.is\_default.
  - Evaluate Platform.db.set\_value(“Bank Account”, mapping(“party\_type” → self.party\_type, “party” → self.party, “is\_company\_account” → self.is\_company\_account, “company” → self.company, …), “is\_default”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L240)

<a id="op-339688536fdf91"></a>
### Get party bank account

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_get_party_bank_account`

**Inputs** party\_type, party.

**Record and data access** read “Bank Account” via get\_value.

**Explicit results** Platform.db.get\_value(“Bank Account”, mapping(“party\_type” → party\_type, “party” → party, “is\_default” → 1, “disabled” → 0), “name”).

**Local steps**

- Return Platform.db.get\_value(“Bank Account”, mapping(“party\_type” → party\_type, “party” → party, “is\_default” → 1, “disabled” → 0), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L4514) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L248)

<a id="op-942f66fb48365f"></a>
### Get default company bank account

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_get_default_company_bank_account`

**Inputs** company, party\_type, party, ignore\_permissions = true.

**Record and data access** read party\_type via get\_value · read “Bank Account” via get\_cached\_value · read “Bank Account” via get\_value · resolve a document from “Bank Account” via get\_cached\_doc.

**Explicit results** default\_company\_bank\_account.

**Local steps**

- Set default\_company\_bank\_account from Platform.db.get\_value(party\_type, party, “default\_bank\_account”).
- If default\_company\_bank\_account.
  - Set bank\_account from Platform.get\_cached\_value(“Bank Account”, default\_company\_bank\_account, list(“company”, “disabled”), as\_dict = true).
  - If (not bank\_account or bank\_account.company differs from company or bank\_account.disabled).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_account → bank\_account.company differs from company → bank\_account.disabled.
    - Set default\_company\_bank\_account from no value.
- If not default\_company\_bank\_account.
  - Set default\_company\_bank\_account from Platform.db.get\_value(“Bank Account”, mapping(“company” → company, “is\_company\_account” → 1, “is\_default” → 1, “disabled” → 0)).
- If not ignore\_permissions.
  - Set default\_company\_bank\_account from default\_company\_bank\_account when (default\_company\_bank\_account and Platform.get\_cached\_doc(“Bank Account”, default\_company\_bank\_account).has\_permission(“select”)), otherwise no value.
    - Value choice on (default\_company\_bank\_account and Platform.get\_cached\_doc(“Bank Account”, default\_company\_bank\_account).has\_permission(“select”)) — true gives default\_company\_bank\_account, false gives no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_company\_bank\_account → Platform.get\_cached\_doc(“Bank Account”, default\_company\_bank\_account).has\_permission(“select”).
- Return default\_company\_bank\_account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, default\_company\_bank\_account, list(“company”, “disabled”), as\_dict = true), Platform.get\_cached\_doc(“Bank Account”, default\_company\_bank\_account).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L246)

<a id="op-e0c84a68b1bc66"></a>
### Get bank account details

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_get_bank_account_details`

**Inputs** bank\_account.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Bank Account” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Bank Account”, bank\_account, list(“account”, “bank”, “bank\_account\_no”), as\_dict = 1).

**Local steps**

- Evaluate Platform.has\_permission(“Bank Account”, doc = bank\_account, ptype = “read”, throw = true).
- Return Platform.get\_cached\_value(“Bank Account”, bank\_account, list(“account”, “bank”, “bank\_account\_no”), as\_dict = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Account”, doc = bank\_account, ptype = “read”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_account, list(“account”, “bank”, “bank\_account\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L244)

<a id="op-0574001774f6bb"></a>
### Get list

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_get_list`

**Inputs** company, show\_disabled = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** read “Bank Account” via get\_list · read “Account” via get\_cached\_value.

**Explicit results** bank\_accounts.

**Local steps**

- Set filters from mapping(“is\_company\_account” → 1, “company” → company).
- If not show\_disabled.
  - Set filters at “disabled” from 0.
- Set bank\_accounts from Platform.get\_list(“Bank Account”, filters = filters, order\_by = “is\_default desc”, fields = list(“name”, “account”, “company”, “account\_name”, …)).
- For each bank\_account in bank\_accounts.
  - Set bank\_account.account\_currency from Platform.get\_cached\_value(“Account”, bank\_account.account, “account\_currency”).
- Return bank\_accounts.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, bank\_account.account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L5241) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L247)

<a id="op-bfb9b07aa5b969"></a>
### Get closing balance as per statement

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_get_closing_balance_as_per_statement`

**Inputs** bank\_account, date.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** read “Bank Account Balance” via get\_list.

**Explicit results** mapping(“balance” → latest\_balance at 0.balance, “date” → latest\_balance at 0.date) · mapping(“balance” → 0, “date” → no value).

**Local steps**

- Set latest\_balance from Platform.get\_list(“Bank Account Balance”, filters = mapping(“bank\_account” → bank\_account, “date” → list(“&lt;=”, date)), fields = list(“balance”, “date”), order\_by = “date desc”, limit = 1).
- If latest\_balance.
  - Return mapping(“balance” → latest\_balance at 0.balance, “date” → latest\_balance at 0.date).
- Return mapping(“balance” → 0, “date” → no value).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L5654) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L245)

<a id="op-dd9a4c8620b716"></a>
### Set closing balance as per statement

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_set_closing_balance_as_per_statement`

**Inputs** bank\_account, date, balance.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** \_set\_closing\_balance\_as\_per\_statement(bank\_account, date, balance).

**Local steps**

- Set bank\_account from cstr(bank\_account).
- If (not bank\_account or not Platform.has\_permission(“Bank Account”, “write”, doc = bank\_account)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_account → not Platform.has\_permission(“Bank Account”, “write”, doc = bank\_account).
  - Evaluate \_refuse().
- Return \_set\_closing\_balance\_as\_per\_statement(bank\_account, date, balance).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Account”, “write”, doc = bank\_account).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L249)

<a id="op-e132716b89276a"></a>
### Set closing balance as per statement

`operation_enterprise_binding_enterprise_accounts_doctype_bank_account_bank_account_set_closing_balance_as_per_statement`

**Inputs** bank\_account, date, balance.

**Record and data access** read “Bank Account Balance” via exists · resolve a document from “Bank Account Balance” via get\_doc.

**State and service calls** call save on doc · request new\_doc for “Bank Account Balance”.

**Local steps**

- Set existing from Platform.db.exists(“Bank Account Balance”, mapping(“bank\_account” → bank\_account, “date” → date)).
- If existing.
  - Set doc from Platform.get\_doc(“Bank Account Balance”, existing).
  - Set doc.balance from balance.
  - Evaluate doc.save().
- Otherwise.
  - Set doc from Platform.new\_doc(“Bank Account Balance”).
  - Set doc.bank\_account from bank\_account.
  - Set doc.date from date.
  - Set doc.balance from balance.
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L762)

## Record · Bank account balance

[Record definition](../../../../data/record-types/bank_account_balance.json)

<a id="op-1bb00e88296e77"></a>
### Bank Account Balance.validate

`operation_enterprise_binding_enterprise_accounts_doctype_bank_account_balance_bank_account_balance_bankaccountbalance_validate`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_value · read self.doctype via exists.

**Explicit failure paths** validation helper — translated “Closing balances can only be recorded for company bank accounts.” · validation helper with Platform.DuplicateEntryError — translated “A closing balance already exists for Bank Account {0} on {1}.”.format(self.bank\_account, formatdate(self.date)).

**Local steps**

- If not Platform.db.get\_value(“Bank Account”, self.bank\_account, “is\_company\_account”).
  - Call the validation error handler Platform.throw(translated “Closing balances can only be recorded for company bank accounts.”).
- If Platform.db.exists(self.doctype, mapping(“bank\_account” → self.bank\_account, “date” → self.date, “name” → list(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “A closing balance already exists for Bank Account {0} on {1}.”.format(self.bank\_account, formatdate(self.date)), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L760)

<a id="op-b85de316116855"></a>
### On doctype update

`operation_enterprise_binding_enterprise_accounts_doctype_bank_account_balance_bank_account_balance_on_doctype_update`

**Inputs** no declared parameters.

**State and service calls** request add\_unique on “Bank Account Balance”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Bank Account Balance”, list(“bank\_account”, “date”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L761)

## Record · Bank clearance

[Record definition](../../../../data/record-types/bank_clearance.json)

<a id="op-dea19254630d3e"></a>
### Bank Clearance.get payment entries

`operation_enterprise_accounts_record_definitions_bank_clearance_business_behavior_bank_clearance_get_payment_entries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set entries from self.get\_entries\_for\_account().
- Set precision from (cint(Platform.db.get\_default(“currency\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“currency\_precision”)) → 2.
- Set entries from sorted(entries, key = deferred anonymous expression).
- Evaluate self.set(“payment\_entries”, list()).
- Set default\_currency from Enterprise.get\_default\_currency().
- For each d in entries.
  - Set row from self.append(“payment\_entries”, mapping()).
  - Set amount from (flt(d.get(“debit”, 0)) − flt(d.get(“credit”, 0))).
  - If not d.get(“account\_currency”).
    - Set d.account\_currency from default\_currency.
  - Set formatted\_amount from fmt\_money(abs(amount), precision, d.account\_currency).
  - Set d.amount from ((formatted\_amount + one space) + translated “Dr” when amount &gt; 0, otherwise translated “Cr”).
    - Value choice on amount &gt; 0 — true gives translated “Dr”, false gives translated “Cr”.
  - Set d.posting\_date from getdate(d.posting\_date).
  - Evaluate d.pop(“credit”).
  - Evaluate d.pop(“debit”).
  - Evaluate d.pop(“account\_currency”).
  - Evaluate row.update(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get entries for account](operations-012.md#op-ea7637cb61eaab).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L253)

<a id="op-ea7637cb61eaab"></a>
### Bank Clearance.get entries for account

`operation_enterprise_binding_enterprise_accounts_doctype_bank_clearance_bank_clearance_bankclearance_get_entries_for_account`

**Inputs** self.

**Record and data access** resolve a document from “Account” via get\_doc.

**Explicit results** entries.

**Explicit failure paths** validation helper — translated “From Date and To Date are Mandatory” · validation helper — translated “Account is mandatory to get payment entries”.

**Local steps**

- If not (self.from\_date and self.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date.
  - Call the validation error handler Platform.throw(translated “From Date and To Date are Mandatory”).
- If not self.account.
  - Call the validation error handler Platform.throw(translated “Account is mandatory to get payment entries”).
- Evaluate Platform.get\_doc(“Account”, self.account).check\_permission(“read”).
- Set entries from list().
- For each method\_name in Platform.get\_hooks(“get\_payment\_entries\_for\_bank\_clearance”).
  - Update entries using + (Platform.get\_attr(method\_name)(self.from\_date, self.to\_date, self.account, self.bank\_account, …) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method\_name)(self.from\_date, self.to\_date, self.account, self.bank\_account, …) → list().
- Return entries.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_payment\_entries\_for\_bank\_clearance”), Platform.get\_attr(method\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L763)

<a id="op-4ff1fd5a3e0289"></a>
### Bank Clearance.update clearance date

`operation_enterprise_accounts_record_definitions_bank_clearance_business_behavior_bank_clearance_update_clearance_date`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from row.payment\_document via get\_doc · read “Sales Invoice Payment” via get\_value.

**State and service calls** request set\_value on “Sales Invoice Payment” · call db\_set on payment\_entry.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Voucher is not eligible for clearance with the selected filters.”.format(row.idx).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set available\_entries from mapping of tuple(entry.payment\_document, entry.payment\_entry) → entry for entry drawn from self.get\_entries\_for\_account().
  - Draw entry from self.get\_entries\_for\_account().
- Set entries\_to\_update from list().
- For each row in self.get(“payment\_entries”).
  - If not (row.clearance\_date or self.include\_reconciled\_entries).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.clearance\_date → self.include\_reconciled\_entries.
    - Continue with the next iteration or loop test.
  - Set entry from available\_entries.get(tuple(row.payment\_document, row.payment\_entry)).
  - If not entry.
    - Call the validation error handler Platform.throw(translated “Row {0}: Voucher is not eligible for clearance with the selected filters.”.format(row.idx), title = translated “Invalid Voucher”).
  - Set voucher from Platform.get\_doc(row.payment\_document, row.payment\_entry).
  - If not has\_clearance\_date\_changed(voucher, row.clearance\_date, self.account).
    - Continue with the next iteration or loop test.
  - If not row.clearance\_date.
    - Set row.clearance\_date from no value.
  - Evaluate validate\_clearance\_date(voucher, row.clearance\_date, self.account, row\_idx = row.idx, cheque\_date = entry.get(“cheque\_date”)).
  - Evaluate entries\_to\_update.append(row).
- If not entries\_to\_update.
  - Evaluate msgprint(translated “Clearance Date not mentioned”).
  - Return no value.
- For each d in entries\_to\_update.
  - If d.payment\_document equals “Sales Invoice”.
    - Set old\_clearance\_date from Platform.db.get\_value(“Sales Invoice Payment”, mapping(“parent” → d.payment\_entry, “account” → self.account, “amount” → list(“!=”, 0)), “clearance\_date”).
    - If (d.clearance\_date or old\_clearance\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.clearance\_date → old\_clearance\_date.
      - Evaluate Platform.db.set\_value(“Sales Invoice Payment”, mapping(“parent” → d.payment\_entry, “account” → self.get(“account”), “amount” → list(“!=”, 0)), “clearance\_date”, d.clearance\_date).
      - Set sales\_invoice from Platform.get\_lazy\_doc(“Sales Invoice”, d.payment\_entry).
      - Evaluate sales\_invoice.add\_comment(“Comment”, translated “Clearance date changed from {0} to {1} via Bank Clearance Tool”.format(old\_clearance\_date, d.clearance\_date)).
  - Otherwise.
    - Set payment\_entry from Platform.get\_lazy\_doc(d.payment\_document, d.payment\_entry).
    - Set old\_clearance\_date from payment\_entry.clearance\_date.
    - If (d.clearance\_date or old\_clearance\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.clearance\_date → old\_clearance\_date.
      - Evaluate payment\_entry.db\_set(“clearance\_date”, d.clearance\_date).
      - Evaluate payment\_entry.add\_comment(“Comment”, translated “Clearance date changed from {0} to {1} via Bank Clearance Tool”.format(old\_clearance\_date, d.clearance\_date)).
- Evaluate self.get\_payment\_entries().
- Evaluate msgprint(translated “Clearance Date updated”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get entries for account](operations-012.md#op-ea7637cb61eaab), [get payment entries](operations-012.md#op-dea19254630d3e).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L254)

<a id="op-07e2478cdade3e"></a>
### Validate clearance date

`operation_enterprise_binding_enterprise_accounts_doctype_bank_clearance_bank_clearance_validate_clearance_date`

**Inputs** voucher, clearance\_date, account, row\_idx = no value, cheque\_date = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0}: Only submitted vouchers can be cleared.”.format(label) · validation helper — translated “{0}: Clearance date cannot be before posting date.”.format(label) · validation helper — translated “{0}: Clearance date cannot be before cheque date.”.format(label) · validation helper — translated “{0}: Unreconcile the voucher from its Bank Transaction before changing the clearance date.”.format(label).

**Local steps**

- Evaluate voucher.check\_permission(“read”).
- Evaluate voucher.check\_permission(“write”).
- Set label from translated “Row {0}”.format(row\_idx) when row\_idx, otherwise formatted text {translated voucher.doctype} {voucher.name}.
  - Value choice on row\_idx — true gives translated “Row {0}”.format(row\_idx), false gives formatted text {translated voucher.doctype} {voucher.name}.
- <a id="op-07e2478cdade3e-guard-6"></a>If voucher.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “{0}: Only submitted vouchers can be cleared.”.format(label), title = translated “Invalid Voucher”).
- If not has\_clearance\_date\_changed(voucher, clearance\_date, account).
  - Return no value.
- If clearance\_date.
  - Set clearance\_date from getdate(clearance\_date).
  - If clearance\_date &lt; getdate(voucher.posting\_date).
    - Call the validation error handler Platform.throw(translated “{0}: Clearance date cannot be before posting date.”.format(label), title = translated “Invalid Clearance Date”).
  - Set cheque\_date from (cheque\_date or voucher.get(“cheque\_date”) or voucher.get(“reference\_date”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cheque\_date → voucher.get(“cheque\_date”) → voucher.get(“reference\_date”).
  - If (cheque\_date and clearance\_date &lt; getdate(cheque\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cheque\_date → clearance\_date &lt; getdate(cheque\_date).
    - Call the validation error handler Platform.throw(translated “{0}: Clearance date cannot be before cheque date.”.format(label), title = translated “Invalid Clearance Date”).
- Set transaction from Platform.qb.DocType(“Bank Transaction”).
- Set payment from Platform.qb.DocType(“Bank Transaction Payments”).
- Set allocated from nested operand in the contract(nested operand in the contract).select(transaction.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contr ….
- If (voucher.doctype equals “Sales Invoice” and account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher.doctype equals “Sales Invoice” → account.
  - Set bank\_account from Platform.qb.DocType(“Bank Account”).
  - Set allocated from allocated.where(transaction.bank\_account.isin(nested operand in the contract(nested operand in the contract).select(bank\_account.name).where(bank\_account.account equals account))).
- If allocated.run().
  - Call the validation error handler Platform.throw(translated “{0}: Unreconcile the voucher from its Bank Transaction before changing the clearance date.”.format(label), title = translated “Voucher Already Reconciled”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison voucher.docstatus differs from 1, voucher.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “{0}: Only submitted vouchers can be cleared.”.format(label). With voucher.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-07e2478cdade3e-guard-6)

**Values supplied outside this operation** effective access from voucher.check\_permission(“read”), voucher.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L765)

<a id="op-c3fd4140546c9f"></a>
### Has clearance date changed

`operation_enterprise_binding_enterprise_accounts_doctype_bank_clearance_bank_clearance_has_clearance_date_changed`

**Inputs** voucher, clearance\_date, account.

**Explicit results** any(generator of getdate(date) when date, otherwise no value differs from clearance\_date for date drawn from clearance\_dates).

**Local steps**

- Set clearance\_date from getdate(clearance\_date) when clearance\_date, otherwise no value.
  - Value choice on clearance\_date — true gives getdate(clearance\_date), false gives no value.
- Set clearance\_dates from list of payment.clearance\_date for payment drawn from voucher.payments where ((not account or payment.account equals account) and payment.amount differs from 0) when voucher.doctype equals “Sales Invoice”, ….
  - Value choice on voucher.doctype equals “Sales Invoice” — true gives list of payment.clearance\_date for payment drawn from voucher.payments where ((not account or payment.account equals account) and payment.amount differs from 0), false gives list(voucher.clearance\_date).
  - Draw payment from voucher.payments, keep a combination only if (((not account or payment.account equals account) and payment.amount differs from 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not account or payment.account equals account) → payment.amount differs from 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not account → payment.account equals account.
- Return any(generator of getdate(date) when date, otherwise no value differs from clearance\_date for date drawn from clearance\_dates).
  - Draw date from clearance\_dates.
  - Value choice on date — true gives getdate(date), false gives no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L764)

<a id="op-5c6c76f791d68e"></a>
### Get payment entries for bank clearance

`operation_enterprise_accounts_record_definitions_bank_clearance_business_behavior_get_payment_entries_for_bank_clearance`

**Inputs** from\_date, to\_date, account, bank\_account, include\_reconciled\_entries, include\_pos\_transactions.

**Explicit results** entries.

**Local steps**

- Set entries from list().
- Set journal\_entry from Platform.qb.DocType(“Journal Entry”).
- Set journal\_entry\_account from Platform.qb.DocType(“Journal Entry Account”).
- Set journal\_entry\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(ConstantColumn(“Journal Entry”).as\_(“payment\_docum ….
- If not include\_reconciled\_entries.
  - Set journal\_entry\_query from journal\_entry\_query.where((journal\_entry.clearance\_date.isnull() bitwise or journal\_entry.clearance\_date equals “0000-00-00”)).
- Set journal\_entries from nested operand in the contract(nested operand in the contract, nested operand in the contract).orderby(journal\_entry.posting\_date).orderby(journal\_entry.name, order = Order.desc).run(as\_dict = true).
- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set company from Platform.qb.DocType(“Company”).
- Set payment\_entry\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.company equals nested operand in the contract.name).select(ConstantColumn(“Payment Entry”).as\_(“payment\_docu ….
- If not include\_reconciled\_entries.
  - Set payment\_entry\_query from payment\_entry\_query.where((pe.clearance\_date.isnull() bitwise or pe.clearance\_date equals “0000-00-00”)).
- Set payment\_entries from payment\_entry\_query.orderby(pe.posting\_date).orderby(pe.name, order = Order.desc).run(as\_dict = true).
- Set acc from Platform.qb.DocType(“Account”).
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set paid\_purchase\_invoices\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.company equals nested operand in the contract.name).select(ConstantColumn(“Purchase Invoice”).as\_(“payment\_d ….
- If not include\_reconciled\_entries.
  - Set paid\_purchase\_invoices\_query from paid\_purchase\_invoices\_query.where((pi.clearance\_date.isnull() bitwise or pi.clearance\_date equals “0000-00-00”)).
- Set paid\_purchase\_invoices from paid\_purchase\_invoices\_query.orderby(pi.posting\_date).orderby(pi.name, order = Order.desc).run(as\_dict = true).
- Set pos\_sales\_invoices from list().
- If include\_pos\_transactions.
  - Set si\_payment from Platform.qb.DocType(“Sales Invoice Payment”).
  - Set si from Platform.qb.DocType(“Sales Invoice”).
  - Set pos\_sales\_invoices\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.company equals nested operand in the contract.name).select(ConstantColumn(“Sales Invoice”).as\_(“payment\_docu ….
  - If not include\_reconciled\_entries.
    - Set pos\_sales\_invoices\_query from pos\_sales\_invoices\_query.where((si\_payment.clearance\_date.isnull() bitwise or si\_payment.clearance\_date equals “0000-00-00”)).
  - Set pos\_sales\_invoices from pos\_sales\_invoices\_query.orderby(si.posting\_date).orderby(si.name, order = Order.desc).run(as\_dict = true).
- Set entries from (((list(payment\_entries) + list(journal\_entries)) + list(pos\_sales\_invoices)) + list(paid\_purchase\_invoices)).
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L255)

## Report · Bank clearance summary

<a id="op-3564e4b4ed1be5"></a>
### Execute

`operation_enterprise_accounts_report_bank_clearance_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns().
- Set data from get\_entries(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L673)

<a id="op-9019af46439da2"></a>
### Get columns

`operation_enterprise_accounts_report_bank_clearance_summary_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Payment Document Type”, “fieldname” → “payment\_document\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Payment Entry”, “fieldname”  ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L674)

<a id="op-e71a8d6706b1b8"></a>
### Get entries

`operation_enterprise_accounts_report_bank_clearance_summary_business_behavior_get_entries`

**Inputs** filters.

**Explicit results** sorted(entries, key = deferred anonymous expression).

**Local steps**

- Set entries from list().
- For each method\_name in Platform.get\_hooks(“get\_entries\_for\_bank\_clearance\_summary”).
  - Update entries using + (Platform.get\_attr(method\_name)(filters) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method\_name)(filters) → list().
- Return sorted(entries, key = deferred anonymous expression).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_entries\_for\_bank\_clearance\_summary”), Platform.get\_attr(method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0230.json#L1329) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L675)
