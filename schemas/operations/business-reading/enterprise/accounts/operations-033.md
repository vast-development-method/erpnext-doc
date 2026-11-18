# Accounting and settlement · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Deferred revenue

<a id="op-9b2a8214131e10"></a>
### Get already booked amount

`operation_enterprise_accounts_deferred_revenue_business_behavior_get_already_booked_amount`

**Inputs** doc, item.

**Explicit results** get\_already\_booked\_amounts(doc, list(item)) at item.name.

**Local steps**

- Return get\_already\_booked\_amounts(doc, list(item)) at item.name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L26) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L20)

<a id="op-825081db01f5e5"></a>
### Get already booked amounts

`operation_enterprise_binding_enterprise_accounts_deferred_revenue_get_already_booked_amounts`

**Inputs** doc, items.

**Explicit results** mapping() · booked\_amounts.

**Local steps**

- If not items.
  - Return mapping().
- If doc.doctype equals “Sales Invoice”.
  - Set tuple(total\_credit\_debit, total\_credit\_debit\_currency) from tuple(“debit”, “debit\_in\_account\_currency”).
  - Set deferred\_account from “deferred\_revenue\_account”.
- Otherwise.
  - Set tuple(total\_credit\_debit, total\_credit\_debit\_currency) from tuple(“credit”, “credit\_in\_account\_currency”).
  - Set deferred\_account from “deferred\_expense\_account”.
- Set accounts from mapping of item.name → item.get(deferred\_account) for item drawn from items.
  - Draw item from items.
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set gl\_entries\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise ….
- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Set journal\_entry\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise ….
- Set booked\_amounts from mapping of item.name → tuple(0, 0) for item drawn from items.
  - Draw item from items.
- For each entry in (gl\_entries\_details + journal\_entry\_details).
  - If entry.account differs from accounts at entry.item\_name.
    - Continue with the next iteration or loop test.
  - Set tuple(amount, account\_amount) from booked\_amounts at entry.item\_name.
  - Set booked\_amounts at entry.item\_name from tuple((amount + entry.total\_credit), (account\_amount + entry.total\_credit when doc.currency equals doc.company\_currency, otherwise entry.total\_credit\_in\_account\_currency)).
    - Value choice on doc.currency equals doc.company\_currency — true gives entry.total\_credit, false gives entry.total\_credit\_in\_account\_currency.
- Return booked\_amounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L743)

<a id="op-1bd8ed192efdc6"></a>
### Validate deferred revenue return cancellation

`operation_enterprise_binding_enterprise_accounts_deferred_revenue_validate_deferred_revenue_return_cancellation`

**Inputs** doc.

**Record and data access** read “Sales Invoice” via get\_value · read “GL Entry” via get\_all · resolve a document from “Sales Invoice” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cancel or delete the deferred revenue entries for Sales Invoice {0} before cancelling this credit note.”.format(get\_link\_to\_form(“Sales Invoice”, invoice.name)).

**Local steps**

- If (not doc.is\_return or not doc.return\_against).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.is\_return → not doc.return\_against.
  - Return no value.
- Set items from list of item for item drawn from doc.items where (item.enable\_deferred\_revenue and item.sales\_invoice\_item).
  - Draw item from doc.items, keep a combination only if ((item.enable\_deferred\_revenue and item.sales\_invoice\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.enable\_deferred\_revenue → item.sales\_invoice\_item.
- If not items.
  - Return no value.
- Evaluate Platform.db.get\_value(“Sales Invoice”, doc.return\_against, “name”, for\_update = true).
- Set entries from set of tuple(entry.voucher\_detail\_no, entry.account) for entry drawn from Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → doc.doctype, “voucher\_no” → doc.name, “is\_cancelled” → 0), fields = ….
  - Draw entry from Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → doc.doctype, “voucher\_no” → doc.name, “is\_cancelled” → 0), fields = list(“voucher\_detail\_no”, “account”)).
- Set deferred\_items from set of item.sales\_invoice\_item for item drawn from items where tuple(item.name, item.deferred\_revenue\_account) belongs to entries.
  - Draw item from items, keep a combination only if (tuple(item.name, item.deferred\_revenue\_account) belongs to entries).
- If not deferred\_items.
  - Return no value.
