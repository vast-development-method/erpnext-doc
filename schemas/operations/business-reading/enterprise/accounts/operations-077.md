# Accounting and settlement · operations 77

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Period closing voucher

[Record definition](../../../../data/record-types/period_closing_voucher.json)

<a id="op-446c624cdd87af"></a>
### Period Closing Voucher.set account balance dict

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_set_account_balance_mapping`

**Inputs** self, gle, acc\_bal\_dict.

**Explicit results** acc\_bal\_dict.

**Local steps**

- Set key from self.get\_key(gle).
- Evaluate acc\_bal\_dict.setdefault(key, Platform.\_dict()).setdefault(gle.account, Platform.\_dict(mapping(“debit\_in\_account\_currency” → 0, “credit\_in\_account\_currency” → 0, “debit” → 0, “credit” → 0, …))).
- Update acc\_bal\_dict at key at gle.account.debit\_in\_account\_currency using + flt(gle.debit\_in\_account\_currency).
- Update acc\_bal\_dict at key at gle.account.credit\_in\_account\_currency using + flt(gle.credit\_in\_account\_currency).
- Update acc\_bal\_dict at key at gle.account.debit using + flt(gle.debit).
- Update acc\_bal\_dict at key at gle.account.credit using + flt(gle.credit).
- Evaluate acc\_bal\_dict at key.setdefault(“balances”, Platform.\_dict(mapping(“balance\_in\_account\_currency” → 0, “balance\_in\_company\_currency” → 0))).
- Set balance\_in\_account\_currency from (flt(gle.debit\_in\_account\_currency) − flt(gle.credit\_in\_account\_currency)).
- Set balance\_in\_company\_currency from (flt(gle.debit) − flt(gle.credit)).
- Update acc\_bal\_dict at key at “balances”.balance\_in\_account\_currency using + balance\_in\_account\_currency.
- Update acc\_bal\_dict at key at “balances”.balance\_in\_company\_currency using + balance\_in\_company\_currency.
- Return acc\_bal\_dict.

**Methods declared on this owner** [get key](operations-077.md#op-67356d2263192e).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L4586) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L445)

<a id="op-67356d2263192e"></a>
### Period Closing Voucher.get key

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_key`

**Inputs** self, gle.

**Explicit results** tuple(list of gle.get(dimension) for dimension drawn from self.accounting\_dimension\_fields).

**Local steps**

- Return tuple(list of gle.get(dimension) for dimension drawn from self.accounting\_dimension\_fields).
  - Draw dimension from self.accounting\_dimension\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L5282) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L436)

<a id="op-c481c59ecd2bfa"></a>
### Period Closing Voucher.get account closing balances

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_account_closing_balances`

**Inputs** self.

**Explicit results** closing\_entries.

**Local steps**

- Set pl\_closing\_entries from self.get\_closing\_entries\_for\_pl\_accounts().
- Set bs\_closing\_entries from self.get\_closing\_entries\_for\_balance\_sheet\_accounts().
- Set closing\_entries\_for\_closing\_account from self.get\_closing\_entries\_for\_closing\_account().
- Set closing\_entries from ((pl\_closing\_entries + bs\_closing\_entries) + closing\_entries\_for\_closing\_account).
- Return closing\_entries.

**Methods declared on this owner** [get closing entries for pl accounts](operations-077.md#op-b58cbc84f5acb8), [get closing entries for balance sheet accounts](operations-077.md#op-8f91b7f96ee4dc), [get closing entries for closing account](operations-077.md#op-600b2fe537eb84).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L5377) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L425)

<a id="op-b58cbc84f5acb8"></a>
### Period Closing Voucher.get closing entries for pl accounts

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_closing_entries_for_profit_and_loss_accounts`

**Inputs** self.

**Explicit results** closing\_entries.

**Local steps**

- Set closing\_entries from copy.deepcopy(self.pl\_accounts\_reverse\_gle).
- For each d in self.pl\_accounts\_reverse\_gle.
  - Set gle\_copy from copy.deepcopy(d).
  - Set gle\_copy.debit from d.credit.
  - Set gle\_copy.credit from d.debit.
  - Set gle\_copy.debit\_in\_account\_currency from d.credit\_in\_account\_currency.
  - Set gle\_copy.credit\_in\_account\_currency from d.debit\_in\_account\_currency.
  - Set gle\_copy.is\_period\_closing\_voucher\_entry from 0.
  - Set gle\_copy.period\_closing\_voucher from self.name.
  - Evaluate closing\_entries.append(gle\_copy).
- Return closing\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L5522) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L429)

