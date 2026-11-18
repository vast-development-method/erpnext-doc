# Accounting and settlement · operations 117

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Trial balance

<a id="op-e6c120f6b247cc"></a>
### Get rootwise opening balances

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_rootwise_opening_balances`

**Inputs** filters, report\_type, ignore\_is\_opening, exchange\_rate = no value, ignore\_reporting\_currency = true.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Period Closing Voucher” via get\_all.

**Explicit results** opening.

**Local steps**

- Set gle from list().
- Set last\_period\_closing\_voucher from empty text.
- Set ignore\_closing\_balances from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).
- Set ignore\_closing\_balances from (ignore\_closing\_balances or has\_gl\_entry\_restrictions()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_closing\_balances → has\_gl\_entry\_restrictions().
- If not ignore\_closing\_balances.
  - Set last\_period\_closing\_voucher from Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“docstatus” → 1, “company” → filters.company, “period\_end\_date” → tuple(“&lt;”, filters.from\_date)), fields = list(“period\_end\_date”, “name”), o ….
- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- If last\_period\_closing\_voucher.
  - Set gle from get\_opening\_balance(“Account Closing Balance”, filters, report\_type, accounting\_dimensions, period\_closing\_voucher = last\_period\_closing\_voucher at 0.name, ignore\_is\_opening = ignore\_is\_opening, ignore\_rep ….
  - If getdate(last\_period\_closing\_voucher at 0.period\_end\_date) &lt; getdate(add\_days(filters.from\_date, negative 1)).
    - Set start\_date from add\_days(last\_period\_closing\_voucher at 0.period\_end\_date, 1).
    - Update gle using + get\_opening\_balance(“GL Entry”, filters, report\_type, accounting\_dimensions, start\_date = start\_date, ignore\_is\_opening = ignore\_is\_opening, ignore\_reporting\_currency = ignore\_reporting\_currency).
- Otherwise.
  - Set gle from get\_opening\_balance(“GL Entry”, filters, report\_type, accounting\_dimensions, ignore\_is\_opening = ignore\_is\_opening, ignore\_reporting\_currency = ignore\_reporting\_currency).
- Set opening from Platform.\_dict().
- Set equity\_accounts from get\_equity\_accounts(filters.company) when not ignore\_reporting\_currency, otherwise set().
  - Value choice on not ignore\_reporting\_currency — true gives get\_equity\_accounts(filters.company), false gives set().
- For each d in gle.
  - Set opening\_dr\_cr from mapping(“account” → d.account, “opening\_debit” → 0.0, “opening\_credit” → 0.0).
  - Evaluate opening.setdefault(d.account, opening\_dr\_cr).
  - If ignore\_reporting\_currency.
    - Update opening at d.account at “opening\_debit” using + flt(d.debit).
    - Update opening at d.account at “opening\_credit” using + flt(d.credit).
  - Otherwise.
    - If (report\_type equals “Balance Sheet” and d.account does not belong to equity\_accounts).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_type equals “Balance Sheet” → d.account does not belong to equity\_accounts.
      - Update opening at d.account at “opening\_debit” using + (flt(d.debit) × flt(exchange\_rate)).
      - Update opening at d.account at “opening\_credit” using + (flt(d.credit) × flt(exchange\_rate)).
    - Otherwise.
      - Update opening at d.account at “opening\_debit” using + flt(d.debit\_in\_reporting\_currency).
      - Update opening at d.account at “opening\_credit” using + flt(d.credit\_in\_reporting\_currency).
- Return opening.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L107)

<a id="op-a6d1b59e450862"></a>
### Get equity accounts

`operation_enterprise_binding_enterprise_accounts_report_trial_balance_trial_balance_get_equity_accounts`

**Inputs** company.

**Declared result** set at str.

**Explicit results** set(nested operand in the contract.select(nested operand in the contract.name).where((nested operand in the contract.company equals company bitwise and (nested operand in the contract equals nested operand in  …).

**Local steps**

- Set account from Platform.qb.DocType(“Account”).
- Return set(nested operand in the contract.select(nested operand in the contract.name).where((nested operand in the contract.company equals company bitwise and (nested operand in the contract equals nested operand in  …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1276)

<a id="op-9130624f176887"></a>
### Get opening balance

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_opening_balance`

**Inputs** doctype, filters, report\_type, accounting\_dimensions, period\_closing\_voucher = no value, start\_date = no value, ignore\_is\_opening = 0, ignore\_reporting\_currency = true.

**Record and data access** read “Account” via get\_all · read “Finance Book” via count · read “Company” via get\_cached\_value · read “DocType” via get\_cached\_value.

