# Accounting and settlement · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Financial statements

<a id="op-ac48757dcdc167"></a>
### Is dimension grouped

`operation_enterprise_accounts_report_financial_statements_business_behavior_is_dimension_grouped`

**Inputs** period\_list.

**Declared result** bool.

**Explicit results** false · bool(period\_list at 0.get(“dimension\_field”)).

**Local steps**

- If (not period\_list or not isinstance(period\_list, list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not period\_list → not isinstance(period\_list, list).
  - Return false.
- Return bool(period\_list at 0.get(“dimension\_field”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L4277) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L936)

<a id="op-1b54365769aa80"></a>
### Get period keys for total

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_period_keys_for_total`

**Inputs** period\_list, accumulated\_values, consolidated = false.

**Declared result** list at str.

**Explicit results** list() · list(period\_list) · list(mapping of period.dimension\_value → period.key for period drawn from period\_list.values()) · list(period\_list at negative 1.key) · list of period.key for period drawn from period\_list.

**Local steps**

- If not period\_list.
  - Return list().
- If consolidated.
  - Return list(period\_list).
- If (is\_dimension\_grouped(period\_list) and accumulated\_values).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_dimension\_grouped(period\_list) → accumulated\_values.
  - Return list(mapping of period.dimension\_value → period.key for period drawn from period\_list.values()).
    - Draw period from period\_list.
- If accumulated\_values.
  - Return list(period\_list at negative 1.key).
- Return list of period.key for period drawn from period\_list.
  - Draw period from period\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L4418) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L934)

<a id="op-6416d8a43f53f3"></a>
### Get period list

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_period_list`

**Inputs** from\_fiscal\_year, to\_fiscal\_year, period\_start\_date, period\_end\_date, filter\_based\_on, periodicity, accumulated\_values = false, company = no value, reset\_period\_on\_fy\_change = true, ignore\_fiscal\_year = false.

**Explicit results** period\_list.

**Local steps**

- If filter\_based\_on equals “Fiscal Year”.
  - Set fy\_data from get\_fiscal\_year\_data(from\_fiscal\_year, to\_fiscal\_year).
  - Evaluate validate\_fiscal\_year(fy\_data, from\_fiscal\_year, to\_fiscal\_year).
  - Set tuple(year\_start\_date, year\_end\_date) from tuple(getdate(fy\_data.year\_start\_date), getdate(fy\_data.year\_end\_date)).
- Otherwise.
  - Evaluate validate\_dates(period\_start\_date, period\_end\_date).
  - Set tuple(year\_start\_date, year\_end\_date) from tuple(getdate(period\_start\_date), getdate(period\_end\_date)).
- Set months\_to\_add from mapping(“Yearly” → 12, “Half-Yearly” → 6, “Quarterly” → 3, “Monthly” → 1) at periodicity.
- Set period\_list from list().
- Set start\_date from year\_start\_date.
- Set months from get\_months(year\_start\_date, year\_end\_date).
- For each i in range(cint(math.ceil((months ÷ months\_to\_add)))).
  - Set period from Platform.\_dict(mapping(“from\_date” → start\_date)).
  - If (i equals 0 and filter\_based\_on equals “Date Range”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in i equals 0 → filter\_based\_on equals “Date Range”.
    - Set to\_date from add\_months(get\_first\_day(start\_date), months\_to\_add).
  - Otherwise.
    - Set to\_date from add\_months(start\_date, months\_to\_add).
  - Set start\_date from to\_date.
  - Set to\_date from add\_days(to\_date, negative 1).
  - If to\_date ≤ year\_end\_date.
    - Set period.to\_date from to\_date.
  - Otherwise.
    - Set period.to\_date from year\_end\_date.
  - If not ignore\_fiscal\_year.
    - Set period.to\_date\_fiscal\_year from get\_fiscal\_year(period.to\_date, company = company) at 0.
    - Set period.from\_date\_fiscal\_year\_start\_date from get\_fiscal\_year(period.from\_date, company = company) at 1.
  - Evaluate period\_list.append(period).
  - If period.to\_date equals year\_end\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
- For each opts in period\_list.
  - Set key from opts at “to\_date”.strftime(“%b\_%Y”).lower().
  - If (periodicity equals “Monthly” and not accumulated\_values).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in periodicity equals “Monthly” → not accumulated\_values.
    - Set label from formatdate(opts at “to\_date”, “MMM YYYY”).
  - Otherwise.
    - If not accumulated\_values.
      - Set label from get\_label(periodicity, opts at “from\_date”, opts at “to\_date”).
    - Otherwise.
      - If reset\_period\_on\_fy\_change.
        - Set label\_start\_date from max(opts.from\_date\_fiscal\_year\_start\_date, year\_start\_date).
        - Set label from get\_label(periodicity, label\_start\_date, opts at “to\_date”).
      - Otherwise.
        - Set label from get\_label(periodicity, period\_list at 0.from\_date, opts at “to\_date”).
  - Evaluate opts.update(mapping(“key” → key.replace(one space, “\_”).replace(“-”, “\_”), “label” → label, “year\_start\_date” → year\_start\_date, “year\_end\_date” → year\_end\_date)).
- Return period\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L935)

<a id="op-79c5df33e33574"></a>
### Get fiscal year data

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_fiscal_year_data`

**Inputs** from\_fiscal\_year, to\_fiscal\_year.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** fiscal\_year at 0 when fiscal\_year, otherwise mapping().

**Local steps**

- Set from\_year\_start\_date from Platform.get\_cached\_value(“Fiscal Year”, from\_fiscal\_year, “year\_start\_date”).
- Set to\_year\_end\_date from Platform.get\_cached\_value(“Fiscal Year”, to\_fiscal\_year, “year\_end\_date”).
- Set fy from Platform.qb.DocType(“Fiscal Year”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“year\_start\_date”), nested operand in the contract.as\_(“year\_end\_date”)).where(fy.year\_start\_date ≥  ….
- Set fiscal\_year from query.run(as\_dict = true).
- Return fiscal\_year at 0 when fiscal\_year, otherwise mapping().
  - Value choice on fiscal\_year — true gives fiscal\_year at 0, false gives mapping().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, from\_fiscal\_year, “year\_start\_date”), Platform.get\_cached\_value(“Fiscal Year”, to\_fiscal\_year, “year\_end\_date”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L6159) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L931)

<a id="op-ed47dca67aac0b"></a>
### Validate fiscal year

`operation_enterprise_accounts_report_financial_statements_business_behavior_validate_fiscal_year`

**Inputs** fiscal\_year, from\_fiscal\_year, to\_fiscal\_year.

**Explicit failure paths** validation helper — translated “Start Year and End Year are mandatory” · validation helper — translated “End Year cannot be before Start Year”.

**Local steps**

- If (not fiscal\_year.get(“year\_start\_date”) or not fiscal\_year.get(“year\_end\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fiscal\_year.get(“year\_start\_date”) → not fiscal\_year.get(“year\_end\_date”).
  - Call the validation error handler Platform.throw(translated “Start Year and End Year are mandatory”).
- If getdate(fiscal\_year.get(“year\_end\_date”)) &lt; getdate(fiscal\_year.get(“year\_start\_date”)).
  - Call the validation error handler Platform.throw(translated “End Year cannot be before Start Year”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L6576) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L942)

<a id="op-546516d25347e2"></a>
### Validate dates

`operation_enterprise_accounts_report_financial_statements_business_behavior_validate_dates`

**Inputs** from\_date, to\_date.

**Explicit failure paths** validation helper — translated “From Date and To Date are mandatory”.

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Call the validation error handler Platform.throw(translated “From Date and To Date are mandatory”).
- Evaluate validate\_date\_range(mapping(“from\_date” → from\_date, “to\_date” → to\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L941)

<a id="op-92982e8c82fe6c"></a>
### Get months

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_months`

**Inputs** start\_date, end\_date.

**Explicit results** (diff + 1).

**Local steps**

- Set diff from (((12 × end\_date.year) + end\_date.month) − ((12 × start\_date.year) + start\_date.month)).
- Return (diff + 1).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L7020) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L933)

