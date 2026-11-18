# Inventory and warehouses · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Item variant details

<a id="op-ecf6b94df4b1e4"></a>
### Get selected warehouses

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_selected_warehouses`

**Inputs** filters.

**Explicit results** list(set of child for warehouse drawn from get\_filter\_values(filters, “warehouse”), then child drawn from get\_child\_warehouses(warehouse)).

**Local steps**

- Return list(set of child for warehouse drawn from get\_filter\_values(filters, “warehouse”), then child drawn from get\_child\_warehouses(warehouse)).
  - Draw warehouse from get\_filter\_values(filters, “warehouse”).
  - Draw child from get\_child\_warehouses(warehouse).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L974)

<a id="op-8b64456321ff5b"></a>
### Get open sales orders

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_open_sales_orders`

**Inputs** variants\_list, warehouses.

**Record and data access** read “Sales Order” via get\_list.

**Explicit results** open\_orders.

**Local steps**

- Set order\_filters from list(list(“Sales Order”, “docstatus”, “=”, 1), list(“Sales Order”, “status”, “not in”, list(“Closed”, “Completed”)), list(“Sales Order Item”, “item\_code”, “in”, variants\_list)).
- If warehouses.
  - Evaluate order\_filters.append(list(“Sales Order Item”, “warehouse”, “in”, warehouses)).
- Set open\_sales\_orders from Platform.db.get\_list(“Sales Order”, fields = list(“name”, “′tabSales Order Item′.item\_code”, “′tabSales Order Item′.qty”, “′tabSales Order Item′.delivered\_qty”), filters = order\_filters).
- Set open\_orders from mapping().
- For each row in open\_sales\_orders.
  - If flt(row.delivered\_qty) &lt; flt(row.qty).
    - Evaluate open\_orders.setdefault(row.item\_code, set()).add(row.name).
- Return open\_orders.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L971)

<a id="op-61cfacc6bd27ed"></a>
### Get stock details map

`operation_enterprise_stock_report_item_variant_details_business_behavior_get_stock_details_map`

**Inputs** variant\_list, warehouses.

**Record and data access** read “Bin” via get\_all.

**Explicit results** stock\_details\_map.

**Local steps**

- Set bin\_filters from list(mapping(“item\_code” → list(“in”, variant\_list))).
- If warehouses.
  - Evaluate bin\_filters.append(mapping(“warehouse” → list(“in”, warehouses))).
- If permitted\_warehouses bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Item”).
  - Evaluate bin\_filters.append(mapping(“warehouse” → list(“in”, permitted\_warehouses))).
