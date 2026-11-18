# Accounting and settlement · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-29b0b3b66583b7"></a>
### Financial Report Engine.generate chart data

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_generate_chart_data`

**Inputs** self, context.

**Declared result** dict at tuple(str, Any).

**Explicit results** context.

**Local steps**

- Set generator from ChartDataGenerator(context).
- Evaluate generator.generate().
- Return context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L3908) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L856)

<a id="op-de5fe943c92c9f"></a>
### Data Collector.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_collector_initialize`

**Inputs** self, filters, periods.

**Local steps**

- Set self.filters from filters.
- Set self.periods from periods.
- Set self.company from filters.get(“company”).
- Set self.account\_requests from list().
- Set self.query\_builder from FinancialQueryBuilder(filters, periods).
- Set self.account\_fields from set of field.fieldname for field drawn from Platform.get\_meta(“Account”).fields.
  - Draw field from Platform.get\_meta(“Account”).fields.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L4018) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L819)

<a id="op-d05b4d2d7cbd3b"></a>
### Data Collector.add account request

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_collector_add_account_request`

**Inputs** self, row.

**Local steps**

- Evaluate self.account\_requests.append(mapping(“row” → row, “accounts” → self.\_parse\_account\_filter(self.company, row), “balance\_type” → row.balance\_type, “reference\_code” → row.reference\_code, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse account filter](operations-039.md#op-51950cbf47e973).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L4284) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L867) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L816)

<a id="op-f1292a2f042b51"></a>
### Data Collector.collect all data

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_collector_collect_all_data`

**Inputs** self.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“account\_data” → mapping(), “summary” → mapping(), “account\_details” → mapping()) · mapping(“account\_data” → account\_data, “summary” → summary, “account\_details” → account\_details).

**Local steps**

- If not self.account\_requests.
  - Return mapping(“account\_data” → mapping(), “summary” → mapping(), “account\_details” → mapping()).
- Set all\_accounts from list().
- For each request in self.account\_requests.
  - Evaluate all\_accounts.extend(request at “accounts”).
- If not all\_accounts.
  - Return mapping(“account\_data” → mapping(), “summary” → mapping(), “account\_details” → mapping()).
- Set account\_data from self.query\_builder.fetch\_account\_balances(all\_accounts).
- Set summary from mapping().
- Set account\_details from mapping().
- Set period\_keys from list of p at “key” for p drawn from self.periods.
  - Draw p from self.periods.
- For each request in self.account\_requests.
  - Set ref\_code from request at “reference\_code”.
  - If not ref\_code.
    - Continue with the next iteration or loop test.
  - Set balance\_type from request at “balance\_type”.
  - Set accounts from request at “accounts”.
  - Set total\_values from (list(0.0) × len(self.periods)).
  - Set request\_account\_details from mapping().
  - For each account in accounts.
    - Set account\_name from account.name.
    - If account\_name does not belong to account\_data.
      - Continue with the next iteration or loop test.
    - Set account\_obj from account\_data at account\_name.copy().
    - If request at “reverse\_sign”.
      - Evaluate account\_obj.reverse\_values().
    - Set account\_values from account\_obj.get\_ordered\_values(period\_keys, balance\_type).
    - For each tuple(i, value) in enumerate(account\_values).
      - Update total\_values at i using + value.
    - Set request\_account\_details at account\_name from account\_obj.
  - Set summary at ref\_code from total\_values.
  - Set account\_details at ref\_code from request\_account\_details.
- Return mapping(“account\_data” → account\_data, “summary” → summary, “account\_details” → account\_details).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L4464) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L868) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L817)

