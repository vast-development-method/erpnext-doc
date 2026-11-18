# Accounting and settlement · operations 121

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-e3a46a83321b11"></a>
### Get companies

`operation_enterprise_accounts_utils_business_behavior_get_companies`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_list.

**Explicit results** list of d.name for d drawn from Platform.get\_list(“Company”, fields = list(“name”), order\_by = “name”).

**Local steps**

- Return list of d.name for d drawn from Platform.get\_list(“Company”, fields = list(“name”), order\_by = “name”).
  - Draw d from Platform.get\_list(“Company”, fields = list(“name”), order\_by = “name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L7073) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L210)

<a id="op-c786c5a2f74ce3"></a>
### Get children

`operation_enterprise_accounts_utils_business_behavior_get_children`

**Inputs** doctype, parent, company, is\_root = false, include\_disabled = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** acc.

**Local steps**

- If isinstance(include\_disabled, str).
  - Set include\_disabled from loads(include\_disabled).
- Bind dependencies sort\_accounts.
- Set parent\_fieldname from (“parent\_” + doctype.lower().replace(one space, “\_”)).
- Set fields from list(“name as value”, “is\_group as expandable”).
- Set filters from list(list(“docstatus”, “&lt;”, 2)).
- If Platform.db.has\_column(doctype, “disabled”).
  - If include\_disabled.
    - Evaluate fields.append(“disabled”).
  - Otherwise.
    - Evaluate filters.append(list(“disabled”, “=”, false)).
- Set node\_fields from mapping(“Account” → list(“root\_type”, “account\_name”, “account\_number”, “account\_currency”, …), “Cost Center” → list(“cost\_center\_name”, “cost\_center\_number”)).
- Update fields using + node\_fields.get(doctype, list()).
- If is\_root.
  - Evaluate filters.append(IfNull(Field(parent\_fieldname), empty text) equals empty text).
  - Evaluate filters.append(list(“company”, “=”, company)).
  - If doctype equals “Account”.
    - Evaluate fields.append(“report\_type”).
- Otherwise.
  - Evaluate filters.append(list(parent\_fieldname, “=”, parent)).
  - Evaluate fields.append((parent\_fieldname + “ as parent”)).
- Set acc from Platform.get\_list(doctype, fields = fields, filters = filters).
- If doctype equals “Account”.
  - Evaluate sort\_accounts(acc, is\_root, key = “value”).
- Return acc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L209)

<a id="op-e6108383f69553"></a>
### Get account balances

`operation_enterprise_accounts_utils_business_behavior_get_account_balances`

**Inputs** accounts, company, finance\_book = no value, include\_default\_fb\_balances = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** list() · accounts.

**Local steps**

- If isinstance(accounts, str).
  - Set accounts from loads(accounts).
- If not accounts.
  - Return list().
- Set company\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- For each account in accounts.
  - Set account at “company\_currency” from company\_currency.
  - Set account at “balance” from flt(get\_balance\_on(account = account at “value”, in\_account\_currency = false, company = company, finance\_book = finance\_book, …)).
  - If (account at “account\_currency” and account at “account\_currency” differs from company\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account at “account\_currency” → account at “account\_currency” differs from company\_currency.
    - Set account at “balance\_in\_account\_currency” from flt(get\_balance\_on(account = account at “value”, company = company, finance\_book = finance\_book, include\_default\_fb\_balances = include\_default\_fb\_balances)).
- Return accounts.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L201)

<a id="op-68f4c03e3d10b1"></a>
### Get account balances coa

`operation_enterprise_accounts_utils_business_behavior_get_account_balances_chart_of_accounts`

**Inputs** company, include\_default\_fb\_balances = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_list.

**Explicit results** accounts\_data.

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set account\_list from Platform.get\_list(“Account”, fields = list(“name”, “parent\_account”, “account\_currency”), filters = mapping(“company” → company), order\_by = “lft”).
- Set account\_balances\_cc from mapping of account.get(“name”) → 0 for account drawn from account\_list.
  - Draw account from account\_list.