<a id="op-8f91b7f96ee4dc"></a>
### Period Closing Voucher.get closing entries for balance sheet accounts

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_closing_entries_for_balance_sheet_accounts`

**Inputs** self.

**Explicit results** closing\_entries.

**Local steps**

- Set closing\_entries from list().
- Set balance\_sheet\_account\_balances from self.get\_account\_balances\_based\_on\_dimensions(report\_type = “Balance Sheet”).
- For each tuple(dimensions, account\_balances) in balance\_sheet\_account\_balances.items().
  - For each tuple(acc, balances) in account\_balances.items().
    - Set balance\_in\_company\_currency from (flt(balances.debit) − flt(balances.credit)).
    - If (acc differs from “balances” and balance\_in\_company\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in acc differs from “balances” → balance\_in\_company\_currency.
      - Evaluate closing\_entries.append(self.get\_closing\_entry(acc, balances, dimensions)).
- Return closing\_entries.

**Methods declared on this owner** [get account balances based on dimensions](operations-076.md#op-be90808fe28296), [get closing entry](operations-077.md#op-67b85dd8ff0036).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L5787) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L427)

<a id="op-67b85dd8ff0036"></a>
### Period Closing Voucher.get closing entry

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_closing_entry`

**Inputs** self, account, balances, dimensions.

**Explicit results** closing\_entry.

**Local steps**

- Set closing\_entry from Platform.\_dict(mapping(“company” → self.company, “closing\_date” → self.period\_end\_date, “period\_closing\_voucher” → self.name, “account” → account, …)).
- Evaluate self.update\_default\_dimensions(closing\_entry, dimensions).
- Return closing\_entry.

**Methods declared on this owner** [update default dimensions](operations-076.md#op-27597048fc42f0).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L6084) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L430)

<a id="op-600b2fe537eb84"></a>
### Period Closing Voucher.get closing entries for closing account

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_closing_entries_for_closing_account`

**Inputs** self.

**Explicit results** closing\_entries.

**Local steps**

- Set closing\_entries from copy.deepcopy(self.closing\_account\_gle).
- For each d in closing\_entries.
  - Set d.period\_closing\_voucher from self.name.
- Return closing\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L6442) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L428)

<a id="op-4687483d08cd9a"></a>
### Period Closing Voucher.is first period closing voucher

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_is_first_period_closing_voucher`

**Inputs** self.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit results** true.

**Local steps**

- Set first\_pcv from Platform.db.get\_value(“Period Closing Voucher”, mapping(“company” → self.company, “docstatus” → 1), “name”, order\_by = “period\_end\_date asc”).
- If (not first\_pcv or first\_pcv equals self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not first\_pcv → first\_pcv equals self.name.
  - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L6551) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L440)

<a id="op-46eea333fd1d4e"></a>
### Period Closing Voucher.cancel gl entries

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_cancel_general_ledger_entries`

**Inputs** self.

**State and service calls** enqueue with process\_cancellation · msgprint with translated “The GL Entries will be cancelled in the background, it can take a few minutes.”.

**Local steps**

- If self.get\_gle\_count\_against\_current\_pcv() &gt; 5000.
  - Evaluate Platform.enqueue(process\_cancellation, voucher\_type = “Period Closing Voucher”, voucher\_no = self.name, queue = “long”, enqueue\_after\_commit = true).
  - Evaluate Platform.msgprint(translated “The GL Entries will be cancelled in the background, it can take a few minutes.”, alert = true).
- Otherwise.
  - Evaluate self.reverse\_closing\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gle count against current pcv](operations-077.md#op-20109f637eef6a), [reverse closing entries](operations-076.md#op-ef77d225b52528).

**Values supplied outside this operation** service or queued work from Platform.enqueue(process\_cancellation, voucher\_type = “Period Closing Voucher”, voucher\_no = self.name, queue = “long”, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L421)

<a id="op-20109f637eef6a"></a>
### Period Closing Voucher.get gle count against current pcv

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_period_closing_voucher_get_general_ledger_entry_count_against_current_period_closing_voucher`

**Inputs** self.

**Record and data access** read “GL Entry” via count.

**Explicit results** Platform.db.count(“GL Entry”, mapping(“voucher\_type” → “Period Closing Voucher”, “voucher\_no” → self.name, “is\_cancelled” → 0)).

**Local steps**

