# Sales · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Customer

[Record definition](../../../../data/record-types/customer.json)

<a id="op-e09f2ffbf00c79"></a>
### Sales order tiles

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_sales_order_tiles`

**Inputs** customer, company, as\_of.

**Explicit results** mapping(“delivery” → mapping(“value” → flt(delivery.value), “count” → delivery.count, “past\_due” → (delivery.past\_due or 0)), “billing” → mapping(“value” → flt(billing.value), “count” → billing.count)).

**Local steps**

- Set so from DocType(“Sales Order”).
- Set open\_orders from mapping(“docstatus” → 1, “customer” → customer, “company” → company, “status” → list(“not in”, OPEN\_SO\_STATUS)).
- Set delivery from permitted(“Sales Order”, mapping(expand open\_orders, “per\_delivered” → list(“&lt;”, 100), “skip\_delivery\_note” → 0), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“value … at 0.
- Set billing from permitted(“Sales Order”, mapping(expand open\_orders, “per\_billed” → list(“&lt;”, 100)), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“value”), Count(nested operand in t … at 0.
- Return mapping(“delivery” → mapping(“value” → flt(delivery.value), “count” → delivery.count, “past\_due” → (delivery.past\_due or 0)), “billing” → mapping(“value” → flt(billing.value), “count” → billing.count)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in delivery.past\_due → 0.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1469)

<a id="op-ea26da87727ad9"></a>
### Base outstanding

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_base_outstanding`

**Inputs** si, company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Case().when(si.party\_account\_currency equals company\_currency, si.outstanding\_amount).else\_((si.outstanding\_amount × si.conversion\_rate)).

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Return Case().when(si.party\_account\_currency equals company\_currency, si.outstanding\_amount).else\_((si.outstanding\_amount × si.conversion\_rate)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1449)

<a id="op-b3b448f8555eb7"></a>
### Unpaid invoices

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_unpaid_invoices`

**Inputs** customer, company, as\_of.

**Explicit results** mapping(“value” → flt(row.value), “count” → row.count, “overdue” → (row.overdue or 0)).

**Local steps**

- Set si from DocType(“Sales Invoice”).
- Set row from permitted(“Sales Invoice”, mapping(“docstatus” → 1, “customer” → customer, “company” → company, “is\_return” → 0, …), list(Coalesce(nested operand in the contract(nested operand in the contract), 0).as\_(“va … at 0.
- Return mapping(“value” → flt(row.value), “count” → row.count, “overdue” → (row.overdue or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.overdue → 0.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1473)

<a id="op-bc9ca19bff343a"></a>
### Get customer transactions

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_get_customer_transactions`

**Inputs** customer, company, doc\_type = “All”, limit = 20.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** rows at slice no value to limit.

**Local steps**

- Evaluate check\_access(customer, company).
- Set limit from min((cint(limit) or 20), 100).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(limit) → 20.
- Set accounts from accounts\_access().
- Set wanted from list(doc\_type) when doc\_type belongs to TRANSACTION\_TYPES, otherwise list(TRANSACTION\_TYPES).
  - Value choice on doc\_type belongs to TRANSACTION\_TYPES — true gives list(doc\_type), false gives list(TRANSACTION\_TYPES).