- Set account\_balances\_ac from mapping of account.get(“name”) → 0 for account drawn from account\_list.
  - Draw account from account\_list.
- Set GLEntry from DocType(“GL Entry”).
- Set precision from get\_currency\_precision().
- Set get\_ledger\_balances\_query from Platform.get\_query(GLEntry, fields = list(nested operand in the contract.account), ignore\_permissions = false).select((nested operand in the contract(nested operand in the contract) − nested operand in the ….
- Set conditions from list(GLEntry.company equals company, GLEntry.is\_cancelled equals 0).
- Set default\_finance\_book from no value.
- If include\_default\_fb\_balances.
  - Set default\_finance\_book from Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).
- Set finance\_books from list(empty text).
- If default\_finance\_book.
  - Evaluate finance\_books.append(default\_finance\_book).
- Evaluate conditions.append((GLEntry.finance\_book.isnull() bitwise or GLEntry.finance\_book.isin(finance\_books))).
- Set get\_ledger\_balances\_query from get\_ledger\_balances\_query.where(Criterion.all(conditions)).
- Set ledger\_balances from get\_ledger\_balances\_query.run(as\_dict = true).
- For each ledger\_entry in ledger\_balances.
  - Set account\_balances\_cc at ledger\_entry.get(“account”) from ledger\_entry.get(“balance”).
  - Set account\_balances\_ac at ledger\_entry.get(“account”) from ledger\_entry.get(“balance\_in\_account\_currency”).
- For each account in reversed(account\_list).
  - Set parent from account.get(“parent\_account”).
  - If parent.
    - Update account\_balances\_cc at parent using + account\_balances\_cc.get(account.get(“name”)).
- Set accounts\_data from list of mapping(“value” → account.get(“name”), “company\_currency” → company\_currency, “balance” → account\_balances\_cc.get(account.get(“name”)), “account\_currency” → account.get(“account\_currency”), …) for  ….
  - Draw account from account\_list.
- Return accounts\_data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”), Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L202)

<a id="op-800a8a822225aa"></a>
### Create payment gateway account

`operation_enterprise_accounts_utils_business_behavior_create_payment_gateway_account`

**Inputs** gateway, payment\_channel = “Email”, company = no value.

**Record and data access** read “Global Defaults” via get\_cached\_value · read “Account” via get\_value · read “Payment Gateway Account” via exists · resolve a document from mapping(“doctype” → “Payment Gateway Account”, “is\_default” → 1, “payment\_gateway” → gateway, “payment\_account” → bank\_account.name, …) via get\_doc.

**State and service calls** msgprint with translated “Payment Gateway Account not created, please create one manually.” · call insert on Platform.get\_doc(mapping(“doctype” → “Payment Gateway Account”, “is\_default” → 1, “payment\_gateway” → gateway, “payment\_account” → bank\_account.name, …)).

**Explicit results** no value.

**Local steps**

- Bind dependencies create\_bank\_account.
- If not company.
  - Set company from Platform.get\_cached\_value(“Global Defaults”, “Global Defaults”, “default\_company”).
  - If not company.
    - Return no value.
- Set bank\_account from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated gateway, “company” → company), list(“name”, “account\_currency”), as\_dict = 1).
- If not bank\_account.
  - Set bank\_account from Platform.db.get\_value(“Account”, mapping(“account\_name” → gateway, “company” → company), list(“name”, “account\_currency”), as\_dict = 1).
- If not bank\_account.
  - Set bank\_account from create\_bank\_account(mapping(“company\_name” → company, “bank\_account” → translated gateway)).
- If not bank\_account.
  - Evaluate Platform.msgprint(translated “Payment Gateway Account not created, please create one manually.”).
  - Return no value.
