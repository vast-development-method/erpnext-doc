# Accounting and settlement · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · General and payment ledger comparison

<a id="op-0bb06d86462ad3"></a>
### General Payment Ledger Comparison.get account currencies

`operation_enterprise_binding_enterprise_accounts_report_general_and_payment_ledger_comparison_general_and_payment_ledger_comparison_general_payment_ledger_comparison_get_account_currencies`

**Inputs** self.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping() · dict(nested operand in the contract.select(nested operand in the contract.name, nested operand in the contract.account\_currency).where(nested operand in the contract.name.isin(accounts)).run()).

**Local steps**

- Set accounts from list(set of key at 1 for key drawn from self.diff).
  - Draw key from self.diff.
- If not accounts.
  - Return mapping().
- Set account from qb.DocType(“Account”).
- Return dict(nested operand in the contract.select(nested operand in the contract.name, nested operand in the contract.account\_currency).where(nested operand in the contract.name.isin(accounts)).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1208)

<a id="op-40a4c0a2065603"></a>
### General Payment Ledger Comparison.generate data

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_generate_data`

**Inputs** self.

**Local steps**

- Set self.data from list().
- Set account\_currencies from self.get\_account\_currencies().
- For each tuple(key, val) in self.diff.items().
  - Evaluate self.data.append(Platform.\_dict(mapping(“company” → key at 0, “account” → key at 1, “voucher\_type” → key at 2, “voucher\_no” → key at 3, …))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get account currencies](operations-047.md#op-0bb06d86462ad3).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L945)

<a id="op-26127686ce4c6b"></a>
### General Payment Ledger Comparison.get columns

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- Evaluate self.columns.append(dict(label = translated “Company”, fieldname = “company”, fieldtype = “Link”, options = “Company”, …)).
- Evaluate self.columns.append(dict(label = translated “Account”, fieldname = “account”, fieldtype = “Link”, options = “Account”, …)).
- Evaluate self.columns.append(dict(label = translated “Voucher Type”, fieldname = “voucher\_type”, fieldtype = “Link”, options = “DocType”, …)).
- Evaluate self.columns.append(dict(label = translated “Voucher No”, fieldname = “voucher\_no”, fieldtype = “Dynamic Link”, options = “voucher\_type”, …)).
- Evaluate self.columns.append(dict(label = translated “Party Type”, fieldname = “party\_type”, fieldtype = “Link”, options = “DocType”, …)).
- Evaluate self.columns.append(dict(label = translated “Party”, fieldname = “party”, fieldtype = “Dynamic Link”, options = “party\_type”, …)).
- Evaluate self.columns.append(dict(label = translated “Against Voucher Type”, fieldname = “against\_voucher\_type”, fieldtype = “Link”, options = “DocType”, …)).
- Evaluate self.columns.append(dict(label = translated “Against Voucher”, fieldname = “against\_voucher\_no”, fieldtype = “Dynamic Link”, options = “against\_voucher\_type”, …)).
- Evaluate self.columns.append(dict(label = translated “GL Balance”, fieldname = “gl\_balance”, fieldtype = “Currency”, options = “Company:company:default\_currency”, …)).
- Evaluate self.columns.append(dict(label = translated “Payment Ledger Balance”, fieldname = “pl\_balance”, fieldtype = “Currency”, options = “Company:company:default\_currency”, …)).
- Evaluate self.columns.append(dict(label = translated “GL Balance (Account Currency)”, fieldname = “gl\_balance\_in\_account\_currency”, fieldtype = “Currency”, options = “account\_currency”, …)).
- Evaluate self.columns.append(dict(label = translated “Payment Ledger Balance (Account Currency)”, fieldname = “pl\_balance\_in\_account\_currency”, fieldtype = “Currency”, options = “account\_currency”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L948)

<a id="op-d649c281f7f9a1"></a>
### General Payment Ledger Comparison.run

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_general_payment_ledger_comparison_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Evaluate self.get\_accounts().
- Evaluate self.generate\_filters().
- Evaluate self.get\_gle().
- Evaluate self.get\_ple().
- Evaluate self.compare().
- Evaluate self.remove\_restricted\_parties().
- Evaluate self.generate\_data().
- Evaluate self.get\_columns().
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [get accounts](operations-046.md#op-9f15ea51fa8317), [generate filters](operations-046.md#op-56ca2acaa50429), [get gle](operations-046.md#op-026c0a3734e74f), [get ple](operations-046.md#op-9201d7760ba397), [compare](operations-046.md#op-b7d111c2211bec), [remove restricted parties](operations-046.md#op-936aa3b582767c), [generate data](operations-047.md#op-40a4c0a2065603), [get columns](operations-047.md#op-26127686ce4c6b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L952)

<a id="op-ab9df1d204f9d6"></a>
### Execute

`operation_enterprise_accounts_report_general_and_payment_ledger_comparison_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters, “period\_start\_date”, “period\_end\_date”).
- Set tuple(columns, data) from tuple(list(), list()).
- Set rpt from General\_Payment\_Ledger\_Comparison(filters).
- Set tuple(columns, data) from rpt.run().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L943)

