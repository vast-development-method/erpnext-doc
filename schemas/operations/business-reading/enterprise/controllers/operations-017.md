# Shared transaction rules · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Queries

<a id="op-54d30caa375c7c"></a>
### Get empty batches

`operation_enterprise_controllers_queries_business_behavior_get_empty_batches`

**Inputs** filters, start, page\_len, filtered\_batches = no value, txt = no value.

**Record and data access** read “Batch” via get\_all.

**Explicit results** Platform.get\_all(“Batch”, fields = list(“name”, “batch\_qty”), filters = query\_filter, limit\_start = start, limit\_page\_length = page\_len, …).

**Local steps**

- Set query\_filter from mapping(“item” → filters.get(“item\_code”), “disabled” → 0).
- If txt.
  - Set query\_filter at “name” from tuple(“like”, formatted text %{txt}%).
- Set exclude\_batches from list of batch at 0 for batch drawn from filtered\_batches when filtered\_batches, otherwise list().
  - Value choice on filtered\_batches — true gives list of batch at 0 for batch drawn from filtered\_batches, false gives list().
  - Draw batch from filtered\_batches.
- If exclude\_batches.
  - Set query\_filter at “name” from tuple(“not in”, exclude\_batches).
- Return Platform.get\_all(“Batch”, fields = list(“name”, “batch\_qty”), filters = query\_filter, limit\_start = start, limit\_page\_length = page\_len, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0379.json#L1279) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L491)

<a id="op-e1d35cdc8be7b2"></a>
### Get filterd batches

`operation_enterprise_controllers_queries_business_behavior_get_filterd_batches`

**Inputs** data.

**Explicit results** filterd\_batch.

**Local steps**

- Set batches from OrderedDict().
- For each batch\_data in data.
  - If batch\_data at 0 does not belong to batches.
    - Set batches at batch\_data at 0 from list(batch\_data).
  - Otherwise.
    - Update batches at batch\_data at 0 at 1 using + batch\_data at 1.
- Set filterd\_batch from list().
- For each tuple(\_batch, batch\_data) in batches.items().
  - If batch\_data at 1 &gt; 0.
    - Evaluate filterd\_batch.append(tuple(batch\_data)).
- Return filterd\_batch.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0379.json#L1664) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L494)

<a id="op-1e80980582a9e6"></a>
### Get batches from stock ledger entries

`operation_enterprise_controllers_queries_business_behavior_get_batches_from_stock_ledger_entries`

**Inputs** searchfields, txt, filters, start = 0, page\_len = 100.

**Explicit results** (query.run(as\_list = 1) or list()).

**Local steps**

- Set stock\_ledger\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch\_table from Platform.qb.DocType(“Batch”).
- Set expiry\_date from (filters.get(“posting\_date”) or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“posting\_date”) → today().
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).having(nested operand in the contract(nested operand in the contract) differs from 0).offset(start).limit(page\_len).
- If not filters.get(“is\_inward”).
  - If (filters.get(“posting\_date”) and filters.get(“posting\_time”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“posting\_date”) → filters.get(“posting\_time”).
    - Set query from query.where(stock\_ledger\_entry.posting\_datetime ≤ get\_combine\_datetime(filters.get(“posting\_date”), filters.get(“posting\_time”))).
- If not filters.get(“include\_expired\_batches”).
  - Set query from query.where((batch\_table.expiry\_date ≥ expiry\_date bitwise or batch\_table.expiry\_date.isnull())).
- Set query from query.select(Concat(“MFG-”, batch\_table.manufacturing\_date).as\_(“manufacturing\_date”), Concat(“EXP-”, batch\_table.expiry\_date).as\_(“expiry\_date”)).
- If filters.get(“warehouse”).
  - Set query from query.where(stock\_ledger\_entry.warehouse equals filters.get(“warehouse”)).
- For each field in searchfields.
  - Set query from query.select(batch\_table at field).
- If txt.
  - Set txt\_condition from batch\_table.name.like(formatted text %{txt}%).
  - For each field in list(expanded searchfields, “name”).
    - Update txt\_condition using bitwise or batch\_table at field.like(formatted text %{txt}%).
  - Set query from query.where(txt\_condition).
- Return (query.run(as\_list = 1) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_list = 1) → list().

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L488)

<a id="op-f4fd8db884d2f7"></a>
### Get batches from serial and batch bundle

