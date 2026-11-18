# Inventory and warehouses · operations 71

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock and account value comparison

<a id="op-83d49e4f9ffadf"></a>
### Repost based on transaction

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_repost_based_on_transaction`

**Inputs** rows, company = no value, entries = no value.

**Record and data access** read “Purchase Invoice” via get\_cached\_value · resolve a document from mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Transaction”, “status” → “Queued”, “voucher\_type” → row.get(“voucher\_type”), …) via get\_doc.

**State and service calls** savepoint “repost\_based\_on\_transaction” · call submit on Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Transaction”, “status” → “Queued”, “voucher\_type” → row.get(“voucher\_type”), …)) · rollback.

**Local steps**

- If entries is identical to no value.
  - Set entries from list().
- Set duplicate\_vouchers from set().
- For each row in rows.
  - If (row.get(“voucher\_type”) equals “Purchase Invoice” and Platform.get\_cached\_value(“Purchase Invoice”, row.get(“voucher\_no”), “update\_stock”) equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“voucher\_type”) equals “Purchase Invoice” → Platform.get\_cached\_value(“Purchase Invoice”, row.get(“voucher\_no”), “update\_stock”) equals 0.
    - Continue with the next iteration or loop test.
  - If row.get(“voucher\_type”) belongs to list(“Purchase Receipt”, “Purchase Invoice”).
    - Set voucher\_key from tuple(row.get(“voucher\_type”), row.get(“voucher\_no”)).
    - If voucher\_key belongs to duplicate\_vouchers.
      - Continue with the next iteration or loop test.
    - Evaluate duplicate\_vouchers.add(voucher\_key).
    - Evaluate Platform.db.savepoint(“repost\_based\_on\_transaction”).
    - Attempt the following.
      - Set doc from Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Transaction”, “status” → “Queued”, “voucher\_type” → row.get(“voucher\_type”), …)).submit().
      - Evaluate entries.append(get\_link\_to\_form(“Repost Item Valuation”, doc.name)).
    - On failure (Platform.DuplicateEntryError).
      - Evaluate Platform.db.rollback(save\_point = “repost\_based\_on\_transaction”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Purchase Invoice”, row.get(“voucher\_no”), “update\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0912.json#L3693) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L843) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L455)

<a id="op-a0c9c55e167608"></a>
### Create gl reposting entries

`operation_enterprise_binding_enterprise_stock_report_stock_and_account_value_comparison_stock_and_account_value_comparison_create_gl_reposting_entries`

**Inputs** rows, company, from\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Transaction”, “status” → “Queued”, “voucher\_type” → voucher\_type, …) via get\_doc.

**State and service calls** call submit on doc · msgprint with translated “GL reposting entries created: {0}”.format(“, ”.join(entries)) · msgprint with translated “No new GL reposting entries were created for the selected rows.”.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Only users with the {0} role can repost GL entries”.format(Platform.bold(translated “Accounts Manager”)) · validation helper — translated “Please select rows to create GL Reposting Entries”.

**Local steps**

- If “Accounts Manager” does not belong to Platform.get\_roles().
  - Call the validation error handler Platform.throw(translated “Only users with the {0} role can repost GL entries”.format(Platform.bold(translated “Accounts Manager”)), Platform.PermissionError).
- If isinstance(rows, str).
  - Set rows from parse\_json(rows).
- If not rows.
  - Call the validation error handler Platform.throw(translated “Please select rows to create GL Reposting Entries”).
- Set entries from list().
- Set processed\_vouchers from set().
- Set vouchers from list().
- For each row in rows.
  - If not isinstance(row, dict).
    - Continue with the next iteration or loop test.
  - Set tuple(voucher\_type, voucher\_no) from tuple(row.get(“voucher\_type”), row.get(“voucher\_no”)).
  - If (isinstance(voucher\_type, str) and isinstance(voucher\_no, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(voucher\_type, str) → isinstance(voucher\_no, str).
    - Evaluate vouchers.append(tuple(voucher\_type, voucher\_no)).
- Set stock\_vouchers from get\_stock\_voucher\_postings(vouchers, company).
- If from\_date.
  - Set from\_date from getdate(from\_date).
  - Set stock\_vouchers from mapping of key → posting for tuple(key, posting) drawn from stock\_vouchers.items() where getdate(posting.posting\_date) ≥ from\_date.
    - Draw tuple(key, posting) from stock\_vouchers.items(), keep a combination only if (getdate(posting.posting\_date) ≥ from\_date).
- Evaluate validate\_closed\_periods(stock\_vouchers, company).
- Set pending\_vouchers from get\_pending\_gl\_reposting\_vouchers(list(stock\_vouchers)).
- For each tuple(voucher\_type, voucher\_no) in vouchers.
  - Set posting from stock\_vouchers.get(tuple(voucher\_type, voucher\_no)).
  - If not posting.
    - Continue with the next iteration or loop test.
  - If tuple(voucher\_type, voucher\_no) belongs to processed\_vouchers.
    - Continue with the next iteration or loop test.
  - Evaluate processed\_vouchers.add(tuple(voucher\_type, voucher\_no)).
  - If tuple(voucher\_type, voucher\_no) belongs to pending\_vouchers.
    - Continue with the next iteration or loop test.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Transaction”, “status” → “Queued”, “voucher\_type” → voucher\_type, …)).
  - Evaluate doc.submit().
  - Evaluate entries.append(get\_link\_to\_form(“Repost Item Valuation”, doc.name)).
- If entries.
  - If len(entries) &gt; 20.
    - Set entries from (entries at slice no value to 20 + list(“...”)).
  - Evaluate Platform.msgprint(translated “GL reposting entries created: {0}”.format(“, ”.join(entries))).
- Otherwise.
  - Evaluate Platform.msgprint(translated “No new GL reposting entries were created for the selected rows.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L999)

<a id="op-8721f82e4590ae"></a>
### Validate closed periods

`operation_enterprise_binding_enterprise_stock_report_stock_and_account_value_comparison_stock_and_account_value_comparison_validate_closed_periods`

**Inputs** stock\_vouchers, company.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — text in the contract.join(messages).

**Local steps**

- If not stock\_vouchers.
  - Return no value.
- Set last\_pcv\_date from Platform.db.get\_value(“Period Closing Voucher”, mapping(“docstatus” → 1, “company” → company), list(mapping(“MAX” → “period\_end\_date”))).
- Set last\_pcv\_date from getdate(last\_pcv\_date) when last\_pcv\_date, otherwise no value.
  - Value choice on last\_pcv\_date — true gives getdate(last\_pcv\_date), false gives no value.
- Set closed\_periods from get\_closed\_accounting\_periods(company).
- Set tuple(pcv\_vouchers, accounting\_period\_vouchers) from tuple(list(), list()).
- For each tuple(tuple(voucher\_type, voucher\_no), posting) in stock\_vouchers.items().
  - Set posting\_date from getdate(posting.posting\_date).
  - Set link from get\_link\_to\_form(voucher\_type, voucher\_no).
  - If (last\_pcv\_date and posting\_date ≤ last\_pcv\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_pcv\_date → posting\_date ≤ last\_pcv\_date.
    - Evaluate pcv\_vouchers.append(link).
    - Continue with the next iteration or loop test.
  - For each period in closed\_periods.
    - If (period.document\_type equals voucher\_type and period.start\_date ≤ posting\_date ≤ period.end\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in period.document\_type equals voucher\_type → period.start\_date ≤ posting\_date ≤ period.end\_date.
      - Compare adjacent operands in order, stopping at the first false comparison in period.start\_date ≤ posting\_date ≤ period.end\_date.
      - Evaluate accounting\_period\_vouchers.append(translated “{0} (Accounting Period {1})”.format(link, Platform.bold(period.name))).
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set messages from list().
- If pcv\_vouchers.
  - Evaluate messages.append(translated “Books are closed till {0} by Period Closing Voucher, remove these rows: {1}”.format(Platform.bold(Platform.format(last\_pcv\_date, “Date”)), “, ”.join(pcv\_vouchers))).
- If accounting\_period\_vouchers.
  - Evaluate messages.append(translated “These rows fall in a closed Accounting Period, remove them: {0}”.format(“, ”.join(accounting\_period\_vouchers))).
- If messages.
  - Call the validation error handler Platform.throw(text in the contract.join(messages), title = translated “Closed Period Rows Selected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1003)

<a id="op-9680274e149047"></a>
### Get closed accounting periods

`operation_enterprise_binding_enterprise_stock_report_stock_and_account_value_comparison_stock_and_account_value_comparison_get_closed_accounting_periods`

**Inputs** company.

**Explicit results** list of d for d drawn from periods where not (d.exempted\_role and d.exempted\_role belongs to roles).

**Local steps**

- Set ap from Platform.qb.DocType(“Accounting Period”).
- Set cd from Platform.qb.DocType(“Closed Document”).
- Set periods from nested operand in the contract(nested operand in the contract).select(ap.name, ap.start\_date, ap.end\_date, ap.exempted\_role, …).where(((nested operand in the contract.company equals company bitwise and nes ….
- Set roles from Platform.get\_roles().
- Return list of d for d drawn from periods where not (d.exempted\_role and d.exempted\_role belongs to roles).
  - Draw d from periods, keep a combination only if (not (d.exempted\_role and d.exempted\_role belongs to roles)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.exempted\_role → d.exempted\_role belongs to roles.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1000)

<a id="op-a07e410b1f2ea9"></a>
### Get stock voucher postings

`operation_enterprise_binding_enterprise_stock_report_stock_and_account_value_comparison_stock_and_account_value_comparison_get_stock_voucher_postings`

**Inputs** vouchers, company.

**Declared result** dict at tuple(tuple at tuple(str, str), Platform.\_dict).

**Explicit results** postings.

**Local steps**

- Set postings from mapping().
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- For each chunk in create\_batch(list(set(vouchers)), 1000).
  - Set chunk from set(chunk).
  - Set entries from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise ….
    - Draw tuple(\_, voucher\_no) from chunk.
  - For each d in entries.
    - If tuple(d.voucher\_type, d.voucher\_no) belongs to chunk.
      - Set postings at tuple(d.voucher\_type, d.voucher\_no) from d.
- Return postings.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1002)

<a id="op-7acd02937e05c8"></a>
### Get pending gl reposting vouchers

`operation_enterprise_binding_enterprise_stock_report_stock_and_account_value_comparison_stock_and_account_value_comparison_get_pending_gl_reposting_vouchers`

**Inputs** transactions.

**Declared result** set at tuple at tuple(str, str).

**Record and data access** read “Repost Item Valuation” via get\_all.

**Explicit results** pending\_vouchers.

**Local steps**

- Set pending\_vouchers from set().
- For each chunk in create\_batch(transactions, 1000).
  - Set entries from Platform.get\_all(“Repost Item Valuation”, filters = mapping(“based\_on” → “Transaction”, “repost\_only\_accounting\_ledgers” → 1, “docstatus” → 1, “status” → tuple(“in”, list(“Queued”, “In Progress”)), …), fie ….
    - Draw tuple(\_, voucher\_no) from chunk.
  - Evaluate pending\_vouchers.update(generator of tuple(d.voucher\_type, d.voucher\_no) for d drawn from entries).
    - Draw d from entries.
- Return pending\_vouchers.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1001)

## Report · Stock balance

<a id="op-95270c52872739"></a>
### Execute

`operation_enterprise_stock_report_stock_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** StockBalanceReport(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return StockBalanceReport(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L849) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L459)