## Report · General ledger

<a id="op-d8c401fad4e326"></a>
### Execute

`operation_enterprise_accounts_report_general_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** execute query text (SELECT, Account).

**Explicit results** tuple(list(), list()) · tuple(columns, res).

**Explicit failure paths** validation helper — translated “Select an account to print in account currency”.

**Local steps**

- If not filters.
  - Return tuple(list(), list()).
- Set account\_details from mapping().
- If (filters and filters.get(“print\_in\_account\_currency”) and not filters.get(“account”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“print\_in\_account\_currency”) → not filters.get(“account”).
  - Call the validation error handler Platform.throw(translated “Select an account to print in account currency”).
- For each acc in Platform.db.sql(query text (SELECT, Account), as\_dict = 1).
  - Evaluate account\_details.setdefault(acc.name, acc).
- If filters.get(“party”).
  - Set filters.party from Platform.parse\_json(filters.get(“party”)).
- Evaluate validate\_filters(filters, account\_details).
- Evaluate validate\_party(filters).
- Set filters from set\_account\_currency(filters).
- Set columns from get\_columns(filters).
- Set res from get\_result(filters, account\_details).
- Return tuple(columns, res).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L957)

<a id="op-4b41e010f3701f"></a>
### Validate filters

`operation_enterprise_accounts_report_general_ledger_business_behavior_validate_filters`

**Inputs** filters, account\_details.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”) · validation helper — translated “{0} and {1} are mandatory”.format(Platform.bold(translated “From Date”), Platform.bold(translated “To Date”)) · validation helper — translated “Account {0} does not exists”.format(account) · validation helper — translated “Can not filter based on Child Account, if grouped by Account” · validation helper — translated “Can not filter based on Voucher No, if grouped by Voucher”.

**Local steps**

- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- If (not filters.get(“from\_date”) or not filters.get(“to\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“from\_date”) → not filters.get(“to\_date”).
  - Call the validation error handler Platform.throw(translated “{0} and {1} are mandatory”.format(Platform.bold(translated “From Date”), Platform.bold(translated “To Date”))).
- If filters.get(“account”).
  - Set filters.account from Platform.parse\_json(filters.get(“account”)).
  - For each account in filters.account.
    - If not account\_details.get(account).
      - Call the validation error handler Platform.throw(translated “Account {0} does not exists”.format(account)).
- If (not filters.get(“categorize\_by”) and filters.get(“group\_by”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.get(“categorize\_by”) → filters.get(“group\_by”).
  - Set filters at “categorize\_by” from filters at “group\_by”.
  - Set filters at “categorize\_by” from filters at “categorize\_by”.replace(“Group by”, “Categorize by”).
- If (filters.get(“account”) and filters.get(“categorize\_by”) equals “Categorize by Account”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“account”) → filters.get(“categorize\_by”) equals “Categorize by Account”.
  - Set filters.account from Platform.parse\_json(filters.get(“account”)).
  - For each account in filters.account.
    - If account\_details at account.is\_group equals 0.
      - Call the validation error handler Platform.throw(translated “Can not filter based on Child Account, if grouped by Account”).
- If (filters.get(“voucher\_no”) and filters.get(“categorize\_by”) belongs to list(“Categorize by Voucher”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“voucher\_no”) → filters.get(“categorize\_by”) belongs to list(“Categorize by Voucher”).
  - Call the validation error handler Platform.throw(translated “Can not filter based on Voucher No, if grouped by Voucher”).
- Evaluate validate\_date\_range(filters).
- If filters.get(“project”).
  - Set filters.project from Platform.parse\_json(filters.get(“project”)).
- If filters.get(“cost\_center”).
  - Set filters.cost\_center from Platform.parse\_json(filters.get(“cost\_center”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L982)

<a id="op-52dfe4b3738681"></a>
### Validate party

`operation_enterprise_accounts_report_general_ledger_business_behavior_validate_party`

**Inputs** filters.

**Record and data access** read party\_type via exists.

**Explicit failure paths** validation helper — translated “Invalid {0}: {1}”.format(party\_type, d).

**Local steps**

- Set tuple(party\_type, party) from tuple(filters.get(“party\_type”), filters.get(“party”)).
- If (party and party\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party → party\_type.
  - For each d in party.
    - If not Platform.db.exists(party\_type, d).
      - Call the validation error handler Platform.throw(translated “Invalid {0}: {1}”.format(party\_type, d)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L1228) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L983)

<a id="op-3bb38e6a402666"></a>
### Set account currency

`operation_enterprise_accounts_report_general_ledger_business_behavior_set_account_currency`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value · read “GL Entry” via get\_value · read filters.party\_type via get\_cached\_value.

**Explicit results** filters.

**Local steps**

- If (filters.get(“account”) or (filters.get(“party”) and len(filters.party) equals 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“account”) → (filters.get(“party”) and len(filters.party) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“party”) → len(filters.party) equals 1.
  - Set filters at “company\_currency” from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
  - Set account\_currency from no value.
  - If filters.get(“account”).
    - If len(filters.get(“account”)) equals 1.
      - Set account\_currency from get\_account\_currency(filters.account at 0).
    - Otherwise.
      - Set currency from get\_account\_currency(filters.account at 0).
      - Set is\_same\_account\_currency from true.
      - For each account in filters.get(“account”).
        - If get\_account\_currency(account) differs from currency.
          - Set is\_same\_account\_currency from false.
          - Leave the innermost loop without its normal-exhaustion alternative.
      - If is\_same\_account\_currency.
        - Set account\_currency from currency.
  - Otherwise.
    - If (filters.get(“party”) and filters.get(“party\_type”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“party”) → filters.get(“party\_type”).
      - Set gle\_currency from Platform.db.get\_value(“GL Entry”, mapping(“party\_type” → filters.party\_type, “party” → filters.party at 0, “company” → filters.company), “account\_currency”).
      - If gle\_currency.
        - Set account\_currency from gle\_currency.
      - Otherwise.
        - Set account\_currency from no value when filters.party\_type belongs to list(“Employee”, “Shareholder”, “Member”), otherwise Platform.get\_cached\_value(filters.party\_type, filters.party at 0, “default\_currency”).
          - Value choice on filters.party\_type belongs to list(“Employee”, “Shareholder”, “Member”) — true gives no value, false gives Platform.get\_cached\_value(filters.party\_type, filters.party at 0, “default\_currency”).
  - Set filters at “account\_currency” from (account\_currency or filters.company\_currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_currency → filters.company\_currency.
  - If (filters.account\_currency differs from filters.company\_currency and not filters.presentation\_currency and not filters.get(“show\_amount\_in\_company\_currency”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.account\_currency differs from filters.company\_currency → not filters.presentation\_currency → not filters.get(“show\_amount\_in\_company\_currency”).
    - Set filters.presentation\_currency from filters.account\_currency.
- Return filters.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”), Platform.get\_cached\_value(filters.party\_type, filters.party at 0, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L980)

<a id="op-924f43ef51724f"></a>
### Get result

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_result`

