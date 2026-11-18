# Inventory and warehouses · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Item price stock

<a id="op-f91e6a7deb2395"></a>
### Get data

`operation_enterprise_stock_report_item_price_stock_business_behavior_get_data`

**Inputs** filters, columns.

**Explicit results** item\_price\_qty\_data.

**Local steps**

- Set item\_price\_qty\_data from list().
- Set item\_price\_qty\_data from get\_item\_price\_qty\_data(filters).
- Return item\_price\_qty\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0893.json#L1498) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L170)

<a id="op-c4121e06b7427c"></a>
### Get item price qty data

`operation_enterprise_stock_report_item_price_stock_business_behavior_get_item_price_quantity_data`

**Inputs** filters.

**Explicit results** result.

**Local steps**

- Set item\_price from Platform.qb.DocType(“Item Price”).
- Set bin from Platform.qb.DocType(“Bin”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.item\_code equals nested operand in the contract.item\_code).select(item\_price.item\_code, item\_price.item\_name ….
- If filters.get(“item\_code”).
  - Set query from query.where(item\_price.item\_code equals filters.get(“item\_code”)).
- If condition bound to get\_allowed\_masters\_condition(item\_price.item\_code, “Item”).
  - Set query from query.where(condition).
- Set item\_results from query.run(as\_dict = true).
- Set price\_list\_names from list(set(generator of item.price\_list\_name for item drawn from item\_results)).
  - Draw item from item\_results.
- Set buying\_price\_map from get\_price\_map(price\_list\_names, buying = 1).
- Set selling\_price\_map from get\_price\_map(price\_list\_names, selling = 1).
- Set result from list().
- If item\_results.
  - For each item\_dict in item\_results.
    - Set data from mapping(“item\_code” → item\_dict.item\_code, “item\_name” → item\_dict.item\_name, “brand” → item\_dict.brand, “warehouse” → item\_dict.warehouse, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_dict.actual\_qty → 0.
    - Set price\_list from item\_dict at “price\_list\_name”.
    - If buying\_price\_map.get(price\_list).
      - Set data at “buying\_price\_list” from (buying\_price\_map.get(price\_list) at “Buying Price List” or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in buying\_price\_map.get(price\_list) at “Buying Price List” → empty text.
      - Set data at “buying\_rate” from (buying\_price\_map.get(price\_list) at “Buying Rate” or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in buying\_price\_map.get(price\_list) at “Buying Rate” → 0.
    - If selling\_price\_map.get(price\_list).
      - Set data at “selling\_price\_list” from (selling\_price\_map.get(price\_list) at “Selling Price List” or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in selling\_price\_map.get(price\_list) at “Selling Price List” → empty text.
      - Set data at “selling\_rate” from (selling\_price\_map.get(price\_list) at “Selling Rate” or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in selling\_price\_map.get(price\_list) at “Selling Rate” → 0.
    - Evaluate result.append(data).
- Return result.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L171)

<a id="op-bd9a953f71b144"></a>
### Get price map

`operation_enterprise_stock_report_item_price_stock_business_behavior_get_price_map`

**Inputs** price\_list\_names, buying = 0, selling = 0.

**Record and data access** read “Item Price” via get\_all.

**Explicit results** price\_map.

**Local steps**

- Set price\_map from mapping().
- If not price\_list\_names.
  - Return price\_map.
- Set rate\_key from “Buying Rate” when buying, otherwise “Selling Rate”.
  - Value choice on buying — true gives “Buying Rate”, false gives “Selling Rate”.
- Set price\_list\_key from “Buying Price List” when buying, otherwise “Selling Price List”.
  - Value choice on buying — true gives “Buying Price List”, false gives “Selling Price List”.
- Set filters from mapping(“name” → tuple(“in”, price\_list\_names)).
- If buying.
  - Set filters at “buying” from 1.
- Otherwise.
  - Set filters at “selling” from 1.
- Set pricing\_details from Platform.get\_all(“Item Price”, fields = list(“name”, “price\_list”, “price\_list\_rate”), filters = filters).
- For each d in pricing\_details.
  - Set name from d at “name”.
  - Set price\_map at name from mapping(price\_list\_key → d at “price\_list”, rate\_key → d at “price\_list\_rate”).
- Return price\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0893.json#L2721) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L172)

## Report · Item prices

<a id="op-1109cf04bb599f"></a>
### Execute

`operation_enterprise_stock_report_item_prices_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns(filters).
- Set item\_map from get\_item\_details(filters).
- Set pl from get\_price\_list().
- Set last\_purchase\_rate from get\_last\_purchase\_rate().
- Set bom\_rate from get\_item\_bom\_rate().
- Set val\_rate\_map from get\_valuation\_rate().
- Bind dependencies get\_currency\_precision.
- Set precision from (get\_currency\_precision() or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_currency\_precision() → 2.
- Set data from list().
- For each item in sorted(item\_map).
  - Evaluate data.append(list(item, item\_map at item at “item\_name”, item\_map at item at “item\_group”, item\_map at item at “brand”, …)).
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0893.json#L3774) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L174)

<a id="op-d01566969cb63f"></a>
### Get columns

`operation_enterprise_stock_report_item_prices_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Item” + “:Link/Item:100”), (translated “Item Name” + “::150”), (translated “Item Group” + “:Link/Item Group:125”), (translated “Brand” + “::100”), …).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0893.json#L4413) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L175)

<a id="op-82549594f56b88"></a>
### Get item details

`operation_enterprise_stock_report_item_prices_business_behavior_get_item_details`

**Inputs** filters.

**Explicit results** item\_map.

**Local steps**

- Set item\_map from mapping().
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item).select(item.name, item.item\_group, item.item\_name, item.description, …).orderby(item.item\_code, item.item\_group).
- If filters.get(“items”) equals “Enabled Items only”.
  - Set query from query.where(item.disabled equals 0).
- Otherwise.
  - If filters.get(“items”) equals “Disabled Items only”.
    - Set query from query.where(item.disabled equals 1).
- If condition bound to get\_allowed\_masters\_condition(item.name, “Item”).
  - Set query from query.where(condition).
- For each i in query.run(as\_dict = true).
  - Evaluate item\_map.setdefault(i.name, i).
- Return item\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L177)

<a id="op-d01beba12d34ca"></a>
### Get price list

`operation_enterprise_stock_report_item_prices_business_behavior_get_price_list`

**Inputs** no declared parameters.

**Explicit results** item\_rate\_map.

**Local steps**

- Set rate from mapping().
- Set ip from Platform.qb.DocType(“Item Price”).
- Set pl from Platform.qb.DocType(“Price List”).
- Set cu from Platform.qb.DocType(“Currency”).
- Set price\_list from nested operand in the contract(nested operand in the contract).select(ip.item\_code, ip.buying, ip.selling, nested operand in the contract.as\_(“currency”), …).where(((((nested operand in the contract bitwis ….
- For each d in price\_list.
  - Set d.price from get\_price\_label(d).
  - If d.price.
    - Evaluate rate.setdefault(d.item\_code, mapping()).setdefault(“Buying” when d.buying, otherwise “Selling”, list()).append(d.price).
      - Value choice on d.buying — true gives “Buying”, false gives “Selling”.
- Set item\_rate\_map from mapping().
- For each item in rate.
  - For each buying\_or\_selling in rate at item.
    - Evaluate item\_rate\_map.setdefault(item, mapping()).setdefault(buying\_or\_selling, “, ”.join(rate at item.get(buying\_or\_selling, list()))).
- Return item\_rate\_map.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L179)

<a id="op-7d6d32cbae9de7"></a>
### Get price label

`operation_enterprise_binding_enterprise_stock_report_item_prices_item_prices_get_price_label`

**Inputs** price.

**Explicit results** label.

**Local steps**

- Set label from formatted text {price.currency} {round(price.price\_list\_rate, 2)} - {price.price\_list}.
- If price.uom.
  - Update label using + formatted text  / {price.uom}.
- If details bound to list of value for value drawn from tuple(price.customer, price.supplier, price.batch\_no) where value.
  - Draw value from tuple(price.customer, price.supplier, price.batch\_no), keep a combination only if (value).
  - Update label using + formatted text  ({“, ”.join(details)}).
- Return label.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L967)

<a id="op-8e725eb0949ecd"></a>
### Get last purchase rate

`operation_enterprise_stock_report_item_prices_business_behavior_get_last_purchase_rate`

**Inputs** no declared parameters.

**Explicit results** item\_last\_purchase\_rate\_map.

**Local steps**

- Set item\_last\_purchase\_rate\_map from mapping().
- Set po from Platform.qb.DocType(“Purchase Order”).
- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract.qb.from\_(((nested operand in the contract + nested operand in the contract) + nested operand in the contract(nested operand in the contract))).select(“\*”).orderby(“item\_code” ….
- For each d in query.run(as\_dict = true).
  - Set item\_last\_purchase\_rate\_map at d.item\_code from d.base\_rate.
- Return item\_last\_purchase\_rate\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L178)

<a id="op-cf218e8f72574b"></a>
### Get item bom rate

`operation_enterprise_stock_report_item_prices_business_behavior_get_item_bill_of_materials_rate`

**Inputs** no declared parameters.

**Explicit results** item\_bom\_map.

**Local steps**

- Set item\_bom\_map from mapping().
- Set bom from Platform.qb.DocType(“BOM”).
- Set bom\_data from nested operand in the contract(nested operand in the contract).select(bom.item, nested operand in the contract.as\_(“bom\_rate”)).where((bom.is\_active equals 1 bitwise and bom.is\_default equals 1)).run(as\_dict = true).
- For each d in bom\_data.
  - Evaluate item\_bom\_map.setdefault(d.item, flt(d.bom\_rate)).
- Return item\_bom\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0893.json#L6964) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L176)

<a id="op-e5523a261e7cf5"></a>
### Get valuation rate

`operation_enterprise_stock_report_item_prices_business_behavior_get_valuation_rate`

**Inputs** no declared parameters.

**Explicit results** item\_val\_rate\_map.

**Local steps**

- Set item\_val\_rate\_map from mapping().
- Set bin from Platform.qb.DocType(“Bin”).
- Set bin\_data from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.actual\_qty &gt; 0).groupby(bin.item\_code).run(as\_dict = true).
- For each d in bin\_data.
  - Evaluate item\_val\_rate\_map.setdefault(d.item\_code, d.val\_rate).
- Return item\_val\_rate\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0894.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L180)

## Report · Item shortage report

<a id="op-2645eeb854ff21"></a>
### Execute

`operation_enterprise_stock_report_item_shortage_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list(), no value, list()) · tuple(columns, data, no value, chart\_data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- If not data.
  - Return tuple(list(), list(), no value, list()).
- Set chart\_data from get\_chart\_data(data).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0894.json#L2366) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L185)

<a id="op-dec50c05e7b5d6"></a>
### Get data

`operation_enterprise_stock_report_item_shortage_report_business_behavior_get_data`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set wh from Platform.qb.DocType(“Warehouse”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(bin.warehouse, bin.item\_code, bin.actual\_qty, bin.ordered\_qty, …).where((((nested operand in the contract equals nested operand in the  ….
- If warehouses bound to filters.get(“warehouse”).
  - Set query from query.where(bin.warehouse.isin(get\_warehouses\_with\_descendants(warehouses))).
- If filters.get(“company”).
  - Set query from query.where(wh.company equals filters.get(“company”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L188)

<a id="op-d252bc589c4185"></a>
### Get warehouses with descendants

`operation_enterprise_binding_enterprise_stock_report_item_shortage_report_item_shortage_report_get_warehouses_with_descendants`

**Inputs** warehouses.

**Explicit results** list(result).

**Local steps**

- Set result from set(warehouses).
- For each warehouse in warehouses.
  - Evaluate result.update(get\_descendants\_of(“Warehouse”, warehouse)).
- Return list(result).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L968)

<a id="op-ceb1e98d91fd95"></a>
### Get chart data

`operation_enterprise_stock_report_item_shortage_report_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Projected Qty”, “values” → datapoints))), “type” → “bar”).

