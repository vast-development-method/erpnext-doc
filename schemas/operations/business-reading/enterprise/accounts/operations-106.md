# Accounting and settlement · operations 106

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Sales payment summary

<a id="op-016fca3a7ca972"></a>
### Get pos sales payment data

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_point_of_sale_sales_payment_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set sales\_invoice\_data from get\_pos\_invoice\_data(filters).
- Set data from list of list(row at “posting\_date”, row at “owner”, row at “mode\_of\_payment”, row at “net\_total”, …) for row drawn from sales\_invoice\_data.
  - Draw row from sales\_invoice\_data.
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0275.json#L6984) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L11)

<a id="op-2fad83042a9f6c"></a>
### Get sales payment data

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_sales_payment_data`

**Inputs** filters, columns.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set show\_payment\_detail from false.
- Set sales\_invoice\_data from get\_sales\_invoice\_data(filters).
- Set mode\_of\_payments from get\_mode\_of\_payments(filters).
- Set mode\_of\_payment\_details from get\_mode\_of\_payment\_details(filters).
- If filters.get(“payment\_detail”).
  - Set show\_payment\_detail from true.
- Otherwise.
  - Set show\_payment\_detail from false.
- For each inv in sales\_invoice\_data.
  - Set owner\_posting\_date from (inv at “owner” + cstr(inv at “posting\_date”)).
  - If show\_payment\_detail.
    - Set row from list(inv.posting\_date, inv.owner, one space, inv.net\_total, …).
    - Evaluate data.append(row).
    - For each mop\_detail in mode\_of\_payment\_details.get(owner\_posting\_date, list()).
      - Set row from list(inv.posting\_date, inv.owner, mop\_detail at 0, 0, …).
      - Evaluate data.append(row).
  - Otherwise.
    - Set total\_payment from 0.
    - For each mop\_detail in mode\_of\_payment\_details.get(owner\_posting\_date, list()).
      - Set total\_payment from (total\_payment + mop\_detail at 1).
    - Set row from list(inv.posting\_date, inv.owner, “, ”.join(mode\_of\_payments.get(owner\_posting\_date, list())), inv.net\_total, …).
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0276.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L13)

<a id="op-add6a3b25a95c6"></a>
### Get conditions

`operation_enterprise_binding_enterprise_accounts_report_sales_payment_summary_sales_payment_summary_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set conditions from “1=1”.
- If filters.get(“from\_date”).
  - Update conditions using + “ and a.posting\_date &gt;= %(from\_date)s”.
- If filters.get(“to\_date”).
  - Update conditions using + “ and a.posting\_date &lt;= %(to\_date)s”.
- If filters.get(“company”).
  - Update conditions using + “ and a.company=%(company)s”.
- If filters.get(“customer”).
  - Update conditions using + “ and a.customer = %(customer)s”.
- If filters.get(“owner”).
  - Update conditions using + “ and a.owner = %(owner)s”.
- If filters.get(“is\_pos”).
  - Update conditions using + “ and a.is\_pos = %(is\_pos)s”.
- If is\_restricted\_user().
  - If “permitted\_invoices” does not belong to filters.
    - Set filters at “permitted\_invoices” from get\_permitted\_invoices(filters).
  - Update conditions using + “ and a.name in %(permitted\_invoices)s”.
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1263)

<a id="op-2a36f085095835"></a>
### Get pos invoice data

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_point_of_sale_invoice_data`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** result.

**Local steps**

- Set conditions from get\_conditions(filters).
- Set result from Platform.db.sql(formatted text SELECT posting\_date, owner, sum(net\_total) as "net\_total", sum(total\_taxes) as "total\_taxes", sum(paid\_amount) as "paid\_amount", sum(outstanding\_amoun, filters, as\_dict = 1).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L10)

<a id="op-b5d774678a9a96"></a>
### Get sales invoice data

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_sales_invoice_data`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text   select  a.posting\_date, a.owner,  sum(a.base\_net\_total) as "net\_total",  sum(a.base\_total\_taxes\_and\_charges) as "total\_taxes",  sum(a.base\_, filters, as\_dict = 1).

**Local steps**