**Inputs** filters, account\_details.

**Explicit results** result.

**Local steps**

- Set accounting\_dimensions from list().
- If filters.get(“include\_dimensions”).
  - Set accounting\_dimensions from get\_accounting\_dimensions().
- Set gl\_entries from get\_gl\_entries(filters, accounting\_dimensions).
- Set data from get\_data\_with\_opening\_closing(filters, account\_details, accounting\_dimensions, gl\_entries).
- Set result from get\_result\_as\_list(data, filters).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L2370) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L972)

<a id="op-b0bf1aee2b13e3"></a>
### Get gl entries

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_general_ledger_entries`

**Inputs** filters, accounting\_dimensions.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Company” via get\_cached\_value.

**State and service calls** execute a supplied database query.

**Explicit results** convert\_gl\_entries\_currency(gl\_entries, currency\_map, filters).

**Local steps**

- Set currency\_map from get\_currency(filters).
- Set select\_fields from “, debit, credit, debit\_in\_account\_currency,\\n\\t\\tcredit\_in\_account\_currency ”.
- If filters.get(“show\_remarks”).
  - If remarks\_length bound to Platform.get\_single\_value(“Accounts Settings”, “general\_ledger\_remarks\_length”).
    - Update select\_fields using + formatted text ,substr(remarks, 1, {remarks\_length}) as 'remarks'.
  - Otherwise.
    - Update select\_fields using + “,remarks”.
- Set order\_by\_statement from “order by posting\_date, account, creation”.
- If filters.get(“include\_dimensions”).
  - Set order\_by\_statement from “order by posting\_date, creation”.
- If filters.get(“categorize\_by”) equals “Categorize by Voucher”.
  - Set order\_by\_statement from “order by posting\_date, voucher\_type, voucher\_no”.
- If filters.get(“categorize\_by”) equals “Categorize by Account”.
  - Set order\_by\_statement from “order by account, posting\_date, creation”.
- If filters.get(“include\_default\_book\_entries”).
  - Set filters at “company\_fb” from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_finance\_book”).
- Set dimension\_fields from empty text.
- If accounting\_dimensions.
  - Set dimension\_fields from (“, ”.join(accounting\_dimensions) + “,”).
- Set transaction\_currency\_fields from empty text.
- If filters.get(“add\_values\_in\_transaction\_currency”).
  - Set transaction\_currency\_fields from “debit\_in\_transaction\_currency, credit\_in\_transaction\_currency, transaction\_currency,”.
- Set gl\_entries from Platform.db.sql(formatted text   select  name as gl\_entry, posting\_date, account, party\_type, party,  voucher\_type, voucher\_subtype, voucher\_no, {dimension\_fields}  cost\_cent, filters, as\_dict = 1).
- Set party\_name\_map from get\_party\_name\_map().
- For each gl\_entry in gl\_entries.
  - If (gl\_entry.party\_type and gl\_entry.party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_entry.party\_type → gl\_entry.party.
    - Set gl\_entry.party\_name from party\_name\_map.get(gl\_entry.party\_type, mapping()).get(gl\_entry.party).
- Return convert\_gl\_entries\_currency(gl\_entries, currency\_map, filters).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “general\_ledger\_remarks\_length”), Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L969)

<a id="op-8c9b003190bcde"></a>
### Convert gl entries currency

`operation_enterprise_binding_enterprise_accounts_report_general_ledger_general_ledger_convert_gl_entries_currency`

**Inputs** gl\_entries, currency\_map, filters.

**Explicit results** gl\_entries · convert\_to\_presentation\_currency(gl\_entries, currency\_map, filters, use\_account\_currency = not filters.get(“convert\_at\_reporting\_date\_rate”)).

**Local steps**

- If not filters.get(“presentation\_currency”).
  - Return gl\_entries.
- Return convert\_to\_presentation\_currency(gl\_entries, currency\_map, filters, use\_account\_currency = not filters.get(“convert\_at\_reporting\_date\_rate”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1211)

<a id="op-49479d0456e321"></a>
### Get conditions

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_conditions`