<a id="op-51950cbf47e973"></a>
### Data Collector.parse account filter

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_collector_parse_account_filter`

**Inputs** company, report\_row.

**Wrappers, in declaration order** staticmethod.

**Declared result** list at dict.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- Set filter\_parser from FilterExpressionParser().
- Set account from Platform.qb.DocType(“Account”).
- Set query from nested operand in the contract(nested operand in the contract).select(account.name, account.account\_name, account.account\_number).where(account.disabled equals 0).where(account.is\_group equals 0).
- If company.
  - Set query from query.where(account.company equals company).
- Set where\_condition from filter\_parser.build\_condition(report\_row, account).
- If where\_condition is identical to no value.
  - Return list().
- Set query from query.where(where\_condition).
- Set query from query.orderby(account.name).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L5299) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L820)

<a id="op-414fc00f61e19b"></a>
### Data Collector.get filtered accounts

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_collector_get_filtered_accounts`

**Inputs** company, account\_rows.

**Wrappers, in declaration order** staticmethod.

**Declared result** list at str.

**Explicit results** query.run(pluck = true).

**Local steps**

- Set filter\_parser from FilterExpressionParser().
- Set account from Platform.qb.DocType(“Account”).
- Set query from nested operand in the contract().where(nested operand in the contract.disabled equals 0).where(account.is\_group equals 0).orderby(account.name).
- If company.
  - Set query from query.where(account.company equals company).
- Set conditions from filter\_parser.build\_conditions(account\_rows, account, raise\_on\_invalid = true).
- If conditions is distinct from no value.
  - Set query from query.where(conditions).
- Return query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L5753) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L818)

<a id="op-c4291babcb5a41"></a>
### Financial Query Builder.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_initialize`

**Inputs** self, filters, periods.

**Local steps**

- Set self.filters from filters.
- Set self.periods from periods.
- Set self.company from filters.get(“company”).
- Set self.account\_meta from mapping().
- Set self.ignore\_opening\_entries from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L6202) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L850)

<a id="op-481e2863d68ee0"></a>
### Financial Query Builder.fetch account balances

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_fetch_account_balances`

**Inputs** self, accounts.

**Declared result** dict at tuple(str, AccountData).

**Explicit results** balances\_data.

**Local steps**

- Set account\_names from list(set of acc.name for acc drawn from accounts).
  - Draw acc from accounts.
- Set self.account\_meta from mapping of acc.name → mapping(“account\_name” → acc.account\_name, “account\_number” → acc.account\_number) for acc drawn from accounts.
  - Draw acc from accounts.
- Set balances\_data from self.\_get\_opening\_balances(account\_names).
- Set gl\_data from self.\_get\_gl\_movements(account\_names).
- Evaluate self.\_calculate\_running\_balances(balances\_data, gl\_data).
- Evaluate self.\_handle\_balance\_accumulation(balances\_data).
- Return balances\_data.

**Methods declared on this owner** [get opening balances](operations-039.md#op-ab07c3c3b23e44), [get gl movements](operations-039.md#op-9309b8bf4901d0), [calculate running balances](operations-039.md#op-f60cf2de50e076), [handle balance accumulation](operations-039.md#op-b7a4c9c318e368).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L6388) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L842)

<a id="op-ab07c3c3b23e44"></a>
### Financial Query Builder.get opening balances

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_get_opening_balances`

**Inputs** self, accounts.

**Declared result** dict at tuple(str, dict at tuple(str, dict at tuple(str, float))).

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Period Closing Voucher” via get\_all.

**Explicit results** self.\_get\_opening\_balances\_from\_gl(accounts) · self.\_rebase\_closing\_balances(closing\_data, closing\_voucher.period\_end\_date).

**Local steps**

- Set self.ignore\_opening\_entries from false.
- If Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).
  - Return self.\_get\_opening\_balances\_from\_gl(accounts).
