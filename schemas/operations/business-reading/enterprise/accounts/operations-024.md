# Accounting and settlement · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Calculated discount mismatch

<a id="op-55f0a713d69a6d"></a>
### Get data

`operation_enterprise_accounts_report_calculated_discount_mismatch_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** list() · data.

**Local steps**

- Set transactions\_with\_discount\_percentage from mapping().
- For each doctype in AFFECTED\_DOCTYPES.
  - Set transactions from get\_transactions\_with\_discount\_percentage(doctype).
  - For each transaction in transactions.
    - Set transactions\_with\_discount\_percentage at tuple(doctype, transaction.name) from transaction.
- If not transactions\_with\_discount\_percentage.
  - Return list().
- Set VERSION from Platform.qb.DocType(“Version”).
- Set versions from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise or nested operand in the contract(nested operand in the contract ….
- If not versions.
  - Return list().
- Set version\_map from mapping().
- For each version in versions.
  - Set key from tuple(version.ref\_doctype, version.docname).
  - If key does not belong to version\_map.
    - Set version\_map at key from list().
  - Evaluate version\_map at key.append(version.data).
- Set data from list().
- Set discount\_amount\_field\_map from mapping of doctype → Platform.get\_meta(doctype).get\_field(“discount\_amount”) for doctype drawn from AFFECTED\_DOCTYPES.
  - Draw doctype from AFFECTED\_DOCTYPES.
- For each tuple(doc, versions) in version\_map.items().
  - For each version\_data in versions.
    - If “"additional\_discount\_percentage"” belongs to version\_data.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Set version\_data from json.loads(version\_data).
    - Set changed\_values from version\_data.get(“changed”).
    - If not changed\_values.
      - Continue with the next iteration or loop test.
    - Set discount\_values from next(generator of row for row drawn from changed\_values where row at 0 equals “discount\_amount”, no value).
      - Draw row from changed\_values, keep a combination only if (row at 0 equals “discount\_amount”).
    - If not discount\_values.
      - Continue with the next iteration or loop test.
    - Set old from discount\_values at 1.
    - Set new from discount\_values at 2.
    - Set doctype from doc at 0.
    - Set doc\_values from transactions\_with\_discount\_percentage.get(doc).
    - Set formatted\_discount\_amount from format\_value(doc\_values.discount\_amount, df = discount\_amount\_field\_map at doctype, currency = doc\_values.currency).
    - If new differs from formatted\_discount\_amount.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Evaluate data.append(mapping(“doctype” → doctype, “docname” → doc\_values.name, “actual\_discount\_percentage” → doc\_values.additional\_discount\_percentage, “actual\_discount\_amount” → doc\_values.discount\_amount, …)).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L729)

<a id="op-b9f2ea78eeab71"></a>
### Get transactions with discount percentage

`operation_enterprise_accounts_report_calculated_discount_mismatch_business_behavior_get_transactions_with_discount_percentage`

**Inputs** doctype.

**Record and data access** read doctype via get\_list.

**Explicit results** list() · transactions.

**Local steps**

- If not Platform.has\_permission(doctype).
  - Return list().
- Set transactions from Platform.get\_list(doctype, fields = list(“name”, “currency”, “additional\_discount\_percentage”, “discount\_amount”), filters = mapping(“docstatus” → list(“&lt;”, 2), “additional\_discount\_percentage” → list(“&gt;”, ….
- Return transactions.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L730)

<a id="op-4f8f80c253c1e6"></a>
### Parse formatted amount

`operation_enterprise_binding_enterprise_accounts_report_calculated_discount_mismatch_calculated_discount_mismatch_parse_formatted_amount`

**Inputs** value, currency.

**Declared result** float.

**Record and data access** read “Currency” via get\_value.

**Explicit results** flt(value) · flt(amount).

**Local steps**

- If not isinstance(value, str).
  - Return flt(value).
- Set number\_format from get\_number\_format().
- Set symbol from (Platform.db.get\_value(“Currency”, currency, “symbol”, cache = true) or currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Currency”, currency, “symbol”, cache = true) → currency.
- Set amount from value.replace(translated symbol, empty text).strip().replace(number\_format.thousands\_separator, empty text).
- If number\_format.decimal\_separator.
  - Set amount from amount.replace(number\_format.decimal\_separator, “.”).
- Return flt(amount).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1138)

## Report · Cash flow

<a id="op-3ffd75a7621fe3"></a>
### Execute

`operation_enterprise_accounts_report_cash_flow_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** msgprint.

