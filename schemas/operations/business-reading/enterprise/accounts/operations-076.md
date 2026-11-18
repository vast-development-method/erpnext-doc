# Accounting and settlement · operations 76

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Period closing voucher

[Record definition](../../../../data/record-types/period_closing_voucher.json)

<a id="op-de0c95cfbb8801"></a>
### Period Closing Voucher.before submit

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_before_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.has\_stock\_transactions().
  - Return no value.
- Evaluate self.validate\_stock\_accounts\_balance().
- Evaluate self.validate\_stock\_closing\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has stock transactions](operations-076.md#op-61991d67041949), [validate stock accounts balance](operations-076.md#op-e933d8b5548299), [validate stock closing entry](operations-076.md#op-eb223e3d3dafa8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L4929) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L419)

<a id="op-61991d67041949"></a>
### Period Closing Voucher.has stock transactions

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_has_stock_transactions`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via exists.

**Explicit results** false · bool(Platform.db.exists(“Stock Ledger Entry”, mapping(“company” → self.company, “is\_cancelled” → 0, “posting\_date” → tuple(“&lt;=”, self.period\_end\_date)))).

**Local steps**

- If not is\_perpetual\_inventory\_enabled(self.company).
  - Return false.
- Return bool(Platform.db.exists(“Stock Ledger Entry”, mapping(“company” → self.company, “is\_cancelled” → 0, “posting\_date” → tuple(“&lt;=”, self.period\_end\_date)))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L5033) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L439)

<a id="op-e933d8b5548299"></a>
### Period Closing Voucher.validate stock accounts balance

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_validate_stock_accounts_balance`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The closing balance {0} of the Stock Asset accounts does not match the closing value {1} of the Stock Balanc …”.format(Platform.bold(fmt\_money(account\_balance, currency = currency)), Platform.b ….

**Local steps**

- Set tuple(account\_balance, stock\_value, difference) from self.get\_stock\_value\_mismatch().
- If not difference.
  - Set self.stock\_value\_difference from 0.
  - Return no value.
- If self.is\_stock\_value\_difference\_accepted(stock\_value, difference).
  - Return no value.
- Set currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
- Call the validation error handler Platform.throw(translated “The closing balance {0} of the Stock Asset accounts does not match the closing value {1} of the Stock Balanc …”.format(Platform.bold(fmt\_money(account\_balance, currency = currenc ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get stock value mismatch](operations-076.md#op-e24f6da1132a25), [is stock value difference accepted](operations-076.md#op-1ba01909d20804).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L450)

<a id="op-1ba01909d20804"></a>
### Period Closing Voucher.is stock value difference accepted

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_is_stock_value_difference_accepted`

**Inputs** self, stock\_value, difference.

**Explicit results** (is\_within\_stock\_value\_tolerance(stock\_value, difference) and flt(self.stock\_value\_difference, precision) equals difference).

**Local steps**

- Set precision from Platform.get\_precision(“GL Entry”, “debit”).
- Return (is\_within\_stock\_value\_tolerance(stock\_value, difference) and flt(self.stock\_value\_difference, precision) equals difference).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_within\_stock\_value\_tolerance(stock\_value, difference) → flt(self.stock\_value\_difference, precision) equals difference.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L876)

<a id="op-e24f6da1132a25"></a>
### Period Closing Voucher.get stock value mismatch

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_get_stock_value_mismatch`

**Inputs** self.

**Explicit results** tuple(account\_balance, stock\_value, flt((account\_balance − stock\_value), precision)).

**Local steps**

- Set precision from Platform.get\_precision(“GL Entry”, “debit”).
- Set account\_balance from flt(self.get\_stock\_accounts\_balance(), precision).
- Set stock\_value from flt(get\_stock\_value\_on(posting\_date = self.period\_end\_date, company = self.company), precision).
- Return tuple(account\_balance, stock\_value, flt((account\_balance − stock\_value), precision)).

**Methods declared on this owner** [get stock accounts balance](operations-076.md#op-5580b70a39cf84).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L875)

<a id="op-fd151d1f441495"></a>
### Period Closing Voucher.get stock value difference

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_get_stock_value_difference`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping() · mapping(“account\_balance” → account\_balance, “stock\_value” → stock\_value, “difference” → difference, “tolerance” → STOCK\_VALUE\_TOLERANCE\_PERCENT, …).

**Local steps**

- If not self.has\_stock\_transactions().
  - Return mapping().
- Set tuple(account\_balance, stock\_value, difference) from self.get\_stock\_value\_mismatch().
- Return mapping(“account\_balance” → account\_balance, “stock\_value” → stock\_value, “difference” → difference, “tolerance” → STOCK\_VALUE\_TOLERANCE\_PERCENT, …).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(difference) → is\_within\_stock\_value\_tolerance(stock\_value, difference).

**Methods declared on this owner** [has stock transactions](operations-076.md#op-61991d67041949), [get stock value mismatch](operations-076.md#op-e24f6da1132a25).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L874)

<a id="op-5580b70a39cf84"></a>
### Period Closing Voucher.get stock accounts balance

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_stock_accounts_balance`

**Inputs** self.

**Explicit results** flt(balance at 0 at 0) when balance, otherwise 0.0.

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Set account from Platform.qb.DocType(“Account”).
- Set stock\_accounts from nested operand in the contract.qb.from\_(account).select(account.name).where(((account.account\_type equals “Stock” bitwise and account.company equals self.company) bitwise and account.is\_group equals 0)).
- Set balance from nested operand in the contract(nested operand in the contract).select(Sum((nested operand in the contract − nested operand in the contract))).where((((nested operand in the contract equals nested operand i ….run().
- Return flt(balance at 0 at 0) when balance, otherwise 0.0.
  - Value choice on balance — true gives flt(balance at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0112.json#L5686) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L438)

<a id="op-eb223e3d3dafa8"></a>
### Period Closing Voucher.validate stock closing entry

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_validate_stock_closing_entry`

**Inputs** self.

**Record and data access** read “Stock Closing Entry” via get\_value.

**Explicit failure paths** validation helper — translated “Create a Stock Closing Entry for the entire company with To Date as {0} before submitting the Period Closing …”.format(Platform.bold(formatdate(self.period\_end\_date))) · validation helper — translated “The Stock Closing Entry for {0} is not completed yet. Wait for it to complete before submitting the Period C …”.format(Platform.bold(formatdate(self.period\_end\_date))).

**Local steps**

- Set closing\_entry from Platform.db.get\_value(“Stock Closing Entry”, apply\_unscoped\_filters(mapping(“company” → self.company, “to\_date” → self.period\_end\_date, “docstatus” → 1)), list(“name”, “status”, “modified”), as\_dict = true).
- If not closing\_entry.
  - Call the validation error handler Platform.throw(translated “Create a Stock Closing Entry for the entire company with To Date as {0} before submitting the Period Closing …”.format(Platform.bold(formatdate(self.period\_end\_date))), title = t ….
- If closing\_entry.status equals “Outdated”.
  - Evaluate self.throw\_outdated\_stock\_closing\_entry(closing\_entry).
- If closing\_entry.status differs from “Completed”.
  - Call the validation error handler Platform.throw(translated “The Stock Closing Entry for {0} is not completed yet. Wait for it to complete before submitting the Period C …”.format(Platform.bold(formatdate(self.period\_end\_date))), title = t ….
- Evaluate self.validate\_stock\_closing\_entry\_is\_fresh(closing\_entry).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw outdated stock closing entry](operations-076.md#op-b61a4d0eade637), [validate stock closing entry is fresh](operations-076.md#op-1da99bdc177f74).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L451)

<a id="op-1da99bdc177f74"></a>
### Period Closing Voucher.validate stock closing entry is fresh

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_validate_stock_closing_entry_is_fresh`

**Inputs** self, closing\_entry.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set last\_change from nested operand in the contract(nested operand in the contract).select(Max(nested operand in the contract.modified)).where((sle.company equals self.company bitwise and sle.posting\_date ≤ self.period\_end\_date)).run().
- If (last\_change and last\_change at 0 at 0 and last\_change at 0 at 0 &gt; closing\_entry.modified).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_change → last\_change at 0 at 0 → last\_change at 0 at 0 &gt; closing\_entry.modified.
  - Evaluate self.throw\_outdated\_stock\_closing\_entry(closing\_entry).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw outdated stock closing entry](operations-076.md#op-b61a4d0eade637).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L452)

<a id="op-b61a4d0eade637"></a>
### Period Closing Voucher.throw outdated stock closing entry

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_throw_outdated_stock_closing_entry`

**Inputs** self, closing\_entry.

**Explicit failure paths** validation helper — translated “Stock transactions were created or modified after the Stock Closing Entry {0} was generated. Regenerate it b …”.format(get\_link\_to\_form(“Stock Closing Entry”, closing\_entry.name)).

**Local steps**

- Call the validation error handler Platform.throw(translated “Stock transactions were created or modified after the Stock Closing Entry {0} was generated. Regenerate it b …”.format(get\_link\_to\_form(“Stock Closing Entry”, closing\_entry.name) ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L879)

<a id="op-72852e1148f8a3"></a>
### Period Closing Voucher.on submit

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_on_submit`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value · resolve a document from mapping(“doctype” → “Process Period Closing Voucher”, “parent\_pcv” → self.name) via get\_doc.

**State and service calls** call db\_set on self · call submit on ppcv.save() · call save on ppcv.

**Local steps**

- Evaluate self.db\_set(“gle\_processing\_status”, “In Progress”).
- If Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_controller\_for\_pcv”).
  - Evaluate self.make\_gl\_entries().
- Otherwise.
  - Set ppcv from Platform.get\_doc(mapping(“doctype” → “Process Period Closing Voucher”, “parent\_pcv” → self.name)).
  - Evaluate ppcv.save().submit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [make gl entries](operations-076.md#op-62fc9d3cfd0ac6).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_controller\_for\_pcv”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L443)

<a id="op-0a2a7be5260072"></a>
### Period Closing Voucher.on cancel

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_on_cancel`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Payment Ledger Entry”, “Account Closing Balance”, …).
- Evaluate self.block\_if\_future\_closing\_voucher\_exists().
- Evaluate self.validate\_accounts\_not\_frozen().
- If not Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_controller\_for\_pcv”).
  - Evaluate self.cancel\_process\_pcv\_docs().
- Evaluate self.db\_set(“gle\_processing\_status”, “In Progress”).
- Evaluate self.cancel\_gl\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [block if future closing voucher exists](operations-075.md#op-71a42a9e4d5e37), [validate accounts not frozen](operations-075.md#op-03ce049e2176ce), [cancel process pcv docs](operations-076.md#op-bd669b8865d895), [cancel gl entries](operations-077.md#op-46eea333fd1d4e).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_controller\_for\_pcv”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L442)

<a id="op-bd669b8865d895"></a>
### Period Closing Voucher.cancel process pcv docs

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_cancel_process_period_closing_voucher_records`

**Inputs** self.

**Record and data access** read “Process Period Closing Voucher” via get\_all · resolve a document from “Process Period Closing Voucher” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Process Period Closing Voucher”, x.name).

**Local steps**

- Set ppcvs from Platform.db.get\_all(“Process Period Closing Voucher”, mapping(“parent\_pcv” → self.name, “docstatus” → 1)).
- For each x in ppcvs.
  - Evaluate Platform.get\_doc(“Process Period Closing Voucher”, x.name).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L1110) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L422)

<a id="op-01bde618b09315"></a>
### Period Closing Voucher.on trash

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_on_trash`

**Inputs** self.

**Record and data access** read “Process Period Closing Voucher” via get\_all.

**State and service calls** request delete\_doc for “Process Period Closing Voucher”.

**Local steps**

- Evaluate super().on\_trash().
- Set ppcvs from Platform.db.get\_all(“Process Period Closing Voucher”, mapping(“parent\_pcv” → self.name, “docstatus” → list(“in”, list(1, 2)))).
- For each x in ppcvs.
  - Evaluate Platform.delete\_doc(“Process Period Closing Voucher”, x.name, force = true, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L444)

<a id="op-62fc9d3cfd0ac6"></a>
### Period Closing Voucher.make gl entries

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_make_general_ledger_entries`

**Inputs** self.

**State and service calls** enqueue with process\_gl\_and\_closing\_entries · msgprint with translated “The GL Entries and closing balances will be processed in the background, it can take a few minutes.”.

**Local steps**

- If Platform.db.estimate\_count(“GL Entry”) &gt; 100000.
  - Evaluate Platform.enqueue(process\_gl\_and\_closing\_entries, doc = self, timeout = 1800).
  - Evaluate Platform.msgprint(translated “The GL Entries and closing balances will be processed in the background, it can take a few minutes.”, alert = true).
- Otherwise.
  - Evaluate self.post\_closing\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [post closing entries](operations-076.md#op-2f4e5efe420115).

**Values supplied outside this operation** service or queued work from Platform.enqueue(process\_gl\_and\_closing\_entries, doc = self, timeout = 1800).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L441)

<a id="op-2f4e5efe420115"></a>
### Period Closing Voucher.post closing entries

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_post_closing_entries`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies make\_gl\_entries.
- Set gl\_entries from self.get\_pcv\_gl\_entries().
- If gl\_entries.
  - Evaluate make\_gl\_entries(gl\_entries, merge\_entries = false).
- Set closing\_entries from self.get\_account\_closing\_balances().
- Evaluate make\_closing\_entries(closing\_entries, self.name, self.company, self.period\_end\_date).
- Evaluate self.db\_set(“gle\_processing\_status”, “Completed”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get pcv gl entries](operations-076.md#op-ef8a8671dd229b), [get account closing balances](operations-077.md#op-c481c59ecd2bfa).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L877)

<a id="op-ef77d225b52528"></a>
### Period Closing Voucher.reverse closing entries

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_periodclosingvoucher_reverse_closing_entries`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies make\_reverse\_gl\_entries.
- Evaluate make\_reverse\_gl\_entries(voucher\_type = self.doctype, voucher\_no = self.name, posting\_date = self.period\_end\_date).
- Evaluate delete\_closing\_entries(self.name).
- Evaluate self.db\_set(“gle\_processing\_status”, “Completed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L878)

<a id="op-ef8a8671dd229b"></a>
### Period Closing Voucher.get pcv gl entries

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_period_closing_voucher_general_ledger_entries`

**Inputs** self.

**Explicit results** (self.pl\_accounts\_reverse\_gle + self.closing\_account\_gle).

**Local steps**

- Set self.pl\_accounts\_reverse\_gle from list().
- Set self.closing\_account\_gle from list().
- Set pl\_account\_balances from self.get\_account\_balances\_based\_on\_dimensions(report\_type = “Profit and Loss”).
- For each tuple(dimensions, account\_balances) in pl\_account\_balances.items().
  - Set pl\_entries from list of self.get\_gle\_for\_pl\_account(acc, balances, dimensions) for tuple(acc, balances) drawn from account\_balances.items() where (acc differs from “balances” and has\_balance(balances)).
    - Draw tuple(acc, balances) from account\_balances.items(), keep a combination only if ((acc differs from “balances” and has\_balance(balances))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in acc differs from “balances” → has\_balance(balances).
  - If not pl\_entries.
    - Continue with the next iteration or loop test.
  - Evaluate self.pl\_accounts\_reverse\_gle.extend(pl\_entries).
  - Evaluate self.closing\_account\_gle.append(self.get\_gle\_for\_closing\_account(account\_balances at “balances”, dimensions)).
- Return (self.pl\_accounts\_reverse\_gle + self.closing\_account\_gle).

**Methods declared on this owner** [get account balances based on dimensions](operations-076.md#op-be90808fe28296), [get gle for pl account](operations-076.md#op-df720d6e469287), [get gle for closing account](operations-076.md#op-6017028f101fa5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L437)

<a id="op-df720d6e469287"></a>
### Period Closing Voucher.get gle for pl account

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_general_ledger_entry_for_profit_and_loss_account`

**Inputs** self, acc, balances, dimensions.

**Explicit results** gl\_entry.

**Local steps**

- Set balance\_in\_account\_currency from (flt(balances.debit\_in\_account\_currency) − flt(balances.credit\_in\_account\_currency)).
- Set balance\_in\_company\_currency from (flt(balances.debit) − flt(balances.credit)).
- Set gl\_entry from Platform.\_dict(mapping(“company” → self.company, “posting\_date” → self.period\_end\_date, “account” → acc, “account\_currency” → balances.account\_currency, …)).
  - Value choice on balance\_in\_account\_currency &lt; 0 — true gives abs(balance\_in\_account\_currency), false gives 0.
  - Value choice on balance\_in\_company\_currency &lt; 0 — true gives abs(balance\_in\_company\_currency), false gives 0.
  - Value choice on balance\_in\_account\_currency &gt; 0 — true gives abs(balance\_in\_account\_currency), false gives 0.
  - Value choice on balance\_in\_company\_currency &gt; 0 — true gives abs(balance\_in\_company\_currency), false gives 0.
- Evaluate self.update\_default\_dimensions(gl\_entry, dimensions).
- Return gl\_entry.

**Methods declared on this owner** [update default dimensions](operations-076.md#op-27597048fc42f0).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L2197) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L435)

<a id="op-6017028f101fa5"></a>
### Period Closing Voucher.get gle for closing account

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_general_ledger_entry_for_closing_account`

**Inputs** self, dimension\_balance, dimensions.

**Record and data access** read “Account” via get\_value.

**Explicit results** gl\_entry.

**Local steps**

- Set balance\_in\_company\_currency from flt(dimension\_balance.balance\_in\_company\_currency).
- Set debit from balance\_in\_company\_currency when balance\_in\_company\_currency &gt; 0, otherwise 0.
  - Value choice on balance\_in\_company\_currency &gt; 0 — true gives balance\_in\_company\_currency, false gives 0.
- Set credit from abs(balance\_in\_company\_currency) when balance\_in\_company\_currency &lt; 0, otherwise 0.
  - Value choice on balance\_in\_company\_currency &lt; 0 — true gives abs(balance\_in\_company\_currency), false gives 0.
- Set gl\_entry from Platform.\_dict(mapping(“company” → self.company, “posting\_date” → self.period\_end\_date, “account” → self.closing\_account\_head, “account\_currency” → Platform.db.get\_value(“Account”, self.closing\_account\_hea ….
- Evaluate self.update\_default\_dimensions(gl\_entry, dimensions).
- Return gl\_entry.

**Methods declared on this owner** [update default dimensions](operations-076.md#op-27597048fc42f0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L2811) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L434)

<a id="op-27597048fc42f0"></a>
### Period Closing Voucher.update default dimensions

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_update_default_dimensions`

**Inputs** self, gl\_entry, dimensions.

**Local steps**

- For each tuple(i, dimension) in enumerate(self.accounting\_dimension\_fields).
  - Set gl\_entry at dimension from dimensions at i.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L3333) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L446)

<a id="op-be90808fe28296"></a>
### Period Closing Voucher.get account balances based on dimensions

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_account_balances_based_on_dimensions`

**Inputs** self, report\_type.

**Explicit results** acc\_bal\_dict.

**Local steps**

- Evaluate self.get\_accounting\_dimension\_fields().
- Set acc\_bal\_dict from Platform.\_dict().
- Set gl\_entries from list().
- Within Platform.db.unbuffered\_cursor().
  - Set gl\_entries from self.get\_gl\_entries\_for\_current\_period(report\_type, as\_iterator = true).
  - For each gle in gl\_entries.
    - Set acc\_bal\_dict from self.set\_account\_balance\_dict(gle, acc\_bal\_dict).
- If (report\_type equals “Balance Sheet” and self.is\_first\_period\_closing\_voucher()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_type equals “Balance Sheet” → self.is\_first\_period\_closing\_voucher().
  - Set opening\_entries from self.get\_gl\_entries\_for\_current\_period(report\_type, only\_opening\_entries = true).
  - For each gle in opening\_entries.
    - Set acc\_bal\_dict from self.set\_account\_balance\_dict(gle, acc\_bal\_dict).
- Return acc\_bal\_dict.

**Methods declared on this owner** [get accounting dimension fields](operations-076.md#op-31e8ef02482b01), [get gl entries for current period](operations-076.md#op-99218147d59b9a), [set account balance dict](operations-077.md#op-446c624cdd87af), [is first period closing voucher](operations-077.md#op-4687483d08cd9a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L3445) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L424)

<a id="op-31e8ef02482b01"></a>
### Period Closing Voucher.get accounting dimension fields

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_accounting_dimension_fields`

**Inputs** self.

**Local steps**

- Set default\_dimensions from list(“cost\_center”, “finance\_book”, “project”).
- Set self.accounting\_dimension\_fields from (default\_dimensions + get\_accounting\_dimensions()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L3807) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L426)

<a id="op-99218147d59b9a"></a>
### Period Closing Voucher.get gl entries for current period

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_general_ledger_entries_for_current_period`

**Inputs** self, report\_type, only\_opening\_entries = false, as\_iterator = false.

**Record and data access** execute query text (SELECT, GL Entry, Account).format(“, ”.join(self.accounting\_dimension\_fields), date\_condition).

**Explicit results** Platform.db.sql(query text (SELECT, GL Entry, Account).format(“, ”.join(self.accounting\_dimension\_fields), date\_condition), tuple(self.company, report\_type), as\_dict = 1, as\_iterator = as\_iterator).

**Local steps**

- Set date\_condition from empty text.
- If only\_opening\_entries.
  - Set date\_condition from “is\_opening = 'Yes'”.
- Otherwise.
  - Set date\_condition from formatted text posting\_date BETWEEN '{self.period\_start\_date}' AND '{self.period\_end\_date}' and is\_opening = 'No'.
- Return Platform.db.sql(query text (SELECT, GL Entry, Account).format(“, ”.join(self.accounting\_dimension\_fields), date\_condition), tuple(self.company, report\_type), as\_dict = 1, as\_iterator = as\_iterator).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L432)