<a id="op-ed8aa42eec4f6f"></a>
### Get label

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_label`

**Inputs** periodicity, from\_date, to\_date.

**Explicit results** label.

**Local steps**

- If periodicity equals “Yearly”.
  - If formatdate(from\_date, “YYYY”) equals formatdate(to\_date, “YYYY”).
    - Set label from formatdate(from\_date, “YYYY”).
  - Otherwise.
    - Set label from ((formatdate(from\_date, “YYYY”) + “-”) + formatdate(to\_date, “YYYY”)).
- Otherwise.
  - Set label from ((formatdate(from\_date, “MMM YY”) + “-”) + formatdate(to\_date, “MMM YY”)).
- Return label.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L7141) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L932)

<a id="op-bc0ca30c5fd5e5"></a>
### Get data

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_data`

**Inputs** company, root\_type, balance\_must\_be, period\_list, filters = no value, accumulated\_values = 1, only\_current\_fiscal\_year = true, ignore\_closing\_entries = false, ignore\_accumulated\_values\_for\_fy = false, total = true.

**Record and data access** execute query text (SELECT, Account).

**Explicit results** no value · out.

**Local steps**

- Set accounts from get\_accounts(company, root\_type).
- If not accounts.
  - Return no value.
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set company\_currency from get\_appropriate\_currency(company, filters).
- Set gl\_entries\_by\_account from mapping().
- For each root in Platform.db.sql(query text (SELECT, Account), root\_type, as\_dict = 1).
  - Evaluate set\_gl\_entries\_by\_account(company, period\_list at 0 at “year\_start\_date” when only\_current\_fiscal\_year, otherwise no value, period\_list at negative 1 at “to\_date”, filters, root\_type = root\_type, ignore\_cl ….
    - Value choice on only\_current\_fiscal\_year — true gives period\_list at 0 at “year\_start\_date”, false gives no value.
- Evaluate calculate\_values(accounts\_by\_name, gl\_entries\_by\_account, period\_list, accumulated\_values, …).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name, period\_list).
- Set out from prepare\_data(accounts, balance\_must\_be, period\_list, company\_currency, accumulated\_values = filters.accumulated\_values).
- Set out from filter\_out\_zero\_value\_rows(out, parent\_children\_map, filters.show\_zero\_values).
- If (out and total).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in out → total.
  - Evaluate add\_total\_row(out, root\_type, balance\_must\_be, period\_list, …).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L927)