**Explicit results** gle.

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set closing\_balance from Platform.qb.DocType(doctype).
- Set accounts from Platform.db.get\_all(“Account”, filters = mapping(“report\_type” → report\_type), pluck = “name”).
- Set opening\_balance from nested operand in the contract(nested operand in the contract).select(closing\_balance.account, closing\_balance.account\_currency, nested operand in the contract.as\_(“debit”), nested operand in the contract. ….
- If not ignore\_reporting\_currency.
  - Set opening\_balance from opening\_balance.select(Sum(closing\_balance.debit\_in\_reporting\_currency).as\_(“debit\_in\_reporting\_currency”), Sum(closing\_balance.credit\_in\_reporting\_currency).as\_(“credit\_in\_reporting\_currency”)).
- If period\_closing\_voucher.
  - Set opening\_balance from opening\_balance.where(closing\_balance.period\_closing\_voucher equals period\_closing\_voucher).
- Otherwise.
  - If start\_date.
    - Set opening\_balance from opening\_balance.where((closing\_balance.posting\_date ≥ start\_date bitwise and closing\_balance.posting\_date &lt; filters.from\_date)).
    - If not ignore\_is\_opening.
      - Set opening\_balance from opening\_balance.where(closing\_balance.is\_opening equals “No”).
  - Otherwise.
    - If not ignore\_is\_opening.
      - Set opening\_balance from opening\_balance.where((closing\_balance.posting\_date &lt; filters.from\_date bitwise or closing\_balance.is\_opening equals “Yes”)).
    - Otherwise.
      - Set opening\_balance from opening\_balance.where(closing\_balance.posting\_date &lt; filters.from\_date).
- If doctype equals “GL Entry”.
  - Set opening\_balance from opening\_balance.where(closing\_balance.is\_cancelled equals 0).
- If (not filters.show\_unclosed\_fy\_pl\_balances and report\_type equals “Profit and Loss” and doctype equals “GL Entry”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.show\_unclosed\_fy\_pl\_balances → report\_type equals “Profit and Loss” → doctype equals “GL Entry”.
  - Set opening\_balance from opening\_balance.where(closing\_balance.posting\_date ≥ filters.year\_start\_date).
- If not flt(filters.with\_period\_closing\_entry\_for\_opening).
  - If doctype equals “Account Closing Balance”.
    - Set opening\_balance from opening\_balance.where(closing\_balance.is\_period\_closing\_voucher\_entry equals 0).
  - Otherwise.
    - Set opening\_balance from opening\_balance.where(closing\_balance.voucher\_type differs from “Period Closing Voucher”).
- If filters.cost\_center.
  - Set opening\_balance from opening\_balance.where(closing\_balance.cost\_center.isin(get\_cost\_centers\_with\_children(filters.get(“cost\_center”)))).
- If filters.project.
  - Set opening\_balance from opening\_balance.where(closing\_balance.project.isin(filters.project)).
- If Platform.db.count(“Finance Book”).
  - If filters.get(“include\_default\_book\_entries”).
    - Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
    - If (filters.finance\_book and company\_fb and cstr(filters.finance\_book) differs from cstr(company\_fb)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.finance\_book → company\_fb → cstr(filters.finance\_book) differs from cstr(company\_fb).
      - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
    - Set opening\_balance from opening\_balance.where((closing\_balance.finance\_book.isin(list(cstr(filters.finance\_book), cstr(company\_fb), empty text)) bitwise or closing\_balance.finance\_book.isnull())).
  - Otherwise.
    - Set opening\_balance from opening\_balance.where((closing\_balance.finance\_book.isin(list(cstr(filters.finance\_book), empty text)) bitwise or closing\_balance.finance\_book.isnull())).
- If accounting\_dimensions.
  - For each dimension in accounting\_dimensions.
    - If filters.get(dimension.fieldname).
      - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
        - Set filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, filters.get(dimension.fieldname)).
        - Set opening\_balance from opening\_balance.where(closing\_balance at dimension.fieldname.isin(filters at dimension.fieldname)).
      - Otherwise.
        - Set opening\_balance from opening\_balance.where(closing\_balance at dimension.fieldname.isin(filters at dimension.fieldname)).
- If match\_conditions bound to build\_match\_conditions(doctype).
  - Set opening\_balance from opening\_balance.where(Bracket(LiteralValue(match\_conditions))).
- Set gle from opening\_balance.run(as\_dict = 1).
- If (filters and filters.get(“presentation\_currency”) and ignore\_reporting\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“presentation\_currency”) → ignore\_reporting\_currency.
  - Evaluate convert\_to\_presentation\_currency(gle, get\_currency(filters)).
- Return gle.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”), Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L103)