- Set invoice from Platform.get\_doc(“Sales Invoice”, doc.return\_against).
- Set booked\_amounts from get\_already\_booked\_amounts(invoice, list of item for item drawn from invoice.items where item.name belongs to deferred\_items).
  - Draw item from invoice.items, keep a combination only if (item.name belongs to deferred\_items).
- If any(generator of any(amounts) for amounts drawn from booked\_amounts.values()).
  - Draw amounts from booked\_amounts.values().
  - Call the validation error handler Platform.throw(translated “Cancel or delete the deferred revenue entries for Sales Invoice {0} before cancelling this credit note.”.format(get\_link\_to\_form(“Sales Invoice”, invoice.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L745)

<a id="op-1bd60cd0e24b31"></a>
### Get deferred revenue returns

`operation_enterprise_binding_enterprise_accounts_deferred_revenue_get_deferred_revenue_returns`

**Inputs** doc.

**Explicit results** mapping() · mapping of row.sales\_invoice\_item → row for row drawn from returns.

**Local steps**

- If doc.doctype differs from “Sales Invoice”.
  - Return mapping().
- Set invoice from Platform.qb.DocType(“Sales Invoice”).
- Set item from Platform.qb.DocType(“Sales Invoice Item”).
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set returns from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Return mapping of row.sales\_invoice\_item → row for row drawn from returns.
  - Draw row from returns.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L744)

<a id="op-40210b424d293c"></a>
### Book deferred income or expense

`operation_enterprise_accounts_deferred_revenue_business_behavior_book_deferred_income_or_expense`

**Inputs** doc, deferred\_process, posting\_date = no value.

**Record and data access** read “Company” via get\_value · read “Sales Invoice” via get\_value.

**Local steps**

- Set enable\_check from “enable\_deferred\_revenue” when doc.doctype equals “Sales Invoice”, otherwise “enable\_deferred\_expense”.
  - Value choice on doc.doctype equals “Sales Invoice” — true gives “enable\_deferred\_revenue”, false gives “enable\_deferred\_expense”.
- Set accounts\_frozen\_upto from Platform.db.get\_value(“Company”, doc.company, “accounts\_frozen\_till\_date”).
- Bind local operation \_book\_deferred\_revenue\_or\_expense for subsequent calls.
- Set via\_journal\_entry from cint(Platform.db.get\_singles\_value(“Accounts Settings”, “book\_deferred\_entries\_via\_journal\_entry”)).
- Set submit\_journal\_entry from cint(Platform.db.get\_singles\_value(“Accounts Settings”, “submit\_journal\_entries”)).
- Set book\_deferred\_entries\_based\_on from Platform.db.get\_singles\_value(“Accounts Settings”, “book\_deferred\_entries\_based\_on”).
- If doc.doctype equals “Sales Invoice”.
  - Evaluate Platform.db.get\_value(“Sales Invoice”, doc.name, “name”, for\_update = true).
- Set returned\_amounts from get\_deferred\_revenue\_returns(doc).
- For each item in doc.get(“items”).
  - If item.get(enable\_check).
    - If returned\_amount bound to returned\_amounts.get(item.name).
      - Set item from copy.copy(item).
      - Set item.base\_net\_amount from max(0, flt((item.base\_net\_amount − returned\_amount.base\_amount))).
      - Set item.net\_amount from max(0, flt((item.net\_amount − returned\_amount.amount))).
    - Evaluate \_book\_deferred\_revenue\_or\_expense(item, via\_journal\_entry, submit\_journal\_entry, book\_deferred\_entries\_based\_on).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L18) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L12)

<a id="op-535be400010d27"></a>
### Book deferred income or expense.book deferred revenue or expense

`operation_enterprise_accounts_deferred_revenue_business_behavior_book_deferred_income_or_expense_book_deferred_revenue_or_expense`

**Inputs** item, via\_journal\_entry, submit\_journal\_entry, book\_deferred\_entries\_based\_on, prev\_posting\_date = no value.

**Explicit results** no value.

**Local steps**