- Set conditions from get\_conditions(filters).
- Return Platform.db.sql(formatted text   select  a.posting\_date, a.owner,  sum(a.base\_net\_total) as "net\_total",  sum(a.base\_total\_taxes\_and\_charges) as "total\_taxes",  sum(a.base\_, filters, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L12)

<a id="op-e3e8ac31421372"></a>
### Get mode of payments

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_mode_of_payments`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** mode\_of\_payments.

**Local steps**

- Set mode\_of\_payments from mapping().
- Set invoice\_list from get\_invoices(filters).
- Set invoice\_list\_names from “,”.join(generator of ((“'” + invoice at “name”) + “'”) for invoice drawn from invoice\_list).
  - Draw invoice from invoice\_list.
- If invoice\_list.
  - Set inv\_mop from Platform.db.sql(formatted text select a.owner,a.posting\_date, ifnull(b.mode\_of\_payment, '') as mode\_of\_payment  from ′tabSales Invoice′ a, ′tabSales Invoice Payment′ b  where a., as\_dict = 1).
  - For each d in inv\_mop.
    - Evaluate mode\_of\_payments.setdefault((d at “owner” + cstr(d at “posting\_date”)), list()).append(d.mode\_of\_payment).
- Return mode\_of\_payments.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L8)

<a id="op-32ac3f9cbf88f9"></a>
### Get invoices

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_invoices`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text select a.name  from ′tabSales Invoice′ a  where a.docstatus = 1 and {conditions}, filters, as\_dict = 1).

**Local steps**

- Set conditions from get\_conditions(filters).
- Return Platform.db.sql(formatted text select a.name  from ′tabSales Invoice′ a  where a.docstatus = 1 and {conditions}, filters, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L6)

<a id="op-045b8d853a8766"></a>
### Get mode of payment details

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_mode_of_payment_details`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** mode\_of\_payment\_details.

**Local steps**

- Set mode\_of\_payment\_details from mapping().
- Set invoice\_list from get\_invoices(filters).
- Set invoice\_list\_names from “,”.join(generator of ((“'” + invoice at “name”) + “'”) for invoice drawn from invoice\_list).
  - Draw invoice from invoice\_list.
- If invoice\_list.
  - Set inv\_mop\_detail from Platform.db.sql(formatted text   select t.owner,         t.posting\_date,     t.mode\_of\_payment,     sum(t.paid\_amount) as paid\_amount  from (  select a.owner, a.posti, as\_dict = 1).
  - Set inv\_change\_amount from Platform.db.sql(formatted text select a.owner, a.posting\_date,  ifnull(b.mode\_of\_payment, '') as mode\_of\_payment, sum(a.base\_change\_amount) as change\_amount  from ′tabSales Invo, as\_dict = 1).
  - For each d in inv\_change\_amount.
    - For each det in inv\_mop\_detail.
      - If (det at “owner” equals d at “owner” and det at “posting\_date” equals d at “posting\_date” and det at “mode\_of\_payment” equals d at “mode\_of\_payment”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in det at “owner” equals d at “owner” → det at “posting\_date” equals d at “posting\_date” → det at “mode\_of\_payment” equals d at “mode\_of\_payment”.
        - Set paid\_amount from (det at “paid\_amount” − d at “change\_amount”).
        - Set det at “paid\_amount” from paid\_amount.
  - For each d in inv\_mop\_detail.
    - Evaluate mode\_of\_payment\_details.setdefault((d at “owner” + cstr(d at “posting\_date”)), list()).append(tuple(d.mode\_of\_payment, d.paid\_amount)).
- Return mode\_of\_payment\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L7)

<a id="op-c372cc6c45d0fb"></a>
### Is restricted user

`operation_enterprise_binding_enterprise_accounts_report_sales_payment_summary_sales_payment_summary_is_restricted_user`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** true · bool(DatabaseQuery(“Sales Invoice”).build\_match\_conditions(as\_condition = true)).

**Local steps**

- If not Platform.has\_permission(“Sales Invoice”, “read”).
  - Return true.
- Return bool(DatabaseQuery(“Sales Invoice”).build\_match\_conditions(as\_condition = true)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Invoice”, “read”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1265)

<a id="op-5029b0cf9e7262"></a>
### Get permitted invoices

`operation_enterprise_binding_enterprise_accounts_report_sales_payment_summary_sales_payment_summary_get_permitted_invoices`

**Inputs** filters.

**Declared result** tuple at tuple(str, ellipsis).

**Record and data access** read “Sales Invoice” via get\_list.

**Explicit results** (tuple(names) or tuple(empty text)).

**Local steps**

- Set invoice\_filters from list(list(“docstatus”, “=”, 1), list(“company”, “=”, filters.get(“company”))).
- If filters.get(“from\_date”).
  - Evaluate invoice\_filters.append(list(“posting\_date”, “&gt;=”, filters.get(“from\_date”))).
- If filters.get(“to\_date”).
  - Evaluate invoice\_filters.append(list(“posting\_date”, “&lt;=”, filters.get(“to\_date”))).
- Set names from Platform.get\_list(“Sales Invoice”, filters = invoice\_filters, pluck = “name”, limit\_page\_length = 0).
- Return (tuple(names) or tuple(empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tuple(names) → tuple(empty text).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1264)

## Report · Sales register

<a id="op-ec5aca5a83ba62"></a>
### Execute

`operation_enterprise_accounts_report_sales_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** \_execute(filters).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return \_execute(filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L18)

