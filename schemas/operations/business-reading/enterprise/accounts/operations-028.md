# Accounting and settlement · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Consolidated financial statement

<a id="op-bf78ae1444bf59"></a>
### Convert to column currency

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_convert_to_column_currency`

**Inputs** amount, company, column\_company, filters.

**Explicit results** amount · convert(amount, column\_currency, company\_currency, filters.end\_date).

**Local steps**

- Set column\_currency from Enterprise.get\_company\_currency(column\_company).
- Set company\_currency from Enterprise.get\_company\_currency(company).
- If (filters.get(“presentation\_currency”) or column\_currency equals company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“presentation\_currency”) → column\_currency equals company\_currency.
  - Return amount.
- Return convert(amount, column\_currency, company\_currency, filters.end\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1172)

<a id="op-cd4eac11a06ba1"></a>
### Get company columns

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_company_columns`

**Inputs** companies, filters.

**Explicit results** company\_columns.

**Local steps**

- Set company\_columns from list().
- For each company in companies.
  - Set apply\_currency\_formatter from 1 when not filters.presentation\_currency, otherwise 0.
    - Value choice on not filters.presentation\_currency — true gives 1, false gives 0.
  - Set currency from filters.presentation\_currency.
  - If not currency.
    - Set currency from Enterprise.get\_company\_currency(company).
  - Evaluate company\_columns.append(mapping(“fieldname” → company, “label” → formatted text {company} ({currency}), “fieldtype” → “Currency”, “options” → “currency”, …)).
- Return company\_columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0236.json#L7079) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L773)

<a id="op-b5701031dc035d"></a>
### Get columns

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_columns`

**Inputs** company\_columns.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “account”, “label” → translated “Account”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“fieldname” → “currency”, “label” → translated “Currency”, “fieldtype” → “Link ….
- Evaluate columns.extend(company\_columns).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L771)

<a id="op-cbb00411468185"></a>
### Get data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_data`

**Inputs** companies, root\_type, balance\_must\_be, fiscal\_year, filters = no value, ignore\_closing\_entries = false, translator = no value.

**Record and data access** execute query text (SELECT, Account).

**Explicit results** list() · out.

**Local steps**

- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from get\_account\_heads(root\_type, companies, filters).
- If not accounts.
  - Return list().
- Set company\_currency from get\_company\_currency(filters).
- If filters.filter\_based\_on equals “Fiscal Year”.
  - Set start\_date from fiscal\_year.year\_start\_date when filters.report differs from “Balance Sheet”, otherwise no value.
    - Value choice on filters.report differs from “Balance Sheet” — true gives fiscal\_year.year\_start\_date, false gives no value.
  - Set end\_date from fiscal\_year.year\_end\_date.
- Otherwise.
  - Set start\_date from filters.period\_start\_date when filters.report differs from “Balance Sheet”, otherwise no value.
    - Value choice on filters.report differs from “Balance Sheet” — true gives filters.period\_start\_date, false gives no value.
  - Set end\_date from filters.period\_end\_date.
- Set filters.end\_date from end\_date.
- Set gl\_entries\_by\_account from mapping().
- For each root in Platform.db.sql(query text (SELECT, Account), root\_type, as\_dict = 1).
  - Evaluate set\_gl\_entries\_by\_account(start\_date, end\_date, root.lft, root.rgt, ignore\_closing\_entries = ignore\_closing\_entries, root\_type = root\_type, …).
- Set translator from (translator or CurrencyTranslator(companies, filters, fiscal\_year)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in translator → CurrencyTranslator(companies, filters, fiscal\_year).
- Evaluate calculate\_values(accounts\_by\_name, gl\_entries\_by\_account, translator).
- If root\_type equals “Equity”.
  - Evaluate add\_translation\_reserve\_account(accounts, translator).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name, companies).
- Set out from prepare\_data(accounts, start\_date, end\_date, balance\_must\_be, …).
- Set out from filter\_out\_zero\_value\_rows(out, parent\_children\_map, show\_zero\_values = filters.get(“show\_zero\_values”)).
- If out.
  - Evaluate add\_total\_row(out, root\_type, balance\_must\_be, companies, …).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L775)

<a id="op-5ad2686f583a35"></a>
### Get company currency

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_company_currency`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** (filters.get(“presentation\_currency”) or Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”)).

**Local steps**

- Return (filters.get(“presentation\_currency”) or Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“presentation\_currency”) → Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L1090) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L774)

<a id="op-8fa67d46c81485"></a>
### Calculate values

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_calculate_values`