- Set stock\_details from Platform.db.get\_all(“Bin”, fields = list(mapping(“SUM” → “planned\_qty”, “as” → “planned\_qty”), mapping(“SUM” → “actual\_qty”, “as” → “actual\_qty”), mapping(“SUM” → “projected\_qty”, “as” → “projected\_qty”),  ….
- Set stock\_details\_map from mapping().
- For each row in stock\_details.
  - Set name from row.get(“item\_code”).
  - Set stock\_details\_map at name from mapping(“Inventory” → row.get(“actual\_qty”), “In Production” → row.get(“planned\_qty”)).
- Return stock\_details\_map.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L196)

<a id="op-31710c9628d6e7"></a>
### Get buying price map

`operation_enterprise_stock_report_item_variant_details_business_behavior_get_buying_price_map`

**Inputs** variant\_list.

**Explicit results** get\_price\_map(variant\_list, “buying”).

**Local steps**

- Return get\_price\_map(variant\_list, “buying”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L192)

<a id="op-9fe3848a889d49"></a>
### Get selling price map

`operation_enterprise_stock_report_item_variant_details_business_behavior_get_selling_price_map`

**Inputs** variant\_list.

**Explicit results** get\_price\_map(variant\_list, “selling”).

**Local steps**

- Return get\_price\_map(variant\_list, “selling”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L195)

<a id="op-9b51fc6ce0f667"></a>
### Get price map

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_price_map`

**Inputs** variant\_list, price\_type.

**Explicit results** dict(rows).

**Local steps**

- Set item\_price from Platform.qb.DocType(“Item Price”).
- Set item from Platform.qb.DocType(“Item”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand ….run().
- Return dict(rows).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L972)

<a id="op-4cabcbe1bfa965"></a>
### Get report currency

`operation_enterprise_binding_enterprise_stock_report_item_variant_details_item_variant_details_get_report_currency`

**Inputs** no declared parameters.

**Explicit results** ((company and Enterprise.get\_company\_currency(company)) or Platform.db.get\_default(“currency”)).

**Local steps**

- Set company from Enterprise.get\_default\_company().
- Return ((company and Enterprise.get\_company\_currency(company)) or Platform.db.get\_default(“currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (company and Enterprise.get\_company\_currency(company)) → Platform.db.get\_default(“currency”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → Enterprise.get\_company\_currency(company).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L973)

<a id="op-53606e6e510f12"></a>
### Get attribute values map

`operation_enterprise_stock_report_item_variant_details_business_behavior_get_attribute_values_map`

**Inputs** variant\_list.

**Record and data access** read “Item Variant Attribute” via get\_all.

**Explicit results** attr\_val\_map.

**Local steps**

- Set attribute\_list from Platform.db.get\_all(“Item Variant Attribute”, fields = list(“attribute”, “attribute\_value”, “parent”), filters = mapping(“parent” → list(“in”, variant\_list))).
- Set attr\_val\_map from mapping().
- For each row in attribute\_list.
  - Set name from row.get(“parent”).
  - If not attr\_val\_map.get(name).
    - Set attr\_val\_map at name from mapping().
  - Set attr\_val\_map at name at row.get(“attribute”) from row.get(“attribute\_value”).
- Return attr\_val\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0895.json#L2091) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L191)

## Record · Item variant settings

[Record definition](../../../../data/record-types/item_variant_settings.json)

<a id="op-4a1fe6cf2a8815"></a>
### Item Variant Settings.set default fields

`operation_enterprise_stock_record_definitions_item_variant_settings_business_behavior_item_variant_settings_set_default_fields`

**Inputs** self.

**Local steps**

- Set self.fields from list().
- Set fields from Platform.get\_meta(“Item”).fields.
- Set exclude\_fields from set(“naming\_series”, “item\_code”, “item\_name”, “published\_in\_website”, …).
- For each d in fields.
  - If (not d.no\_copy and d.fieldname does not belong to exclude\_fields and d.fieldtype does not belong to list(“HTML”, “Section Break”, “Column Break”, “Button”, …)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.no\_copy → d.fieldname does not belong to exclude\_fields → d.fieldtype does not belong to list(“HTML”, “Section Break”, “Column Break”, “Button”, …).
    - Evaluate self.append(“fields”, mapping(“field\_name” → d.fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0744.json#L6033) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1233)

<a id="op-d4d06b977af259"></a>
### Item Variant Settings.remove invalid fields for copy fields in variants

`operation_enterprise_stock_record_definitions_item_variant_settings_business_behavior_item_variant_settings_remove_invalid_fields_for_copy_fields_in_variants`

**Inputs** self.

**State and service calls** call save on self.

**Local steps**

- Set fields from list of row for row drawn from self.fields where row.field\_name does not belong to self.invalid\_fields\_for\_copy\_fields\_in\_variants.
  - Draw row from self.fields, keep a combination only if (row.field\_name does not belong to self.invalid\_fields\_for\_copy\_fields\_in\_variants).
- Set self.fields from fields.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0744.json#L6400) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1232)

<a id="op-3b619ea08fd1bf"></a>
### Item Variant Settings.validate

`operation_enterprise_stock_record_definitions_item_variant_settings_business_behavior_item_variant_settings_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot set the field &lt;b&gt;{0}&lt;/b&gt; for copying in variants”.format(d.field\_name).

**Local steps**

- For each d in self.fields.
  - If d.field\_name belongs to self.invalid\_fields\_for\_copy\_fields\_in\_variants.
    - Call the validation error handler Platform.throw(translated “Cannot set the field &lt;b&gt;{0}&lt;/b&gt; for copying in variants”.format(d.field\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0744.json#L6526) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1234)

## Report · Item where used

<a id="op-e111a30c1cdb00"></a>
### Execute

`operation_enterprise_stock_report_item_where_used_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(data), data).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set data from list().
- If filters.get(“item”).
  - Evaluate Platform.has\_permission(“Item”, “read”, doc = filters.item, throw = true).
  - Set data from get\_data(filters).
- Return tuple(get\_columns(data), data).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, doc = filters.item, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L199)

<a id="op-19c42db3ed702e"></a>
### Get columns

`operation_enterprise_stock_report_item_where_used_business_behavior_get_columns`

**Inputs** data = no value.

**Explicit results** hide\_empty\_optional\_columns(columns, (data or list())).

**Local steps**

- Set columns from list(mapping(“fieldname” → “section”, “label” → translated “Section”, “fieldtype” → “Data”, “width” → 110), mapping(“fieldname” → “reference\_type”, “label” → translated “Reference Type”, “fieldtype” → “Dat ….
- Return hide\_empty\_optional\_columns(columns, (data or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data → list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L205)

<a id="op-32e86416a2436b"></a>
### Get data

`operation_enterprise_stock_report_item_where_used_business_behavior_get_data`

**Inputs** filters.

**Explicit results** list of row for row drawn from data where row.related\_item belongs to allowed\_items.

**Local steps**

- Set data from list().
- If (not filters.get(“section”) or filters.section equals WHERE\_USED\_SECTION).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“section”) → filters.section equals WHERE\_USED\_SECTION.
  - Evaluate data.extend(get\_where\_used\_data(filters)).
- If (not filters.get(“section”) or filters.section equals REFERENCES\_SECTION).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“section”) → filters.section equals REFERENCES\_SECTION.
  - Evaluate data.extend(get\_reference\_data(filters)).
- Set allowed\_items from set(get\_permitted\_list(“Item”, filters = mapping(“name” → list(“in”, get\_unique\_names(list of nested operand in the contract.related\_item for row drawn from data))), pluck = “name”)).
  - Draw row from data.
- Return list of row for row drawn from data where row.related\_item belongs to allowed\_items.
  - Draw row from data, keep a combination only if (row.related\_item belongs to allowed\_items).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L206)

<a id="op-9fa85b8b75fe8c"></a>
### Get where used data

`operation_enterprise_stock_report_item_where_used_business_behavior_get_where_used_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set item from filters.item.
- Set data from list().
- Evaluate data.extend(get\_bom\_component\_rows(item, filters.get(“company”))).
- Evaluate data.extend(get\_product\_bundle\_component\_rows(item)).
- Evaluate data.extend(get\_bom\_secondary\_item\_rows(item, filters.get(“company”))).
- Evaluate data.extend(get\_subcontracting\_bom\_rows(item)).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0895.json#L4866) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L215)

<a id="op-0be1bbacf999b9"></a>
### Get reference data

`operation_enterprise_stock_report_item_where_used_business_behavior_get_reference_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set item from filters.item.
- Set data from list().
- Evaluate data.extend(get\_bom\_output\_rows(item, filters.get(“company”))).
- Evaluate data.extend(get\_product\_bundle\_parent\_rows(item)).
- Evaluate data.extend(get\_variant\_rows(item)).
- Evaluate data.extend(get\_item\_alternative\_rows(item)).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0895.json#L5129) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L211)

<a id="op-92d66d7536aea4"></a>
### Get bom component rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_bill_of_materials_component_rows`

**Inputs** item, company = no value.

**Record and data access** read “BOM Item” via get\_all.

**Explicit results** data.

**Local steps**

- Set rows from Platform.get\_all(“BOM Item”, filters = mapping(“item\_code” → item, “parenttype” → “BOM”, “docstatus” → 1), fields = list(“parent”, “idx”, “qty”, “uom”, …), order\_by = “parent asc, idx asc”).
- Set bom\_map from get\_bom\_map(list of row.parent for row drawn from rows, company).
  - Draw row from rows.
- Set data from list().
- For each row in rows.
  - If bom bound to bom\_map.get(row.parent).
    - Evaluate data.append(build\_row(section = WHERE\_USED\_SECTION, reference\_type = translated “BOM Component”, document\_type = “BOM”, document\_name = row.parent, …)).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0895.json#L5368) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L201)

<a id="op-7efbf7dcedf850"></a>
### Get bom secondary item rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_bill_of_materials_secondary_item_rows`

**Inputs** item, company = no value.

**Record and data access** read “BOM Secondary Item” via get\_all.

**Explicit results** data.

**Local steps**

- Set rows from Platform.get\_all(“BOM Secondary Item”, filters = mapping(“item\_code” → item, “parenttype” → “BOM”, “docstatus” → 1), fields = list(“parent”, “idx”, “secondary\_item\_type”, “qty”, …), order\_by = “parent asc, idx asc”).
- Set bom\_map from get\_bom\_map(list of row.parent for row drawn from rows, company).
  - Draw row from rows.
- Set data from list().
- For each row in rows.
  - If bom bound to bom\_map.get(row.parent).
    - Evaluate data.append(build\_row(section = WHERE\_USED\_SECTION, reference\_type = translated “BOM Secondary Item”, document\_type = “BOM”, document\_name = row.parent, …)).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0895.json#L5962) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L204)

<a id="op-6070dfdc8df617"></a>
### Get bom output rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_bill_of_materials_output_rows`

**Inputs** item, company = no value.

**Explicit results** list of build\_row(section = REFERENCES\_SECTION, reference\_type = translated “BOM Output”, document\_type = “BOM”, document\_name = row.name, …) for row drawn from rows.

**Local steps**

- Set filters from mapping(“item” → item, “docstatus” → 1).
- If company.
  - Set filters at “company” from company.
- Set rows from get\_permitted\_list(“BOM”, filters = filters, fields = list(“name”, “item”, “company”, “is\_default”, …), order\_by = “is\_default desc, name asc”).
- Return list of build\_row(section = REFERENCES\_SECTION, reference\_type = translated “BOM Output”, document\_type = “BOM”, document\_name = row.name, …) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L203)

<a id="op-48fa69b292788f"></a>
### Get product bundle component rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_product_bundle_component_rows`

**Inputs** item.

**Record and data access** read “Product Bundle Item” via get\_all.

**Explicit results** data.

**Local steps**

- Set rows from Platform.get\_all(“Product Bundle Item”, filters = mapping(“item\_code” → item, “parenttype” → “Product Bundle”, “docstatus” → 0), fields = list(“parent”, “idx”, “qty”, “uom”), order\_by = “parent asc, idx asc”).
- Set bundle\_map from get\_product\_bundle\_map(list of row.parent for row drawn from rows).
  - Draw row from rows.
- Set data from list().
- For each row in rows.
  - If bundle bound to bundle\_map.get(row.parent).
    - Evaluate data.append(build\_row(section = WHERE\_USED\_SECTION, reference\_type = translated “Product Bundle Component”, document\_type = “Product Bundle”, document\_name = row.parent, …)).
      - Value choice on bundle.disabled — true gives 0, false gives 1.
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L208)

<a id="op-7c97574047d318"></a>
### Get product bundle parent rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_product_bundle_parent_rows`

**Inputs** item.

**Explicit results** list of build\_row(section = REFERENCES\_SECTION, reference\_type = translated “Product Bundle Parent”, document\_type = “Product Bundle”, document\_name = row.name, …) for row drawn from rows.

**Local steps**

- Set rows from get\_permitted\_list(“Product Bundle”, filters = mapping(“new\_item\_code” → item, “docstatus” → 0), fields = list(“name”, “new\_item\_code”, “disabled”), order\_by = “name asc”).
- Return list of build\_row(section = REFERENCES\_SECTION, reference\_type = translated “Product Bundle Parent”, document\_type = “Product Bundle”, document\_name = row.name, …) for row drawn from rows.
  - Draw row from rows.
  - Value choice on row.disabled — true gives 0, false gives 1.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L210)