**Local steps**

- Set tuple(labels, datapoints) from tuple(list(), list()).
- For each row in data.
  - Evaluate labels.append(row.get(“item\_code”)).
  - Evaluate datapoints.append(row.get(“projected\_qty”)).
- If len(data) &gt; 10.
  - Set labels from labels at slice no value to 10.
  - Set datapoints from datapoints at slice no value to 10.
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Projected Qty”, “values” → datapoints))), “type” → “bar”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0894.json#L3201) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L186)

<a id="op-2385552ad7d5e6"></a>
### Get columns

`operation_enterprise_stock_report_item_shortage_report_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …), mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “L ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L187)

## Report · Item variant details

<a id="op-953249802e431a"></a>
### Execute

`operation_enterprise_stock_report_item_variant_details_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set templates from get\_templates(filters).
- Set columns from get\_columns(list(templates)).
- Set data from get\_data(templates, filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L190)

<a id="op-c269992fd0dd0b"></a>
### Get templates

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_templates`

**Inputs** filters.

**Record and data access** read “Item” via get\_list.

**Explicit results** mapping() · dict(Platform.get\_list(“Item”, filters = template\_filters, fields = list(“name”, “item\_group”), order\_by = “name”, as\_list = true)).

**Explicit failure paths** validation helper — translated “Select either Items or Item Groups, not both”.

**Local steps**

- Set items from get\_filter\_values(filters, “item”).
- Set item\_groups from get\_filter\_values(filters, “item\_group”).
- If (items and item\_groups).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in items → item\_groups.
  - Call the validation error handler Platform.throw(translated “Select either Items or Item Groups, not both”).
- If not (items or item\_groups).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items → item\_groups.
  - Return mapping().
- Set template\_filters from mapping(“has\_variants” → 1).
- If items.
  - Set template\_filters at “name” from list(“in”, items).
- Otherwise.
  - Evaluate template\_filters.update(disabled = 0, item\_group = list(“in”, get\_item\_groups\_with\_descendants(item\_groups))).
- Return dict(Platform.get\_list(“Item”, filters = template\_filters, fields = list(“name”, “item\_group”), order\_by = “name”, as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L976)

<a id="op-7f5dc0ca81b553"></a>
### Get item groups with descendants

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_item_groups_with_descendants`

