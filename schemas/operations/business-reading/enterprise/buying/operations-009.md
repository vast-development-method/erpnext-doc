# Purchasing · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Supplier

[Record definition](../../../../data/record-types/supplier.json)

<a id="op-d8a2301a7c3c98"></a>
### Supplier.after rename

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_after_rename`

**Inputs** self, olddn, newdn, merge = false.

**State and service calls** call db\_set on self.

**Local steps**

- If Platform.defaults.get\_global\_default(“supp\_master\_name”) equals “Supplier Name”.
  - Evaluate self.db\_set(“supplier\_name”, newdn).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L3361) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L56)

<a id="op-d5879d9b9467cf"></a>
### Get supplier primary

`operation_enterprise_buying_record_definitions_supplier_business_behavior_get_supplier_primary`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** query.run().

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid type”.

**Local steps**

- Set supplier from filters.get(“supplier”).
- Set type from filters.get(“type”).
- If type does not belong to tuple(“Contact”, “Address”).
  - Call the validation error handler Platform.throw(translated “Invalid type”, Platform.PermissionError).
- Evaluate Platform.has\_permission(“Supplier”, doc = supplier, throw = true).
- Set type\_doctype from Platform.qb.DocType(type).
- Set dynamic\_link from Platform.qb.DocType(“Dynamic Link”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(type\_doctype.name).where(((dynamic\_link.link\_name  ….
- If type equals “Contact”.
  - Set query from query.select(type\_doctype.email\_id).
- Return query.run().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Supplier”, doc = supplier, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L53)

<a id="op-95442a04d95c17"></a>
### Get data

`operation_enterprise_buying_record_definitions_supplier_supplier_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “supplier”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “party”, “Bank Account” → “party”), “dynamic\_links” → mapping(“party” → list(“Supplier”, “party\_type”)), “transaction ….

**Local steps**

- Return mapping(“fieldname” → “supplier”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “party”, “Bank Account” → “party”), “dynamic\_links” → mapping(“party” → list(“Supplier”, “party\_type”)), “transaction ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L4069) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L179)

<a id="op-f2c96677a0a421"></a>
### Get supplier overview

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_get_supplier_overview`

**Inputs** supplier, company, period = “Current Fiscal Year”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** payload.

**Local steps**

- Evaluate check\_access(supplier, company).
- If period does not belong to PERIODS.
  - Set period from “Current Fiscal Year”.
- Set as\_of from getdate(today()).
- Set tuple(from\_date, to\_date) from resolve\_period(period, company, as\_of).
- Set accounts from accounts\_access().
- Set payload from mapping(“supplier” → supplier, “company” → company, “currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “period” → period, …).
- For each tuple(key, fn, args) in tuple(tuple(“position”, position, tuple(supplier, company, from\_date, to\_date, …)), tuple(“trend”, trend, tuple(supplier, company, from\_date, to\_date, …)), tuple(“delivery”, delivery, tuple(supplier, compa ….
  - Attempt the following.
    - Set payload at key from fn(expanded args).
  - On failure (Exception).
    - Set payload at key from no value.
    - Set payload at “errors” at key from 1.
    - Evaluate Platform.log\_error(title = (“Supplier Overview: ” + key)).
- Return payload.

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L95)

<a id="op-f0e518551fda08"></a>
### Get supplier payables

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_get_supplier_payables`

