# Sales · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Customer

[Record definition](../../../../data/record-types/customer.json)

<a id="op-cf028739928b92"></a>
### Make address

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_address`

**Inputs** args, is\_primary\_address = 1, is\_shipping\_address = 1.

**Record and data access** resolve a document from mapping(“doctype” → “Address”, “address\_title” → args.get(party\_name\_key), “address\_line1” → args.get(“address\_line1”), “address\_line2” → args.get(“address\_line2”), …) via get\_doc.

**State and service calls** call insert on address.

**Explicit results** address.

**Explicit failure paths** validation helper — “{} &lt;br&gt;&lt;br&gt; &lt;ul&gt;{}&lt;/ul&gt;”.format(msg, whitespace '\\n'.join(reqd\_fields)).

**Local steps**

- Set reqd\_fields from list().
- For each field in list(“city”, “country”).
  - If not args.get(field).
    - Evaluate reqd\_fields.append(((text in the contract + field.title()) + “&lt;/li&gt;”)).
- If reqd\_fields.
  - Set msg from translated “Following fields are mandatory to create address:”.
  - Call the validation error handler Platform.throw(“{} &lt;br&gt;&lt;br&gt; &lt;ul&gt;{}&lt;/ul&gt;”.format(msg, whitespace '\\n'.join(reqd\_fields)), title = translated “Missing Values Required”).
- Set party\_name\_key from “customer\_name” when args.doctype equals “Customer”, otherwise “supplier\_name”.
  - Value choice on args.doctype equals “Customer” — true gives “customer\_name”, false gives “supplier\_name”.
- Set address from Platform.get\_doc(mapping(“doctype” → “Address”, “address\_title” → args.get(party\_name\_key), “address\_line1” → args.get(“address\_line1”), “address\_line2” → args.get(“address\_line2”), …)).
- If flags bound to args.get(“flags”).
  - Evaluate address.insert(ignore\_permissions = flags.get(“ignore\_permissions”)).
- Otherwise.
  - Evaluate address.insert().
- Return address.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1440)

<a id="op-d60b82c1d6fc5c"></a>
### Get customer primary

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_customer_primary`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** query.run().

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid type”.

**Local steps**

- Set customer from filters.get(“customer”).
- Set type from filters.get(“type”).
- If type does not belong to tuple(“Contact”, “Address”).
  - Call the validation error handler Platform.throw(translated “Invalid type”, Platform.PermissionError).