**Inputs** item\_groups.

**Explicit results** list(expanded item\_groups, expanded generator of child for group drawn from item\_groups, then child drawn from get\_descendants\_of(“Item Group”, group)).

**Local steps**

- Return list(expanded item\_groups, expanded generator of child for group drawn from item\_groups, then child drawn from get\_descendants\_of(“Item Group”, group)).
  - Draw group from item\_groups.
  - Draw child from get\_descendants\_of(“Item Group”, group).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L970)

<a id="op-917c187bda970c"></a>
### Get filter values

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_filter_values`

**Inputs** filters, fieldname.

**Explicit results** list(values) when isinstance(values, str), otherwise values.

**Local steps**

- Set values from (filters.get(fieldname) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(fieldname) → list().
- Return list(values) when isinstance(values, str), otherwise values.
  - Value choice on isinstance(values, str) — true gives list(values), false gives values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L969)

<a id="op-04f3900daa1211"></a>
### Get data

`operation_enterprise_stock_report_item_variant_details_business_behavior_get_data`

**Inputs** templates, filters.

**Record and data access** read “Item” via get\_list.

**State and service calls** msgprint with translated “There are no item variants for the selected filters”.

**Explicit results** list() · data.

**Local steps**

- If not templates.
  - Return list().
- Set variant\_results from Platform.get\_list(“Item”, fields = list(“name”, “variant\_of”, “item\_group”, “stock\_uom”), filters = mapping(“variant\_of” → list(“in”, list(templates)), “disabled” → 0)).
- If not variant\_results.
  - Evaluate Platform.msgprint(translated “There are no item variants for the selected filters”).
  - Return list().
- Set variant\_list from list of variant.name for variant drawn from variant\_results.
  - Draw variant from variant\_results.
- Set warehouses from get\_selected\_warehouses(filters).
- Set open\_orders from get\_open\_sales\_orders(variant\_list, warehouses).
- Set variant\_rows from get\_variant\_rows(variant\_results, warehouses, open\_orders).
- Set rows\_by\_template from mapping().
- For each row in variant\_rows.
  - Evaluate rows\_by\_template.setdefault(row at “template”, list()).append(row).
- Set data from list().
- For each tuple(template, item\_group) in templates.items().
  - If rows bound to rows\_by\_template.get(template).
    - Evaluate data.append(get\_template\_row(template, item\_group, rows, open\_orders)).
    - Evaluate data.extend(rows).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L194)

<a id="op-da7b954a4b80cb"></a>
### Get variant rows

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_variant_rows`

