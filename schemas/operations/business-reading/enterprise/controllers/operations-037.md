# Shared transaction rules · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Trends

<a id="op-a476781f730182"></a>
### Get period wise terms

`operation_enterprise_binding_enterprise_controllers_trends_get_period_wise_terms`

**Inputs** bet\_dates, trans\_date, t2.

**Explicit results** list(Sum(Case().when(in\_period, t2.stock\_qty)), Sum(Case().when(in\_period, t2.base\_net\_amount))).

**Local steps**

- Set in\_period from trans\_date at slice bet\_dates at 0 to bet\_dates at 1.
- Return list(Sum(Case().when(in\_period, t2.stock\_qty)), Sum(Case().when(in\_period, t2.base\_net\_amount))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L463)

<a id="op-1c3dc40f60d458"></a>
### Get period date ranges

`operation_enterprise_controllers_trends_business_behavior_get_period_date_ranges`

**Inputs** period, fiscal\_year = no value, year\_start\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** period\_date\_ranges.

**Local steps**

- Bind dependencies relativedelta.
- If not year\_start\_date.
  - Set tuple(year\_start\_date, year\_end\_date) from Platform.get\_cached\_value(“Fiscal Year”, fiscal\_year, list(“year\_start\_date”, “year\_end\_date”)).
- Set increment from mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(period).
- Set period\_date\_ranges from list().
- For each \_i in range(1, 13, increment).
  - Set period\_end\_date from (getdate(year\_start\_date) + relativedelta(months = increment, days = negative 1)).
  - If period\_end\_date &gt; getdate(year\_end\_date).
    - Set period\_end\_date from year\_end\_date.
  - Evaluate period\_date\_ranges.append(list(year\_start\_date, period\_end\_date)).
  - Set year\_start\_date from (period\_end\_date + relativedelta(days = 1)).
  - If period\_end\_date equals year\_end\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return period\_date\_ranges.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, fiscal\_year, list(“year\_start\_date”, “year\_end\_date”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L998)

<a id="op-7fd50c84ae5da6"></a>
### Get period month ranges

`operation_enterprise_controllers_trends_business_behavior_get_period_month_ranges`

**Inputs** period, fiscal\_year.

**Explicit results** period\_month\_ranges.

**Local steps**

- Bind dependencies relativedelta.
- Set period\_month\_ranges from list().
- For each tuple(start\_date, end\_date) in get\_period\_date\_ranges(period, fiscal\_year).
  - Set months\_in\_this\_period from list().
  - While start\_date ≤ end\_date.
    - Evaluate months\_in\_this\_period.append(start\_date.strftime(“%B”)).
    - Update start\_date using + relativedelta(months = 1).
  - Evaluate period\_month\_ranges.append(months\_in\_this\_period).
- Return period\_month\_ranges.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0423.json#L1795) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L999)

<a id="op-dec8423c6a24d9"></a>
### Quotation party name expr

`operation_enterprise_controllers_trends_business_behavior_quotation_party_name_expr`

**Inputs** t1.

**Explicit results** expr.

**Local steps**