- Evaluate Platform.has\_permission(“Customer”, doc = customer, throw = true).
- Set type\_doctype from qb.DocType(type).
- Set dlink from qb.DocType(“Dynamic Link”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(type\_doctype.name).where(((dlink.link\_name equals  ….
- If type equals “Contact”.
  - Set query from query.select(type\_doctype.email\_id).
- Return query.run().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, doc = customer, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1157)

<a id="op-97108709eb821f"></a>
### Parse full name

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_parse_full_name`

**Inputs** full\_name.

**Declared result** tuple at tuple(str, (str bitwise or no value), (str bitwise or no value)).

**Explicit results** tuple(first\_name, middle\_name, last\_name).

**Local steps**

- Set names from full\_name.split().
- Set first\_name from names at 0.
- Set middle\_name from one space.join(names at slice 1 to negative 1) when len(names) &gt; 2, otherwise no value.
  - Value choice on len(names) &gt; 2 — true gives one space.join(names at slice 1 to negative 1), false gives no value.
- Set last\_name from names at negative 1 when len(names) &gt; 1, otherwise no value.
  - Value choice on len(names) &gt; 1 — true gives names at negative 1, false gives no value.
- Return tuple(first\_name, middle\_name, last\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1475)

<a id="op-b0e550aa1bde44"></a>
### Get data

`operation_enterprise_selling_record_definitions_customer_customer_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “customer”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “party”, “Quotation” → “party\_name”, “Opportunity” → “party\_name”, “Bank Account” → “party”, …), “dynamic\_links” → ma ….

**Local steps**

- Return mapping(“fieldname” → “customer”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “party”, “Quotation” → “party\_name”, “Opportunity” → “party\_name”, “Bank Account” → “party”, …), “dynamic\_links” → ma ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0626.json#L3168) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1165)

<a id="op-2a2bc882b986a1"></a>
### Get customer overview

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_get_customer_overview`

**Inputs** customer, company, period = “Current Fiscal Year”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** payload.

**Local steps**

- Evaluate check\_access(customer, company).
- If period does not belong to PERIODS.
  - Set period from “Current Fiscal Year”.
- Set as\_of from getdate(today()).
- Set tuple(from\_date, to\_date) from resolve\_period(period, company, as\_of).
- Set accounts from accounts\_access().
- Set payload from mapping(“customer” → customer, “company” → company, “currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “period” → period, …).
- For each tuple(key, fn, args) in tuple(tuple(“position”, position, tuple(customer, company, from\_date, to\_date, …)), tuple(“trend”, trend, tuple(customer, company, from\_date, to\_date, …)), tuple(“pipeline”, pipeline, tuple(customer, compa ….
  - Attempt the following.
    - Set payload at key from fn(expanded args).
  - On failure (Exception).
    - Set payload at key from no value.
    - Set payload at “errors” at key from 1.
    - Evaluate Platform.log\_error(title = (“Customer Overview: ” + key)).
- Return payload.

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1455)

<a id="op-11d3333b0d3097"></a>
### Get customer receivables

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_get_customer_receivables`

**Inputs** customer, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value · mapping(“currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “outstanding” → mapping(“value” → ar at “outstanding”, “unpaid\_count” → unpaid\_invoices(customer, company, as\_of) at  ….

**Local steps**

- Evaluate check\_access(customer, company).
- If not receivables\_access().
  - Return no value.
- Set as\_of from getdate(today()).
- Set ar from receivables(customer, company, as\_of).
- Set overdue\_prev from receivables(customer, company, add\_days(as\_of, negative 30)) at “overdue”.
- Return mapping(“currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “outstanding” → mapping(“value” → ar at “outstanding”, “unpaid\_count” → unpaid\_invoices(customer, company, as\_of) at  ….

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1456)

<a id="op-99665f4411c1f1"></a>
### Check access

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_check_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** customer, company.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1450)

<a id="op-945e8bf8b98576"></a>
### Accounts access

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_accounts_access`

**Inputs** no declared parameters.

**Explicit results** bool((Platform.has\_permission(“Sales Invoice”, “read”) and Platform.has\_permission(“GL Entry”, “read”))).

**Local steps**

- Return bool((Platform.has\_permission(“Sales Invoice”, “read”) and Platform.has\_permission(“GL Entry”, “read”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(“Sales Invoice”, “read”) → Platform.has\_permission(“GL Entry”, “read”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Invoice”, “read”), Platform.has\_permission(“GL Entry”, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1447)

<a id="op-a326cf1fa641d5"></a>
### Receivables access

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_receivables_access`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Report” via get\_cached\_doc.

**Explicit results** (accounts\_access() and Platform.get\_cached\_doc(“Report”, “Accounts Receivable Summary”).is\_permitted()).

**Local steps**

- Return (accounts\_access() and Platform.get\_cached\_doc(“Report”, “Accounts Receivable Summary”).is\_permitted()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in accounts\_access() → Platform.get\_cached\_doc(“Report”, “Accounts Receivable Summary”).is\_permitted().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Report”, “Accounts Receivable Summary”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1466)

<a id="op-b12601550ff95a"></a>
### Unrestricted read

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_unrestricted_read`

**Inputs** doctype.

**Explicit results** (readable and not build\_match\_conditions(doctype)).

**Local steps**

- Bind dependencies build\_match\_conditions.
- Set readable from Platform.has\_permission(doctype, “read”).
- Return (readable and not build\_match\_conditions(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in readable → not build\_match\_conditions(doctype).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1474)

<a id="op-6012a8f1f39c13"></a>
### Credit position

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_credit_position`

**Inputs** customer, company.

**Explicit results** mapping(“limit” → flt(get\_credit\_limit(customer, company)), “used” → flt(get\_customer\_outstanding(customer, company)) when unrestricted, otherwise no value).

**Local steps**

- Set unrestricted from all(generator of \_unrestricted\_read(doctype) for doctype drawn from tuple(“GL Entry”, “Sales Order”, “Delivery Note”)).
  - Draw doctype from tuple(“GL Entry”, “Sales Order”, “Delivery Note”).
- Return mapping(“limit” → flt(get\_credit\_limit(customer, company)), “used” → flt(get\_customer\_outstanding(customer, company)) when unrestricted, otherwise no value).
  - Value choice on unrestricted — true gives flt(get\_customer\_outstanding(customer, company)), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1452)

<a id="op-9a8ad3023dabf3"></a>
### Permitted

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_permitted`

**Inputs** doctype, filters, fields, remaining named values kwargs.

**Explicit results** Platform.qb.get\_query(doctype, filters = filters, fields = fields, ignore\_permissions = false, expanded names kwargs).run(as\_dict = true).

**Local steps**

- Return Platform.qb.get\_query(doctype, filters = filters, fields = fields, ignore\_permissions = false, expanded names kwargs).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1461)

<a id="op-8d80ec3ec8433e"></a>
### Invoice filters

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_invoice_filters`

**Inputs** customer, company, from\_date, to\_date.

**Explicit results** list(list(“docstatus”, “=”, 1), list(“customer”, “=”, customer), list(“company”, “=”, company), list(“is\_opening”, “!=”, “Yes”), …).

**Local steps**

- Return list(list(“docstatus”, “=”, 1), list(“customer”, “=”, customer), list(“company”, “=”, company), list(“is\_opening”, “!=”, “Yes”), …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1458)

<a id="op-98e049a0d246d1"></a>
### Resolve period

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_resolve_period`

**Inputs** period, company, as\_of.

**Explicit results** tuple(add\_months(as\_of.replace(day = 1), negative 11), as\_of) · tuple(as\_of.replace(month = quarter\_start\_month, day = 1), as\_of) · tuple(add\_to\_date(as\_of, months = negative 12, as\_string = false), as\_of) · tuple(getdate(prev.year\_start\_date), getdate(prev.year\_end\_date)) · tuple(getdate(fy.year\_start\_date), min(as\_of, getdate(fy.year\_end\_date))).

**Local steps**

- If period equals “Last 12 Months”.
  - Return tuple(add\_months(as\_of.replace(day = 1), negative 11), as\_of).
- If period equals “This Quarter”.
  - Set quarter\_start\_month from ((((as\_of.month − 1) floor divide 3) × 3) + 1).
  - Return tuple(as\_of.replace(month = quarter\_start\_month, day = 1), as\_of).
- Set fy from get\_fiscal\_year(as\_of, company = company, as\_dict = true, raise\_on\_missing = false).
- If not fy.
  - Return tuple(add\_to\_date(as\_of, months = negative 12, as\_string = false), as\_of).
- If period equals “Last Fiscal Year”.
  - Set prev from get\_fiscal\_year(add\_days(getdate(fy.year\_start\_date), negative 1), company = company, as\_dict = true, raise\_on\_missing = false).
  - If prev.
    - Return tuple(getdate(prev.year\_start\_date), getdate(prev.year\_end\_date)).
- Return tuple(getdate(fy.year\_start\_date), min(as\_of, getdate(fy.year\_end\_date))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1468)

<a id="op-e8d47162457fee"></a>
### Sales totals

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_sales_totals`

**Inputs** customer, company, from\_date, to\_date.

**Explicit results** tuple(flt(row.total), cint(row.count)).

**Local steps**

- Set si from DocType(“Sales Invoice”).
- Set row from permitted(“Sales Invoice”, invoice\_filters(customer, company, from\_date, to\_date), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“total”), Coalesce(nested operand in  … at 0.
- Return tuple(flt(row.total), cint(row.count)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1470)

<a id="op-e6ca33ad57dc3e"></a>
### Net sales

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_net_sales`

**Inputs** customer, company, from\_date, to\_date.

**Explicit results** sales\_totals(customer, company, from\_date, to\_date) at 0.

**Local steps**

- Return sales\_totals(customer, company, from\_date, to\_date) at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1459)

<a id="op-cef7ef91292fad"></a>
### Position

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_position`

**Inputs** customer, company, from\_date, to\_date, accounts.

**Explicit results** mapping() · mapping(“net\_sales” → mapping(“value” → current, “count” → invoice\_count, “delta” → pct\_change(current, prev), “delta\_positive\_is\_good” → true)).

**Local steps**

- If not accounts.
  - Return mapping().
- Set tuple(current, invoice\_count) from sales\_totals(customer, company, from\_date, to\_date).
- Set prev from net\_sales(customer, company, add\_to\_date(from\_date, years = negative 1), add\_to\_date(to\_date, years = negative 1)).
- Return mapping(“net\_sales” → mapping(“value” → current, “count” → invoice\_count, “delta” → pct\_change(current, prev), “delta\_positive\_is\_good” → true)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1463)

<a id="op-97f051c411b399"></a>
### Collection days

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_collection_days`

**Inputs** customer, company, as\_of, outstanding.

**Record and data access** read “Sales Invoice” via get\_list.

**Explicit results** no value · days when days ≤ 730, otherwise no value.

**Local steps**

- If outstanding ≤ 0.
  - Return no value.
- Set first\_invoice from Platform.get\_list(“Sales Invoice”, filters = mapping(“docstatus” → 1, “customer” → customer, “company” → company, “is\_opening” → list(“!=”, “Yes”), …), order\_by = “posting\_date asc”, limit = 1, pluck = “po ….
- Set history from (date\_diff(as\_of, first\_invoice at 0) + 1) when first\_invoice, otherwise 0.
  - Value choice on first\_invoice — true gives (date\_diff(as\_of, first\_invoice at 0) + 1), false gives 0.
- If history &lt; 30.
  - Return no value.
- Set trailing from net\_sales(customer, company, add\_days(as\_of, negative history), as\_of).
- If trailing ≤ 0.
  - Return no value.
- Set days from round((outstanding ÷ (trailing ÷ history))).
- Return days when days ≤ 730, otherwise no value.
  - Value choice on days ≤ 730 — true gives days, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1451)

<a id="op-26216df0787342"></a>
### Receivables

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_receivables`

**Inputs** customer, company, report\_date.

**Explicit results** mapping(“buckets” → buckets, “outstanding” → outstanding, “overdue” → overdue).

**Local steps**

- Bind dependencies accounts\_receivable.
- Set data from accounts\_receivable(mapping(“company” → company, “report\_date” → report\_date, “party\_type” → “Customer”, “party” → list(customer), …)) at 1.
- Set owed from list of d for d drawn from data where flt(d.get(“outstanding”)) &gt; 0.
  - Draw d from data, keep a combination only if (flt(d.get(“outstanding”)) &gt; 0).
- Set row from mapping of key → sum(generator of flt(d.get(key)) for d drawn from owed) for key drawn from tuple(“outstanding”, “total\_due”, “range1”, “range2”, …).
  - Draw key from tuple(“outstanding”, “total\_due”, “range1”, “range2”, …).
  - Draw d from owed.
- Set outstanding from sum(generator of flt(d.get(“outstanding”)) for d drawn from data).
  - Draw d from data.
- Set overdue from flt(row.get(“total\_due”)).
- Set not\_due from (flt(row.get(“outstanding”)) − overdue).
- Set buckets from list(mapping(“key” → “not\_due”, “label” → translated “Not due”, “value” → not\_due, “overdue” → false), mapping(“key” → “b1”, “label” → translated “0–30 days”, “value” → flt(row.get(“range1”)), “overdue” →  ….
- Return mapping(“buckets” → buckets, “outstanding” → outstanding, “overdue” → overdue).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1465)

<a id="op-8f132d60540cd6"></a>
### Reported advances

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_reported_advances`

**Inputs** customer, company, report\_date.

**Explicit results** row.get(“advance”) · no value · flt(get\_partywise\_advanced\_payment\_amount(list(“Customer”), report\_date, company = company, party = customer).get(customer)).

**Local steps**

- Bind dependencies execute.
- Set rows from execute(mapping(“company” → company, “report\_date” → report\_date, “party\_type” → “Customer”, “party” → list(customer), …)) at 1.
- Set row from next(generator of row for row drawn from rows where row.get(“party”) equals customer, no value).
  - Draw row from rows, keep a combination only if (row.get(“party”) equals customer).
- If row.
  - Return row.get(“advance”).
- If not \_unrestricted\_read(“Payment Ledger Entry”).
  - Return no value.
- Return flt(get\_partywise\_advanced\_payment\_amount(list(“Customer”), report\_date, company = company, party = customer).get(customer)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1467)

<a id="op-86a5788d590d72"></a>
### Ageing

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_ageing`

**Inputs** ar.

**Explicit results** mapping(“buckets” → buckets, “total” → total, “overdue” → overdue, “overdue\_pct” → flt(((overdue ÷ total) × 100), 1) when total, otherwise 0).

**Local steps**

- Set buckets from ar at “buckets”.
- Set total from flt(sum(generator of b at “value” for b drawn from buckets)).
  - Draw b from buckets.
- Set overdue from flt(sum(generator of b at “value” for b drawn from buckets where b at “overdue”)).
  - Draw b from buckets, keep a combination only if (b at “overdue”).
- Return mapping(“buckets” → buckets, “total” → total, “overdue” → overdue, “overdue\_pct” → flt(((overdue ÷ total) × 100), 1) when total, otherwise 0).
  - Value choice on total — true gives flt(((overdue ÷ total) × 100), 1), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1448)

<a id="op-d65aac78b1818d"></a>
### Trend

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_trend`

**Inputs** customer, company, from\_date, to\_date, as\_of, accounts.

**Explicit results** no value · mapping(“points” → points, “average” → flt((sum(closed) ÷ len(closed))) when closed, otherwise 0, “has\_mtd” → any(generator of p at “mtd” for p drawn from points)).

**Local steps**

- If not accounts.
  - Return no value.
- Set si from DocType(“Sales Invoice”).
- Set rows from permitted(“Sales Invoice”, invoice\_filters(customer, company, from\_date, to\_date), list(“posting\_date”, Sum(si.base\_net\_total).as\_(“total”)), group\_by = “posting\_date”).
- Set by\_month from mapping().
- For each r in rows.
  - Set month from getdate(r.posting\_date).replace(day = 1).
  - Set by\_month at month from (by\_month.get(month, 0.0) + flt(r.total)).
- Set tuple(points, closed) from tuple(list(), list()).
- Set cursor from getdate(from\_date).replace(day = 1).
- Set last from getdate(to\_date).replace(day = 1).
- Set current\_month from as\_of.replace(day = 1).
- While cursor ≤ last.
  - Set is\_mtd from cursor equals current\_month.
  - Set value from by\_month.get(cursor, 0.0).
  - Evaluate points.append(mapping(“month” → cursor, “value” → value, “mtd” → is\_mtd)).
  - If not is\_mtd.
    - Evaluate closed.append(value).
  - Set cursor from add\_months(cursor, 1).
- Return mapping(“points” → points, “average” → flt((sum(closed) ÷ len(closed))) when closed, otherwise 0, “has\_mtd” → any(generator of p at “mtd” for p drawn from points)).
  - Value choice on closed — true gives flt((sum(closed) ÷ len(closed))), false gives 0.
  - Draw p from points.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1471)

<a id="op-7166000000f483"></a>
### Pipeline

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_pipeline`

**Inputs** customer, company, as\_of, accounts.

**Explicit results** tiles.

**Local steps**

- Set tiles from mapping().
- If Platform.has\_permission(“Quotation”, “read”).
  - Evaluate tiles.update(quotation\_tiles(customer, company)).
- If Platform.has\_permission(“Sales Order”, “read”).
  - Evaluate tiles.update(sales\_order\_tiles(customer, company, as\_of)).
- If accounts.
  - Set tiles at “invoices” from unpaid\_invoices(customer, company, as\_of).
- Return tiles.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Quotation”, “read”), Platform.has\_permission(“Sales Order”, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1462)

<a id="op-2dab6efb00885f"></a>
### Quotation tiles

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_quotation_tiles`

**Inputs** customer, company.

**Explicit results** mapping(“quotations” → mapping(“value” → flt(quote.value), “count” → quote.count)).

**Local steps**

- Set quotation from DocType(“Quotation”).
- Set quote from permitted(“Quotation”, mapping(“docstatus” → 1, “status” → “Open”, “quotation\_to” → “Customer”, “party\_name” → customer, …), list(Coalesce(nested operand in the contract(nested operand in the contract), 0) … at 0.
- Return mapping(“quotations” → mapping(“value” → flt(quote.value), “count” → quote.count)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1464)
