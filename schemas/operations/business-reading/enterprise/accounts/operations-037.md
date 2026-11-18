# Accounting and settlement · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Exchange rate revaluation

[Record definition](../../../../data/record-types/exchange_rate_revaluation.json)

<a id="op-e6b8365553bb04"></a>
### Exchange Rate Revaluation.make jv for zero balance

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_make_journal_voucher_for_zero_balance`

**Inputs** self.

**State and service calls** request new\_doc for “Journal Entry” · call save on journal\_entry.

**Explicit results** no value · journal\_entry.

**Local steps**

- <a id="op-e6b8365553bb04-guard-2"></a>If self.gain\_loss\_booked equals 0.
  - Return no value.
- Set accounts from list of x for x drawn from self.accounts where x.zero\_balance.
  - Draw x from self.accounts, keep a combination only if (x.zero\_balance).
- If not accounts.
  - Return no value.
- Set unrealized\_exchange\_gain\_loss\_account from self.get\_for\_unrealized\_gain\_loss\_account().
- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.voucher\_type from “Exchange Gain Or Loss”.
- Set journal\_entry.company from self.company.
- Set journal\_entry.posting\_date from self.posting\_date.
- Set journal\_entry.multi\_currency from 1.
- Set journal\_entry\_accounts from list().
- For each d in accounts.
  - Set journal\_account from Platform.\_dict(mapping(“account” → d.get(“account”), “party\_type” → d.get(“party\_type”), “party” → d.get(“party”), “account\_currency” → d.get(“account\_currency”), …)).
  - If (d.get(“balance\_in\_account\_currency”) and not d.get(“new\_balance\_in\_account\_currency”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“balance\_in\_account\_currency”) → not d.get(“new\_balance\_in\_account\_currency”).
    - Set dr\_or\_cr from “credit\_in\_account\_currency” when d.get(“balance\_in\_account\_currency”) &gt; 0, otherwise “debit\_in\_account\_currency”.
      - Value choice on d.get(“balance\_in\_account\_currency”) &gt; 0 — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
    - Set reverse\_dr\_or\_cr from “debit\_in\_account\_currency” when dr\_or\_cr equals “credit\_in\_account\_currency”, otherwise “credit\_in\_account\_currency”.
      - Value choice on dr\_or\_cr equals “credit\_in\_account\_currency” — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
    - Evaluate journal\_account.update(mapping(dr\_or\_cr → flt(abs(d.get(“balance\_in\_account\_currency”)), d.precision(“balance\_in\_account\_currency”)), reverse\_dr\_or\_cr → 0, “debit” → 0, “credit” → 0)).
    - Evaluate journal\_entry\_accounts.append(journal\_account).
    - Evaluate journal\_entry\_accounts.append(mapping(“account” → unrealized\_exchange\_gain\_loss\_account, “balance” → get\_balance\_on(unrealized\_exchange\_gain\_loss\_account), “debit” → 0, “credit” → 0, …)).
      - Value choice on d.gain\_loss &lt; 0 — true gives abs(d.gain\_loss), false gives 0.
      - Value choice on d.gain\_loss &gt; 0 — true gives abs(d.gain\_loss), false gives 0.
  - Otherwise.
    - If (d.get(“balance\_in\_base\_currency”) and not d.get(“new\_balance\_in\_base\_currency”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“balance\_in\_base\_currency”) → not d.get(“new\_balance\_in\_base\_currency”).
      - Set dr\_or\_cr from “credit” when d.get(“balance\_in\_base\_currency”) &gt; 0, otherwise “debit”.
        - Value choice on d.get(“balance\_in\_base\_currency”) &gt; 0 — true gives “credit”, false gives “debit”.
      - Set reverse\_dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
        - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
      - Evaluate journal\_account.update(mapping(dr\_or\_cr → flt(abs(d.get(“balance\_in\_base\_currency”)), d.precision(“balance\_in\_base\_currency”)), reverse\_dr\_or\_cr → 0, “debit\_in\_account\_currency” → 0, “credit\_in\_account\_cur ….
      - Evaluate journal\_entry\_accounts.append(journal\_account).
      - Evaluate journal\_entry\_accounts.append(mapping(“account” → unrealized\_exchange\_gain\_loss\_account, “balance” → get\_balance\_on(unrealized\_exchange\_gain\_loss\_account), “debit” → abs(d.gain\_loss) when d.gain\_loss &lt; 0,  ….
        - Value choice on d.gain\_loss &lt; 0 — true gives abs(d.gain\_loss), false gives 0.
        - Value choice on d.gain\_loss &gt; 0 — true gives abs(d.gain\_loss), false gives 0.
- Evaluate journal\_entry.set(“accounts”, journal\_entry\_accounts).
- Evaluate journal\_entry.set\_total\_debit\_credit().
- Evaluate journal\_entry.save().
- Return journal\_entry.

**Derived branch illustrations**

- At the comparison self.gain\_loss\_booked equals 0, self.gain\_loss\_booked = 0 selects the branch that returns no value. With self.gain\_loss\_booked = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e6b8365553bb04-guard-2)

**Methods declared on this owner** [get for unrealized gain loss account](operations-036.md#op-ef196a5da326b4).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0043.json#L3536) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L774)

<a id="op-2fe764819750c5"></a>
### Exchange Rate Revaluation.make jv for revaluation

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_make_journal_voucher_for_revaluation`