`operation_enterprise_controllers_queries_business_behavior_get_batches_from_serial_and_batch_bundle`

**Inputs** searchfields, txt, filters, start = 0, page\_len = 100.

**Explicit results** bundle\_query.run(as\_list = 1).

**Local steps**

- Set bundle from Platform.qb.DocType(“Serial and Batch Entry”).
- Set stock\_ledger\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch\_table from Platform.qb.DocType(“Batch”).
- Set expiry\_date from (filters.get(“posting\_date”) or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“posting\_date”) → today().
- Set bundle\_query from nested operand in the contract(nested operand in the contract, nested operand in the contract).having(nested operand in the contract(nested operand in the contract) differs from 0).offset(start).limit(page\_len).
- If not filters.get(“is\_inward”).
  - If (filters.get(“posting\_date”) and filters.get(“posting\_time”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“posting\_date”) → filters.get(“posting\_time”).
    - Set bundle\_query from bundle\_query.where(stock\_ledger\_entry.posting\_datetime ≤ get\_combine\_datetime(filters.get(“posting\_date”), filters.get(“posting\_time”))).
- If not filters.get(“include\_expired\_batches”).
  - Set bundle\_query from bundle\_query.where((batch\_table.expiry\_date ≥ expiry\_date bitwise or batch\_table.expiry\_date.isnull())).
- Set bundle\_query from bundle\_query.select(Concat(“MFG-”, batch\_table.manufacturing\_date), Concat(“EXP-”, batch\_table.expiry\_date)).
- If filters.get(“warehouse”).
  - Set bundle\_query from bundle\_query.where(stock\_ledger\_entry.warehouse equals filters.get(“warehouse”)).
- For each field in searchfields.
  - Set bundle\_query from bundle\_query.select(batch\_table at field).
- If txt.
  - Set txt\_condition from batch\_table.name.like(formatted text %{txt}%).
  - For each field in list(expanded searchfields, “name”).
    - Update txt\_condition using bitwise or batch\_table at field.like(formatted text %{txt}%).
  - Set bundle\_query from bundle\_query.where(txt\_condition).
- Return bundle\_query.run(as\_list = 1).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L487)

<a id="op-8fdcc04c766aac"></a>
### Get account list

`operation_enterprise_controllers_queries_business_behavior_get_account_list`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** Platform.desk.reportview.execute(doctype, filters = filter\_list, fields = list(“name”, “parent\_account”), limit\_start = start, limit\_page\_length = page\_len, …).

**Local steps**

- Set doctype from “Account”.
- Set filter\_list from list().
- If isinstance(filters, dict).
  - For each tuple(key, val) in filters.items().
    - If isinstance(val, (list bitwise or tuple)).
      - Evaluate filter\_list.append(list(doctype, key, val at 0, val at 1)).
    - Otherwise.
      - Evaluate filter\_list.append(list(doctype, key, “=”, val)).
- Otherwise.
  - If isinstance(filters, list).
    - Evaluate filter\_list.extend(filters).
- If “is\_group” does not belong to list of d at 1 for d drawn from filter\_list.
  - Draw d from filter\_list.
  - Evaluate filter\_list.append(list(“Account”, “is\_group”, “=”, “0”)).
- If (searchfield and txt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in searchfield → txt.
  - Evaluate filter\_list.append(list(doctype, searchfield, “like”, (“%%%s%%” modulo or format txt))).
- Return Platform.desk.reportview.execute(doctype, filters = filter\_list, fields = list(“name”, “parent\_account”), limit\_start = start, limit\_page\_length = page\_len, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L803) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L484)

<a id="op-d1675cf17696a2"></a>
### Get blanket orders

`operation_enterprise_controllers_queries_business_behavior_get_blanket_orders`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Blanket Order Item” via get\_all · read “Blanket Order” via get\_list.

**Explicit results** Platform.get\_list(“Blanket Order”, filters = bo\_filters, fields = list(“name”, “blanket\_order\_type”, “to\_date”), group\_by = “name”, as\_list = true).

**Local steps**

- Set bo\_filters from list(list(“docstatus”, “=”, 1), list(“blanket\_order\_type”, “=”, filters.get(“blanket\_order\_type”)), list(“company”, “=”, filters.get(“company”))).
- If Platform.has\_permission(“Blanket Order”, “read”).
  - Evaluate bo\_filters.append(list(“Blanket Order Item”, “item\_code”, “=”, filters.get(“item”))).
