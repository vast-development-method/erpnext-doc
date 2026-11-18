# Inventory and warehouses · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Item where used

<a id="op-752ad635d31b2c"></a>
### Get bom map

`operation_enterprise_stock_report_item_where_used_business_behavior_get_bill_of_materials_map`

**Inputs** bom\_names, company = no value.

**Explicit results** mapping() · mapping of row.name → row for row drawn from get\_permitted\_list(“BOM”, filters = filters, fields = list(“name”, “item”, “company”, “is\_default”, …)).

**Local steps**

- Set bom\_names from get\_unique\_names(bom\_names).
- If not bom\_names.
  - Return mapping().
- Set filters from mapping(“name” → list(“in”, bom\_names), “docstatus” → 1).
- If company.
  - Set filters at “company” from company.
- Return mapping of row.name → row for row drawn from get\_permitted\_list(“BOM”, filters = filters, fields = list(“name”, “item”, “company”, “is\_default”, …)).
  - Draw row from get\_permitted\_list(“BOM”, filters = filters, fields = list(“name”, “item”, “company”, “is\_default”, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L202)

<a id="op-f893066962234d"></a>
### Get product bundle map

`operation_enterprise_stock_report_item_where_used_business_behavior_get_product_bundle_map`

**Inputs** bundle\_names.

**Explicit results** mapping() · mapping of row.name → row for row drawn from get\_permitted\_list(“Product Bundle”, filters = mapping(“name” → list(“in”, bundle\_names), “docstatus” → 0), fields = list(“name”, “new\_item\_code”, “disabled”)).

**Local steps**

- Set bundle\_names from get\_unique\_names(bundle\_names).
- If not bundle\_names.
  - Return mapping().
- Return mapping of row.name → row for row drawn from get\_permitted\_list(“Product Bundle”, filters = mapping(“name” → list(“in”, bundle\_names), “docstatus” → 0), fields = list(“name”, “new\_item\_code”, “disabled”)).
  - Draw row from get\_permitted\_list(“Product Bundle”, filters = mapping(“name” → list(“in”, bundle\_names), “docstatus” → 0), fields = list(“name”, “new\_item\_code”, “disabled”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L209)

<a id="op-88503e49ee497b"></a>
### Build row

`operation_enterprise_stock_report_item_where_used_business_behavior_build_row`

**Inputs** remaining named values kwargs.

**Explicit results** Platform.\_dict(kwargs).

**Local steps**

- Return Platform.\_dict(kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0896.json#L2795) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L198)

<a id="op-2ca95460986135"></a>
### Hide empty optional columns

`operation_enterprise_stock_report_item_where_used_business_behavior_hide_empty_optional_columns`

**Inputs** columns, data.

**Explicit results** columns · list of column for column drawn from columns where column at “fieldname” does not belong to (optional\_fields − fields\_with\_values).

**Local steps**

- Set optional\_fields from set(“stock\_quantity”, “stock\_uom”, “company”, “is\_default”, …).
- If not data.
  - Return columns.
- Set fields\_with\_values from set().
- For each row in data.
  - For each column in columns.
    - Set fieldname from column at “fieldname”.
    - If (fieldname belongs to optional\_fields and field\_has\_value(row, column)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname belongs to optional\_fields → field\_has\_value(row, column).
      - Evaluate fields\_with\_values.add(column at “fieldname”).
- Return list of column for column drawn from columns where column at “fieldname” does not belong to (optional\_fields − fields\_with\_values).
  - Draw column from columns, keep a combination only if (column at “fieldname” does not belong to (optional\_fields − fields\_with\_values)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0896.json#L2847) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L216)

<a id="op-2c5960c65e8411"></a>
### Field has value

`operation_enterprise_stock_report_item_where_used_business_behavior_field_has_value`

**Inputs** row, column.

**Explicit results** false · bool(value) · (value is distinct from no value and value differs from empty text).

**Local steps**

- Set fieldname from column at “fieldname”.
- If fieldname does not belong to row.
  - Return false.
- Set value from row.get(fieldname).
- If column.get(“fieldtype”) equals “Check”.
  - Return bool(value).
- Return (value is distinct from no value and value differs from empty text).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → value differs from empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0896.json#L3183) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L200)

<a id="op-3b2ed45e981755"></a>
### Get unique names

`operation_enterprise_stock_report_item_where_used_business_behavior_get_unique_names`

**Inputs** names.

**Explicit results** unique\_names.

**Local steps**

- Set unique\_names from list().
- Set seen from set().
- For each name in names.
  - If (not name or name belongs to seen).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → name belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(name).
  - Evaluate unique\_names.append(name).
- Return unique\_names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0896.json#L3406) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L213)

<a id="op-0c95d94e99d62b"></a>
### Get permitted list

`operation_enterprise_binding_enterprise_stock_report_item_where_used_item_where_used_get_permitted_list`

**Inputs** doctype, remaining named values kwargs.

**Record and data access** read doctype via get\_list.

**Explicit results** list() · Platform.get\_list(doctype, limit\_page\_length = 0, expanded names kwargs).

**Local steps**

- If not Platform.has\_permission(doctype, “read”).
  - Return list().
- Return Platform.get\_list(doctype, limit\_page\_length = 0, expanded names kwargs).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L978)

## Report · Item wise consumption

<a id="op-ee7b5b064b6473"></a>
### Execute

`operation_enterprise_stock_report_item_wise_consumption_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns(filters).
- Set consumed\_details from get\_consumed\_details(filters).
- Set supplier\_details from get\_suppliers\_details(filters).
- Set data from list().
- For each tuple(item\_code, entries) in consumed\_details.items().
  - If (filters.get(“supplier”) and item\_code does not belong to supplier\_details).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“supplier”) → item\_code does not belong to supplier\_details.
    - Continue with the next iteration or loop test.
  - If row bound to get\_item\_row(entries, supplier\_details.get(item\_code, list())).
    - Evaluate data.append(row).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L219)

<a id="op-f70e7b6e681abf"></a>
### Get item row

`operation_enterprise_binding_enterprise_stock_report_item_wise_consumption_item_wise_consumption_get_item_row`

**Inputs** entries, suppliers.

**Explicit results** no value · list(cd.item\_code, cd.item\_name, cd.description, cd.stock\_uom, …).

**Local steps**

- Set consumed\_qty, consumed\_amount, delivered\_qty, delivered\_amount from 0.0.
- For each cd in entries.
  - If cd.voucher\_type belongs to SALES\_VOUCHER\_TYPES.
    - Update delivered\_qty using − flt(cd.actual\_qty).
    - Update delivered\_amount using − flt(cd.stock\_value\_difference).
  - Otherwise.
    - If cd.voucher\_type does not belong to PURCHASE\_VOUCHER\_TYPES.
      - Update consumed\_qty using − flt(cd.actual\_qty).
      - Update consumed\_amount using − flt(cd.stock\_value\_difference).
- If not (consumed\_qty or consumed\_amount or delivered\_qty or delivered\_amount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in consumed\_qty → consumed\_amount → delivered\_qty → delivered\_amount.
  - Return no value.
- Set cd from entries at 0.
- Return list(cd.item\_code, cd.item\_name, cd.description, cd.stock\_uom, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L979)

<a id="op-f4a58a7c2a30eb"></a>
### Get columns

`operation_enterprise_stock_report_item_wise_consumption_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Item” + “:Link/Item:100”), (translated “Item Name” + “::100”), (translated “Description” + “::150”), (translated “UOM” + “:Link/UOM:90”), …).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0896.json#L5043) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L220)

<a id="op-c445550a14e448"></a>
### Get consumed details

`operation_enterprise_stock_report_item_wise_consumption_business_behavior_get_consumed_details`

**Inputs** filters.

**Explicit results** consumed\_details.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(item).select(sle.item\_code, item.item\_name, item.description, item.stock\_uom, …).where((((sle.is\_cancelled equals 0 bitwise and sle.item ….
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set query from query.where((sle.posting\_date ≥ filters.get(“from\_date”) bitwise and sle.posting\_date ≤ filters.get(“to\_date”))).
- Set entries from query.run(as\_dict = true).
- Set transfer\_rows from get\_stock\_entry\_transfer\_rows(entries).
- Set consumed\_details from mapping().
- For each d in entries.
  - If d.voucher\_detail\_no does not belong to transfer\_rows.
    - Evaluate consumed\_details.setdefault(d.item\_code, list()).append(d).
- Return consumed\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L221)

<a id="op-90298ca7cedc5c"></a>
### Get stock entry transfer rows

`operation_enterprise_binding_enterprise_stock_report_item_wise_consumption_item_wise_consumption_get_stock_entry_transfer_rows`

**Inputs** entries.

**Explicit results** set() · set(nested operand in the contract.select(nested operand in the contract.name).where(((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract differs from nes …).

**Local steps**

- Set names from list of d.voucher\_detail\_no for d drawn from entries where (d.voucher\_type equals “Stock Entry” and d.voucher\_detail\_no).
  - Draw d from entries, keep a combination only if ((d.voucher\_type equals “Stock Entry” and d.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.voucher\_type equals “Stock Entry” → d.voucher\_detail\_no.
- If not names.
  - Return set().
- Set detail from Platform.qb.DocType(“Stock Entry Detail”).
- Return set(nested operand in the contract.select(nested operand in the contract.name).where(((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract differs from nes …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L980)

<a id="op-ea5923ae5cbc2c"></a>
### Get suppliers details

`operation_enterprise_stock_report_item_wise_consumption_business_behavior_get_suppliers_details`

**Inputs** filters.

**Explicit results** item\_supplier\_map.

**Local steps**

- Set item\_supplier\_map from mapping().
- Set supplier from filters.get(“supplier”).
- Set item from Platform.qb.DocType(“Item”).
- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(pr\_item).select(pr.supplier, pr\_item.item\_code).where(((pr.name equals pr\_item.parent bitwise and pr.docstatus equals 1) bitwise and pr\_ ….
- For each d in query.run(as\_dict = true).
  - Evaluate item\_supplier\_map.setdefault(d.item\_code, list()).append(d.supplier).
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(pi\_item).select(pi.supplier, pi\_item.item\_code).where((((pi.name equals pi\_item.parent bitwise and pi.docstatus equals 1) bitwise and If ….
- For each d in query.run(as\_dict = true).
  - If d.item\_code does not belong to item\_supplier\_map.
    - Evaluate item\_supplier\_map.setdefault(d.item\_code, list()).append(d.supplier).
- If supplier.
  - Set invalid\_items from list().
  - For each tuple(item\_code, suppliers) in item\_supplier\_map.items().
    - If supplier does not belong to suppliers.
      - Evaluate invalid\_items.append(item\_code).
  - For each item\_code in invalid\_items.
    - Remove item\_supplier\_map at item\_code.
- Return item\_supplier\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0896.json#L5971) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L222)

## Report · Items to be requested

<a id="op-59171f1bac369c"></a>
### Execute

`operation_enterprise_binding_enterprise_stock_report_items_to_be_requested_items_to_be_requested_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data()).

**Local steps**

- Return tuple(get\_columns(), get\_data()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L981)

<a id="op-ac90fa3c9977da"></a>
### Get columns

`operation_enterprise_binding_enterprise_stock_report_items_to_be_requested_items_to_be_requested_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, ….

**Local steps**

- Return list(mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L982)

<a id="op-00b2549facded2"></a>
### Get data

`operation_enterprise_binding_enterprise_stock_report_items_to_be_requested_items_to_be_requested_get_data`

**Inputs** no declared parameters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set bin\_table from Platform.qb.DocType(“Bin”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(bin\_table.item\_code, bin\_table.warehouse, bin\_table.actual\_qty, bin\_table.indented\_qty, …).where((bin\_table.projected\_qty &lt; 0 bitwise a ….
- If condition bound to get\_allowed\_masters\_condition(item.name, “Item”).
  - Set query from query.where(condition).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L983)

## Report · Itemwise recommended reorder level

<a id="op-7148a3d17af418"></a>
### Execute

`operation_enterprise_stock_report_itemwise_recommended_reorder_level_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set float\_precision from Platform.db.get\_default(“float\_precision”).
- Set avg\_daily\_outgoing from 0.
- Set tuple(from\_date, to\_date) from tuple(getdate(filters.get(“from\_date”)), getdate(filters.get(“to\_date”))).
- Evaluate validate\_date\_range(mapping(“from\_date” → from\_date, “to\_date” → to\_date)).
- Set diff from ((to\_date − from\_date).days + 1).
- Set columns from get\_columns().
- Set items from get\_item\_info(filters).
- Set consumed\_item\_map from get\_consumed\_items(filters).
- Set delivered\_item\_map from get\_delivered\_items(filters).
- Set data from list().
- For each item in items.
  - Set total\_outgoing from (flt(consumed\_item\_map.get(item.name, 0)) + flt(delivered\_item\_map.get(item.name, 0))).
  - Set avg\_daily\_outgoing from flt((total\_outgoing ÷ diff), float\_precision).
  - Set reorder\_level from ((avg\_daily\_outgoing × flt(item.lead\_time\_days)) + flt(item.safety\_stock)).
  - Evaluate data.append(list(item.name, item.item\_name, item.item\_group, item.brand, …)).
- Return tuple(columns, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L224)

<a id="op-b7a7b5cc06fa46"></a>
### Get columns

`operation_enterprise_stock_report_itemwise_recommended_reorder_level_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list((translated “Item” + “:Link/Item:120”), (translated “Item Name” + “:Data:120”), (translated “Item Group” + “:Link/Item Group:100”), (translated “Brand” + “:Link/Brand:100”), …).

**Local steps**

- Return list((translated “Item” + “:Link/Item:120”), (translated “Item Name” + “:Data:120”), (translated “Item Group” + “:Link/Item Group:100”), (translated “Brand” + “:Link/Brand:100”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0897.json#L1770) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L225)

<a id="op-d0b2f5c9ded60a"></a>
### Get item info

`operation_enterprise_stock_report_itemwise_recommended_reorder_level_business_behavior_get_item_info`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Bind dependencies get\_item\_group\_condition.
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item).select(item.name, item.item\_name, item.description, item.brand, …).where((item.is\_stock\_item equals 1 bitwise and item.disabled equals 0)).
- If brand bound to filters.get(“brand”).
  - Set query from query.where(item.brand equals brand).
- If conditions bound to get\_item\_group\_condition(filters.get(“item\_group”), item).
  - Set query from query.where(conditions).
- If condition bound to get\_allowed\_masters\_condition(item.name, “Item”).
  - Set query from query.where(condition).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L229)

<a id="op-72443610824946"></a>
### Get consumed items

`operation_enterprise_stock_report_itemwise_recommended_reorder_level_business_behavior_get_consumed_items`

**Inputs** filters.

**Explicit results** consumed\_items\_map.

**Local steps**

- Set purpose\_to\_exclude from list(“Material Transfer for Manufacture”, “Material Transfer”, “Send to Subcontractor”).
- Set se from Platform.qb.DocType(“Stock Entry”).
- Set scr from Platform.qb.DocType(“Subcontracting Receipt”).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, nested operand in the contract.as\_(“consumed\_qty”)).where(((((nested operand in the contract bitwise and nested operand  ….
- Set query from get\_filtered\_query(filters, sle, query).
- Set consumed\_items from query.run(as\_dict = true).
- Set consumed\_items\_map from mapping of item.item\_code → item.consumed\_qty for item drawn from consumed\_items.
  - Draw item from consumed\_items.
- Return consumed\_items\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L226)

<a id="op-4b5104ea8ee1ff"></a>
### Get delivered items

`operation_enterprise_stock_report_itemwise_recommended_reorder_level_business_behavior_get_delivered_items`

**Inputs** filters.

**Explicit results** mapping of item.item\_code → negative flt(item.delivered\_qty) for item drawn from query.run(as\_dict = true).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, nested operand in the contract.as\_(“delivered\_qty”)).where((sle.is\_cancelled equals 0 bitwise and nested operand in the  ….
- Set query from get\_filtered\_query(filters, sle, query).
- Return mapping of item.item\_code → negative flt(item.delivered\_qty) for item drawn from query.run(as\_dict = true).
  - Draw item from query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L227)

<a id="op-5e0d6c32c60215"></a>
### Get filtered query

`operation_enterprise_stock_report_itemwise_recommended_reorder_level_business_behavior_get_filtered_query`

**Inputs** filters, table, query.

**Explicit results** query.

**Explicit failure paths** validation helper — translated “From and To dates are required”.

**Local steps**

- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set query from query.where(table.posting\_date.between(filters at “from\_date”, filters at “to\_date”)).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “From and To dates are required”).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0897.json#L3964) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L228)

## Report · Landed cost report

<a id="op-bdf8dd70603504"></a>
### Execute

`operation_enterprise_stock_report_landed_cost_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L232)

<a id="op-e6d55a6020564d"></a>
### Get columns

`operation_enterprise_stock_report_landed_cost_report_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Landed Cost Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Landed Cost Voucher”), mapping(“label” → translated “Landed Cost”, “fieldname” → “landed\_cost”,  ….

**Local steps**

- Return list(mapping(“label” → translated “Landed Cost Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Landed Cost Voucher”), mapping(“label” → translated “Landed Cost”, “fieldname” → “landed\_cost”,  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L233)
