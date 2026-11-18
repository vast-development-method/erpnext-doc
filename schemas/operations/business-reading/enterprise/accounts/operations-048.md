# Accounting and settlement · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · General ledger

<a id="op-8653ce24890008"></a>
### Get accountwise gle

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_accountwise_general_ledger_entry`

**Inputs** filters, accounting\_dimensions, gl\_entries, gle\_map.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** tuple(totals, entries).

**Local steps**

- Set entries from list().
- Set consolidated\_gle from mapping().
- Set group\_by from get\_group\_by\_fields(filters.get(“categorize\_by”)).
- Set group\_by\_voucher\_consolidated from filters.get(“categorize\_by”) equals “Categorize by Voucher (Consolidated)”.
- If filters.get(“show\_net\_values\_in\_party\_account”).
  - Set account\_type\_map from get\_account\_type\_map(filters.get(“company”)).
- Set immutable\_ledger from Platform.get\_single\_value(“Accounts Settings”, “enable\_immutable\_ledger”).
- Bind local operation update\_value\_in\_dict for subsequent calls.
- Set tuple(from\_date, to\_date) from tuple(getdate(filters.from\_date), getdate(filters.to\_date)).
- Set show\_opening\_entries from filters.get(“show\_opening\_entries”).
- Set totals from get\_totals\_dict().
- For each gle in gl\_entries.
  - Set group\_by\_value from get\_group\_by\_value(gle, group\_by).
  - Set gle.voucher\_subtype from translated gle.voucher\_subtype.
  - Set gle.remarks from translated gle.remarks.
  - Set gle.party\_type from translated gle.party\_type.
  - If (gle.posting\_date &lt; from\_date or (cstr(gle.is\_opening) equals “Yes” and not show\_opening\_entries and not filters.disable\_opening\_balance\_calculation)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in gle.posting\_date &lt; from\_date → (cstr(gle.is\_opening) equals “Yes” and not show\_opening\_entries and not filters.disable\_opening\_balance\_calculation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cstr(gle.is\_opening) equals “Yes” → not show\_opening\_entries → not filters.disable\_opening\_balance\_calculation.
    - If not group\_by\_voucher\_consolidated.
      - Evaluate update\_value\_in\_dict(gle\_map at group\_by\_value.totals, “opening”, gle, true).
      - Evaluate update\_value\_in\_dict(gle\_map at group\_by\_value.totals, “closing”, gle, true).
    - Evaluate update\_value\_in\_dict(totals, “opening”, gle, true).
    - Evaluate update\_value\_in\_dict(totals, “closing”, gle, true).
  - Otherwise.
    - If (gle.posting\_date ≤ to\_date or (cstr(gle.is\_opening) equals “Yes” and show\_opening\_entries)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in gle.posting\_date ≤ to\_date → (cstr(gle.is\_opening) equals “Yes” and show\_opening\_entries).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cstr(gle.is\_opening) equals “Yes” → show\_opening\_entries.
      - If not group\_by\_voucher\_consolidated.
        - Evaluate update\_value\_in\_dict(gle\_map at group\_by\_value.totals, “total”, gle).
        - Evaluate update\_value\_in\_dict(gle\_map at group\_by\_value.totals, “closing”, gle).
        - Evaluate update\_value\_in\_dict(totals, “total”, gle).
        - Evaluate update\_value\_in\_dict(totals, “closing”, gle).
        - Evaluate gle\_map at group\_by\_value.entries.append(gle).
      - Otherwise.
        - If group\_by\_voucher\_consolidated.
          - Set keylist from list(gle.get(“posting\_date”), gle.get(“voucher\_type”), gle.get(“voucher\_no”), gle.get(“account”), …).
          - If immutable\_ledger.
            - Evaluate keylist.append(gle.get(“creation”)).
          - If filters.get(“include\_dimensions”).
            - For each dim in accounting\_dimensions.
              - Evaluate keylist.append(gle.get(dim)).
            - Evaluate keylist.append(gle.get(“cost\_center”)).
            - Evaluate keylist.append(gle.get(“project”)).
          - Set key from tuple(keylist).
          - If key does not belong to consolidated\_gle.
            - Evaluate consolidated\_gle.setdefault(key, gle).
          - Otherwise.
            - Evaluate update\_value\_in\_dict(consolidated\_gle, key, gle).
  - If filters.get(“include\_dimensions”).
    - Set dimensions from list(expanded accounting\_dimensions, “cost\_center”, “project”).
    - For each dimension in dimensions.
      - If val bound to gle.get(dimension).
        - Set gle at dimension from translated val.
- For each value in consolidated\_gle.values().
  - Evaluate update\_value\_in\_dict(totals, “total”, value).
  - Evaluate update\_value\_in\_dict(totals, “closing”, value).
  - Evaluate entries.append(value).
- Return tuple(totals, entries).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_immutable\_ledger”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L962)

<a id="op-e0bf2be83955e9"></a>
### Get accountwise gle.update value in dict

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_accountwise_general_ledger_entry_update_value_in_mapping`

**Inputs** data, key, gle, show\_net\_values = false.

**Local steps**

