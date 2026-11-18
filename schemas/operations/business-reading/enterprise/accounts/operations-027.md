# Accounting and settlement · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Consolidated accounts receivable

<a id="op-e1a638e4d902b3"></a>
### Add company columns

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_consolidated_accounts_receivable_add_company_columns`

**Inputs** columns.

**State and service calls** call insert on columns.

**Local steps**

- Set at from company\_column\_index(columns).
- Evaluate columns.insert(at, dict(label = translated “Company”, fieldname = “company”, fieldtype = “Link”, options = “Company”, …)).
- Evaluate columns.insert((at + 1), dict(label = translated “Parent Company”, fieldname = “parent\_company”, fieldtype = “Data”, width = 160)).
- For each column in columns.
  - Set column at “align” from “right” when column at “fieldtype” belongs to numeric\_fieldtypes, otherwise “left”.
    - Value choice on column at “fieldtype” belongs to numeric\_fieldtypes — true gives “right”, false gives “left”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1149)

<a id="op-a051cdbc7e53c0"></a>
### Company column index

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_consolidated_accounts_receivable_company_column_index`

**Inputs** columns.

**Explicit results** (fieldnames.index(fieldname) + 1) · 0.

**Local steps**

- Set fieldnames from list of column at “fieldname” for column drawn from columns.
  - Draw column from columns.
- For each fieldname in tuple(“party\_name”, “party”).
  - If fieldname belongs to fieldnames.
    - Return (fieldnames.index(fieldname) + 1).
- Return 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1150)

## Report · Consolidated accounts receivable summary

<a id="op-7ae43ae1f758dd"></a>
### Execute

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_summary_consolidated_accounts_receivable_summary_execute`

**Inputs** filters = no value.

**Explicit results** ConsolidatedReceivablePayableSummary(filters).run(args).

**Local steps**

- Set args from mapping(“account\_type” → “Receivable”, “naming\_by” → list(“Selling Settings”, “cust\_master\_name”)).
- Return ConsolidatedReceivablePayableSummary(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1167)

<a id="op-2e02e0f2dbe936"></a>
### Consolidated Receivable Payable Summary.run

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_summary_consolidated_accounts_receivable_summary_consolidatedreceivablepayablesummary_run`

**Inputs** self, args.

**Explicit results** super().run(args).

**Local steps**

- Set self.companies from get\_consolidated\_companies(self.filters).
- Return super().run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1165)

<a id="op-870fbc736edbc8"></a>
### Consolidated Receivable Payable Summary.get columns

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_summary_consolidated_accounts_receivable_summary_consolidatedreceivablepayablesummary_get_columns`

**Inputs** self.

**Local steps**

- Evaluate super().get\_columns().
- Evaluate add\_company\_columns(self.columns).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1162)

<a id="op-b2dc50e4805d9e"></a>
### Consolidated Receivable Payable Summary.get data

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_summary_consolidated_accounts_receivable_summary_consolidatedreceivablepayablesummary_get_data`

**Inputs** self, args.

**Local steps**