<a id="op-3a88279b52dba1"></a>
### Calculate values

`operation_enterprise_accounts_report_trial_balance_business_behavior_calculate_values`

**Inputs** accounts, gl\_entries\_by\_account, opening\_balances, show\_net\_values, ignore\_is\_opening = 0, exchange\_rate = no value, ignore\_reporting\_currency = true.

**Local steps**

- Set init from mapping(“opening\_debit” → 0.0, “opening\_credit” → 0.0, “debit” → 0.0, “credit” → 0.0, …).
- For each d in accounts.
  - Evaluate d.update(init.copy()).
  - Set d at “opening\_debit” from opening\_balances.get(d.name, mapping()).get(“opening\_debit”, 0).
  - Set d at “opening\_credit” from opening\_balances.get(d.name, mapping()).get(“opening\_credit”, 0).
  - For each entry in gl\_entries\_by\_account.get(d.name, list()).
    - If (cstr(entry.is\_opening) differs from “Yes” or ignore\_is\_opening).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(entry.is\_opening) differs from “Yes” → ignore\_is\_opening.
      - If ignore\_reporting\_currency.
        - Update d at “debit” using + flt(entry.debit).
        - Update d at “credit” using + flt(entry.credit).
      - Otherwise.
        - If (d.report\_type equals “Balance Sheet” and not (d.root\_type equals “Equity” or d.account\_type equals “Equity”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.report\_type equals “Balance Sheet” → not (d.root\_type equals “Equity” or d.account\_type equals “Equity”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.root\_type equals “Equity” → d.account\_type equals “Equity”.
          - Update d at “debit” using + (flt(entry.debit) × flt(exchange\_rate)).
          - Update d at “credit” using + (flt(entry.credit) × flt(exchange\_rate)).
        - Otherwise.
          - Update d at “debit” using + flt(entry.debit\_in\_reporting\_currency).
          - Update d at “credit” using + flt(entry.credit\_in\_reporting\_currency).
  - Set d at “closing\_debit” from (d at “opening\_debit” + d at “debit”).
  - Set d at “closing\_credit” from (d at “opening\_credit” + d at “credit”).
  - If show\_net\_values.
    - Evaluate prepare\_opening\_closing(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L94)

<a id="op-e679e856d854d2"></a>
### Calculate total row

`operation_enterprise_accounts_report_trial_balance_business_behavior_calculate_total_row`

**Inputs** data, company\_currency, show\_group\_accounts = true.

**Explicit results** total\_row.

**Local steps**

- Set total\_row from mapping(“account” → ((“'” + translated “Total”) + “'”), “account\_name” → ((“'” + translated “Total”) + “'”), “warn\_if\_negative” → true, “opening\_debit” → 0.0, …).
- Bind local operation sum\_value\_fields for subsequent calls.
- For each d in data.
  - If not show\_group\_accounts.
    - Evaluate sum\_value\_fields(d).
  - Otherwise.
    - If (show\_group\_accounts and not d.get(“parent\_account”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in show\_group\_accounts → not d.get(“parent\_account”).
      - Evaluate sum\_value\_fields(d).
- Return total\_row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L943) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1006) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L92)

<a id="op-bdeb6e5c026aaa"></a>
### Calculate total row.sum value fields

`operation_enterprise_accounts_report_trial_balance_business_behavior_calculate_total_row_sum_value_fields`

**Inputs** row.

**Local steps**

- For each field in value\_fields.
  - Update total\_row at field using + row at field.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L1424) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L93)

<a id="op-93121ad3e8417e"></a>
### Accumulate values into parents

`operation_enterprise_accounts_report_trial_balance_business_behavior_accumulate_values_into_parents`

**Inputs** accounts, accounts\_by\_name.

**Local steps**

- For each d in reversed(accounts).
  - If d.parent\_account.
    - For each key in value\_fields.
      - Update accounts\_by\_name at d.parent\_account at key using + d at key.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L1495) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1005) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L91)

<a id="op-3795dfbee7b32f"></a>
### Prepare data

`operation_enterprise_accounts_report_trial_balance_business_behavior_prepare_data`