- Set first\_period\_start from getdate(self.periods at 0 at “from\_date”).
- Set last\_closing\_voucher from Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“docstatus” → 1, “company” → self.company, “period\_end\_date” → tuple(“&lt;”, first\_period\_start)), fields = list(“period\_end\_date”, “name”), ord ….
- If last\_closing\_voucher.
  - Set closing\_voucher from last\_closing\_voucher at 0.
  - Set closing\_data from self.\_get\_closing\_balances(accounts, closing\_voucher.name).
  - Set self.ignore\_opening\_entries from true.
  - Return self.\_rebase\_closing\_balances(closing\_data, closing\_voucher.period\_end\_date).
- Return self.\_get\_opening\_balances\_from\_gl(accounts).

**Methods declared on this owner** [get opening balances from gl](operations-039.md#op-fd106aedb06274), [get closing balances](operations-039.md#op-2ae2536f92e5a2), [rebase closing balances](operations-039.md#op-11af62e913b99e).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L6717) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L847)

<a id="op-2ae2536f92e5a2"></a>
### Financial Query Builder.get closing balances

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_get_closing_balances`

**Inputs** self, account\_names, closing\_voucher.

**Declared result** dict at tuple(str, float).

**Explicit results** closing\_balances.

**Local steps**

- Set closing\_balances from mapping of account → 0.0 for account drawn from account\_names.
  - Draw account from account\_names.
- Set acb\_table from Platform.qb.DocType(“Account Closing Balance”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(account\_names)).where(acb\_table.period\_closing\_voucher equals closing\_voucher).groupby(acb\_table.account).
- Set query from self.\_apply\_standard\_filters(query, acb\_table, “Account Closing Balance”).
- Set results from self.\_execute\_with\_permissions(query, “Account Closing Balance”).
- For each row in results.
  - Set closing\_balances at row at “account” from (row at “balance” or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “balance” → 0.0.
- Return closing\_balances.

**Methods declared on this owner** [apply standard filters](operations-039.md#op-95500262ca6009), [execute with permissions](operations-039.md#op-a63662db3724f4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L7251) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L844)

<a id="op-11af62e913b99e"></a>
### Financial Query Builder.rebase closing balances

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_rebase_closing_balances`

**Inputs** self, closing\_data, closing\_date.

**Declared result** dict at tuple(str, dict at tuple(str, dict at tuple(str, float))).

**Explicit results** balances\_data.

**Local steps**

- Set balances\_data from mapping().
- Set first\_period\_key from self.periods at 0 at “key”.
- Set report\_start from getdate(self.periods at 0 at “from\_date”).
- Set closing\_end from getdate(closing\_date).
- Set has\_gap from date\_diff(report\_start, closing\_end) &gt; 1.
- Set gap\_movements from mapping().
- If has\_gap.
  - Set gap\_movements from self.\_get\_gap\_movements(list(closing\_data.keys()), closing\_date, report\_start).
- For each tuple(account, closing\_balance) in closing\_data.items().
  - Set gap\_movement from gap\_movements.get(account, 0.0).
  - Set opening\_balance from (closing\_balance + gap\_movement).
  - Set account\_data from AccountData(account = account, expanded names self.\_get\_account\_meta(account)).
  - Evaluate account\_data.add\_period(PeriodValue(first\_period\_key, opening\_balance, 0, 0)).
  - Set balances\_data at account from account\_data.
- Return balances\_data.

**Methods declared on this owner** [get gap movements](operations-039.md#op-ed2c6d78e47511), [get account meta](operations-039.md#op-426f41a1c34140).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L851)

<a id="op-fd106aedb06274"></a>
### Financial Query Builder.get opening balances from gl

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_get_opening_balances_from_general_ledger`

**Inputs** self, accounts.

**Declared result** dict.

**Explicit results** self.\_rebase\_closing\_balances(zero\_closing\_balances, earliest\_date).

**Local steps**

- Set zero\_closing\_balances from mapping of account → 0.0 for account drawn from accounts.
  - Draw account from accounts.
- Set earliest\_date from “1900-01-01”.
- Return self.\_rebase\_closing\_balances(zero\_closing\_balances, earliest\_date).

**Methods declared on this owner** [rebase closing balances](operations-039.md#op-11af62e913b99e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L596) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L848)

<a id="op-ed2c6d78e47511"></a>
### Financial Query Builder.get gap movements

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_get_gap_movements`

**Inputs** self, account\_names, from\_date, to\_date.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of row at “account” → (row at “movement” or 0.0) for row drawn from results.

**Local steps**

- Set gl\_table from Platform.qb.DocType(“GL Entry”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.posting\_date &gt; from\_date).where(gl\_table.posting\_date &lt; to\_date).groupby(gl\_table.account).
- Set query from self.\_apply\_standard\_filters(query, gl\_table).
- Set results from self.\_execute\_with\_permissions(query, “GL Entry”).
- Return mapping of row at “account” → (row at “movement” or 0.0) for row drawn from results.
  - Draw row from results.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “movement” → 0.0.

**Methods declared on this owner** [apply standard filters](operations-039.md#op-95500262ca6009), [execute with permissions](operations-039.md#op-a63662db3724f4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L728) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L845)

<a id="op-9309b8bf4901d0"></a>
### Financial Query Builder.get gl movements

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_get_general_ledger_movements`

**Inputs** self, account\_names.

**Declared result** list at dict.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** self.\_execute\_with\_permissions(query, “GL Entry”).

**Local steps**

- Set gl\_table from Platform.qb.DocType(“GL Entry”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(account\_names)).where(gl\_table.posting\_date ≥ nested operand in the contract.periods at 0 at “from\_d ….
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- If (self.ignore\_opening\_entries and not ignore\_is\_opening).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.ignore\_opening\_entries → not ignore\_is\_opening.
  - Set query from query.where(gl\_table.is\_opening equals “No”).
- For each period in self.periods.
  - Set period\_condition from Case().when((gl\_table.posting\_date ≥ period at “from\_date” bitwise and gl\_table.posting\_date ≤ period at “to\_date”), (gl\_table.debit − gl\_table.credit)).else\_(0).
  - Set query from query.select(Sum(period\_condition).as\_(period at “key”)).
- Set query from self.\_apply\_standard\_filters(query, gl\_table).
- Return self.\_execute\_with\_permissions(query, “GL Entry”).

**Methods declared on this owner** [apply standard filters](operations-039.md#op-95500262ca6009), [execute with permissions](operations-039.md#op-a63662db3724f4).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L1279) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L846)

<a id="op-f60cf2de50e076"></a>
### Financial Query Builder.calculate running balances

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_calculate_running_balances`

**Inputs** self, balances\_data, gl\_data.

**Declared result** dict.

**Local steps**

- Set gl\_dict from mapping of row at “account” → row for row drawn from gl\_data.
  - Draw row from gl\_data.
- Set accounts from (set(balances\_data.keys()) bitwise or set(gl\_dict.keys())).
- For each account in accounts.
  - If account does not belong to balances\_data.
    - Set balances\_data at account from AccountData(account = account, expanded names self.\_get\_account\_meta(account)).
  - Set account\_data from balances\_data at account.
  - Set gl\_movement from gl\_dict.get(account, mapping()).
  - If account\_data.has\_periods().
    - Set first\_period from account\_data.get\_period(self.periods at 0 at “key”).
    - Set current\_balance from first\_period.get\_value(“Opening Balance”) when first\_period, otherwise 0.0.
      - Value choice on first\_period — true gives first\_period.get\_value(“Opening Balance”), false gives 0.0.
  - Otherwise.
    - Set current\_balance from 0.0.
  - For each period in self.periods.
    - Set period\_key from period at “key”.
    - Set movement from gl\_movement.get(period\_key, 0.0).
    - Set closing\_balance from (current\_balance + movement).
    - Evaluate account\_data.add\_period(PeriodValue(period\_key, current\_balance, closing\_balance, movement)).
    - Set current\_balance from closing\_balance.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get account meta](operations-039.md#op-426f41a1c34140).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L2021) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L840)

<a id="op-b7a4c9c318e368"></a>
### Financial Query Builder.handle balance accumulation

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_handle_balance_accumulation`

**Inputs** self, balances\_data.

**Local steps**

- For each account\_data in balances\_data.values().
  - Set accumulated\_values from self.filters.get(“accumulated\_values”).
  - If accumulated\_values is identical to no value.
    - Continue with the next iteration or loop test.
  - Otherwise.
    - If accumulated\_values.
      - Evaluate account\_data.accumulate\_values().
    - Otherwise.
      - Evaluate account\_data.unaccumulate\_values().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L2640) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L849)

<a id="op-95500262ca6009"></a>
### Financial Query Builder.apply standard filters

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_apply_standard_filters`

**Inputs** self, query, table, doctype = “GL Entry”.

**Record and data access** read “Company” via get\_cached\_value · read “DocType” via get\_cached\_value.

**Explicit results** query.

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set pcv from Platform.qb.DocType(“Period Closing Voucher”).
- Set closing\_heads from nested operand in the contract.qb.from\_(pcv).select(pcv.closing\_account\_head).where(pcv.docstatus equals 1).
- If doctype equals “GL Entry”.
  - Set is\_pcv from table.voucher\_type equals “Period Closing Voucher”.
- Otherwise.
  - Set is\_pcv from table.is\_period\_closing\_voucher\_entry equals 1.
- Set query from query.where((complement is\_pcv bitwise or table.account.isin(closing\_heads))).
- If self.filters.get(“project”).
  - Set projects from self.filters.get(“project”).
  - If isinstance(projects, str).
    - Set projects from list(projects).
  - Set query from query.where(table.project.isin(projects)).
- If self.filters.get(“cost\_center”).
  - Set self.filters.cost\_center from get\_cost\_centers\_with\_children(self.filters.cost\_center).
  - Set query from query.where(table.cost\_center.isin(self.filters.cost\_center)).
- Set finance\_book from self.filters.get(“finance\_book”).
- If self.filters.get(“include\_default\_book\_entries”).
  - Set default\_book from Platform.get\_cached\_value(“Company”, self.filters.company, “default\_finance\_book”).
  - If (finance\_book and default\_book and cstr(finance\_book) differs from cstr(default\_book)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in finance\_book → default\_book → cstr(finance\_book) differs from cstr(default\_book).
    - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
  - Set query from query.where((table.finance\_book.isin(list(cstr(finance\_book), cstr(default\_book), empty text)) bitwise or table.finance\_book.isnull())).
- Otherwise.
  - Set query from query.where((table.finance\_book.isin(list(cstr(finance\_book), empty text)) bitwise or table.finance\_book.isnull())).
- Set dimensions from get\_accounting\_dimensions(as\_list = false).
- For each dimension in dimensions.
  - If self.filters.get(dimension.fieldname).
    - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
      - Set self.filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, self.filters.get(dimension.fieldname)).
    - Set query from query.where(table at dimension.fieldname.isin(self.filters.get(dimension.fieldname))).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.filters.company, “default\_finance\_book”), Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L2822) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L839)