- If Platform.db.exists(“Payment Gateway Account”, mapping(“payment\_gateway” → gateway, “currency” → bank\_account.account\_currency)).
  - Return no value.
- Attempt the following.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Payment Gateway Account”, “is\_default” → 1, “payment\_gateway” → gateway, “payment\_account” → bank\_account.name, …)).insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
- On failure (Platform.DuplicateEntryError).
  - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Global Defaults”, “Global Defaults”, “default\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L2864) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L192)

<a id="op-6df9f83dcd9b70"></a>
### Update cost center

`operation_enterprise_accounts_utils_business_behavior_update_cost_center`

**Inputs** docname, cost\_center\_name, cost\_center\_number, company, merge.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Cost Center” · request rename\_doc for “Cost Center”.

**Explicit results** new\_name.

**Local steps**

- Evaluate Platform.has\_permission(“Cost Center”, “write”, doc = docname, throw = true).
- Evaluate validate\_field\_number(“Cost Center”, docname, cost\_center\_number, company, …).
- If cost\_center\_number.
  - Evaluate Platform.db.set\_value(“Cost Center”, docname, “cost\_center\_number”, cost\_center\_number.strip()).
- Otherwise.
  - Evaluate Platform.db.set\_value(“Cost Center”, docname, “cost\_center\_number”, empty text).
- Evaluate Platform.db.set\_value(“Cost Center”, docname, “cost\_center\_name”, cost\_center\_name.strip()).
- Set new\_name from get\_autoname\_with\_number(cost\_center\_number, cost\_center\_name, company).
- If docname differs from new\_name.
  - Evaluate Platform.rename\_doc(“Cost Center”, docname, new\_name, force = 1, merge = merge).
  - Return new\_name.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Cost Center”, “write”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L250)

<a id="op-a1aa3504ed0b91"></a>
### Validate field number

`operation_enterprise_accounts_utils_business_behavior_validate_field_number`

**Inputs** doctype\_name, docname, number\_value, company, field\_name.

**Record and data access** read doctype\_name via get\_value.

**Explicit failure paths** validation helper — translated “{0} Number {1} is already used in {2} {3}”.format(doctype\_name, number\_value, doctype\_name.lower(), doctype\_with\_same\_number).

**Local steps**

- If number\_value.
  - Set filters from mapping(field\_name → number\_value, “name” → list(“!=”, docname)).
  - If company.
    - Set filters at “company” from company.
  - Set doctype\_with\_same\_number from Platform.db.get\_value(doctype\_name, filters).
  - If doctype\_with\_same\_number.
    - Call the validation error handler Platform.throw(translated “{0} Number {1} is already used in {2} {3}”.format(doctype\_name, number\_value, doctype\_name.lower(), doctype\_with\_same\_number)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L4188) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L257)

<a id="op-cb262ebdf7d6d3"></a>
### Get autoname with number

`operation_enterprise_accounts_utils_business_behavior_get_autoname_with_number`

**Inputs** number\_value, doc\_title, company.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** call insert on parts.

**Explicit results** “ - ”.join(parts).

**Explicit failure paths** validation helper — translated “Company {0} does not exist or has no abbreviation”.format(company).

**Local steps**

- Set company\_abbr from Platform.get\_cached\_value(“Company”, company, “abbr”).
- If not company\_abbr.
  - Call the validation error handler Platform.throw(translated “Company {0} does not exist or has no abbreviation”.format(company)).
- Set parts from list(doc\_title.strip(), company\_abbr).
- If cstr(number\_value).strip().
  - Evaluate parts.insert(0, cstr(number\_value).strip()).
- Return “ - ”.join(parts).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “abbr”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L206)

<a id="op-43286e8700d9d2"></a>
### Parse naming series variable

`operation_enterprise_accounts_utils_business_behavior_parse_naming_series_variable`

**Inputs** doc, variable.