**Inputs** accounts, filters, parent\_children\_map, company\_currency.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each d in accounts.
  - If (parent\_children\_map.get(d.account) and filters.get(“show\_net\_values”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_children\_map.get(d.account) → filters.get(“show\_net\_values”).
    - Evaluate prepare\_opening\_closing(d).
  - Set has\_value from false.
  - Set row from mapping(“account” → d.name, “parent\_account” → d.parent\_account, “indent” → d.indent, “from\_date” → filters.from\_date, …).
    - Value choice on d.account\_number — true gives formatted text {d.account\_number} - {d.account\_name}, false gives d.account\_name.
  - For each key in value\_fields.
    - Set row at key from flt(d.get(key, 0.0)).
    - If abs(row at key) ≥ get\_zero\_cutoff(company\_currency).
      - Set has\_value from true.
  - Set row at “has\_value” from has\_value.
  - Evaluate data.append(row).
- If not filters.get(“show\_group\_accounts”).
  - Set data from hide\_group\_accounts(data).
- Set total\_row from calculate\_total\_row(data, company\_currency, show\_group\_accounts = filters.get(“show\_group\_accounts”)).
- Evaluate data.extend(list(mapping(), total\_row)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L1626) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1024) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L110)

<a id="op-ef1cb708e61416"></a>
### Get columns

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “account”, “label” → translated “Account”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“fieldname” → “acc\_name”, “label” → translated “Account Name”, “fieldtype” → “ ….

**Local steps**

- Return list(mapping(“fieldname” → “account”, “label” → translated “Account”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“fieldname” → “acc\_name”, “label” → translated “Account Name”, “fieldtype” → “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L2374) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1013) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L99)

<a id="op-2399f5107e7efa"></a>
### Prepare opening closing

`operation_enterprise_accounts_report_trial_balance_business_behavior_prepare_opening_closing`

**Inputs** row.

**Local steps**

- Set dr\_or\_cr from “debit” when row at “root\_type” belongs to list(“Asset”, “Equity”, “Expense”), otherwise “credit”.
  - Value choice on row at “root\_type” belongs to list(“Asset”, “Equity”, “Expense”) — true gives “debit”, false gives “credit”.
- Set reverse\_dr\_or\_cr from “credit” when dr\_or\_cr equals “debit”, otherwise “debit”.
  - Value choice on dr\_or\_cr equals “debit” — true gives “credit”, false gives “debit”.
- For each col\_type in list(“opening”, “closing”).
  - Set valid\_col from ((col\_type + “\_”) + dr\_or\_cr).
  - Set reverse\_col from ((col\_type + “\_”) + reverse\_dr\_or\_cr).
  - Update row at valid\_col using − row at reverse\_col.
  - If row at valid\_col &lt; 0.
    - Set row at reverse\_col from abs(row at valid\_col).
    - Set row at valid\_col from 0.0.
  - Otherwise.
    - Set row at reverse\_col from 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L3486) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1025) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L111)

<a id="op-4499db9c170fc5"></a>
### Hide group accounts

`operation_enterprise_accounts_report_trial_balance_business_behavior_hide_group_accounts`

**Inputs** data.

**Explicit results** non\_group\_accounts\_data.

**Local steps**

- Set non\_group\_accounts\_data from list().
- For each d in data.
  - If not d.get(“is\_group\_account”).
    - Evaluate d.update(indent = 0).
    - Evaluate non\_group\_accounts\_data.append(d).
- Return non\_group\_accounts\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L3861) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1023) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L109)

<a id="op-102596bb0ad28c"></a>
### Execute snapshot report

`operation_enterprise_accounts_report_trial_balance_business_behavior_execute_snapshot_report`

**Inputs** filters.

**Explicit results** execute(filters) · tuple(columns, data).

**Explicit failure paths** validation helper — translated “Trial Balance requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”)).

**Local steps**

- If has\_gl\_entry\_restrictions().
  - Return execute(filters).
- Bind dependencies get\_latest\_sync.
- If conn bound to get\_latest\_sync(“GL Entry”).
  - Evaluate validate\_company\_permission(filters.company).
  - Evaluate validate\_filters(filters).
  - Set columns from get\_columns().
  - Set data from get\_data\_duckdb(filters, conn).
  - Return tuple(columns, data).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Trial Balance requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L96)

