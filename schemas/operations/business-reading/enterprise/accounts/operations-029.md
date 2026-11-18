# Accounting and settlement · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Consolidated financial statement

<a id="op-060b61637d4810"></a>
### Get subsidiary companies

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_subsidiary_companies`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.db.sql\_list(formatted text select name from ′tabCompany′  where lft &gt;= {lft} and rgt &lt;= {rgt} order by lft, rgt).

**Local steps**

- Set tuple(lft, rgt) from Platform.get\_cached\_value(“Company”, company, list(“lft”, “rgt”)).
- Return Platform.db.sql\_list(formatted text select name from ′tabCompany′  where lft &gt;= {lft} and rgt &lt;= {rgt} order by lft, rgt).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“lft”, “rgt”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L780)

<a id="op-05390623493634"></a>
### Get accounts

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_accounts`

**Inputs** root\_type, companies.

**Record and data access** read “Account” via get\_all.

**Explicit results** accounts.

**Local steps**

- Set accounts from list().
- For each company in companies.
  - Evaluate accounts.extend(Platform.get\_all(“Account”, fields = list(“name”, “is\_group”, “company”, “parent\_account”, …), filters = mapping(“company” → company, “root\_type” → root\_type))).
- Return accounts.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L3446) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L767)

<a id="op-799294335f2694"></a>
### Prepare data

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_prepare_data`

**Inputs** accounts, start\_date, end\_date, balance\_must\_be, companies, company\_currency, filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each d in accounts.
  - Set has\_value from false.
  - Set total from 0.
  - Set row from Platform.\_dict(mapping(“account\_name” → formatted text {translated d.account\_number} - {translated d.account\_name} when d.account\_number, otherwise translated d.account\_name, “account” → translated d.name, ….
    - Value choice on d.account\_number — true gives formatted text {translated d.account\_number} - {translated d.account\_name}, false gives translated d.account\_name.
    - Value choice on balance\_must\_be equals “Debit” — true gives 1, false gives negative 1.
  - For each company in companies.
    - If (d.get(company) and balance\_must\_be equals “Credit”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(company) → balance\_must\_be equals “Credit”.
      - Update d at company using × negative 1.
    - Set row at company from flt(d.get(company, 0.0), 3).
    - If abs(row at company) ≥ get\_zero\_cutoff(filters.presentation\_currency).
      - Set has\_value from true.
      - Update total using + flt(row at company).
  - Set row at “has\_value” from has\_value.
  - Set row at “total” from total.
  - Evaluate set\_group\_company\_total(row, filters).
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L782)

<a id="op-70a43159710516"></a>
### Set group company total

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_set_group_company_total`

**Inputs** row, filters.

**Local steps**