- Update data at key.debit using + gle.debit.
- Update data at key.credit using + gle.credit.
- Update data at key.debit\_in\_account\_currency using + gle.debit\_in\_account\_currency.
- Update data at key.credit\_in\_account\_currency using + gle.credit\_in\_account\_currency.
- If (filters.get(“add\_values\_in\_transaction\_currency”) and key does not belong to list(“opening”, “closing”, “total”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“add\_values\_in\_transaction\_currency”) → key does not belong to list(“opening”, “closing”, “total”).
  - Update data at key.debit\_in\_transaction\_currency using + gle.debit\_in\_transaction\_currency.
  - Update data at key.credit\_in\_transaction\_currency using + gle.credit\_in\_transaction\_currency.
- If ((filters.get(“show\_net\_values\_in\_party\_account”) and account\_type\_map.get(data at key.account) belongs to tuple(“Receivable”, “Payable”)) or show\_net\_values).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (filters.get(“show\_net\_values\_in\_party\_account”) and account\_type\_map.get(data at key.account) belongs to tuple(“Receivable”, “Payable”)) → show\_net\_values.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“show\_net\_values\_in\_party\_account”) → account\_type\_map.get(data at key.account) belongs to tuple(“Receivable”, “Payable”).
  - Set net\_value from (data at key.debit − data at key.credit).
  - Set net\_value\_in\_account\_currency from (data at key.debit\_in\_account\_currency − data at key.credit\_in\_account\_currency).
  - If net\_value &lt; 0.
    - Set dr\_or\_cr from “credit”.
    - Set rev\_dr\_or\_cr from “debit”.
  - Otherwise.
    - Set dr\_or\_cr from “debit”.
    - Set rev\_dr\_or\_cr from “credit”.
  - Set data at key at dr\_or\_cr from abs(net\_value).
  - Set data at key at (dr\_or\_cr + “\_in\_account\_currency”) from abs(net\_value\_in\_account\_currency).
  - Set data at key at rev\_dr\_or\_cr from 0.
  - Set data at key at (rev\_dr\_or\_cr + “\_in\_account\_currency”) from 0.
- If (data at key.against\_voucher and gle.against\_voucher).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data at key.against\_voucher → gle.against\_voucher.
  - Update data at key.against\_voucher using + (“, ” + gle.against\_voucher).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L4227) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L963)

<a id="op-f3bf66ed494d31"></a>
### Get account type map

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_account_type_map`

**Inputs** company.

**Record and data access** read “Account” via get\_all.

**Explicit results** account\_type\_map.

**Local steps**

- Set account\_type\_map from Platform.\_dict(Platform.get\_all(“Account”, fields = list(“name”, “account\_type”), filters = mapping(“company” → company), as\_list = 1)).
- Return account\_type\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L5007) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L960)

<a id="op-46ead7bd73a616"></a>
### Get result as list

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_result_as_list`

**Inputs** data, filters.

**Explicit results** data.

**Local steps**

- Set balance from 0.
- For each d in data.
  - If not d.get(“posting\_date”).
    - Set balance from 0.
  - Set balance from get\_balance(d, balance, “debit”, “credit”).
  - Set d at “balance” from balance.
  - Set d at “account\_currency” from filters.account\_currency.
  - Set d at “presentation\_currency” from filters.presentation\_currency.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L5162) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L973)

<a id="op-3e1403424fee25"></a>
### Get supplier invoice details

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_supplier_invoice_details`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Purchase Invoice).

**Explicit results** inv\_details.

**Local steps**

- Set inv\_details from mapping().
- For each d in Platform.db.sql(query text (SELECT, Purchase Invoice), as\_dict = 1).
  - Set inv\_details at d.name from d.bill\_no.
- Return inv\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L975)

<a id="op-e6790fc769fda1"></a>
### Get balance

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_balance`

**Inputs** row, balance, debit\_field, credit\_field.

**Explicit results** balance.

**Local steps**

- Update balance using + (row.get(debit\_field, 0) − row.get(credit\_field, 0)).
- Return balance.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L5602) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L964)