<a id="op-2ded19c0822517"></a>
### Execute snapshot report

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_execute_snapshot_report`

**Inputs** filters = no value.

**Explicit results** execute\_from\_snapshot(filters).

**Local steps**

- Bind dependencies execute\_from\_snapshot.
- Evaluate validate\_date\_range(filters).
- Return execute\_from\_snapshot(filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1004)

<a id="op-0ed5140940b9f4"></a>
### Stock Balance Report.initialize

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_initialize`

**Inputs** self, filters.

**Declared result** no value.

**Local steps**

- Set self.filters from filters.
- Set self.from\_date from getdate(filters.get(“from\_date”)).
- Set self.to\_date from getdate(filters.get(“to\_date”)).
- Set self.start\_from from no value.
- Set self.data from list().
- Set self.columns from list().
- Set self.sle\_entries from list().
- Set self.item\_warehouse\_balances from mapping().
- Set self.latest\_valuation\_rates from mapping().
- Evaluate self.set\_company\_currency().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set company currency](operations-071.md#op-438b7e8415a2d5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L478)

<a id="op-438b7e8415a2d5"></a>
### Stock Balance Report.set company currency

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_set_company_currency`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Global Defaults” via get\_single\_value.

**Local steps**

- If self.filters.get(“company”).
  - Set self.company\_currency from Enterprise.get\_company\_currency(self.filters.get(“company”)).
- Otherwise.
  - Set self.company\_currency from Platform.db.get\_single\_value(“Global Defaults”, “default\_currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0912.json#L7087) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L487)

<a id="op-f1cc75c8fa0902"></a>
### Stock Balance Report.run

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Set self.float\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 3.
- Set self.item\_warehouse\_map from Platform.\_dict(mapping()).
- Set self.inventory\_dimensions from self.get\_inventory\_dimension\_fields().
- Evaluate self.prepare\_opening\_stock().
- Evaluate self.prepare\_sle\_query().
- Evaluate self.prepare\_item\_warehouse\_map\_for\_current\_period().
- Evaluate self.set\_pool\_rate\_on\_dimension\_rows().
- Evaluate self.prepare\_new\_data().
- If not self.columns.
  - Set self.columns from self.get\_columns().
- Evaluate self.add\_additional\_uom\_columns().
- Evaluate self.add\_alt\_uom\_columns().
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [get inventory dimension fields](operations-072.md#op-8cd87fb2f71b69), [prepare opening stock](operations-071.md#op-f67b132596c28e), [prepare sle query](operations-071.md#op-6f0354b32db652), [prepare item warehouse map for current period](operations-071.md#op-e945cc9c1a1bcb), [set pool rate on dimension rows](operations-071.md#op-08a583f3946506), [prepare new data](operations-072.md#op-7dd6aefda042c1), [get columns](operations-072.md#op-aa6f7cb9af9ca1), [add additional uom columns](operations-072.md#op-f1fe7562d746dc), [add alt uom columns](operations-072.md#op-26dd3d5e162295).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L486)

<a id="op-f67b132596c28e"></a>
### Stock Balance Report.prepare opening stock

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_prepare_opening_stock`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set opening\_entries from self.get\_entries\_from\_stock\_closing\_balance().
- For each entry in opening\_entries.
  - Set key from self.get\_group\_by\_key(entry).
  - Set self.item\_warehouse\_map at key from Platform.\_dict(mapping(“item\_code” → entry.item\_code, “warehouse” → entry.warehouse, “item\_group” → entry.item\_group, “company” → entry.company, …)).
    - Value choice on entry.actual\_qty — true gives flt((entry.stock\_value\_difference ÷ entry.actual\_qty)), false gives 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get entries from stock closing balance](operations-071.md#op-ab2068cdd5e711), [get group by key](operations-072.md#op-45124a0e9c8ff2).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L483)

<a id="op-ab2068cdd5e711"></a>
### Stock Balance Report.get entries from stock closing balance

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_entries_from_stock_closing_balance`

**Inputs** self.

**Declared result** list.

**Explicit results** list() · list of d for d drawn from opening\_entries where not d.batch\_no.

**Local steps**

- If self.filters.get(“ignore\_closing\_balance”).
  - Return list().
- If self.filters.get(“show\_dimension\_wise\_stock”).
  - Return list().
- Set stk\_cl\_obj from StockClosing(self.filters.company, self.from\_date, self.from\_date).
- If not stk\_cl\_obj.last\_closing\_balance.
  - Return list().
- Set self.start\_from from add\_days(stk\_cl\_obj.last\_closing\_balance.to\_date, 1).
- Set closing\_entry from stk\_cl\_obj.last\_closing\_balance.name.
- Set opening\_entries from self.get\_closing\_balance\_query(closing\_entry).run(as\_dict = true).
- Return list of d for d drawn from opening\_entries where not d.batch\_no.
  - Draw d from opening\_entries, keep a combination only if (not d.batch\_no).

**Methods declared on this owner** [get closing balance query](operations-071.md#op-4fc37c0e4b9a08).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L470)

<a id="op-4fc37c0e4b9a08"></a>
### Stock Balance Report.get closing balance query

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_get_closing_balance_query`

**Inputs** self, stock\_closing\_entry.

**Explicit results** self.apply\_items\_filters(query, item\_table).

**Local steps**

- Set closing from Platform.qb.DocType(“Stock Closing Balance”).
- Set item\_table from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.item\_code equals nested operand in the contract.name).select(closing.star).where(closing.stock\_closing\_entry ….
- Set query from self.apply\_closing\_dimension\_filters(query, closing).
- Set query from self.apply\_warehouse\_filters(query, closing).
- Return self.apply\_items\_filters(query, item\_table).

**Methods declared on this owner** [apply closing dimension filters](operations-071.md#op-47810fb634a713), [apply warehouse filters](operations-072.md#op-29963056035fe1), [apply items filters](operations-072.md#op-7a796ca7cb414a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1025)

<a id="op-47810fb634a713"></a>
### Stock Balance Report.apply closing dimension filters

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_apply_closing_dimension_filters`

**Inputs** self, query, closing.

**Explicit results** query.where(closing.inventory\_dimension\_key equals json.dumps(tuple(“item\_code”, “warehouse”, expanded dimension\_keys))) · query.where((closing.inventory\_dimension\_key.isnull() bitwise or closing.inventory\_dimension\_key equals empty text)).

**Local steps**

- Set dimension\_keys from list().
- For each field in self.inventory\_dimensions.
  - If values bound to self.filters.get(field).
    - Evaluate dimension\_keys.append(field).
    - Set query from query.where(closing at field.isin(values when isinstance(values, list), otherwise list(values))).
      - Value choice on isinstance(values, list) — true gives values, false gives list(values).
- If dimension\_keys.
  - Return query.where(closing.inventory\_dimension\_key equals json.dumps(tuple(“item\_code”, “warehouse”, expanded dimension\_keys))).
- Return query.where((closing.inventory\_dimension\_key.isnull() bitwise or closing.inventory\_dimension\_key equals empty text)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1024)

<a id="op-6f0354b32db652"></a>
### Stock Balance Report.prepare sle query

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_prepare_stock_ledger_entry_query`

**Inputs** self.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set item\_table from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract &lt; nes ….
- Set query from self.apply\_inventory\_dimensions\_filters(query, sle).
- Set query from self.apply\_warehouse\_filters(query, sle).
- Set query from self.apply\_items\_filters(query, item\_table).
- Set query from self.apply\_date\_filters(query, sle).
- If self.filters.get(“company”).
  - Set query from query.where(sle.company equals self.filters.get(“company”)).
- Set self.sle\_query from query.

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply inventory dimensions filters](operations-072.md#op-690082251c8e15), [apply warehouse filters](operations-072.md#op-29963056035fe1), [apply items filters](operations-072.md#op-7a796ca7cb414a), [apply date filters](operations-072.md#op-9001027475e616).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L484)

<a id="op-e945cc9c1a1bcb"></a>
### Stock Balance Report.prepare item warehouse map for current period

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_prepare_item_warehouse_map_for_current_period`

**Inputs** self.

**Record and data access** resolve a document from “System Settings” via get\_cached\_doc.

**Local steps**

- Set self.opening\_vouchers from self.get\_opening\_vouchers().
- If self.filters.get(“show\_stock\_ageing\_data”).
  - Set self.sle\_entries from self.sle\_query.run(as\_dict = true).
- Evaluate self.prepare\_stock\_reco\_voucher\_wise\_count().
- Set \_system\_settings from Platform.get\_cached\_doc(“System Settings”).
- Set self.adjustment\_netting from AdjustmentNetting().
- Set track\_rates from self.shows\_whole\_pools.
- Within Platform.db.unbuffered\_cursor().
  - If not self.filters.get(“show\_stock\_ageing\_data”).
    - Set self.sle\_entries from self.sle\_query.run(as\_dict = true, as\_iterator = true).
  - For each entry in self.adjustment\_netting.net(self.sle\_entries).
    - Set group\_by\_key from self.get\_group\_by\_key(entry).
    - If group\_by\_key does not belong to self.item\_warehouse\_map.
      - Evaluate self.initialize\_data(group\_by\_key, entry).
    - Evaluate self.prepare\_item\_warehouse\_map(entry, group\_by\_key).
    - If track\_rates.
      - Set self.latest\_valuation\_rates at tuple(entry.item\_code, entry.warehouse) from entry.valuation\_rate.
- Set self.item\_warehouse\_map from filter\_items\_with\_no\_transactions(self.item\_warehouse\_map, self.float\_precision, self.inventory\_dimensions).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get opening vouchers](operations-072.md#op-c533753f9090d0), [prepare stock reco voucher wise count](operations-072.md#op-f7740d61b3aa97), [get group by key](operations-072.md#op-45124a0e9c8ff2), [initialize data](operations-072.md#op-c2addb7b8447ec), [prepare item warehouse map](operations-072.md#op-915e04733245ac).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“System Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L481)

<a id="op-08a583f3946506"></a>
### Stock Balance Report.set pool rate on dimension rows

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_set_pool_rate_on_dimension_rows`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.filters.get(“show\_dimension\_wise\_stock”) or self.has\_dimension\_filter).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“show\_dimension\_wise\_stock”) → self.has\_dimension\_filter.
  - Return no value.