- If (row and filters.get(“accumulated\_in\_group\_company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → filters.get(“accumulated\_in\_group\_company”).
  - Set row at “total” from flt(row.get(filters.company, 0.0), 3).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1190)

<a id="op-56761ab3d52876"></a>
### Set gl entries by account

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_set_general_ledger_entries_by_account`

**Inputs** from\_date, to\_date, root\_lft, root\_rgt, filters, gl\_entries\_by\_account, accounts\_by\_name, accounts, ignore\_closing\_entries = false, root\_type = no value.

**Record and data access** read “Company” via get\_cached\_value · execute query text (SELECT, Company).

**Explicit results** gl\_entries\_by\_account.

**Local steps**

- Set tuple(company\_lft, company\_rgt) from Platform.get\_cached\_value(“Company”, filters.get(“company”), list(“lft”, “rgt”)).
- Set companies from Platform.db.sql(query text (SELECT, Company), mapping(“company\_lft” → company\_lft, “company\_rgt” → company\_rgt), as\_dict = 1).
- Set currency\_info from Platform.\_dict(mapping(“report\_date” → to\_date, “presentation\_currency” → filters.get(“presentation\_currency”))).
- For each d in companies.
  - Set gle from Platform.qb.DocType(“GL Entry”).
  - Set account from Platform.qb.DocType(“Account”).
  - Set query from nested operand in the contract(nested operand in the contract).select(gle.posting\_date, gle.account, gle.debit, gle.credit, …).where(((((nested operand in the contract bitwise and nested operand in the con ….
  - If root\_type.
    - Set query from query.where(account.root\_type equals root\_type).
  - Set additional\_conditions from get\_additional\_conditions(from\_date, ignore\_closing\_entries, filters, d).
  - If additional\_conditions.
    - Set query from query.where(Criterion.all(additional\_conditions)).
  - Set gl\_entries from query.run(as\_dict = true).
  - For each entry in gl\_entries.
    - Set entry.currency from d.default\_currency.
  - If (filters and filters.get(“presentation\_currency”) and filters.get(“presentation\_currency”) differs from d.default\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“presentation\_currency”) → filters.get(“presentation\_currency”) differs from d.default\_currency.
    - Set currency\_info at “company” from d.name.
    - Set currency\_info at “company\_currency” from d.default\_currency.
    - Evaluate convert\_closing\_rate\_entries(gl\_entries, currency\_info).
  - For each entry in gl\_entries.
    - If entry.account\_number.
      - Set account\_name from ((entry.account\_number + “ - ”) + entry.account\_name).
    - Otherwise.
      - Set account\_name from entry.account\_name.
    - Evaluate validate\_entries(account\_name, entry, accounts\_by\_name, accounts).
    - Evaluate gl\_entries\_by\_account.setdefault(account\_name, list()).append(entry).
- Return gl\_entries\_by\_account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), list(“lft”, “rgt”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L783)

<a id="op-b8a90a03d29eac"></a>
### Convert closing rate entries

`operation_enterprise_binding_enterprise_accounts_report_consolidated_financial_statement_consolidated_financial_statement_convert_closing_rate_entries`

**Inputs** gl\_entries, currency\_info.

**Local steps**

- Set entries from list of entry for entry drawn from gl\_entries where not uses\_transaction\_rate(entry).
  - Draw entry from gl\_entries, keep a combination only if (not uses\_transaction\_rate(entry)).
- Evaluate convert\_to\_presentation\_currency(entries, currency\_info).
- For each entry in entries.
  - Set entry.currency from currency\_info.presentation\_currency.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1171)

<a id="op-7b4b44442d86de"></a>
### Get account details

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_account_details`

**Inputs** account.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Account”, account, list(“name”, “report\_type”, “root\_type”, “company”, …), as\_dict = 1).

**Local steps**

- Return Platform.get\_cached\_value(“Account”, account, list(“name”, “report\_type”, “root\_type”, “company”, …), as\_dict = 1).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, list(“name”, “report\_type”, “root\_type”, “company”, …), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L5977) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L764)

<a id="op-2ba098910c2734"></a>
### Validate entries

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_validate_entries`

**Inputs** key, entry, accounts\_by\_name, accounts.

**State and service calls** call insert on accounts.

**Local steps**

- If key does not belong to accounts\_by\_name.
  - Set args from get\_account\_details(entry.account).
  - If args.parent\_account.
    - Set parent\_args from get\_account\_details(args.parent\_account).
    - Evaluate args.update(mapping(“lft” → (parent\_args.lft + 1), “rgt” → (parent\_args.rgt − 1), “indent” → 3, “root\_type” → parent\_args.root\_type, …)).
  - Evaluate accounts\_by\_name.setdefault(key, args).
  - Set idx from len(accounts).
  - For each tuple(index, row) in enumerate(accounts).
    - If row.parent\_account\_name equals args.parent\_account\_name.
      - Set idx from index.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate accounts.insert((idx + 1), args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L6145) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L785)

<a id="op-93e93a0ff354d3"></a>
### Get additional conditions

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_get_additional_conditions`