**Inputs** supplier, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value · mapping(“currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “outstanding” → mapping(“value” → ap at “outstanding”, “unpaid\_count” → unpaid\_bills(supplier, company), “days\_to\_pay ….

**Local steps**

- Evaluate check\_access(supplier, company).
- If not payables\_access().
  - Return no value.
- Set as\_of from getdate(today()).
- Set ap from payables(supplier, company, as\_of).
- Set overdue\_prev from payables(supplier, company, add\_days(as\_of, negative 30)) at “overdue”.
- Return mapping(“currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “outstanding” → mapping(“value” → ap at “outstanding”, “unpaid\_count” → unpaid\_bills(supplier, company), “days\_to\_pay ….

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L96)

<a id="op-76c050fa43a9fe"></a>
### Check access

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_check_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** supplier, company.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L90)

<a id="op-d723e19ecfa3b5"></a>
### Accounts access

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_accounts_access`

**Inputs** no declared parameters.

**Explicit results** bool((Platform.has\_permission(“Purchase Invoice”, “read”) and Platform.has\_permission(“GL Entry”, “read”))).

**Local steps**

- Return bool((Platform.has\_permission(“Purchase Invoice”, “read”) and Platform.has\_permission(“GL Entry”, “read”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(“Purchase Invoice”, “read”) → Platform.has\_permission(“GL Entry”, “read”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Invoice”, “read”), Platform.has\_permission(“GL Entry”, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L848) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L88)

<a id="op-1ed83864681cca"></a>
### Payables access

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_payables_access`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Report” via get\_cached\_doc.

**Explicit results** (accounts\_access() and Platform.get\_cached\_doc(“Report”, “Accounts Payable”).is\_permitted()).

**Local steps**

- Return (accounts\_access() and Platform.get\_cached\_doc(“Report”, “Accounts Payable”).is\_permitted()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in accounts\_access() → Platform.get\_cached\_doc(“Report”, “Accounts Payable”).is\_permitted().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Report”, “Accounts Payable”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L106)

<a id="op-392eb5e1fa1b2c"></a>
### Invoice filters

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_invoice_filters`

**Inputs** supplier, company, from\_date, to\_date.

**Explicit results** list(list(“docstatus”, “=”, 1), list(“supplier”, “=”, supplier), list(“company”, “=”, company), list(“is\_opening”, “!=”, “Yes”), …).

**Local steps**

- Return list(list(“docstatus”, “=”, 1), list(“supplier”, “=”, supplier), list(“company”, “=”, company), list(“is\_opening”, “!=”, “Yes”), …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L98)

<a id="op-c40fcc99252015"></a>
### Purchase totals

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_purchase_totals`

**Inputs** supplier, company, from\_date, to\_date.

**Explicit results** tuple(flt(row.total), cint(row.count)).

**Local steps**

- Set pi from DocType(“Purchase Invoice”).
- Set row from permitted(“Purchase Invoice”, invoice\_filters(supplier, company, from\_date, to\_date), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“total”), Coalesce(nested operand  … at 0.
- Return tuple(flt(row.total), cint(row.count)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L110)

<a id="op-1ca6213c7a2751"></a>
### Position

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_position`

**Inputs** supplier, company, from\_date, to\_date, accounts.

**Explicit results** mapping() · mapping(“net\_purchases” → mapping(“value” → current, “count” → bill\_count, “delta” → pct\_change(current, previous), “delta\_positive\_is\_good” → true)).

**Local steps**

- If not accounts.
  - Return mapping().
- Set tuple(current, bill\_count) from purchase\_totals(supplier, company, from\_date, to\_date).
- Set previous from purchase\_totals(supplier, company, add\_months(from\_date, negative 12), add\_months(to\_date, negative 12)) at 0.
- Return mapping(“net\_purchases” → mapping(“value” → current, “count” → bill\_count, “delta” → pct\_change(current, previous), “delta\_positive\_is\_good” → true)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L109)

<a id="op-1d55db7b395de3"></a>
### Trend

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_trend`

**Inputs** supplier, company, from\_date, to\_date, accounts.

**Explicit results** no value · mapping(“points” → points, “purchased” → sum(generator of p at “purchased” for p drawn from points), “paid” → sum(generator of p at “paid” for p drawn from points)).

**Local steps**

- If not accounts.
  - Return no value.
- Set pi from DocType(“Purchase Invoice”).
- Set billed from monthly(permitted(“Purchase Invoice”, invoice\_filters(supplier, company, from\_date, to\_date), list(“posting\_date as date”, Sum(nested operand in the contract.base\_grand\_total).as\_(“amount”)), group\_by = “p ….
- Set pe from DocType(“Payment Entry”).
- Set signed from Case().when(pe.payment\_type equals “Pay”, pe.base\_paid\_amount).else\_(negative pe.base\_received\_amount).
- Set paid from monthly(((permitted(“Purchase Invoice”, list(expanded nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the co ….
- Set points from list().
- Set cursor from getdate(from\_date).replace(day = 1).
- While cursor ≤ getdate(to\_date).
  - Evaluate points.append(mapping(“month” → cursor, “purchased” → billed.get(cursor, 0.0), “paid” → paid.get(cursor, 0.0))).
  - Set cursor from add\_months(cursor, 1).
- Return mapping(“points” → points, “purchased” → sum(generator of p at “purchased” for p drawn from points), “paid” → sum(generator of p at “paid” for p drawn from points)).
  - Draw p from points.
  - Draw p from points.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L112)

<a id="op-7d95ccb275b113"></a>
### Journal payments

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_journal_payments`

**Inputs** supplier, company, from\_date, to\_date.

**Explicit results** list() · list of Platform.\_dict(date = row.date, amount = (flt(row.debit) − flt(row.credit))) for row drawn from rows.

**Local steps**

- If not Platform.has\_permission(“Journal Entry”, “read”).
  - Return list().
- Set rows from permitted(“Journal Entry”, list(list(“docstatus”, “=”, 1), list(“company”, “=”, company), list(“voucher\_type”, “in”, tuple(“Bank Entry”, “Cash Entry”)), list(“posting\_date”, “between”, tuple(from\_date, to\_ ….
- Return list of Platform.\_dict(date = row.date, amount = (flt(row.debit) − flt(row.credit))) for row drawn from rows.
  - Draw row from rows.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Journal Entry”, “read”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L101)

<a id="op-ab696194faa296"></a>
### Monthly

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_monthly`

**Inputs** rows.

**Explicit results** totals.

**Local steps**

- Set totals from mapping().
- For each row in rows.
  - Set month from getdate(row.date).replace(day = 1).
  - Set totals at month from (totals.get(month, 0.0) + flt(row.amount)).
- Return totals.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L102)

<a id="op-a93045f9552a59"></a>
### Delivery

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_delivery`

**Inputs** supplier, company, from\_date, to\_date, as\_of.

**Record and data access** read “Supplier Scorecard” via exists.

**Explicit results** no value · mapping(expand counts, “lines” → lines\_due, “orders” → len(orders), “on\_time\_rate” → flt(((counts at “on\_time” ÷ lines\_due) × 100), 1) when lines\_due, otherwise no value, …).

**Local steps**

- If not (Platform.has\_permission(“Purchase Order”, “read”) and Platform.has\_permission(“Purchase Receipt”, “read”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(“Purchase Order”, “read”) → Platform.has\_permission(“Purchase Receipt”, “read”).
  - Return no value.
- Set lines from permitted(“Purchase Order”, list(list(“docstatus”, “=”, 1), list(“supplier”, “=”, supplier), list(“company”, “=”, company), list(“status”, “!=”, “Closed”), …), list(“name”, “items.name as line”, “items.qty ….
- Set received\_on from fulfilment\_dates(supplier, company, mapping of line.line → flt(line.qty) for line drawn from lines).
  - Draw line from lines.
- Set counts from mapping(“on\_time” → 0, “late” → 0, “overdue” → 0).
- Set orders from set().
- For each line in lines.
  - Set due from getdate(line.schedule\_date).
  - If flt(line.received\_qty) ≥ flt(line.qty).
    - If line.line does not belong to received\_on.
      - Continue with the next iteration or loop test.
    - Set outcome from “late” when received\_on at line.line &gt; due, otherwise “on\_time”.
      - Value choice on received\_on at line.line &gt; due — true gives “late”, false gives “on\_time”.
  - Otherwise.
    - If (due &lt; as\_of and not line.closed).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in due &lt; as\_of → not line.closed.
      - Set outcome from “overdue”.
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Update counts at outcome using + 1.
  - Evaluate orders.add(line.name).
- Set lines\_due from sum(counts.values()).
- Return mapping(expand counts, “lines” → lines\_due, “orders” → len(orders), “on\_time\_rate” → flt(((counts at “on\_time” ÷ lines\_due) × 100), 1) when lines\_due, otherwise no value, …).
  - Value choice on lines\_due — true gives flt(((counts at “on\_time” ÷ lines\_due) × 100), 1), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.exists(“Supplier Scorecard”, supplier) → Platform.has\_permission(“Supplier Scorecard”, “read”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Order”, “read”), Platform.has\_permission(“Purchase Receipt”, “read”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L91)

<a id="op-a494be72ce370f"></a>
### Fulfilment dates

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_fulfilment_dates`

**Inputs** supplier, company, ordered.

**Explicit results** dates.

**Local steps**

- Set receipts from mapping().
- For each tuple(doctype, line\_field, extra) in tuple(tuple(“Purchase Receipt”, “purchase\_order\_item”, mapping()), tuple(“Purchase Invoice”, “po\_detail”, mapping(“update\_stock” → 1))).
  - If (not ordered or not Platform.has\_permission(doctype, “read”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ordered → not Platform.has\_permission(doctype, “read”).
    - Continue with the next iteration or loop test.
  - Set item from DocType(formatted text {doctype} Item).
  - For each row in permitted(doctype, list(mapping(“docstatus” → 1, “supplier” → supplier, “company” → company, expand extra), list(formatted text {doctype} Item, line\_field, “in”, list(ordered))), list(formatted text items. ….
    - Set day from receipts.setdefault(row.line, mapping()).
    - Set posted from getdate(row.posting\_date).
    - Set day at posted from (day.get(posted, 0) + flt(row.qty)).
- Set dates from mapping().
- For each tuple(line, by\_day) in receipts.items().
  - Set tuple(received, fulfilled) from tuple(0, no value).
  - For each posted in sorted(by\_day).
    - Update received using + by\_day at posted.
    - If received &lt; ordered at line.
      - Set fulfilled from no value.
    - Otherwise.
      - If not fulfilled.
        - Set fulfilled from posted.
  - If fulfilled.
    - Set dates at line from fulfilled.
- Return dates.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L92)

<a id="op-848e482ab1f661"></a>
### Pipeline

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_pipeline`

**Inputs** supplier, company, as\_of.

**Explicit results** tiles.

**Local steps**

- Set tiles from mapping().
- If Platform.has\_permission(“Supplier Quotation”, “read”).
  - Set tiles at “quotations” from open\_quotations(supplier, company, as\_of).
- If Platform.has\_permission(“Purchase Order”, “read”).
  - Evaluate tiles.update(order\_tiles(supplier, company, as\_of)).
- Return tiles.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Supplier Quotation”, “read”), Platform.has\_permission(“Purchase Order”, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L868) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L108)

<a id="op-fc178cb07ba74e"></a>
### Open quotations

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_open_quotations`

**Inputs** supplier, company, as\_of.

**Explicit results** mapping(“value” → flt(row.value), “count” → row.count, “expiring” → cint(row.expiring)).

**Local steps**

- Set sq from DocType(“Supplier Quotation”).
- Set expiring from Case().when((sq.valid\_till ≥ as\_of bitwise and sq.valid\_till ≤ add\_days(as\_of, 7)), 1).else\_(0).
- Set row from permitted(“Supplier Quotation”, mapping(“docstatus” → 1, “supplier” → supplier, “company” → company, “status” → list(“in”, OPEN\_SQ\_STATUS)), list(Coalesce(nested operand in the contract(nested operand in t … at 0.
- Return mapping(“value” → flt(row.value), “count” → row.count, “expiring” → cint(row.expiring)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L103)

<a id="op-e7bb054527aa93"></a>
### Order tiles

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_order_tiles`

**Inputs** supplier, company, as\_of.

**Explicit results** mapping(“receipt” → mapping(“value” → flt(sum(receipt.values()), 2), “count” → len(receipt), “next\_due” → str(min(upcoming)) when upcoming, otherwise no value, “orders” → sorted(receipt)), “billing” → no v ….

**Local steps**

- Set lines from permitted(“Purchase Order”, mapping(“docstatus” → 1, “supplier” → supplier, “company” → company, “status” → list(“not in”, CLOSED\_PO\_STATUS)), list(“name”, “items.name as line”, “items.qty”, “items.receive ….
- Set billed\_qty from invoiced\_quantities(list of line.line for line drawn from lines).
  - Draw line from lines.
- Set tuple(receipt, billing, late) from tuple(mapping(), mapping(), mapping()).
- Set tuple(upcoming, oldest) from tuple(list(), no value).
- For each line in lines.
  - If line.closed.
    - Continue with the next iteration or loop test.
  - Set qty from flt(line.qty).
  - Set rate from (flt(line.base\_amount) ÷ qty) when qty, otherwise 0.
    - Value choice on qty — true gives (flt(line.base\_amount) ÷ qty), false gives 0.
  - Set received from min(max(flt(line.received\_qty), 0), qty) when qty, otherwise 0.
    - Value choice on qty — true gives min(max(flt(line.received\_qty), 0), qty), false gives 0.
  - Set unbilled from ((received − flt(billed\_qty.get(line.line))) × rate) when billed\_qty is distinct from no value, otherwise 0.
    - Value choice on billed\_qty is distinct from no value — true gives ((received − flt(billed\_qty.get(line.line))) × rate), false gives 0.
  - If unbilled &gt; 0.
    - Set billing at line.name from (billing.get(line.name, 0) + unbilled).
  - Set pending from ((qty − received) × rate).
  - If (qty − received) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set receipt at line.name from (receipt.get(line.name, 0) + pending).
  - If not line.due.
    - Continue with the next iteration or loop test.
  - Set due from getdate(line.due).
  - If due &lt; as\_of.
    - Set late at line.name from (late.get(line.name, 0) + pending).
    - Set oldest from min((oldest or due), due).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in oldest → due.
  - Otherwise.
    - Evaluate upcoming.append(due).
- Return mapping(“receipt” → mapping(“value” → flt(sum(receipt.values()), 2), “count” → len(receipt), “next\_due” → str(min(upcoming)) when upcoming, otherwise no value, “orders” → sorted(receipt)), “billing” → no v ….
  - Value choice on upcoming — true gives str(min(upcoming)), false gives no value.
  - Value choice on billed\_qty is identical to no value — true gives no value, false gives mapping(“value” → flt(sum(billing.values()), 2), “count” → len(billing), “orders” → sorted(billing)).
  - Value choice on oldest — true gives date\_diff(as\_of, oldest), false gives no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L104)

<a id="op-4860306ebf1d47"></a>
### Invoiced quantities

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_invoiced_quantities`

**Inputs** lines.

**Explicit results** no value · mapping() · get\_invoiced\_qty\_against\_po\_items(lines).

**Local steps**

- If not \_unrestricted\_read(“Purchase Invoice”).
  - Return no value.
- If not lines.
  - Return mapping().
- Return get\_invoiced\_qty\_against\_po\_items(lines).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L100)

<a id="op-a08a15d86b8f3c"></a>
### Get invoiced qty against po items

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_get_invoiced_qty_against_po_items`

**Inputs** po\_items.

**Declared result** dict.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set purchase\_invoice from DocType(“Purchase Invoice”).
- Set purchase\_invoice\_item from DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(purchase\_invoice\_item.po\_detail, Sum(nested operand in the contract.qty)).where(((nested operand in the contract.isin(po\_items) bitwise ….
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L93)

<a id="op-5dd5af7c0f9fe4"></a>
### Payables

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_payables`

**Inputs** supplier, company, report\_date.

**Explicit results** mapping(“outstanding” → outstanding, “overdue” → total at “total\_due”, “buckets” → list(mapping(“label” → translated “Not due”, “value” → (outstanding − total at “total\_due”), “overdue” → false), mapping(“ ….

**Local steps**

- Bind dependencies execute.
- Set data from execute(mapping(“company” → company, “report\_date” → report\_date, “party\_type” → “Supplier”, “party” → list(supplier), …)) at 1.
- Set owed from list of d for d drawn from data where flt(d.get(“outstanding”)) &gt; 0.
  - Draw d from data, keep a combination only if (flt(d.get(“outstanding”)) &gt; 0).
- Set total from mapping of key → sum(generator of flt(d.get(key)) for d drawn from owed) for key drawn from tuple(“total\_due”, “range1”, “range2”, “range3”, …).
  - Draw key from tuple(“total\_due”, “range1”, “range2”, “range3”, …).
  - Draw d from owed.
- Set outstanding from sum(generator of flt(d.get(“outstanding”)) for d drawn from owed).
  - Draw d from owed.
- Return mapping(“outstanding” → outstanding, “overdue” → total at “total\_due”, “buckets” → list(mapping(“label” → translated “Not due”, “value” → (outstanding − total at “total\_due”), “overdue” → false), mapping(“ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L105)

<a id="op-89ad4cd295c6bf"></a>
### Unpaid bills

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_unpaid_bills`

**Inputs** supplier, company.

**Explicit results** permitted(“Purchase Invoice”, mapping(“docstatus” → 1, “supplier” → supplier, “company” → company, “is\_return” → 0, …), list(nested operand in the contract(nested operand in the contract).as\_(“count”))) at 0.count.

**Local steps**

- Set pi from DocType(“Purchase Invoice”).
- Return permitted(“Purchase Invoice”, mapping(“docstatus” → 1, “supplier” → supplier, “company” → company, “is\_return” → 0, …), list(nested operand in the contract(nested operand in the contract).as\_(“count”))) at 0.count.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L113)

<a id="op-ec94de70866d28"></a>
### Payment days

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_payment_days`

**Inputs** supplier, company, as\_of, outstanding.

**Record and data access** read “Purchase Invoice” via get\_list.

**Explicit results** no value · days when days ≤ 730, otherwise no value.

**Local steps**

- If outstanding ≤ 0.
  - Return no value.
- Set first\_bill from Platform.get\_list(“Purchase Invoice”, filters = mapping(“docstatus” → 1, “supplier” → supplier, “company” → company, “is\_opening” → list(“!=”, “Yes”), …), order\_by = “posting\_date asc”, limit = 1, pluck =  ….
- Set history from (date\_diff(as\_of, first\_bill at 0) + 1) when first\_bill, otherwise 0.
  - Value choice on first\_bill — true gives (date\_diff(as\_of, first\_bill at 0) + 1), false gives 0.
- If history &lt; 30.
  - Return no value.
- Set trailing from purchase\_totals(supplier, company, add\_days(as\_of, negative history), as\_of) at 0.
- If trailing ≤ 0.
  - Return no value.
- Set days from round((outstanding ÷ (trailing ÷ history))).
- Return days when days ≤ 730, otherwise no value.
  - Value choice on days ≤ 730 — true gives days, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L867) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L107)