<a id="op-2eeb6e4584b907"></a>
### Get subcontracting bom rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_subcontracting_bill_of_materials_rows`

**Inputs** item.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each row in get\_permitted\_list(“Subcontracting BOM”, filters = mapping(“service\_item” → item), fields = list(“name”, “is\_active”, “finished\_good”, “service\_item”, …), order\_by = “finished\_good asc, name asc”).
  - Evaluate data.append(build\_row(section = WHERE\_USED\_SECTION, reference\_type = translated “Subcontracting Service Item”, document\_type = “Subcontracting BOM”, document\_name = row.name, …)).
- For each row in get\_permitted\_list(“Subcontracting BOM”, filters = mapping(“finished\_good” → item), fields = list(“name”, “is\_active”, “finished\_good”, “finished\_good\_qty”, …), order\_by = “name asc”).
  - Evaluate data.append(build\_row(section = WHERE\_USED\_SECTION, reference\_type = translated “Subcontracting Finished Good”, document\_type = “Subcontracting BOM”, document\_name = row.name, …)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L212)

<a id="op-8224a7185a74a6"></a>
### Get variant rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_variant_rows`

**Inputs** item.

**Explicit results** list of build\_row(section = REFERENCES\_SECTION, reference\_type = translated “Item Variant”, document\_type = “Item”, document\_name = row.name, …) for row drawn from rows.

