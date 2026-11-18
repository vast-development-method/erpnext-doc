# Production · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Bom explorer

<a id="op-977aad0a0abae1"></a>
### Get exploded items

`operation_enterprise_binding_enterprise_manufacturing_report_bom_explorer_bom_explorer_get_exploded_items`

**Inputs** bom, data, indent = 0, qty = 1.

**Record and data access** read “BOM Item” via get\_all.

**Local steps**

- Set exploded\_items from Platform.get\_all(“BOM Item”, filters = mapping(“parent” → bom), fields = list(“qty”, “bom\_no”, “bom\_no.quantity as child\_bom\_qty”, “stock\_qty”, …), order\_by = “idx ASC”).
- For each item in exploded\_items.
  - Set item at “indent” from indent.
  - Evaluate data.append(mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “indent” → indent, “bom\_level” → indent, …)).
  - If item.bom\_no.
    - Evaluate get\_exploded\_items(item.bom\_no, data, indent = (indent + 1), qty = ((qty × item.stock\_qty) ÷ item.child\_bom\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1120)

<a id="op-bd58041d507dff"></a>
### Get columns

`operation_enterprise_manufacturing_report_bill_of_materials_explorer_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Item Code”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “width” → 300, …), mapping(“label” → translated “Item Name”, “fieldtype” → “data”, “fieldname” → “item\_name”, ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “width” → 300, …), mapping(“label” → translated “Item Name”, “fieldtype” → “data”, “fieldname” → “item\_name”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0540.json#L1981) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1018)

## Report · Bom operations time

<a id="op-29363a8f479842"></a>
### Execute

`operation_enterprise_manufacturing_report_bill_of_materials_operations_time_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0540.json#L5396) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1020)

<a id="op-739d69ff93e15f"></a>
### Get data

`operation_enterprise_manufacturing_report_bill_of_materials_operations_time_business_behavior_get_data`

**Inputs** filters.

**Explicit results** report\_data.

**Local steps**

- Set bom\_wise\_data from mapping().
- Set tuple(bom\_data, report\_data) from tuple(list(), list()).
- Set bom\_operation\_data from get\_filtered\_data(filters).
- For each d in bom\_operation\_data.
  - Set row from get\_args().
  - If d.name does not belong to bom\_data.
    - Set bom\_wise\_data at d.name from list().
    - Evaluate bom\_data.append(d.name).
    - Evaluate row.update(d).
  - Otherwise.
    - Evaluate row.update(mapping(“operation” → d.operation, “workstation” → d.workstation, “time\_in\_mins” → d.time\_in\_mins)).
  - Evaluate bom\_wise\_data at d.name.append(row).
- Set used\_as\_subassembly\_items from get\_bom\_count(bom\_data).
- For each d in bom\_wise\_data.
  - For each row in bom\_wise\_data at d.
    - Set row.used\_as\_subassembly\_items from used\_as\_subassembly\_items.get(d, 0).
    - Evaluate report\_data.append(row).
- Return report\_data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1024)

<a id="op-3b38223ddac8ec"></a>
### Get filtered data

`operation_enterprise_manufacturing_report_bill_of_materials_operations_time_business_behavior_get_filtered_data`

**Inputs** filters.

**Explicit results** bom\_operation\_data.

**Local steps**

- Set bom from Platform.qb.DocType(“BOM”).
- Set bom\_ops from Platform.qb.DocType(“BOM Operation”).
- Set bom\_ops\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(bom.name, bom.item, bom.item\_name, bom.uom, …).whe ….
- If filters.get(“item\_code”).
  - Set bom\_ops\_query from bom\_ops\_query.where(bom.item equals filters.get(“item\_code”)).
- If filters.get(“bom\_id”).
  - Set bom\_ops\_query from bom\_ops\_query.where(bom.name.isin(filters.get(“bom\_id”))).