**Inputs** variant\_results, warehouses, open\_orders.

**Explicit results** variant\_rows.

**Local steps**

- Set variant\_list from list of variant.name for variant drawn from variant\_results.
  - Draw variant from variant\_results.
- Set stock\_details\_map from get\_stock\_details\_map(variant\_list, warehouses).
- Set buying\_price\_map from get\_buying\_price\_map(variant\_list).
- Set selling\_price\_map from get\_selling\_price\_map(variant\_list).
- Set currency from get\_report\_currency().
- Set attr\_val\_map from get\_attribute\_values\_map(variant\_list).
- Set variant\_rows from list().
- For each variant in variant\_results.
  - Set stock\_details from stock\_details\_map.get(variant.name, mapping()).
  - Evaluate variant\_rows.append(mapping(expand mapping of Platform.scrub(attribute) → value for tuple(attribute, value) drawn from nested operand in the contract.get(nested operand in the contract.name, mapping()).ite ….
    - Draw tuple(attribute, value) from attr\_val\_map.get(variant.name, mapping()).items().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in stock\_details.get(“Inventory”) → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in stock\_details.get(“In Production”) → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in buying\_price\_map.get(variant.name) → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in selling\_price\_map.get(variant.name) → 0.
- Return variant\_rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L977)

<a id="op-01e2f59545428f"></a>
### Get template row

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_template_row`

**Inputs** template, item\_group, rows, open\_orders.

**Explicit results** template\_row.

**Local steps**

- Set orders from set().union(expanded generator of open\_orders.get(row at “variant\_name”, tuple()) for row drawn from rows).
  - Draw row from rows.
- Set template\_row from mapping(“variant\_name” → template, “item\_group” → item\_group, “indent” → 0, “open\_orders” → len(orders), …).
- Set stock\_uoms from set of row at “stock\_uom” for row drawn from rows.
  - Draw row from rows.
- If len(stock\_uoms) equals 1.
  - Evaluate template\_row.update(stock\_uom = stock\_uoms.pop(), current\_stock = sum(generator of row at “current\_stock” for row drawn from rows), in\_production = sum(generator of row at “in\_production” for row drawn from rows)).
    - Draw row from rows.
    - Draw row from rows.
- Return template\_row.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L975)

<a id="op-a3be79cdf32194"></a>
### Get columns

`operation_enterprise_stock_report_item_variant_details_business_behavior_get_columns`

**Inputs** templates.

**Record and data access** read “Item Variant Attribute” via get\_all.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “variant\_name”, “label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “item\_group”, “label” → translated “Item Group”, “fieldtype” → “L ….
- Set attributes from Platform.get\_all(“Item Variant Attribute”, filters = mapping(“parent” → list(“in”, templates), “parenttype” → “Item”), pluck = “attribute”, order\_by = “idx”).
- For each attribute in dict.fromkeys(attributes).
  - Evaluate columns.append(mapping(“fieldname” → Platform.scrub(attribute), “label” → attribute, “fieldtype” → “Data”, “width” → 100)).
- Set additional\_columns from list(mapping(“fieldname” → “avg\_buying\_price\_list\_rate”, “label” → translated “Avg. Buying Price List Rate”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“fieldname” → “avg\_selling\_price\_l ….
- Evaluate columns.extend(additional\_columns).
- Return columns.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L193)