**Inputs** from\_date, ignore\_closing\_entries, filters, d.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** additional\_conditions.

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Set additional\_conditions from list().
- If ignore\_closing\_entries.
  - Evaluate additional\_conditions.append(gle.voucher\_type differs from “Period Closing Voucher”).
- If from\_date.
  - Evaluate additional\_conditions.append(gle.posting\_date ≥ from\_date).
- Set finance\_books from list().
- Evaluate finance\_books.append(empty text).
- If filter\_fb bound to filters.get(“finance\_book”).
  - Evaluate finance\_books.append(filter\_fb).
- If filters.get(“include\_default\_book\_entries”).
  - If company\_fb bound to Platform.get\_cached\_value(“Company”, d.name, “default\_finance\_book”).
    - Evaluate finance\_books.append(company\_fb).
  - Evaluate additional\_conditions.append((gle.finance\_book.isin(finance\_books) bitwise or gle.finance\_book.isnull())).
- Otherwise.
  - Evaluate additional\_conditions.append((gle.finance\_book.isin(finance\_books) bitwise or gle.finance\_book.isnull())).
- Return additional\_conditions.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, d.name, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0237.json#L6642) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L768)

<a id="op-b310bd1133de88"></a>
### Add total row

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_add_total_row`

**Inputs** out, root\_type, balance\_must\_be, companies, company\_currency.

**Local steps**

- Set total\_row from mapping(“account\_name” → ((“'” + translated “Total {0} ({1})”.format(translated root\_type, translated balance\_must\_be)) + “'”), “account” → ((“'” + translated “Total {0} ({1})”.format(translated root\_type, ….
- For each row in out.
  - If not row.get(“parent\_account”).
    - For each company in companies.
      - Evaluate total\_row.setdefault(company, 0.0).
      - Update total\_row at company using + row.get(company, 0.0).
    - Evaluate total\_row.setdefault(“total”, 0.0).
    - Update total\_row at “total” using + flt(row at “total”).
    - Set row at “total” from empty text.
- If “total” belongs to total\_row.
  - Evaluate out.append(total\_row).
  - Evaluate out.append(mapping()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L759)

<a id="op-4d1c32a9500221"></a>
### Filter accounts

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_filter_accounts`

**Inputs** accounts, depth = 10.

**Explicit results** tuple(filtered\_accounts, accounts\_by\_name, parent\_children\_map).

**Local steps**

- Set parent\_children\_map from mapping().
- Set accounts\_by\_name from mapping().
- Set added\_accounts from list().
- For each d in accounts.
  - If d.account\_key belongs to added\_accounts.
    - Continue with the next iteration or loop test.
  - Evaluate added\_accounts.append(d.account\_key).
  - Set d at “company\_wise\_opening\_bal” from defaultdict(float).
  - Set accounts\_by\_name at d.account\_key from d.
  - Evaluate parent\_children\_map.setdefault((d.parent\_account\_name or no value), list()).append(d).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.parent\_account\_name → no value.
- Set filtered\_accounts from list().
- Bind local operation add\_to\_list for subsequent calls.
- Evaluate add\_to\_list(no value, 0).
- Return tuple(filtered\_accounts, accounts\_by\_name, parent\_children\_map).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L584) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L762)

<a id="op-9be375dfba6fd3"></a>
### Filter accounts.add to list

`operation_enterprise_accounts_report_consolidated_financial_statement_business_behavior_filter_accounts_add_to_list`

**Inputs** parent, level.

**Local steps**

- If level &lt; depth.
  - Set children from (parent\_children\_map.get(parent) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_children\_map.get(parent) → list().
  - Evaluate sort\_accounts(children, is\_root = true when parent is identical to no value, otherwise false).
    - Value choice on parent is identical to no value — true gives true, false gives false.
  - For each child in children.
    - Set child.indent from level.
    - Evaluate filtered\_accounts.append(child).
    - Evaluate add\_to\_list(child.account\_key, (level + 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L1136) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L763)

## Report · Consolidated trial balance

<a id="op-2c7c4b962cb14b"></a>
### Execute

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_filters(filters = filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L3559) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L797)