- Set items from self.get\_pool\_valuation\_details(set of row.item\_code for row drawn from self.item\_warehouse\_map.values()).
  - Draw row from self.item\_warehouse\_map.values().
- Set rows from list of row for row drawn from self.item\_warehouse\_map.values() where self.is\_valued\_in\_pool(row, items).
  - Draw row from self.item\_warehouse\_map.values(), keep a combination only if (self.is\_valued\_in\_pool(row, items)).
- Set rates from self.latest\_valuation\_rates.
- Evaluate rates.update(self.get\_latest\_valuation\_rates(list of row for row drawn from rows where tuple(row.item\_code, row.warehouse) does not belong to rates)).
  - Draw row from rows, keep a combination only if (tuple(row.item\_code, row.warehouse) does not belong to rates).
- Set pools from self.get\_pool\_balances(rows).
- For each row in rows.
  - Set row.val\_rate from rates.get(tuple(row.item\_code, row.warehouse), 0.0).
  - Set row.bal\_val from (row.bal\_qty × row.val\_rate).
- Evaluate self.add\_stranded\_pool\_values(pools, rates).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get pool valuation details](operations-071.md#op-b4cf3097a48df3), [is valued in pool](operations-071.md#op-f35116d2b74de9), [get latest valuation rates](operations-072.md#op-deb3e33dba2c18), [get pool balances](operations-071.md#op-578deca775cba6), [add stranded pool values](operations-071.md#op-efff11d36adbba).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1034)

<a id="op-578deca775cba6"></a>
### Stock Balance Report.get pool balances

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_get_pool_balances`

**Inputs** self, rows.

**Declared result** dict.

**Explicit results** mapping() · pools.

**Local steps**

- If not self.shows\_whole\_pools.
  - Return mapping().
- Set pools from mapping().
- For each row in rows.
  - Set key from tuple(row.item\_code, row.warehouse).
  - If key does not belong to pools.
    - Set balance from self.item\_warehouse\_balances.get(key, row).
    - Set pools at key from Platform.\_dict(row = row, bal\_qty = balance.bal\_qty, bal\_val = balance.bal\_val).
- Return pools.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1028)

<a id="op-efff11d36adbba"></a>
### Stock Balance Report.add stranded pool values

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_add_stranded_pool_values`

**Inputs** self, pools, rates.

**Local steps**

- For each tuple(key, pool) in pools.items().
  - Set stranded\_value from (flt(pool.bal\_val) − (flt(pool.bal\_qty) × rates.get(key, 0.0))).
  - If not flt(stranded\_value, self.float\_precision).
    - Continue with the next iteration or loop test.
  - If key does not belong to self.item\_warehouse\_map.
    - Evaluate self.initialize\_data(key, pool.row).
  - Update self.item\_warehouse\_map at key.bal\_val using + stranded\_value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize data](operations-072.md#op-c2addb7b8447ec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1022)

<a id="op-9da2b3fb67abbc"></a>
### Stock Balance Report.has dimension filter

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_has_dimension_filter`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** any(generator of self.filters.get(field) for field drawn from self.inventory\_dimensions).

**Local steps**

- Return any(generator of self.filters.get(field) for field drawn from self.inventory\_dimensions).
  - Draw field from self.inventory\_dimensions.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1031)

<a id="op-60f167aaa8f5db"></a>
### Stock Balance Report.shows whole pools

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_shows_whole_pools`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** (bool(self.filters.get(“show\_dimension\_wise\_stock”)) and not self.has\_dimension\_filter).

**Local steps**

- Return (bool(self.filters.get(“show\_dimension\_wise\_stock”)) and not self.has\_dimension\_filter).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(self.filters.get(“show\_dimension\_wise\_stock”)) → not self.has\_dimension\_filter.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1035)