**Inputs** self.

**State and service calls** request new\_doc for “Journal Entry” · call save on journal\_entry.

**Explicit results** no value · journal\_entry.

**Local steps**

- <a id="op-2fe764819750c5-guard-2"></a>If self.gain\_loss\_unbooked equals 0.
  - Return no value.
- Set accounts from list of x for x drawn from self.accounts where not x.zero\_balance.
  - Draw x from self.accounts, keep a combination only if (not x.zero\_balance).
- If not accounts.
  - Return no value.
- Set unrealized\_exchange\_gain\_loss\_account from self.get\_for\_unrealized\_gain\_loss\_account().
- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.voucher\_type from “Exchange Rate Revaluation”.
- Set journal\_entry.company from self.company.
- Set journal\_entry.posting\_date from self.posting\_date.
- Set journal\_entry.multi\_currency from 1.
- Set journal\_entry\_accounts from list().
- For each d in accounts.
  - If not flt(d.get(“balance\_in\_account\_currency”), d.precision(“balance\_in\_account\_currency”)).
    - Continue with the next iteration or loop test.
  - Set dr\_or\_cr from “debit\_in\_account\_currency” when d.get(“balance\_in\_account\_currency”) &gt; 0, otherwise “credit\_in\_account\_currency”.
    - Value choice on d.get(“balance\_in\_account\_currency”) &gt; 0 — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
  - Set reverse\_dr\_or\_cr from “debit\_in\_account\_currency” when dr\_or\_cr equals “credit\_in\_account\_currency”, otherwise “credit\_in\_account\_currency”.
    - Value choice on dr\_or\_cr equals “credit\_in\_account\_currency” — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
  - Evaluate journal\_entry\_accounts.append(mapping(“account” → d.get(“account”), “party\_type” → d.get(“party\_type”), “party” → d.get(“party”), “account\_currency” → d.get(“account\_currency”), …)).
  - Evaluate journal\_entry\_accounts.append(mapping(“account” → d.get(“account”), “party\_type” → d.get(“party\_type”), “party” → d.get(“party”), “account\_currency” → d.get(“account\_currency”), …)).
