# Accounting and settlement · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Deferred revenue and expense

<a id="op-520885f8fba88f"></a>
### Deferred Invoice.report data

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_invoice_report_data`

**Inputs** self.

**Explicit results** ret\_data.

**Local steps**

- Set ret\_data from list().
- Set inv\_total from Platform.\_dict(mapping(“name” → self.name, “amount” → self.amount\_total)).
- For each x in self.period\_total.
  - Set inv\_total at x.key from x.total.
  - Set inv\_total.indent from 0.
- Evaluate ret\_data.append(inv\_total).
- Evaluate list(map(deferred anonymous expression, self.items)).
- Return ret\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L6528) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L845)

<a id="op-d8b4ad0b48ee95"></a>
### Deferred Revenue and Expense Report.initialize

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_initialize`

**Inputs** self, filters = no value.

**Record and data access** resolve a document from “Fiscal Year” via get\_doc.

**Local steps**

- If not filters.
  - Set fiscal\_year from Platform.get\_doc(“Fiscal Year”, get\_fiscal\_year(date = getdate())).
  - Set self.filters from Platform.\_dict(mapping(“company” → Platform.defaults.get\_user\_default(“Company”), “filter\_based\_on” → “Fiscal Year”, “period\_start\_date” → fiscal\_year.year\_start\_date, “period\_end\_date” → fiscal\_year.year\_ ….
- Otherwise.
  - Set self.filters from Platform.\_dict(filters).
- Set self.filters.book\_deferred\_entries\_based\_on from Platform.db.get\_singles\_value(“Accounts Settings”, “book\_deferred\_entries\_based\_on”).
- Set self.period\_list from no value.
- Set self.deferred\_invoices from list().
- Set self.period\_total from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L6815) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L862)

<a id="op-e9f7d1829c497f"></a>
### Deferred Revenue and Expense Report.get period list

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_get_period_list`

**Inputs** self.

**Local steps**

- Set self.period\_list from get\_period\_list(self.filters.from\_fiscal\_year, self.filters.to\_fiscal\_year, self.filters.period\_start\_date, self.filters.period\_end\_date, company = self.filters.company, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L7292) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L861)

<a id="op-1c0d362720a689"></a>
### Deferred Revenue and Expense Report.get invoices

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_get_invoices`

**Inputs** self.

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Set posted from Column(“posted”).
- If self.filters.type equals “Revenue”.
  - Set invoice\_doctype from “Sales Invoice”.
  - Set inv from qb.DocType(invoice\_doctype).
  - Set inv\_item from qb.DocType(“Sales Invoice Item”).
  - Set deferred\_flag\_field from inv\_item at “enable\_deferred\_revenue”.
  - Set deferred\_account\_field from inv\_item at “deferred\_revenue\_account”.
- Otherwise.
  - If self.filters.type equals “Expense”.
    - Set invoice\_doctype from “Purchase Invoice”.
    - Set inv from qb.DocType(invoice\_doctype).
    - Set inv\_item from qb.DocType(“Purchase Invoice Item”).
    - Set deferred\_flag\_field from inv\_item at “enable\_deferred\_expense”.
    - Set deferred\_account\_field from inv\_item at “deferred\_expense\_account”.
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If match\_conditions bound to build\_match\_conditions(invoice\_doctype).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set self.invoices from query.run(as\_dict = true).
- Set uniq\_invoice from set(list of x.doc for x drawn from self.invoices).
  - Draw x from self.invoices.
- For each inv in uniq\_invoice.
  - Evaluate self.deferred\_invoices.append(Deferred\_Invoice(inv, list of x for x drawn from self.invoices where x.doc equals inv, self.filters, self.period\_list)).
    - Draw x from self.invoices, keep a combination only if (x.doc equals inv).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L860)

<a id="op-0a491fa789b072"></a>
### Deferred Revenue and Expense Report.estimate future

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_estimate_future`

**Inputs** self.

**Local steps**

- For each x in self.deferred\_invoices.
  - Evaluate x.estimate\_future().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L1541) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L857)

<a id="op-8911af9b1c0c66"></a>
### Deferred Revenue and Expense Report.calculate revenue and expense

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_calculate_revenue_and_expense`

**Inputs** self.

**Local steps**

- For each period in self.period\_list.
  - Evaluate self.period\_total.append(Platform.\_dict(mapping(“key” → period.key, “total” → 0, “actual” → 0))).
- For each inv in self.deferred\_invoices.
  - Set inv\_total from inv.calculate\_invoice\_revenue\_expense\_for\_period().
  - For each idx in range(len(self.period\_list)).
    - Update self.period\_total at idx.total using + inv\_total at idx.total.
    - Update self.period\_total at idx.actual using + inv\_total at idx.actual.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L1609) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L856)