- Set customer from Platform.qb.DocType(“Customer”).
- Set lead from Platform.qb.DocType(“Lead”).
- Set expr from nested operand in the contract().when(nested operand in the contract.quotation\_to equals “Customer”, nested operand in the contract.where(nested operand in the contract equals nested operand in the contrac ….
- If Platform.db.table\_exists(“CRM Deal”).
  - Set deal from Platform.qb.DocType(“CRM Deal”).
  - Set expr from expr.when(t1.quotation\_to equals “CRM Deal”, nested operand in the contract.from\_(deal).select(deal.organization).where(deal.name equals t1.party\_name)).
- Return expr.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1003)

<a id="op-7814edd0e3418c"></a>
### Quotation territory expr

`operation_enterprise_controllers_trends_business_behavior_quotation_territory_expr`

**Inputs** t1.

**Explicit results** nested operand in the contract().when(nested operand in the contract.quotation\_to equals “Customer”, nested operand in the contract.where(nested operand in the contract equals nested operand in the contrac ….

**Local steps**

- Set customer from Platform.qb.DocType(“Customer”).
- Set lead from Platform.qb.DocType(“Lead”).
- Set prospect from Platform.qb.DocType(“Prospect”).
- Return nested operand in the contract().when(nested operand in the contract.quotation\_to equals “Customer”, nested operand in the contract.where(nested operand in the contract equals nested operand in the contrac ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1004)

<a id="op-ea23e83d8aa8ec"></a>
### Based wise columns query

`operation_enterprise_controllers_trends_business_behavior_based_wise_columns_query`

**Inputs** based\_on, trans.

**Explicit results** based\_on\_details.

**Explicit failure paths** validation helper — translated “Project-wise data is not available for Quotation”.

**Local steps**

- Set tuple(t1, t2) from get\_tables(trans).
- Set based\_on\_details from mapping(“joins” → list()).
- If based\_on equals “Item”.
  - Set item\_master from Platform.qb.DocType(“Item”).
  - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, “width” → 120, …), mapping(“label” → translated “Item Name”, “fieldtype” → “Data”, “width” → 120, “fieldname” → “item\_name”)).
  - Set based\_on\_details at “based\_on\_select” from list(t2.item\_code, item\_master.item\_name.as\_(“item\_name”)).
  - Set based\_on\_details at “based\_on\_group\_by” from list(t2.item\_code, item\_master.item\_name).
  - Set based\_on\_details at “joins” from list(tuple(item\_master, t2.item\_code equals item\_master.name)).
- Otherwise.
  - If based\_on equals “Item Group”.
    - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Item Group”, “fieldtype” → “Link”, “options” → “Item Group”, “width” → 120, …)).
    - Set based\_on\_details at “based\_on\_select” from list(t2.item\_group).
    - Set based\_on\_details at “based\_on\_group\_by” from list(t2.item\_group).
  - Otherwise.
    - If based\_on equals “Customer”.
      - If trans equals “Quotation”.
        - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Party”, “fieldtype” → “Link”, “options” → “Customer”, “width” → 120, …), mapping(“label” → translated “Party Name”, “fieldtype” → “Data”, “width” → 120, “fieldname” → “pa ….
        - Set based\_on\_details at “based\_on\_select” from list(t1.party\_name, quotation\_party\_name\_expr(t1).as\_(“customer\_name”), quotation\_territory\_expr(t1).as\_(“territory”)).
        - Set based\_on\_details at “based\_on\_group\_by” from list(t1.party\_name, t1.quotation\_to).
      - Otherwise.
        - Set customer\_master from Platform.qb.DocType(“Customer”).
        - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Customer”, “fieldtype” → “Link”, “options” → “Customer”, “width” → 120, …), mapping(“label” → translated “Customer Name”, “fieldtype” → “Data”, “width” → 120, “fieldname” ….
        - Set based\_on\_details at “based\_on\_select” from list(t1.customer, customer\_master.customer\_name.as\_(“customer\_name”), customer\_master.territory.as\_(“territory”)).
        - Set based\_on\_details at “based\_on\_group\_by” from list(t1.customer, customer\_master.customer\_name, customer\_master.territory).
        - Set based\_on\_details at “joins” from list(tuple(customer\_master, t1.customer equals customer\_master.name)).
    - Otherwise.
      - If based\_on equals “Customer Group”.
        - Set customer\_group from t1.customer\_group.
        - Set customer\_group\_col from mapping(“label” → translated “Customer Group”, “fieldtype” → “Link”, “options” → “Customer Group”, “fieldname” → “customer\_group”).
        - If trans equals “Quotation”.
          - Set customer\_group from Coalesce(t1.customer\_group, empty text).
          - Set customer\_group\_col from mapping(“label” → translated “Customer Group”, “fieldtype” → “Data”, “fieldname” → “customer\_group”).
        - Set based\_on\_details at “based\_on\_cols” from list(customer\_group\_col).
        - Set based\_on\_details at “based\_on\_select” from list(customer\_group).
        - Set based\_on\_details at “based\_on\_group\_by” from list(customer\_group).
      - Otherwise.
        - If based\_on equals “Supplier”.
          - Set supplier\_master from Platform.qb.DocType(“Supplier”).
          - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Supplier”, “fieldtype” → “Link”, “options” → “Supplier”, “width” → 120, …), mapping(“label” → translated “Supplier Name”, “fieldtype” → “Data”, “width” → 120, “fieldname” ….
          - Set based\_on\_details at “based\_on\_select” from list(t1.supplier, supplier\_master.supplier\_name, supplier\_master.supplier\_group).
          - Set based\_on\_details at “based\_on\_group\_by” from list(t1.supplier, supplier\_master.supplier\_name, supplier\_master.supplier\_group).
          - Set based\_on\_details at “joins” from list(tuple(supplier\_master, t1.supplier equals supplier\_master.name)).
        - Otherwise.
          - If based\_on equals “Supplier Group”.
            - Set supplier\_master from Platform.qb.DocType(“Supplier”).
            - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Supplier Group”, “fieldtype” → “Link”, “options” → “Supplier Group”, “width” → 140, …)).
            - Set based\_on\_details at “based\_on\_select” from list(supplier\_master.supplier\_group).
            - Set based\_on\_details at “based\_on\_group\_by” from list(supplier\_master.supplier\_group).
            - Set based\_on\_details at “joins” from list(tuple(supplier\_master, t1.supplier equals supplier\_master.name)).
          - Otherwise.
            - If based\_on equals “Territory”.
              - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Territory”, “fieldtype” → “Link”, “options” → “Territory”, “width” → 120, …)).
              - Set based\_on\_details at “based\_on\_select” from list(t1.territory).
              - Set based\_on\_details at “based\_on\_group\_by” from list(t1.territory).
            - Otherwise.
              - If based\_on equals “Project”.
                - If trans belongs to list(“Sales Invoice”, “Delivery Note”, “Sales Order”).
                  - Set project from t1.project.
                - Otherwise.
                  - If trans belongs to list(“Purchase Order”, “Purchase Invoice”, “Purchase Receipt”).
                    - Set project from t2.project.
                  - Otherwise.
                    - Call the validation error handler Platform.throw(translated “Project-wise data is not available for Quotation”).
                - Set based\_on\_details at “based\_on\_cols” from list(mapping(“label” → translated “Project”, “fieldtype” → “Link”, “options” → “Project”, “width” → 120, …)).
                - Set based\_on\_details at “based\_on\_select” from list(project).
                - Set based\_on\_details at “based\_on\_group\_by” from list(project).