<a id="op-43afb78e75659c"></a>
### Get appropriate currency

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_appropriate_currency`

**Inputs** company, filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** filters at “presentation\_currency” · Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Local steps**

- If (filters and filters.get(“presentation\_currency”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“presentation\_currency”).
  - Return filters at “presentation\_currency”.
- Otherwise.
  - Return Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L729) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L924)

<a id="op-b53a0b0e6558c9"></a>
### Calculate values

`operation_enterprise_accounts_report_financial_statements_business_behavior_calculate_values`

**Inputs** accounts\_by\_name, gl\_entries\_by\_account, period\_list, accumulated\_values, ignore\_accumulated\_values\_for\_fy.

**State and service calls** msgprint with translated “Could not retrieve information for {0}.”.format(entry.account).

**Local steps**

- Set grouped\_by\_dimension from is\_dimension\_grouped(period\_list).
- For each entries in gl\_entries\_by\_account.values().
  - For each entry in entries.
    - Set d from accounts\_by\_name.get(entry.account).
    - If not d.
      - Evaluate Platform.msgprint(translated “Could not retrieve information for {0}.”.format(entry.account), title = “Error”, raise\_exception = 1).
    - For each period in period\_list.
      - If (grouped\_by\_dimension and entry.get(period.dimension\_field) differs from period.dimension\_value).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in grouped\_by\_dimension → entry.get(period.dimension\_field) differs from period.dimension\_value.
        - Continue with the next iteration or loop test.
      - If entry.posting\_date ≤ period.to\_date.
        - If ((accumulated\_values or entry.posting\_date ≥ period.from\_date) and (not (accumulated\_values and ignore\_accumulated\_values\_for\_fy) or entry.fiscal\_year equals period.to\_date\_fiscal\_year)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in (accumulated\_values or entry.posting\_date ≥ period.from\_date) → (not (accumulated\_values and ignore\_accumulated\_values\_for\_fy) or entry.fiscal\_year equals period.to\_date\_fiscal\_year).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in accumulated\_values → entry.posting\_date ≥ period.from\_date.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (accumulated\_values and ignore\_accumulated\_values\_for\_fy) → entry.fiscal\_year equals period.to\_date\_fiscal\_year.
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in accumulated\_values → ignore\_accumulated\_values\_for\_fy.
          - Set d at period.key from ((d.get(period.key, 0.0) + flt(entry.debit)) − flt(entry.credit)).
    - If (not grouped\_by\_dimension and entry.posting\_date &lt; period\_list at 0.year\_start\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not grouped\_by\_dimension → entry.posting\_date &lt; period\_list at 0.year\_start\_date.
      - Set d at “opening\_balance” from ((d.get(“opening\_balance”, 0.0) + flt(entry.debit)) − flt(entry.credit)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L914)

<a id="op-457050752ba15b"></a>
### Accumulate values into parents

`operation_enterprise_accounts_report_financial_statements_business_behavior_accumulate_values_into_parents`

**Inputs** accounts, accounts\_by\_name, period\_list.

**Local steps**

- For each d in reversed(accounts).
  - If d.parent\_account.
    - For each period in period\_list.
      - Set accounts\_by\_name at d.parent\_account at period.key from (accounts\_by\_name at d.parent\_account.get(period.key, 0.0) + d.get(period.key, 0.0)).
    - Set accounts\_by\_name at d.parent\_account at “opening\_balance” from (accounts\_by\_name at d.parent\_account.get(“opening\_balance”, 0.0) + d.get(“opening\_balance”, 0.0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L1536) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L910)

<a id="op-bddaeb7e4a981d"></a>
### Prepare data

`operation_enterprise_accounts_report_financial_statements_business_behavior_prepare_data`

**Inputs** accounts, balance\_must\_be, period\_list, company\_currency, accumulated\_values.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set year\_start\_date from period\_list at 0 at “year\_start\_date”.strftime(“%Y-%m-%d”).
- Set year\_end\_date from period\_list at negative 1 at “year\_end\_date”.strftime(“%Y-%m-%d”).
- Set total\_keys from get\_period\_keys\_for\_total(period\_list, accumulated\_values).
- For each d in accounts.
  - Set has\_value from false.
  - Set row from Platform.\_dict(mapping(“account” → translated d.name, “parent\_account” → translated d.parent\_account when d.parent\_account, otherwise empty text, “indent” → flt(d.indent), “year\_start\_date” → year\_start\_date, …)).
    - Value choice on d.parent\_account — true gives translated d.parent\_account, false gives empty text.
    - Value choice on balance\_must\_be equals “Debit” — true gives 1, false gives negative 1.
    - Value choice on d.account\_number — true gives formatted text {translated d.account\_number} - {translated d.account\_name}, false gives translated d.account\_name.
  - For each period in period\_list.
    - If (d.get(period.key) and balance\_must\_be equals “Credit”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(period.key) → balance\_must\_be equals “Credit”.
      - Update d at period.key using × negative 1.
    - Set row at period.key from flt(d.get(period.key, 0), 3).
    - If abs(row at period.key) ≥ get\_zero\_cutoff(company\_currency).
      - Set has\_value from true.
  - Set row at “has\_value” from has\_value.
  - Set row at “total” from flt(sum(generator of row.get(k, 0) for k drawn from total\_keys), 3).
    - Draw k from total\_keys.
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L1827) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L937)

<a id="op-60d181b34469fc"></a>
### Filter out zero value rows

`operation_enterprise_accounts_report_financial_statements_business_behavior_filter_out_zero_value_rows`

**Inputs** data, parent\_children\_map, show\_zero\_values = false.

**Explicit results** data\_with\_value.

**Local steps**

- Bind local operation get\_all\_parents for subsequent calls.
- Set data\_with\_value from list().
- Set accounts\_to\_show from set().
- For each d in data.
  - If (show\_zero\_values or d.get(“has\_value”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in show\_zero\_values → d.get(“has\_value”).
    - Evaluate accounts\_to\_show.add(d.get(“account”)).
    - Evaluate get\_all\_parents(d.get(“account”), parent\_children\_map).
- For each d in data.
  - If d.get(“account”) belongs to accounts\_to\_show.
    - Evaluate data\_with\_value.append(d).
- Return data\_with\_value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L2884) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L919)

<a id="op-d6fa28cf2b2e03"></a>
### Filter out zero value rows.get all parents

`operation_enterprise_accounts_report_financial_statements_business_behavior_filter_out_zero_value_rows_get_all_parents`

**Inputs** account, parent\_children\_map.

**Local steps**

- For each tuple(parent, children) in parent\_children\_map.items().
  - For each child in children.
    - If (child at “name” equals account and parent).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in child at “name” equals account → parent.
      - Evaluate accounts\_to\_show.add(parent).
      - Evaluate get\_all\_parents(parent, parent\_children\_map).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L3357) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L920)

<a id="op-f242e2fca96358"></a>
### Add total row

`operation_enterprise_accounts_report_financial_statements_business_behavior_add_total_row`

**Inputs** out, root\_type, balance\_must\_be, period\_list, company\_currency.

**Local steps**

- Set total\_row from mapping(“account\_name” → ((“'” + translated “Total {0} ({1})”.format(translated root\_type, translated balance\_must\_be)) + “'”), “account” → ((“'” + translated “Total {0} ({1})”.format(translated root\_type, ….
- For each row in out.
  - If not row.get(“parent\_account”).
    - For each period in period\_list.
      - Evaluate total\_row.setdefault(period.key, 0.0).
      - Update total\_row at period.key using + row.get(period.key, 0.0).
    - Evaluate total\_row.setdefault(“total”, 0.0).
    - Update total\_row at “total” using + flt(row at “total”).
    - Update total\_row at “opening\_balance” using + row at “opening\_balance”.
- If “total” belongs to total\_row.
  - Evaluate out.append(total\_row).
  - Evaluate out.append(mapping()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L3538) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L911)

<a id="op-b26509da496564"></a>
### Get accounts

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_accounts`