- Evaluate journal\_entry.set(“accounts”, journal\_entry\_accounts).
- Evaluate journal\_entry.set\_amounts\_in\_company\_currency().
- Evaluate journal\_entry.set\_total\_debit\_credit().
- Update self.gain\_loss\_unbooked using + (journal\_entry.difference − self.gain\_loss\_unbooked).
- Evaluate journal\_entry.append(“accounts”, mapping(“account” → unrealized\_exchange\_gain\_loss\_account, “balance” → get\_balance\_on(unrealized\_exchange\_gain\_loss\_account), “debit\_in\_account\_currency” → abs(self.gain\_lo ….
  - Value choice on self.gain\_loss\_unbooked &lt; 0 — true gives abs(self.gain\_loss\_unbooked), false gives 0.
  - Value choice on self.gain\_loss\_unbooked &gt; 0 — true gives self.gain\_loss\_unbooked, false gives 0.
- Evaluate journal\_entry.set\_amounts\_in\_company\_currency().
- Evaluate journal\_entry.set\_total\_debit\_credit().
- Evaluate journal\_entry.save().
- Return journal\_entry.

**Derived branch illustrations**

- At the comparison self.gain\_loss\_unbooked equals 0, self.gain\_loss\_unbooked = 0 selects the branch that returns no value. With self.gain\_loss\_unbooked = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2fe764819750c5-guard-2)

**Methods declared on this owner** [get for unrealized gain loss account](operations-036.md#op-ef196a5da326b4).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0044.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L773)

<a id="op-e1fc2b6643fcba"></a>
### Exchange Rate Revaluation.make reverse journal

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_make_reverse_journal`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Journal Entry” via get\_all.

**State and service calls** call save on reversal · msgprint with translated “A draft reverse journal for {0} has been created: {1}”.format(Platform.bold(x), get\_link\_to\_form(“Journal Entry”, reversal.name)).

**Explicit failure paths** validation helper.

**Local steps**

- Evaluate Platform.has\_permission(“Journal Entry”, “write”, throw = true).
- Set je from qb.DocType(“Journal Entry”).
- Set jea from qb.DocType(“Journal Entry Account”).
- Set journals from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nes ….
- If journals.
  - Bind dependencies make\_reverse\_journal\_entry.
  - If drafts bound to Platform.db.get\_all(“Journal Entry”, filters = mapping(“docstatus” → 0, “reversal\_of” → list(“in”, journals)), pluck = “name”, as\_list = 1).
    - Set part from “journals are” when len(drafts) &gt; 1, otherwise “journal is”.
      - Value choice on len(drafts) &gt; 1 — true gives “journals are”, false gives “journal is”.
    - Set doc\_links from “, ”.join(list of “{}”.format(get\_link\_to\_form(“Journal Entry”, x)) for x drawn from drafts).
      - Draw x from drafts.
    - Call the validation error handler Platform.throw(msg = translated “Reverse {0} already available in draft status: {1}”.format(part, doc\_links)).
  - Otherwise.
    - For each x in journals.
      - Set reversal from make\_reverse\_journal\_entry(x).
      - Set reversal.posting\_date from nowdate().
      - Evaluate reversal.save().
      - Evaluate Platform.msgprint(translated “A draft reverse journal for {0} has been created: {1}”.format(Platform.bold(x), get\_link\_to\_form(“Journal Entry”, reversal.name))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Journal Entry”, “write”, throw = true) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L775)

<a id="op-5e8e62c3fc486f"></a>
### Calculate exchange rate using last gle

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_calculate_exchange_rate_using_last_general_ledger_entry`

**Inputs** company, account, party\_type, party.

**Explicit results** last\_exchange\_rate.

**Local steps**

- Set last\_exchange\_rate from no value.
- If (company and account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → account.
  - Set gl from qb.DocType(“GL Entry”).
  - Set conditions from list().
  - Evaluate conditions.append(gl.company equals company).
  - Evaluate conditions.append(gl.account equals account).
  - Evaluate conditions.append(gl.is\_cancelled equals 0).
  - Evaluate conditions.append((gl.debit &gt; 0 bitwise or gl.credit &gt; 0)).
  - Evaluate conditions.append((gl.debit\_in\_account\_currency &gt; 0 bitwise or gl.credit\_in\_account\_currency &gt; 0)).
  - If party\_type.
    - Evaluate conditions.append(gl.party\_type equals party\_type).
  - If party.
    - Evaluate conditions.append(gl.party equals party).
  - Set tuple(voucher\_type, voucher\_no) from nested operand in the contract.orderby(nested operand in the contract.posting\_date, order = nested operand in the contract.desc).limit(1).run() at 0.
  - Set last\_exchange\_rate from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(1).run() at 0 at 0.
- Return last\_exchange\_rate.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L764)

<a id="op-66d2e8b9ad148d"></a>
### Get account details

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_get_account_details`

**Inputs** company, posting\_date, account, party\_type = no value, party = no value, rounding\_loss\_allowance = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value · account\_details.

**Explicit failure paths** validation helper — translated “Company and Posting Date is mandatory” · validation helper — translated “Party Type and Party is mandatory for {0} account”.format(account\_type).

**Local steps**

- If not account.
  - Return no value.
- Evaluate Platform.has\_permission(“Account”, doc = account, throw = true).
- If not (company and posting\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → posting\_date.
  - Call the validation error handler Platform.throw(translated “Company and Posting Date is mandatory”).
- Set tuple(account\_currency, account\_type) from Platform.get\_cached\_value(“Account”, account, list(“account\_currency”, “account\_type”)).
- If (account\_type belongs to list(“Receivable”, “Payable”) and not (party\_type and party)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type belongs to list(“Receivable”, “Payable”) → not (party\_type and party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
  - Call the validation error handler Platform.throw(translated “Party Type and Party is mandatory for {0} account”.format(account\_type)).
- Set account\_details from mapping().
- Evaluate Enterprise.get\_company\_currency(company).
- Set account\_details from mapping(“account\_currency” → account\_currency).
- Set account\_balance from ExchangeRateRevaluation.get\_account\_balance\_from\_gle(company = company, posting\_date = posting\_date, account = account, party\_type = party\_type, …).
- If (account\_balance and (account\_balance at 0.balance or account\_balance at 0.balance\_in\_account\_currency)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_balance → (account\_balance at 0.balance or account\_balance at 0.balance\_in\_account\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_balance at 0.balance → account\_balance at 0.balance\_in\_account\_currency.
  - If account\_with\_new\_balance bound to ExchangeRateRevaluation.calculate\_new\_account\_balance(company, posting\_date, account\_balance).
    - Set row from account\_with\_new\_balance at 0.
    - Evaluate account\_details.update(mapping(“balance\_in\_base\_currency” → row at “balance\_in\_base\_currency”, “balance\_in\_account\_currency” → row at “balance\_in\_account\_currency”, “current\_exchange\_rate” → row at “curren ….
- Return account\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”, doc = account, throw = true) · configured or stored value from Platform.get\_cached\_value(“Account”, account, list(“account\_currency”, “account\_type”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L828) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L783)

<a id="op-c1f5aff2382878"></a>
### Get data

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_exchange_rate_revaluation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “reference\_name”, “transactions” → list(mapping(“items” → list(“Journal Entry”)))).

**Local steps**

- Return mapping(“fieldname” → “reference\_name”, “transactions” → list(mapping(“items” → list(“Journal Entry”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0044.json#L4747) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L829) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L784)

## Record · Finance book

[Record definition](../../../../data/record-types/finance_book.json)

<a id="op-051523d6d45917"></a>
### Get data

`operation_enterprise_accounts_record_definitions_finance_book_finance_book_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “finance\_book”, “non\_standard\_fieldnames” → mapping(“Asset” → “default\_finance\_book”, “Company” → “default\_finance\_book”), “transactions” → list(mapping(“label” → translated “Assets”, ….

**Local steps**

- Return mapping(“fieldname” → “finance\_book”, “non\_standard\_fieldnames” → mapping(“Asset” → “default\_finance\_book”, “Company” → “default\_finance\_book”), “transactions” → list(mapping(“label” → translated “Assets”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0045.json#L7006) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L843) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L792)

## Report · Financial ratios

<a id="op-7a3de826b8f204"></a>
### Group Ledgers.get accounts

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_groupledgers_get_accounts`

**Inputs** self, accounts.

**Declared result** set at str.

**Explicit results** ledgers · set of name for tuple(name, row) drawn from accounts.items() where (row.get(“is\_group”) and not row.get(“parent\_account”)).

**Local steps**

- Set categories from get\_account\_categories(accounts).
- Set ledgers from set of name for tuple(name, row) drawn from accounts.items() where (not row.get(“is\_group”) and self.matches(row, categories.get(name))).
  - Draw tuple(name, row) from accounts.items(), keep a combination only if ((not row.get(“is\_group”) and self.matches(row, categories.get(name)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.get(“is\_group”) → self.matches(row, categories.get(name)).
- If (not self.whole\_root\_if\_none or self.has\_category\_accounts(accounts)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.whole\_root\_if\_none → self.has\_category\_accounts(accounts).
  - Return ledgers.
- Return set of name for tuple(name, row) drawn from accounts.items() where (row.get(“is\_group”) and not row.get(“parent\_account”)).
  - Draw tuple(name, row) from accounts.items(), keep a combination only if ((row.get(“is\_group”) and not row.get(“parent\_account”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“is\_group”) → not row.get(“parent\_account”).

**Methods declared on this owner** [matches](operations-037.md#op-74683a271e220f), [has category accounts](operations-037.md#op-36a5e9ca2db27c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1203)

<a id="op-36a5e9ca2db27c"></a>
### Group Ledgers.has category accounts

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_groupledgers_has_category_accounts`

**Inputs** self, accounts.

**Declared result** bool.

**Record and data access** read “Account” via get\_cached\_value · read “Account” via exists.

**Explicit results** false · bool(Platform.db.exists(“Account”, mapping(“company” → company, “account\_category” → tuple(“in”, self.categories)))).

**Local steps**

- If not accounts.
  - Return false.
- Set company from Platform.get\_cached\_value(“Account”, next(iter(accounts)), “company”).
- Return bool(Platform.db.exists(“Account”, mapping(“company” → company, “account\_category” → tuple(“in”, self.categories)))).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, next(iter(accounts)), “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1204)

<a id="op-74683a271e220f"></a>
### Group Ledgers.matches

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_groupledgers_matches`

**Inputs** self, row, category.

**Declared result** bool.

**Explicit results** category belongs to self.categories · row.get(“account\_type”) belongs to self.account\_types.

**Local steps**

- If category.
  - Return category belongs to self.categories.
- Return row.get(“account\_type”) belongs to self.account\_types.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1205)

<a id="op-feed6a5f2f2136"></a>
### Execute

`operation_enterprise_accounts_report_financial_ratios_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set filters at “filter\_based\_on” from “Fiscal Year”.
- Set tuple(columns, data) from tuple(list(), list()).
- Evaluate setup\_filters(filters).
- Set period\_list from get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters.period\_start\_date, filters.period\_end\_date, company = filters.company, …).
- Set tuple(columns, years) from get\_columns(period\_list).
- Set data from get\_ratios\_data(filters, period\_list, years).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L2984) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L899)

<a id="op-5d94ff1d8a5830"></a>
### Setup filters

`operation_enterprise_accounts_report_financial_ratios_business_behavior_setup_filters`

**Inputs** filters.

**Local steps**

- If not filters.get(“period\_start\_date”).
  - Set period\_start\_date from get\_fiscal\_year(fiscal\_year = filters.from\_fiscal\_year) at 1.
  - Set filters at “period\_start\_date” from period\_start\_date.
- If not filters.get(“period\_end\_date”).
  - Set period\_end\_date from get\_fiscal\_year(fiscal\_year = filters.to\_fiscal\_year) at 2.
  - Set filters at “period\_end\_date” from period\_end\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L3268) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L903)

<a id="op-7367877efa9929"></a>
### Get columns

`operation_enterprise_accounts_report_financial_ratios_business_behavior_get_columns`

**Inputs** period\_list.

**Explicit results** tuple(columns, years).

**Local steps**

- Set years from list().
- Set columns from list(mapping(“label” → translated “Ratios”, “fieldname” → “ratio”, “fieldtype” → “Data”, “width” → 200)).
- For each period in period\_list.
  - Evaluate columns.append(mapping(“fieldname” → period.key, “label” → period.label, “fieldtype” → “Float”, “width” → 150)).
  - Evaluate years.append(period.key).
- Return tuple(columns, years).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L3506) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L900)