<a id="op-a63662db3724f4"></a>
### Financial Query Builder.execute with permissions

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_execute_with_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, query, doctype.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L4172) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L841)

<a id="op-426f41a1c34140"></a>
### Financial Query Builder.get account meta

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_query_builder_get_account_meta`

**Inputs** self, account.

**Declared result** dict at tuple(str, Any).

**Explicit results** self.account\_meta.get(account, mapping()).

**Local steps**

- Return self.account\_meta.get(account, mapping()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L4343) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L843)

<a id="op-fe5e2cd4131101"></a>
### Filter Expression Parser.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_filter_expression_parser_initialize`

**Inputs** self.

**Local steps**

- Set self.validator from AccountFilterValidator().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L4434) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L838)

<a id="op-9082e7dd125cab"></a>
### Filter Expression Parser.build conditions

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_filter_expression_parser_build_conditions`

**Inputs** self, report\_rows, table, raise\_on\_invalid = false.

**Explicit results** no value · reduce(deferred anonymous expression, conditions).

**Local steps**

- Set conditions from list().
- For each row in (report\_rows or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in report\_rows → list().
  - Set condition from self.build\_condition(row, table, raise\_on\_invalid = raise\_on\_invalid).
  - If condition is distinct from no value.
    - Evaluate conditions.append(condition).
- If not conditions.
  - Return no value.
- Return reduce(deferred anonymous expression, conditions).

**Methods declared on this owner** [build condition](operations-039.md#op-105629254cc9fa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L4489) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L834)

<a id="op-105629254cc9fa"></a>
### Filter Expression Parser.build condition

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_filter_expression_parser_build_condition`