**Local steps**

- Set rows from get\_permitted\_list(“Item”, filters = mapping(“variant\_of” → item), fields = list(“name”, “variant\_of”, “disabled”), order\_by = “name asc”).
- Return list of build\_row(section = REFERENCES\_SECTION, reference\_type = translated “Item Variant”, document\_type = “Item”, document\_name = row.name, …) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L214)

<a id="op-7c74668ca64483"></a>
### Get item alternative rows

`operation_enterprise_stock_report_item_where_used_business_behavior_get_item_alternative_rows`

**Inputs** item.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each row in get\_permitted\_list(“Item Alternative”, filters = mapping(“item\_code” → item), fields = list(“name”, “item\_code”, “alternative\_item\_code”), order\_by = “alternative\_item\_code asc”).
  - Evaluate data.append(build\_row(section = REFERENCES\_SECTION, reference\_type = translated “Item Alternative”, document\_type = “Item Alternative”, document\_name = row.name, …)).
- For each row in get\_permitted\_list(“Item Alternative”, filters = mapping(“alternative\_item\_code” → item), fields = list(“name”, “item\_code”, “alternative\_item\_code”), order\_by = “item\_code asc”).
  - Evaluate data.append(build\_row(section = REFERENCES\_SECTION, reference\_type = translated “Alternative For Item”, document\_type = “Item Alternative”, document\_name = row.name, …)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L207)