**Record and data access** read “Company” via get\_value · resolve a document from doc.reference\_doctype via get\_doc · read “Global Defaults” via get\_single\_value.

**Explicit results** get\_fiscal\_year(date = date, company = company, truncate = variable equals “TFY”) at 0 · Platform.db.get\_value(“Company”, company, “abbr”) when company, otherwise empty text · date.strftime(data at variable) when variable belongs to data, otherwise determine\_consecutive\_week\_number(date).

**Local steps**

- If variable belongs to list(“FY”, “TFY”).
  - If doc.
    - Set date from (doc.get(“posting\_date”) or doc.get(“transaction\_date”) or getdate()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“posting\_date”) → doc.get(“transaction\_date”) → getdate().
    - Set company from doc.get(“company”).
  - Otherwise.
    - Set date from getdate().
    - Set company from no value.
  - Return get\_fiscal\_year(date = date, company = company, truncate = variable equals “TFY”) at 0.
- Otherwise.
  - If variable equals “ABBR”.
    - If doc.
      - Set company from (doc.get(“company”) or Platform.db.get\_default(“company”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“company”) → Platform.db.get\_default(“company”).
    - Otherwise.
      - Set company from Platform.db.get\_default(“company”).
    - Return Platform.db.get\_value(“Company”, company, “abbr”) when company, otherwise empty text.
      - Value choice on company — true gives Platform.db.get\_value(“Company”, company, “abbr”), false gives empty text.
  - Otherwise.
    - Set data from mapping(“YY” → “%y”, “YYYY” → “%Y”, “MM” → “%m”, “DD” → “%d”, …).
    - If (doc and doc.doctype belongs to list(“Batch”, “Serial No”) and doc.reference\_doctype and doc.reference\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.doctype belongs to list(“Batch”, “Serial No”) → doc.reference\_doctype → doc.reference\_name.
      - Set doc from Platform.get\_doc(doc.reference\_doctype, doc.reference\_name).
    - Set date from (getdate((doc.get(“posting\_date”) or doc.get(“transaction\_date”) or doc.get(“posting\_datetime”))) or now\_datetime()) when (doc and Platform.get\_single\_value(“Global Defaults”, “use\_posting\_datetime\_for\_nam ….
      - Value choice on (doc and Platform.get\_single\_value(“Global Defaults”, “use\_posting\_datetime\_for\_naming\_documents”)) — true gives (getdate((doc.get(“posting\_date”) or doc.get(“transaction\_date”) or doc.get(“posting\_datetime”))) or now\_datetime()), false gives now\_datetime().
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → Platform.get\_single\_value(“Global Defaults”, “use\_posting\_datetime\_for\_naming\_documents”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate((doc.get(“posting\_date”) or doc.get(“transaction\_date”) or doc.get(“posting\_datetime”))) → now\_datetime().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“posting\_date”) → doc.get(“transaction\_date”) → doc.get(“posting\_datetime”).
    - Return date.strftime(data at variable) when variable belongs to data, otherwise determine\_consecutive\_week\_number(date).
      - Value choice on variable belongs to data — true gives date.strftime(data at variable), false gives determine\_consecutive\_week\_number(date).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Global Defaults”, “use\_posting\_datetime\_for\_naming\_documents”) · clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L4700) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L234)

<a id="op-b74a66dba36b30"></a>
### Get coa

`operation_enterprise_accounts_utils_business_behavior_get_chart_of_accounts`

**Inputs** doctype, parent, is\_root = no value, chart = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** accounts.

**Local steps**

- Bind dependencies build\_tree\_from\_json.
- Set chart from chart when chart, otherwise Platform.flags.chart.
  - Value choice on chart — true gives chart, false gives Platform.flags.chart.
- Set Platform.flags.chart from chart.
- Set parent from no value when parent equals translated “All Accounts”, otherwise parent.
  - Value choice on parent equals translated “All Accounts” — true gives no value, false gives parent.
- Set accounts from build\_tree\_from\_json(chart).
- Set accounts from list of d for d drawn from accounts where d at “parent\_account” equals parent.
  - Draw d from accounts, keep a combination only if (d at “parent\_account” equals parent).
- Return accounts.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L208)