- Otherwise.
  - Set parents from Platform.get\_all(“Blanket Order Item”, filters = mapping(“item\_code” → filters.get(“item”), “parenttype” → “Blanket Order”), pluck = “parent”, distinct = true).
  - Evaluate bo\_filters.append(list(“name”, “in”, (parents or list(empty text)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parents → list(empty text).
- If currency bound to filters.get(“currency”).
  - Evaluate bo\_filters.append(list(“currency”, “=”, currency)).
- Return Platform.get\_list(“Blanket Order”, filters = bo\_filters, fields = list(“name”, “blanket\_order\_type”, “to\_date”), group\_by = “name”, as\_list = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Blanket Order”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L489)

<a id="op-2d6e6302319bf9"></a>
### Get income account

`operation_enterprise_controllers_queries_business_behavior_get_income_account`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(acc.idx, order = Order.desc).orderby(acc.name).run().

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set dt from “Account”.
- Set acc from qb.DocType(dt).
- Set condition from list((acc.report\_type.eq(“Profit and Loss”) bitwise or acc.account\_type.isin(list(“Income Account”, “Temporary”))), acc.is\_group.eq(0), acc.disabled.eq(0)).
- If txt.
  - Evaluate condition.append(acc.name.like(formatted text %{txt}%)).
- If filters.get(“company”).
  - Evaluate condition.append(acc.company.eq(filters.get(“company”))).
- Return nested operand in the contract(nested operand in the contract).orderby(acc.idx, order = Order.desc).orderby(acc.name).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L497)

<a id="op-e0271fd646ddb2"></a>
### Get filtered dimensions

`operation_enterprise_controllers_queries_business_behavior_get_filtered_dimensions`

**Inputs** doctype, txt, searchfield, start, page\_len, filters, reference\_doctype = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read doctype via get\_list.

**Explicit results** list of tuple(d) for d drawn from set(output).

**Local steps**

- Bind dependencies get\_dimension\_filter\_map.
- Set dimension\_filters from get\_dimension\_filter\_map().
- Set dimension\_filters from dimension\_filters.get(tuple(filters.get(“dimension”), filters.get(“account”))).
- Set query\_filters from list().
- Set or\_filters from list().
- Set fields from list(“name”).
- Set searchfields from Platform.get\_meta(doctype).get\_search\_fields().
- Set meta from Platform.get\_meta(doctype).
- If (meta.is\_tree and meta.has\_field(“is\_group”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.is\_tree → meta.has\_field(“is\_group”).
  - Evaluate query\_filters.append(list(“is\_group”, “=”, 0)).
- If meta.has\_field(“disabled”).
  - Evaluate query\_filters.append(list(“disabled”, “!=”, 1)).
- If meta.has\_field(“company”).
  - Evaluate query\_filters.append(list(“company”, “=”, filters.get(“company”))).
- For each field in searchfields.
  - Evaluate or\_filters.append(list(field, “LIKE”, (“%%%s%%” modulo or format txt))).
  - Evaluate fields.append(field).
- If dimension\_filters.
  - If dimension\_filters at “allow\_or\_restrict” equals “Allow”.
    - Set query\_selector from “in”.
  - Otherwise.
    - Set query\_selector from “not in”.
  - If len(dimension\_filters at “allowed\_dimensions”) equals 1.
    - Set dimensions from tuple((dimension\_filters at “allowed\_dimensions” × 2)).
  - Otherwise.
    - Set dimensions from tuple(dimension\_filters at “allowed\_dimensions”).
  - Evaluate query\_filters.append(list(“name”, query\_selector, dimensions)).
- Set output from Platform.get\_list(doctype, fields = fields, filters = query\_filters, or\_filters = or\_filters, as\_list = 1, …).
- Return list of tuple(d) for d drawn from set(output).
  - Draw d from set(output).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L496)

<a id="op-2fba69ea969970"></a>
### Get expense account

`operation_enterprise_controllers_queries_business_behavior_get_expense_account`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** nested operand in the contract.qb.get\_query(dt, fields = list(“name”), ignore\_permissions = false).where(Criterion.all(condition)).run().

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set dt from “Account”.
- Set acc from qb.DocType(dt).
- Set condition from list((acc.report\_type.eq(“Profit and Loss”) bitwise or acc.account\_type.isin(list(“Expense Account”, “Fixed Asset”, “Temporary”, “Asset Received But Not Billed”, …))), acc.is\_group.eq(0), acc.disabled.eq(0)).
- If txt.
  - Evaluate condition.append(acc.name.like(formatted text %{txt}%)).
- If filters.get(“company”).
  - Evaluate condition.append(acc.company.eq(filters.get(“company”))).
- Return nested operand in the contract.qb.get\_query(dt, fields = list(“name”), ignore\_permissions = false).where(Criterion.all(condition)).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L492)

<a id="op-b3ebc50665a9ed"></a>
### Warehouse query

`operation_enterprise_controllers_queries_business_behavior_warehouse_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(query).

**Local steps**

- Set doctype from “Warehouse”.
- Set tuple(conditions, bin\_conditions) from tuple(list(), list()).
- Set filter\_dict from get\_doctype\_wise\_filters(filters).
- Set warehouse\_field from “name”.
- Set meta from Platform.get\_meta(“Warehouse”).
- If (meta.get(“show\_title\_field\_in\_link”) and meta.get(“title\_field”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.get(“show\_title\_field\_in\_link”) → meta.get(“title\_field”).
  - Set searchfield from meta.get(“title\_field”).
  - Set warehouse\_field from meta.get(“title\_field”).
- Set tuple(stock\_column, bin\_join, stock\_order) from tuple(empty text, empty text, empty text).
- If Platform.has\_permission(“Bin”, “read”).
  - Set stock\_column from “, CONCAT\_WS(' : ', 'Actual Qty', ifnull(round(′tabBin′.actual\_qty, 2), 0 )) actual\_qty”.
  - Set bin\_join from (“left join ′tabBin′ on ′tabBin′.warehouse = ′tabWarehouse′.name ” + get\_filters\_cond(doctype, filter\_dict.get(“Bin”), bin\_conditions, ignore\_permissions = true)).
  - Set stock\_order from “ifnull(′tabBin′.actual\_qty, 0) desc,”.
- Set query from query text (SELECT, Warehouse).format(warehouse\_field = warehouse\_field, stock\_column = stock\_column, bin\_join = bin\_join, stock\_order = stock\_order, …).
- Return Platform.db.sql(query).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bin”, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L833) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L514)

<a id="op-60d23569d5be16"></a>
### Get doctype wise filters

`operation_enterprise_controllers_queries_business_behavior_get_record_type_wise_filters`

**Inputs** filters.

**Explicit results** filter\_dict.

**Local steps**

- Set filter\_dict from defaultdict(list).
- For each row in filters.
  - Evaluate filter\_dict at row at 0.append(row).
- Return filter\_dict.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0380.json#L2735) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L503)

<a id="op-29b895d3a87bf8"></a>
### Get batch numbers

`operation_enterprise_controllers_queries_business_behavior_get_batch_numbers`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Batch” via get\_list.

**Explicit results** Platform.get\_list(“Batch”, filters = batch\_filters, or\_filters = list(list(“expiry\_date”, “is”, “not set”), list(“expiry\_date”, “&gt;=”, today())), fields = list(“batch\_id”), order\_by = “batch\_id”, …).

**Local steps**

- Set batch\_filters from list(list(“disabled”, “=”, 0), list(“name”, “like”, formatted text %{txt}%)).
- If (filters and filters.get(“item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“item”).
  - Evaluate batch\_filters.append(list(“item”, “=”, filters.get(“item”))).
- Return Platform.get\_list(“Batch”, filters = batch\_filters, or\_filters = list(list(“expiry\_date”, “is”, “not set”), list(“expiry\_date”, “&gt;=”, today())), fields = list(“batch\_id”), order\_by = “batch\_id”, …).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L486)

<a id="op-f733d6856220c3"></a>
### Item manufacturer query

`operation_enterprise_controllers_queries_business_behavior_item_manufacturer_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Item Manufacturer” via get\_all.

**Explicit results** list() · item\_manufacturers.

**Local steps**

- Set item\_code from filters.get(“item\_code”).
- If (not item\_code or not isinstance(item\_code, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_code → not isinstance(item\_code, str).
  - Return list().
- Evaluate Platform.has\_permission(“Item”, “read”, item\_code, throw = true).
- Set item\_filters from list(list(“manufacturer”, “like”, ((“%” + txt) + “%”)), list(“item\_code”, “=”, item\_code)).
- Set item\_manufacturers from Platform.get\_all(“Item Manufacturer”, fields = list(“manufacturer”, “manufacturer\_part\_no”), filters = item\_filters, limit\_start = start, limit\_page\_length = page\_len, …).
- Return item\_manufacturers.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, item\_code, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L827) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L508)

<a id="op-8e676e22b31b19"></a>
### Get purchase receipts

`operation_enterprise_controllers_queries_business_behavior_get_purchase_receipts`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Purchase Receipt Item” via get\_all · read “Purchase Receipt” via get\_list.

**Explicit results** Platform.get\_list(“Purchase Receipt”, filters = pr\_filters, fields = list(“name”), group\_by = “name”, order\_by = “name”, …).

**Local steps**

- Set pr\_filters from list(list(“docstatus”, “=”, 1), list(“name”, “like”, formatted text %{txt}%)).
- If (filters and filters.get(“item\_code”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“item\_code”).
  - If Platform.has\_permission(“Purchase Receipt”, “read”).
    - Evaluate pr\_filters.append(list(“Purchase Receipt Item”, “item\_code”, “=”, filters.get(“item\_code”))).
  - Otherwise.
    - Set parents from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“item\_code” → filters.get(“item\_code”), “parenttype” → “Purchase Receipt”), pluck = “parent”, distinct = true).
    - Evaluate pr\_filters.append(list(“name”, “in”, (parents or list(empty text)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in parents → list(empty text).
- Return Platform.get\_list(“Purchase Receipt”, filters = pr\_filters, fields = list(“name”), group\_by = “name”, order\_by = “name”, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Receipt”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L502)

<a id="op-ed0431426321d9"></a>
### Get purchase invoices

`operation_enterprise_controllers_queries_business_behavior_get_purchase_invoices`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Purchase Invoice Item” via get\_all · read “Purchase Invoice” via get\_list.

**Explicit results** Platform.get\_list(“Purchase Invoice”, filters = pi\_filters, fields = list(“name”), group\_by = “name”, order\_by = “name”, …).

**Local steps**

- Set pi\_filters from list(list(“docstatus”, “=”, 1), list(“name”, “like”, formatted text %{txt}%)).
- If (filters and filters.get(“item\_code”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“item\_code”).
  - If Platform.has\_permission(“Purchase Invoice”, “read”).
    - Evaluate pi\_filters.append(list(“Purchase Invoice Item”, “item\_code”, “=”, filters.get(“item\_code”))).
  - Otherwise.
    - Set parents from Platform.get\_all(“Purchase Invoice Item”, filters = mapping(“item\_code” → filters.get(“item\_code”), “parenttype” → “Purchase Invoice”), pluck = “parent”, distinct = true).
    - Evaluate pi\_filters.append(list(“name”, “in”, (parents or list(empty text)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in parents → list(empty text).
- Return Platform.get\_list(“Purchase Invoice”, filters = pi\_filters, fields = list(“name”), group\_by = “name”, order\_by = “name”, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Invoice”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L501)

<a id="op-acdc9d2fa34e69"></a>
### Get doctypes for closing

`operation_enterprise_controllers_queries_business_behavior_get_record_types_for_closing`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list of tuple(d) for d drawn from set(doctypes).

**Local steps**

- Set doctypes from Platform.get\_hooks(“period\_closing\_doctypes”).
- If txt.
  - Set doctypes from list of d for d drawn from doctypes where txt.lower() belongs to d.lower().
    - Draw d from doctypes, keep a combination only if (txt.lower() belongs to d.lower()).
- Return list of tuple(d) for d drawn from set(doctypes).
  - Draw d from set(doctypes).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“period\_closing\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L504)

<a id="op-6eeb7e42f2a154"></a>
### Get tax template

`operation_enterprise_controllers_queries_business_behavior_get_tax_template`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · resolve a document from “Item Group” via get\_cached\_doc · read “Item Tax Template” via get\_list.

**Explicit results** Platform.get\_list(“Item Tax Template”, filters = mapping(“disabled” → 0, “company” → company), or\_filters = or\_filters, as\_list = true) · list() · Platform.get\_list(“Item Tax Template”, filters = mapping(“name” → list(“in”, templates)), as\_list = true).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid Item Code or Item Group”.

**Local steps**

- Set item\_code from filters.get(“item\_code”).
- Set item\_group from filters.get(“item\_group”).
- If (not isinstance(item\_code, str) or not isinstance(item\_group, (str bitwise or no value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(item\_code, str) → not isinstance(item\_group, (str bitwise or no value)).
  - Call the validation error handler Platform.throw(translated “Invalid Item Code or Item Group”, Platform.PermissionError).
- Evaluate Platform.has\_permission(“Item”, “read”, item\_code, throw = true).
- Set item\_doc from Platform.get\_cached\_doc(“Item”, item\_code).
- Set company from filters.get(“company”).
- Set taxes from (item\_doc.taxes or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_doc.taxes → list().
- While item\_group.
  - Set item\_group\_doc from Platform.get\_cached\_doc(“Item Group”, item\_group).
  - Update taxes using + (item\_group\_doc.taxes or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_group\_doc.taxes → list().
  - Set item\_group from item\_group\_doc.parent\_item\_group.
- If not taxes.
  - Set or\_filters from list().
  - If txt.
    - Set search\_fields from list(“name”).
    - Set tax\_template\_doc from Platform.get\_meta(“Item Tax Template”).
    - If title\_field bound to tax\_template\_doc.title\_field.
      - Evaluate search\_fields.append(title\_field).
    - If tax\_template\_doc.search\_fields.
      - Evaluate search\_fields.extend(tax\_template\_doc.get\_search\_fields()).
    - For each f in search\_fields.
      - Evaluate or\_filters.append(list(doctype, f.strip(), “like”, formatted text %{txt}%)).
  - Return Platform.get\_list(“Item Tax Template”, filters = mapping(“disabled” → 0, “company” → company), or\_filters = or\_filters, as\_list = true).
- Otherwise.
  - Set valid\_from from filters.get(“valid\_from”).
  - Set valid\_from from valid\_from at 1 when isinstance(valid\_from, list), otherwise valid\_from.
    - Value choice on isinstance(valid\_from, list) — true gives valid\_from at 1, false gives valid\_from.
  - Set ctx from ItemDetailsCtx(mapping(“item\_code” → item\_code, “posting\_date” → valid\_from, “tax\_category” → filters.get(“tax\_category”), “company” → company, …)).
  - Set taxes from \_get\_item\_tax\_template(ctx, taxes, for\_validate = true).
  - Set txt from txt.lower().
  - Set templates from list of d for d drawn from set(taxes) where (not txt or txt belongs to d.lower()).
    - Draw d from set(taxes), keep a combination only if ((not txt or txt belongs to d.lower())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not txt → txt belongs to d.lower().
  - If not templates.
    - Return list().
  - Return Platform.get\_list(“Item Tax Template”, filters = mapping(“name” → list(“in”, templates)), as\_list = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, item\_code, throw = true) · configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code), Platform.get\_cached\_doc(“Item Group”, item\_group).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L824) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L505)

<a id="op-810a5da0602466"></a>
### Get fields

`operation_enterprise_controllers_queries_business_behavior_get_fields`

**Inputs** doctype, fields = no value.

**State and service calls** call insert on fields.

**Explicit results** unique(fields).

**Local steps**

- If fields is identical to no value.
  - Set fields from list().
- Set meta from Platform.get\_meta(doctype).
- Evaluate fields.extend(meta.get\_search\_fields()).
- If (meta.title\_field and meta.title\_field.strip() does not belong to fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.title\_field → meta.title\_field.strip() does not belong to fields.
  - Evaluate fields.insert(1, meta.title\_field.strip()).
- Return unique(fields).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0380.json#L6269) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L493)

<a id="op-50e1aba8e18ee0"></a>
### Get payment terms for references

`operation_enterprise_controllers_queries_business_behavior_get_payment_terms_for_references`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Record and data access** read “Payment Schedule” via get\_value · read “Payment Schedule” via get\_all.

**Explicit results** terms.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid reference”.

**Local steps**

- Set terms from list().
- If filters.
  - Set reference from filters.get(“reference”).
  - If not reference.
    - Return terms.
  - If not isinstance(reference, str).
    - Call the validation error handler Platform.throw(translated “Invalid reference”, Platform.PermissionError).
  - Set parenttype from (filters.get(“reference\_doctype”) or Platform.db.get\_value(“Payment Schedule”, mapping(“parent” → reference), “parenttype”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“reference\_doctype”) → Platform.db.get\_value(“Payment Schedule”, mapping(“parent” → reference), “parenttype”).
  - If not parenttype.
    - Return terms.
  - Evaluate Platform.has\_permission(parenttype, doc = reference, throw = true).
  - Set terms from Platform.db.get\_all(“Payment Schedule”, filters = mapping(“parent” → reference, “parenttype” → parenttype), fields = list(“payment\_term”), limit = page\_len, as\_list = 1).
- Return terms.

**Values supplied outside this operation** effective access from Platform.has\_permission(parenttype, doc = reference, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L499)

<a id="op-5e828a1e3f7ab1"></a>
### Get filtered child rows

`operation_enterprise_controllers_queries_business_behavior_get_filtered_child_rows`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Record and data access** read doctype via get\_value · read parenttype via exists.

**Explicit results** list() · query.run(as\_dict = false).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Parent document is required to search child rows” · validation helper with Platform.PermissionError — translated “{0} is not a child table”.format(doctype).

**Local steps**

- Set parent from filters.get(“parent”) when filters, otherwise no value.
  - Value choice on filters — true gives filters.get(“parent”), false gives no value.
- If (not parent or not isinstance(parent, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → not isinstance(parent, str).
  - Call the validation error handler Platform.throw(translated “Parent document is required to search child rows”, Platform.PermissionError).
- If not Platform.get\_meta(doctype).istable.
  - Call the validation error handler Platform.throw(translated “{0} is not a child table”.format(doctype), Platform.PermissionError).
- Set parenttype from Platform.db.get\_value(doctype, mapping(“parent” → parent), “parenttype”).
- If (not parenttype or not Platform.db.exists(parenttype, parent)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parenttype → not Platform.db.exists(parenttype, parent).
  - Return list().
- Evaluate Platform.has\_permission(doctype, parent\_doctype = parenttype, throw = true).
- Evaluate Platform.has\_permission(parenttype, doc = parent, throw = true).
- Set table from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract(nested operand in the contract).orderby(table.idx).offset(start).limit(page\_len).
- If txt.
  - Update txt using + “%”.
  - Set query from query.where(((table.idx.like(txt.replace(“#”, empty text)) bitwise or table.item\_code.like(txt)) bitwise or table.name.like(txt))).
- Return query.run(as\_dict = false).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, parent\_doctype = parenttype, throw = true), Platform.has\_permission(parenttype, doc = parent, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L495)

<a id="op-396eae3a36bb43"></a>
### Get item uom query

`operation_enterprise_controllers_queries_business_behavior_get_item_unit_of_measure_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Item” via get\_list · read “UOM Conversion Detail” via get\_all · read “UOM” via get\_list.

**Explicit results** list() · Platform.get\_all(“UOM Conversion Detail”, filters = query\_filters, fields = list(“uom”, “conversion\_factor”), limit\_start = start, limit\_page\_length = page\_len, …) · Platform.get\_list(“UOM”, filters = mapping(“name” → list(“like”, formatted text %{txt}%), “enabled” → 1), fields = list(“name”), limit\_start = start, limit\_page\_length = page\_len, …).

**Local steps**

- If Platform.get\_single\_value(“Stock Settings”, “allow\_uom\_with\_conversion\_rate\_defined\_in\_item”).
  - Set item\_code from filters.get(“item\_code”).
  - If (not item\_code or not Platform.get\_list(“Item”, filters = list(list(“name”, “=”, item\_code)), pluck = “name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_code → not Platform.get\_list(“Item”, filters = list(list(“name”, “=”, item\_code)), pluck = “name”).
    - Return list().
  - Set query\_filters from mapping(“parent” → item\_code, “parenttype” → “Item”).
  - If txt.
    - Set query\_filters at “uom” from list(“like”, formatted text %{txt}%).
  - Return Platform.get\_all(“UOM Conversion Detail”, filters = query\_filters, fields = list(“uom”, “conversion\_factor”), limit\_start = start, limit\_page\_length = page\_len, …).
- Return Platform.get\_list(“UOM”, filters = mapping(“name” → list(“like”, formatted text %{txt}%), “enabled” → 1), fields = list(“name”), limit\_start = start, limit\_page\_length = page\_len, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_uom\_with\_conversion\_rate\_defined\_in\_item”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L498)

<a id="op-fe45d96de55e3b"></a>
### Get warehouse address

`operation_enterprise_controllers_queries_business_behavior_get_warehouse_address`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list() · query.run(as\_list = 1).

**Local steps**

- Set warehouse from filters.get(“warehouse”).
- If (not warehouse or not isinstance(warehouse, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not warehouse → not isinstance(warehouse, str).
  - Return list().
- Evaluate Platform.has\_permission(“Warehouse”, “read”, warehouse, throw = true).
- Set table from Platform.qb.DocType(doctype).
- Set child\_table from Platform.qb.DocType(“Dynamic Link”).
- Set query from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand i ….
- Return query.run(as\_list = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Warehouse”, “read”, warehouse, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L825) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L506)

## Service · Sales and purchase return

<a id="op-7b9846c68a1718"></a>
### Validate return

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_validate_return`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If (not doc.meta.get\_field(“is\_return”) or not doc.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.meta.get\_field(“is\_return”) → not doc.is\_return.
  - Return no value.
- If doc.return\_against.
  - Evaluate validate\_return\_against(doc).
  - Evaluate validate\_returned\_items(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0381.json#L1086) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L547)

<a id="op-458313e3ebf057"></a>
### Validate return against

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_validate_return_against`

**Inputs** doc.

**Record and data access** read doc.doctype via exists · resolve a document from doc.doctype via get\_doc.

**Explicit failure paths** validation helper — translated “Invalid {0}: {1}”.format(doc.meta.get\_label(“return\_against”), doc.return\_against) · validation helper — translated “The {0} {1} does not match with the {0} {2} in the {3} {4}”.format(doc.meta.get\_label(party\_type), bold(doc.get(party\_type)), bold(ref\_doc.get(party\_type)), ref\_doc.doctype, …) · validation helper — translated “Posting timestamp must be after {0}”.format(format\_datetime(ref\_posting\_datetime)) · validation helper — translated “Exchange Rate must be same as {0} {1} ({2})”.format(doc.doctype, doc.return\_against, ref\_doc.conversion\_rate) · validation helper — translated “'Update Stock' can not be checked because items are not delivered via {0}”.format(doc.return\_against).

**Local steps**

- If not Platform.db.exists(doc.doctype, doc.return\_against).
  - Call the validation error handler Platform.throw(translated “Invalid {0}: {1}”.format(doc.meta.get\_label(“return\_against”), doc.return\_against)).
- Otherwise.
  - Set ref\_doc from Platform.get\_doc(doc.doctype, doc.return\_against).
  - Set party\_type from “customer” when doc.doctype belongs to tuple(“Sales Invoice”, “Delivery Note”), otherwise “supplier”.
    - Value choice on doc.doctype belongs to tuple(“Sales Invoice”, “Delivery Note”) — true gives “customer”, false gives “supplier”.
  - If ref\_doc.get(party\_type) differs from doc.get(party\_type).
    - Call the validation error handler Platform.throw(translated “The {0} {1} does not match with the {0} {2} in the {3} {4}”.format(doc.meta.get\_label(party\_type), bold(doc.get(party\_type)), bold(ref\_doc.get(party\_type)), ref\_doc.doctype, …),  ….
  - If (ref\_doc.company equals doc.company and ref\_doc.get(party\_type) equals doc.get(party\_type) and ref\_doc.docstatus.is\_submitted()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doc.company equals doc.company → ref\_doc.get(party\_type) equals doc.get(party\_type) → ref\_doc.docstatus.is\_submitted().
    - Set return\_posting\_datetime from “{} {}”.format(doc.posting\_date, (doc.get(“posting\_time”) or “00:00:00”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“posting\_time”) → “00:00:00”.
    - Set ref\_posting\_datetime from “{} {}”.format(ref\_doc.posting\_date, (ref\_doc.get(“posting\_time”) or “00:00:00”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“posting\_time”) → “00:00:00”.
    - If get\_datetime(return\_posting\_datetime) &lt; get\_datetime(ref\_posting\_datetime).
      - Call the validation error handler Platform.throw(translated “Posting timestamp must be after {0}”.format(format\_datetime(ref\_posting\_datetime))).
    - If doc.get(“conversion\_rate”) differs from ref\_doc.get(“conversion\_rate”).
      - Call the validation error handler Platform.throw(translated “Exchange Rate must be same as {0} {1} ({2})”.format(doc.doctype, doc.return\_against, ref\_doc.conversion\_rate)).
    - If (doc.doctype equals “Sales Invoice” and doc.update\_stock and not ref\_doc.update\_stock).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Sales Invoice” → doc.update\_stock → not ref\_doc.update\_stock.
      - Call the validation error handler Platform.throw(translated “'Update Stock' can not be checked because items are not delivered via {0}”.format(doc.return\_against)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L867) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L548)
