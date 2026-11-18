# Accounting and settlement · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Financial statements

<a id="op-46a292c5bf7753"></a>
### Apply additional conditions

`operation_enterprise_accounts_report_financial_statements_business_behavior_apply_additional_conditions`

**Inputs** doctype, query, from\_date, ignore\_closing\_entries, filters.

**Record and data access** read “Company” via get\_cached\_value · read “DocType” via get\_cached\_value.

**Explicit results** query.

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set gl\_entry from Platform.qb.DocType(doctype).
- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- If ignore\_closing\_entries.
  - If doctype equals “GL Entry”.
    - Set query from query.where(gl\_entry.voucher\_type differs from “Period Closing Voucher”).
  - Otherwise.
    - Set query from query.where(gl\_entry.is\_period\_closing\_voucher\_entry equals 0).
- If (from\_date and doctype equals “GL Entry”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → doctype equals “GL Entry”.
  - Set query from query.where(gl\_entry.posting\_date ≥ from\_date).
- If filters.
  - If filters.get(“project”).
    - If not isinstance(filters.get(“project”), list).
      - Set filters.project from Platform.parse\_json(filters.get(“project”)).
    - Set query from query.where(gl\_entry.project.isin(filters.project)).
  - If filters.get(“cost\_center”).
    - Set filters.cost\_center from get\_cost\_centers\_with\_children(filters.cost\_center).
    - Set query from query.where(gl\_entry.cost\_center.isin(filters.cost\_center)).
  - If filters.get(“include\_default\_book\_entries”).
    - Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
    - If (filters.finance\_book and company\_fb and cstr(filters.finance\_book) differs from cstr(company\_fb)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.finance\_book → company\_fb → cstr(filters.finance\_book) differs from cstr(company\_fb).
      - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
    - Set query from query.where((gl\_entry.finance\_book.isin(list(cstr(filters.finance\_book), cstr(company\_fb), empty text)) bitwise or gl\_entry.finance\_book.isnull())).
  - Otherwise.
    - Set query from query.where((gl\_entry.finance\_book.isin(list(cstr(filters.finance\_book), empty text)) bitwise or gl\_entry.finance\_book.isnull())).
- If accounting\_dimensions.
  - For each dimension in accounting\_dimensions.
    - If filters.get(dimension.fieldname).
      - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
        - Set filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, filters.get(dimension.fieldname)).
      - Set query from query.where(gl\_entry at dimension.fieldname.isin(filters at dimension.fieldname)).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”), Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L2151) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L912)

<a id="op-6cbb6da4adc909"></a>
### Get cost centers with children

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_cost_centers_with_children`

**Inputs** cost\_centers.

**Record and data access** read “Cost Center” via exists · read “Cost Center” via get\_value · read “Cost Center” via get\_all.

**Explicit results** list(set(all\_cost\_centers)).

**Explicit failure paths** validation helper — translated “Cost Center: {0} does not exist”.format(d).

**Local steps**

- If not isinstance(cost\_centers, list).
  - Set cost\_centers from list of d.strip() for d drawn from cost\_centers.strip().split(“,”) where d.
    - Draw d from cost\_centers.strip().split(“,”), keep a combination only if (d).
- Set all\_cost\_centers from list().
- For each d in cost\_centers.
  - If Platform.db.exists(“Cost Center”, d).
    - Set tuple(lft, rgt) from Platform.db.get\_value(“Cost Center”, d, list(“lft”, “rgt”)).
    - Set children from Platform.get\_all(“Cost Center”, filters = mapping(“lft” → list(“&gt;=”, lft), “rgt” → list(“&lt;=”, rgt))).
    - Update all\_cost\_centers using + list of c.name for c drawn from children.
      - Draw c from children.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Cost Center: {0} does not exist”.format(d)).
- Return list(set(all\_cost\_centers)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L3438) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L926)

<a id="op-706f5bfdab3756"></a>
### Get columns

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_columns`