<a id="op-65ae22f9103877"></a>
### Get data duckdb

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_data_duckdb`

**Inputs** filters, conn.

**Record and data access** execute query text (SELECT, Account) · read “Accounts Settings” via get\_single\_value.

**Explicit results** no value · filter\_out\_zero\_value\_rows(data, parent\_children\_map, show\_zero\_values = filters.get(“show\_zero\_values”)).

**Local steps**

- Set accounts from Platform.db.sql(query text (SELECT, Account), filters.company, as\_dict = true).
- If not accounts.
  - Return no value.
- Set company\_currency from (filters.presentation\_currency or Enterprise.get\_company\_currency(filters.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.presentation\_currency → Enterprise.get\_company\_currency(filters.company).
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set gl\_entries\_by\_account from get\_period\_gl\_entries\_duckdb(conn, filters, ignore\_is\_opening).
- Set opening\_balances from get\_opening\_balances\_duckdb(conn, filters, ignore\_is\_opening).
- Evaluate calculate\_values(accounts, gl\_entries\_by\_account, opening\_balances, filters.get(“show\_net\_values”), ignore\_is\_opening = ignore\_is\_opening).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name).
- Set data from prepare\_data(accounts, filters, parent\_children\_map, company\_currency).
- Return filter\_out\_zero\_value\_rows(data, parent\_children\_map, show\_zero\_values = filters.get(“show\_zero\_values”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L101)

<a id="op-2d1edf3843f1c8"></a>
### Extra gl conditions

`operation_enterprise_accounts_report_trial_balance_business_behavior_extra_general_ledger_conditions`

**Inputs** filters.

**Record and data access** read “Finance Book” via count · read “Company” via get\_cached\_value · read “DocType” via get\_cached\_value.

**Explicit results** tuple(conditions, params).

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set tuple(conditions, params) from tuple(list(), list()).
- If filters.get(“cost\_center”).
  - Set cc from get\_cost\_centers\_with\_children(filters.get(“cost\_center”)).
  - Evaluate conditions.append(formatted text cost\_center IN ({“, ”.join((list(“?”) × len(cc)))})).
  - Evaluate params.extend(cc).
- If filters.get(“project”).
  - Set proj from filters.project when isinstance(filters.project, list), otherwise list(filters.project).
    - Value choice on isinstance(filters.project, list) — true gives filters.project, false gives list(filters.project).
  - Evaluate conditions.append(formatted text project IN ({“, ”.join((list(“?”) × len(proj)))})).
  - Evaluate params.extend(proj).
- If Platform.db.count(“Finance Book”).
  - Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
  - If filters.get(“include\_default\_book\_entries”).
    - If (filters.get(“finance\_book”) and company\_fb and cstr(filters.finance\_book) differs from cstr(company\_fb)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“finance\_book”) → company\_fb → cstr(filters.finance\_book) differs from cstr(company\_fb).
      - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
    - Set fb\_list from list(cstr(filters.get(“finance\_book”)), cstr(company\_fb), empty text).
  - Otherwise.
    - Set fb\_list from list(cstr(filters.get(“finance\_book”)), empty text).
  - Evaluate conditions.append(formatted text (finance\_book IN ({“, ”.join((list(“?”) × len(fb\_list)))}) OR finance\_book IS NULL)).
  - Evaluate params.extend(fb\_list).
- For each dim in get\_accounting\_dimensions(as\_list = false).
  - If filters.get(dim.fieldname).
    - If Platform.get\_cached\_value(“DocType”, dim.document\_type, “is\_tree”).
      - Set filters at dim.fieldname from get\_dimension\_with\_children(dim.document\_type, filters.get(dim.fieldname)).
    - Set vals from filters at dim.fieldname when isinstance(filters at dim.fieldname, list), otherwise list(filters at dim.fieldname).
      - Value choice on isinstance(filters at dim.fieldname, list) — true gives filters at dim.fieldname, false gives list(filters at dim.fieldname).
    - Evaluate conditions.append(formatted text {dim.fieldname} IN ({“, ”.join((list(“?”) × len(vals)))})).
    - Evaluate params.extend(vals).
- Return tuple(conditions, params).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”), Platform.get\_cached\_value(“DocType”, dim.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L4861) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L97)

<a id="op-46a26211e8bc89"></a>
### Fetch gl rows duckdb

`operation_enterprise_accounts_report_trial_balance_business_behavior_fetch_general_ledger_rows_duckdb`

**Inputs** conn, conditions, params.

**Explicit results** list of Platform.\_dict(zip(cols, row, strict = false)) for row drawn from conn.execute(sql, params).fetchall().

**Local steps**

- Set cols from list(“account”, “debit”, “credit”, “debit\_in\_account\_currency”, …).
- Set sql from formatted text SELECT account, SUM(debit), SUM(credit),                   SUM(debit\_in\_account\_currency), SUM(credit\_in\_account\_currency), account\_currency.
- Return list of Platform.\_dict(zip(cols, row, strict = false)) for row drawn from conn.execute(sql, params).fetchall().
  - Draw row from conn.execute(sql, params).fetchall().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L6154) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1012) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L98)

<a id="op-79bf53c2ed8931"></a>
### Get period gl entries duckdb

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_period_general_ledger_entries_duckdb`