<a id="op-c3b91d7f55619d"></a>
### Update gl entries after

`operation_enterprise_accounts_utils_business_behavior_update_general_ledger_entries_after`

**Inputs** posting\_date, posting\_time, for\_warehouses = no value, for\_items = no value, warehouse\_account = no value, company = no value.

**Local steps**

- Set stock\_vouchers from get\_future\_stock\_vouchers(posting\_date, posting\_time, for\_warehouses, for\_items, …).
- Evaluate repost\_gle\_for\_stock\_vouchers(stock\_vouchers, posting\_date, company, warehouse\_account).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L5927) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L251)

<a id="op-68821eb45b1c47"></a>
### Repost gle for stock vouchers

`operation_enterprise_accounts_utils_business_behavior_repost_general_ledger_entry_for_stock_vouchers`

**Inputs** stock\_vouchers, posting\_date, company = no value, warehouse\_account = no value, repost\_doc = no value.

**State and service calls** commit · call db\_set on repost\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies toggle\_debit\_credit\_if\_negative.
- If not stock\_vouchers.
  - Return no value.
- If not warehouse\_account.
  - Set warehouse\_account from get\_warehouse\_account\_map(company).
- Set stock\_vouchers from sort\_stock\_vouchers\_by\_posting\_date(stock\_vouchers, company = company).
- If (repost\_doc and repost\_doc.gl\_reposting\_index).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in repost\_doc → repost\_doc.gl\_reposting\_index.
  - Set stock\_vouchers from stock\_vouchers at slice cint(repost\_doc.gl\_reposting\_index) to no value.
- Set precision from (get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit”)) → 2.
- For each stock\_vouchers\_chunk in create\_batch(stock\_vouchers, GL\_REPOSTING\_CHUNK).
  - Set gle from get\_voucherwise\_gl\_entries(stock\_vouchers\_chunk, posting\_date).
  - For each tuple(voucher\_type, voucher\_no) in stock\_vouchers\_chunk.
    - Set existing\_gle from gle.get(tuple(voucher\_type, voucher\_no), list()).
    - Set voucher\_obj from Platform.get\_lazy\_doc(voucher\_type, voucher\_no).
    - Set inventory\_account\_map from voucher\_obj.get\_inventory\_account\_map().
    - Set expected\_gle from toggle\_debit\_credit\_if\_negative(voucher\_obj.get\_gl\_entries(inventory\_account\_map)).
    - If expected\_gle.
      - If (not existing\_gle or not compare\_existing\_and\_expected\_gle(existing\_gle, expected\_gle, precision)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not existing\_gle → not compare\_existing\_and\_expected\_gle(existing\_gle, expected\_gle, precision).
        - Evaluate \_delete\_accounting\_ledger\_entries(voucher\_type, voucher\_no).
        - Evaluate voucher\_obj.make\_gl\_entries(gl\_entries = expected\_gle, from\_repost = true).
    - Otherwise.
      - Evaluate \_delete\_accounting\_ledger\_entries(voucher\_type, voucher\_no).
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
  - If repost\_doc.
    - Evaluate repost\_doc.db\_set(“gl\_reposting\_index”, (cint(repost\_doc.gl\_reposting\_index) + len(stock\_vouchers\_chunk))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L6081) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L244)

<a id="op-6878b8555d2c38"></a>
### Delete pl entries

`operation_enterprise_accounts_utils_business_behavior_delete_profit_and_loss_entries`

**Inputs** voucher\_type, voucher\_no.

**Local steps**

- Set ple from qb.DocType(“Payment Ledger Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((ple.voucher\_type equals voucher\_type bitwise and ple.voucher\_no equals voucher\_no)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L6969) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L198)