**Inputs** self, report\_row, table, raise\_on\_invalid = false.

**Explicit results** no value · self.\_build\_from\_parsed(parsed, table).

**Explicit failure paths** validation helper — text in the contract.join(error\_messages).

**Local steps**

- Set filter\_formula from report\_row.calculation\_formula.
- If not filter\_formula.
  - Return no value.
- Set errors from self.validator.validate\_filter(report\_row).
- If not errors.is\_valid.
  - Set error\_messages from list of str(issue) for issue drawn from errors.issues.
    - Draw issue from errors.issues.
  - If raise\_on\_invalid.
    - Call the validation error handler Platform.throw(text in the contract.join(error\_messages), title = translated “Invalid Filter”).
  - Evaluate Platform.log\_error(formatted text Filter validation errors found: {text in the contract.join(error\_messages)}).
  - Return no value.
- Attempt the following.
  - Set parsed from ast.literal\_eval(filter\_formula).
  - Return self.\_build\_from\_parsed(parsed, table).
- On failure (tuple(ValueError, SyntaxError)) bound to e.
  - Evaluate Platform.log\_error(formatted text Invalid filter formula syntax: {filter\_formula} - {e}).
  - Return no value.
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(formatted text Failed to build condition from formula: {filter\_formula} - {e}).
  - Return no value.