**Inputs** conn, filters, ignore\_is\_opening.

**Explicit results** gl\_entries\_by\_account.

**Local steps**

- Set conditions from list(“company = ?”, “is\_cancelled = 0”, “posting\_date &gt;= ?”, “posting\_date &lt;= ?”).
- Set params from list(filters.company, filters.from\_date, filters.to\_date).
- If not ignore\_is\_opening.
  - Evaluate conditions.append(“is\_opening = 'No'”).
- If not flt(filters.get(“with\_period\_closing\_entry\_for\_current\_period”)).
  - Evaluate conditions.append(“voucher\_type != 'Period Closing Voucher'”).
- Set tuple(extra\_cond, extra\_params) from \_extra\_gl\_conditions(filters).
- Evaluate conditions.extend(extra\_cond).
- Evaluate params.extend(extra\_params).
- Set entries from \_fetch\_gl\_rows\_duckdb(conn, conditions, params).
- If filters.get(“presentation\_currency”).
  - Evaluate convert\_to\_presentation\_currency(entries, get\_currency(filters)).
- Set gl\_entries\_by\_account from mapping().
- For each entry in entries.
  - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).
- Return gl\_entries\_by\_account.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L6501) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L106)

<a id="op-fa7cc1dcfd69b7"></a>
### Get opening balances duckdb

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_opening_balances_duckdb`

**Inputs** conn, filters, ignore\_is\_opening.

**Explicit results** bs.

**Local steps**

- Set bs from \_get\_rootwise\_opening\_duckdb(conn, filters, “Balance Sheet”, ignore\_is\_opening).
- Set pl from \_get\_rootwise\_opening\_duckdb(conn, filters, “Profit and Loss”, ignore\_is\_opening).
- Evaluate bs.update(pl).
- Return bs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0285.json#L6979) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L105)

<a id="op-318e6600ad18c9"></a>
### Get rootwise opening duckdb

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_rootwise_opening_duckdb`

**Inputs** conn, filters, report\_type, ignore\_is\_opening.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Period Closing Voucher” via get\_all.

**Explicit results** opening.

**Local steps**

- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- Set ignore\_closing\_balances from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).
- Set last\_pcv from empty text.
- If not ignore\_closing\_balances.
  - Set last\_pcv from Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“docstatus” → 1, “company” → filters.company, “period\_end\_date” → tuple(“&lt;”, filters.from\_date)), fields = list(“period\_end\_date”, “name”), o ….
- If last\_pcv.
  - Set gle from get\_opening\_balance(“Account Closing Balance”, filters, report\_type, accounting\_dimensions, period\_closing\_voucher = last\_pcv at 0.name, ignore\_is\_opening = ignore\_is\_opening).
  - If getdate(last\_pcv at 0.period\_end\_date) &lt; getdate(add\_days(filters.from\_date, negative 1)).
    - Set start\_date from add\_days(last\_pcv at 0.period\_end\_date, 1).
    - Update gle using + \_get\_gl\_entry\_opening\_duckdb(conn, filters, report\_type, ignore\_is\_opening, start\_date = start\_date).
- Otherwise.
  - Set gle from \_get\_gl\_entry\_opening\_duckdb(conn, filters, report\_type, ignore\_is\_opening).
- Set opening from Platform.\_dict().
- For each d in gle.
  - Evaluate opening.setdefault(d.account, mapping(“account” → d.account, “opening\_debit” → 0.0, “opening\_credit” → 0.0)).
  - Update opening at d.account at “opening\_debit” using + flt(d.debit).
  - Update opening at d.account at “opening\_credit” using + flt(d.credit).
- Return opening.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0286.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L108)