- Set tuple(start\_date, end\_date, last\_gl\_entry) from get\_booking\_dates(doc, item, posting\_date = posting\_date, prev\_posting\_date = prev\_posting\_date).
- If not (start\_date and end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → end\_date.
  - Return no value.
- Set account\_currency from get\_account\_currency((item.expense\_account or item.income\_account)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.expense\_account → item.income\_account.
- If doc.doctype equals “Sales Invoice”.
  - Set tuple(against, project) from tuple(doc.customer, doc.project).
  - Set tuple(credit\_account, debit\_account) from tuple(item.income\_account, item.deferred\_revenue\_account).
- Otherwise.
  - Set tuple(against, project) from tuple(doc.supplier, item.project).
  - Set tuple(credit\_account, debit\_account) from tuple(item.deferred\_expense\_account, item.expense\_account).
- Set total\_days from (date\_diff(item.service\_end\_date, item.service\_start\_date) + 1).
- Set total\_booking\_days from (date\_diff(end\_date, start\_date) + 1).
- If book\_deferred\_entries\_based\_on equals “Months”.
  - Set tuple(amount, base\_amount) from calculate\_monthly\_amount(doc, item, last\_gl\_entry, start\_date, …).
- Otherwise.
  - Set tuple(amount, base\_amount) from calculate\_amount(doc, item, last\_gl\_entry, total\_days, …).
- If not amount.
  - Set prev\_posting\_date from end\_date.
- Otherwise.
  - Set gl\_posting\_date from end\_date.
  - Set prev\_posting\_date from no value.
  - If (accounts\_frozen\_upto and getdate(end\_date) ≤ getdate(accounts\_frozen\_upto)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in accounts\_frozen\_upto → getdate(end\_date) ≤ getdate(accounts\_frozen\_upto).
    - Set gl\_posting\_date from get\_last\_day(add\_days(accounts\_frozen\_upto, 1)).
    - Set prev\_posting\_date from end\_date.
  - If via\_journal\_entry.
    - Evaluate book\_revenue\_via\_journal\_entry(doc, credit\_account, debit\_account, amount, …).
  - Otherwise.
    - Evaluate make\_gl\_entries(doc, credit\_account, debit\_account, against, …).
- If Platform.flags.deferred\_accounting\_error.
  - Return no value.
- If (getdate(end\_date) &lt; getdate(posting\_date) and not last\_gl\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(end\_date) &lt; getdate(posting\_date) → not last\_gl\_entry.
  - Evaluate \_book\_deferred\_revenue\_or\_expense(item, via\_journal\_entry, submit\_journal\_entry, book\_deferred\_entries\_based\_on, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L3272) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L19) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L13)

<a id="op-24e035855e7100"></a>
### Process deferred accounting

`operation_enterprise_accounts_deferred_revenue_business_behavior_process_deferred_accounting`

**Inputs** posting\_date = no value.

**Record and data access** read “Company” via get\_all · resolve a document from “Process Deferred Accounting” via get\_doc.

**State and service calls** call insert on doc · call submit on doc.

**Explicit results** no value.

**Local steps**

- If not posting\_date.
  - Set posting\_date from today().
- If not cint(Platform.db.get\_singles\_value(“Accounts Settings”, “automatically\_process\_deferred\_accounting\_entry”)).
  - Return no value.
- Set start\_date from add\_months(today(), negative 1).
- Set end\_date from add\_days(today(), negative 1).
- Set companies from Platform.get\_all(“Company”).
- For each company in companies.
  - For each record\_type in tuple(“Income”, “Expense”).
    - Set doc from Platform.get\_doc(doctype = “Process Deferred Accounting”, company = company.name, posting\_date = posting\_date, start\_date = start\_date, …).
    - Evaluate doc.insert().
    - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L4332) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L30) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L24)

<a id="op-42271fdd95571c"></a>
### Make gl entries

`operation_enterprise_accounts_deferred_revenue_business_behavior_make_general_ledger_entries`

**Inputs** doc, credit\_account, debit\_account, against, amount, base\_amount, posting\_date, project, account\_currency, cost\_center, item, deferred\_process = no value.

**State and service calls** commit · rollback.

**Explicit results** no value.

**Explicit failure paths** e.

**Local steps**

- Bind dependencies make\_gl\_entries.
- <a id="op-42271fdd95571c-guard-18"></a>If amount equals 0.
  - Return no value.