**Inputs** periodicity, period\_list, accumulated\_values = 1, company = no value, cash\_flow = false, selected\_view = “Report”.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “account” when not cash\_flow, otherwise “section”, “label” → translated “Account” when not cash\_flow, otherwise translated “Section”, “fieldtype” → “Link”, “options” → “Account”, …)).
  - Value choice on not cash\_flow — true gives “account”, false gives “section”.
  - Value choice on not cash\_flow — true gives translated “Account”, false gives translated “Section”.
- If not cash\_flow.
  - Evaluate columns.extend(list(mapping(“fieldname” → “acc\_name”, “label” → translated “Account Name”, “fieldtype” → “Data”, “width” → 250, …), mapping(“fieldname” → “acc\_number”, “label” → translated “Account Number” ….
- If company.
  - Evaluate columns.append(mapping(“fieldname” → “currency”, “label” → translated “Currency”, “fieldtype” → “Link”, “options” → “Currency”, …)).
- Set seen\_dim\_values from set().
- For each period in period\_list.
  - Set col from mapping(“fieldname” → period.key, “label” → period.label, “fieldtype” → “Currency”, “options” → “currency”, …).
  - If dim\_value bound to period.get(“dimension\_value”).
    - Set col at “dimension\_value” from dim\_value.
    - If dim\_value does not belong to seen\_dim\_values.
      - Evaluate seen\_dim\_values.add(dim\_value).
      - Set col at “is\_first\_in\_dimension” from true.
  - Evaluate columns.append(col).
- If (selected\_view does not belong to tuple(“Growth”, “Margin”) and (is\_dimension\_grouped(period\_list) or (periodicity differs from “Yearly” and not accumulated\_values))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_view does not belong to tuple(“Growth”, “Margin”) → (is\_dimension\_grouped(period\_list) or (periodicity differs from “Yearly” and not accumulated\_values)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_dimension\_grouped(period\_list) → (periodicity differs from “Yearly” and not accumulated\_values).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in periodicity differs from “Yearly” → not accumulated\_values.
  - Evaluate columns.append(mapping(“fieldname” → “total”, “label” → translated “Total”, “fieldtype” → “Currency”, “width” → 150, …)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L3935) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L925)

<a id="op-6be4ba8dbf94fa"></a>
### Get filtered list for consolidated report

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_filtered_list_for_consolidated_report`

**Inputs** filters, period\_list.

**Explicit results** filtered\_summary\_list.

**Local steps**

- Set filtered\_summary\_list from list().
- For each period in period\_list.
  - If period equals filters.get(“company”).
    - Evaluate filtered\_summary\_list.append(period).
- Return filtered\_summary\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L5095) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L930)

<a id="op-8dd0446d63180e"></a>
### Compute growth view data

`operation_enterprise_accounts_report_financial_statements_business_behavior_compute_growth_view_data`

**Inputs** data, columns.

**Local steps**

- Set data\_copy from copy.deepcopy(data).
- For each row\_idx in range(len(data\_copy)).
  - If not data\_copy at row\_idx.
    - Continue with the next iteration or loop test.
  - For each column\_idx in range(1, len(columns)).
    - If columns at (column\_idx − 1).get(“dimension\_value”) differs from columns at column\_idx.get(“dimension\_value”).
      - Continue with the next iteration or loop test.
    - Set previous\_period\_key from columns at (column\_idx − 1).get(“key”).
    - Set current\_period\_key from columns at column\_idx.get(“key”).
    - Set current\_period\_value from data\_copy at row\_idx.get(current\_period\_key).
    - Set previous\_period\_value from data\_copy at row\_idx.get(previous\_period\_key).
    - Set annual\_growth from 0.
    - If current\_period\_value is identical to no value.
      - Set data at row\_idx at current\_period\_key from no value.
      - Continue with the next iteration or loop test.
    - If (previous\_period\_value equals 0 and current\_period\_value &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_period\_value equals 0 → current\_period\_value &gt; 0.
      - Set annual\_growth from 1.
    - Otherwise.
      - If previous\_period\_value &gt; 0.
        - Set annual\_growth from ((current\_period\_value − previous\_period\_value) ÷ previous\_period\_value).
    - Set growth\_percent from round((annual\_growth × 100), 2).
    - Set data at row\_idx at current\_period\_key from growth\_percent.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L5234) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L915)

<a id="op-22ce2101750aa4"></a>
### Compute margin view data

`operation_enterprise_accounts_report_financial_statements_business_behavior_compute_margin_view_data`

**Inputs** data, columns, base\_row.

**Explicit results** no value.

**Local steps**

- If (not columns or not base\_row).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not columns → not base\_row.
  - Return no value.
- Set data\_copy from copy.deepcopy(data).
- Set base\_row from copy.deepcopy(base\_row).
- For each row\_idx in range(len(data\_copy)).
  - Set row from data\_copy at row\_idx.
  - If not row.
    - Continue with the next iteration or loop test.
  - For each column in columns.
    - Set curr\_period from column.get(“key”).
    - Set base\_value from base\_row.get(curr\_period).
    - Set curr\_value from row.get(curr\_period).
    - If (base\_value is identical to no value or curr\_value is identical to no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in base\_value is identical to no value → curr\_value is identical to no value.
      - Set data at row\_idx at curr\_period from no value.
      - Continue with the next iteration or loop test.
    - If base\_value equals 0.
      - If curr\_value equals 0.
        - Set data at row\_idx at curr\_period from 0.
      - Otherwise.
        - Set data at row\_idx at curr\_period from no value.
      - Continue with the next iteration or loop test.
    - Set margin\_percent from round(((curr\_value ÷ base\_value) × 100), 2).
    - Set data at row\_idx at curr\_period from margin\_percent.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L916)

## Record · Fiscal year

[Record definition](../../../../data/record-types/fiscal_year.json)

<a id="op-3e84dc84ba7aef"></a>
### Fiscal Year.validate

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_fiscal_year_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate self.validate\_overlap().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-046.md#op-39e60fb05744d3), [validate overlap](operations-046.md#op-125d7e57f98f06).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0057.json#L3851) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1041)

<a id="op-5500003d482630"></a>
### Fiscal Year.on update

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_fiscal_year_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_fiscal\_year\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear fiscal year cache](operations-046.md#op-ffd3a7d28b91c9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1040)

<a id="op-85e2a9ae6d4879"></a>
### Fiscal Year.on trash

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_fiscal_year_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_fiscal\_year\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear fiscal year cache](operations-046.md#op-ffd3a7d28b91c9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1092) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1039)

<a id="op-ffd3a7d28b91c9"></a>
### Fiscal Year.clear fiscal year cache

`operation_enterprise_binding_enterprise_accounts_doctype_fiscal_year_fiscal_year_fiscalyear_clear_fiscal_year_cache`

**Inputs** self.

**Local steps**

- Set cache\_keys from list(“fiscal\_years”, “bootinfo”).
- Evaluate Platform.cache.delete\_value(cache\_keys).
- Evaluate Platform.db.after\_commit.add(deferred anonymous expression).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L795)

<a id="op-39e60fb05744d3"></a>
### Fiscal Year.validate dates

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_fiscal_year_validate_dates`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.exceptions.InvalidDates — translated “Fiscal Year End Date should be one year after Fiscal Year Start Date”.

**Local steps**

- Evaluate self.validate\_from\_to\_dates(“year\_start\_date”, “year\_end\_date”).
- If self.is\_short\_year.
  - Return no value.
- Set date from ((getdate(self.year\_start\_date) + relativedelta(years = 1)) − relativedelta(days = 1)).
- If getdate(self.year\_end\_date) differs from date.
  - Call the validation error handler Platform.throw(translated “Fiscal Year End Date should be one year after Fiscal Year Start Date”, Platform.exceptions.InvalidDates).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0057.json#L4052) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1042)

<a id="op-125d7e57f98f06"></a>
### Fiscal Year.validate overlap

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_fiscal_year_validate_overlap`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.NameError — translated “Year start date or end date is overlapping with {0}. To avoid please set company”.format(Platform.get\_desk\_link(“Fiscal Year”, existing.name, open\_in\_new\_tab = true)).

**Local steps**

- Set fy from Platform.qb.DocType(“Fiscal Year”).
- Set name from (self.name or self.year).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → self.year.
- Set existing\_fiscal\_years from nested operand in the contract(nested operand in the contract).select(fy.name).where(((nested operand in the contract.year\_start\_date ≤ nested operand in the contract.year\_end\_date bitwise and nested opera ….
- If existing\_fiscal\_years.
  - For each existing in existing\_fiscal\_years.
    - Set company\_for\_existing from Platform.db.sql\_list(query text (SELECT, Fiscal Year Company), existing.name).
    - Set overlap from false.
    - If (not self.get(“companies”) and not company\_for\_existing).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“companies”) → not company\_for\_existing.
      - Set overlap from true.
    - For each d in self.get(“companies”).
      - If d.company belongs to company\_for\_existing.
        - Set overlap from true.
    - If overlap.
      - Call the validation error handler Platform.throw(translated “Year start date or end date is overlapping with {0}. To avoid please set company”.format(Platform.get\_desk\_link(“Fiscal Year”, existing.name, open\_in\_new\_tab = true)), Platform.NameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1043)

<a id="op-60900835438006"></a>
### Auto create fiscal year

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_auto_create_fiscal_year`

**Inputs** no declared parameters.

**Record and data access** read “Fiscal Year” via get\_all · resolve a document from “Fiscal Year” via get\_doc.

**State and service calls** savepoint “auto\_create\_fiscal\_year” · request new\_doc for “Fiscal Year” · call insert on new\_fy · rollback.

**Explicit results** no value.

**Local steps**

- Set fy from Platform.qb.DocType(“Fiscal Year”).
- Set follow\_up\_date from add\_days(getdate(), days = 3).
- Set fiscal\_year from nested operand in the contract(nested operand in the contract).select(fy.name, fy.year\_end\_date).where((fy.year\_end\_date ≤ follow\_up\_date bitwise and fy.is\_short\_year equals 0)).run(as\_dict = true).
- If not fiscal\_year.
  - Return no value.
- Set existing\_years from set(Platform.get\_all(“Fiscal Year”, pluck = “name”)).
- For each d in fiscal\_year.
  - Set year\_start\_date from add\_days(d.year\_end\_date, 1).
  - Set year\_end\_date from add\_days(add\_years(year\_start\_date, 1), negative 1).
  - Set start\_year from cstr(year\_start\_date.year).
  - Set end\_year from cstr(year\_end\_date.year).
  - Set year from start\_year when start\_year equals end\_year, otherwise ((start\_year + “-”) + end\_year).
    - Value choice on start\_year equals end\_year — true gives start\_year, false gives ((start\_year + “-”) + end\_year).
  - If year belongs to existing\_years.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.db.savepoint(“auto\_create\_fiscal\_year”).
  - Attempt the following.
    - Set current\_fy from Platform.get\_doc(“Fiscal Year”, d.name).
    - Set new\_fy from Platform.new\_doc(“Fiscal Year”).
    - Set new\_fy.disabled from cint(current\_fy.disabled).
    - Set new\_fy.year\_start\_date from year\_start\_date.
    - Set new\_fy.year\_end\_date from year\_end\_date.
    - Set new\_fy.year from year.
    - For each row in current\_fy.companies.
      - Evaluate new\_fy.append(“companies”, mapping(“company” → row.company)).
    - Set new\_fy.auto\_created from 1.
    - Evaluate new\_fy.insert(ignore\_permissions = true).
    - Evaluate existing\_years.add(year).
  - On failure (Platform.NameError).
    - Evaluate Platform.db.rollback(save\_point = “auto\_create\_fiscal\_year”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1038)

<a id="op-ce2709fb52479d"></a>
### Get from and to date

`operation_enterprise_accounts_record_definitions_fiscal_year_business_behavior_get_from_and_to_date`

**Inputs** fiscal\_year.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** dict(from\_date = cached\_results.year\_start\_date, to\_date = cached\_results.year\_end\_date).

**Local steps**

- Set fields from list(“year\_start\_date”, “year\_end\_date”).
- Set cached\_results from Platform.get\_cached\_value(“Fiscal Year”, fiscal\_year, fields, as\_dict = 1).
- Return dict(from\_date = cached\_results.year\_start\_date, to\_date = cached\_results.year\_end\_date).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, fiscal\_year, fields, as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0057.json#L5716) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1044)

<a id="op-ee2eadd1be2e42"></a>
### Get data

`operation_enterprise_accounts_record_definitions_fiscal_year_fiscal_year_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “fiscal\_year”, “non\_standard\_fieldnames” → mapping(“Budget” → “from\_fiscal\_year”), “transactions” → list(mapping(“label” → translated “Budgets”, “items” → list(“Budget”)), mapping(“la ….

**Local steps**

- Return mapping(“fieldname” → “fiscal\_year”, “non\_standard\_fieldnames” → mapping(“Budget” → “from\_fiscal\_year”), “transactions” → list(mapping(“label” → translated “Budgets”, “items” → list(“Budget”)), mapping(“la ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0057.json#L5872) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1045)

## Report · General and payment ledger comparison

<a id="op-259dd19210ec35"></a>
### General Payment Ledger Comparison.initialize

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from filters.
- Set self.gle from list().
- Set self.ple from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L6521) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L951)

<a id="op-9f15ea51fa8317"></a>
### General Payment Ledger Comparison.get accounts

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_get_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Local steps**

- Set receivable\_accounts from list of x at 0 for x drawn from Platform.db.get\_all(“Account”, filters = mapping(“company” → self.filters.company, “account\_type” → “Receivable”), as\_list = true).
  - Draw x from Platform.db.get\_all(“Account”, filters = mapping(“company” → self.filters.company, “account\_type” → “Receivable”), as\_list = true).
- Set payable\_accounts from list of x at 0 for x drawn from Platform.db.get\_all(“Account”, filters = mapping(“company” → self.filters.company, “account\_type” → “Payable”), as\_list = true).
  - Draw x from Platform.db.get\_all(“Account”, filters = mapping(“company” → self.filters.company, “account\_type” → “Payable”), as\_list = true).
- Set self.account\_types from Platform.\_dict(mapping(“receivable” → Platform.\_dict(mapping(“accounts” → receivable\_accounts, “gle” → list(), “ple” → list())), “payable” → Platform.\_dict(mapping(“accounts” → payable\_accounts, “gle” → li ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L6612) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L947)

<a id="op-56ca2acaa50429"></a>
### General Payment Ledger Comparison.generate filters

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_generate_filters`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Local steps**

- If self.filters.account.
  - Set self.account\_types.receivable.accounts from list().
  - Set self.account\_types.payable.accounts from list().
  - For each acc in Platform.db.get\_all(“Account”, filters = mapping(“name” → list(“in”, self.filters.account)), fields = list(“name”, “account\_type”)).
    - If acc.account\_type equals “Receivable”.
      - Evaluate self.account\_types.receivable.accounts.append(acc.name).
    - Otherwise.
      - Evaluate self.account\_types.payable.accounts.append(acc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L7052) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L946)

<a id="op-026c0a3734e74f"></a>
### General Payment Ledger Comparison.get gle

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_get_general_ledger_entry`

**Inputs** self.

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- For each tuple(acc\_type, val) in self.account\_types.items().
  - If val.accounts.
    - Set filter\_criterion from list().
    - If self.filters.voucher\_no.
      - Evaluate filter\_criterion.append(gle.voucher\_no equals self.filters.voucher\_no).
    - If self.filters.period\_start\_date.
      - Evaluate filter\_criterion.append(gle.posting\_date.gte(self.filters.period\_start\_date)).
    - If self.filters.period\_end\_date.
      - Evaluate filter\_criterion.append(gle.posting\_date.lte(self.filters.period\_end\_date)).
    - If self.filters.party\_type.
      - Evaluate filter\_criterion.append(gle.party\_type.eq(self.filters.party\_type)).
    - If self.filters.party.
      - Evaluate filter\_criterion.append(gle.party.eq(self.filters.party)).
    - If acc\_type equals “receivable”.
      - Set outstanding from (Sum(gle.debit) − Sum(gle.credit)).as\_(“outstanding”).
      - Set outstanding\_in\_account\_currency from (Sum(gle.debit\_in\_account\_currency) − Sum(gle.credit\_in\_account\_currency)).as\_(“outstanding\_in\_account\_currency”).
    - Otherwise.
      - Set outstanding from (Sum(gle.credit) − Sum(gle.debit)).as\_(“outstanding”).
      - Set outstanding\_in\_account\_currency from (Sum(gle.credit\_in\_account\_currency) − Sum(gle.debit\_in\_account\_currency)).as\_(“outstanding\_in\_account\_currency”).
    - Set against\_voucher\_type from IfNull(NullIf(gle.against\_voucher\_type, empty text), gle.voucher\_type).
    - Set against\_voucher from IfNull(NullIf(gle.against\_voucher, empty text), gle.voucher\_no).
    - Set self.account\_types at acc\_type.gle from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.all(filter\_criterion)).groupby(gle.company, gle.account, gle.voucher\_type, gle.voucher\_no, …).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L949)

<a id="op-9201d7760ba397"></a>
### General Payment Ledger Comparison.get ple

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_get_ple`

**Inputs** self.

**Local steps**

- Set ple from qb.DocType(“Payment Ledger Entry”).
- For each tuple(acc\_type, val) in self.account\_types.items().
  - If val.accounts.
    - Set filter\_criterion from list().
    - If self.filters.voucher\_no.
      - Evaluate filter\_criterion.append(ple.voucher\_no equals self.filters.voucher\_no).
    - If self.filters.period\_start\_date.
      - Evaluate filter\_criterion.append(ple.posting\_date.gte(self.filters.period\_start\_date)).
    - If self.filters.period\_end\_date.
      - Evaluate filter\_criterion.append(ple.posting\_date.lte(self.filters.period\_end\_date)).
    - If self.filters.party\_type.
      - Evaluate filter\_criterion.append(ple.party\_type.eq(self.filters.party\_type)).
    - If self.filters.party.
      - Evaluate filter\_criterion.append(ple.party.eq(self.filters.party)).
    - Set self.account\_types at acc\_type.ple from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.all(filter\_criterion)).groupby(ple.company, ple.account, ple.voucher\_type, ple.voucher\_no, …).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L950)

<a id="op-b7d111c2211bec"></a>
### General Payment Ledger Comparison.compare

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_compare`

**Inputs** self.

**Local steps**

- Set self.gle\_balances from set().
- Set self.ple\_balances from set().
- For each tuple(\_acc\_type, val) in self.account\_types.items().
  - Set self.gle\_balances from (set(val.gle) bitwise or self.gle\_balances).
  - Set self.ple\_balances from (set(val.ple) bitwise or self.ple\_balances).
- Set self.ple\_balances from self.fold\_reconciled\_allocations().
- Set self.variation\_in\_payment\_ledger from self.gle\_balances.difference(self.ple\_balances).
- Set self.variation\_in\_general\_ledger from self.ple\_balances.difference(self.gle\_balances).
- Set self.diff from Platform.\_dict(mapping()).
- For each x in self.variation\_in\_payment\_ledger.
  - Set tuple(gl\_balance, gl\_balance\_in\_account\_currency) from x at slice KEY\_LENGTH to no value.
  - Set self.diff at x at slice no value to KEY\_LENGTH from Platform.\_dict(gl\_balance = gl\_balance, gl\_balance\_in\_account\_currency = gl\_balance\_in\_account\_currency).
- For each x in self.variation\_in\_general\_ledger.
  - Set tuple(pl\_balance, pl\_balance\_in\_account\_currency) from x at slice KEY\_LENGTH to no value.
  - Evaluate self.diff.setdefault(x at slice no value to KEY\_LENGTH, Platform.\_dict(mapping(“gl\_balance” → 0.0, “gl\_balance\_in\_account\_currency” → 0.0))).update(pl\_balance = pl\_balance, pl\_balance\_in\_account\_currency = ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [fold reconciled allocations](operations-046.md#op-560d6592be412f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L944)

<a id="op-560d6592be412f"></a>
### General Payment Ledger Comparison.fold reconciled allocations

`operation_enterprise_binding_enterprise_accounts_report_general_and_payment_ledger_comparison_general_and_payment_ledger_comparison_general_payment_ledger_comparison_fold_reconciled_allocations`

**Inputs** self.

**Declared result** set at tuple.

**Explicit results** set of tuple(expanded key, expanded amounts) for tuple(key, amounts) drawn from balances.items().

**Local steps**

- Set gl\_keys from set of row at slice no value to KEY\_LENGTH for row drawn from self.gle\_balances.
  - Draw row from self.gle\_balances.
- Set balances from mapping().
- For each row in self.ple\_balances.
  - Set tuple(key, unallocated) from tuple(row at slice no value to KEY\_LENGTH, tuple(expanded row at slice no value to 6, row at 2, row at 3)).
  - If (key does not belong to gl\_keys and unallocated belongs to gl\_keys).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in key does not belong to gl\_keys → unallocated belongs to gl\_keys.
    - Set key from unallocated.
  - Set balances at key from tuple(generator of flt((total + amount), 9) for tuple(total, amount) drawn from zip(balances at key, row at slice KEY\_LENGTH to no value, strict = true)) when key belongs to balances, otherwise row at slic ….
    - Value choice on key belongs to balances — true gives tuple(generator of flt((total + amount), 9) for tuple(total, amount) drawn from zip(balances at key, row at slice KEY\_LENGTH to no value, strict = true)), false gives row at slice KEY\_LENGTH to no value.
    - Draw tuple(total, amount) from zip(balances at key, row at slice KEY\_LENGTH to no value, strict = true).
- Return set of tuple(expanded key, expanded amounts) for tuple(key, amounts) drawn from balances.items().
  - Draw tuple(key, amounts) from balances.items().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1207)

<a id="op-936aa3b582767c"></a>
### General Payment Ledger Comparison.remove restricted parties

`operation_enterprise_binding_enterprise_accounts_report_general_and_payment_ledger_comparison_general_and_payment_ledger_comparison_general_payment_ledger_comparison_remove_restricted_parties`

**Inputs** self.

**Local steps**

- Set permitted from self.get\_permitted\_parties().
- Set self.diff from Platform.\_dict(mapping of key → val for tuple(key, val) drawn from self.diff.items() where tuple(key at 4, key at 5) belongs to permitted).
  - Draw tuple(key, val) from self.diff.items(), keep a combination only if (tuple(key at 4, key at 5) belongs to permitted).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permitted parties](operations-046.md#op-dfec94f9d501eb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1210)

<a id="op-dfec94f9d501eb"></a>
### General Payment Ledger Comparison.get permitted parties

`operation_enterprise_binding_enterprise_accounts_report_general_and_payment_ledger_comparison_general_and_payment_ledger_comparison_general_payment_ledger_comparison_get_permitted_parties`

**Inputs** self.

**Declared result** set at tuple at tuple(str, str).

**Record and data access** read party\_type via get\_list.

**Explicit results** permitted.

**Local steps**

- Set parties\_by\_type from mapping().
- For each key in self.diff.
  - Evaluate parties\_by\_type.setdefault(key at 4, set()).add(key at 5).
- Set permitted from set().
- For each tuple(party\_type, parties) in parties\_by\_type.items().
  - If (not party\_type or not Platform.has\_permission(party\_type, “read”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not party\_type → not Platform.has\_permission(party\_type, “read”).
    - Continue with the next iteration or loop test.
  - Set names from Platform.get\_list(party\_type, filters = mapping(“name” → list(“in”, list(parties))), pluck = “name”).
  - Evaluate permitted.update(generator of tuple(party\_type, name) for name drawn from names).
    - Draw name from names.
- Return permitted.

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1209)