<a id="op-910471f6633171"></a>
### Get columns

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_columns`

**Inputs** filters.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Selling Settings” via get\_single\_value.

**Explicit results** columns.

**Explicit failure paths** validation helper — translated formatted text Presentation Currency cannot be {Platform.bold(filters at “presentation\_currency”)} , When {Platform.bold(“Show Credit / Debit in Company Currency”)}.

**Local steps**

- If filters.get(“presentation\_currency”).
  - Set currency from filters at “presentation\_currency”.
- Otherwise.
  - Set company from (filters.get(“company”) or get\_default\_company()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → get\_default\_company().
  - Set filters at “presentation\_currency”, currency from get\_company\_currency(company).
- Set company\_currency from get\_company\_currency((filters.get(“company”) or get\_default\_company())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → get\_default\_company().
- If (filters.get(“show\_amount\_in\_company\_currency”) and filters at “presentation\_currency” differs from company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“show\_amount\_in\_company\_currency”) → filters at “presentation\_currency” differs from company\_currency.
  - Call the validation error handler Platform.throw(translated formatted text Presentation Currency cannot be {Platform.bold(filters at “presentation\_currency”)} , When {Platform.bold(“Show Credit / Debit in Company Currency”)} ).
- Set columns from list(mapping(“label” → translated “GL Entry”, “fieldname” → “gl\_entry”, “fieldtype” → “Link”, “options” → “GL Entry”, …), mapping(“label” → translated “Posting Date”, “fieldname” → “posting\_date”, “fieldty ….
- If filters.get(“add\_values\_in\_transaction\_currency”).
  - Update columns using + list(mapping(“label” → translated “Debit (Transaction)”, “fieldname” → “debit\_in\_transaction\_currency”, “fieldtype” → “Currency”, “width” → 130, …), mapping(“label” → translated “Credit (Transaction)”, “fi ….
- Update columns using + list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Voucher Subtype”, “fieldname” → “voucher\_subty ….
- Set supplier\_master\_name from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).
- Set customer\_master\_name from Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).
- If (supplier\_master\_name differs from “Supplier Name” or customer\_master\_name differs from “Customer Name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in supplier\_master\_name differs from “Supplier Name” → customer\_master\_name differs from “Customer Name”.
  - Evaluate columns.append(mapping(“label” → translated “Party Name”, “fieldname” → “party\_name”, “fieldtype” → “Data”, “width” → 150)).
- If filters.get(“include\_dimensions”).
  - Evaluate columns.append(mapping(“label” → translated “Project”, “options” → “Project”, “fieldname” → “project”, “width” → 100)).
  - For each dim in get\_accounting\_dimensions(as\_list = false).
    - Evaluate columns.append(mapping(“label” → translated dim.label, “options” → dim.label, “fieldname” → dim.fieldname, “width” → 100)).
  - Evaluate columns.append(mapping(“label” → translated “Cost Center”, “options” → “Cost Center”, “fieldname” → “cost\_center”, “width” → 100)).
- Evaluate columns.extend(list(mapping(“label” → translated “Against Voucher Type”, “fieldname” → “against\_voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Against Voucher ….
- If filters.get(“show\_remarks”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Remarks”, “fieldname” → “remarks”, “width” → 400))).
- Return columns.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”), Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L965)

<a id="op-af4260aab17815"></a>
### Execute snapshot report

`operation_enterprise_accounts_report_general_ledger_business_behavior_execute_snapshot_report`

**Inputs** filters.

**Explicit results** execute(filters) · \_execute\_with\_duckdb\_conn(filters, conn).

**Explicit failure paths** validation helper — translated “General Ledger requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”)).

**Local steps**

- If has\_gl\_entry\_restrictions().
  - Return execute(filters).
- Bind dependencies get\_latest\_sync.
- If conn bound to get\_latest\_sync(“GL Entry”).
  - Return \_execute\_with\_duckdb\_conn(filters, conn).
- Call the validation error handler Platform.throw(translated “General Ledger requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L958)

<a id="op-41de9aa3692ce5"></a>
### Execute with duckdb conn

`operation_enterprise_accounts_report_general_ledger_business_behavior_execute_with_duckdb_conn`

**Inputs** filters, conn.

**Record and data access** read “Account” via get\_all.

**Explicit results** tuple(list(), list()) · tuple(columns, res).

**Explicit failure paths** validation helper — translated “Select an account to print in account currency”.

**Local steps**

- If not filters.
  - Return tuple(list(), list()).
- Set account\_details from mapping().
- If (filters.get(“print\_in\_account\_currency”) and not filters.get(“account”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“print\_in\_account\_currency”) → not filters.get(“account”).
  - Call the validation error handler Platform.throw(translated “Select an account to print in account currency”).
- For each acc in Platform.get\_all(“Account”, fields = list(“name”, “is\_group”)).
  - Evaluate account\_details.setdefault(acc.name, acc).
- If filters.get(“party”).
  - Set filters.party from Platform.parse\_json(filters.get(“party”)).
- Evaluate validate\_filters(filters, account\_details).
- Evaluate validate\_party(filters).
- Set filters from set\_account\_currency(filters).
- Set columns from get\_columns(filters).
- Set res from get\_result\_duckdb(filters, account\_details, conn).
- Return tuple(columns, res).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0252.json#L3254) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L959)

<a id="op-a7ac3b82d0ef5f"></a>
### Get result duckdb

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_result_duckdb`

**Inputs** filters, account\_details, conn.

**Explicit results** get\_result\_as\_list(data, filters).

**Local steps**

- Set accounting\_dimensions from list().
- If filters.get(“include\_dimensions”).
  - Set accounting\_dimensions from get\_accounting\_dimensions().