- Set gl\_entries from list().
- Evaluate gl\_entries.append(doc.get\_gl\_dict(mapping(“account” → credit\_account, “against” → against, “credit” → base\_amount, “credit\_in\_account\_currency” → amount, …), account\_currency, item = item)).
- Evaluate gl\_entries.append(doc.get\_gl\_dict(mapping(“account” → debit\_account, “against” → against, “debit” → base\_amount, “debit\_in\_account\_currency” → amount, …), account\_currency, item = item)).
- If gl\_entries.
  - Attempt the following.
    - Evaluate make\_gl\_entries(gl\_entries, cancel = doc.docstatus equals 2, merge\_entries = true).
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
  - On failure (Exception) bound to e.
    - If Platform.in\_test.
      - Evaluate doc.log\_error(formatted text Error while processing deferred accounting for Invoice {doc.name}).
      - Raise e.
    - Otherwise.
      - Evaluate Platform.db.rollback().
      - Evaluate doc.log\_error(formatted text Error while processing deferred accounting for Invoice {doc.name}).
      - Set Platform.flags.deferred\_accounting\_error from true.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison amount equals 0, amount = 0 selects the branch that returns no value. With amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-42271fdd95571c-guard-18)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L29) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L23)

<a id="op-a4fe9fa3cb80f5"></a>
### Send mail

`operation_enterprise_accounts_deferred_revenue_business_behavior_send_mail`

**Inputs** deferred\_process.

**Local steps**

- Set title from translated “Error while processing deferred accounting for {0}”.format(deferred\_process).
- Set link from get\_link\_to\_form(“Process Deferred Accounting”, deferred\_process).
- Set content from (translated “Deferred accounting failed for some invoices:” + whitespace '\\n').
- Update content using + translated “Please check Process Deferred Accounting {0} and submit manually after resolving errors.”.format(link).
- Evaluate sendmail\_to\_system\_managers(title, content).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L5672) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L31) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L25)

<a id="op-5f53491ffe8f46"></a>
### Book revenue via journal entry

`operation_enterprise_accounts_deferred_revenue_business_behavior_book_revenue_via_journal_entry`

**Inputs** doc, credit\_account, debit\_account, amount, base\_amount, posting\_date, project, account\_currency, cost\_center, item, deferred\_process = no value, submit = “No”.

**State and service calls** request new\_doc for “Journal Entry” · call save on journal\_entry · call submit on journal\_entry · commit · rollback.

**Explicit results** no value.

**Local steps**

- <a id="op-5f53491ffe8f46-guard-15"></a>If amount equals 0.
  - Return no value.
- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.posting\_date from posting\_date.
- Set journal\_entry.company from doc.company.
- Set journal\_entry.voucher\_type from “Deferred Revenue” when doc.doctype equals “Sales Invoice”, otherwise “Deferred Expense”.
  - Value choice on doc.doctype equals “Sales Invoice” — true gives “Deferred Revenue”, false gives “Deferred Expense”.
- Set journal\_entry.process\_deferred\_accounting from deferred\_process.
- Set debit\_entry from mapping(“account” → credit\_account, “credit” → base\_amount, “credit\_in\_account\_currency” → amount, “account\_currency” → account\_currency, …).
- Set credit\_entry from mapping(“account” → debit\_account, “debit” → base\_amount, “debit\_in\_account\_currency” → amount, “account\_currency” → account\_currency, …).
- For each dimension in get\_accounting\_dimensions().
  - Evaluate debit\_entry.update(mapping(dimension → item.get(dimension))).
  - Evaluate credit\_entry.update(mapping(dimension → item.get(dimension))).
- Evaluate journal\_entry.append(“accounts”, debit\_entry).
- Evaluate journal\_entry.append(“accounts”, credit\_entry).
- Attempt the following.
  - Evaluate journal\_entry.save().
  - If submit.
    - Evaluate journal\_entry.submit().
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate doc.log\_error(formatted text Error while processing deferred accounting for Invoice {doc.name}).
  - Set Platform.flags.deferred\_accounting\_error from true.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison amount equals 0, amount = 0 selects the branch that returns no value. With amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5f53491ffe8f46-guard-15)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L5882) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L20) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L14)

<a id="op-5e3880d8d742d3"></a>
### Get deferred booking accounts