<a id="op-dc2d38cd970f22"></a>
### Deferred Revenue and Expense Report.get columns

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_get_columns`

**Inputs** self.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- Evaluate columns.append(mapping(“label” → translated “Name”, “fieldname” → “name”, “fieldtype” → “Data”, “read\_only” → 1)).
- Evaluate columns.append(mapping(“label” → translated “Service Start Date”, “fieldname” → “service\_start\_date”, “fieldtype” → “Date”, “read\_only” → 1)).
- Evaluate columns.append(mapping(“label” → translated “Service End Date”, “fieldname” → “service\_end\_date”, “fieldtype” → “Date”, “read\_only” → 1)).
- Evaluate columns.append(mapping(“label” → translated “Amount”, “fieldname” → “amount”, “fieldtype” → “Currency”, “read\_only” → 1)).
- For each period in self.period\_list.
  - Evaluate columns.append(mapping(“label” → translated period.label, “fieldname” → period.key, “fieldtype” → “Currency”, “read\_only” → 1)).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L1912) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L859)

<a id="op-72376bc78fb93b"></a>
### Deferred Revenue and Expense Report.generate report data

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_generate_report_data`

**Inputs** self.

**Explicit results** ret.

**Local steps**

- Set ret from list().
- For each inv in self.deferred\_invoices.
  - Update ret using + inv.report\_data().
- Update ret using + list(mapping()).
- If self.filters.type equals “Revenue”.
  - Set total\_row from Platform.\_dict(mapping(“name” → “Total Deferred Income”)).
- Otherwise.
  - If self.filters.type equals “Expense”.
    - Set total\_row from Platform.\_dict(mapping(“name” → “Total Deferred Expense”)).
- Set total\_row at “amount” from sum(generator of inv.amount\_total for inv drawn from self.deferred\_invoices).
  - Draw inv from self.deferred\_invoices.
- For each tuple(idx, period) in enumerate(self.period\_list, 0).
  - Set total\_row at period.key from self.period\_total at idx.total.
- Evaluate ret.append(total\_row).
- Return ret.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L2523) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L858)

<a id="op-71cc767922d4d9"></a>
### Deferred Revenue and Expense Report.prepare chart

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_prepare_chart`

**Inputs** self.

**Explicit results** chart.

**Local steps**

- Set chart from mapping(“data” → mapping(“labels” → list of period.label for period drawn from self.period\_list, “datasets” → list(mapping(“name” → translated “Actual Posting”, “chartType” → “bar”, “values” → list of x.ac ….
  - Draw period from self.period\_list.
  - Draw x from self.period\_total.
- If self.filters.with\_upcoming\_postings.
  - Evaluate chart at “data” at “datasets”.append(mapping(“name” → translated “Expected”, “chartType” → “line”, “values” → list of x.total for x drawn from self.period\_total)).
    - Draw x from self.period\_total.
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L2954) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L863)

<a id="op-8ea3518fee7eba"></a>
### Deferred Revenue and Expense Report.run

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_revenue_and_expense_report_run`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate self.deferred\_invoices.clear().
- Evaluate self.get\_period\_list().
- Evaluate self.get\_invoices().
- If self.filters.with\_upcoming\_postings.
  - Evaluate self.estimate\_future().
- Evaluate self.calculate\_revenue\_and\_expense().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period list](operations-034.md#op-e9f7d1829c497f), [get invoices](operations-034.md#op-1c0d362720a689), [estimate future](operations-034.md#op-0a491fa789b072), [calculate revenue and expense](operations-034.md#op-8911af9b1c0c66).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L3394) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L864)

<a id="op-c0950d9574eb27"></a>
### Execute

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, message, chart).

**Local steps**