**Inputs** filters.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Journal Entry” via get\_all · read “DocType” via get\_cached\_value.

**Explicit results** “and {}”.format(“ and ”.join(conditions)) when conditions, otherwise empty text.

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Entries'”.

**Local steps**

- Set conditions from list().
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- If filters.get(“account”).
  - Set filters.account from get\_accounts\_with\_children(filters.account).
  - If filters.account.
    - Evaluate conditions.append(“account in %(account)s”).
- If filters.get(“cost\_center”).
  - Set filters.cost\_center from get\_cost\_centers\_with\_children(filters.cost\_center).
  - Evaluate conditions.append(“cost\_center in %(cost\_center)s”).
- If filters.get(“voucher\_no”).
  - Evaluate conditions.append(“voucher\_no=%(voucher\_no)s”).
- If filters.get(“against\_voucher\_no”).
  - Evaluate conditions.append(“against\_voucher=%(against\_voucher\_no)s”).
- If filters.get(“ignore\_err”).
  - Set err\_journals from Platform.db.get\_all(“Journal Entry”, filters = mapping(“company” → filters.get(“company”), “docstatus” → 1, “voucher\_type” → tuple(“in”, list(“Exchange Rate Revaluation”, “Exchange Gain Or Loss”))), as\_list = true).
  - If err\_journals.
    - Evaluate filters.update(mapping(“voucher\_no\_not\_in” → list of x at 0 for x drawn from err\_journals)).
      - Draw x from err\_journals.