<a id="op-ab605ccad224e6"></a>
### Validate filters

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_validate_filters`

**Inputs** filters.

**Local steps**

- Evaluate validate\_companies(filters).
- Evaluate tb\_validate\_filters(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L3698) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L808)

<a id="op-8577987f666e6d"></a>
### Validate companies

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_validate_companies`

**Inputs** filters.

**Record and data access** read “Company” via get\_value · read “Company” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Consolidated Trial Balance can be generated for Companies having same root Company.”.

**Local steps**

- If not filters.company.
  - Return no value.
- Set filters.company from expand\_group\_companies(filters.company).
- Set root\_company from get\_root\_company(filters.company at 0).
- Set root\_company from root\_company at 0 when root\_company, otherwise filters.company at 0.
  - Value choice on root\_company — true gives root\_company at 0, false gives filters.company at 0.
- Set tuple(lft, rgt) from Platform.db.get\_value(“Company”, root\_company, fieldname = list(“lft”, “rgt”)).
- Set company\_subtree from Platform.db.get\_all(“Company”, mapping(“lft” → list(“&gt;=”, lft), “rgt” → list(“&lt;=”, rgt)), “name”, order\_by = “lft”, pluck = “name”).
- For each company in filters.company.
  - Evaluate Platform.has\_permission(“Company”, “read”, company, throw = true).
  - If company does not belong to company\_subtree.
    - Call the validation error handler Platform.throw(translated “Consolidated Trial Balance can be generated for Companies having same root Company.”).
- Evaluate sort\_companies(filters).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L807)

<a id="op-df8174b0c65f83"></a>
### Expand group companies

`operation_enterprise_binding_enterprise_accounts_report_consolidated_trial_balance_consolidated_trial_balance_expand_group_companies`

**Inputs** selected\_companies.

**Declared result** list at str.

**Explicit results** companies.

**Local steps**

- Set companies from list().
- For each selected in selected\_companies.
  - For each company in get\_subsidiary\_companies(selected).
    - If company does not belong to companies.
      - Evaluate companies.append(company).
- Return companies.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1192)

<a id="op-53d2bfb4eb2c3d"></a>
### Sort companies

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_sort_companies`

**Inputs** filters.

**Record and data access** read “Company” via get\_all.

**Local steps**

- Set companies from Platform.db.get\_all(“Company”, mapping(“name” → list(“in”, filters.company)), “name”, order\_by = “lft”, pluck = “name”).
- Set filters.company from companies.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L4219) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L805)

<a id="op-dfb563bdf47087"></a>
### Get data

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_get_data`

**Inputs** filters.

**Declared result** list at list.

**Explicit results** data.

**Local steps**

- Set data from list().
- If filters.company.
  - Set tuple(reporting\_currency, ignore\_reporting\_currency) from get\_reporting\_currency(filters).
- Otherwise.
  - Return data.
- For each company in filters.company.
  - Set company\_filter from Platform.\_dict(filters).
  - Set company\_filter.company from company.
  - Set tb\_data from get\_company\_wise\_tb\_data(company\_filter, reporting\_currency, ignore\_reporting\_currency).
  - Evaluate consolidate\_trial\_balance\_data(data, tb\_data).
- If filters.get(“show\_net\_values”).
  - Evaluate prepare\_opening\_closing\_for\_ctb(data).
- If not filters.get(“show\_group\_accounts”).
  - Set data from hide\_group\_accounts(data).
- Set total\_row from calculate\_total\_row(data, reporting\_currency, show\_group\_accounts = filters.get(“show\_group\_accounts”)).
- Evaluate calculate\_foreign\_currency\_translation\_reserve(total\_row, data, filters = filters).
- Evaluate data.extend(list(total\_row)).
- If filters.get(“presentation\_currency”).
  - Evaluate update\_to\_presentation\_currency(data, reporting\_currency, filters.get(“presentation\_currency”), filters.get(“to\_date”), …).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L4377) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L800)