<a id="op-0d0583373146b6"></a>
### Delete adv pl entries

`operation_enterprise_accounts_utils_business_behavior_delete_adv_profit_and_loss_entries`

**Inputs** voucher\_type, voucher\_no.

**Local steps**

- Set adv from qb.DocType(“Advance Payment Ledger Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((adv.voucher\_type equals voucher\_type bitwise and adv.voucher\_no equals voucher\_no)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L7142) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L195)

<a id="op-a4ff1c4d70cab9"></a>
### Delete gl entries

`operation_enterprise_accounts_utils_business_behavior_delete_general_ledger_entries`

**Inputs** voucher\_type, voucher\_no.

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((gle.voucher\_type equals voucher\_type bitwise and gle.voucher\_no equals voucher\_no)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L7315) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L197)

<a id="op-b55caaa036d340"></a>
### Delete accounting ledger entries

`operation_enterprise_accounts_utils_business_behavior_delete_accounting_ledger_entries`

**Inputs** voucher\_type, voucher\_no.

**Local steps**

- Evaluate \_delete\_gl\_entries(voucher\_type, voucher\_no).
- Evaluate \_delete\_pl\_entries(voucher\_type, voucher\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0303.json#L7488) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L194)

<a id="op-5bb585d0533119"></a>
### Sort stock vouchers by posting date

`operation_enterprise_accounts_utils_business_behavior_sort_stock_vouchers_by_posting_date`

**Inputs** stock\_vouchers, company = no value.

**Declared result** list at tuple at tuple(str, str).

**Explicit results** sorted\_vouchers.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set voucher\_nos from list of v at 1 for v drawn from stock\_vouchers.
  - Draw v from stock\_vouchers.
- Set sles from nested operand in the contract(nested operand in the contract).groupby(sle.voucher\_type, sle.voucher\_no).orderby(sle.posting\_datetime).orderby(sle.creation).
- If company.
  - Set sles from sles.where(sle.company equals company).
- Set sles from sles.run(as\_dict = true).
- Set sorted\_vouchers from list of tuple(sle.voucher\_type, sle.voucher\_no) for sle drawn from sles.
  - Draw sle from sles.
- Set unknown\_vouchers from (set(stock\_vouchers) − set(sorted\_vouchers)).
- If unknown\_vouchers.
  - Evaluate sorted\_vouchers.extend(unknown\_vouchers).
- Return sorted\_vouchers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L246)

<a id="op-b2002ba1f87d94"></a>
### Get future stock vouchers

`operation_enterprise_accounts_utils_business_behavior_get_future_stock_vouchers`

**Inputs** posting\_date, posting\_time, for\_warehouses = no value, for\_items = no value, company = no value.

**Explicit results** list of tuple(d.voucher\_type, d.voucher\_no) for d drawn from future\_stock\_vouchers.

**Local steps**

- Set posting\_datetime from get\_combine\_datetime(posting\_date, posting\_time).
- Set SLE from DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).orderby(SLE.posting\_datetime).orderby(SLE.creation).for\_update().
- If for\_items.
  - Set query from query.where(SLE.item\_code.isin(for\_items)).
- If for\_warehouses.
  - Set query from query.where(SLE.warehouse.isin(for\_warehouses)).
- If company.
  - Set query from query.where(SLE.company equals company).
- Set future\_stock\_vouchers from query.run(as\_dict = true).
- Return list of tuple(d.voucher\_type, d.voucher\_no) for d drawn from future\_stock\_vouchers.
  - Draw d from future\_stock\_vouchers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L219)

<a id="op-7434200339bdbc"></a>
### Get voucherwise gl entries

`operation_enterprise_accounts_utils_business_behavior_get_voucherwise_general_ledger_entries`

**Inputs** future\_stock\_vouchers, posting\_date.