- If filters.get(“workstation”).
  - Set bom\_ops\_query from bom\_ops\_query.where(bom\_ops.workstation equals filters.get(“workstation”)).
- Set bom\_operation\_data from bom\_ops\_query.run(as\_dict = true).
- Return bom\_operation\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0540.json#L6003) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1025)

<a id="op-0d776cf678b6ba"></a>
### Get bom count

`operation_enterprise_manufacturing_report_bill_of_materials_operations_time_business_behavior_get_bill_of_materials_count`

**Inputs** bom\_data.

**Explicit results** mapping() · mapping of d.bom\_no → d.count for d drawn from data.

**Local steps**

- If not bom\_data.
  - Return mapping().
- Set bom from Platform.qb.DocType(“BOM”).
- Set bom\_item from Platform.qb.DocType(“BOM Item”).
- Set data from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Return mapping of d.bom\_no → d.count for d drawn from data.
  - Draw d from data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1022)

<a id="op-8ceef332dd8cd3"></a>
### Get args

`operation_enterprise_manufacturing_report_bill_of_materials_operations_time_business_behavior_get_arguments`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(mapping(“name” → empty text, “item” → empty text, “item\_name” → empty text, “uom” → empty text)).

**Local steps**

- Return Platform.\_dict(mapping(“name” → empty text, “item” → empty text, “item\_name” → empty text, “uom” → empty text)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0540.json#L6884) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1021)

<a id="op-732af45363f5f5"></a>
### Get columns

`operation_enterprise_manufacturing_report_bill_of_materials_operations_time_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “BOM ID”, “options” → “BOM”, “fieldname” → “name”, “fieldtype” → “Link”, …), mapping(“label” → translated “Item Code”, “options” → “Item”, “fieldname” → “item”, “fieldtype ….

**Local steps**

- Return list(mapping(“label” → translated “BOM ID”, “options” → “BOM”, “fieldname” → “name”, “fieldtype” → “Link”, …), mapping(“label” → translated “Item Code”, “options” → “Item”, “fieldname” → “item”, “fieldtype ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1023)

## Report · Bom stock analysis

<a id="op-432adea209155a"></a>
### Execute

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set filters from (filters or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If filters.get(“qty\_to\_make”).
  - Set columns from get\_columns\_with\_qty\_to\_make().
  - Set data from get\_data\_with\_qty\_to\_make(filters).
- Otherwise.
  - Set columns from get\_columns\_without\_qty\_to\_make().
  - Set data from get\_data\_without\_qty\_to\_make(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L3121) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1033)

<a id="op-1c264c5c1663c7"></a>
### Fmt qty

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_format_quantity`

**Inputs** value.

**Explicit results** Platform.utils.fmt\_money(value, precision = 2, currency = no value).

**Local steps**

- Return Platform.utils.fmt\_money(value, precision = 2, currency = no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L3320) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1035)