**Inputs** accounts\_by\_name, gl\_entries\_by\_account, translator.

**Local steps**

- For each entries in gl\_entries\_by\_account.values().
  - For each entry in entries.
    - If entry.account\_number.
      - Set account\_name from ((entry.account\_number + “ - ”) + entry.account\_name).
    - Otherwise.
      - Set account\_name from entry.account\_name.
    - If account bound to accounts\_by\_name.get(account\_name).
      - Evaluate add\_entry\_to\_columns(account, entry, translator).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L760)

<a id="op-d233fb6d418951"></a>
### Add entry to columns

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_add_entry_to_columns`

**Inputs** account, entry, translator.

**Local steps**

- Set amount from 0.0.
- Set is\_opening from translator.is\_opening(entry).
- For each company in translator.get\_column\_companies(entry).
  - Set amount from translator.translate(entry, company).
  - Set account at company from (account.get(company, 0.0) + amount).
  - If is\_opening.
    - Update account at “company\_wise\_opening\_bal” at company using + amount.
- If is\_opening.
  - Set account at “opening\_balance” from (account.get(“opening\_balance”, 0.0) + amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1169)

<a id="op-44420f0282b5e1"></a>
### Currency Translator.initialize

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_init`

**Inputs** self, companies, filters, fiscal\_year.

**Local steps**

- Set self.companies from companies.
- Set self.filters from filters.
- Set tuple(self.start\_date, self.end\_date) from get\_period\_dates(fiscal\_year, filters).
- Set self.start\_date from getdate(self.start\_date).
- Set self.reserve from defaultdict(float).
- Set self.opening\_reserve from defaultdict(float).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1181)

<a id="op-7af81820bcc8ee"></a>
### Currency Translator.get column companies

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_get_column_companies`

**Inputs** self, entry.

**Declared result** list at str.

**Explicit results** list of company for company drawn from self.companies where entry.company belongs to self.get\_column\_scope(company).

**Local steps**

- Return list of company for company drawn from self.companies where entry.company belongs to self.get\_column\_scope(company).
  - Draw company from self.companies, keep a combination only if (entry.company belongs to self.get\_column\_scope(company)).

**Methods declared on this owner** [get column scope](operations-028.md#op-4af02225b0c42a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1175)

<a id="op-4af02225b0c42a"></a>
### Currency Translator.get column scope

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_get_column_scope`

**Inputs** self, company.

**Declared result** list at str.

**Explicit results** self.companies at company · list(company).

**Local steps**

- If self.filters.get(“accumulated\_in\_group\_company”).
  - Return self.companies at company.
- Return list(company).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1176)

<a id="op-3fefb7db811e53"></a>
### Currency Translator.get target currency

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_get_target_currency`

**Inputs** self, company.

**Declared result** str.

**Explicit results** (self.filters.get(“presentation\_currency”) or Enterprise.get\_company\_currency(company)).

**Local steps**

- Return (self.filters.get(“presentation\_currency”) or Enterprise.get\_company\_currency(company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“presentation\_currency”) → Enterprise.get\_company\_currency(company).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1178)

<a id="op-aa8a4ed8a22306"></a>
### Currency Translator.is opening

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_is_opening`

**Inputs** self, entry.

**Declared result** bool.

**Explicit results** entry.posting\_date &lt; self.start\_date.

**Local steps**

- Return entry.posting\_date &lt; self.start\_date.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1182)

<a id="op-1a4ad62fc6eb41"></a>
### Currency Translator.translate

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_translate`

**Inputs** self, entry, company.

**Declared result** float.

**Explicit results** amount · closing\_amount · translated\_amount.

**Local steps**

- Set amount from (flt(entry.debit) − flt(entry.credit)).
- Set currency from self.get\_target\_currency(company).
- If entry.currency equals currency.
  - Return amount.
- Set closing\_amount from convert(amount, currency, entry.currency, self.end\_date).
- If not uses\_transaction\_rate(entry).
  - Return closing\_amount.
- Set translated\_amount from self.get\_transaction\_rate\_amount(entry, currency, amount).
- Update self.reserve at company using + (closing\_amount − translated\_amount).
- If self.is\_opening(entry).
  - Update self.opening\_reserve at company using + (closing\_amount − translated\_amount).
- Return translated\_amount.

**Methods declared on this owner** [get target currency](operations-028.md#op-3fefb7db811e53), [get transaction rate amount](operations-028.md#op-1749c017eddfbe), [is opening](operations-028.md#op-aa8a4ed8a22306).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1183)

<a id="op-1749c017eddfbe"></a>
### Currency Translator.get transaction rate amount

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_get_transaction_rate_amount`