<a id="op-09a3c865ff1973"></a>
### Get ratios data

`operation_enterprise_accounts_report_financial_ratios_business_behavior_get_ratios_data`

**Inputs** filters, period\_list, years.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set tuple(assets, liabilities, income, expense) from get\_gl\_data(filters, period\_list, years).
- Set tuple(current\_asset, total\_asset) from tuple(mapping(), mapping()).
- Set tuple(current\_liability, total\_liability) from tuple(mapping(), mapping()).
- Set tuple(net\_sales, total\_income) from tuple(mapping(), mapping()).
- Set tuple(cogs, total\_expense) from tuple(mapping(), mapping()).
- Set quick\_asset from mapping().
- Set direct\_expense from mapping().
- Set fixed\_asset from mapping().
- For each year in years.
  - Set total\_quick\_asset from 0.
  - Set total\_net\_sales from 0.
  - Set total\_cogs from 0.
  - For each d in list(list(current\_asset, total\_asset, “Current Asset”, year, …), list(fixed\_asset, total\_asset, “Fixed Asset”, year, …), list(current\_liability, total\_liability, “Current Liability”, year, …), list(cogs, t ….
    - Evaluate update\_balances(d at 0, d at 1, d at 2, d at 3, …).
- Evaluate add\_liquidity\_ratios(data, years, current\_asset, current\_liability, …).
- Evaluate add\_solvency\_ratios(data, years, total\_asset, total\_liability, …).
- Evaluate add\_turnover\_ratios(data, years, period\_list, filters, …).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L902)

<a id="op-eb99f3999badc3"></a>
### Get gl data

`operation_enterprise_accounts_report_financial_ratios_business_behavior_get_general_ledger_data`

**Inputs** filters, period\_list, years.

**Explicit results** tuple(assets, liabilities, income, expense).

**Local steps**

- Set data from mapping().
- For each tuple(root\_type, balance\_must\_be) in list(list(“Asset”, “Debit”), list(“Liability”, “Credit”)).
  - Set data at Platform.scrub(root\_type) from get\_data(filters.company, root\_type, balance\_must\_be, period\_list, only\_current\_fiscal\_year = false, filters = filters).
- For each tuple(root\_type, balance\_must\_be) in list(list(“Income”, “Credit”), list(“Expense”, “Debit”)).
  - Set data at Platform.scrub(root\_type) from get\_data(filters.company, root\_type, balance\_must\_be, period\_list, filters = filters, accumulated\_values = 0, ignore\_closing\_entries = true).
- Set tuple(assets, liabilities, income, expense) from tuple(data.get(“asset”), data.get(“liability”), data.get(“income”), data.get(“expense”)).
- Return tuple(assets, liabilities, income, expense).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L901)