<a id="op-177c98ae98bca1"></a>
### Fmt rate

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_format_rate`

**Inputs** value.

**Explicit results** Platform.utils.fmt\_money(value, precision = 2, currency = currency).

**Local steps**

- Set currency from Platform.defaults.get\_global\_default(“currency”).
- Return Platform.utils.fmt\_money(value, precision = 2, currency = currency).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L3400) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1036)

<a id="op-ff7ceeb000dcdf"></a>
### Get data with qty to make

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_data_with_quantity_to_make`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set bom\_data from get\_bom\_data(filters).
- Set manufacture\_details from get\_manufacturer\_records().
- Set purchase\_rates from batch\_fetch\_purchase\_rates(bom\_data).
- Set qty\_to\_make from flt(filters.get(“qty\_to\_make”)).
- Set data from list().
- For each row in bom\_data.
  - Set qty\_per\_unit from flt(row.qty\_per\_unit) when row.qty\_per\_unit &gt; 0, otherwise 0.
    - Value choice on row.qty\_per\_unit &gt; 0 — true gives flt(row.qty\_per\_unit), false gives 0.
  - Set required\_qty from (qty\_to\_make × qty\_per\_unit).
  - Set difference\_qty from (flt(row.actual\_qty) − required\_qty).
  - Set rate from purchase\_rates.get(row.item\_code, 0).
  - Evaluate data.append(mapping(“item” → row.item\_code, “description” → row.description, “from\_bom\_no” → row.from\_bom\_no, “manufacturer” → comma\_and(nested operand in the contract.get(nested operand in the contract.it ….
- Set min\_producible from min(generator of get\_producible\_qty(r at “\_available\_qty”, r at “\_qty\_per\_unit”) for r drawn from data where r at “\_qty\_per\_unit”) when data, otherwise 0.
  - Value choice on data — true gives min(generator of get\_producible\_qty(r at “\_available\_qty”, r at “\_qty\_per\_unit”) for r drawn from data where r at “\_qty\_per\_unit”), false gives 0.
  - Draw r from data, keep a combination only if (r at “\_qty\_per\_unit”).
- For each row in data.
  - Evaluate row.pop(“\_available\_qty”, no value).
  - Evaluate row.pop(“\_qty\_per\_unit”, no value).
- Evaluate data.append(mapping()).
- Evaluate data.append(mapping(“item” → translated “Maximum Producible Items”, “description” → min\_producible, “from\_bom\_no” → empty text, “manufacturer” → empty text, …)).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1040)

<a id="op-a91ae21652eba9"></a>
### Get columns with qty to make

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_columns_with_quantity_to_make`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “item”, “label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “description”, “label” → translated “Description”, “fieldtype” → “Data”,  ….

**Local steps**

- Return list(mapping(“fieldname” → “item”, “label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “description”, “label” → translated “Description”, “fieldtype” → “Data”,  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L4659) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1038)

<a id="op-70acfe3bd0788f"></a>
### Get data without qty to make

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_data_without_quantity_to_make`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set raw\_rows from get\_producible\_fg\_items(filters).
- Set data from list().
- For each row in raw\_rows.
  - Evaluate data.append(mapping(“item” → row.item\_code, “description” → row.description, “from\_bom\_no” → row.from\_bom\_no, “qty\_per\_unit” → fmt\_qty(row.qty\_per\_unit), …)).
- Set min\_producible from min(generator of row.producible\_qty for row drawn from raw\_rows where row.producible\_qty is distinct from no value, default = 0).
  - Draw row from raw\_rows, keep a combination only if (row.producible\_qty is distinct from no value).
- Evaluate data.append(mapping()).
- Evaluate data.append(mapping(“item” → translated “Maximum Producible Items”, “description” → min\_producible, “from\_bom\_no” → empty text, “qty\_per\_unit” → empty text, …)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1041)

<a id="op-640487b42f28bd"></a>
### Get columns without qty to make

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_columns_without_quantity_to_make`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “item”, “label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “description”, “label” → translated “Description”, “fieldtype” → “Data”,  ….

**Local steps**

- Return list(mapping(“fieldname” → “item”, “label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “description”, “label” → translated “Description”, “fieldtype” → “Data”,  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L6041) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1039)

<a id="op-4f24d8a7aa914a"></a>
### Batch fetch purchase rates

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_batch_fetch_purchase_rates`

**Inputs** bom\_data.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · mapping of r.name → r.last\_purchase\_rate for r drawn from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, item\_codes)), fields = list(“name”, “last\_purchase\_rate”)).

**Local steps**

- If not bom\_data.
  - Return mapping().
- Set item\_codes from list of row.item\_code for row drawn from bom\_data.
  - Draw row from bom\_data.
