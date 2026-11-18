# Inventory and warehouses · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item lead time

[Record definition](../../../../data/record-types/item_lead_time.json)

<a id="op-c0235cdba3ba36"></a>
### Item Lead Time.set capacity per day

`operation_enterprise_binding_enterprise_stock_doctype_item_lead_time_item_lead_time_itemleadtime_set_capacity_per_day`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.total\_workstation\_time from ((cint(self.shift\_time\_in\_hours) × cint(self.no\_of\_workstations)) × cint(self.no\_of\_shift)).
- If (self.total\_workstation\_time and cint(self.manufacturing\_time\_in\_mins)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.total\_workstation\_time → cint(self.manufacturing\_time\_in\_mins).
  - Set units\_produced from ((flt(self.total\_workstation\_time) ÷ cint(self.manufacturing\_time\_in\_mins)) × 60).
- Otherwise.
  - If self.has\_manufacturing\_inputs\_changed().
    - Set units\_produced from 0.
  - Otherwise.
    - Return no value.
- Set self.no\_of\_units\_produced from cint(units\_produced).
- Set self.capacity\_per\_day from ceil(((flt(self.daily\_yield) × units\_produced) ÷ 100)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has manufacturing inputs changed](operations-026.md#op-7f80fc3d32a16d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L319)

<a id="op-7f80fc3d32a16d"></a>
### Item Lead Time.has manufacturing inputs changed

`operation_enterprise_binding_enterprise_stock_doctype_item_lead_time_item_lead_time_itemleadtime_has_manufacturing_inputs_changed`

**Inputs** self.

**Explicit results** (not self.is\_new() and any(generator of self.has\_value\_changed(fieldname) for fieldname drawn from MANUFACTURING\_INPUT\_FIELDS)).

**Local steps**

- Return (not self.is\_new() and any(generator of self.has\_value\_changed(fieldname) for fieldname drawn from MANUFACTURING\_INPUT\_FIELDS)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → any(generator of self.has\_value\_changed(fieldname) for fieldname drawn from MANUFACTURING\_INPUT\_FIELDS).
  - Draw fieldname from MANUFACTURING\_INPUT\_FIELDS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L318)

## Record · Item manufacturer

[Record definition](../../../../data/record-types/item_manufacturer.json)

<a id="op-87e050edf1482e"></a>
### Item Manufacturer.validate

`operation_enterprise_stock_record_definitions_item_manufacturer_business_behavior_item_manufacturer_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_entry().
- Evaluate self.manage\_default\_item\_manufacturer().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate entry](operations-026.md#op-fca13e25e7c9bb), [manage default item manufacturer](operations-026.md#op-0f2d8f0aefa34c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0740.json#L3419) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1154)

<a id="op-306cf0748587b0"></a>
### Item Manufacturer.on trash

`operation_enterprise_stock_record_definitions_item_manufacturer_business_behavior_item_manufacturer_on_trash`

**Inputs** self.

**Local steps**

- If self.is\_default.
  - Evaluate self.clear\_item\_default(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear item default](operations-026.md#op-bb51171756b777).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1153)

<a id="op-fca13e25e7c9bb"></a>
### Item Manufacturer.validate duplicate entry

`operation_enterprise_stock_record_definitions_item_manufacturer_business_behavior_item_manufacturer_validate_duplicate_entry`

**Inputs** self.

**Record and data access** read “Item Manufacturer” via exists.

**Explicit failure paths** validation helper — translated “Duplicate entry against the item code {0} and manufacturer {1}”.format(self.item\_code, self.manufacturer).

**Local steps**

- Set filters from mapping(“item\_code” → self.item\_code, “manufacturer” → self.manufacturer, “manufacturer\_part\_no” → self.manufacturer\_part\_no, “name” → tuple(“!=”, self.name)).
- If Platform.db.exists(“Item Manufacturer”, filters).
  - Call the validation error handler Platform.throw(translated “Duplicate entry against the item code {0} and manufacturer {1}”.format(self.item\_code, self.manufacturer)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1155)

<a id="op-0f2d8f0aefa34c"></a>
### Item Manufacturer.manage default item manufacturer

`operation_enterprise_stock_record_definitions_item_manufacturer_business_behavior_item_manufacturer_manage_default_item_manufacturer`

**Inputs** self.

**Local steps**

- Bind dependencies set\_default.
- Set previous from self.get\_doc\_before\_save().
- If (previous and previous.is\_default and self.has\_default\_changed(previous)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.is\_default → self.has\_default\_changed(previous).
  - Evaluate self.clear\_item\_default(previous).
- If self.is\_default.
  - Evaluate set\_default(self, “item\_code”).
  - Evaluate self.set\_item\_default(self.item\_code, self.manufacturer, self.manufacturer\_part\_no).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has default changed](operations-026.md#op-b6590899db6bae), [clear item default](operations-026.md#op-bb51171756b777), [set item default](operations-026.md#op-2bd2c6a7f76450).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1152)

<a id="op-b6590899db6bae"></a>
### Item Manufacturer.has default changed

`operation_enterprise_binding_enterprise_stock_doctype_item_manufacturer_item_manufacturer_itemmanufacturer_has_default_changed`

**Inputs** self, previous.

**Explicit results** any(generator of previous.get(fieldname) differs from self.get(fieldname) for fieldname drawn from fieldnames).

**Local steps**

- Set fieldnames from tuple(“is\_default”, “item\_code”, “manufacturer”, “manufacturer\_part\_no”).
- Return any(generator of previous.get(fieldname) differs from self.get(fieldname) for fieldname drawn from fieldnames).
  - Draw fieldname from fieldnames.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L825) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L322)

<a id="op-bb51171756b777"></a>
### Item Manufacturer.clear item default

`operation_enterprise_binding_enterprise_stock_doctype_item_manufacturer_item_manufacturer_itemmanufacturer_clear_item_default`

**Inputs** self, row.

**Record and data access** read “Item” via get\_value.

**Local steps**

- Set item\_default from Platform.db.get\_value(“Item”, row.item\_code, list(“default\_item\_manufacturer”, “default\_manufacturer\_part\_no”)).
- If tuple((item\_default or tuple())) equals tuple(row.manufacturer, row.manufacturer\_part\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_default → tuple().
  - Evaluate self.set\_item\_default(row.item\_code, no value, no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set item default](operations-026.md#op-2bd2c6a7f76450).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L824) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L321)

<a id="op-2bd2c6a7f76450"></a>
### Item Manufacturer.set item default

`operation_enterprise_binding_enterprise_stock_doctype_item_manufacturer_item_manufacturer_itemmanufacturer_set_item_default`

**Inputs** self, item\_code, manufacturer, manufacturer\_part\_no.

**State and service calls** request set\_value on “Item”.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “write”, doc = item\_code, throw = true).
- Evaluate Platform.db.set\_value(“Item”, item\_code, mapping(“default\_item\_manufacturer” → manufacturer, “default\_manufacturer\_part\_no” → manufacturer\_part\_no)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “write”, doc = item\_code, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L826) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L323)

<a id="op-4cac163659727e"></a>
### Get item manufacturer part no

`operation_enterprise_stock_record_definitions_item_manufacturer_business_behavior_get_item_manufacturer_part_number`

**Inputs** item\_code, manufacturer.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_item\_manufacturer\_part\_no(item\_code, manufacturer).

**Local steps**

- Evaluate Enterprise.require\_permission(“Item”, item\_code).
- Return \_get\_item\_manufacturer\_part\_no(item\_code, manufacturer).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1151)

<a id="op-3e409b8a487b50"></a>
### Get item manufacturer part no

`operation_enterprise_binding_enterprise_stock_doctype_item_manufacturer_item_manufacturer_get_item_manufacturer_part_no`

**Inputs** item\_code, manufacturer.

**Record and data access** read “Item Manufacturer” via get\_value.

**Explicit results** Platform.db.get\_value(“Item Manufacturer”, mapping(“item\_code” → item\_code, “manufacturer” → manufacturer), “manufacturer\_part\_no”).

**Local steps**

- Return Platform.db.get\_value(“Item Manufacturer”, mapping(“item\_code” → item\_code, “manufacturer” → manufacturer), “manufacturer\_part\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L320)

## Record · Item price

[Record definition](../../../../data/record-types/item_price.json)

<a id="op-b6517addc672f4"></a>
### Item Price.validate

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_item().
- Evaluate self.validate\_from\_to\_dates(“valid\_from”, “valid\_upto”).
- Evaluate self.update\_price\_list\_details().
- Evaluate self.clear\_party\_not\_applicable().
- Evaluate self.update\_item\_details().
- Evaluate self.validate\_batch().
- Evaluate self.check\_duplicates().
- Evaluate self.validate\_item\_template().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item](operations-026.md#op-38c6eedea2ecc2), [update price list details](operations-026.md#op-6122b55885b49c), [clear party not applicable](operations-026.md#op-18424a21f614d7), [update item details](operations-026.md#op-af8503bda0c3e2), [validate batch](operations-026.md#op-063cfc56969ccc), [check duplicates](operations-026.md#op-93ee23d731c0ee), [validate item template](operations-026.md#op-8f59d7cc55baa4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1160)

<a id="op-38c6eedea2ecc2"></a>
### Item Price.validate item

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_validate_item`

**Inputs** self.

**Record and data access** read “Item” via exists · read “UOM Conversion Detail” via exists.

**Explicit failure paths** validation helper — translated “Item {0} not found.”.format(self.item\_code) · validation helper — translated “UOM {0} not found in Item {1}”.format(self.uom, self.item\_code).

**Local steps**

- If not Platform.db.exists(“Item”, self.item\_code).
  - Call the validation error handler Platform.throw(translated “Item {0} not found.”.format(self.item\_code)).
- If (self.uom and not Platform.db.exists(“UOM Conversion Detail”, mapping(“parenttype” → “Item”, “parent” → self.item\_code, “uom” → self.uom))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.uom → not Platform.db.exists(“UOM Conversion Detail”, mapping(“parenttype” → “Item”, “parent” → self.item\_code, “uom” → self.uom)).
  - Call the validation error handler Platform.throw(translated “UOM {0} not found in Item {1}”.format(self.uom, self.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0740.json#L4678) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1161)

<a id="op-6122b55885b49c"></a>
### Item Price.update price list details

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_update_price_list_details`

**Inputs** self.

**Record and data access** read “Price List” via get\_value.

**Explicit failure paths** validation helper — formatted text The price list {link} does not exist or is disabled.

**Local steps**

- If self.price\_list.
  - Set price\_list\_details from Platform.db.get\_value(“Price List”, mapping(“name” → self.price\_list, “enabled” → 1), list(“buying”, “selling”, “currency”)).
  - If not price\_list\_details.
    - Set link from Platform.utils.get\_link\_to\_form(“Price List”, self.price\_list).
    - Call the validation error handler Platform.throw(formatted text The price list {link} does not exist or is disabled).
  - Set tuple(self.buying, self.selling, self.currency) from price\_list\_details.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1159)

<a id="op-af8503bda0c3e2"></a>
### Item Price.update item details

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_update_item_details`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Local steps**

- If self.item\_code.
  - Set tuple(self.item\_name, self.item\_description) from Platform.db.get\_value(“Item”, self.item\_code, list(“item\_name”, “description”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0740.json#L5310) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1158)

<a id="op-8f59d7cc55baa4"></a>
### Item Price.validate item template

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_validate_item_template`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Item Price cannot be created for the template item {0}”.format(bold(self.item\_code)).

**Local steps**

- If Platform.get\_cached\_value(“Item”, self.item\_code, “has\_variants”).
  - Call the validation error handler Platform.throw(translated “Item Price cannot be created for the template item {0}”.format(bold(self.item\_code))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “has\_variants”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1162)

<a id="op-93ee23d731c0ee"></a>
### Item Price.check duplicates

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_check_duplicates`

**Inputs** self.

**Explicit failure paths** validation helper with ItemPriceDuplicateItem — translated “Item Price appears multiple times based on Price List, Supplier/Customer, Currency, Item, Batch, UOM, Qty, a …”.

**Local steps**

- If self.get\_duplicate\_price\_query().run().
  - Call the validation error handler Platform.throw(translated “Item Price appears multiple times based on Price List, Supplier/Customer, Currency, Item, Batch, UOM, Qty, a …”, ItemPriceDuplicateItem).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get duplicate price query](operations-026.md#op-e8498a1155feb2).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1157)

<a id="op-e8498a1155feb2"></a>
### Item Price.get duplicate price query

`operation_enterprise_binding_enterprise_stock_doctype_item_price_item_price_itemprice_get_duplicate_price_query`

**Inputs** self.

**Explicit results** query.where(self.get\_match\_condition(item\_price.packing\_unit, item\_price.packing\_unit equals 0)).

**Local steps**

- Set item\_price from Platform.qb.DocType(“Item Price”).
- Set query from nested operand in the contract.qb.from\_(item\_price).select(item\_price.price\_list\_rate).where(((item\_price.item\_code equals self.item\_code bitwise and item\_price.price\_list equals self.price\_list) bitwise a ….
- For each field in tuple(“uom”, “valid\_from”, “customer”, “supplier”, …).
  - Set query from query.where(self.get\_match\_condition(item\_price at field, Cast\_(item\_price at field, “varchar”) equals empty text)).
- Return query.where(self.get\_match\_condition(item\_price.packing\_unit, item\_price.packing\_unit equals 0)).

**Methods declared on this owner** [get match condition](operations-026.md#op-8e79686a33b68d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L828) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L325)

<a id="op-8e79686a33b68d"></a>
### Item Price.get match condition

`operation_enterprise_binding_enterprise_stock_doctype_item_price_item_price_itemprice_get_match_condition`

**Inputs** self, column, empty\_condition.

**Explicit results** column equals value · Criterion.any(list(column.isnull(), empty\_condition)).

**Local steps**

- If value bound to self.get(column.name).
  - Return column equals value.
- Return Criterion.any(list(column.isnull(), empty\_condition)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L829) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L326)

<a id="op-18424a21f614d7"></a>
### Item Price.clear party not applicable

`operation_enterprise_binding_enterprise_stock_doctype_item_price_item_price_itemprice_clear_party_not_applicable`

**Inputs** self.

**Local steps**

- If (self.selling and not self.buying).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.selling → not self.buying.
  - Set self.supplier from no value.
- If (self.buying and not self.selling).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.buying → not self.selling.
  - Set self.customer from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L827) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L324)

<a id="op-063cfc56969ccc"></a>
### Item Price.validate batch

`operation_enterprise_binding_enterprise_stock_doctype_item_price_item_price_itemprice_validate_batch`

**Inputs** self.

**Record and data access** read “Batch” via get\_value.

**Explicit failure paths** validation helper — translated “Batch {0} does not belong to Item {1}”.format(bold(self.batch\_no), bold(self.item\_code)).

**Local steps**

- If (self.batch\_no and Platform.db.get\_value(“Batch”, self.batch\_no, “item”) differs from self.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.batch\_no → Platform.db.get\_value(“Batch”, self.batch\_no, “item”) differs from self.item\_code.
  - Call the validation error handler Platform.throw(translated “Batch {0} does not belong to Item {1}”.format(bold(self.batch\_no), bold(self.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L830) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L327)

<a id="op-f198e2dd425ae6"></a>
### Item Price.before save

`operation_enterprise_stock_record_definitions_item_price_business_behavior_item_price_before_save`

**Inputs** self.

**Local steps**

- Set self.reference from (self.customer or self.supplier).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.customer → self.supplier.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1156)

## Report · Item price stock

<a id="op-2ece2e0e6e0132"></a>
### Execute

`operation_enterprise_stock_report_item_price_stock_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate Platform.has\_permission(“Item Price”, “read”, throw = true).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns().
- Set data from get\_data(filters, columns).
- Return tuple(columns, data).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item Price”, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L168)

<a id="op-5260e0b83438bd"></a>
### Get columns

`operation_enterprise_stock_report_item_price_stock_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L169)