<a id="op-e80108dcf2061f"></a>
### Add liquidity ratios

`operation_enterprise_accounts_report_financial_ratios_business_behavior_add_liquidity_ratios`

**Inputs** data, years, current\_asset, current\_liability, quick\_asset.

**Record and data access** read “System Settings” via get\_single\_value.

**Local steps**

- Set precision from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).
- Evaluate data.append(mapping(“ratio” → translated “Liquidity Ratios”)).
- Set ratio\_data from list(list(translated “Current Ratio”, current\_asset), list(translated “Quick Ratio”, quick\_asset)).
- For each d in ratio\_data.
  - Set row from mapping(“ratio” → d at 0).
  - For each year in years.
    - Set row at year from calculate\_ratio(d at 1.get(year, 0), current\_liability.get(year, 0), precision).
  - Evaluate data.append(row).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L5013) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L894)

<a id="op-c4f9e7efb99d95"></a>
### Add solvency ratios

`operation_enterprise_accounts_report_financial_ratios_business_behavior_add_solvency_ratios`

**Inputs** data, years, total\_asset, total\_liability, net\_sales, cogs, total\_income, total\_expense.

**Record and data access** read “System Settings” via get\_single\_value.

**Local steps**

- Set precision from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).
- Evaluate data.append(mapping(“ratio” → translated “Solvency Ratios”)).
- Set debt\_equity\_ratio from mapping(“ratio” → translated “Debt Equity Ratio”).
- Set gross\_profit\_ratio from mapping(“ratio” → translated “Gross Profit Ratio”).
- Set net\_profit\_ratio from mapping(“ratio” → translated “Net Profit Ratio”).
- Set return\_on\_asset\_ratio from mapping(“ratio” → translated “Return on Asset Ratio”).
- Set return\_on\_equity\_ratio from mapping(“ratio” → translated “Return on Equity Ratio”).
- For each year in years.
  - Set profit\_after\_tax from (flt(total\_income.get(year)) − flt(total\_expense.get(year))).
  - Set share\_holder\_fund from (flt(total\_asset.get(year)) − flt(total\_liability.get(year))).
  - Set debt\_equity\_ratio at year from calculate\_ratio(total\_liability.get(year), share\_holder\_fund, precision).
  - Set return\_on\_equity\_ratio at year from calculate\_ratio(profit\_after\_tax, share\_holder\_fund, precision).
  - Set net\_profit\_ratio at year from calculate\_ratio(profit\_after\_tax, net\_sales.get(year), precision).
  - Set gross\_profit\_ratio at year from calculate\_ratio((net\_sales.get(year, 0) − cogs.get(year, 0)), net\_sales.get(year), precision).
  - Set return\_on\_asset\_ratio at year from calculate\_ratio(profit\_after\_tax, total\_asset.get(year), precision).