**Inputs** company, root\_type.

**Record and data access** execute query text (SELECT, Account).

**Explicit results** Platform.db.sql(query text (SELECT, Account), tuple(company, root\_type), as\_dict = true).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Account), tuple(company, root\_type), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L923)

<a id="op-c6e7507675e160"></a>
### Filter accounts

`operation_enterprise_accounts_report_financial_statements_business_behavior_filter_accounts`

**Inputs** accounts, depth = 20.

**Explicit results** tuple(filtered\_accounts, accounts\_by\_name, parent\_children\_map).

**Local steps**

- Set parent\_children\_map from mapping().
- Set accounts\_by\_name from mapping().
- For each d in accounts.
  - Set accounts\_by\_name at d.name from d.
  - Evaluate parent\_children\_map.setdefault((d.parent\_account or no value), list()).append(d).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.parent\_account → no value.
- Set filtered\_accounts from list().
- Bind local operation add\_to\_list for subsequent calls.
- Evaluate add\_to\_list(no value, 0).
- Return tuple(filtered\_accounts, accounts\_by\_name, parent\_children\_map).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L4374) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L917)

<a id="op-4a03e6cc99c977"></a>
### Filter accounts.add to list

`operation_enterprise_accounts_report_financial_statements_business_behavior_filter_accounts_add_to_list`

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
    - Evaluate add\_to\_list(child.name, (level + 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L4829) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L918)