**Methods declared on this owner** [build from parsed](operations-039.md#op-04b652e6f0b17c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L4744) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L833)

<a id="op-04b652e6f0b17c"></a>
### Filter Expression Parser.build from parsed

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_filter_expression_parser_build_from_parsed`

**Inputs** self, parsed, table.

**Explicit results** self.\_build\_logical\_condition(parsed, table) · self.\_build\_simple\_condition(parsed, table) · no value.

**Local steps**

- If isinstance(parsed, dict).
  - Return self.\_build\_logical\_condition(parsed, table).
- If isinstance(parsed, list).
  - Return self.\_build\_simple\_condition(parsed, table).
- Return no value.

**Methods declared on this owner** [build logical condition](operations-040.md#op-ff111d53f6d0e0), [build simple condition](operations-039.md#op-848048cf2d16bc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L5287) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L835)

<a id="op-848048cf2d16bc"></a>
### Filter Expression Parser.build simple condition

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_filter_expression_parser_build_simple_condition`

**Inputs** self, condition\_list, table.

**Explicit results** no value · operator\_fn(field, value).

**Local steps**

- Set tuple(field\_name, operator, value) from condition\_list.
- If value is identical to no value.
  - Return no value.
- Set field from getattr(table, field\_name, no value).
- Set operator\_fn from OPERATOR\_MAP.get(operator.casefold()).
- If (“like” belongs to operator.casefold() and “%” does not belong to value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “like” belongs to operator.casefold() → “%” does not belong to value.
  - Set value from formatted text %{value}%.
- Return operator\_fn(field, value).

**Values supplied outside this operation** selected callable from getattr(table, field\_name, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L837)