- Set rows from list().
- For each dt in wanted.
  - If ((dt belongs to tuple(“Sales Invoice”, “Payment Entry”) and not accounts) or not Platform.has\_permission(dt, “read”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (dt belongs to tuple(“Sales Invoice”, “Payment Entry”) and not accounts) → not Platform.has\_permission(dt, “read”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt belongs to tuple(“Sales Invoice”, “Payment Entry”) → not accounts.
    - Continue with the next iteration or loop test.
  - Evaluate rows.extend(\_fetch\_rows(dt, customer, company, limit)).
- Evaluate rows.sort(key = deferred anonymous expression, reverse = true).
- Return rows at slice no value to limit.

**Values supplied outside this operation** effective access from Platform.has\_permission(dt, “read”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1457)

<a id="op-676c06f5952982"></a>
### Txn specs

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_txn_specs`

**Inputs** no declared parameters.

**Explicit results** mapping(“Sales Invoice” → mapping(“party\_field” → “customer”, “extra” → mapping(), “fields” → list(“name”, “posting\_date as date”, “status”, “base\_grand\_total as amount”, …), “order\_by” → “posting\_date des ….

**Local steps**

- Return mapping(“Sales Invoice” → mapping(“party\_field” → “customer”, “extra” → mapping(), “fields” → list(“name”, “posting\_date as date”, “status”, “base\_grand\_total as amount”, …), “order\_by” → “posting\_date des ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1472)

<a id="op-5bace5d29a8cba"></a>
### Fetch rows

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_fetch_rows`

**Inputs** doctype, customer, company, limit.

**Record and data access** read “Company” via get\_cached\_value · read doctype via get\_list.

**Explicit results** rows.

**Local steps**

- Set spec from \_txn\_specs() at doctype.
- Set filters from mapping(“docstatus” → 1, “company” → company, spec at “party\_field” → customer, expand spec at “extra”).
- Set currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set rows from list().
- For each r in Platform.get\_list(doctype, filters = filters, fields = spec at “fields”, order\_by = spec at “order\_by”, limit = limit).
  - Evaluate rows.append(mapping(“name” → r.name, “doctype” → doctype, “type\_label” → translated doctype, “date” → str(r.date), …)).
- Return rows.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1453)

<a id="op-38fbb8cefb62a4"></a>
### Pct change

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_pct_change`

**Inputs** current, previous.

**Explicit results** no value · flt((((current − previous) ÷ abs(previous)) × 100), 1).

**Local steps**

- If not previous.
  - Return no value.
- Return flt((((current − previous) ÷ abs(previous)) × 100), 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1460)

<a id="op-5eb5def09e54d9"></a>
### Get customer companies

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_overview_get_customer_companies`

**Inputs** customer.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** sorted(companies).

**Local steps**

- Evaluate check\_access(customer).
- Set companies from set().
- For each tuple(doctype, filters) in tuple(tuple(“Sales Invoice”, mapping(“customer” → customer)), tuple(“Sales Order”, mapping(“customer” → customer)), tuple(“Quotation”, mapping(“quotation\_to” → “Customer”, “party\_name” → customer)), tuple( ….
  - If Platform.has\_permission(doctype, “read”).
    - Evaluate companies.update(Platform.get\_list(doctype, filters = mapping(expand filters, “docstatus” → 1), distinct = true, pluck = “company”)).
- Evaluate companies.discard(no value).
- Return sorted(companies).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1454)

## Report · Customer acquisition and loyalty

<a id="op-2a30226240e6c1"></a>
### Execute

`operation_enterprise_selling_report_customer_acquisition_and_loyalty_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** get\_data\_by\_time(filters, common\_columns) · get\_data\_by\_territory(filters, common\_columns).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set common\_columns from list(mapping(“label” → translated “New Customers”, “fieldname” → “new\_customers”, “fieldtype” → “Int”, “default” → 0, …), mapping(“label” → translated “Repeat Customers”, “fieldname” → “repeat\_customers”,  ….
- If filters.get(“view\_type”) equals “Monthly”.
  - Return get\_data\_by\_time(filters, common\_columns).
- Otherwise.
  - Return get\_data\_by\_territory(filters, common\_columns).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1533)

<a id="op-aeaed4bc485769"></a>
### Get data by time

`operation_enterprise_selling_report_customer_acquisition_and_loyalty_business_behavior_get_data_by_time`

**Inputs** filters, common\_columns.

**Explicit results** tuple(columns, out).

**Local steps**

- Set columns from list(mapping(“label” → translated “Year”, “fieldname” → “year”, “fieldtype” → “Data”, “width” → 100), mapping(“label” → translated “Month”, “fieldname” → “month”, “fieldtype” → “Data”, “width” → 100)).
- Update columns using + common\_columns.
- Set customers\_in from get\_customer\_stats(filters).
- Set tuple(from\_year, from\_month, temp) from filters.get(“from\_date”).split(“-”).
- Set tuple(to\_year, to\_month, temp) from filters.get(“to\_date”).split(“-”).
- Set tuple(from\_year, from\_month, to\_year, to\_month) from tuple(cint(from\_year), cint(from\_month), cint(to\_year), cint(to\_month)).
- Set out from list().
- For each year in range(from\_year, (to\_year + 1)).
  - For each month in range(from\_month when year equals from\_year, otherwise 1, (to\_month + 1) when year equals to\_year, otherwise 13).
    - Value choice on year equals from\_year — true gives from\_month, false gives 1.
    - Value choice on year equals to\_year — true gives (to\_month + 1), false gives 13.
    - Set key from formatted text {year}-{month}.
    - Set data from customers\_in.get(key).
    - Set new from data at “new” when data, otherwise list(0, 0.0).
      - Value choice on data — true gives data at “new”, false gives list(0, 0.0).
    - Set repeat from data at “repeat” when data, otherwise list(0, 0.0).
      - Value choice on data — true gives data at “repeat”, false gives list(0, 0.0).
    - Evaluate out.append(mapping(“year” → cstr(year), “month” → formatdate(formatted text {key}-01, “MMMM”), “new\_customers” → new at 0, “repeat\_customers” → repeat at 0, …)).
- Return tuple(columns, out).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1536)

<a id="op-32ef8ee9d785a8"></a>
### Get data by territory

`operation_enterprise_selling_report_customer_acquisition_and_loyalty_business_behavior_get_data_by_territory`

**Inputs** filters, common\_columns.

**Record and data access** execute query text (SELECT, Territory).

**Explicit results** tuple(columns, data, no value, no value, …).

**Local steps**

- Set columns from list(mapping(“label” → translated “Territory”, “fieldname” → “territory”, “fieldtype” → “Link”, “options” → “Territory”, …)).
- Update columns using + common\_columns.
- Set customers\_in from get\_customer\_stats(filters, tree\_view = true).
- Set territory\_dict from mapping().
- For each t in Platform.db.sql(query text (SELECT, Territory), as\_dict = 1).
  - Evaluate territory\_dict.update(mapping(t.name → mapping(“parent” → t.parent\_territory, “is\_group” → t.is\_group))).
- Set depth\_map from Platform.\_dict().
- For each tuple(name, info) in territory\_dict.items().
  - Set default from (depth\_map.get(info at “parent”) + 1) when info at “parent”, otherwise 0.
    - Value choice on info at “parent” — true gives (depth\_map.get(info at “parent”) + 1), false gives 0.
  - Evaluate depth\_map.setdefault(name, default).
- Set data from list().
- For each tuple(name, indent) in depth\_map.items().
  - Set condition from customers\_in.get(name).
  - Set new from customers\_in at name at “new” when condition, otherwise list(0, 0.0).
    - Value choice on condition — true gives customers\_in at name at “new”, false gives list(0, 0.0).
  - Set repeat from customers\_in at name at “repeat” when condition, otherwise list(0, 0.0).
    - Value choice on condition — true gives customers\_in at name at “repeat”, false gives list(0, 0.0).
  - Set temp from mapping(“territory” → name, “parent\_territory” → territory\_dict at name at “parent”, “indent” → indent, “new\_customers” → new at 0, …).
    - Value choice on indent — true gives 0, false gives 1.
  - Evaluate data.append(temp).
- Set loop\_data from sorted(data, key = deferred anonymous expression, reverse = true).
- For each ld in loop\_data.
  - If ld at “parent\_territory”.
    - Set parent\_data from next(generator of x for x drawn from data where x at “territory” equals ld at “parent\_territory”).
      - Draw x from data, keep a combination only if (x at “territory” equals ld at “parent\_territory”).
    - For each key in parent\_data.keys().
      - If key does not belong to list(“indent”, “territory”, “parent\_territory”, “bold”).
        - Update parent\_data at key using + ld at key.
- Return tuple(columns, data, no value, no value, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1535)

<a id="op-b86bbaf72a5a66"></a>
### Get customer stats

`operation_enterprise_selling_report_customer_acquisition_and_loyalty_business_behavior_get_customer_stats`

**Inputs** filters, tree\_view = false.

**Explicit results** customers\_in.

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract equal ….
- If filters.get(“company”).
  - Set query from query.where(si.company equals filters.get(“company”)).
- Set permitted\_customers from get\_permitted\_customers().
- If permitted\_customers is distinct from no value.
  - Set query from query.where(si.customer.isin(permitted\_customers)).
- Set invoices from query.run(as\_dict = true).
- Set acquisition from mapping().
- For each row in invoices.
  - If (not row.is\_return and row.customer does not belong to acquisition).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.is\_return → row.customer does not belong to acquisition.
    - Set key from row.territory when tree\_view, otherwise getdate(row.posting\_date).strftime(“%Y-%m”).
      - Value choice on tree\_view — true gives row.territory, false gives getdate(row.posting\_date).strftime(“%Y-%m”).
    - Set acquisition at row.customer from tuple(key, getdate(row.posting\_date)).
- Set from\_date from getdate(filters.get(“from\_date”)).
- Set counted from mapping().
- Set customers\_in from mapping().
- For each row in invoices.
  - Set posting\_date from getdate(row.posting\_date).
  - If posting\_date &lt; from\_date.
    - Continue with the next iteration or loop test.
  - Set key from row.territory when tree\_view, otherwise posting\_date.strftime(“%Y-%m”).
    - Value choice on tree\_view — true gives row.territory, false gives posting\_date.strftime(“%Y-%m”).
  - Set acq from acquisition.get(row.customer).
  - Set new\_or\_repeat from “new” when (acq and key equals acq at 0 and acq at 1 ≥ from\_date), otherwise “repeat”.
    - Value choice on (acq and key equals acq at 0 and acq at 1 ≥ from\_date) — true gives “new”, false gives “repeat”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in acq → key equals acq at 0 → acq at 1 ≥ from\_date.
  - Evaluate customers\_in.setdefault(key, mapping(“new” → list(0, 0.0), “repeat” → list(0, 0.0))).
  - Evaluate counted.setdefault(key, mapping(“new” → set(), “repeat” → set())).
  - If (not row.is\_return and row.customer does not belong to counted at key at new\_or\_repeat).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.is\_return → row.customer does not belong to counted at key at new\_or\_repeat.
    - Evaluate counted at key at new\_or\_repeat.add(row.customer).
    - Update customers\_in at key at new\_or\_repeat at 0 using + 1.
  - Update customers\_in at key at new\_or\_repeat at 1 using + row.base\_grand\_total.
- Return customers\_in.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1534)

<a id="op-e7bdbbb92f0be2"></a>
### Get permitted customers

`operation_enterprise_binding_enterprise_selling_report_customer_acquisition_and_loyalty_customer_acquisition_and_loyalty_get_permitted_customers`

**Inputs** no declared parameters.

**Explicit results** (allowed or no value).

**Local steps**

- Set customer\_perms from (get\_user\_permissions(Platform.session.user).get(“Customer”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_user\_permissions(Platform.session.user).get(“Customer”) → list().
- Set allowed from list of perm.get(“doc”) for perm drawn from customer\_perms where (not perm.get(“applicable\_for”) or perm.get(“applicable\_for”) equals “Sales Invoice”).
  - Draw perm from customer\_perms, keep a combination only if ((not perm.get(“applicable\_for”) or perm.get(“applicable\_for”) equals “Sales Invoice”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not perm.get(“applicable\_for”) → perm.get(“applicable\_for”) equals “Sales Invoice”.
- Return (allowed or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in allowed → no value.

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L97)

## Report · Customer credit balance

<a id="op-4b71d26d135c75"></a>
### Execute

`operation_enterprise_selling_report_customer_credit_balance_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set customer\_naming\_type from Platform.get\_single\_value(“Selling Settings”, “cust\_master\_name”).
- Set columns from get\_columns(customer\_naming\_type).
- Set data from list().
- Set customer\_list from get\_details(filters).
- For each d in customer\_list.
  - Set row from list().
  - Set tuple(credit\_limit, bypass\_credit\_limit\_check) from get\_credit\_limit\_settings(d.name, filters.get(“company”)).
  - Set outstanding\_amt from get\_customer\_outstanding(d.name, filters.get(“company”), ignore\_outstanding\_sales\_order = bypass\_credit\_limit\_check).
  - Set bal from (flt(credit\_limit) − flt(outstanding\_amt)).
  - If customer\_naming\_type equals “Naming Series”.
    - Set row from list(d.name, d.customer\_name, credit\_limit, outstanding\_amt, …).
  - Otherwise.
    - Set row from list(d.name, credit\_limit, outstanding\_amt, bal, …).
  - If credit\_limit.
    - Evaluate data.append(row).
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “cust\_master\_name”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1539)

<a id="op-358384a4efcaf1"></a>
### Get columns

`operation_enterprise_selling_report_customer_credit_balance_business_behavior_get_columns`

**Inputs** customer\_naming\_type.

**State and service calls** call insert on columns.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Customer” + “:Link/Customer:120”), (translated “Credit Limit” + “:Currency:120”), (translated “Outstanding Amt” + “:Currency:100”), (translated “Credit Balance” + “:Currency:120”), …).
- If customer\_naming\_type equals “Naming Series”.
  - Evaluate columns.insert(1, (translated “Customer Name” + “:Data:120”)).