<a id="op-01843101c0ef1c"></a>
### Get gl entry opening duckdb

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_general_ledger_entry_opening_duckdb`

**Inputs** conn, filters, report\_type, ignore\_is\_opening, start\_date = no value.

**Record and data access** read “Account” via get\_all.

**Explicit results** list() · gle.

**Local steps**

- Set accounts from Platform.db.get\_all(“Account”, filters = mapping(“report\_type” → report\_type), pluck = “name”).
- If not accounts.
  - Return list().
- Set conditions from list(“company = ?”, formatted text account IN ({“, ”.join((list(“?”) × len(accounts)))}), “is\_cancelled = 0”).
- Set params from list(filters.company, expanded accounts).
- If start\_date.
  - Evaluate conditions.append(“posting\_date &gt;= ? AND posting\_date &lt; ?”).
  - Evaluate params.extend(list(start\_date, filters.from\_date)).
  - If not ignore\_is\_opening.
    - Evaluate conditions.append(“is\_opening = 'No'”).
- Otherwise.
  - If not ignore\_is\_opening.
    - Evaluate conditions.append(“(posting\_date &lt; ? OR is\_opening = 'Yes')”).
    - Evaluate params.append(filters.from\_date).
  - Otherwise.
    - Evaluate conditions.append(“posting\_date &lt; ?”).
    - Evaluate params.append(filters.from\_date).
- If (not filters.get(“show\_unclosed\_fy\_pl\_balances”) and report\_type equals “Profit and Loss”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.get(“show\_unclosed\_fy\_pl\_balances”) → report\_type equals “Profit and Loss”.
  - Evaluate conditions.append(“posting\_date &gt;= ?”).
  - Evaluate params.append(filters.year\_start\_date).
- If not flt(filters.get(“with\_period\_closing\_entry\_for\_opening”)).
  - Evaluate conditions.append(“voucher\_type != 'Period Closing Voucher'”).
- Set tuple(extra\_cond, extra\_params) from \_extra\_gl\_conditions(filters).
- Evaluate conditions.extend(extra\_cond).
- Evaluate params.extend(extra\_params).
- Set gle from \_fetch\_gl\_rows\_duckdb(conn, conditions, params).
- If filters.get(“presentation\_currency”).
  - Evaluate convert\_to\_presentation\_currency(gle, get\_currency(filters)).
- Return gle.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0286.json#L836) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L102)

## Report · Trial balance for party

<a id="op-f2303b86270402"></a>
### Execute

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_filters(filters).
- Set show\_party\_name from is\_party\_name\_visible(filters).
- Set columns from get\_columns(filters, show\_party\_name).
- Set data from get\_data(filters, show\_party\_name).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0286.json#L3902) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1027) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L113)

<a id="op-0c0f1ec9b9720d"></a>
### Get data

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_get_data`

**Inputs** filters, show\_party\_name.

**Record and data access** read filters.get(“party\_type”) via get\_list · read “Company” via get\_cached\_value.

**Explicit results** data.

**Local steps**

- If filters.get(“party\_type”) belongs to tuple(“Customer”, “Supplier”, “Employee”, “Member”).
  - Set party\_name\_field from “{}\_name”.format(Platform.scrub(filters.get(“party\_type”))).
- Otherwise.
  - If filters.get(“party\_type”) equals “Shareholder”.
    - Set party\_name\_field from “title”.
  - Otherwise.
    - Set party\_name\_field from “name”.
- Set party\_filters from list(mapping(“name” → filters.get(“party”))) when filters.get(“party”), otherwise list().
  - Value choice on filters.get(“party”) — true gives list(mapping(“name” → filters.get(“party”))), false gives list().
- Set party\_type from Platform.qb.DocType(filters.get(“party\_type”)).
- If condition bound to get\_allowed\_masters\_condition(party\_type.name, filters.get(“party\_type”)).
  - Evaluate party\_filters.append(condition).