- Evaluate data.append(debt\_equity\_ratio).
- Evaluate data.append(gross\_profit\_ratio).
- Evaluate data.append(net\_profit\_ratio).
- Evaluate data.append(return\_on\_asset\_ratio).
- Evaluate data.append(return\_on\_equity\_ratio).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L5408) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L895)

<a id="op-72f508a47157e2"></a>
### Add turnover ratios

`operation_enterprise_accounts_report_financial_ratios_business_behavior_add_turnover_ratios`

**Inputs** data, years, period\_list, filters, fixed\_asset, net\_sales, cogs, direct\_expense.

**Record and data access** read “System Settings” via get\_single\_value.

**Local steps**

- Set precision from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).
- Evaluate data.append(mapping(“ratio” → translated “Turnover Ratios”)).
- Set avg\_data from mapping().
- For each d in list(“Receivable”, “Payable”, “Stock”).
  - Set avg\_data at Platform.scrub(d) from avg\_ratio\_balance(d, period\_list, precision, filters).
- Set tuple(avg\_debtors, avg\_stock) from tuple(avg\_data.get(“receivable”), avg\_data.get(“stock”)).
- Set avg\_creditors from mapping of key → negative flt(balance) for tuple(key, balance) drawn from avg\_data.get(“payable”).items().
  - Draw tuple(key, balance) from avg\_data.get(“payable”).items().