- Set report from Deferred\_Revenue\_and\_Expense\_Report(filters = filters).
- Evaluate report.run().
- Set columns from report.get\_columns().
- Set data from report.generate\_report\_data().
- Set message from list().
- Set chart from report.prepare\_chart().
- Return tuple(columns, data, message, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0243.json#L3556) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L865)

## Report · Delivered items to be billed

<a id="op-c50f00bc3484ac"></a>
### Execute

`operation_enterprise_accounts_report_delivered_items_to_be_billed_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_column().
- Set args from get\_args().
- Set data from get\_ordered\_to\_be\_billed\_data(args, filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0244.json#L2495) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L873)

<a id="op-75b197db5564d1"></a>
### Get column

`operation_enterprise_accounts_report_delivered_items_to_be_billed_business_behavior_get_column`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Delivery Note”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Delivery Note”, …), mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Dat ….

**Local steps**

- Return list(mapping(“label” → translated “Delivery Note”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Delivery Note”, …), mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Dat ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0244.json#L2620) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L875)

<a id="op-90951484d6c946"></a>
### Get args

`operation_enterprise_accounts_report_delivered_items_to_be_billed_business_behavior_get_arguments`

**Inputs** no declared parameters.

**Explicit results** mapping(“doctype” → “Delivery Note”, “party” → “customer”, “date” → “posting\_date”, “order” → “name”, …).

**Local steps**

- Return mapping(“doctype” → “Delivery Note”, “party” → “customer”, “date” → “posting\_date”, “order” → “name”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0244.json#L3869) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L874)

## Report · Dimension wise accounts balance report

<a id="op-6ea8373cbe3c26"></a>
### Execute

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list()) · tuple(columns, data).

**Local steps**

- Evaluate validate\_filters(filters).
- Set dimension\_list from get\_dimensions(filters).
- If not dimension\_list.
  - Return tuple(list(), list()).
- Set columns from get\_columns(dimension\_list).
- Set data from get\_data(filters, dimension\_list).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0244.json#L5269) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L882)

<a id="op-70d8c72d543a71"></a>
### Get data

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_get_data`

**Inputs** filters, dimension\_list.

**Record and data access** execute query text (SELECT, Account).

**Explicit results** no value · out.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(filters.company).
- Set acc from Platform.db.sql(query text (SELECT, Account), filters.company, as\_dict = true).
- If not acc.
  - Return no value.
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(acc).
- Set tuple(min\_lft, max\_rgt) from Platform.db.sql(query text (SELECT, Account), filters.company) at 0.
- Set account from Platform.db.sql\_list(query text (SELECT, Account), tuple(min\_lft, max\_rgt, filters.company)).
- Set gl\_entries\_by\_account from mapping().
- Evaluate set\_gl\_entries\_by\_account(dimension\_list, filters, account, gl\_entries\_by\_account).
- Evaluate format\_gl\_entries(gl\_entries\_by\_account, accounts\_by\_name, dimension\_list, Platform.scrub(filters.get(“dimension”))).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name, dimension\_list).
- Set out from prepare\_data(accounts, filters, company\_currency, dimension\_list).
- Set out from filter\_out\_zero\_value\_rows(out, parent\_children\_map).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L885)

<a id="op-e73d490e560bf1"></a>
### Set gl entries by account

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_set_general_ledger_entries_by_account`

**Inputs** dimension\_list, filters, account, gl\_entries\_by\_account.

**Record and data access** read “Company” via get\_cached\_value · execute query text (SELECT, GL Entry).format(dimension = Platform.scrub(filters.get(“dimension”)), condition = condition).

**Local steps**

- Set condition from get\_condition(filters.get(“dimension”)).
- If account.
  - Update condition using + “ and account in ({})”.format(“, ”.join(list of Platform.db.escape(d) for d drawn from account)).
    - Draw d from account.
- Set gl\_filters from mapping(“company” → filters.get(“company”), “from\_date” → filters.get(“from\_date”), “to\_date” → filters.get(“to\_date”), “finance\_book” → cstr(filters.get(“finance\_book”))).
- Set gl\_filters at “dimensions” from tuple(set(dimension\_list)).
- If filters.get(“include\_default\_book\_entries”).
  - Set gl\_filters at “company\_fb” from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
- Set gl\_entries from Platform.db.sql(query text (SELECT, GL Entry).format(dimension = Platform.scrub(filters.get(“dimension”)), condition = condition), gl\_filters, as\_dict = true).
- For each entry in gl\_entries.
  - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L888)

<a id="op-d3da816433c92e"></a>
### Format gl entries

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_format_general_ledger_entries`

**Inputs** gl\_entries\_by\_account, accounts\_by\_name, dimension\_list, dimension\_type.

**State and service calls** msgprint with translated “Could not retrieve information for {0}.”.format(entry.account).

**Local steps**