- If filters.get(“ignore\_cr\_dr\_notes”).
  - Set system\_generated\_cr\_dr\_journals from Platform.db.get\_all(“Journal Entry”, filters = mapping(“company” → filters.get(“company”), “docstatus” → 1, “voucher\_type” → tuple(“in”, list(“Credit Note”, “Debit Note”)), “is\_system\_generated” → 1), as\_l ….
  - If system\_generated\_cr\_dr\_journals.
    - Set vouchers\_to\_ignore from ((filters.get(“voucher\_no\_not\_in”) or list()) + list of x at 0 for x drawn from system\_generated\_cr\_dr\_journals).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“voucher\_no\_not\_in”) → list().
      - Draw x from system\_generated\_cr\_dr\_journals.
    - Evaluate filters.update(mapping(“voucher\_no\_not\_in” → vouchers\_to\_ignore)).
- If filters.get(“voucher\_no\_not\_in”).
  - Evaluate conditions.append(“voucher\_no not in %(voucher\_no\_not\_in)s”).
- If (filters.get(“categorize\_by”) equals “Categorize by Party” and not filters.get(“party\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“categorize\_by”) equals “Categorize by Party” → not filters.get(“party\_type”).
  - Evaluate conditions.append(“party\_type in ('Customer', 'Supplier')”).
- If filters.get(“party\_type”).
  - Evaluate conditions.append(“party\_type=%(party\_type)s”).
- If filters.get(“party”).
  - Evaluate conditions.append(“party in %(party)s”).
- If filters.get(“disable\_opening\_balance\_calculation”).
  - If not ignore\_is\_opening.
    - Evaluate conditions.append(“(posting\_date &gt;=%(from\_date)s or is\_opening = 'Yes')”).
  - Otherwise.
    - Evaluate conditions.append(“posting\_date &gt;=%(from\_date)s”).
- Otherwise.
  - If not (filters.get(“account”) or filters.get(“party”) or filters.get(“categorize\_by”) belongs to list(“Categorize by Account”, “Categorize by Party”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“account”) → filters.get(“party”) → filters.get(“categorize\_by”) belongs to list(“Categorize by Account”, “Categorize by Party”).
    - If not ignore\_is\_opening.
      - Evaluate conditions.append(“(posting\_date &gt;=%(from\_date)s or is\_opening = 'Yes')”).
    - Otherwise.
      - Evaluate conditions.append(“posting\_date &gt;=%(from\_date)s”).
- If not ignore\_is\_opening.
  - Evaluate conditions.append(“(posting\_date &lt;=%(to\_date)s or is\_opening = 'Yes')”).
- Otherwise.
  - Evaluate conditions.append(“posting\_date &lt;=%(to\_date)s”).
- If filters.get(“project”).
  - Evaluate conditions.append(“project in %(project)s”).
- If filters.get(“include\_default\_book\_entries”).
  - If filters.get(“finance\_book”).
    - If (filters.get(“company\_fb”) and cstr(filters.get(“finance\_book”)) differs from cstr(filters.get(“company\_fb”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“company\_fb”) → cstr(filters.get(“finance\_book”)) differs from cstr(filters.get(“company\_fb”)).
      - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Entries'”).
    - Otherwise.
      - Evaluate conditions.append(“(finance\_book in (%(finance\_book)s, '') OR finance\_book IS NULL)”).
  - Otherwise.
    - Evaluate conditions.append(“(finance\_book in (%(company\_fb)s, '') OR finance\_book IS NULL)”).
- Otherwise.
  - If filters.get(“finance\_book”).
    - Evaluate conditions.append(“(finance\_book in (%(finance\_book)s, '') OR finance\_book IS NULL)”).
  - Otherwise.
    - Evaluate conditions.append(“(finance\_book in ('') OR finance\_book IS NULL)”).
- If not filters.get(“show\_cancelled\_entries”).
  - Evaluate conditions.append(“is\_cancelled = 0”).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(“GL Entry”).
  - Evaluate conditions.append(formatted text ({match\_conditions})).
- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- If accounting\_dimensions.
  - For each dimension in accounting\_dimensions.
    - If (not dimension.disabled and dimension.document\_type differs from “Finance Book”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not dimension.disabled → dimension.document\_type differs from “Finance Book”.
      - If filters.get(dimension.fieldname).
        - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
          - Set filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, filters.get(dimension.fieldname)).
          - Evaluate conditions.append(formatted text {dimension.fieldname} in %({dimension.fieldname})s).
        - Otherwise.
          - Evaluate conditions.append(formatted text {dimension.fieldname} in %({dimension.fieldname})s).
- Return “and {}”.format(“ and ”.join(conditions)) when conditions, otherwise empty text.
  - Value choice on conditions — true gives “and {}”.format(“ and ”.join(conditions)), false gives empty text.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”), Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L3480) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L966)

<a id="op-66c3e723b07685"></a>
### Get party name map

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_party_name_map`

**Inputs** no declared parameters.

**Record and data access** read “Customer” via get\_all · read “Supplier” via get\_all · read “Employee” via get\_all.

**Explicit results** party\_map.

**Local steps**

- Set party\_map from mapping().
- Set customers from Platform.get\_all(“Customer”, fields = list(“name”, “customer\_name”)).
- Set party\_map at “Customer” from mapping of c.name → c.customer\_name for c drawn from customers.
  - Draw c from customers.
- Set suppliers from Platform.get\_all(“Supplier”, fields = list(“name”, “supplier\_name”)).
- Set party\_map at “Supplier” from mapping of s.name → s.supplier\_name for s drawn from suppliers.
  - Draw s from suppliers.
- Set employees from Platform.get\_all(“Employee”, fields = list(“name”, “employee\_name”)).
- Set party\_map at “Employee” from mapping of e.name → e.employee\_name for e drawn from employees.
  - Draw e from employees.
- Return party\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L5907) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L971)

<a id="op-392c6b3b69b724"></a>
### Get accounts with children

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_accounts_with_children`

**Inputs** accounts.

**Explicit results** no value · nested operand in the contract(nested operand in the contract).select(doctype.name).where(Criterion.any(conditions)).run(pluck = true).

**Local steps**

- If not isinstance(accounts, list).
  - Set accounts from list of d.strip() for d drawn from accounts.strip().split(“,”) where d.
    - Draw d from accounts.strip().split(“,”), keep a combination only if (d).
- If not accounts.
  - Return no value.
- Set doctype from Platform.qb.DocType(“Account”).
- Set accounts\_data from nested operand in the contract(nested operand in the contract).select(doctype.lft, doctype.rgt).where(doctype.name.isin(accounts)).run(as\_dict = true).
- Set conditions from list().
- For each account in accounts\_data.
  - Evaluate conditions.append((doctype.lft ≥ account.lft bitwise and doctype.rgt ≤ account.rgt)).
- Return nested operand in the contract(nested operand in the contract).select(doctype.name).where(Criterion.any(conditions)).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L6314) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L961)