- Set company from Platform.qb.DocType(“Company”).
- Evaluate based\_on\_details at “based\_on\_select”.append(company.default\_currency.as\_(“currency”)).
- Evaluate based\_on\_details at “based\_on\_group\_by”.append(company.default\_currency).
- Evaluate based\_on\_details at “based\_on\_cols”.append(mapping(“label” → translated “Currency”, “fieldtype” → “Link”, “options” → “Currency”, “width” → 120, …)).
- Evaluate based\_on\_details at “joins”.append(tuple(company, t1.company equals company.name)).
- Return based\_on\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L992)

<a id="op-4c7953cba34a14"></a>
### Group wise column

`operation_enterprise_controllers_trends_business_behavior_group_wise_column`

**Inputs** group\_by, trans = no value.

**Explicit results** list() · list(mapping(“label” → translated “Party”, “fieldtype” → “Data”, “width” → 120, “fieldname” → “party”)) · list(mapping(“label” → translated group\_by, “fieldtype” → “Link”, “options” → group\_by, “width” → 120, …)).

**Local steps**

- If not group\_by.
  - Return list().
- If (trans equals “Quotation” and group\_by equals “Customer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in trans equals “Quotation” → group\_by equals “Customer”.
  - Return list(mapping(“label” → translated “Party”, “fieldtype” → “Data”, “width” → 120, “fieldname” → “party”)).
- Return list(mapping(“label” → translated group\_by, “fieldtype” → “Link”, “options” → group\_by, “width” → 120, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1001)

## Service · Website list for contact

<a id="op-fbde1cfc1b88ce"></a>
### Get list context

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_list_context`

**Inputs** context = no value.

**Record and data access** execute query text (SELECT, Currency).

**Explicit results** mapping(“global\_number\_format” → (Platform.db.get\_default(“number\_format”) or “#,###.##”), “currency” → Platform.db.get\_default(“currency”), “currency\_symbols” → json.dumps(dict(Platform.db.sql(query text  ….

**Local steps**

- Return mapping(“global\_number\_format” → (Platform.db.get\_default(“number\_format”) or “#,###.##”), “currency” → Platform.db.get\_default(“currency”), “currency\_symbols” → json.dumps(dict(Platform.db.sql(query text  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(“number\_format”) → “#,###.##”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1010)

<a id="op-e95ca94fc92d84"></a>
### Get webform list context

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_webform_list_context`

**Inputs** module.

**Explicit results** no value · mapping(“get\_list” → get\_webform\_transaction\_list).

**Local steps**

- If get\_module\_app(module) differs from “Enterprise”.
  - Return no value.
- Return mapping(“get\_list” → get\_webform\_transaction\_list).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L466) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1014)