- Return mapping of r.name → r.last\_purchase\_rate for r drawn from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, item\_codes)), fields = list(“name”, “last\_purchase\_rate”)).
  - Draw r from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, item\_codes)), fields = list(“name”, “last\_purchase\_rate”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0541.json#L6545) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1032)

<a id="op-ce4d3414acd6b0"></a>
### Get stock qty by item

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_stock_quantity_by_item`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** query.

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract.qb.from\_(bin).select(bin.item\_code, Sum(nested operand in the contract.actual\_qty).as\_(“actual\_qty”)).groupby(bin.item\_code).
- If filters.get(“warehouse”).
  - Set warehouse\_details from Platform.db.get\_value(“Warehouse”, filters.get(“warehouse”), list(“lft”, “rgt”), as\_dict = 1).
  - If warehouse\_details.
    - Set wh from Platform.qb.DocType(“Warehouse”).
    - Set query from query.where(ExistsCriterion(nested operand in the contract(nested operand in the contract).select(wh.name).where(((nested operand in the contract.lft ≥ nested operand in the contract.lft bitwise and nested ….
  - Otherwise.
    - Set query from query.where(bin.warehouse equals filters.get(“warehouse”)).
- Otherwise.
  - Set query from query.where(bin.warehouse.isin(get\_permitted\_warehouses((filters.get(“top\_bom”) or filters.get(“bom”))))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“top\_bom”) → filters.get(“bom”).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1044)

<a id="op-6ed2cc3efa58d8"></a>
### Get permitted warehouses

`operation_enterprise_binding_enterprise_manufacturing_report_bom_stock_analysis_bom_stock_analysis_get_permitted_warehouses`

**Inputs** bom.

**Record and data access** read “BOM” via get\_value.

**Explicit results** Platform.qb.get\_query(“Warehouse”, fields = list(“name”), filters = mapping(“company” → company), ignore\_permissions = false).

**Local steps**

- Set company from Platform.db.get\_value(“BOM”, bom, “company”, cache = true).
- Return Platform.qb.get\_query(“Warehouse”, fields = list(“name”), filters = mapping(“company” → company), ignore\_permissions = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1121)

<a id="op-6c1ad5f8b0b62a"></a>
### Get bom data

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_bill_of_materials_data`

**Inputs** filters.

**Record and data access** read “BOM” via get\_value.

**Explicit results** explode\_phantom\_boms(data, filters) when bom\_item\_table equals “BOM Item”, otherwise data.

**Local steps**

- Set bom\_item\_table from “BOM Explosion Item” when filters.get(“show\_exploded\_view”), otherwise “BOM Item”.
  - Value choice on filters.get(“show\_exploded\_view”) — true gives “BOM Explosion Item”, false gives “BOM Item”.
- Set bom\_item from Platform.qb.DocType(bom\_item\_table).
- Set stock\_qty from get\_stock\_qty\_by\_item(filters).as\_(“stock\_qty”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract equal ….
- If bom\_item\_table equals “BOM Item”.
  - Set query from query.select(bom\_item.bom\_no, bom\_item.is\_phantom\_item).
- Set data from query.run(as\_dict = true).
- Set bom\_quantity from (flt(Platform.db.get\_value(“BOM”, filters.get(“bom”), “quantity”)) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(Platform.db.get\_value(“BOM”, filters.get(“bom”), “quantity”)) → 1.0.
- For each row in data.
  - Set row.qty\_per\_unit from (flt(row.pop(“bom\_stock\_qty”)) ÷ bom\_quantity).
- Return explode\_phantom\_boms(data, filters) when bom\_item\_table equals “BOM Item”, otherwise data.
  - Value choice on bom\_item\_table equals “BOM Item” — true gives explode\_phantom\_boms(data, filters), false gives data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1037)

<a id="op-9afe3506b1f6ec"></a>
### Explode phantom boms

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_explode_phantom_bills_of_materials`

**Inputs** data, filters.

**Explicit results** merge\_rows\_by\_item(data) when replacements, otherwise data.

**Local steps**

- Set original\_bom from filters.get(“bom”).
- Evaluate filters.setdefault(“top\_bom”, original\_bom).
- Set replacements from list().
- For each tuple(idx, item) in enumerate(data).
  - If not item.is\_phantom\_item.
    - Continue with the next iteration or loop test.
  - Set filters at “bom” from item.bom\_no.
  - Set children from get\_bom\_data(filters).
  - Set filters at “bom” from original\_bom.
  - For each child in children.
    - Set child.qty\_per\_unit from ((child.qty\_per\_unit or 0) × (item.qty\_per\_unit or 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in child.qty\_per\_unit → 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.qty\_per\_unit → 0.
  - Evaluate replacements.append(tuple(idx, children)).
- For each tuple(idx, children) in reversed(replacements).
  - Evaluate data.pop(idx).
  - Set data at slice idx to idx from children.
- Return merge\_rows\_by\_item(data) when replacements, otherwise data.
  - Value choice on replacements — true gives merge\_rows\_by\_item(data), false gives data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1034)

<a id="op-118cede281ba18"></a>
### Merge rows by item

`operation_enterprise_binding_enterprise_manufacturing_report_bom_stock_analysis_bom_stock_analysis_merge_rows_by_item`

**Inputs** data.

**Explicit results** list(merged.values()).

**Local steps**

- Set merged from mapping().
- For each row in data.
  - If row.item\_code belongs to merged.
    - Set merged at row.item\_code.qty\_per\_unit from (flt(merged at row.item\_code.qty\_per\_unit) + flt(row.qty\_per\_unit)).
  - Otherwise.
    - Set merged at row.item\_code from row.
- Return list(merged.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1123)

<a id="op-1141b759a1529c"></a>
### Get manufacturer records

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_manufacturer_records`

**Inputs** no declared parameters.

**Record and data access** read “Item Manufacturer” via get\_all.

**Explicit results** manufacture\_details.

**Local steps**

- Set details from Platform.get\_all(“Item Manufacturer”, fields = list(“manufacturer”, “manufacturer\_part\_no”, “item\_code”)).
- Set manufacture\_details from Platform.\_dict().
- For each detail in details.
  - Set dic from manufacture\_details.setdefault(detail.get(“item\_code”), mapping()).
  - Evaluate dic.setdefault(“manufacturer”, list()).append(detail.get(“manufacturer”)).
  - Evaluate dic.setdefault(“manufacturer\_part”, list()).append(detail.get(“manufacturer\_part\_no”)).
- Return manufacture\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0542.json#L2275) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1042)

<a id="op-f44df4c03cc4b1"></a>
### Get producible fg items

`operation_enterprise_manufacturing_report_bill_of_materials_stock_analysis_business_behavior_get_producible_finished_goods_items`

**Inputs** filters.

**Explicit results** rows.

**Local steps**

- Set rows from get\_bom\_data(filters).
- For each row in rows.
  - Set row.qty\_per\_unit from flt(row.qty\_per\_unit).
  - Set row.available\_qty from flt(row.actual\_qty).
  - Set row.producible\_qty from get\_producible\_qty(row.available\_qty, row.qty\_per\_unit) when row.qty\_per\_unit &gt; 0, otherwise no value.
    - Value choice on row.qty\_per\_unit &gt; 0 — true gives get\_producible\_qty(row.available\_qty, row.qty\_per\_unit), false gives no value.
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1043)

<a id="op-3cf2f3ee9bc107"></a>
### Get producible qty

`operation_enterprise_binding_enterprise_manufacturing_report_bom_stock_analysis_bom_stock_analysis_get_producible_qty`

**Inputs** available\_qty, qty\_per\_unit.

**Explicit results** math.floor(flt((flt(available\_qty) ÷ flt(qty\_per\_unit)), 9)).

**Local steps**

- Return math.floor(flt((flt(available\_qty) ÷ flt(qty\_per\_unit)), 9)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1122)