**Inputs** self, entry, currency, amount.

**Declared result** float.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** (flt(entry.debit\_in\_reporting\_currency) − flt(entry.credit\_in\_reporting\_currency)) · (amount × get\_rate\_as\_at(entry.posting\_date, entry.currency, currency)).

**Local steps**

- Set reporting\_currency from Platform.get\_cached\_value(“Company”, entry.company, “reporting\_currency”).
- If (reporting\_currency equals currency and (entry.debit\_in\_reporting\_currency or entry.credit\_in\_reporting\_currency)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reporting\_currency equals currency → (entry.debit\_in\_reporting\_currency or entry.credit\_in\_reporting\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.debit\_in\_reporting\_currency → entry.credit\_in\_reporting\_currency.
  - Return (flt(entry.debit\_in\_reporting\_currency) − flt(entry.credit\_in\_reporting\_currency)).
- Return (amount × get\_rate\_as\_at(entry.posting\_date, entry.currency, currency)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, entry.company, “reporting\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1179)

<a id="op-abea690f739cf1"></a>
### Currency Translator.add profit and loss difference

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_add_profit_and_loss_difference`

**Inputs** self.

**Local steps**

- For each company in self.get\_foreign\_companies().
  - Set from\_date from self.get\_unclosed\_from\_date(company).
  - For each entry in get\_profit\_and\_loss\_totals(company, from\_date, self.end\_date, self.filters).
    - For each column in self.get\_column\_companies(entry).
      - Evaluate self.translate(entry, column).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get foreign companies](operations-028.md#op-13caa9ceb8ea04), [get unclosed from date](operations-028.md#op-8769802271271d), [get column companies](operations-028.md#op-7af81820bcc8ee), [translate](operations-028.md#op-1a4ad62fc6eb41).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1174)

<a id="op-8769802271271d"></a>
### Currency Translator.get unclosed from date

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_get_unclosed_from_date`

**Inputs** self, company.

**Record and data access** read “Period Closing Voucher” via get\_all.

**Explicit results** add\_days(closed\_until at 0, 1) · self.start\_date.

**Local steps**

- Set closed\_until from Platform.get\_all(“Period Closing Voucher”, filters = mapping(“company” → company, “docstatus” → 1, “gle\_processing\_status” → “Completed”, “period\_end\_date” → tuple(“&lt;=”, self.end\_date)), order\_by = “period ….
- If (closed\_until and getdate(closed\_until at 0) ≥ self.start\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in closed\_until → getdate(closed\_until at 0) ≥ self.start\_date.
  - Return add\_days(closed\_until at 0, 1).
- Return self.start\_date.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1180)

<a id="op-13caa9ceb8ea04"></a>
### Currency Translator.get foreign companies

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_currencytranslator_get_foreign_companies`

**Inputs** self.

**Declared result** set at str.

**Explicit results** set of company for column drawn from self.companies, then company drawn from self.get\_column\_scope(column) where Enterprise.get\_company\_currency(company) differs from self.get\_target\_currency(column).

**Local steps**

- Return set of company for column drawn from self.companies, then company drawn from self.get\_column\_scope(column) where Enterprise.get\_company\_currency(company) differs from self.get\_target\_currency(column).
  - Draw column from self.companies.
  - Draw company from self.get\_column\_scope(column), keep a combination only if (Enterprise.get\_company\_currency(company) differs from self.get\_target\_currency(column)).

**Methods declared on this owner** [get column scope](operations-028.md#op-4af02225b0c42a), [get target currency](operations-028.md#op-3fefb7db811e53).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1177)

<a id="op-6e33b08c46e490"></a>
### Uses transaction rate

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_uses_transaction_rate`

**Inputs** entry.

**Declared result** bool.

**Explicit results** (entry.report\_type equals “Profit and Loss” or “Equity” belongs to tuple(entry.root\_type, entry.account\_type)).

**Local steps**

- Return (entry.report\_type equals “Profit and Loss” or “Equity” belongs to tuple(entry.root\_type, entry.account\_type)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.report\_type equals “Profit and Loss” → “Equity” belongs to tuple(entry.root\_type, entry.account\_type).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1191)

<a id="op-2ab1643e3c47cf"></a>
### Get profit and loss totals

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_get_profit_and_loss_totals`

**Inputs** company, from\_date, to\_date, filters.

**Declared result** list at dict.

**Explicit results** entries.

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Set account from Platform.qb.DocType(“Account”).
- Set has\_reporting\_amounts from Case().when((gle.debit\_in\_reporting\_currency differs from 0 bitwise or gle.credit\_in\_reporting\_currency differs from 0), 1).else\_(0).
- Set entries from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.all(nested operand in the contract(nested operand in the contract, nested operand in the contract, nested ….
- Set currency from Enterprise.get\_company\_currency(company).
- For each entry in entries.
  - Evaluate entry.update(currency = currency, report\_type = “Profit and Loss”).
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1187)

<a id="op-5e0670c9c28bdc"></a>
### Add translation reserve account

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_add_translation_reserve_account`

**Inputs** accounts, translator.

**State and service calls** call insert on accounts.

**Explicit results** no value.

**Local steps**

- If not any(generator of flt(amount, 3) for amount drawn from translator.reserve.values()).
  - Draw amount from translator.reserve.values().
  - Return no value.
- Set root from accounts at 0.
- Set label from translated “Foreign Currency Translation Reserve”.
- Set reserve from Platform.\_dict(translator.reserve, name = label, account\_name = label, account\_key = label, parent\_account = root.name, …).
- Evaluate accounts.insert(1, reserve).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1170)

<a id="op-9d46c1d4f1098f"></a>
### Accumulate values into parents

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_accumulate_values_into_parents`

**Inputs** accounts, accounts\_by\_name, companies.

**Local steps**

- For each d in reversed(accounts).
  - If d.parent\_account.
    - Set account from d.parent\_account\_name.
    - For each company in companies.
      - Set accounts\_by\_name at account at company from (accounts\_by\_name at account.get(company, 0.0) + d.get(company, 0.0)).
      - Update accounts\_by\_name at account at “company\_wise\_opening\_bal” at company using + d.get(“company\_wise\_opening\_bal”, mapping()).get(company, 0.0).
    - Set accounts\_by\_name at account at “opening\_balance” from (accounts\_by\_name at account.get(“opening\_balance”, 0.0) + d.get(“opening\_balance”, 0.0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L2193) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L758)

<a id="op-6d52d3a833d9aa"></a>
### Get account heads

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_account_heads`

**Inputs** root\_type, companies, filters.

**Explicit results** tuple(no value, no value, no value) · tuple(accounts, accounts\_by\_name, parent\_children\_map).

**Local steps**

- Set accounts from get\_accounts(root\_type, companies).
- If not accounts.
  - Return tuple(no value, no value, no value).
- Set accounts from update\_parent\_account\_names(accounts).
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Return tuple(accounts, accounts\_by\_name, parent\_children\_map).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L2544) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L765)