<a id="op-0280023537413f"></a>
### Get webform transaction list

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_webform_transaction_list`

**Inputs** doctype, txt = no value, filters = no value, limit\_start = 0, limit\_page\_length = 20, order\_by = “creation”.

**Explicit results** get\_list(doctype, txt, filters, limit\_start, ignore\_permissions = false, fields = no value, order\_by = “creation”, …).

**Local steps**

- Bind dependencies get\_list.
- If not filters.
  - Set filters from list().
- Set meta from Platform.get\_meta(doctype).
- For each d in meta.fields.
  - If (d.fieldtype equals “Link” and d.fieldname differs from “amended\_from”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “Link” → d.fieldname differs from “amended\_from”.
    - Set allowed\_docs from list of d.name for d drawn from get\_transaction\_list(doctype = d.options, custom = true).
      - Draw d from get\_transaction\_list(doctype = d.options, custom = true).
    - Evaluate allowed\_docs.append(empty text).
    - Evaluate filters.append(tuple(d.fieldname, “in”, allowed\_docs)).
- Return get\_list(doctype, txt, filters, limit\_start, ignore\_permissions = false, fields = no value, order\_by = “creation”, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L558) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1015)

<a id="op-619e4790f685c6"></a>
### Get transaction list

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_transaction_list`

**Inputs** doctype, txt = no value, filters = no value, limit\_start = 0, limit\_page\_length = 20, order\_by = “creation desc”, custom = false.

**Explicit results** list() · rfq\_transaction\_list(parties\_doctype, doctype, parties, limit\_start, …) · transactions · post\_process(doctype, transactions).

**Local steps**

- Set user from Platform.session.user.
- Set ignore\_permissions from false.
- If not filters.
  - Set filters from mapping().
- Set filters at “docstatus” from list(“&lt;”, “2”) when doctype belongs to list(“Supplier Quotation”, “Purchase Invoice”), otherwise 1.
  - Value choice on doctype belongs to list(“Supplier Quotation”, “Purchase Invoice”) — true gives list(“&lt;”, “2”), false gives 1.