<a id="op-b4cf3097a48df3"></a>
### Stock Balance Report.get pool valuation details

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_get_pool_valuation_details`

**Inputs** self, item\_codes.

**Declared result** dict.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · mapping of item.name → item for item drawn from items.

**Local steps**

- If not item\_codes.
  - Return mapping().
- Set items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(item\_codes))), fields = list(“name”, “has\_batch\_no”, “has\_serial\_no”, “use\_serial\_no\_wise\_valuation”, …)).
- Return mapping of item.name → item for item drawn from items.
  - Draw item from items.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1029)

<a id="op-f35116d2b74de9"></a>
### Stock Balance Report.is valued in pool

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_is_valued_in_pool`

**Inputs** self, row, items.

**Declared result** bool.

**Record and data access** read “Company” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** not item.use\_serial\_no\_wise\_valuation · (valuation\_method equals “Moving Average” and bool(Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”))) · true.

**Local steps**

- Set item from items at row.item\_code.
- If item.has\_serial\_no.
  - Return not item.use\_serial\_no\_wise\_valuation.
- If item.has\_batch\_no.
  - Set valuation\_method from (item.valuation\_method or Platform.get\_cached\_value(“Company”, row.company, “valuation\_method”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.valuation\_method → Platform.get\_cached\_value(“Company”, row.company, “valuation\_method”).
  - Return (valuation\_method equals “Moving Average” and bool(Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in valuation\_method equals “Moving Average” → bool(Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”)).
- Return true.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, row.company, “valuation\_method”), Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1033)