- Set self.data from list().
- For each rows in self.get\_rows\_by\_party(args).values().
  - Evaluate self.data.extend(rows).
  - If len(row\_currencies(rows)) ≤ 1.
    - Evaluate self.data.append(self.total\_row(rows)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows by party](operations-027.md#op-27aee84eda1c61), [total row](operations-027.md#op-b9795a74d225b1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1163)

<a id="op-27aee84eda1c61"></a>
### Consolidated Receivable Payable Summary.get rows by party

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_summary_consolidated_accounts_receivable_summary_consolidatedreceivablepayablesummary_get_rows_by_party`

**Inputs** self, args.

**Explicit results** by\_party.

**Local steps**

- Set by\_party from OrderedDict().
- For each row in rows\_per\_company(self.companies, self.filters, args, AccountsReceivableSummary).
  - Evaluate by\_party.setdefault(row.party, list()).append(row).
- Return by\_party.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1164)

<a id="op-b9795a74d225b1"></a>
### Consolidated Receivable Payable Summary.total row

`operation_enterprise_binding_enterprise_accounts_report_consolidated_accounts_receivable_summary_consolidated_accounts_receivable_summary_consolidatedreceivablepayablesummary_total_row`

**Inputs** self, rows.

**Explicit results** total.

**Local steps**

- Set total from Platform.\_dict(party\_type = translated “Total”, party = empty text, company = empty text, currency = rows at 0.get(“currency”), …).
- For each row in rows.
  - For each tuple(field, value) in row.items().
    - If (isinstance(value, (int bitwise or float)) and not isinstance(value, bool)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, (int bitwise or float)) → not isinstance(value, bool).
      - Set total at field from (flt(total.get(field)) + value).
- Return total.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1166)

## Report · Consolidated financial statement

<a id="op-c5478cc6716a03"></a>
### Execute

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, message, chart) · tuple(columns, data, message, chart, …).

**Local steps**

- Set tuple(columns, data, message, chart) from tuple(list(), list(), list(), list()).
- If not filters.get(“company”).
  - Return tuple(columns, data, message, chart).
- If filters.get(“filter\_based\_on”) equals “Date Range”.
  - Evaluate validate\_dates(filters.get(“period\_start\_date”), filters.get(“period\_end\_date”)).
- Set fiscal\_year from get\_fiscal\_year\_data(filters.get(“from\_fiscal\_year”), filters.get(“to\_fiscal\_year”)).
- Set tuple(company\_list, companies) from get\_companies(filters).
- Set company\_columns from get\_company\_columns(company\_list, filters).
- Set columns from get\_columns(company\_columns).
- If filters.get(“report”) equals “Balance Sheet”.
  - Set tuple(data, message, chart, report\_summary) from get\_balance\_sheet\_data(fiscal\_year, companies, company\_columns, filters).
- Otherwise.
  - If filters.get(“report”) equals “Profit and Loss Statement”.
    - Set tuple(data, message, chart, report\_summary) from get\_profit\_loss\_data(fiscal\_year, companies, company\_columns, filters).
  - Otherwise.
    - Set tuple(data, report\_summary) from get\_cash\_flow\_data(fiscal\_year, companies, filters).
- Return tuple(columns, data, message, chart, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L761)

<a id="op-dc816922096fe2"></a>
### Get balance sheet data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_balance_sheet_data`

**Inputs** fiscal\_year, companies, company\_columns, filters.

**Explicit results** tuple(data, message, chart, report\_summary).

**Local steps**

- Set translator from CurrencyTranslator(companies, filters, fiscal\_year).
- Evaluate translator.add\_profit\_and\_loss\_difference().
- Set asset from get\_data(companies, “Asset”, “Debit”, fiscal\_year, translator = translator, …).
- Set liability from get\_data(companies, “Liability”, “Credit”, fiscal\_year, translator = translator, …).
- Set equity from get\_data(companies, “Equity”, “Credit”, fiscal\_year, translator = translator, …).
- Set data from list().
- Evaluate data.extend((asset or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset → list().
- Evaluate data.extend((liability or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in liability → list().
- Evaluate data.extend((equity or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in equity → list().
- Set company\_currency from get\_company\_currency(filters).
- Set tuple(provisional\_profit\_loss, total\_credit) from get\_provisional\_profit\_loss(asset, liability, equity, companies, …).
- Set tuple(message, opening\_balance) from prepare\_companywise\_opening\_balance(asset, liability, equity, companies).
- If opening\_balance.
  - Set unclosed from mapping(“account\_name” → ((“'” + translated “Unclosed Fiscal Years Profit / Loss (Credit)”) + “'”), “account” → ((“'” + translated “Unclosed Fiscal Years Profit / Loss (Credit)”) + “'”), “warn\_if\_negative” ….
  - For each company in companies.
    - Set unclosed at company from opening\_balance.get(company).
    - If (provisional\_profit\_loss and provisional\_profit\_loss.get(company)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in provisional\_profit\_loss → provisional\_profit\_loss.get(company).
      - Set provisional\_profit\_loss at company from (flt(provisional\_profit\_loss at company) − flt(opening\_balance.get(company))).
  - Set unclosed at “total” from sum(opening\_balance.values()).
  - Evaluate set\_group\_company\_total(unclosed, filters).
  - Evaluate data.append(unclosed).
- Evaluate set\_group\_company\_total(provisional\_profit\_loss, filters).
- Evaluate set\_group\_company\_total(total\_credit, filters).
- If provisional\_profit\_loss.
  - Evaluate data.append(provisional\_profit\_loss).
- If total\_credit.
  - Evaluate data.append(total\_credit).
- Set tuple(report\_summary, primitive\_summary) from get\_bs\_summary(get\_summary\_companies(companies, filters), asset, liability, equity, …).
- Set chart from get\_chart\_data(filters, company\_columns, asset, liability, …).
- Return tuple(data, message, chart, report\_summary).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L769)

<a id="op-f1c1cf6961cc21"></a>
### Prepare companywise opening balance

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_prepare_companywise_opening_balance`

**Inputs** asset\_data, liability\_data, equity\_data, companies.

**Explicit results** tuple(translated “Previous Financial Year is not closed”, opening\_balance) · tuple(empty text, mapping()).

**Local steps**

- Set opening\_balance from mapping().
- For each company in companies.
  - Set opening\_value from 0.
  - For each data in list(asset\_data, liability\_data, equity\_data).
    - If data.
      - Set account\_name from get\_root\_account\_name(data at 0.root\_type, company).
      - If account\_name.
        - Update opening\_value using + (get\_opening\_balance(account\_name, data, company) or 0.0).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_opening\_balance(account\_name, data, company) → 0.0.
  - Set opening\_balance at company from opening\_value.
- If any(generator of flt(value, 3) for value drawn from opening\_balance.values()).
  - Draw value from opening\_balance.values().
  - Return tuple(translated “Previous Financial Year is not closed”, opening\_balance).
- Return tuple(empty text, mapping()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L781)

<a id="op-e5c1c87615d946"></a>
### Get opening balance

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_opening_balance`

**Inputs** account\_name, data, company.

**Explicit results** row.get(“company\_wise\_opening\_bal”, mapping()).get(company, 0.0).

**Local steps**

- For each row in data.
  - If row.get(“account\_name”) equals account\_name.
    - Return row.get(“company\_wise\_opening\_bal”, mapping()).get(company, 0.0).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0236.json#L4876) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L777)

<a id="op-c3ee1075fc98c6"></a>
### Get root account name

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_root_account_name`

**Inputs** root\_type, company.

**Record and data access** read “Account” via get\_all.

**Explicit results** root\_account at 0 at 0.

**Local steps**

- Set root\_account from Platform.get\_all(“Account”, fields = list(“account\_name”), filters = mapping(“root\_type” → root\_type, “is\_group” → 1, “company” → company, “parent\_account” → tuple(“is”, “not set”)), as\_list = 1).
- If root\_account.
  - Return root\_account at 0 at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0236.json#L5025) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L779)

<a id="op-9a9f98fc1a2e2c"></a>
### Get profit loss data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_profit_loss_data`

**Inputs** fiscal\_year, companies, company\_columns, filters.

**Explicit results** tuple(data, no value, chart, report\_summary).

**Local steps**

- Set tuple(income, expense, net\_profit\_loss) from get\_income\_expense\_data(companies, fiscal\_year, filters).
- Set company\_currency from get\_company\_currency(filters).
- Set data from list().
- Evaluate data.extend((income or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in income → list().
- Evaluate data.extend((expense or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in expense → list().
- If net\_profit\_loss.
  - Evaluate data.append(net\_profit\_loss).
- Set chart from get\_pl\_chart\_data(filters, company\_columns, income, expense, …).
- Set tuple(report\_summary, primitive\_summary) from get\_pl\_summary(get\_summary\_companies(companies, filters), empty text, income, expense, …).
- Return tuple(data, no value, chart, report\_summary).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L778)

<a id="op-4db2e4b62cf690"></a>
### Get summary companies

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_get_summary_companies`

**Inputs** companies, filters.

**Explicit results** list(companies) · list(companies) when len(currencies) equals 1, otherwise list(filters.company).

**Local steps**

- If filters.get(“presentation\_currency”).
  - Return list(companies).
- Set currencies from set of Enterprise.get\_company\_currency(company) for company drawn from companies.
  - Draw company from companies.
- Return list(companies) when len(currencies) equals 1, otherwise list(filters.company).
  - Value choice on len(currencies) equals 1 — true gives list(companies), false gives list(filters.company).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1188)

<a id="op-8543479d9316c7"></a>
### Get income expense data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_income_expense_data`

**Inputs** companies, fiscal\_year, filters, translator = no value.

**Explicit results** tuple(income, expense, net\_profit\_loss).

**Local steps**

- Set company\_currency from get\_company\_currency(filters).
- Set translator from (translator or CurrencyTranslator(companies, filters, fiscal\_year)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in translator → CurrencyTranslator(companies, filters, fiscal\_year).
- Set income from get\_data(companies, “Income”, “Credit”, fiscal\_year, …).
- Set expense from get\_data(companies, “Expense”, “Debit”, fiscal\_year, …).
- Set net\_profit\_loss from get\_net\_profit\_loss(income, expense, companies, filters.company, consolidated = true, accumulated\_values = bool(filters.accumulated\_values), …).
- Evaluate set\_group\_company\_total(net\_profit\_loss, filters).
- Return tuple(income, expense, net\_profit\_loss).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L776)

<a id="op-19e2f65c9d524e"></a>
### Get cash flow data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_cash_flow_data`

**Inputs** fiscal\_year, companies, filters.

**Explicit results** tuple(data, report\_summary).

**Local steps**

- Set cash\_flow\_accounts from get\_cash\_flow\_accounts().
- Set translator from CurrencyTranslator(companies, filters, fiscal\_year).
- Set tuple(income, expense, net\_profit\_loss) from get\_income\_expense\_data(companies, fiscal\_year, filters, translator).
- Set translation\_difference from get\_translation\_difference\_row(translator, companies, filters).
- Set data from list().
- Set summary\_data from mapping().
- Set company\_currency from get\_company\_currency(filters).
- For each cash\_flow\_account in cash\_flow\_accounts.
  - Set section\_data from list().
  - Evaluate data.append(mapping(“account\_name” → cash\_flow\_account at “section\_header”, “parent\_account” → no value, “indent” → 0.0, “account” → cash\_flow\_account at “section\_header”)).
  - If len(data) equals 1.
    - If net\_profit\_loss.
      - Evaluate net\_profit\_loss.update(mapping(“indent” → 1, “parent\_account” → cash\_flow\_accounts at 0 at “section\_header”)).
      - Evaluate data.append(net\_profit\_loss).
      - Evaluate section\_data.append(net\_profit\_loss).
    - If translation\_difference.
      - Evaluate translation\_difference.update(mapping(“currency” → company\_currency, “parent\_account” → cash\_flow\_accounts at 0 at “section\_header”)).
      - Evaluate data.append(translation\_difference).
      - Evaluate section\_data.append(translation\_difference).
  - For each account in cash\_flow\_account at “account\_types”.
    - Set account\_data from get\_account\_type\_based\_data(account at “account\_type”, companies, fiscal\_year, filters).
    - Evaluate account\_data.update(mapping(“account\_name” → account at “label”, “account” → account at “label”, “indent” → 1, “parent\_account” → cash\_flow\_account at “section\_header”, …)).
    - Evaluate data.append(account\_data).
    - Evaluate section\_data.append(account\_data).
  - Evaluate add\_cash\_flow\_total\_row(data, section\_data, cash\_flow\_account at “section\_footer”, companies, …).
- Evaluate add\_cash\_flow\_total\_row(data, data, translated “Net Change in Cash”, companies, …).
- Set report\_summary from get\_cash\_flow\_summary(summary\_data, company\_currency).
- Return tuple(data, report\_summary).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L770)

<a id="op-9cc26f92033837"></a>
### Get translation difference row

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_get_translation_difference_row`

**Inputs** translator, companies, filters.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · row.

**Local steps**

- If not any(generator of flt(amount, 3) for amount drawn from translator.reserve.values()).
  - Draw amount from translator.reserve.values().
  - Return no value.
- Set label from translated “Foreign Currency Translation Reserve”.
- Set row from mapping of company → negative flt(translator.reserve.get(company), 3) for company drawn from companies.
  - Draw company from companies.
- Evaluate row.update(mapping(“total” → sum(row.values()), “account\_name” → label, “account” → label, “indent” → 1)).
- Evaluate set\_group\_company\_total(row, filters).
- Return row.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1189)

<a id="op-396426fb2b2b86"></a>
### Add cash flow total row

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_add_cash_flow_total_row`

**Inputs** out, rows, label, companies, currency, summary\_data, filters.

**Declared result** no value.

**Local steps**

- Set column\_filters from Platform.\_dict(filters, accumulated\_in\_group\_company = 0).
- Set total\_row from add\_total\_row\_account(out, rows, label, companies, …).
- If filters.get(“accumulated\_in\_group\_company”).
  - Set summary\_data at label from total\_row.get(filters.company, 0.0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1168)

<a id="op-d3d9c337e58e9c"></a>
### Get account type based data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_account_type_based_data`

**Inputs** account\_type, companies, fiscal\_year, filters.

**Explicit results** data.

**Local steps**

- Set gl\_filters from Platform.\_dict(filters, account\_type = account\_type).
- Set tuple(gl\_filters.start\_date, gl\_filters.end\_date) from get\_period\_dates(fiscal\_year, filters).
- Set own\_amounts from mapping of company → get\_company\_account\_type\_amount(company, gl\_filters) for company drawn from companies.
  - Draw company from companies.
- Set data from mapping of company → get\_column\_amount(company, companies, own\_amounts, gl\_filters) for company drawn from companies.
  - Draw company from companies.
- If filters.get(“accumulated\_in\_group\_company”).
  - Set data at “total” from data at filters.company.
- Otherwise.
  - Set data at “total” from sum(own\_amounts.values()).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L766)

<a id="op-75697941410c2d"></a>
### Get period dates

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_get_period_dates`

**Inputs** fiscal\_year, filters.

**Explicit results** tuple(filters.period\_start\_date, filters.period\_end\_date) · tuple(fiscal\_year.year\_start\_date, fiscal\_year.year\_end\_date).

**Local steps**

- If filters.filter\_based\_on equals “Date Range”.
  - Return tuple(filters.period\_start\_date, filters.period\_end\_date).
- Return tuple(fiscal\_year.year\_start\_date, fiscal\_year.year\_end\_date).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1186)

<a id="op-a9e4833fc58ff3"></a>
### Get company account type amount

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_get_company_account_type_amount`

**Inputs** company, filters.

**Explicit results** convert\_to\_presentation\_currency\_amount(amount, company, filters).

**Local steps**

- Set amount from get\_account\_type\_based\_gl\_data(company, filters).
- If filters.account\_type equals “Depreciation”.
  - Update amount using × negative 1.
- Return convert\_to\_presentation\_currency\_amount(amount, company, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1185)

<a id="op-6435de17bda3d4"></a>
### Convert to presentation currency amount

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_convert_to_presentation_currency_amount`

**Inputs** amount, company, filters.

**Explicit results** amount · flt(convert(amount, presentation\_currency, company\_currency, filters.end\_date), 3).

**Local steps**

- Set presentation\_currency from filters.get(“presentation\_currency”).
- Set company\_currency from Enterprise.get\_company\_currency(company).
- If (not presentation\_currency or presentation\_currency equals company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not presentation\_currency → presentation\_currency equals company\_currency.
  - Return amount.
- Return flt(convert(amount, presentation\_currency, company\_currency, filters.end\_date), 3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1173)

<a id="op-70fdb0e7d0905e"></a>
### Get column amount

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_get_column_amount`

**Inputs** company, companies, own\_amounts, filters.

**Explicit results** own\_amounts at company · flt(amount, 3).

**Local steps**

- If not filters.get(“accumulated\_in\_group\_company”).
  - Return own\_amounts at company.
- Set amount from sum(generator of convert\_to\_column\_currency(own\_amounts at subsidiary, subsidiary, company, filters) for subsidiary drawn from companies at company).
  - Draw subsidiary from companies at company.
- Return flt(amount, 3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1184)