- Return Platform.db.count(“GL Entry”, mapping(“voucher\_type” → “Period Closing Voucher”, “voucher\_no” → self.name, “is\_cancelled” → 0)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0113.json#L6966) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L433)

<a id="op-c85039c6d96b46"></a>
### Process gl and closing entries

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_process_general_ledger_and_closing_entries`

**Inputs** doc.

**Local steps**

- Evaluate run\_and\_record\_failure(doc.name, translated “Period Closing Voucher {0} GL Entry Processing Failed”.format(doc.name), doc.post\_closing\_entries).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L454)

<a id="op-821c88bfe8ffe1"></a>
### Process cancellation

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_process_cancellation`

**Inputs** voucher\_type, voucher\_no.

**Record and data access** resolve a document from voucher\_type via get\_doc.

**Local steps**

- Evaluate run\_and\_record\_failure(voucher\_no, translated “Period Closing Voucher {0} GL Entry Cancellation Failed”.format(voucher\_no), Platform.get\_doc(voucher\_type, voucher\_no).reverse\_closing\_entries).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L453)

<a id="op-fe1bee3331464b"></a>
### Run and record failure

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_run_and_record_failure`

**Inputs** pcv\_name, title, method, remaining positional values args.

**State and service calls** savepoint “period\_closing” · rollback · request set\_value on “Period Closing Voucher”.

**Local steps**

- Evaluate Platform.db.savepoint(“period\_closing”).
- Attempt the following.
  - Evaluate method(expanded args).
- On failure (Exception) bound to e.
  - Evaluate Platform.db.rollback(save\_point = “period\_closing”).
  - Evaluate Platform.log\_error(title = title).
  - Evaluate Platform.db.set\_value(“Period Closing Voucher”, pcv\_name, mapping(“error\_message” → str(e), “gle\_processing\_status” → “Failed”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L880)

<a id="op-15a00c2769fef9"></a>
### Delete closing entries

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_delete_closing_entries`

**Inputs** voucher\_no.

**Local steps**