<a id="op-5174ef1a37d8d9"></a>
### Set bill no

`operation_enterprise_accounts_report_general_ledger_business_behavior_set_bill_number`

**Inputs** gl\_entries.

**Local steps**

- Set inv\_details from get\_supplier\_invoice\_details().
- For each gl in gl\_entries.
  - Set gl at “bill\_no” from inv\_details.get(gl.get(“against\_voucher”), empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L6836) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L981)

<a id="op-7dac4e7fe3bdb5"></a>
### Get translated labels for totals

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_translated_labels_for_totals`

**Inputs** no declared parameters.

**Explicit results** mapping(“opening” → wrap\_in\_quotes(translated “Opening”), “total” → wrap\_in\_quotes(translated “Total”), “closing” → wrap\_in\_quotes(translated “Closing (Opening + Total)”)).

**Local steps**

- Bind local operation wrap\_in\_quotes for subsequent calls.
- Return mapping(“opening” → wrap\_in\_quotes(translated “Opening”), “total” → wrap\_in\_quotes(translated “Total”), “closing” → wrap\_in\_quotes(translated “Closing (Opening + Total)”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L6971) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L977)

<a id="op-ab6237b5768134"></a>
### Get translated labels for totals.wrap in quotes

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_translated_labels_for_totals_wrap_in_quotes`