- Set parties from Platform.get\_list(filters.get(“party\_type”), fields = list(“name”, party\_name\_field), filters = party\_filters, order\_by = “name”).
- Set account\_filter from list().
- If filters.get(“account”).
  - Set account\_filter from get\_accounts\_with\_children(filters.get(“account”)).
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set precision from get\_currency\_precision().
- Set opening\_balances from get\_opening\_balances(filters, account\_filter).
- Set balances\_within\_period from get\_balances\_within\_period(filters, account\_filter).
- Set data from list().
- Set total\_row from Platform.\_dict(mapping(“opening\_debit” → 0, “opening\_credit” → 0, “debit” → 0, “credit” → 0, …)).
- For each party in parties.
  - Set row from mapping(“party” → party.name).
  - If show\_party\_name.
    - Set row at “party\_name” from party.get(party\_name\_field).
  - Set tuple(opening\_debit, opening\_credit) from opening\_balances.get(party.name, list(0, 0)).
  - Set tuple(opening\_debit, opening\_credit) from tuple(flt(opening\_debit, precision), flt(opening\_credit, precision)).
  - Evaluate row.update(mapping(“opening\_debit” → opening\_debit, “opening\_credit” → opening\_credit)).
  - Set tuple(debit, credit) from balances\_within\_period.get(party.name, list(0, 0)).
  - Set tuple(debit, credit) from tuple(flt(debit, precision), flt(credit, precision)).
  - Evaluate row.update(mapping(“debit” → debit, “credit” → credit)).
  - Set tuple(closing\_debit, closing\_credit) from toggle\_debit\_credit((opening\_debit + debit), (opening\_credit + credit)).
  - Set tuple(closing\_debit, closing\_credit) from tuple(flt(closing\_debit, precision), flt(closing\_credit, precision)).
  - Evaluate row.update(mapping(“closing\_debit” → closing\_debit, “closing\_credit” → closing\_credit)).
  - Evaluate row.update(mapping(“currency” → company\_currency)).
  - Set has\_value from false.
  - If (opening\_debit or opening\_credit or debit or credit or closing\_debit or closing\_credit).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in opening\_debit → opening\_credit → debit → credit → closing\_debit → closing\_credit.
    - Set has\_value from true.
  - If (filters.get(“exclude\_zero\_balance\_parties”) and not closing\_debit and not closing\_credit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“exclude\_zero\_balance\_parties”) → not closing\_debit → not closing\_credit.
    - Continue with the next iteration or loop test.
  - If (cint(filters.show\_zero\_values) or has\_value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(filters.show\_zero\_values) → has\_value.
    - Evaluate data.append(row).
    - For each col in total\_row.
      - Update total\_row at col using + row.get(col).
- Evaluate total\_row.update(mapping(“party” → ((“'” + translated “Totals”) + “'”), “currency” → company\_currency)).
- Evaluate data.append(total\_row).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L116)

<a id="op-5e473f620dce9d"></a>
### Get opening balances

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_get_opening_balances`

**Inputs** filters, account\_filter = no value.

**Explicit results** opening.

**Local steps**

- Set GL\_Entry from Platform.qb.DocType(“GL Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(GL\_Entry.party, nested operand in the contract.as\_(“opening\_debit”), nested operand in the contract.as\_(“opening\_credit”)).where(((((ne ….
- If account\_filter.
  - Set query from query.where(GL\_Entry.account.isin(account\_filter)).
- If finance\_book\_condition bound to get\_finance\_book\_condition(GL\_Entry, filters).
  - Set query from query.where(finance\_book\_condition).
- Set gle from query.run(as\_dict = true).
- Set opening from Platform.\_dict().
- For each d in gle.
  - Set tuple(opening\_debit, opening\_credit) from toggle\_debit\_credit(d.opening\_debit, d.opening\_credit).
  - Evaluate opening.setdefault(d.party, list(opening\_debit, opening\_credit)).
- Return opening.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L117)

<a id="op-56ed69b3f8fdb7"></a>
### Get balances within period

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_get_balances_within_period`

**Inputs** filters, account\_filter = no value.

**Explicit results** balances\_within\_period.

**Local steps**

- Set GL\_Entry from Platform.qb.DocType(“GL Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(GL\_Entry.party, nested operand in the contract.as\_(“debit”), nested operand in the contract.as\_(“credit”)).where(((((nested operand in  ….
- If account\_filter.
  - Set query from query.where(GL\_Entry.account.isin(account\_filter)).
- If finance\_book\_condition bound to get\_finance\_book\_condition(GL\_Entry, filters).
  - Set query from query.where(finance\_book\_condition).
- Set gle from query.run(as\_dict = true).
- Set balances\_within\_period from Platform.\_dict().
- For each d in gle.
  - Evaluate balances\_within\_period.setdefault(d.party, list(d.debit, d.credit)).
- Return balances\_within\_period.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1028) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L114)

<a id="op-5ae753ec63ba7c"></a>
### Get finance book condition

`operation_enterprise_binding_enterprise_accounts_report_trial_balance_for_party_trial_balance_for_party_get_finance_book_condition`

**Inputs** gl\_entry, filters.

**Record and data access** read “Finance Book” via count · read “Company” via get\_cached\_value.

**Explicit results** no value · (gl\_entry.finance\_book.isin(finance\_books) bitwise or gl\_entry.finance\_book.isnull()).

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- If not Platform.db.count(“Finance Book”).
  - Return no value.
- Set finance\_books from list(cstr(filters.get(“finance\_book”)), empty text).
- If filters.get(“include\_default\_book\_entries”).
  - Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
  - If (filters.get(“finance\_book”) and company\_fb and cstr(filters.finance\_book) differs from cstr(company\_fb)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“finance\_book”) → company\_fb → cstr(filters.finance\_book) differs from cstr(company\_fb).
    - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
  - Evaluate finance\_books.append(cstr(company\_fb)).
- Return (gl\_entry.finance\_book.isin(finance\_books) bitwise or gl\_entry.finance\_book.isnull()).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1275)