- Set gl\_entries from get\_gl\_entries\_duckdb(filters, accounting\_dimensions, conn).
- Set data from get\_data\_with\_opening\_closing(filters, account\_details, accounting\_dimensions, gl\_entries).
- Return get\_result\_as\_list(data, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0252.json#L3769) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L974)

<a id="op-7dd7a4e9f6c725"></a>
### Get gl entries duckdb

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_general_ledger_entries_duckdb`

**Inputs** filters, accounting\_dimensions, conn.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Company” via get\_cached\_value.

**Explicit results** convert\_gl\_entries\_currency(gl\_entries, currency\_map, filters).

**Local steps**

- Set currency\_map from get\_currency(filters).
- Set col\_names from list(“gl\_entry”, “posting\_date”, “account”, “party\_type”, …).
- Set select\_exprs from list(“name”, “posting\_date”, “account”, “party\_type”, …).
- If filters.get(“show\_remarks”).
  - Set remarks\_length from Platform.get\_single\_value(“Accounts Settings”, “general\_ledger\_remarks\_length”).
  - If remarks\_length.
    - Evaluate select\_exprs.append(formatted text substr(remarks, 1, {int(remarks\_length)})).
  - Otherwise.
    - Evaluate select\_exprs.append(“remarks”).
  - Evaluate col\_names.append(“remarks”).
- If filters.get(“add\_values\_in\_transaction\_currency”).
  - Update select\_exprs using + list(“debit\_in\_transaction\_currency”, “credit\_in\_transaction\_currency”, “transaction\_currency”).
  - Update col\_names using + list(“debit\_in\_transaction\_currency”, “credit\_in\_transaction\_currency”, “transaction\_currency”).
- If accounting\_dimensions.
  - Update select\_exprs using + accounting\_dimensions.
  - Update col\_names using + accounting\_dimensions.
- Set order\_by from “posting\_date, account, creation”.
- If filters.get(“include\_dimensions”).
  - Set order\_by from “posting\_date, creation”.
- If filters.get(“categorize\_by”) equals “Categorize by Voucher”.
  - Set order\_by from “posting\_date, voucher\_type, voucher\_no”.
- If filters.get(“categorize\_by”) equals “Categorize by Account”.
  - Set order\_by from “account, posting\_date, creation”.
- If filters.get(“include\_default\_book\_entries”).
  - Set filters at “company\_fb” from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_finance\_book”).
- Set tuple(conditions, params) from \_build\_gl\_conditions\_duckdb(filters).
- Set select\_clause from “, ”.join(select\_exprs).
- Set sql from formatted text SELECT {select\_clause} FROM "tabGL Entry" WHERE {“ AND ”.join(conditions)} ORDER BY {order\_by}.
- Set rows from conn.execute(sql, params).fetchall().
- Set gl\_entries from list of Platform.\_dict(zip(col\_names, row, strict = false)) for row drawn from rows.
  - Draw row from rows.
- Set party\_name\_map from get\_party\_name\_map().
- For each gl\_entry in gl\_entries.
  - If (gl\_entry.party\_type and gl\_entry.party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_entry.party\_type → gl\_entry.party.
    - Set gl\_entry.party\_name from party\_name\_map.get(gl\_entry.party\_type, mapping()).get(gl\_entry.party).
- Return convert\_gl\_entries\_currency(gl\_entries, currency\_map, filters).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “general\_ledger\_remarks\_length”), Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L970)

<a id="op-e86ae1fec65e05"></a>
### Build gl conditions duckdb

`operation_enterprise_accounts_report_general_ledger_business_behavior_build_general_ledger_conditions_duckdb`

**Inputs** filters.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Journal Entry” via get\_all · read “Company” via get\_cached\_value · read “DocType” via get\_cached\_value.

**Explicit results** tuple(conditions, params).

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- Set conditions from list(“company = ?”).
- Set params from list(filters.company).
- If filters.get(“account”).
  - Set filters.account from get\_accounts\_with\_children(filters.account).
  - If filters.account.
    - Evaluate conditions.append(formatted text account IN ({“, ”.join((list(“?”) × len(filters.account)))})).
    - Evaluate params.extend(filters.account).
- If filters.get(“cost\_center”).
  - Set filters.cost\_center from get\_cost\_centers\_with\_children(filters.cost\_center).
  - Evaluate conditions.append(formatted text cost\_center IN ({“, ”.join((list(“?”) × len(filters.cost\_center)))})).
  - Evaluate params.extend(filters.cost\_center).
- If filters.get(“voucher\_no”).
  - Evaluate conditions.append(“voucher\_no = ?”).
  - Evaluate params.append(filters.voucher\_no).
- If filters.get(“against\_voucher\_no”).
  - Evaluate conditions.append(“against\_voucher = ?”).
  - Evaluate params.append(filters.against\_voucher\_no).
- If filters.get(“ignore\_err”).
  - Set err\_journals from Platform.db.get\_all(“Journal Entry”, filters = mapping(“company” → filters.get(“company”), “docstatus” → 1, “voucher\_type” → tuple(“in”, list(“Exchange Rate Revaluation”, “Exchange Gain Or Loss”))), pluck = “name”).
  - If err\_journals.
    - Evaluate filters.update(mapping(“voucher\_no\_not\_in” → err\_journals)).
- If filters.get(“ignore\_cr\_dr\_notes”).
  - Set system\_generated from Platform.db.get\_all(“Journal Entry”, filters = mapping(“company” → filters.get(“company”), “docstatus” → 1, “voucher\_type” → tuple(“in”, list(“Credit Note”, “Debit Note”)), “is\_system\_generated” → 1), pluc ….
  - If system\_generated.
    - Set vouchers\_to\_ignore from ((filters.get(“voucher\_no\_not\_in”) or list()) + system\_generated).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“voucher\_no\_not\_in”) → list().
    - Evaluate filters.update(mapping(“voucher\_no\_not\_in” → vouchers\_to\_ignore)).
- If filters.get(“voucher\_no\_not\_in”).
  - Set vouchers from filters.voucher\_no\_not\_in.
  - Evaluate conditions.append(formatted text voucher\_no NOT IN ({“, ”.join((list(“?”) × len(vouchers)))})).
  - Evaluate params.extend(vouchers).
- If (filters.get(“categorize\_by”) equals “Categorize by Party” and not filters.get(“party\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“categorize\_by”) equals “Categorize by Party” → not filters.get(“party\_type”).
  - Evaluate conditions.append(“party\_type IN ('Customer', 'Supplier')”).
- If filters.get(“party\_type”).
  - Evaluate conditions.append(“party\_type = ?”).
  - Evaluate params.append(filters.party\_type).
- If filters.get(“party”).
  - Evaluate conditions.append(formatted text party IN ({“, ”.join((list(“?”) × len(filters.party)))})).
  - Evaluate params.extend(filters.party).
- If filters.get(“disable\_opening\_balance\_calculation”).
  - If not ignore\_is\_opening.
    - Evaluate conditions.append(“(posting\_date &gt;= ? OR is\_opening = 'Yes')”).
  - Otherwise.
    - Evaluate conditions.append(“posting\_date &gt;= ?”).
  - Evaluate params.append(filters.from\_date).
- Otherwise.
  - If not (filters.get(“account”) or filters.get(“party”) or filters.get(“categorize\_by”) belongs to list(“Categorize by Account”, “Categorize by Party”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“account”) → filters.get(“party”) → filters.get(“categorize\_by”) belongs to list(“Categorize by Account”, “Categorize by Party”).
    - If not ignore\_is\_opening.
      - Evaluate conditions.append(“(posting\_date &gt;= ? OR is\_opening = 'Yes')”).
    - Otherwise.
      - Evaluate conditions.append(“posting\_date &gt;= ?”).
    - Evaluate params.append(filters.from\_date).
- If not ignore\_is\_opening.
  - Evaluate conditions.append(“(posting\_date &lt;= ? OR is\_opening = 'Yes')”).
- Otherwise.
  - Evaluate conditions.append(“posting\_date &lt;= ?”).
- Evaluate params.append(filters.to\_date).
- If filters.get(“project”).
  - Evaluate conditions.append(formatted text project IN ({“, ”.join((list(“?”) × len(filters.project)))})).
  - Evaluate params.extend(filters.project).
- Set company\_fb from (filters.get(“company\_fb”) or Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company\_fb”) → Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
- If filters.get(“include\_default\_book\_entries”).
  - If filters.get(“finance\_book”).
    - If (company\_fb and cstr(filters.finance\_book) differs from cstr(company\_fb)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_fb → cstr(filters.finance\_book) differs from cstr(company\_fb).
      - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
    - Set fb\_vals from list(cstr(filters.finance\_book), empty text).
  - Otherwise.
    - Set fb\_vals from list(cstr(company\_fb), empty text).
  - Evaluate conditions.append(formatted text (finance\_book IN ({“, ”.join((list(“?”) × len(fb\_vals)))}) OR finance\_book IS NULL)).
  - Evaluate params.extend(fb\_vals).
- Otherwise.
  - If filters.get(“finance\_book”).
    - Evaluate conditions.append(“(finance\_book IN (?, '') OR finance\_book IS NULL)”).
    - Evaluate params.append(cstr(filters.finance\_book)).
  - Otherwise.
    - Evaluate conditions.append(“(finance\_book IN ('') OR finance\_book IS NULL)”).
- If not filters.get(“show\_cancelled\_entries”).
  - Evaluate conditions.append(“is\_cancelled = 0”).
- Set accounting\_dimensions\_list from get\_accounting\_dimensions(as\_list = false).
- If accounting\_dimensions\_list.
  - For each dimension in accounting\_dimensions\_list.
    - If (not dimension.disabled and dimension.document\_type differs from “Finance Book”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not dimension.disabled → dimension.document\_type differs from “Finance Book”.
      - If filters.get(dimension.fieldname).
        - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
          - Set filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, filters.get(dimension.fieldname)).
        - Set vals from filters at dimension.fieldname when isinstance(filters at dimension.fieldname, list), otherwise list(filters at dimension.fieldname).
          - Value choice on isinstance(filters at dimension.fieldname, list) — true gives filters at dimension.fieldname, false gives list(filters at dimension.fieldname).
        - Evaluate conditions.append(formatted text {dimension.fieldname} IN ({“, ”.join((list(“?”) × len(vals)))})).
        - Evaluate params.extend(vals).
- Return tuple(conditions, params).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”), Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0253.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L956)

## Service · General ledger

<a id="op-75f652e99d2e0c"></a>
### Make gl entries

`operation_enterprise_accounts_general_ledger_business_behavior_make_general_ledger_entries`

**Inputs** gl\_map, cancel = false, adv\_adj = false, merge\_entries = true, update\_outstanding = “Yes”, from\_repost = false.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Incorrect number of General Ledger Entries found. You might have selected a wrong Account in the transaction.”.

**Local steps**

- If gl\_map.
  - If (not cancel and not cint(Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_budget\_controller”)) and gl\_map at 0.voucher\_type differs from “Period Closing Voucher”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cancel → not cint(Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_budget\_controller”)) → gl\_map at 0.voucher\_type differs from “Period Closing Voucher”.
    - Set bud\_val from BudgetValidation(gl\_map = gl\_map).
    - Evaluate bud\_val.validate().
  - If not cancel.
    - Evaluate make\_acc\_dimensions\_offsetting\_entry(gl\_map).
    - Evaluate validate\_accounting\_period(gl\_map).
    - Evaluate validate\_disabled\_accounts(gl\_map).
    - Set gl\_map from process\_gl\_map(gl\_map, merge\_entries, from\_repost = from\_repost).
    - If (gl\_map and len(gl\_map) &gt; 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_map → len(gl\_map) &gt; 1.
      - If gl\_map at 0.voucher\_type differs from “Period Closing Voucher”.
        - Evaluate create\_payment\_ledger\_entry(gl\_map, cancel = 0, adv\_adj = adv\_adj, update\_outstanding = update\_outstanding, from\_repost = from\_repost).
      - Evaluate save\_entries(gl\_map, adv\_adj, update\_outstanding, from\_repost).
    - Otherwise.
      - If gl\_map.
        - Call the validation error handler Platform.throw(translated “Incorrect number of General Ledger Entries found. You might have selected a wrong Account in the transaction.”).
  - Otherwise.
    - Evaluate make\_reverse\_gl\_entries(gl\_map, adv\_adj = adv\_adj, update\_outstanding = update\_outstanding).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_budget\_controller”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L39)

<a id="op-944360b7399262"></a>
### Make acc dimensions offsetting entry

`operation_enterprise_accounts_general_ledger_business_behavior_make_accounting_dimensions_offsetting_entry`

**Inputs** gl\_map.

**Explicit results** no value.

**Local steps**

- Set accounting\_dimensions\_to\_offset from get\_accounting\_dimensions\_for\_offsetting\_entry(gl\_map, gl\_map at 0.company).
- Set no\_of\_dimensions from len(accounting\_dimensions\_to\_offset).
- If no\_of\_dimensions equals 0.
  - Return no value.
- Set offsetting\_entries from list().
- For each gle in gl\_map.
  - For each dimension in accounting\_dimensions\_to\_offset.
    - Set offsetting\_entry from gle.copy().
    - Set debit from (flt(gle.credit) ÷ no\_of\_dimensions) when gle.credit differs from 0, otherwise 0.
      - Value choice on gle.credit differs from 0 — true gives (flt(gle.credit) ÷ no\_of\_dimensions), false gives 0.
    - Set credit from (flt(gle.debit) ÷ no\_of\_dimensions) when gle.debit differs from 0, otherwise 0.
      - Value choice on gle.debit differs from 0 — true gives (flt(gle.debit) ÷ no\_of\_dimensions), false gives 0.
    - Evaluate offsetting\_entry.update(mapping(“account” → dimension.offsetting\_account, “debit” → debit, “credit” → credit, “debit\_in\_account\_currency” → debit, …)).
    - Set offsetting\_entry at “against\_voucher\_type” from no value.
    - Evaluate offsetting\_entries.append(offsetting\_entry).
- Update gl\_map using + offsetting\_entries.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L644) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L43) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L37)

<a id="op-d626093c900628"></a>
### Get accounting dimensions for offsetting entry

`operation_enterprise_accounts_general_ledger_business_behavior_get_accounting_dimensions_for_offsetting_entry`

**Inputs** gl\_map, company.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** accounting\_dimensions\_to\_offset.

**Local steps**

- Set acc\_dimension from Platform.qb.DocType(“Accounting Dimension”).
- Set dimension\_detail from Platform.qb.DocType(“Accounting Dimension Detail”).
- Set acc\_dimensions from nested operand in the contract(nested operand in the contract).select(acc\_dimension.fieldname, acc\_dimension.name, dimension\_detail.offsetting\_account).where(((nested operand in the contract.disabled equal ….
- Set accounting\_dimensions\_to\_offset from list().
- For each acc\_dimension in acc\_dimensions.
  - Set values from set(list of entry.get(acc\_dimension.fieldname) for entry drawn from gl\_map).
    - Draw entry from gl\_map.
  - Set acc\_dimension.account\_currency from Platform.get\_cached\_value(“Account”, acc\_dimension.offsetting\_account, “account\_currency”).
  - If len(values) &gt; 1.
    - Evaluate accounting\_dimensions\_to\_offset.append(acc\_dimension).
- Return accounting\_dimensions\_to\_offset.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, acc\_dimension.offsetting\_account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L1257) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L35) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L29)

<a id="op-0b998588e6992a"></a>
### Validate disabled accounts

`operation_enterprise_binding_enterprise_accounts_general_ledger_validate_disabled_accounts`

**Inputs** gl\_map.

**Record and data access** read “Account” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot create accounting entries against disabled accounts: {0}”.format(account\_list).

**Local steps**

- Set accounts from list of d.account for d drawn from gl\_map where d.account.
  - Draw d from gl\_map, keep a combination only if (d.account).
- Set disabled\_accounts from Platform.get\_all(“Account”, filters = mapping(“disabled” → 1, “is\_group” → 0, “company” → gl\_map at 0.company), fields = list(“name”)).
- Set used\_disabled\_accounts from set(accounts).intersection(set(list of d.name for d drawn from disabled\_accounts)).
  - Draw d from disabled\_accounts.
- If used\_disabled\_accounts.
  - Set account\_list from text in the contract.
  - Update account\_list using + “, ”.join(list of Platform.bold(d) for d drawn from used\_disabled\_accounts).
    - Draw d from used\_disabled\_accounts.
  - Call the validation error handler Platform.throw(translated “Cannot create accounting entries against disabled accounts: {0}”.format(account\_list), title = translated “Disabled Account Selected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1101)

<a id="op-7f6414264879b0"></a>
### Validate accounting period

`operation_enterprise_binding_enterprise_accounts_general_ledger_validate_accounting_period`

**Inputs** gl\_map.

**Record and data access** execute query text (SELECT, Accounting Period).

**Explicit results** no value.

**Explicit failure paths** validation helper with ClosedAccountingPeriod — translated “You cannot create or cancel any accounting entries with in the closed Accounting Period {0}”.format(Platform.bold(accounting\_periods at 0.name)).

**Local steps**

- Set accounting\_periods from Platform.db.sql(query text (SELECT, Accounting Period), mapping(“date” → gl\_map at 0.posting\_date, “company” → gl\_map at 0.company, “voucher\_type” → gl\_map at 0.voucher\_type), as\_dict = 1).
- If accounting\_periods.
  - If accounting\_periods at 0.exempted\_role.
    - Set exempted\_roles from accounting\_periods at 0.exempted\_role.
    - If exempted\_roles belongs to Platform.get\_roles().
      - Return no value.
  - Call the validation error handler Platform.throw(translated “You cannot create or cancel any accounting entries with in the closed Accounting Period {0}”.format(Platform.bold(accounting\_periods at 0.name)), ClosedAccountingPeriod).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1097)

<a id="op-f6dced7496fbc0"></a>
### Process gl map

`operation_enterprise_accounts_general_ledger_business_behavior_process_general_ledger_map`

**Inputs** gl\_map, merge\_entries = true, precision = no value, from\_repost = false.

**Explicit results** list() · gl\_map.

**Local steps**

- If not gl\_map.
  - Return list().
- If gl\_map at 0.voucher\_type differs from “Period Closing Voucher”.
  - Set gl\_map from distribute\_gl\_based\_on\_cost\_center\_allocation(gl\_map, precision, from\_repost).
- If merge\_entries.
  - Set gl\_map from merge\_similar\_entries(gl\_map, precision).
- Set gl\_map from toggle\_debit\_credit\_if\_negative(gl\_map).
- Return gl\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L1808) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L44)

<a id="op-374caccf7373c4"></a>
### Distribute gl based on cost center allocation

`operation_enterprise_accounts_general_ledger_business_behavior_distribute_general_ledger_based_on_cost_center_allocation`

**Inputs** gl\_map, precision = no value, from\_repost = false.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** new\_gl\_map.

**Local steps**

- Set tuple(round\_off\_account, default\_currency) from Platform.get\_cached\_value(“Company”, gl\_map at 0.company, list(“round\_off\_account”, “default\_currency”)).
- If not precision.
  - Set precision from get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit”), currency = default\_currency).
- Set new\_gl\_map from list().
- For each d in gl\_map.
  - Set cost\_center from d.get(“cost\_center”).
  - Set cost\_center\_allocation from get\_cost\_center\_allocation\_data(gl\_map at 0 at “company”, gl\_map at 0 at “posting\_date”, cost\_center).
  - If not cost\_center\_allocation.
    - Evaluate new\_gl\_map.append(d).
    - Continue with the next iteration or loop test.
  - If not from\_repost.
    - Evaluate validate\_expense\_against\_budget(d, expense\_amount = (flt(d.debit, precision) − flt(d.credit, precision))).
  - If d.account equals round\_off\_account.
    - Set d.cost\_center from cost\_center\_allocation at 0 at 0.
    - Evaluate new\_gl\_map.append(d).
    - Continue with the next iteration or loop test.
  - Evaluate new\_gl\_map.extend(split\_gl\_entry\_by\_cost\_center\_allocation(d, cost\_center\_allocation, precision)).
- Return new\_gl\_map.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, gl\_map at 0.company, list(“round\_off\_account”, “default\_currency”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L34) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L28)

<a id="op-766ac17a2dd007"></a>
### Get transaction currency precision

`operation_enterprise_binding_enterprise_accounts_general_ledger_get_transaction_currency_precision`

**Inputs** entry, default\_precision.

**Explicit results** default\_precision · get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit\_in\_transaction\_currency”), currency = entry.transaction\_currency).

**Local steps**

- If not entry.get(“transaction\_currency”).
  - Return default\_precision.
- Return get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit\_in\_transaction\_currency”), currency = entry.transaction\_currency).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1095)

<a id="op-308c15646a4171"></a>
### Split gl entry by cost center allocation

`operation_enterprise_binding_enterprise_accounts_general_ledger_split_gl_entry_by_cost_center_allocation`

**Inputs** gl\_entry, cost\_center\_allocation, precision.

**Explicit results** split\_entries.

**Local steps**

- Set transaction\_precision from get\_transaction\_currency\_precision(gl\_entry, precision).
- Set field\_precisions from mapping(“debit” → precision, “credit” → precision, “debit\_in\_account\_currency” → precision, “credit\_in\_account\_currency” → precision, …).
- Set split\_entries from list().
- Set cumulative\_percentage from 0.
- Set allocated from dict.fromkeys(field\_precisions, 0).
- For each tuple(sub\_cost\_center, percentage) in cost\_center\_allocation.
  - Update cumulative\_percentage using + percentage.
  - Set entry from copy.deepcopy(gl\_entry).
  - Set entry.cost\_center from sub\_cost\_center.
  - For each tuple(field, field\_precision) in field\_precisions.items().
    - Set allocated\_till\_now from flt(((flt(gl\_entry.get(field)) × cumulative\_percentage) ÷ 100), field\_precision).
    - Set entry at field from flt((allocated\_till\_now − allocated at field), field\_precision).
    - Set allocated at field from allocated\_till\_now.
  - Evaluate split\_entries.append(entry).
- Return split\_entries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1096)

<a id="op-db19b4d8641f72"></a>
### Get cost center allocation data

`operation_enterprise_accounts_general_ledger_business_behavior_get_cost_center_allocation_data`

**Inputs** company, posting\_date, cost\_center.

**Wrappers, in declaration order** request\_cache.

**Record and data access** read “Cost Center Allocation” via get\_value · read “Cost Center Allocation Percentage” via get\_all.

**Explicit results** list() · records.

**Local steps**

- Set cost\_center\_allocation from Platform.db.get\_value(“Cost Center Allocation”, mapping(“docstatus” → 1, “company” → company, “valid\_from” → tuple(“&lt;=”, posting\_date), “main\_cost\_center” → cost\_center), pluck = true, order\_by = “valid\_fr ….
- If not cost\_center\_allocation.
  - Return list().
- Set records from Platform.db.get\_all(“Cost Center Allocation Percentage”, mapping(“parent” → cost\_center\_allocation), list(“cost\_center”, “percentage”), order\_by = “idx”, as\_list = true).
- Return records.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L36) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L30)

<a id="op-8fbcf5c6d9f252"></a>
### Merge similar entries

`operation_enterprise_accounts_general_ledger_business_behavior_merge_similar_entries`

**Inputs** gl\_map, precision = no value.

**Explicit results** merged\_gl\_map.

**Local steps**

- Set merged\_gl\_map from list().
- Set accounting\_dimensions from get\_accounting\_dimensions().
- Set merge\_properties from get\_merge\_properties(accounting\_dimensions).
- For each entry in gl\_map.
  - If entry.\_skip\_merge.
    - Evaluate merged\_gl\_map.append(entry).
    - Continue with the next iteration or loop test.
  - Set entry.merge\_key from get\_merge\_key(entry, merge\_properties).
  - Set same\_head from check\_if\_in\_list(entry, merged\_gl\_map).
  - If same\_head.
    - Set same\_head.debit from (flt(same\_head.debit) + flt(entry.debit)).
    - Set same\_head.debit\_in\_account\_currency from (flt(same\_head.debit\_in\_account\_currency) + flt(entry.debit\_in\_account\_currency)).
    - Set same\_head.debit\_in\_transaction\_currency from (flt(same\_head.debit\_in\_transaction\_currency) + flt(entry.debit\_in\_transaction\_currency)).
    - Set same\_head.credit from (flt(same\_head.credit) + flt(entry.credit)).
    - Set same\_head.credit\_in\_account\_currency from (flt(same\_head.credit\_in\_account\_currency) + flt(entry.credit\_in\_account\_currency)).
    - Set same\_head.credit\_in\_transaction\_currency from (flt(same\_head.credit\_in\_transaction\_currency) + flt(entry.credit\_in\_transaction\_currency)).
  - Otherwise.
    - Evaluate merged\_gl\_map.append(entry).
- Set company from gl\_map at 0.company when gl\_map, otherwise Enterprise.get\_default\_company().
  - Value choice on gl\_map — true gives gl\_map at 0.company, false gives Enterprise.get\_default\_company().
- Set company\_currency from Enterprise.get\_company\_currency(company).
- If not precision.
  - Set precision from get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit”), currency = company\_currency).
- Set merged\_gl\_map from filter(deferred anonymous expression, merged\_gl\_map).
- Set merged\_gl\_map from list(merged\_gl\_map).
- Return merged\_gl\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L3151) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L42)

<a id="op-8533dfd2ae805a"></a>
### Get merge properties

`operation_enterprise_accounts_general_ledger_business_behavior_get_merge_properties`

**Inputs** dimensions = no value.

**Explicit results** merge\_properties.

**Local steps**

- Set merge\_properties from list(“account”, “cost\_center”, “party”, “party\_type”, …).
- If dimensions.
  - Evaluate merge\_properties.extend(dimensions).
- Return merge\_properties.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L4143) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L40) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L34)