- If ((user differs from “Guest” and is\_website\_user()) or doctype equals “Request for Quotation”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (user differs from “Guest” and is\_website\_user()) → doctype equals “Request for Quotation”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user differs from “Guest” → is\_website\_user().
  - Set parties\_doctype from “Request for Quotation Supplier” when doctype equals “Request for Quotation”, otherwise doctype.
    - Value choice on doctype equals “Request for Quotation” — true gives “Request for Quotation Supplier”, false gives doctype.
  - Set tuple(customers, suppliers) from get\_customers\_suppliers(parties\_doctype, user).
  - If customers.
    - If doctype equals “Quotation”.
      - Set filters at “quotation\_to” from “Customer”.
      - Set filters at “party\_name” from list(“in”, customers).
    - Otherwise.
      - Set filters at “customer” from list(“in”, customers).
  - Otherwise.
    - If suppliers.
      - Set filters at “supplier” from list(“in”, suppliers).
    - Otherwise.
      - If not custom.
        - Return list().
  - If doctype equals “Request for Quotation”.
    - Set parties from (customers or suppliers).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in customers → suppliers.
    - Return rfq\_transaction\_list(parties\_doctype, doctype, parties, limit\_start, …).
  - Set ignore\_permissions from true.
  - If (not customers and not suppliers and custom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not customers → not suppliers → custom.
    - Set ignore\_permissions from false.
    - Set filters from mapping().
- Set transactions from get\_list\_for\_transactions(doctype, txt, filters, limit\_start, fields = “name”, ignore\_permissions = ignore\_permissions, order\_by = order\_by, …).
- If custom.
  - Return transactions.
- Return post\_process(doctype, transactions).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L991) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1013)

<a id="op-fce41b9acdf8d9"></a>
### Get list for transactions

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_list_for_transactions`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, ignore\_permissions = false, fields = no value, order\_by = no value.

**Record and data access** read child\_doctype via get\_all · resolve a document from child\_doctype via get\_doc · read doctype via get\_list.

**Explicit results** data.

**Local steps**

- Bind dependencies get\_list.
- Set meta from Platform.get\_meta(doctype).
- Set data from list().
- Set or\_filters from list().
- For each d in get\_list(doctype, txt, filters = filters, fields = “name”, limit\_start = limit\_start, limit\_page\_length = limit\_page\_length, …).
  - Evaluate data.append(d).
- If txt.
  - If meta.get\_field(“items”).
    - If meta.get\_field(“items”).options.
      - Set child\_doctype from meta.get\_field(“items”).options.
      - For each item in Platform.get\_all(child\_doctype, mapping(“item\_name” → list(“like”, ((“%” + txt) + “%”)))).
        - Set child from Platform.get\_doc(child\_doctype, item.name).
        - Evaluate or\_filters.append(list(doctype, “name”, “=”, child.parent)).
- If or\_filters.
  - For each r in Platform.get\_list(doctype, fields = fields, filters = filters, or\_filters = or\_filters, limit\_start = limit\_start, …).
    - Evaluate data.append(r).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L1859) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1011)

<a id="op-ffb5658389bcd6"></a>
### Rfq transaction list

`operation_enterprise_controllers_website_list_for_contact_business_behavior_request_for_quotation_transaction_list`

**Inputs** parties\_doctype, doctype, parties, limit\_start, limit\_page\_length.

**Explicit results** post\_process(doctype, data).

**Local steps**

- Set party from Platform.qb.DocType(parties\_doctype).
- Set data from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(limit\_page\_length).offset(limit\_start).run(as\_dict = true).
- Return post\_process(doctype, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1019)

<a id="op-c8f6b1e69c5c29"></a>
### Post process

`operation_enterprise_controllers_website_list_for_contact_business_behavior_post_process`

**Inputs** doctype, data.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** result.

**Local steps**

- Set result from list().
- For each d in data.
  - Set doc from Platform.get\_doc(doctype, d.name).
  - Set doc.status\_percent from 0.
  - Set doc.status\_display from list().
  - If doc.get(“per\_billed”).
    - Update doc.status\_percent using + flt(doc.per\_billed).
    - Evaluate doc.status\_display.append(translated “Billed” when doc.per\_billed equals 100, otherwise translated “{0}% Billed”.format(doc.per\_billed)).
      - Value choice on doc.per\_billed equals 100 — true gives translated “Billed”, false gives translated “{0}% Billed”.format(doc.per\_billed).
  - If doc.get(“per\_delivered”).
    - Update doc.status\_percent using + flt(doc.per\_delivered, 2).
    - Evaluate doc.status\_display.append(translated “Delivered” when flt(doc.per\_delivered, 2) equals 100, otherwise translated “{0}% Delivered”.format(doc.per\_delivered)).
      - Value choice on flt(doc.per\_delivered, 2) equals 100 — true gives translated “Delivered”, false gives translated “{0}% Delivered”.format(doc.per\_delivered).
  - If hasattr(doc, “set\_indicator”).
    - Evaluate doc.set\_indicator().
  - Set doc.status\_display from “, ”.join(doc.status\_display).
  - Set doc.items\_preview from “, ”.join(generator of d.item\_name for d drawn from doc.items where d.item\_name).
    - Draw d from doc.items, keep a combination only if (d.item\_name).
  - Evaluate result.append(get\_portal\_row(doc)).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1018)

<a id="op-9f1c9c6b0f34bc"></a>
### Get portal row

`operation_enterprise_binding_enterprise_controllers_website_list_for_contact_get_portal_row`

**Inputs** doc.

**Record and data access** resolve a document from mapping(“doctype” → doc.doctype, expand mapping of f → doc.get(f) for f drawn from PORTAL\_ROW\_FIELDS) via get\_doc.

**Explicit results** row.

**Local steps**

- Set row from Platform.get\_doc(mapping(“doctype” → doc.doctype, expand mapping of f → doc.get(f) for f drawn from PORTAL\_ROW\_FIELDS)).
  - Draw f from PORTAL\_ROW\_FIELDS.
- For each key in PORTAL\_ROW\_DISPLAY\_KEYS.
  - Evaluate row.set(key, doc.get(key)).
- Return row.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L467)

<a id="op-06cf4c73a096ad"></a>
### Get customers suppliers

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_customers_suppliers`