**Inputs** label.

**Explicit results** formatted text '{label}'.

**Local steps**

- Return formatted text '{label}'.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0250.json#L7164) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L978)

<a id="op-262beb3ae9d712"></a>
### Get data with opening closing

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_data_with_opening_closing`

**Inputs** filters, account\_details, accounting\_dimensions, gl\_entries.

**Explicit results** data.

**Local steps**

- Bind local operation add\_total\_to\_data for subsequent calls.
- Set labels from get\_translated\_labels\_for\_totals().
- Set data from list().
- Evaluate set\_bill\_no(gl\_entries).
- Set gle\_map from initialize\_gle\_map(gl\_entries, filters).
- Set tuple(totals, entries) from get\_accountwise\_gle(filters, accounting\_dimensions, gl\_entries, gle\_map).
- Evaluate add\_total\_to\_data(totals, “opening”).
- If not filters.get(“categorize\_by”).
  - Set all\_entries from list().
  - For each acc\_dict in gle\_map.values().
    - Evaluate all\_entries.extend(acc\_dict.entries).
  - Update data using + all\_entries.
- Otherwise.
  - If filters.get(“categorize\_by”) differs from “Categorize by Voucher (Consolidated)”.
    - Set set\_opening\_closing from ((not filters.get(“categorize\_by”) and not filters.get(“voucher\_no”)) or (filters.get(“categorize\_by”) and filters.get(“categorize\_by”) differs from “Categorize by Voucher”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not filters.get(“categorize\_by”) and not filters.get(“voucher\_no”)) → (filters.get(“categorize\_by”) and filters.get(“categorize\_by”) differs from “Categorize by Voucher”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.get(“categorize\_by”) → not filters.get(“voucher\_no”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“categorize\_by”) → filters.get(“categorize\_by”) differs from “Categorize by Voucher”.
    - Set set\_total from (filters.get(“categorize\_by”) or not filters.voucher\_no).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“categorize\_by”) → not filters.voucher\_no.
    - For each acc\_dict in gle\_map.values().
      - If not acc\_dict.entries.
        - Continue with the next iteration or loop test.
      - Evaluate data.append(mapping(“debit\_in\_transaction\_currency” → no value, “credit\_in\_transaction\_currency” → no value)).
      - If set\_opening\_closing.
        - Evaluate add\_total\_to\_data(acc\_dict.totals, “opening”).
      - Update data using + acc\_dict.entries.
      - If set\_total.
        - Evaluate add\_total\_to\_data(acc\_dict.totals, “total”).
      - If set\_opening\_closing.
        - Evaluate add\_total\_to\_data(acc\_dict.totals, “closing”).
    - Evaluate data.append(mapping(“debit\_in\_transaction\_currency” → no value, “credit\_in\_transaction\_currency” → no value)).
  - Otherwise.
    - Update data using + entries.
- Evaluate add\_total\_to\_data(totals, “total”).
- Evaluate add\_total\_to\_data(totals, “closing”).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L967)

<a id="op-bb54d972320af3"></a>
### Get data with opening closing.add total to data

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_data_with_opening_closing_add_total_to_data`