**Explicit results** FinancialReportEngine().execute(filters) · no value · tuple(columns, data, no value, chart, …).

**Local steps**

- If (filters and filters.report\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.report\_template.
  - Return FinancialReportEngine().execute(filters).
- Set period\_list from build\_period\_list(filters, accumulated\_values = bool(filters.accumulated\_values)).
- If not period\_list.
  - Return no value.
- Set cash\_flow\_sections from get\_cash\_flow\_accounts().
- Set income from get\_data(filters.company, “Income”, “Credit”, period\_list, filters = filters, accumulated\_values = filters.accumulated\_values, ignore\_closing\_entries = true, ignore\_accumulated\_values\_for\_fy = true).
- Set expense from get\_data(filters.company, “Expense”, “Debit”, period\_list, filters = filters, accumulated\_values = filters.accumulated\_values, ignore\_closing\_entries = true, ignore\_accumulated\_values\_for\_fy = true).
- Set net\_profit\_loss from get\_net\_profit\_loss(income, expense, period\_list, filters.company, accumulated\_values = bool(filters.accumulated\_values)).
- If net\_profit\_loss.
  - Set total\_keys from get\_total\_keys(period\_list, filters.accumulated\_values, filters.company).
  - Set net\_profit\_loss at “total” from sum(generator of net\_profit\_loss at key for key drawn from total\_keys).
    - Draw key from total\_keys.
- Set data from list().
- Set summary\_data from mapping().
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- For each cash\_flow\_section in cash\_flow\_sections.
  - Set section\_data from list().
  - Evaluate data.append(mapping(“section\_name” → ((“'” + cash\_flow\_section at “section\_header”) + “'”), “parent\_section” → no value, “indent” → 0.0, “section” → cash\_flow\_section at “section\_header”, …)).
  - If len(data) equals 1.
    - If net\_profit\_loss.
      - Evaluate net\_profit\_loss.update(mapping(“indent” → 1, “parent\_section” → cash\_flow\_sections at 0 at “section\_header”, “section” → net\_profit\_loss at “account”)).
      - Evaluate data.append(net\_profit\_loss).
      - Evaluate section\_data.append(net\_profit\_loss).
  - For each row in cash\_flow\_section at “account\_types”.
    - Set row\_data from get\_account\_type\_based\_data(filters.company, row at “account\_type”, period\_list, filters.accumulated\_values, …).
    - Set accounts from get\_row\_accounts(filters.company, row at “account\_type”).
    - Evaluate row\_data.update(mapping(“section\_name” → row at “label”, “section” → row at “label”, “indent” → 1, “accounts” → accounts, …)).
    - Evaluate data.append(row\_data).
    - Evaluate section\_data.append(row\_data).
  - Evaluate add\_total\_row\_account(data, section\_data, cash\_flow\_section at “section\_footer”, period\_list, …).
- Set net\_change\_in\_cash from add\_total\_row\_account(data, data, translated “Net Change in Cash”, period\_list, add\_blank\_row = false, …).
- If (filters.show\_opening\_and\_closing\_balance and not is\_dimension\_grouped(period\_list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.show\_opening\_and\_closing\_balance → not is\_dimension\_grouped(period\_list).
  - Evaluate show\_opening\_and\_closing\_balance(data, period\_list, company\_currency, net\_change\_in\_cash, …).
- Otherwise.
  - If filters.show\_opening\_and\_closing\_balance.
    - Set filters.show\_opening\_and\_closing\_balance from false.
    - Evaluate Platform.msgprint(indicator = “orange”, title = translated “Not Supported”, msg = translated “Opening and Closing balance is not supported for dimension grouped cash flow statement”).
- Set columns from get\_columns(filters.periodicity, period\_list, filters.accumulated\_values, filters.company, …).
- Set chart from get\_chart\_data(period\_list, data, company\_currency).
- Set report\_summary from get\_report\_summary(summary\_data, company\_currency).
- Return tuple(columns, data, no value, chart, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L737)

<a id="op-5efd3e98ca91a3"></a>
### Get cash flow accounts

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_cash_flow_accounts`

**Inputs** no declared parameters.

**Explicit results** list(operation\_accounts, investing\_accounts, financing\_accounts).

**Local steps**

- Set operation\_accounts from mapping(“section\_name” → “Operations”, “section\_footer” → translated “Net Cash from Operations”, “section\_header” → translated “Cash Flow from Operations”, “account\_types” → list(mapping(“account\_type” → “ ….
- Set investing\_accounts from mapping(“section\_name” → “Investing”, “section\_footer” → translated “Net Cash from Investing”, “section\_header” → translated “Cash Flow from Investing”, “account\_types” → list(mapping(“account\_type” → “Fix ….
- Set financing\_accounts from mapping(“section\_name” → “Financing”, “section\_footer” → translated “Net Cash from Financing”, “section\_header” → translated “Cash Flow from Financing”, “account\_types” → list(mapping(“account\_type” → “Equ ….
- Return list(operation\_accounts, investing\_accounts, financing\_accounts).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L740)

<a id="op-78116faa18d7ad"></a>
### Get row accounts

`operation_enterprise_binding_enterprise_accounts_report_cash_flow_cash_flow_get_row_accounts`

**Inputs** company, account\_type.

**Declared result** list at str.

**Explicit results** get\_row\_accounts\_query(account, company, account\_type).run(pluck = true).

**Local steps**

- Set account from Platform.qb.DocType(“Account”).
- Return get\_row\_accounts\_query(account, company, account\_type).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1142)

<a id="op-61b5243ae83ff1"></a>
### Get row accounts query

`operation_enterprise_binding_enterprise_accounts_report_cash_flow_cash_flow_get_row_accounts_query`

**Inputs** account, company, account\_type.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_group equals 0).where(account.company equals company).where(get\_row\_account\_condition(account, account\_type)).

**Local steps**

- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_group equals 0).where(account.company equals company).where(get\_row\_account\_condition(account, account\_type)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1143)

<a id="op-a1705c38e551c1"></a>
### Get row account condition

`operation_enterprise_binding_enterprise_accounts_report_cash_flow_cash_flow_get_row_account_condition`

**Inputs** account, account\_type.

**Explicit results** account.account\_type equals account\_type · (other\_balance\_sheet\_accounts bitwise or account.account\_type equals “Depreciation”).

**Local steps**

- If account\_type differs from OTHER\_BALANCE\_SHEET\_ACCOUNTS.
  - Return account.account\_type equals account\_type.
- Set excluded\_types from list(expanded get\_mapped\_account\_types(), “Cash”, “Bank”).
- Set other\_balance\_sheet\_accounts from (account.root\_type.isin(list(“Asset”, “Liability”, “Equity”)) bitwise and IfNull(account.account\_type, empty text).notin(excluded\_types)).
- Return (other\_balance\_sheet\_accounts bitwise or account.account\_type equals “Depreciation”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1141)

<a id="op-3d06414b250eb0"></a>
### Get mapped account types

`operation_enterprise_binding_enterprise_accounts_report_cash_flow_cash_flow_get_mapped_account_types`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list of row at “account\_type” for section drawn from get\_cash\_flow\_accounts(), then row drawn from section at “account\_types” where row at “account\_type” differs from OTHER\_BALANCE\_SHEET\_ACCOUNTS.

**Local steps**

- Return list of row at “account\_type” for section drawn from get\_cash\_flow\_accounts(), then row drawn from section at “account\_types” where row at “account\_type” differs from OTHER\_BALANCE\_SHEET\_ACCOUNTS.
  - Draw section from get\_cash\_flow\_accounts().
  - Draw row from section at “account\_types”, keep a combination only if (row at “account\_type” differs from OTHER\_BALANCE\_SHEET\_ACCOUNTS).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1140)

<a id="op-d9e045372f865b"></a>
### Get account type based data

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_account_type_based_data`

**Inputs** company, account\_type, period\_list, accumulated\_values, filters.

**Explicit results** data.

**Local steps**

- Set data from mapping().
- For each period in period\_list.
  - Set start\_date from get\_start\_date(period, accumulated\_values, company).
  - Set filters.start\_date from start\_date.
  - Set filters.end\_date from period at “to\_date”.
  - Set filters.account\_type from account\_type.
  - Set filters.dimension\_field from period.get(“dimension\_field”).
  - Set filters.dimension\_value from period.get(“dimension\_value”).
  - Set amount from get\_account\_type\_based\_gl\_data(company, filters).
  - If (amount and account\_type equals “Depreciation”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in amount → account\_type equals “Depreciation”.
    - Update amount using × negative 1.
  - Evaluate data.setdefault(period at “key”, amount).
- Set data at “total” from sum(generator of data at key for key drawn from get\_total\_keys(period\_list, accumulated\_values, company)).
  - Draw key from get\_total\_keys(period\_list, accumulated\_values, company).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L738)

<a id="op-85fbf274ea033c"></a>
### Get total keys

`operation_enterprise_binding_enterprise_accounts_report_cash_flow_cash_flow_get_total_keys`

**Inputs** period\_list, accumulated\_values, company, consolidated = false.

**Declared result** list at str.

**Explicit results** get\_period\_keys\_for\_total(period\_list, accumulated\_values, consolidated) · list(last\_keys.values()).

**Local steps**

- If (consolidated or not accumulated\_values).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in consolidated → not accumulated\_values.
  - Return get\_period\_keys\_for\_total(period\_list, accumulated\_values, consolidated).
- Set last\_keys from mapping().
- For each period in period\_list.
  - Set fiscal\_year from get\_fiscal\_year(period.to\_date, company = company) at 0.
  - Set last\_keys at tuple(period.get(“dimension\_value”), fiscal\_year) from period.key.
- Return list(last\_keys.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1144)

<a id="op-d5ccac5e039817"></a>
### Get account type based gl data

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_account_type_based_general_ledger_data`

**Inputs** company, filters = no value.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** flt(result at 0 at 0) when (result and result at 0 at 0), otherwise 0.

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set gl from Platform.qb.DocType(“GL Entry”).
- Set acc from Platform.qb.DocType(“Account”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.posting\_date ≤ nested operand in the contract.end\_date).where(gl.voucher\_type differs from “Period Closin ….
- If not Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
  - Set query from query.where(gl.is\_opening differs from “Yes”).
- Set query from apply\_gl\_filters(query, gl, company, filters).
- Set result from query.run().
- Return flt(result at 0 at 0) when (result and result at 0 at 0), otherwise 0.
  - Value choice on (result and result at 0 at 0) — true gives flt(result at 0 at 0), false gives 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in result → result at 0 at 0.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L739)

<a id="op-e874acb4e90ede"></a>
### Apply gl filters

`operation_enterprise_binding_enterprise_accounts_report_cash_flow_cash_flow_apply_gl_filters`

**Inputs** query, gl, company, filters.

**Record and data access** read “Company” via get\_cached\_value · read “DocType” via get\_cached\_value.

**Explicit results** query.

**Local steps**

- If filters.include\_default\_book\_entries.
  - Set company\_fb from Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).
  - Set query from query.where((gl.finance\_book.isin(list(cstr(filters.finance\_book), cstr(company\_fb), empty text)) bitwise or gl.finance\_book.isnull())).
- Otherwise.
  - Set query from query.where((gl.finance\_book.isin(list(cstr(filters.finance\_book), empty text)) bitwise or gl.finance\_book.isnull())).
- If filters.get(“cost\_center”).
  - Set cost\_centers from get\_cost\_centers\_with\_children(filters.cost\_center).
  - Set query from query.where(gl.cost\_center.isin(cost\_centers)).
- If filters.get(“project”).
  - Set projects from filters.project.
  - If not isinstance(projects, list).
    - Set projects from Platform.parse\_json(projects).
  - Set query from query.where(gl.project.isin(projects)).
- If (filters.get(“dimension\_field”) and filters.get(“dimension\_value”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“dimension\_field”) → filters.get(“dimension\_value”).
  - Set query from query.where(gl at filters.dimension\_field equals filters.dimension\_value).
- For each dimension in get\_accounting\_dimensions(as\_list = false).
  - If filters.get(dimension.fieldname).
    - Set values from filters at dimension.fieldname.
    - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
      - Set values from get\_dimension\_with\_children(dimension.document\_type, values).
    - Set query from query.where(gl at dimension.fieldname.isin(values)).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(“GL Entry”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”), Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1139)

<a id="op-deeeb6ed133d65"></a>
### Get start date

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_start_date`

**Inputs** period, accumulated\_values, company.

**Explicit results** period at “from\_date” · start\_date.

**Local steps**

- If (not accumulated\_values and period.get(“from\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not accumulated\_values → period.get(“from\_date”).
  - Return period at “from\_date”.
- Set start\_date from period at “year\_start\_date”.
- If accumulated\_values.
  - Set start\_date from max(start\_date, get\_fiscal\_year(period.to\_date, company = company) at 1).
- Return start\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L744)

<a id="op-66e506dc6e2a40"></a>
### Add total row account

`operation_enterprise_accounts_report_cash_flow_business_behavior_add_total_row_account`

**Inputs** out, data, label, period\_list, currency, summary\_data, filters, consolidated = false, add\_blank\_row = true.

**Explicit results** total\_row.

**Local steps**

- Set name\_key from “account” when consolidated, otherwise “section”.
  - Value choice on consolidated — true gives “account”, false gives “section”.
- Set parent\_key from “parent\_account” when consolidated, otherwise “parent\_section”.
  - Value choice on consolidated — true gives “parent\_account”, false gives “parent\_section”.
- Set label\_str from ((“'” + str(label)) + “'”).
- Set total\_row from mapping(formatted text {name\_key}\_name → label\_str, name\_key → label\_str, “currency” → currency).
- If filters.get(“accumulated\_in\_group\_company”).
  - Set period\_list from get\_filtered\_list\_for\_consolidated\_report(filters, period\_list).
- For each row in data.
  - If row.get(parent\_key).
    - For each period in period\_list.
      - Set key from period when consolidated, otherwise period at “key”.
        - Value choice on consolidated — true gives period, false gives period at “key”.
      - Evaluate total\_row.setdefault(key, 0.0).
      - Update total\_row at key using + row.get(key, 0.0).
    - Evaluate total\_row.setdefault(“total”, 0.0).
    - Update total\_row at “total” using + row.get(“total”, 0.0).
- Set summary\_keys from get\_total\_keys(period\_list, filters.get(“accumulated\_values”), filters.company, consolidated).
- Set summary\_data at label from sum(generator of flt(total\_row.get(key)) for key drawn from summary\_keys).
  - Draw key from summary\_keys.
- Evaluate out.append(total\_row).
- If add\_blank\_row.
  - Evaluate out.append(mapping()).
- Return total\_row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L736)

<a id="op-d1cbe6572fcb52"></a>
### Show opening and closing balance

`operation_enterprise_accounts_report_cash_flow_business_behavior_show_opening_and_closing_balance`

**Inputs** out, period\_list, currency, net\_change\_in\_cash, filters.

**Local steps**

- Set opening\_balance from mapping(“section\_name” → “Opening”, “section” → “Opening”, “currency” → currency).
- Set closing\_balance from mapping(“section\_name” → “Closing (Opening + Total)”, “section” → “Closing (Opening + Total)”, “currency” → currency).
- Set opening, closing from (get\_opening\_balance(filters.company, period\_list, filters) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_opening\_balance(filters.company, period\_list, filters) → 0.0.
- Set movement\_start\_date from no value.
- For each period in period\_list.
  - Set key from period at “key”.
  - Set start\_date from get\_start\_date(period, filters.accumulated\_values, filters.company).
  - If start\_date differs from movement\_start\_date.
    - Set opening from closing.
    - Set movement\_start\_date from start\_date.
  - Set opening\_balance at key from opening.
  - Set closing from (opening + net\_change\_in\_cash.get(key, 0.0)).
  - Set closing\_balance at key from closing.
- Set opening\_balance at “total” from opening\_balance at period\_list at 0 at “key”.
- Set closing\_balance at “total” from closing\_balance at period\_list at negative 1 at “key”.
- Evaluate out.extend(list(opening\_balance, net\_change\_in\_cash, closing\_balance, mapping())).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L745)

<a id="op-857d32bc003f32"></a>
### Get opening balance

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_opening_balance`

**Inputs** company, period\_list, filters.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** flt(result at 0 at 0) when result, otherwise 0.0.

**Local steps**

- Set gl from Platform.qb.DocType(“GL Entry”).
- Set account from Platform.qb.DocType(“Account”).
- Set cash\_accounts from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals company).where(account.is\_group equals 0).where(account.account\_type.isin(list(“Cash”, “Bank”))).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals company).where(gl.is\_cancelled equals 0).where(gl.account.isin(cash\_accounts)).
- Set before\_first\_period from gl.posting\_date &lt; period\_list at 0 at “from\_date”.
- If Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
  - Set query from query.where(before\_first\_period).
- Otherwise.
  - Set query from query.where((before\_first\_period bitwise or gl.is\_opening equals “Yes”)).
- Set query from apply\_gl\_filters(query, gl, company, filters).
- Set result from query.run().
- Return flt(result at 0 at 0) when result, otherwise 0.0.
  - Value choice on result — true gives flt(result at 0 at 0), false gives 0.0.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L742)

<a id="op-8eeefbda445afe"></a>
### Get report summary

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_report_summary`

**Inputs** summary\_data, currency.

**Explicit results** report\_summary.

**Local steps**

- Set report\_summary from list().
- For each tuple(label, value) in summary\_data.items().
  - Evaluate report\_summary.append(mapping(“value” → value, “label” → label, “datatype” → “Currency”, “currency” → currency)).
- Return report\_summary.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0235.json#L4758) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L743)

<a id="op-97ea48d1aaf00c"></a>
### Get chart data

`operation_enterprise_accounts_report_cash_flow_business_behavior_get_chart_data`

**Inputs** period\_list, data, currency.

**Explicit results** chart.

**Local steps**

- Set labels from list of period.get(“label”) for period drawn from period\_list.
  - Draw period from period\_list.
- Set datasets from list of mapping(“name” → section.get(“section”).replace(“'”, empty text), “values” → list of section.get(period.get(“key”)) for period drawn from period\_list) for section drawn from data where (section.get ….
  - Draw section from data, keep a combination only if ((section.get(“parent\_section”) is identical to no value and section.get(“currency”))).
  - Draw period from period\_list.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“parent\_section”) is identical to no value → section.get(“currency”).
- Set datasets from datasets at slice no value to negative 2.
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “bar”).
- Set chart at “fieldtype” from “Currency”.
- Set chart at “options” from “currency”.
- Set chart at “currency” from currency.
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0235.json#L4939) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L741)

## Record · Cashier closing

[Record definition](../../../../data/record-types/cashier_closing.json)

<a id="op-a5367acc767aa4"></a>
### Cashier Closing.validate

`operation_enterprise_accounts_record_definitions_cashier_closing_business_behavior_cashier_closing_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_time().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate time](operations-024.md#op-63aa8873094826).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0035.json#L7475) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L630)

<a id="op-e930f52304a2f2"></a>
### Cashier Closing.before save

`operation_enterprise_accounts_record_definitions_cashier_closing_business_behavior_cashier_closing_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.get\_outstanding().
- Evaluate self.make\_calculations().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get outstanding](operations-024.md#op-6fed6aec155947), [make calculations](operations-024.md#op-d6cf0548e7e01e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0035.json#L7526) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L627)

<a id="op-6fed6aec155947"></a>
### Cashier Closing.get outstanding

`operation_enterprise_accounts_record_definitions_cashier_closing_business_behavior_cashier_closing_get_outstanding`

**Inputs** self.

**Record and data access** execute query text (SELECT, Sales Invoice).

**Local steps**

- Set values from Platform.db.sql(query text (SELECT, Sales Invoice), tuple(self.date, self.from\_time, self.time, self.user)).
- Set self.outstanding\_amount from flt(values at 0 at 0 when values, otherwise 0).
  - Value choice on values — true gives values at 0 at 0, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L628)

<a id="op-d6cf0548e7e01e"></a>
### Cashier Closing.make calculations

`operation_enterprise_accounts_record_definitions_cashier_closing_business_behavior_cashier_closing_make_calculations`

**Inputs** self.

**Local steps**

- Set total from 0.0.
- For each i in self.payments.
  - Update total using + flt(i.amount).
- Set self.net\_amount from ((((total + self.outstanding\_amount) + flt(self.expense)) − flt(self.custody)) + flt(self.returns)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0036.json#L325) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L629)

<a id="op-63aa8873094826"></a>
### Cashier Closing.validate time

`operation_enterprise_accounts_record_definitions_cashier_closing_business_behavior_cashier_closing_validate_time`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Time Should Be Less Than To Time”.

**Local steps**

- If self.from\_time ≥ self.time.
  - Call the validation error handler Platform.throw(translated “From Time Should Be Less Than To Time”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0036.json#L514) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L631)
