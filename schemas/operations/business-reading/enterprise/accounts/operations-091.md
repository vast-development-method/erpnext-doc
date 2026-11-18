# Accounting and settlement · operations 91

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Profit and loss statement

<a id="op-f5d0be45941b9f"></a>
### Get data duckdb

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_get_data_duckdb`

**Inputs** conn, filters, root\_type, balance\_must\_be, period\_list.

**Explicit results** no value · out.

**Local steps**

- Set accounts from get\_accounts(filters.company, root\_type).
- If not accounts.
  - Return no value.
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set company\_currency from get\_appropriate\_currency(filters.company, filters).
- Set gl\_entries\_by\_account from mapping().
- Evaluate \_load\_gl\_entries\_duckdb(conn, filters, period\_list, accounts, …).
- Evaluate calculate\_values(accounts\_by\_name, gl\_entries\_by\_account, period\_list, filters.accumulated\_values, …).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name, period\_list).
- Set out from prepare\_data(accounts, balance\_must\_be, period\_list, company\_currency, accumulated\_values = filters.accumulated\_values).
- Set out from filter\_out\_zero\_value\_rows(out, parent\_children\_map, filters.show\_zero\_values).
- If out.
  - Evaluate add\_total\_row(out, root\_type, balance\_must\_be, period\_list, …).
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0270.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1162)

<a id="op-4821e3cb6ba86c"></a>
### Load gl entries duckdb

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_load_general_ledger_entries_duckdb`

**Inputs** conn, filters, period\_list, accounts, gl\_entries\_by\_account.

**Explicit results** no value.

**Local steps**

- Bind dependencies \_extra\_gl\_conditions, \_fetch\_gl\_rows\_duckdb.
- Bind dependencies convert\_to\_presentation\_currency, get\_currency.
- Set company from filters.company.
- Set leaf\_accounts from list of acc.name for acc drawn from accounts where not acc.is\_group.
  - Draw acc from accounts, keep a combination only if (not acc.is\_group).
- If not leaf\_accounts.
  - Return no value.
- Set tuple(extra\_cond, extra\_params) from \_extra\_gl\_conditions(filters).
- Set account\_placeholders from “, ”.join((list(“?”) × len(leaf\_accounts))).
- Set base\_conds from list(“company = ?”, “is\_cancelled = 0”, formatted text account IN ({account\_placeholders}), “voucher\_type != 'Period Closing Voucher'”).
- Set base\_params from list(company, expanded leaf\_accounts).
- Evaluate base\_conds.extend(extra\_cond).
- Evaluate base\_params.extend(extra\_params).
- For each period in period\_list.
  - Set period\_conds from list(expanded base\_conds, “posting\_date &gt;= ?”, “posting\_date &lt;= ?”).
  - Set period\_params from list(expanded base\_params, period.from\_date, period.to\_date).
  - Set period\_entries from \_fetch\_gl\_rows\_duckdb(conn, period\_conds, period\_params).
  - If filters.get(“presentation\_currency”).
    - Evaluate convert\_to\_presentation\_currency(period\_entries, get\_currency(filters)).
  - For each entry in period\_entries.
    - Set entry.posting\_date from period.to\_date.
    - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0270.json#L462) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1165)

## Report · Profitability analysis

<a id="op-e92bfa3c412830"></a>
### Execute

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Select Accounting Dimension.”.

**Local steps**