**Inputs** doctype, user.

**Record and data access** read “Customer” via get\_list.

**Explicit results** tuple(customers when has\_customer\_field, otherwise no value, suppliers when has\_supplier\_field, otherwise no value).

**Local steps**

- Set customers from list().
- Set suppliers from list().
- Set meta from Platform.get\_meta(doctype).
- Set customer\_field\_name from get\_customer\_field\_name(doctype).
- Set has\_supplier\_field from meta.has\_field(“supplier”).
- Set has\_customer\_field from (meta.has\_field(customer\_field\_name) and not has\_supplier\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.has\_field(customer\_field\_name) → not has\_supplier\_field.
- If has\_common(list(“Supplier”, “Customer”), Platform.get\_roles(user)).
  - Set suppliers from get\_parents\_for\_user(“Supplier”, user).
  - Set customers from get\_parents\_for\_user(“Customer”, user).
- Otherwise.
  - If (Platform.has\_permission(doctype, “read”, user = user) and Platform.has\_permission(“Customer”, “read”, user = user)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(doctype, “read”, user = user) → Platform.has\_permission(“Customer”, “read”, user = user).
    - Set customer\_list from Platform.get\_list(“Customer”).
    - Set customers, suppliers from list of customer.name for customer drawn from customer\_list.
      - Draw customer from customer\_list.
- Return tuple(customers when has\_customer\_field, otherwise no value, suppliers when has\_supplier\_field, otherwise no value).
  - Value choice on has\_customer\_field — true gives customers, false gives no value.
  - Value choice on has\_supplier\_field — true gives suppliers, false gives no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(user), Platform.has\_permission(doctype, “read”, user = user) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1009)

<a id="op-762b48cb159d4d"></a>
### Get parents for user

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_parents_for_user`

**Inputs** parenttype, user = no value.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.user equals (nested operand in the contract or nested operand in the contract)).where(portal\_user.parentt ….

**Local steps**

- Set portal\_user from Platform.qb.DocType(“Portal User”).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.user equals (nested operand in the contract or nested operand in the contract)).where(portal\_user.parentt ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1012)

<a id="op-4a833aec810d80"></a>
### Has website permission

`operation_enterprise_controllers_website_list_for_contact_business_behavior_has_website_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, verbose.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1016)