`operation_enterprise_accounts_deferred_revenue_business_behavior_get_deferred_booking_accounts`

**Inputs** doctype, voucher\_detail\_no, dr\_or\_cr.

**Record and data access** read “Sales Invoice Item” via get\_value · read “Purchase Invoice Item” via get\_value.

**Explicit results** debit\_account · credit\_account.

**Local steps**

- If doctype equals “Sales Invoice”.
  - Set tuple(credit\_account, debit\_account) from Platform.db.get\_value(“Sales Invoice Item”, mapping(“name” → voucher\_detail\_no), list(“income\_account”, “deferred\_revenue\_account”)).
- Otherwise.
  - Set tuple(credit\_account, debit\_account) from Platform.db.get\_value(“Purchase Invoice Item”, mapping(“name” → voucher\_detail\_no), list(“deferred\_expense\_account”, “expense\_account”)).
- If dr\_or\_cr equals “Debit”.
  - Return debit\_account.
- Otherwise.
  - Return credit\_account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L6894) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L28) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L22)

## Report · Deferred revenue and expense

<a id="op-0115ca060ac700"></a>
### Deferred Item.initialize

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_initialize`

**Inputs** self, item, inv, gle\_entries.

**Local steps**

- Set self.name from item.
- Set self.parent from inv.name.
- Set self.item\_name from gle\_entries at 0.item\_name.
- Set self.service\_start\_date from gle\_entries at 0.service\_start\_date.
- Set self.service\_end\_date from gle\_entries at 0.service\_end\_date.
- Set self.base\_net\_amount from gle\_entries at 0.base\_net\_amount.
- Set self.filters from inv.filters.
- Set self.period\_list from inv.period\_list.
- If gle\_entries at 0.deferred\_revenue\_account.
  - Set self.type from “Deferred Sale Item”.
  - Set self.deferred\_account from gle\_entries at 0.deferred\_revenue\_account.
- Otherwise.
  - If gle\_entries at 0.deferred\_expense\_account.
    - Set self.type from “Deferred Purchase Item”.
    - Set self.deferred\_account from gle\_entries at 0.deferred\_expense\_account.
- Set self.gle\_entries from list().
- Set self.period\_total from list().
- Set self.last\_entry\_date from no value.
- If gle\_entries.
  - Set self.gle\_entries from gle\_entries.
  - For each x in self.gle\_entries.
    - If self.get\_amount(x).
      - Set self.last\_entry\_date from x.gle\_posting\_date.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get amount](operations-033.md#op-66249203c6f5a7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L852)

<a id="op-ad6a3833adbd72"></a>
### Deferred Item.report data

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_report_data`

**Inputs** self.

**Explicit results** ret\_data.

**Local steps**

- Set ret\_data from Platform.\_dict(mapping(“name” → self.item\_name)).
- Set ret\_data.service\_start\_date from self.service\_start\_date.
- Set ret\_data.service\_end\_date from self.service\_end\_date.
- Set ret\_data.amount from self.base\_net\_amount.
- For each period in self.period\_total.
  - Set ret\_data at period.key from period.total.
  - Set ret\_data.indent from 1.
- Return ret\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L3222) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L854)

<a id="op-66249203c6f5a7"></a>
### Deferred Item.get amount

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_get_amount`

**Inputs** self, entry.

**Explicit results** (flt(entry.debit) − flt(entry.credit)) · negative (flt(entry.credit) − flt(entry.debit)) · 0.

**Local steps**

- If self.type equals “Deferred Sale Item”.
  - Return (flt(entry.debit) − flt(entry.credit)).
- Otherwise.
  - If self.type equals “Deferred Purchase Item”.
    - Return negative (flt(entry.credit) − flt(entry.debit)).
- Return 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L3437) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L850)

<a id="op-8c3ac4ffb79a0a"></a>
### Deferred Item.get item total

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_get_item_total`

**Inputs** self.

**Explicit results** total.

**Local steps**

- Set total from 0.
- For each gle\_posting in self.gle\_entries.
  - Update total using + self.get\_amount(gle\_posting).
- Return total.