<a id="op-a9f5739a2bcd45"></a>
### Get company wise tb data

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_get_company_wise_tb_data`

**Inputs** filters, reporting\_currency, ignore\_reporting\_currency.

**Record and data access** execute query text (SELECT, Account) · read “Accounts Settings” via get\_single\_value.

**Explicit results** list() · data.

**Explicit failure paths** validation helper — translated “Consolidated Trial balance could not be generated as Exchange Rate from {0} to {1} is not available for {2}.”.format(default\_currency, reporting\_currency, current\_date).

**Local steps**

- Set accounts from Platform.db.sql(query text (SELECT, Account), filters.company, as\_dict = true).
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- Set default\_currency from Enterprise.get\_company\_currency(filters.company).
- Set current\_date from filters.get(“to\_date”) when getdate(filters.get(“to\_date”)) ≤ now\_datetime().date(), otherwise nowdate().
  - Value choice on getdate(filters.get(“to\_date”)) ≤ now\_datetime().date() — true gives filters.get(“to\_date”), false gives nowdate().
- Set closing\_exchange\_rate from get\_exchange\_rate(default\_currency, reporting\_currency, current\_date).
- If not closing\_exchange\_rate.
  - Call the validation error handler Platform.throw(translated “Consolidated Trial balance could not be generated as Exchange Rate from {0} to {1} is not available for {2}.”.format(default\_currency, reporting\_currency, current\_date)).
- If not accounts.
  - Return list().
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set gl\_entries\_by\_account from mapping().
- Set opening\_balances from get\_opening\_balances(filters, ignore\_is\_opening, exchange\_rate = closing\_exchange\_rate, ignore\_reporting\_currency = ignore\_reporting\_currency).
- Evaluate set\_gl\_entries\_by\_account(filters.company, filters.from\_date, filters.to\_date, filters, root\_lft = no value, root\_rgt = no value, ignore\_closing\_entries = not flt(filters.with\_period\_closing\_entry\_for\_curr ….
- Evaluate calculate\_values(accounts, gl\_entries\_by\_account, opening\_balances, filters.get(“show\_net\_values”), ignore\_is\_opening = ignore\_is\_opening, exchange\_rate = closing\_exchange\_rate, ignore\_reporting\_currency = ….
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name).
- Set data from prepare\_companywise\_tb\_data(accounts, filters, parent\_children\_map, reporting\_currency).
- Set data from filter\_out\_zero\_value\_rows(data, parent\_children\_map, show\_zero\_values = filters.get(“show\_zero\_values”)).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”) · clock or generated value from now\_datetime(), nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L799)

<a id="op-0ac69d6f2d6a8e"></a>
### Prepare companywise tb data

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_prepare_companywise_tb_data`

**Inputs** accounts, filters, parent\_children\_map, reporting\_currency.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each d in accounts.
  - Set has\_value from false.
  - Set row from mapping(“account” → d.name, “parent\_account” → d.parent\_account, “indent” → d.indent, “from\_date” → filters.from\_date, …).
    - Value choice on d.account\_number — true gives formatted text {d.account\_number} - {d.account\_name}, false gives d.account\_name.
  - For each key in value\_fields.
    - Set row at key from flt(d.get(key, 0.0), 3).
    - If abs(row at key) ≥ get\_zero\_cutoff(reporting\_currency).
      - Set has\_value from true.
  - Set row at “has\_value” from has\_value.
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L6007) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L803)