<a id="op-e3d47f45095b95"></a>
### Execute

`operation_enterprise_accounts_report_sales_register_business_behavior_execute_2`

**Inputs** filters, additional\_table\_columns = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, invoice\_list) · tuple(columns, res, no value, no value, …).

**Explicit failure paths** validation helper — translated “Please select a customer for fetching payments.”.

**Local steps**

- If not filters.
  - Set filters from Platform.\_dict(mapping()).
- Set include\_payments from filters.get(“include\_payments”).
- If (filters.get(“include\_payments”) and not filters.get(“customer”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“include\_payments”) → not filters.get(“customer”).
  - Call the validation error handler Platform.throw(translated “Please select a customer for fetching payments.”).
- Set invoice\_list from get\_invoices(filters, get\_query\_columns(additional\_table\_columns)).
- If filters.get(“include\_payments”).
  - Update invoice\_list using + get\_payments(filters).
- Set tuple(columns, income\_accounts, unrealized\_profit\_loss\_accounts, tax\_accounts) from get\_columns(invoice\_list, additional\_table\_columns, include\_payments).
- If not invoice\_list.
  - Evaluate msgprint(translated “No record found”).
  - Return tuple(columns, invoice\_list).
- Set invoice\_income\_map from get\_invoice\_income\_map(invoice\_list).
- Set internal\_invoice\_map from get\_internal\_invoice\_map(invoice\_list).
- Set tuple(invoice\_income\_map, invoice\_tax\_map) from get\_invoice\_tax\_map(invoice\_list, invoice\_income\_map, income\_accounts, include\_payments).
- Set invoice\_cc\_wh\_map from get\_invoice\_cc\_wh\_map(invoice\_list).
- Set invoice\_so\_dn\_map from get\_invoice\_so\_dn\_map(invoice\_list).
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- Set mode\_of\_payments from get\_mode\_of\_payments(list of inv.name for inv drawn from invoice\_list).
  - Draw inv from invoice\_list.
- Set customers from list(set(generator of d.customer for d drawn from invoice\_list)).
  - Draw d from invoice\_list.
- Set customer\_details from get\_party\_details(“Customer”, customers).
- Set res from list().
- If include\_payments.
  - Set opening\_row from get\_opening\_row(“Customer”, filters.customer, getdate(filters.from\_date), filters.company) at 0.
  - Evaluate res.append(mapping(“receivable\_account” → opening\_row.account, “debit” → flt(opening\_row.debit), “credit” → flt(opening\_row.credit), “balance” → flt(opening\_row.balance))).
- Set data from list().
- For each inv in invoice\_list.
  - Set sales\_order from list(set(invoice\_so\_dn\_map.get(inv.name, mapping()).get(“sales\_order”, list()))).
  - Set delivery\_note from list(set(invoice\_so\_dn\_map.get(inv.name, mapping()).get(“delivery\_note”, list()))).
  - Set cost\_center from list(set(invoice\_cc\_wh\_map.get(inv.name, mapping()).get(“cost\_center”, list()))).
  - Set warehouse from list(set(invoice\_cc\_wh\_map.get(inv.name, mapping()).get(“warehouse”, list()))).
  - Set inv\_customer\_details from customer\_details.get(inv.customer, mapping()).
  - Set row from mapping(“voucher\_type” → inv.doctype, “voucher\_no” → inv.name, “posting\_date” → inv.posting\_date, “customer” → inv.customer, …).
  - Set base\_net\_total from 0.
  - For each income\_acc in income\_accounts.
    - If (inv.is\_internal\_customer and inv.company equals inv.represents\_company).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in inv.is\_internal\_customer → inv.company equals inv.represents\_company.
      - Set income\_amount from 0.
    - Otherwise.
      - Set income\_amount from flt(invoice\_income\_map.get(inv.name, mapping()).get(income\_acc)).
    - Update base\_net\_total using + income\_amount.
    - Evaluate row.update(mapping(Platform.scrub(income\_acc) → income\_amount)).
  - For each account in unrealized\_profit\_loss\_accounts.
    - Evaluate row.update(mapping(Platform.scrub((account + “\_unrealized”)) → flt(internal\_invoice\_map.get(tuple(inv.name, account))))).
  - Evaluate row.update(mapping(“net\_total” → (base\_net\_total or inv.base\_net\_total))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in base\_net\_total → inv.base\_net\_total.
  - Set total\_tax from 0.
  - For each tax\_acc in tax\_accounts.
    - If tax\_acc does not belong to income\_accounts.
      - Set tax\_amount\_precision from (get\_field\_precision(Platform.get\_meta(“Sales Taxes and Charges”).get\_field(“tax\_amount”), currency = company\_currency) or 2).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_field\_precision(Platform.get\_meta(“Sales Taxes and Charges”).get\_field(“tax\_amount”), currency = company\_currency) → 2.
      - Set tax\_amount from flt(invoice\_tax\_map.get(inv.name, mapping()).get(tax\_acc), tax\_amount\_precision).
      - Update total\_tax using + tax\_amount.
      - Evaluate row.update(mapping(Platform.scrub(tax\_acc) → tax\_amount)).
  - Set outstanding\_precision from (get\_field\_precision(Platform.get\_meta(“Sales Invoice”).get\_field(“outstanding\_amount”), currency = company\_currency) or 2).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_field\_precision(Platform.get\_meta(“Sales Invoice”).get\_field(“outstanding\_amount”), currency = company\_currency) → 2.
  - Evaluate row.update(mapping(“tax\_total” → total\_tax, “grand\_total” → inv.base\_grand\_total, “rounded\_total” → inv.base\_rounded\_total)).
  - If inv.doctype equals “Sales Invoice”.
    - Evaluate row.update(mapping(“debit” → get\_receivable\_debit(inv), “credit” → get\_in\_invoice\_receivable\_credit(inv), “outstanding\_amount” → flt(get\_outstanding\_in\_company\_currency(inv, company\_currency), outstanding\_ ….
  - Otherwise.
    - Evaluate row.update(mapping(“debit” → inv.debit, “credit” → inv.credit)).
  - Evaluate data.append(row).
- Update res using + sorted(data, key = deferred anonymous expression).
- If include\_payments.
  - Set running\_balance from flt(opening\_row.balance).
  - For each row in range(1, len(res)).
    - Update running\_balance using + (res at row at “debit” − res at row at “credit”).
    - Evaluate res at row.update(mapping(“balance” → running\_balance)).
- Return tuple(columns, res, no value, no value, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L19)

<a id="op-9ed64bf49910eb"></a>
### Get receivable debit

`operation_enterprise_binding_enterprise_accounts_report_sales_register_sales_register_get_receivable_debit`

**Inputs** inv.

**Explicit results** inv.base\_rounded\_total · inv.base\_grand\_total.

**Local steps**

- If (inv.base\_rounding\_adjustment and inv.base\_rounded\_total).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in inv.base\_rounding\_adjustment → inv.base\_rounded\_total.
  - Return inv.base\_rounded\_total.
- Return inv.base\_grand\_total.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1267)

<a id="op-05911373f929f2"></a>
### Get outstanding in company currency

`operation_enterprise_binding_enterprise_accounts_report_sales_register_sales_register_get_outstanding_in_company_currency`

**Inputs** inv, company\_currency.

**Explicit results** flt(inv.outstanding\_amount) · (flt(inv.outstanding\_amount) × (inv.conversion\_rate or 1)).

**Local steps**

- If inv.party\_account\_currency equals company\_currency.
  - Return flt(inv.outstanding\_amount).
- Return (flt(inv.outstanding\_amount) × (inv.conversion\_rate or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv.conversion\_rate → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1266)

<a id="op-bffe0362143025"></a>
### Get in invoice receivable credit

`operation_enterprise_accounts_report_sales_register_business_behavior_get_in_invoice_receivable_credit`

**Inputs** inv.

**Explicit results** credit.

**Local steps**

- Set credit from flt(inv.loyalty\_amount).
- If inv.is\_pos.
  - Update credit using + ((flt(inv.base\_paid\_amount) − flt(inv.base\_change\_amount)) + flt(inv.base\_write\_off\_amount)).
- Return credit.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0278.json#L3297) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L23)

<a id="op-a23d76dbd9b992"></a>
### Get columns

`operation_enterprise_accounts_report_sales_register_business_behavior_get_columns`

**Inputs** invoice\_list, additional\_table\_columns, include\_payments = false.

**Explicit results** tuple(columns, accounts at 0, accounts at 1, accounts at 2).

**Local steps**

- Set columns from list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Voucher”, “fieldname” → “voucher\_no”, “fieldty ….
- If (additional\_table\_columns and not include\_payments).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_table\_columns → not include\_payments.
  - Update columns using + additional\_table\_columns.
- If not include\_payments.
  - Update columns using + list(mapping(“label” → translated “Customer Group”, “fieldname” → “customer\_group”, “fieldtype” → “Link”, “options” → “Customer Group”, …), mapping(“label” → translated “Territory”, “fieldname” → “territor ….
- Otherwise.
  - Update columns using + list(mapping(“fieldname” → “receivable\_account”, “label” → translated “Receivable Account”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“fieldname” → “debit”, “label” → translated “Debit”, “fi ….
- Set tuple(account\_columns, accounts) from get\_account\_columns(invoice\_list, include\_payments).
- Set net\_total\_column from list(mapping(“label” → translated “Net Total”, “fieldname” → “net\_total”, “fieldtype” → “Currency”, “options” → “currency”, …)).
- Set total\_columns from list(mapping(“label” → translated “Tax Total”, “fieldname” → “tax\_total”, “fieldtype” → “Currency”, “options” → “currency”, …)).
- If not include\_payments.
  - Update total\_columns using + list(mapping(“label” → translated “Grand Total”, “fieldname” → “grand\_total”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“label” → translated “Rounded Total”, “fieldname” → “rounded\_tota ….
- Set columns from (((((columns + account\_columns at 0) + account\_columns at 2) + net\_total\_column) + account\_columns at 1) + total\_columns).
- Update columns using + list(mapping(“label” → translated “Remarks”, “fieldname” → “remarks”, “fieldtype” → “Data”, “width” → 150)).
- Return tuple(columns, accounts at 0, accounts at 1, accounts at 2).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L21)

<a id="op-dea0b4a0847d84"></a>
### Get account columns

`operation_enterprise_accounts_report_sales_register_business_behavior_get_account_columns`

**Inputs** invoice\_list, include\_payments.

**Explicit results** tuple(columns, accounts).

**Local steps**

- Set income\_accounts from list().
- Set tax\_accounts from list().
- Set unrealized\_profit\_loss\_accounts from list().
- Set income\_columns from list().
- Set tax\_columns from list().
- Set unrealized\_profit\_loss\_account\_columns from list().
- If invoice\_list.
  - Set income\_accounts from Platform.db.sql\_list((query text (SELECT, Sales Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list)).
    - Draw inv from invoice\_list.
  - Set sales\_taxes\_query from get\_taxes\_query(invoice\_list, “Sales Taxes and Charges”, “Sales Invoice”).
  - Set sales\_tax\_accounts from sales\_taxes\_query.run(as\_dict = true, pluck = “account\_head”).
  - Set tax\_accounts from sales\_tax\_accounts.
  - If include\_payments.
    - Set advance\_taxes\_query from get\_taxes\_query(invoice\_list, “Advance Taxes and Charges”, “Payment Entry”).
    - Set advance\_tax\_accounts from advance\_taxes\_query.run(as\_dict = true, pluck = “account\_head”).
    - Set tax\_accounts from set((tax\_accounts + advance\_tax\_accounts)).
  - Set unrealized\_profit\_loss\_accounts from Platform.db.sql\_list((query text (SELECT, Sales Invoice) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list)).
    - Draw inv from invoice\_list.
- For each account in income\_accounts.
  - Evaluate income\_columns.append(mapping(“label” → account, “fieldname” → Platform.scrub(account), “fieldtype” → “Currency”, “options” → “currency”, …)).
- For each account in tax\_accounts.
  - If account does not belong to income\_accounts.
    - Evaluate tax\_columns.append(mapping(“label” → account, “fieldname” → Platform.scrub(account), “fieldtype” → “Currency”, “options” → “currency”, …)).
- For each account in unrealized\_profit\_loss\_accounts.
  - Evaluate unrealized\_profit\_loss\_account\_columns.append(mapping(“label” → account, “fieldname” → Platform.scrub((account + “\_unrealized”)), “fieldtype” → “Currency”, “options” → “currency”, …)).
- Set columns from list(income\_columns, unrealized\_profit\_loss\_account\_columns, tax\_columns).
- Set accounts from list(income\_accounts, unrealized\_profit\_loss\_accounts, tax\_accounts).
- Return tuple(columns, accounts).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L20)

<a id="op-705d65d1f7c2ce"></a>
### Get invoices

`operation_enterprise_accounts_report_sales_register_business_behavior_get_invoices`

**Inputs** filters, additional\_query\_columns.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set query from nested operand in the contract.qb.from\_(si).select(ConstantColumn(“Sales Invoice”).as\_(“doctype”), si.name, si.posting\_date, si.debit\_to, …).where(si.docstatus equals 1).
- If additional\_query\_columns.
  - For each col in additional\_query\_columns.
    - Set query from query.select(col).
- If filters.get(“customer”).
  - Set query from query.where(si.customer equals filters.customer).
- If filters.get(“customer\_group”).
  - Set customer\_groups from list(filters.customer\_group, expanded get\_descendants\_of(“Customer Group”, filters.customer\_group, ignore\_permissions = true)).
  - Set query from query.where(si.customer\_group.isin(customer\_groups)).
- Set query from get\_conditions(filters, query, “Sales Invoice”).
- Set query from apply\_common\_conditions(filters, query, doctype = “Sales Invoice”, child\_doctype = “Sales Invoice Item”).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(“Sales Invoice”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set query from query.orderby(“posting\_date”, order = Order.desc).
- Set query from query.orderby(“name”, order = Order.desc).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L29)

<a id="op-d7ebea36440286"></a>
### Get conditions

`operation_enterprise_accounts_report_sales_register_business_behavior_get_conditions`

**Inputs** filters, query, doctype.

**Explicit results** query.

**Local steps**

- Set parent\_doc from Platform.qb.DocType(doctype).
- If filters.get(“owner”).
  - Set query from query.where(parent\_doc.owner equals filters.owner).
- If filters.get(“mode\_of\_payment”).
  - Set payment\_doc from Platform.qb.DocType(“Sales Invoice Payment”).
  - Set query from query.inner\_join(payment\_doc).on(parent\_doc.name equals payment\_doc.parent).
  - Set query from query.where(payment\_doc.mode\_of\_payment equals filters.mode\_of\_payment).distinct().
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0279.json#L2195) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L22)

<a id="op-8c68b966a2338c"></a>
### Get payments

`operation_enterprise_accounts_report_sales_register_business_behavior_get_payments`

**Inputs** filters.

**Explicit results** (payment\_entries + journal\_entries).

**Local steps**

- Set args from Platform.\_dict(account = “debit\_to”, party = “customer”, party\_name = “customer\_name”, party\_account = get\_party\_account(“Customer”, filters.customer, filters.company, include\_advance = true)).
- Set payment\_entries from get\_payment\_entries(filters, args).
- Set journal\_entries from get\_journal\_entries(filters, args).
- Return (payment\_entries + journal\_entries).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L31)

<a id="op-098dfd4ab6140e"></a>
### Get invoice income map

`operation_enterprise_accounts_report_sales_register_business_behavior_get_invoice_income_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** invoice\_income\_map.

**Local steps**

- Set income\_details from Platform.db.sql((query text (SELECT, Sales Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set invoice\_income\_map from mapping().
- For each d in income\_details.
  - Evaluate invoice\_income\_map.setdefault(d.parent, Platform.\_dict()).setdefault(d.income\_account, list()).
  - Set invoice\_income\_map at d.parent at d.income\_account from flt(d.amount).
- Return invoice\_income\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L26)

<a id="op-5e2821559febaf"></a>
### Get internal invoice map

`operation_enterprise_accounts_report_sales_register_business_behavior_get_internal_invoice_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** internal\_invoice\_map.

**Local steps**

- Set unrealized\_amount\_details from Platform.db.sql((query text (SELECT, Sales Invoice) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set internal\_invoice\_map from mapping().
- For each d in unrealized\_amount\_details.
  - If d.unrealized\_profit\_loss\_account.
    - Evaluate internal\_invoice\_map.setdefault(tuple(d.name, d.unrealized\_profit\_loss\_account), d.amount).
- Return internal\_invoice\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L24)

<a id="op-5c9b8b1a6fc7a2"></a>
### Get invoice tax map

`operation_enterprise_accounts_report_sales_register_business_behavior_get_invoice_tax_map`

**Inputs** invoice\_list, invoice\_income\_map, income\_accounts, include\_payments = false.

**State and service calls** execute a supplied database query.

**Explicit results** tuple(invoice\_income\_map, invoice\_tax\_map).

**Local steps**

- Set tax\_details from Platform.db.sql((query text (SELECT, Sales Taxes and Charges) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- If include\_payments.
  - Update tax\_details using + get\_advance\_taxes\_and\_charges(invoice\_list).
- Set invoice\_tax\_map from mapping().
- For each d in tax\_details.
  - If d.account\_head belongs to income\_accounts.
    - If d.account\_head belongs to invoice\_income\_map at d.parent.
      - Update invoice\_income\_map at d.parent at d.account\_head using + flt(d.tax\_amount).
    - Otherwise.
      - Set invoice\_income\_map at d.parent at d.account\_head from flt(d.tax\_amount).
  - Otherwise.
    - Evaluate invoice\_tax\_map.setdefault(d.parent, Platform.\_dict()).setdefault(d.account\_head, list()).
    - Set invoice\_tax\_map at d.parent at d.account\_head from flt(d.tax\_amount).
- Return tuple(invoice\_income\_map, invoice\_tax\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L28)

<a id="op-06f7c772e33f23"></a>
### Get invoice so dn map

`operation_enterprise_accounts_report_sales_register_business_behavior_get_invoice_sales_order_record_name_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** invoice\_so\_dn\_map.

**Local steps**

- Set si\_items from Platform.db.sql((query text (SELECT, Sales Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set invoice\_so\_dn\_map from mapping().
- For each d in si\_items.
  - If d.sales\_order.
    - Evaluate invoice\_so\_dn\_map.setdefault(d.parent, nested operand in the contract.\_dict()).setdefault(“sales\_order”, list()).append(d.sales\_order).
  - Set delivery\_note\_list from no value.
  - If d.delivery\_note.
    - Set delivery\_note\_list from list(d.delivery\_note).
  - Otherwise.
    - If d.sales\_order.
      - Set delivery\_note\_list from Platform.db.sql\_list(query text (SELECT, Delivery Note Item), d.so\_detail).
  - If delivery\_note\_list.
    - Evaluate invoice\_so\_dn\_map.setdefault(d.parent, Platform.\_dict()).setdefault(“delivery\_note”, delivery\_note\_list).
- Return invoice\_so\_dn\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L27)