- Return columns.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0662.json#L6395) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1540)

<a id="op-9c7a953a5dbce3"></a>
### Get details

`operation_enterprise_selling_report_customer_credit_balance_business_behavior_get_details`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set company from filters.get(“company”).
- Set c from Platform.qb.DocType(“Customer”).
- Set ccl from Platform.qb.DocType(“Customer Credit Limit”).
- Set query from nested operand in the contract(nested operand in the contract).left\_join(ccl).on(((nested operand in the contract.parent equals nested operand in the contract.name bitwise and nested operand in the contrac ….
- If filters.get(“customer”).
  - Set query from query.where(c.name equals filters.get(“customer”)).
- If not flt(Platform.get\_cached\_value(“Company”, company, “credit\_limit”)).
  - Set gccl from Platform.qb.DocType(“Customer Credit Limit”).as\_(“gccl”).
  - Set groups\_with\_limit from nested operand in the contract.qb.from\_(gccl).select(gccl.parent).where(((gccl.parenttype equals “Customer Group” bitwise and gccl.company equals company) bitwise and gccl.credit\_limit &gt; 0)).
  - Set query from query.where((ccl.name.isnotnull() bitwise or c.customer\_group.isin(groups\_with\_limit))).
- Return query.run(as\_dict = 1).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “credit\_limit”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1541)

## Report · Customer wise item price

<a id="op-32f30331a6d2ae"></a>
### Execute

`operation_enterprise_selling_report_customer_wise_item_price_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Please select a Customer”.

**Local steps**

- If not filters.
  - Set filters from mapping().
- If not filters.get(“customer”).
  - Call the validation error handler Platform.throw(translated “Please select a Customer”).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0663.json#L368) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1544)

<a id="op-a864db8b6f34aa"></a>
### Get columns

`operation_enterprise_selling_report_customer_wise_item_price_business_behavior_get_columns`

**Inputs** filters = no value.

**Explicit results** list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0663.json#L574) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L2)

<a id="op-20db916ea2864a"></a>
### Get data

`operation_enterprise_selling_report_customer_wise_item_price_business_behavior_get_data`

**Inputs** filters = no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** data.

**Local steps**

- Set customer\_details from get\_customer\_details(filters).
- Set items from get\_selling\_items(filters).
- Set item\_stock\_map from get\_item\_stock\_map().
- Set price\_lists from list(customer\_details.price\_list).
- If Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”).
  - Evaluate price\_lists.append(Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”)).
- Set price\_lists from list(dict.fromkeys(generator of pl for pl drawn from price\_lists where pl)).
  - Draw pl from price\_lists, keep a combination only if (pl).
- Set data from list().
- For each item in items.
  - Set tuple(rate, price\_list) from get\_item\_selling\_rate(item, customer\_details.customer, price\_lists).
  - Evaluate data.append(mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “selling\_rate” → rate, “price\_list” → price\_list, …)).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”), Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L4)

<a id="op-897d510c045639"></a>
### Get item selling rate

`operation_enterprise_binding_enterprise_selling_report_customer_wise_item_price_customer_wise_item_price_get_item_selling_rate`

**Inputs** item, customer, price\_lists.

**Explicit results** tuple(rate, price\_list) · tuple(0.0, price\_lists at 0 when price\_lists, otherwise no value).

**Local steps**

- Set ctx from Platform.\_dict(mapping(“customer” → customer, “uom” → item.stock\_uom, “transaction\_date” → nowdate())).
- For each price\_list in price\_lists.
  - Set ctx.price\_list from price\_list.
  - Set prices from get\_item\_price(ctx, item.item\_code).
  - If (prices and rate bound to flt(prices at 0.price\_list\_rate)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in prices → rate bound to flt(prices at 0.price\_list\_rate).
    - Return tuple(rate, price\_list).
- Return tuple(0.0, price\_lists at 0 when price\_lists, otherwise no value).
  - Value choice on price\_lists — true gives price\_lists at 0, false gives no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L98)

<a id="op-977d3bf275a9cf"></a>
### Get item stock map

`operation_enterprise_binding_enterprise_selling_report_customer_wise_item_price_customer_wise_item_price_get_item_stock_map`

**Inputs** no declared parameters.

**Record and data access** read “Bin” via get\_all.

**Explicit results** mapping of item.item\_code → item.available for item drawn from item\_stock.

**Local steps**

- Set item\_stock from Platform.get\_all(“Bin”, fields = list(“item\_code”, mapping(“SUM” → “actual\_qty”, “as” → “available”)), group\_by = “item\_code”).
- Return mapping of item.item\_code → item.available for item drawn from item\_stock.
  - Draw item from item\_stock.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L99)

<a id="op-68f5f38d40fe2e"></a>
### Get customer details

`operation_enterprise_selling_report_customer_wise_item_price_business_behavior_get_customer_details`

**Inputs** filters.

**Explicit results** customer\_details.

**Local steps**

- Set customer\_details from \_get\_party\_details(party = filters.get(“customer”), party\_type = “Customer”).
- Evaluate customer\_details.update(mapping(“company” → get\_default\_company(), “price\_list” → customer\_details.get(“selling\_price\_list”))).
- Return customer\_details.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0663.json#L2381) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L3)

<a id="op-4e5c646e3c1225"></a>
### Get selling items

`operation_enterprise_selling_report_customer_wise_item_price_business_behavior_get_selling_items`

**Inputs** filters.

**Record and data access** read “Item” via get\_all.

**Explicit results** items.

**Local steps**

- If filters.get(“item”).
  - Set item\_filters from list(mapping(“item\_code” → filters.get(“item”), “is\_sales\_item” → 1, “disabled” → 0)).
- Otherwise.
  - Set item\_filters from list(mapping(“is\_sales\_item” → 1, “disabled” → 0)).
- If condition bound to get\_allowed\_masters\_condition(Platform.qb.DocType(“Item”).name, “Item”).
  - Evaluate item\_filters.append(condition).
- Set items from Platform.get\_all(“Item”, filters = item\_filters, fields = list(“item\_code”, “item\_name”, “stock\_uom”), order\_by = “item\_name”).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L5)

## Report · Customers without any sales transactions

<a id="op-2826c6b84e4955"></a>
### Execute

`operation_enterprise_binding_enterprise_selling_report_customers_without_any_sales_transactions_customers_without_any_sales_transactions_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Local steps**

- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L100)