**Record and data access** read “GL Entry” via get\_all.

**Explicit results** gl\_entries.

**Local steps**

- Set gl\_entries from mapping().
- If not future\_stock\_vouchers.
  - Return gl\_entries.
- Set voucher\_nos from list of d at 1 for d drawn from future\_stock\_vouchers.
  - Draw d from future\_stock\_vouchers.
- Set gles from Platform.get\_all(“GL Entry”, filters = mapping(“is\_cancelled” → 0, “posting\_date” → list(“&gt;=”, posting\_date), “voucher\_no” → list(“in”, voucher\_nos)), fields = list(“name”, “account”, “credit”, “debit”, …) ….
- For each d in gles.
  - Evaluate gl\_entries.setdefault(tuple(d.voucher\_type, d.voucher\_no), list()).append(d).
- Return gl\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L231)

<a id="op-eb8b81380be1ca"></a>
### Compare existing and expected gle

`operation_enterprise_accounts_utils_business_behavior_compare_existing_and_expected_general_ledger_entry`

**Inputs** existing\_gle, expected\_gle, precision.

**Explicit results** false · matched.

**Local steps**

- If len(existing\_gle) differs from len(expected\_gle).
  - Return false.
- Set matched from true.
- For each entry in expected\_gle.
  - Set account\_existed from false.
  - For each e in existing\_gle.
    - If entry.account equals e.account.
      - Set account\_existed from true.
    - If (entry.account equals e.account and (not entry.cost\_center or not e.cost\_center or entry.cost\_center equals e.cost\_center) and (flt(entry.debit, precision) differs from flt(e.debit, precision) or flt(entry ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.account equals e.account → (not entry.cost\_center or not e.cost\_center or entry.cost\_center equals e.cost\_center) → (flt(entry.debit, precision) differs from flt(e.debit, precision) or flt(entry.credit, precision) differs from flt(e.credit, precision)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not entry.cost\_center → not e.cost\_center → entry.cost\_center equals e.cost\_center.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(entry.debit, precision) differs from flt(e.debit, precision) → flt(entry.credit, precision) differs from flt(e.credit, precision).
      - Set matched from false.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If not account\_existed.
    - Set matched from false.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return matched.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L1718) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L188)

<a id="op-1464b289bacae1"></a>
### Get stock accounts

`operation_enterprise_accounts_utils_business_behavior_get_stock_accounts`

**Inputs** company, voucher\_type = no value, voucher\_no = no value, accounts = no value.

**Record and data access** read “Account” via get\_all · read “Journal Entry Account” via get\_all · read “GL Entry” via get\_all.

**Explicit results** list(set(stock\_accounts)).

**Local steps**

- Set stock\_accounts from list of d.name for d drawn from Platform.db.get\_all(“Account”, mapping(“account\_type” → “Stock”, “company” → company, “is\_group” → 0)).
  - Draw d from Platform.db.get\_all(“Account”, mapping(“account\_type” → “Stock”, “company” → company, “is\_group” → 0)).
- If accounts.
  - Set stock\_accounts from list of row.account for row drawn from accounts where row.account belongs to stock\_accounts.
    - Draw row from accounts, keep a combination only if (row.account belongs to stock\_accounts).
- Otherwise.
  - If (voucher\_type and voucher\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type → voucher\_no.
    - If voucher\_type equals “Journal Entry”.
      - Set stock\_accounts from list of d.account for d drawn from Platform.db.get\_all(“Journal Entry Account”, mapping(“parent” → voucher\_no, “account” → list(“in”, stock\_accounts)), “account”).
        - Draw d from Platform.db.get\_all(“Journal Entry Account”, mapping(“parent” → voucher\_no, “account” → list(“in”, stock\_accounts)), “account”).
    - Otherwise.
      - Set stock\_accounts from list of d.account for d drawn from Platform.db.get\_all(“GL Entry”, mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no, “account” → list(“in”, stock\_accounts)), “account”).
        - Draw d from Platform.db.get\_all(“GL Entry”, mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no, “account” → list(“in”, stock\_accounts)), “account”).
- Return list(set(stock\_accounts)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L2172) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L229)