- Set closing\_balance from Platform.qb.DocType(“Account Closing Balance”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(closing\_balance.period\_closing\_voucher equals voucher\_no).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0114.json#L3092) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L416)

<a id="op-2ec727ecaffda9"></a>
### Get period start end date

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_get_period_start_end_date`

**Inputs** fiscal\_year, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “Period Closing Voucher”, “company” → company, “fiscal\_year” → fiscal\_year) via get\_doc · read “Fiscal Year” via get\_value.

**Explicit results** tuple(period\_start\_date, fy\_end\_date).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Period Closing Voucher”, “company” → company, “fiscal\_year” → fiscal\_year)).check\_permission(“read”).
- Set tuple(fy\_start\_date, fy\_end\_date) from Platform.db.get\_value(“Fiscal Year”, fiscal\_year, list(“year\_start\_date”, “year\_end\_date”)).
- Set prev\_closed\_period\_end\_date from get\_previous\_closed\_period\_in\_current\_year(fiscal\_year, company).
- Set period\_start\_date from add\_days(prev\_closed\_period\_end\_date, 1) when prev\_closed\_period\_end\_date, otherwise fy\_start\_date.
  - Value choice on prev\_closed\_period\_end\_date — true gives add\_days(prev\_closed\_period\_end\_date, 1), false gives fy\_start\_date.
- Return tuple(period\_start\_date, fy\_end\_date).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L417)

<a id="op-a7457456136006"></a>
### Get previous closed period in current year

`operation_enterprise_accounts_record_definitions_period_closing_voucher_business_behavior_get_previous_closed_period_in_current_year`

**Inputs** fiscal\_year, company.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit results** prev\_closed\_period\_end\_date.

**Local steps**

- Set prev\_closed\_period\_end\_date from Platform.db.get\_value(“Period Closing Voucher”, filters = mapping(“company” → company, “fiscal\_year” → fiscal\_year, “docstatus” → 1), fieldname = list(“period\_end\_date”), order\_by = “period\_end\_date desc”).
- Return prev\_closed\_period\_end\_date.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0114.json#L3472) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L418)

<a id="op-04e57b3897882f"></a>
### Has balance

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_has_balance`

**Inputs** balances.

**Explicit results** bool(((flt(balances.debit) − flt(balances.credit)) or (flt(balances.debit\_in\_account\_currency) − flt(balances.credit\_in\_account\_currency)))).

**Local steps**

- Return bool(((flt(balances.debit) − flt(balances.credit)) or (flt(balances.debit\_in\_account\_currency) − flt(balances.credit\_in\_account\_currency)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (flt(balances.debit) − flt(balances.credit)) → (flt(balances.debit\_in\_account\_currency) − flt(balances.credit\_in\_account\_currency)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L868)

<a id="op-217a74d66cb527"></a>
### Is within stock value tolerance

`operation_enterprise_binding_enterprise_accounts_doctype_period_closing_voucher_period_closing_voucher_is_within_stock_value_tolerance`

**Inputs** stock\_value, difference.

**Explicit results** abs(difference) ≤ ((abs(stock\_value) × STOCK\_VALUE\_TOLERANCE\_PERCENT) ÷ 100).

**Local steps**

- Return abs(difference) ≤ ((abs(stock\_value) × STOCK\_VALUE\_TOLERANCE\_PERCENT) ÷ 100).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L869)

## Record · Pos closing entry

<a id="op-0547ceede392c3"></a>
### POSClosing Entry.validate

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_posting\_date\_and\_time().
- Evaluate self.fetch\_invoice\_type().
- Evaluate self.validate\_pos\_opening\_entry().
- Evaluate self.validate\_invoice\_mode().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set posting date and time](operations-077.md#op-d411815850b7d7), [fetch invoice type](operations-077.md#op-eb62a95e240fb2), [validate pos opening entry](operations-077.md#op-4cc373e49a1750), [validate invoice mode](operations-077.md#op-30bf6a3145f3dc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L1475) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L488)

<a id="op-d411815850b7d7"></a>
### POSClosing Entry.set posting date and time

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_set_posting_date_and_time`

**Inputs** self.

**Local steps**

- If not self.posting\_date.
  - Set self.posting\_date from Platform.utils.nowdate().
- If self.posting\_time belongs to tuple(no value, empty text).
  - Set self.posting\_time from Platform.utils.nowtime().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L485)

<a id="op-eb62a95e240fb2"></a>
### POSClosing Entry.fetch invoice type

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_fetch_invoice_type`

**Inputs** self.

**Record and data access** read “POS Settings” via get\_single\_value.

**Local steps**

- Set self.invoice\_type from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L1713) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L481)

<a id="op-4cc373e49a1750"></a>
### POSClosing Entry.validate pos opening entry

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate_point_of_sale_opening_entry`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via get\_value.

**Explicit failure paths** validation helper — translated “Selected POS Opening Entry should be open.”.

**Local steps**

- If Platform.db.get\_value(“POS Opening Entry”, self.pos\_opening\_entry, “status”) differs from “Open”.
  - Call the validation error handler Platform.throw(translated “Selected POS Opening Entry should be open.”, title = translated “Invalid Opening Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L1795) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L493)

<a id="op-30bf6a3145f3dc"></a>
### POSClosing Entry.validate invoice mode

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate_invoice_mode`

**Inputs** self.

**Explicit failure paths** validation helper — translated “POS Invoices can't be added when Sales Invoice is enabled”.

**Local steps**

- If self.invoice\_type equals “POS Invoice”.
  - Evaluate self.validate\_duplicate\_pos\_invoices().
  - Evaluate self.validate\_pos\_invoices().
- If self.invoice\_type equals “Sales Invoice”.
  - <a id="op-30bf6a3145f3dc-guard-7"></a>If len(self.pos\_invoices) differs from 0.
    - Call the validation error handler Platform.throw(translated “POS Invoices can't be added when Sales Invoice is enabled”).
- Evaluate self.validate\_duplicate\_sales\_invoices().
- Evaluate self.validate\_sales\_invoices().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(self.pos\_invoices) differs from 0, length of self.pos\_invoices = 1 selects the branch that calls the validation-error handler with translated “POS Invoices can't be added when Sales Invoice is enabled”. With length of self.pos\_invoices = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-30bf6a3145f3dc-guard-7)

**Methods declared on this owner** [validate duplicate pos invoices](operations-077.md#op-420f4cd9c707c9), [validate pos invoices](operations-078.md#op-10e05fe5a8fb4e), [validate duplicate sales invoices](operations-078.md#op-3c32bbc55e1252), [validate sales invoices](operations-078.md#op-51e4db44510cd9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L1954) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L491)

<a id="op-420f4cd9c707c9"></a>
### POSClosing Entry.validate duplicate pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate_duplicate_point_of_sale_invoices`

**Inputs** self.

**Explicit failure paths** validation helper — error\_list.

**Local steps**

- Set pos\_occurences from mapping().
- For each tuple(idx, inv) in enumerate(self.pos\_invoices, 1).
  - Evaluate pos\_occurences.setdefault(inv.pos\_invoice, list()).append(idx).
- Set error\_list from list().
- For each tuple(key, value) in pos\_occurences.items().
  - If len(value) &gt; 1.
    - Evaluate error\_list.append(translated “{0} is added multiple times on rows: {1}”.format(Platform.bold(key), Platform.bold(value))).
- If error\_list.
  - Call the validation error handler Platform.throw(error\_list, title = translated “Duplicate POS Invoices found”, as\_list = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L2205) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L489)