**Inputs** totals, key.

**Local steps**

- Set row from totals at key.
- Set row at “account” from labels at key.
- Evaluate data.append(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L1028) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L968)

<a id="op-f853a2ca4b3e81"></a>
### Get totals dict

`operation_enterprise_accounts_report_general_ledger_business_behavior_get_totals_mapping`

**Inputs** no declared parameters.

**Explicit results** \_dict(opening = \_dict(DEBIT\_CREDIT\_DICT), total = \_dict(DEBIT\_CREDIT\_DICT), closing = \_dict(DEBIT\_CREDIT\_DICT)).

**Local steps**

- Return \_dict(opening = \_dict(DEBIT\_CREDIT\_DICT), total = \_dict(DEBIT\_CREDIT\_DICT), closing = \_dict(DEBIT\_CREDIT\_DICT)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0251.json#L1141) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L976)

<a id="op-6ea373b30ed4ca"></a>
### Get group by fields

`operation_enterprise_binding_enterprise_accounts_report_general_ledger_general_ledger_get_group_by_fields`

**Inputs** group\_by.

**Declared result** tuple at tuple(str, ellipsis).

**Explicit results** tuple(“party\_type”, “party”) · tuple(“account”) · tuple(“voucher\_type”, “voucher\_no”).

**Local steps**

- If group\_by equals “Categorize by Party”.
  - Return tuple(“party\_type”, “party”).
- Otherwise.
  - If group\_by belongs to list(“Categorize by Voucher (Consolidated)”, “Categorize by Account”).
    - Return tuple(“account”).
  - Otherwise.
    - Return tuple(“voucher\_type”, “voucher\_no”).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1212)

<a id="op-0d3958a779edff"></a>
### Get group by value

`operation_enterprise_binding_enterprise_accounts_report_general_ledger_general_ledger_get_group_by_value`

**Inputs** gle, group\_by\_fields.

**Declared result** tuple.

**Explicit results** tuple(generator of gle.get(field) for field drawn from group\_by\_fields).

**Local steps**

- Return tuple(generator of gle.get(field) for field drawn from group\_by\_fields).
  - Draw field from group\_by\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1213)

<a id="op-a5924376bc6832"></a>
### Initialize gle map

`operation_enterprise_accounts_report_general_ledger_business_behavior_initialize_general_ledger_entry_map`

**Inputs** gl\_entries, filters.

**Explicit results** gle\_map.

**Local steps**

- Set gle\_map from mapping().
- Set group\_by from get\_group\_by\_fields(filters.get(“categorize\_by”)).
- For each gle in gl\_entries.
  - Set group\_by\_value from get\_group\_by\_value(gle, group\_by).
  - If group\_by\_value does not belong to gle\_map.
    - Set gle\_map at group\_by\_value from \_dict(totals = get\_totals\_dict(), entries = list()).
- Return gle\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L979)