- Set ratio\_data from list(list(translated “Fixed Asset Turnover Ratio”, net\_sales, fixed\_asset), list(translated “Debtor Turnover Ratio”, net\_sales, avg\_debtors), list(translated “Creditor Turnover Ratio”, direct\_expense, avg\_ ….
- For each ratio in ratio\_data.
  - Set row from mapping(“ratio” → ratio at 0).
  - For each year in years.
    - Set row at year from calculate\_ratio(ratio at 1.get(year, 0), ratio at 2.get(year, 0), precision).
  - Evaluate data.append(row).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L896)

<a id="op-0c892d8e48cf44"></a>
### Update balances

`operation_enterprise_accounts_report_financial_ratios_business_behavior_update_balances`

**Inputs** ratio\_dict, total\_dict, account\_type, year, root\_type\_data, root\_type, net\_dict = no value, total\_net = 0.

**Local steps**

- Set group\_accounts from get\_group\_accounts(account\_type, root\_type\_data).
- For each entry in root\_type\_data.
  - If (not entry.get(“parent\_account”) and entry.get(“is\_group”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entry.get(“parent\_account”) → entry.get(“is\_group”).
    - Set total\_dict at year from entry at year.
  - If (root\_type equals “Expense” and account\_type equals “Cost of Goods Sold”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_type equals “Expense” → account\_type equals “Cost of Goods Sold”.
    - If entry.get(“account\_type”) equals account\_type.
      - Update total\_net using + entry.get(year).
      - Set ratio\_dict at year from total\_net.
  - Otherwise.
    - If entry.get(“account”) belongs to group\_accounts.
      - Set ratio\_dict at year from (flt(ratio\_dict.get(year)) + flt(entry.get(year))).
  - If root\_type belongs to tuple(“Asset”, “Liability”).
    - If (entry.get(“account\_type”) belongs to list(“Bank”, “Cash”, “Receivable”) and not entry.get(“is\_group”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.get(“account\_type”) belongs to list(“Bank”, “Cash”, “Receivable”) → not entry.get(“is\_group”).
      - Update total\_net using + entry.get(year).
      - Set net\_dict at year from total\_net.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L904)

<a id="op-00e8184cf080f6"></a>
### Get group accounts

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_get_group_accounts`

**Inputs** account\_type, root\_type\_data.

**Declared result** set at str.

**Explicit results** typed\_groups · GROUP\_LEDGERS at account\_type.get\_accounts(accounts).

**Local steps**

- Set accounts from mapping of entry.get(“account”) → entry for entry drawn from root\_type\_data where entry.get(“account”).
  - Draw entry from root\_type\_data, keep a combination only if (entry.get(“account”)).
- Set typed\_groups from set of name for tuple(name, entry) drawn from accounts.items() where is\_outermost\_group\_of\_type(entry, account\_type, accounts).
  - Draw tuple(name, entry) from accounts.items(), keep a combination only if (is\_outermost\_group\_of\_type(entry, account\_type, accounts)).
- If (typed\_groups or account\_type does not belong to GROUP\_LEDGERS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in typed\_groups → account\_type does not belong to GROUP\_LEDGERS.
  - Return typed\_groups.
- Return GROUP\_LEDGERS at account\_type.get\_accounts(accounts).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1201)

<a id="op-fe2b49a8901529"></a>
### Is outermost group of type

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_is_outermost_group_of_type`

**Inputs** entry, account\_type, accounts.

**Explicit results** false · true.

**Local steps**

- If not (entry.get(“is\_group”) and entry.get(“account\_type”) equals account\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.get(“is\_group”) → entry.get(“account\_type”) equals account\_type.
  - Return false.
- Set parent from accounts.get(entry.get(“parent\_account”)).
- While parent.
  - If (parent.get(“is\_group”) and parent.get(“account\_type”) equals account\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.get(“is\_group”) → parent.get(“account\_type”) equals account\_type.
    - Return false.
  - Set parent from accounts.get(parent.get(“parent\_account”)).
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1206)

<a id="op-33efe694c4e5b8"></a>
### Get account categories

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_get_account_categories`

**Inputs** accounts.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Account” via get\_all.

**Explicit results** mapping() · mapping of name → get\_inherited\_category(name, own\_categories, accounts) for name drawn from accounts.

**Local steps**

- If not accounts.
  - Return mapping().
- Set own\_categories from dict(Platform.get\_all(“Account”, filters = mapping(“name” → tuple(“in”, list(accounts)), “account\_category” → tuple(“is”, “set”)), fields = list(“name”, “account\_category”), as\_list = true)).
- Return mapping of name → get\_inherited\_category(name, own\_categories, accounts) for name drawn from accounts.
  - Draw name from accounts.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1200)

<a id="op-86e2c82ac292cb"></a>
### Get inherited category

`operation_enterprise_binding_enterprise_accounts_report_financial_ratios_financial_ratios_get_inherited_category`

**Inputs** account, categories, accounts.

**Declared result** (str bitwise or no value).

**Explicit results** categories.get(account).

**Local steps**

- While (account and not categories.get(account)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account → not categories.get(account).
  - Set account from accounts.get(account, mapping()).get(“parent\_account”).
- Return categories.get(account).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1202)

<a id="op-6e25a4f1cac71d"></a>
### Avg ratio balance

`operation_enterprise_accounts_report_financial_ratios_business_behavior_average_ratio_balance`

**Inputs** account\_type, period\_list, precision, filters.

**Explicit results** avg\_ratio.

**Local steps**

- Set avg\_ratio from mapping().
- For each period in period\_list.
  - Set opening\_date from add\_days(period at “from\_date”, negative 1).
  - Set closing\_date from period at “to\_date”.
  - Set closing\_balance from get\_balance\_on(date = closing\_date, company = filters.company, account\_type = account\_type, in\_account\_currency = false).
  - Set opening\_balance from get\_balance\_on(date = opening\_date, company = filters.company, account\_type = account\_type, in\_account\_currency = false).
  - Set avg\_ratio at period at “key” from flt(((flt(closing\_balance) + flt(opening\_balance)) ÷ 2), precision = precision).
- Return avg\_ratio.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L897)