**Methods declared on this owner** [get amount](operations-033.md#op-66249203c6f5a7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L3630) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L851)

<a id="op-7d4c070b0deeca"></a>
### Deferred Item.calculate amount

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_calculate_amount`

**Inputs** self, start\_date, end\_date.

**Explicit results** self.calculate\_monthly\_amount(start\_date, end\_date) · self.calculate\_days\_amount(start\_date, end\_date).

**Local steps**

- If self.filters.book\_deferred\_entries\_based\_on equals “Months”.
  - Return self.calculate\_monthly\_amount(start\_date, end\_date).
- Otherwise.
  - Return self.calculate\_days\_amount(start\_date, end\_date).

**Methods declared on this owner** [calculate monthly amount](operations-033.md#op-5b41ca0f142adb), [calculate days amount](operations-033.md#op-8493d2295b5b76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L3730) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L846)

<a id="op-5b41ca0f142adb"></a>
### Deferred Item.calculate monthly amount

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_calculate_monthly_amount`

**Inputs** self, start\_date, end\_date.

**Explicit results** (self.base\_net\_amount − already\_booked\_amount) · base\_amount.

**Local steps**

- Set total\_months from ((((self.service\_end\_date.year − self.service\_start\_date.year) × 12) + (self.service\_end\_date.month − self.service\_start\_date.month)) + 1).
- Set prorate from (date\_diff(self.service\_end\_date, self.service\_start\_date) ÷ date\_diff(get\_last\_day(self.service\_end\_date), get\_first\_day(self.service\_start\_date))).
- Set actual\_months from rounded((total\_months × prorate), 1).
- Set already\_booked\_amount from self.get\_item\_total().
- If not actual\_months.
  - Return (self.base\_net\_amount − already\_booked\_amount).
- Set base\_amount from (self.base\_net\_amount ÷ actual\_months).
- If (base\_amount + already\_booked\_amount) &gt; self.base\_net\_amount.
  - Set base\_amount from (self.base\_net\_amount − already\_booked\_amount).
- If (get\_first\_day(start\_date) differs from start\_date or get\_last\_day(end\_date) differs from end\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_first\_day(start\_date) differs from start\_date → get\_last\_day(end\_date) differs from end\_date.
  - Set partial\_month from (flt(date\_diff(end\_date, start\_date)) ÷ flt(date\_diff(get\_last\_day(end\_date), get\_first\_day(start\_date)))).
  - Update base\_amount using × rounded(partial\_month, 1).
- Return base\_amount.

**Methods declared on this owner** [get item total](operations-033.md#op-8c3ac4ffb79a0a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L849)

<a id="op-8493d2295b5b76"></a>
### Deferred Item.calculate days amount

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_calculate_days_amount`

**Inputs** self, start\_date, end\_date.

**Explicit results** base\_amount.

**Local steps**

- Set base\_amount from 0.
- Set total\_days from (date\_diff(self.service\_end\_date, self.service\_start\_date) + 1).
- Set total\_booking\_days from (date\_diff(end\_date, start\_date) + 1).
- Set already\_booked\_amount from self.get\_item\_total().
- Set base\_amount from flt(((self.base\_net\_amount × total\_booking\_days) ÷ flt(total\_days))).
- If (base\_amount + already\_booked\_amount) &gt; self.base\_net\_amount.
  - Set base\_amount from (self.base\_net\_amount − already\_booked\_amount).
- Return base\_amount.

**Methods declared on this owner** [get item total](operations-033.md#op-8c3ac4ffb79a0a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L4448) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L847)

<a id="op-ee3de1e1780c95"></a>
### Deferred Item.make dummy gle

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_make_dummy_general_ledger_entry`

**Inputs** self, name, date, amount.

**Explicit results** entry.

**Local steps**

- Set entry from Platform.\_dict(mapping(“name” → name, “gle\_posting\_date” → date, “debit” → 0, “credit” → 0, …)).
- If self.type equals “Deferred Sale Item”.
  - Set entry.debit from amount.
- Otherwise.
  - If self.type equals “Deferred Purchase Item”.
    - Set entry.credit from amount.
- Return entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L4740) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L853)

<a id="op-149097bc68ab82"></a>
### Deferred Item.simulate future posting

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_simulate_future_posting`

**Inputs** self.

**Local steps**

- Set forecast\_start\_date from add\_days(self.last\_entry\_date, 1) when self.last\_entry\_date, otherwise self.service\_start\_date.
  - Value choice on self.last\_entry\_date — true gives add\_days(self.last\_entry\_date, 1), false gives self.service\_start\_date.
- If forecast\_start\_date ≤ self.service\_end\_date.
  - Set self.estimate\_for\_period\_list from get\_period\_list(self.filters.from\_fiscal\_year, self.filters.to\_fiscal\_year, forecast\_start\_date, self.service\_end\_date, company = self.filters.company, ignore\_fiscal\_year = true, …).
  - For each period in self.estimate\_for\_period\_list.
    - Set amount from self.calculate\_amount(period.from\_date, period.to\_date).
    - Set gle from self.make\_dummy\_gle(period.key, period.to\_date, amount).
    - Evaluate self.gle\_entries.append(gle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate amount](operations-033.md#op-7d4c070b0deeca), [make dummy gle](operations-033.md#op-ee3de1e1780c95).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L855)

<a id="op-0bea6119d0154d"></a>
### Deferred Item.calculate item revenue expense for period

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_item_calculate_item_revenue_expense_for_period`

**Inputs** self.

**Explicit results** self.period\_total.

**Local steps**

- For each period in self.period\_list.
  - Set period\_sum from 0.
  - Set actual from 0.
  - For each posting in self.gle\_entries.
    - If period.from\_date ≤ getdate(posting.gle\_posting\_date) ≤ period.to\_date.
      - Compare adjacent operands in order, stopping at the first false comparison in period.from\_date ≤ getdate(posting.gle\_posting\_date) ≤ period.to\_date.
      - Update period\_sum using + self.get\_amount(posting).
      - If posting.posted equals “posted”.
        - Update actual using + self.get\_amount(posting).
  - Evaluate self.period\_total.append(Platform.\_dict(mapping(“key” → period.key, “total” → period\_sum, “actual” → actual))).
- Return self.period\_total.

**Methods declared on this owner** [get amount](operations-033.md#op-66249203c6f5a7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L5343) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L848)

<a id="op-288af663619258"></a>
### Deferred Invoice.initialize

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_invoice_initialize`

**Inputs** self, invoice, items, filters, period\_list.

**Local steps**

- Set self.name from invoice.
- Set self.posting\_date from items at 0.posting\_date.
- Set self.filters from filters.
- Set self.period\_list from period\_list.
- Set self.period\_total from list().
- If items at 0.deferred\_revenue\_account.
  - Set self.type from “Sales”.
- Otherwise.
  - If items at 0.deferred\_expense\_account.
    - Set self.type from “Purchase”.
- Set self.items from list().
- Set self.uniq\_items from set(list of x.item for x drawn from items).
  - Draw x from items.
- For each item in self.uniq\_items.
  - Evaluate self.items.append(Deferred\_Item(item, self, list of x for x drawn from items where x.item equals item)).
    - Draw x from items, keep a combination only if (x.item equals item).
- Set self.amount\_total from sum(generator of item.base\_net\_amount for item drawn from self.items).
  - Draw item from self.items.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L5681) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L844)

<a id="op-fbbc0f4583e517"></a>
### Deferred Invoice.calculate invoice revenue expense for period

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_invoice_calculate_invoice_revenue_expense_for_period`

**Inputs** self.

**Explicit results** self.period\_total.

**Local steps**

- For each period in self.period\_list.
  - Evaluate self.period\_total.append(Platform.\_dict(mapping(“key” → period.key, “total” → 0, “actual” → 0))).
- For each item in self.items.
  - Set item\_total from item.calculate\_item\_revenue\_expense\_for\_period().
  - For each idx in range(len(self.period\_list)).
    - Update self.period\_total at idx.total using + item\_total at idx.total.
    - Update self.period\_total at idx.actual using + item\_total at idx.actual.
- Return self.period\_total.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L6143) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L842)

<a id="op-6aa42f42ccdd5e"></a>
### Deferred Invoice.estimate future

`operation_enterprise_accounts_report_deferred_revenue_and_expense_business_behavior_deferred_invoice_estimate_future`

**Inputs** self.

**Local steps**

- Evaluate list of item.simulate\_future\_posting() for item drawn from self.items.
  - Draw item from self.items.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0242.json#L6457) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L843)