<a id="op-4008625fbdd2a0"></a>
### Get stock and account balance

`operation_enterprise_accounts_utils_business_behavior_get_stock_and_account_balance`

**Inputs** account = no value, posting\_date = no value, company = no value.

**Explicit results** tuple(flt(account\_balance, precision), flt(total\_stock\_value, precision), related\_warehouses).

**Local steps**

- If not posting\_date.
  - Set posting\_date from nowdate().
- Set account\_balance from get\_balance\_on(account, posting\_date, in\_account\_currency = false, ignore\_account\_permission = true).
- Set account\_table from Platform.qb.DocType(“Account”).
- Set query from nested operand in the contract.qb.from\_(account\_table).select(Count(account\_table.name)).where(((account\_table.account\_type equals “Stock” bitwise and account\_table.company equals company) bitwise and acco ….
- Set no\_of\_stock\_accounts from cint(query.run() at 0 at 0).
- Set related\_warehouses from list().
- If no\_of\_stock\_accounts &gt; 1.
  - Set warehouse\_account from get\_warehouse\_account\_map(company).
  - Set related\_warehouses from list of wh for tuple(wh, wh\_details) drawn from warehouse\_account.items() where (wh\_details.account equals account and not wh\_details.is\_group).
    - Draw tuple(wh, wh\_details) from warehouse\_account.items(), keep a combination only if ((wh\_details.account equals account and not wh\_details.is\_group)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in wh\_details.account equals account → not wh\_details.is\_group.
- Set total\_stock\_value from get\_stock\_value\_on(related\_warehouses, posting\_date, company = company).
- Set precision from Platform.get\_precision(“Journal Entry Account”, “debit\_in\_account\_currency”).
- Return tuple(flt(account\_balance, precision), flt(total\_stock\_value, precision), related\_warehouses).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L2738) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L230)

<a id="op-e569de31a0a5a2"></a>
### Get journal entry

`operation_enterprise_accounts_utils_business_behavior_get_journal_entry`

**Inputs** account, stock\_adjustment\_account, amount.

**Explicit results** mapping(“accounts” → list(mapping(“account” → account, db\_or\_cr\_warehouse\_account → abs(amount)), mapping(“account” → stock\_adjustment\_account, db\_or\_cr\_stock\_adjustment\_account → abs(amount)))).

**Local steps**

- Set db\_or\_cr\_warehouse\_account from “credit\_in\_account\_currency” when amount &lt; 0, otherwise “debit\_in\_account\_currency”.
  - Value choice on amount &lt; 0 — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
- Set db\_or\_cr\_stock\_adjustment\_account from “debit\_in\_account\_currency” when amount &lt; 0, otherwise “credit\_in\_account\_currency”.
  - Value choice on amount &lt; 0 — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
- Return mapping(“accounts” → list(mapping(“account” → account, db\_or\_cr\_warehouse\_account → abs(amount)), mapping(“account” → stock\_adjustment\_account, db\_or\_cr\_stock\_adjustment\_account → abs(amount)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L3406) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L221)

<a id="op-b6dcc418d91246"></a>
### Check and delete linked reports

`operation_enterprise_accounts_utils_business_behavior_check_and_delete_linked_reports`

**Inputs** report.

**Record and data access** read “Desktop Icon” via get\_all.

**State and service calls** request delete\_doc for “Desktop Icon”.

**Local steps**

- Set icons from Platform.get\_all(“Desktop Icon”, fields = list(“name”), filters = mapping(“\_report” → report)).
- If icons.
  - For each icon in icons.
    - Evaluate Platform.delete\_doc(“Desktop Icon”, icon).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L3655) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L186)