- For each entries in gl\_entries\_by\_account.values().
  - For each entry in entries.
    - Set d from accounts\_by\_name.get(entry.account).
    - If not d.
      - Evaluate Platform.msgprint(translated “Could not retrieve information for {0}.”.format(entry.account), title = “Error”, raise\_exception = 1).
    - For each dimension in dimension\_list.
      - If dimension equals entry.get(dimension\_type).
        - Set d at Platform.scrub(dimension) from ((d.get(Platform.scrub(dimension), 0.0) + flt(entry.debit)) − flt(entry.credit)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0244.json#L6854) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L883)

<a id="op-73e8d16aa33b23"></a>
### Prepare data

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_prepare_data`

**Inputs** accounts, filters, company\_currency, dimension\_list.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each d in accounts.
  - Set has\_value from false.
  - Set total from 0.
  - Set row from mapping(“account” → d.name, “is\_group” → d.is\_group, “parent\_account” → d.parent\_account, “indent” → d.indent, …).
    - Value choice on d.account\_number — true gives formatted text {d.account\_number} - {d.account\_name}, false gives d.account\_name.
  - For each dimension in dimension\_list.
    - Set row at Platform.scrub(dimension) from flt(d.get(Platform.scrub(dimension), 0.0), 3).
    - If abs(row at Platform.scrub(dimension)) ≥ get\_zero\_cutoff(company\_currency).
      - Set has\_value from true.
      - Update total using + flt(d.get(Platform.scrub(dimension), 0.0), 3).
  - Set row at “has\_value” from has\_value.
  - Set row at “total” from total.
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L887)

<a id="op-2eba3aeec4e59c"></a>
### Accumulate values into parents

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_accumulate_values_into_parents`

**Inputs** accounts, accounts\_by\_name, dimension\_list.

**Local steps**

- For each d in reversed(accounts).
  - If d.parent\_account.
    - For each dimension in dimension\_list.
      - Set accounts\_by\_name at d.parent\_account at Platform.scrub(dimension) from (accounts\_by\_name at d.parent\_account.get(Platform.scrub(dimension), 0.0) + d.get(Platform.scrub(dimension), 0.0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L664) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L881)

<a id="op-f2a99e105d34e4"></a>
### Get condition

`operation_enterprise_binding_enterprise_accounts_report_dimension_wise_accounts_balance_report_dimension_wise_accounts_balance_report_get_condition`

**Inputs** dimension.

**Explicit results** “ and {}”.format(“ and ”.join(conditions)) when conditions, otherwise empty text.

**Local steps**

- Set conditions from list().
- Evaluate conditions.append(formatted text {Platform.scrub(dimension)} in %(dimensions)s).
- Return “ and {}”.format(“ and ”.join(conditions)) when conditions, otherwise empty text.
  - Value choice on conditions — true gives “ and {}”.format(“ and ”.join(conditions)), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1199)

<a id="op-c1930226e64634"></a>
### Get dimensions

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_get_dimensions`

**Inputs** filters.

**Record and data access** read filters.get(“dimension”) via get\_list.

**Explicit results** Platform.get\_list(filters.get(“dimension”), filters = query\_filters, pluck = “name”).

**Local steps**

- Set meta from Platform.get\_meta(filters.get(“dimension”), cached = false).
- Set query\_filters from mapping().
- If meta.has\_field(“company”).
  - Set query\_filters from mapping(“company” → filters.get(“company”)).
- Return Platform.get\_list(filters.get(“dimension”), filters = query\_filters, pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L886)

<a id="op-154111f1ff2a4a"></a>
### Get columns

`operation_enterprise_accounts_report_dimension_wise_accounts_balance_report_business_behavior_get_columns`

**Inputs** dimension\_list.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “account”, “label” → translated “Account”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“fieldname” → “currency”, “label” → translated “Currency”, “fieldtype” → “Link ….
- For each dimension in dimension\_list.
  - Evaluate columns.append(mapping(“fieldname” → Platform.scrub(dimension), “label” → dimension, “fieldtype” → “Currency”, “options” → “currency”, …)).
- Evaluate columns.append(mapping(“fieldname” → “total”, “label” → translated “Total”, “fieldtype” → “Currency”, “options” → “currency”, …)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0245.json#L1153) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L884)

## Record · Dunning

[Record definition](../../../../data/record-types/dunning.json)

<a id="op-609134641efdf2"></a>
### Dunning.validate

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_currency().
- Evaluate self.set\_dunning\_fee().
- Evaluate self.validate\_overdue\_payment\_references().
- Evaluate self.validate\_overdue\_payments().
- Evaluate self.validate\_totals().
- <a id="op-609134641efdf2-guard-7"></a>If self.docstatus equals 0.
  - Set self.status from “Draft”.
  - Set self.superseded\_by from no value.
- Evaluate self.set\_party\_details().
- Evaluate self.set\_dunning\_level().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that assigns “Draft” to self.status. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-609134641efdf2-guard-7)

**Methods declared on this owner** [validate currency](operations-035.md#op-460cb59076c542), [set dunning fee](operations-035.md#op-90f179a081118c), [validate overdue payment references](operations-035.md#op-cad8b56f60213a), [validate overdue payments](operations-035.md#op-68e1ea5202fb89), [validate totals](operations-035.md#op-9d9424a8f72fa3), [set party details](operations-035.md#op-51903ffdf468ae), [set dunning level](operations-035.md#op-e1b4d3b6b637cb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L711)