<a id="op-d41de4a301c61d"></a>
### Sort accounts

`operation_enterprise_accounts_report_financial_statements_business_behavior_sort_accounts`

**Inputs** accounts, is\_root = false, key = “name”.

**Local steps**

- Bind local operation compare\_accounts for subsequent calls.
- Evaluate accounts.sort(key = functools.cmp\_to\_key(compare\_accounts)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L5077) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L939)

<a id="op-c4eb9790f1f88a"></a>
### Sort accounts.compare accounts

`operation_enterprise_accounts_report_financial_statements_business_behavior_sort_accounts_compare_accounts`

**Inputs** a, b.

**Explicit results** (int(a at key &gt; b at key) − int(a at key &lt; b at key)) · negative 1 · 1.

**Local steps**

- If re.split(“\\W+”, a at key) at 0.isdigit().
  - Return (int(a at key &gt; b at key) − int(a at key &lt; b at key)).
- Otherwise.
  - If is\_root.
    - If (a.report\_type differs from b.report\_type and a.report\_type equals “Balance Sheet”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.report\_type differs from b.report\_type → a.report\_type equals “Balance Sheet”.
      - Return negative 1.
    - If (a.root\_type differs from b.root\_type and a.root\_type equals “Asset”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.root\_type differs from b.root\_type → a.root\_type equals “Asset”.
      - Return negative 1.
    - If (a.root\_type equals “Liability” and b.root\_type equals “Equity”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.root\_type equals “Liability” → b.root\_type equals “Equity”.
      - Return negative 1.
    - If (a.root\_type equals “Income” and b.root\_type equals “Expense”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.root\_type equals “Income” → b.root\_type equals “Expense”.
      - Return negative 1.
  - Otherwise.
    - Return (int(a at key &gt; b at key) − int(a at key &lt; b at key)).
- Return 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0247.json#L5721) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L940)

<a id="op-5952aec98804cd"></a>
### Set gl entries by account

`operation_enterprise_accounts_report_financial_statements_business_behavior_set_general_ledger_entries_by_account`

**Inputs** company, from\_date, to\_date, filters, gl\_entries\_by\_account, root\_lft = no value, root\_rgt = no value, root\_type = no value, ignore\_closing\_entries = false, ignore\_opening\_entries = false, group\_by\_account = false, ignore\_reporting\_currency = true.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Period Closing Voucher” via get\_all.

**Explicit results** gl\_entries\_by\_account.

**Local steps**

- Set gl\_entries from list().
- Set ignore\_closing\_balances from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).
- Set ignore\_closing\_balances from (ignore\_closing\_balances or has\_gl\_entry\_restrictions()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_closing\_balances → has\_gl\_entry\_restrictions().
- If (not from\_date and not ignore\_closing\_balances).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_date → not ignore\_closing\_balances.
  - Set last\_period\_closing\_voucher from Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“docstatus” → 1, “company” → filters.company, “period\_end\_date” → tuple(“&lt;”, filters at “period\_start\_date”)), fields = list(“period\_end\_date ….
  - If last\_period\_closing\_voucher.
    - Update gl\_entries using + get\_accounting\_entries(“Account Closing Balance”, from\_date, to\_date, filters, group\_by\_account = group\_by\_account, ignore\_reporting\_currency = ignore\_reporting\_currency, …).
    - Set from\_date from add\_days(last\_period\_closing\_voucher at 0.period\_end\_date, 1).
    - Set ignore\_opening\_entries from true.
- Update gl\_entries using + get\_accounting\_entries(“GL Entry”, from\_date, to\_date, filters, ignore\_opening\_entries = ignore\_opening\_entries, group\_by\_account = group\_by\_account, ignore\_reporting\_currency = ignore\_reporting\_currency, …).
- If (filters and filters.get(“presentation\_currency”) and ignore\_reporting\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“presentation\_currency”) → ignore\_reporting\_currency.
  - Evaluate convert\_to\_presentation\_currency(gl\_entries, get\_currency(filters)).
- For each entry in gl\_entries.
  - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).
- Return gl\_entries\_by\_account.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L938)

<a id="op-69cbe709df57bf"></a>
### Get accounting entries

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_accounting_entries`

**Inputs** doctype, from\_date, to\_date, filters, root\_lft = no value, root\_rgt = no value, root\_type = no value, ignore\_closing\_entries = no value, period\_closing\_voucher = no value, ignore\_opening\_entries = false, group\_by\_account = false, ignore\_reporting\_currency = true.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set gl\_entry from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract.qb.from\_(gl\_entry).select(gl\_entry.account, gl\_entry.debit when not group\_by\_account, otherwise nested operand in the contract(nested operand in the contract).as\_(“debit”), g ….
  - Value choice on not group\_by\_account — true gives gl\_entry.debit, false gives Sum(gl\_entry.debit).as\_(“debit”).
  - Value choice on not group\_by\_account — true gives gl\_entry.credit, false gives Sum(gl\_entry.credit).as\_(“credit”).
  - Value choice on not group\_by\_account — true gives gl\_entry.debit\_in\_account\_currency, false gives Sum(gl\_entry.debit\_in\_account\_currency).as\_(“debit\_in\_account\_currency”).
  - Value choice on not group\_by\_account — true gives gl\_entry.credit\_in\_account\_currency, false gives Sum(gl\_entry.credit\_in\_account\_currency).as\_(“credit\_in\_account\_currency”).
- If (filters.group\_by\_dimension and doctype belongs to get\_doctypes\_with\_dimensions() and not group\_by\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.group\_by\_dimension → doctype belongs to get\_doctypes\_with\_dimensions() → not group\_by\_account.
  - Set dimension\_field from get\_dimension\_fieldname(filters.group\_by\_dimension).
  - Set query from query.select(gl\_entry at dimension\_field).
- If not ignore\_reporting\_currency.
  - Set query from query.select(gl\_entry.debit\_in\_reporting\_currency when not group\_by\_account, otherwise Sum(gl\_entry.debit\_in\_reporting\_currency).as\_(“debit\_in\_reporting\_currency”), gl\_entry.credit\_in\_reporting\_currency wh ….
    - Value choice on not group\_by\_account — true gives gl\_entry.debit\_in\_reporting\_currency, false gives Sum(gl\_entry.debit\_in\_reporting\_currency).as\_(“debit\_in\_reporting\_currency”).
    - Value choice on not group\_by\_account — true gives gl\_entry.credit\_in\_reporting\_currency, false gives Sum(gl\_entry.credit\_in\_reporting\_currency).as\_(“credit\_in\_reporting\_currency”).
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- If doctype equals “GL Entry”.
  - Set query from query.select(gl\_entry.posting\_date, gl\_entry.is\_opening, gl\_entry.fiscal\_year).
  - Set query from query.where(gl\_entry.is\_cancelled equals 0).
  - Set query from query.where(gl\_entry.posting\_date ≤ to\_date).
  - Set query from query.force\_index(“posting\_date\_company\_index”).
  - If (ignore\_opening\_entries and not ignore\_is\_opening).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_opening\_entries → not ignore\_is\_opening.
    - Set query from query.where(gl\_entry.is\_opening equals “No”).
- Otherwise.
  - Set query from query.select(gl\_entry.closing\_date.as\_(“posting\_date”)).
  - Set query from query.where(gl\_entry.period\_closing\_voucher equals period\_closing\_voucher).
- Set query from apply\_additional\_conditions(doctype, query, from\_date, ignore\_closing\_entries, …).
- If ((root\_lft and root\_rgt) or root\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (root\_lft and root\_rgt) → root\_type.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_lft → root\_rgt.
  - Set account\_filter\_query from get\_account\_filter\_query(root\_lft, root\_rgt, root\_type, gl\_entry).
  - Set query from query.where(ExistsCriterion(account\_filter\_query)).
- If group\_by\_account.
  - Set query from query.groupby(“account”).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(doctype).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L922)

<a id="op-41a63cc460bc2d"></a>
### Get account filter query

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_account_filter_query`

**Inputs** root\_lft, root\_rgt, root\_type, gl\_entry.

**Explicit results** exists\_query.

**Local steps**

- Set acc from Platform.qb.DocType(“Account”).
- Set exists\_query from nested operand in the contract(nested operand in the contract).select(acc.name).where(acc.name equals gl\_entry.account).where(acc.is\_group equals 0).
- If (root\_lft and root\_rgt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_lft → root\_rgt.
  - Set exists\_query from exists\_query.where(acc.lft ≥ root\_lft).where(acc.rgt ≤ root\_rgt).
- If root\_type.
  - Set exists\_query from exists\_query.where(acc.root\_type equals root\_type).
- Return exists\_query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0248.json#L1776) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L921)