- If (filters.get(“based\_on”) equals “Accounting Dimension” and not filters.get(“accounting\_dimension”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“based\_on”) equals “Accounting Dimension” → not filters.get(“accounting\_dimension”).
  - Call the validation error handler Platform.throw(translated “Select Accounting Dimension.”).
- Set based\_on from filters.based\_on when filters.based\_on differs from “Accounting Dimension”, otherwise filters.accounting\_dimension.
  - Value choice on filters.based\_on differs from “Accounting Dimension” — true gives filters.based\_on, false gives filters.accounting\_dimension.
- Evaluate validate\_filters(filters).
- Set accounts from get\_accounts\_data(based\_on, filters.get(“company”)).
- Set data from get\_data(accounts, filters, based\_on).
- Set columns from get\_columns(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0270.json#L6037) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L836) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1178)

<a id="op-ec61ca0086410c"></a>
### Validate company permission

`operation_enterprise_binding_enterprise_accounts_report_profitability_analysis_profitability_analysis_validate_company_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** company.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1252)

<a id="op-f9bd6516356412"></a>
### Get accounts data

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_get_accounts_data`

**Inputs** based\_on, company.

**Record and data access** read “Cost Center” via get\_list · read “Project” via get\_list · read doctype via get\_list.

**Explicit results** cost\_centers · Platform.get\_list(“Project”, fields = list(“name”), filters = mapping(“company” → company), order\_by = “name”) · Platform.get\_list(doctype, fields = list(“name”), filters = filters, order\_by = “name”).

**Local steps**

- If based\_on equals “Cost Center”.
  - Set cost\_centers from Platform.get\_list(“Cost Center”, fields = list(“name”, “parent\_cost\_center as parent\_account”, “cost\_center\_name as account\_name”, “lft”, …), filters = mapping(“company” → company), order\_by = “name”).
  - Set names from set of cc.name for cc drawn from cost\_centers.
    - Draw cc from cost\_centers.
  - For each cc in cost\_centers.
    - If cc.parent\_account does not belong to names.
      - Set cc.parent\_account from no value.
  - Return cost\_centers.
- Otherwise.
  - If based\_on equals “Project”.
    - Return Platform.get\_list(“Project”, fields = list(“name”), filters = mapping(“company” → company), order\_by = “name”).
  - Otherwise.
    - Evaluate validate\_company\_permission(company).
    - Set filters from mapping().
    - Set doctype from Platform.unscrub(based\_on).
    - Set has\_company from Platform.db.has\_column(doctype, “company”).
    - If has\_company.
      - Evaluate filters.update(mapping(“company” → company)).
    - Return Platform.get\_list(doctype, fields = list(“name”), filters = filters, order\_by = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1179)

<a id="op-e5f5eefe57dc15"></a>
### Get data

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_get_data`

**Inputs** accounts, filters, based\_on.

**Explicit results** list() · data.

**Local steps**

- If not accounts.
  - Return list().
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set gl\_entries\_by\_account from mapping().
- Set accounting\_dimensions from get\_dimensions(with\_cost\_center\_and\_project = true) at 0.
- Set fieldname from empty text.
- For each dimension in accounting\_dimensions.
  - If dimension at “document\_type” equals based\_on.
    - Set fieldname from dimension at “fieldname”.
- Evaluate set\_gl\_entries\_by\_account(filters.get(“company”), filters.get(“from\_date”), filters.get(“to\_date”), fieldname, ignore\_closing\_entries = not flt(filters.get(“with\_period\_closing\_entry”)), finance\_books = ge ….
- Set total\_row from calculate\_values(accounts, gl\_entries\_by\_account, filters).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name).
- Set data from prepare\_data(accounts, filters, total\_row, parent\_children\_map, …).
- Set data from filter\_out\_zero\_value\_rows(data, parent\_children\_map, show\_zero\_values = filters.get(“show\_zero\_values”)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1181)

<a id="op-2a0b3c81ffe93c"></a>
### Calculate values

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_calculate_values`

**Inputs** accounts, gl\_entries\_by\_account, filters.

**Explicit results** total\_row.

**Local steps**

- Set init from mapping(“income” → 0.0, “expense” → 0.0, “gross\_profit\_loss” → 0.0).
- Set total\_row from mapping(“cost\_center” → no value, “account\_name” → ((“'” + translated “Total”) + “'”), “warn\_if\_negative” → true, “income” → 0.0, …).
- For each d in accounts.
  - Evaluate d.update(init.copy()).
  - For each entry in gl\_entries\_by\_account.get(d.name, list()).
    - If cstr(entry.is\_opening) differs from “Yes”.
      - If entry.type equals “Income”.
        - Update d at “income” using + (flt(entry.credit) − flt(entry.debit)).
      - If entry.type equals “Expense”.
        - Update d at “expense” using + (flt(entry.debit) − flt(entry.credit)).
      - Set d at “gross\_profit\_loss” from (d.get(“income”) − d.get(“expense”)).
  - Update total\_row at “income” using + d at “income”.
  - Update total\_row at “expense” using + d at “expense”.
- Set total\_row at “gross\_profit\_loss” from (total\_row.get(“income”) − total\_row.get(“expense”)).
- Return total\_row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0271.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L835) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1177)

<a id="op-2b271a0eaf66c1"></a>
### Accumulate values into parents

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_accumulate_values_into_parents`

**Inputs** accounts, accounts\_by\_name.

**Local steps**

- For each d in reversed(accounts).
  - If d.parent\_account.
    - For each key in value\_fields.
      - Update accounts\_by\_name at d.parent\_account at key using + d at key.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0271.json#L849) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L834) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1176)

<a id="op-4a25240425a6bb"></a>
### Prepare data

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_prepare_data`

**Inputs** accounts, filters, total\_row, parent\_children\_map, based\_on.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- For each d in accounts.
  - Set has\_value from false.
  - Set row from mapping(“account\_name” → (d.account\_name or d.name), “account” → d.name, “parent\_account” → d.parent\_account, “indent” → d.indent, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.account\_name → d.name.
  - For each key in value\_fields.
    - Set row at key from flt(d.get(key, 0.0), 3).
    - If abs(row at key) ≥ get\_zero\_cutoff(company\_currency).
      - Set has\_value from true.
  - Set row at “has\_value” from has\_value.
  - Evaluate data.append(row).
- Evaluate data.extend(list(mapping(), total\_row)).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0271.json#L980) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1182)

<a id="op-df56a9e6c446f7"></a>
### Get columns

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“fieldname” → “account”, “label” → translated filters.get(“based\_on”), “fieldtype” → “Link”, “options” → filters.get(“based\_on”), …), mapping(“fieldname” → “currency”, “label” → translated “Cu ….

**Local steps**

- Return list(mapping(“fieldname” → “account”, “label” → translated filters.get(“based\_on”), “fieldtype” → “Link”, “options” → filters.get(“based\_on”), …), mapping(“fieldname” → “currency”, “label” → translated “Cu ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0271.json#L1550) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1180)

<a id="op-0b00f9f42d68ad"></a>
### Set gl entries by account

`operation_enterprise_accounts_report_profitability_analysis_business_behavior_set_general_ledger_entries_by_account`

**Inputs** company, from\_date, to\_date, based\_on, gl\_entries\_by\_account, ignore\_closing\_entries = false, finance\_books = no value.

**Explicit results** gl\_entries\_by\_account.

**Local steps**

- Set gl from qb.DocType(“GL Entry”).
- Set acc from qb.DocType(“Account”).
- Set conditions from list().
- Evaluate conditions.append(gl.company.eq(company)).
- Evaluate conditions.append(gl at based\_on.notnull()).
- Evaluate conditions.append(gl.is\_cancelled.eq(0)).
- If (from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date.
  - Evaluate conditions.append(gl.posting\_date.between(from\_date, to\_date)).
- Otherwise.
  - If (from\_date and not to\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → not to\_date.
    - Evaluate conditions.append(gl.posting\_date.gte(from\_date)).
  - Otherwise.
    - If (not from\_date and to\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_date → to\_date.
      - Evaluate conditions.append(gl.posting\_date.lte(to\_date)).
- If ignore\_closing\_entries.
  - Evaluate conditions.append(gl.voucher\_type.ne(“Period Closing Voucher”)).
- Evaluate conditions.append((gl.finance\_book.isin(list(empty text, expanded (finance\_books or list()))) bitwise or gl.finance\_book.isnull())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in finance\_books → list().
- If match\_conditions bound to build\_match\_conditions(“GL Entry”).
  - Evaluate conditions.append(Bracket(LiteralValue(match\_conditions))).
- Set root\_subquery from qb.from\_(acc).select(acc.root\_type).where(acc.name.eq(gl.account)).
- Set gl\_entries from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.all(co ….
- For each entry in gl\_entries.
  - Evaluate gl\_entries\_by\_account.setdefault(entry.based\_on, list()).append(entry).
- Return gl\_entries\_by\_account.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L841) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1183)

<a id="op-23df6ce51049bb"></a>
### Get finance books

`operation_enterprise_binding_enterprise_accounts_report_profitability_analysis_profitability_analysis_get_finance_books`

**Inputs** filters.

**Declared result** list at str.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** finance\_books.

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set finance\_books from list(cstr(filters.get(“finance\_book”))).
- If filters.get(“include\_default\_book\_entries”).
  - Set company\_finance\_book from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
  - If (filters.get(“finance\_book”) and company\_finance\_book and filters.finance\_book differs from company\_finance\_book).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“finance\_book”) → company\_finance\_book → filters.finance\_book differs from company\_finance\_book.
    - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
  - Evaluate finance\_books.append(cstr(company\_finance\_book)).
- Return finance\_books.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1251)

## Record · Promotional scheme

[Record definition](../../../../data/record-types/promotional_scheme.json)

<a id="op-fcf51ae4303241"></a>
### Promotional Scheme.validate

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Either 'Selling' or 'Buying' must be selected” · validation helper — translated “Price or product discount slabs are required”.

**Local steps**

- If (not self.selling and not self.buying).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.selling → not self.buying.
  - Call the validation error handler Platform.throw(translated “Either 'Selling' or 'Buying' must be selected”, title = translated “Mandatory”).
- If not (self.price\_discount\_slabs or self.product\_discount\_slabs).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.price\_discount\_slabs → self.product\_discount\_slabs.
  - Call the validation error handler Platform.throw(translated “Price or product discount slabs are required”).
- Evaluate self.validate\_applicable\_for().
- Evaluate self.validate\_overlapping\_slabs().
- Evaluate self.validate\_pricing\_rules().
- Evaluate self.validate\_mixed\_with\_recursion().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate applicable for](operations-091.md#op-769d0538c64f18), [validate overlapping slabs](operations-091.md#op-83282864b7dbcc), [validate pricing rules](operations-091.md#op-4f90c13dce2f37), [validate mixed with recursion](operations-091.md#op-1d033dc3bfcc7d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L896)

<a id="op-769d0538c64f18"></a>
### Promotional Scheme.validate applicable for

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_validate_applicable_for`

**Inputs** self.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- If self.applicable\_for.
  - Set applicable\_for from Platform.scrub(self.applicable\_for).
  - If not self.get(applicable\_for).
    - Set msg from formatted text The field {Platform.bold(self.applicable\_for)} is required.
    - Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L897)

<a id="op-83282864b7dbcc"></a>
### Promotional Scheme.validate overlapping slabs

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_promotionalscheme_validate_overlapping_slabs`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0} in {1} and row {2} in {3} apply to the same quantity and amount. Change the ranges, set a different  …”.format(slab.idx, Platform.bold(translated self.meta.get\_label(slab.parentfield)), ….

**Local steps**

- If (self.disable or self.apply\_on equals “Transaction”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.disable → self.apply\_on equals “Transaction”.
  - Return no value.
- Set slabs from list of d for d drawn from (self.price\_discount\_slabs + self.product\_discount\_slabs) where not d.disable.
  - Draw d from (self.price\_discount\_slabs + self.product\_discount\_slabs), keep a combination only if (not d.disable).
- For each tuple(index, slab) in enumerate(slabs).
  - For each other\_slab in slabs at slice (index + 1) to no value.
    - If are\_slabs\_conflicting(slab, other\_slab).
      - Call the validation error handler Platform.throw(translated “Row {0} in {1} and row {2} in {3} apply to the same quantity and amount. Change the ranges, set a different  …”.format(slab.idx, Platform.bold(translated nested operand in the co ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L937)

<a id="op-4f90c13dce2f37"></a>
### Promotional Scheme.validate pricing rules

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_validate_pricing_rules`

**Inputs** self.

**Record and data access** read “Pricing Rule Detail” via exists.

**State and service calls** request delete\_doc for “Pricing Rule” · msgprint with (((translated “The following invalid Pricing Rules are deleted:” + text in the contract) + “&lt;/li&gt;&lt;li&gt;”.join(invalid\_pricing\_rule)) + “&lt;/li&gt;&lt;/ul&gt;”).

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - Return no value.
- Set invalid\_pricing\_rule from self.get\_invalid\_pricing\_rules().
- If not invalid\_pricing\_rule.
  - Return no value.
- If Platform.db.exists(“Pricing Rule Detail”, mapping(“pricing\_rule” → list(“in”, invalid\_pricing\_rule), “docstatus” → list(“&lt;”, 2))).
  - Evaluate raise\_for\_transaction\_exists(self.name).
- For each doc in invalid\_pricing\_rule.
  - Evaluate Platform.delete\_doc(“Pricing Rule”, doc).
- Evaluate Platform.msgprint((((translated “The following invalid Pricing Rules are deleted:” + text in the contract) + “&lt;/li&gt;&lt;li&gt;”.join(invalid\_pricing\_rule)) + “&lt;/li&gt;&lt;/ul&gt;”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get invalid pricing rules](operations-091.md#op-4c84ad5eb34f1d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L899)

<a id="op-4c84ad5eb34f1d"></a>
### Promotional Scheme.get invalid pricing rules

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_get_invalid_pricing_rules`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).select(pr.name).where(Criterion.all(conditions)).run(pluck = true).

**Local steps**

- Set pr from Platform.qb.DocType(“Pricing Rule”).
- Set conditions from list().
- Evaluate conditions.append(pr.promotional\_scheme equals self.name).
- If self.applicable\_for.
  - Set applicable\_for from Platform.scrub(self.applicable\_for).
  - Set applicable\_for\_list from list of d.get(applicable\_for) for d drawn from self.get(applicable\_for).
    - Draw d from self.get(applicable\_for).
  - Evaluate conditions.append((IfNull(pr.applicable\_for, empty text) differs from self.applicable\_for bitwise or (IfNull(pr.applicable\_for, empty text) equals self.applicable\_for bitwise and IfNull(nested operand in t ….
- Otherwise.
  - Evaluate conditions.append(IfNull(pr.applicable\_for, empty text) differs from empty text).
- Return nested operand in the contract(nested operand in the contract).select(pr.name).where(Criterion.all(conditions)).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L569) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L892)

<a id="op-f72f217cbdf6ce"></a>
### Promotional Scheme.on update

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_on_update`

**Inputs** self.

**Record and data access** read “Pricing Rule” via get\_all.

**Local steps**

- Evaluate self.validate().
- Evaluate self.remove\_pricing\_rules\_of\_deleted\_slabs().
- Set pricing\_rules from (Platform.get\_all(“Pricing Rule”, fields = list(“promotional\_scheme\_id”, “name”, “creation”), filters = mapping(“promotional\_scheme” → self.name, “applicable\_for” → self.applicable\_for), order\_by = “creati ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Pricing Rule”, fields = list(“promotional\_scheme\_id”, “name”, “creation”), filters = mapping(“promotional\_scheme” → self.name, “applicable\_for” → self.applicable\_for), order\_by = “creation asc”) → mapping().
- Evaluate self.update\_pricing\_rules(pricing\_rules).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate](operations-091.md#op-fcf51ae4303241), [remove pricing rules of deleted slabs](operations-091.md#op-b2497268ed8df9), [update pricing rules](operations-091.md#op-7f303f44ba4399).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L894)

<a id="op-b2497268ed8df9"></a>
### Promotional Scheme.remove pricing rules of deleted slabs

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_promotionalscheme_remove_pricing_rules_of_deleted_slabs`

**Inputs** self.

**Record and data access** read “Pricing Rule” via get\_all.

**State and service calls** request delete\_doc for “Pricing Rule” · request set\_value on “Pricing Rule”.

**Explicit results** no value.

**Local steps**

- Set slabs from list of d.name for d drawn from (self.price\_discount\_slabs + self.product\_discount\_slabs).
  - Draw d from (self.price\_discount\_slabs + self.product\_discount\_slabs).
- Set pricing\_rules from Platform.get\_all(“Pricing Rule”, filters = mapping(“promotional\_scheme” → self.name, “promotional\_scheme\_id” → list(“not in”, slabs)), fields = list(“name”, “disable”)).
- If not pricing\_rules.
  - Return no value.
- Set used\_pricing\_rules from get\_linked\_pricing\_rules(list of d.name for d drawn from pricing\_rules).
  - Draw d from pricing\_rules.
- For each pricing\_rule in pricing\_rules.
  - If pricing\_rule.name does not belong to used\_pricing\_rules.
    - Evaluate Platform.delete\_doc(“Pricing Rule”, pricing\_rule.name).
  - Otherwise.
    - If not pricing\_rule.disable.
      - Evaluate Platform.db.set\_value(“Pricing Rule”, pricing\_rule.name, “disable”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L936)

<a id="op-1d033dc3bfcc7d"></a>
### Promotional Scheme.validate mixed with recursion

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_validate_mixed_with_recursion`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Recursive Discounts with Mixed condition is not supported by the system”.

**Local steps**

- If self.mixed\_conditions.
  - If self.product\_discount\_slabs.
    - For each slab in self.product\_discount\_slabs.
      - If slab.is\_recursive.
        - Call the validation error handler Platform.throw(translated “Recursive Discounts with Mixed condition is not supported by the system”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L1333) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L898)

<a id="op-7f303f44ba4399"></a>
### Promotional Scheme.update pricing rules

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_update_pricing_rules`

**Inputs** self, pricing\_rules.

**State and service calls** call insert on doc · call save on doc · msgprint with translated “Pricing Rule {0} is updated”.format(doc.name) · msgprint with translated “New {0} pricing rules are created”.format(count).

**Local steps**

- Set rules from mapping().
- Set count from 0.
- Set names from list().
- For each rule in pricing\_rules.
  - Evaluate names.append(rule.name).
  - Set rules at rule.get(“promotional\_scheme\_id”) from names.
- Set docs from get\_pricing\_rules(self, rules).
- For each doc in docs.
  - Evaluate doc.run\_method(“validate”).
  - If doc.get(“\_\_islocal”).
    - Update count using + 1.
    - Evaluate doc.insert().
  - Otherwise.
    - Evaluate doc.save().
    - Evaluate Platform.msgprint(translated “Pricing Rule {0} is updated”.format(doc.name)).
- If count.
  - Evaluate Platform.msgprint(translated “New {0} pricing rules are created”.format(count)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“validate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L1464) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L895)

<a id="op-315a6edad39be3"></a>
### Promotional Scheme.on trash

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_promotional_scheme_on_trash`

**Inputs** self.

**Record and data access** read “Pricing Rule” via get\_all.

**State and service calls** request delete\_doc for “Pricing Rule”.

**Local steps**

- For each rule in Platform.get\_all(“Pricing Rule”, mapping(“promotional\_scheme” → self.name)).
  - Evaluate Platform.delete\_doc(“Pricing Rule”, rule.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L1894) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L893)

<a id="op-e5030583f558ba"></a>
### Are slabs conflicting

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_are_slabs_conflicting`

**Inputs** slab, other\_slab.

**Explicit results** false · (are\_ranges\_overlapping(slab.min\_qty, slab.max\_qty, other\_slab.min\_qty, other\_slab.max\_qty) and are\_ranges\_overlapping(slab.min\_amount, slab.max\_amount, other\_slab.min\_amount, other\_slab.max\_amount)).

**Local steps**

- If cint(slab.priority) differs from cint(other\_slab.priority).
  - Return false.
- If (slab.apply\_multiple\_pricing\_rules and other\_slab.apply\_multiple\_pricing\_rules).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in slab.apply\_multiple\_pricing\_rules → other\_slab.apply\_multiple\_pricing\_rules.
  - Return false.
- If are\_warehouses\_distinct(slab.get(“warehouse”), other\_slab.get(“warehouse”)).
  - Return false.
- If are\_price\_lists\_distinct(slab, other\_slab).
  - Return false.
- Return (are\_ranges\_overlapping(slab.min\_qty, slab.max\_qty, other\_slab.min\_qty, other\_slab.max\_qty) and are\_ranges\_overlapping(slab.min\_amount, slab.max\_amount, other\_slab.min\_amount, other\_slab.max\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in are\_ranges\_overlapping(slab.min\_qty, slab.max\_qty, other\_slab.min\_qty, other\_slab.max\_qty) → are\_ranges\_overlapping(slab.min\_amount, slab.max\_amount, other\_slab.min\_amount, other\_slab.max\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L933)

<a id="op-fc0b26de7d7956"></a>
### Are warehouses distinct

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_are_warehouses_distinct`

**Inputs** warehouse, other\_warehouse.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit results** false · (rgt &lt; other\_lft or other\_rgt &lt; lft).

**Local steps**

- If (not (warehouse and other\_warehouse) or warehouse equals other\_warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (warehouse and other\_warehouse) → warehouse equals other\_warehouse.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → other\_warehouse.
  - Return false.
- Set tuple(lft, rgt) from Platform.get\_cached\_value(“Warehouse”, warehouse, list(“lft”, “rgt”)).
- Set tuple(other\_lft, other\_rgt) from Platform.get\_cached\_value(“Warehouse”, other\_warehouse, list(“lft”, “rgt”)).
- Return (rgt &lt; other\_lft or other\_rgt &lt; lft).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rgt &lt; other\_lft → other\_rgt &lt; lft.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, warehouse, list(“lft”, “rgt”)), Platform.get\_cached\_value(“Warehouse”, other\_warehouse, list(“lft”, “rgt”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L934)