<a id="op-bf3d8054c9275f"></a>
### Get customer filter

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_customer_filter`

**Inputs** doc, customers.

**Explicit results** filters.

**Local steps**

- Set doctype from doc.doctype.
- Set filters from Platform.\_dict().
- Set filters.name from doc.name.
- Set filters at get\_customer\_field\_name(doctype) from list(“in”, customers).
- If doctype equals “Quotation”.
  - Set filters.quotation\_to from “Customer”.
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L4624) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1008)

<a id="op-24ad6b58d20bf1"></a>
### Get customer field name

`operation_enterprise_controllers_website_list_for_contact_business_behavior_get_customer_field_name`

**Inputs** doctype.

**Explicit results** “party\_name” · “customer”.

**Local steps**

- If doctype equals “Quotation”.
  - Return “party\_name”.
- Otherwise.
  - Return “customer”.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L4828) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1007)

<a id="op-456aebb5dc077e"></a>
### Add role for portal user

`operation_enterprise_controllers_website_list_for_contact_business_behavior_add_role_for_portal_user`

**Inputs** portal\_user, role.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** msgprint with translated “Please add {1} role to user {0}.”.format(portal\_user.user, role) · msgprint with translated “Added {1} Role to User {0}.”.format(Platform.bold(user\_doc.name), role).

**Explicit results** no value.

**Local steps**

- If not portal\_user.is\_new().
  - Return no value.
- Set user\_doc from Platform.get\_doc(“User”, portal\_user.user).
- Set roles from set of r.role for r drawn from user\_doc.roles.
  - Draw r from user\_doc.roles.
- If role belongs to roles.
  - Return no value.
- If “System Manager” does not belong to Platform.get\_roles().
  - Evaluate Platform.msgprint(translated “Please add {1} role to user {0}.”.format(portal\_user.user, role), alert = true).
  - Return no value.
- Evaluate user\_doc.add\_roles(role).
- Evaluate Platform.msgprint(translated “Added {1} Role to User {0}.”.format(Platform.bold(user\_doc.name), role), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1006)

<a id="op-287e7dabba7ae4"></a>
### Link portal users to contacts

`operation_enterprise_controllers_website_list_for_contact_business_behavior_link_portal_users_to_contacts`

**Inputs** doc.

**Record and data access** resolve a document from “Contact” via get\_doc.

**State and service calls** call save on contact\_doc.

**Explicit results** no value.

**Local steps**

- Set portal\_users from set of p.user for p drawn from (doc.get(“portal\_users”) or list()) where p.user.
  - Draw p from (doc.get(“portal\_users”) or list()), keep a combination only if (p.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“portal\_users”) → list().
- If not portal\_users.
  - Return no value.
- Set before from doc.get\_doc\_before\_save().
- If before.
  - Set previous\_users from set of p.user for p drawn from (before.get(“portal\_users”) or list()) where p.user.
    - Draw p from (before.get(“portal\_users”) or list()), keep a combination only if (p.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in before.get(“portal\_users”) → list().
  - If portal\_users equals previous\_users.
    - Return no value.
- Set portal\_users from list(portal\_users).
- Set contact from Platform.qb.DocType(“Contact”).
- Set contact\_email from Platform.qb.DocType(“Contact Email”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(contact.name).distinct().
- Set conditions from list(contact.user.isin(portal\_users), Lower(contact.email\_id).isin(portal\_users), Lower(contact\_email.email\_id).isin(portal\_users)).
- Set query from query.where(Criterion.any(conditions)).
- Set contacts from query.run(pluck = true).
- If not contacts.
  - Return no value.
- Set dynamic\_link from Platform.qb.DocType(“Dynamic Link”).
- Set existing\_links from nested operand in the contract(nested operand in the contract).select(dynamic\_link.parent).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the co ….
- Set contacts\_to\_link from list of name for name drawn from contacts where name does not belong to existing\_links.
  - Draw name from contacts, keep a combination only if (name does not belong to existing\_links).
- For each name in contacts\_to\_link.
  - Set contact\_doc from Platform.get\_doc(“Contact”, name).
  - If not contact\_doc.has\_link(doc.doctype, doc.name).
    - Evaluate contact\_doc.append(“links”, mapping(“link\_doctype” → doc.doctype, “link\_name” → doc.name)).
    - Evaluate contact\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L5318) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1017)