<a id="op-fd7e6bc4a6a140"></a>
### Calculate foreign currency translation reserve

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_calculate_foreign_currency_translation_reserve`

**Inputs** total\_row, data, filters.

**State and service calls** call insert on data.

**Explicit results** no value.

**Local steps**

- If (not data or not total\_row).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not data → not total\_row.
  - Return no value.
- Set opening\_dr\_cr\_diff from (total\_row at “opening\_debit” − total\_row at “opening\_credit”).
- Set dr\_cr\_diff from (total\_row at “debit” − total\_row at “credit”).
- Set idx from get\_fctr\_root\_row\_index(data).
- Set fctr\_row from mapping(“account” → translated “Foreign Currency Translation Reserve”, “account\_name” → translated “Foreign Currency Translation Reserve”, “warn\_if\_negative” → true, “opening\_debit” → abs(opening\_dr\_cr\_dif ….
  - Value choice on opening\_dr\_cr\_diff &lt; 0 — true gives abs(opening\_dr\_cr\_diff), false gives 0.0.
  - Value choice on opening\_dr\_cr\_diff &gt; 0 — true gives abs(opening\_dr\_cr\_diff), false gives 0.0.
  - Value choice on dr\_cr\_diff &lt; 0 — true gives abs(dr\_cr\_diff), false gives 0.0.
  - Value choice on dr\_cr\_diff &gt; 0 — true gives abs(dr\_cr\_diff), false gives 0.0.
  - Value choice on filters.get(“show\_group\_accounts”) — true gives (data at idx.get(“indent”) + 1), false gives 0.
- Set fctr\_row at “closing\_debit” from (fctr\_row at “opening\_debit” + fctr\_row at “debit”).
- Set fctr\_row at “closing\_credit” from (fctr\_row at “opening\_credit” + fctr\_row at “credit”).
- If filters.get(“show\_net\_values”).
  - Evaluate prepare\_opening\_closing(fctr\_row).
- Evaluate data.insert((idx + 1), fctr\_row).
- For each field in value\_fields.
  - Update total\_row at field using + fctr\_row at field.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0238.json#L6577) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L794)

<a id="op-35f30ab6d9166a"></a>
### Get fctr root row index

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_get_fctr_root_row_index`

**Inputs** data.

**Explicit results** liabilities\_idx · equity\_idx.

**Local steps**

- Set tuple(liabilities\_idx, equity\_idx, tmp\_idx) from tuple(negative 1, negative 1, 0).
- For each d in data.
  - If (liabilities\_idx equals negative 1 and d.get(“root\_type”) equals “Liability”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in liabilities\_idx equals negative 1 → d.get(“root\_type”) equals “Liability”.
    - Set liabilities\_idx from tmp\_idx.
  - If (equity\_idx equals negative 1 and d.get(“root\_type”) equals “Equity”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in equity\_idx equals negative 1 → d.get(“root\_type”) equals “Equity”.
    - Set equity\_idx from tmp\_idx.
  - Update tmp\_idx using + 1.
- If equity\_idx equals negative 1.
  - Return liabilities\_idx.
- Return equity\_idx.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L801)

<a id="op-dafccc27d422af"></a>
### Consolidate trial balance data

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_consolidate_trial_balance_data`

**Inputs** data, tb\_data.

**Explicit results** no value.

**Local steps**

- If not data.
  - Evaluate data.extend(list(tb\_data)).
  - Return no value.
- For each entry in tb\_data.
  - If entry.
    - Evaluate consolidate\_gle\_data(data, entry, tb\_data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L314) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L796)

<a id="op-5251ef1781055c"></a>
### Get reporting currency

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_get_reporting_currency`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(reporting\_currency, false) · tuple(default\_currency, true).

**Local steps**

- Set reporting\_currency from Platform.get\_cached\_value(“Company”, filters.company at 0, “reporting\_currency”).
- Set default\_currency from no value.
- For each company in filters.company.
  - Set company\_default\_currency from Enterprise.get\_company\_currency(company).
  - If not default\_currency.
    - Set default\_currency from company\_default\_currency.
  - If company\_default\_currency differs from default\_currency.
    - Return tuple(reporting\_currency, false).
- Return tuple(default\_currency, true).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company at 0, “reporting\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L462) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L802)