<a id="op-35dd24e8db4530"></a>
### Update parent account names

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_update_parent_account_names`

**Inputs** accounts.

**Explicit results** accounts.

**Local steps**

- Set name\_to\_account\_map from mapping().
- For each d in accounts.
  - If d.account\_number.
    - Set account\_key from ((d.account\_number + “ - ”) + d.account\_name).
  - Otherwise.
    - Set account\_key from d.account\_name.
  - Set d.account\_key from account\_key.
  - Set name\_to\_account\_map at d.name from account\_key.
- For each account in accounts.
  - If account.parent\_account.
    - Set account at “parent\_account\_name” from name\_to\_account\_map.get(account.parent\_account).
- Return accounts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L2738) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L784)

<a id="op-036c87e3890d3f"></a>
### Get companies

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_companies`

**Inputs** filters.

**Explicit results** tuple(all\_companies, companies).

**Local steps**

- Set companies from mapping().
- Set all\_companies from get\_subsidiary\_companies(filters.get(“company”)).
- Evaluate companies.setdefault(filters.get(“company”), all\_companies).
- For each d in all\_companies.
  - If d does not belong to companies.
    - Set subsidiary\_companies from get\_subsidiary\_companies(d).
    - Evaluate companies.setdefault(d, subsidiary\_companies).
- Return tuple(all\_companies, companies).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L2985) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L772)
