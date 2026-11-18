# Inventory and warehouses · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item

[Record definition](../../../../data/record-types/item.json)

<a id="op-251388c7177ae9"></a>
### Item.update template tables

`operation_enterprise_stock_record_definitions_item_business_behavior_item_update_template_tables`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Local steps**

- Set template from Platform.get\_cached\_doc(“Item”, self.variant\_of).
- For each d in template.get(“taxes”).
  - Evaluate self.append(“taxes”, d).
- If not self.get(“reorder\_levels”).
  - For each d in template.get(“reorder\_levels”).
    - Set n from mapping().
    - For each k in tuple(“warehouse”, “warehouse\_reorder\_level”, “warehouse\_reorder\_qty”, “material\_request\_type”).
      - Set n at k from d.get(k).
    - Evaluate self.append(“reorder\_levels”, n).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, self.variant\_of).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L2836) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1109)

<a id="op-53f939702d3995"></a>
### Item.validate conversion factor

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_conversion_factor`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Unit of Measure {0} has been entered more than once in Conversion Factor Table”.format(d.uom) · validation helper — translated “Conversion factor for default Unit of Measure must be 1 in row {0}”.format(d.idx).

**Local steps**

- Set check\_list from list().
- For each d in self.get(“uoms”).
  - If cstr(d.uom) belongs to check\_list.
    - Call the validation error handler Platform.throw(translated “Unit of Measure {0} has been entered more than once in Conversion Factor Table”.format(d.uom)).
  - Otherwise.
    - Evaluate check\_list.append(cstr(d.uom)).
  - If (d.uom and cstr(d.uom) equals cstr(self.stock\_uom) and flt(d.conversion\_factor) differs from 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.uom → cstr(d.uom) equals cstr(self.stock\_uom) → flt(d.conversion\_factor) differs from 1.
    - Call the validation error handler Platform.throw(translated “Conversion factor for default Unit of Measure must be 1 in row {0}”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L3179) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1118)

<a id="op-95b90bebcf4323"></a>
### Item.validate item type

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_item_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “'Has Serial No' can not be 'Yes' for non-stock item”.

**Local steps**

- If (self.has\_serial\_no equals 1 and self.is\_stock\_item equals 0 and not self.is\_fixed\_asset).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no equals 1 → self.is\_stock\_item equals 0 → not self.is\_fixed\_asset.
  - Call the validation error handler Platform.throw(translated “'Has Serial No' can not be 'Yes' for non-stock item”).
- If (self.has\_serial\_no equals 0 and self.serial\_no\_series).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no equals 0 → self.serial\_no\_series.
  - Set self.serial\_no\_series from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1127)

<a id="op-75bb239bd857f5"></a>
### Item.validate naming series

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_naming_series`

**Inputs** self.

**State and service calls** msgprint with translated “The {0} prefix '{1}' already exists. Please change the Serial No Series, otherwise you will get a Duplicate  …”.format(bold(Platform.unscrub(field)), bold(prefix)).

**Explicit failure paths** validation helper — translated “Invalid naming series (. missing) for {0}”.format(Platform.bold(self.meta.get\_field(field).label)).

**Local steps**

- For each field in list(“serial\_no\_series”, “batch\_number\_series”).
  - Set series from self.get(field).
  - If (series and “#” belongs to series and “.” does not belong to series).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in series → “#” belongs to series → “.” does not belong to series.
    - Call the validation error handler Platform.throw(translated “Invalid naming series (. missing) for {0}”.format(Platform.bold(nested operand in the contract.meta.get\_field(field).label))).
  - If (self.is\_new() and series).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → series.
    - Set obj from NamingSeries(series).
    - Set prefix from obj.get\_prefix().
    - Set doctype from Platform.qb.DocType(“Series”).
    - Set query from nested operand in the contract.qb.from\_(doctype).select(doctype.name).where(doctype.name.like(formatted text {prefix}%)).
    - Set prefix\_exists from query.run(as\_dict = true).
    - If prefix\_exists.
      - Evaluate Platform.msgprint(translated “The {0} prefix '{1}' already exists. Please change the Serial No Series, otherwise you will get a Duplicate  …”.format(bold(Platform.unscrub(field)), bold(prefix)), title = tr ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L3750) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1128)

<a id="op-05079363241a04"></a>
### Item.check for active boms

`operation_enterprise_stock_record_definitions_item_business_behavior_item_check_for_active_bills_of_materials`

**Inputs** self.

**Record and data access** read “BOM” via get\_value.

**Explicit failure paths** validation helper — translated “Default BOM ({0}) must be active for this item or its template”.format(bom\_item).

**Local steps**

- If self.default\_bom.
  - Set bom\_item from Platform.db.get\_value(“BOM”, self.default\_bom, “item”).
  - If bom\_item does not belong to tuple(self.name, self.variant\_of).
    - Call the validation error handler Platform.throw(translated “Default BOM ({0}) must be active for this item or its template”.format(bom\_item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L4401) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1092)

<a id="op-b3b22ac834f1d1"></a>
### Item.fill customer code

`operation_enterprise_stock_record_definitions_item_business_behavior_item_fill_customer_code`

**Inputs** self.

**Local steps**

- Set customer\_codes from set(generator of d.ref\_code for d drawn from self.get(“customer\_items”, list())).
  - Draw d from self.get(“customer\_items”, list()).
- Set self.customer\_code from “,”.join(customer\_codes).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L4598) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1096)

<a id="op-233eb1242cdf83"></a>
### Item.check item tax

`operation_enterprise_stock_record_definitions_item_business_behavior_item_check_item_tax`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} entered twice {1} in Item Taxes”.format(Platform.bold(d.item\_tax\_template), formatted text for tax category {Platform.bold(d.tax\_category)} when d.tax\_category, otherwise empty text).

**Local steps**

- Set check\_list from list().
- For each d in self.get(“taxes”).
  - If d.item\_tax\_template.
    - If tuple(d.item\_tax\_template, d.tax\_category) belongs to check\_list.
      - Call the validation error handler Platform.throw(translated “{0} entered twice {1} in Item Taxes”.format(Platform.bold(d.item\_tax\_template), formatted text for tax category {Platform.bold(d.tax\_category)} when d.tax\_category, otherwise empty text)).
        - Value choice on d.tax\_category — true gives formatted text for tax category {Platform.bold(d.tax\_category)}, false gives empty text.
    - Otherwise.
      - Evaluate check\_list.append(tuple(d.item\_tax\_template, d.tax\_category)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L4734) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1093)

<a id="op-d0ac9e027dc852"></a>
### Item.validate barcode

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_barcode`

**Inputs** self.

**Record and data access** execute query text (SELECT, Item Barcode).

**Explicit failure paths** validation helper — translated “Barcode {0} already used in Item {1}”.format(item\_barcode.barcode, duplicate at 0 at 0) · validation helper with InvalidBarcode — translated “Barcode {0} is not a valid {1} code”.format(item\_barcode.barcode, item\_barcode.barcode\_type).

**Local steps**

- Bind dependencies barcodenumber.
- If len(self.barcodes) &gt; 0.
  - For each item\_barcode in self.barcodes.
    - Set options from Platform.get\_meta(“Item Barcode”).get\_options(“barcode\_type”).split(whitespace '\\n').
    - If item\_barcode.barcode.
      - Set duplicate from Platform.db.sql(query text (SELECT, Item Barcode), tuple(item\_barcode.barcode, self.name)).
      - If duplicate.
        - Call the validation error handler Platform.throw(translated “Barcode {0} already used in Item {1}”.format(item\_barcode.barcode, duplicate at 0 at 0)).
      - Set item\_barcode.barcode\_type from empty text when item\_barcode.barcode\_type does not belong to options, otherwise item\_barcode.barcode\_type.
        - Value choice on item\_barcode.barcode\_type does not belong to options — true gives empty text, false gives item\_barcode.barcode\_type.
      - If item\_barcode.barcode\_type.
        - Set barcode\_type from convert\_Enterprise\_to\_barcodenumber(item\_barcode.barcode\_type.replace(“-”, empty text).upper(), item\_barcode.barcode).
        - If barcode\_type belongs to barcodenumber.barcodes().
          - If not barcodenumber.check\_code(barcode\_type, item\_barcode.barcode).
            - Call the validation error handler Platform.throw(translated “Barcode {0} is not a valid {1} code”.format(item\_barcode.barcode, item\_barcode.barcode\_type), InvalidBarcode).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1117)

<a id="op-c271a1f91794f0"></a>
### Item.validate warehouse for reorder

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_warehouse_for_reorder`

**Inputs** self.

**Explicit failure paths** validation helper with DuplicateReorderRows — translated “Row #{0}: A reorder entry already exists for warehouse {1} with reorder type {2}.”.format(d.idx, d.warehouse, d.material\_request\_type) · validation helper — translated “Row #{0}: Please set reorder quantity”.format(d.idx) · validation helper — translated “Row #{0}: The warehouse {1} is not a child warehouse of a group warehouse {2}”.format(d.idx, bold(d.warehouse), bold(d.warehouse\_group)).

**Local steps**

- Set warehouse\_material\_request\_type from list().
- Set \_warehouse\_before\_save from Platform.\_dict().
- If (not self.is\_new() and self.\_doc\_before\_save).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.\_doc\_before\_save.
  - Set \_warehouse\_before\_save from mapping of d.name → tuple(d.warehouse, d.warehouse\_group) for d drawn from (self.\_doc\_before\_save.get(“reorder\_levels”) or list()).
    - Draw d from (self.\_doc\_before\_save.get(“reorder\_levels”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_doc\_before\_save.get(“reorder\_levels”) → list().
- For each d in self.get(“reorder\_levels”).
  - If not d.warehouse\_group.
    - Set d.warehouse\_group from d.warehouse.
  - If tuple(d.get(“warehouse”), d.get(“material\_request\_type”)) does not belong to warehouse\_material\_request\_type.
    - Update warehouse\_material\_request\_type using + list(tuple(d.get(“warehouse”), d.get(“material\_request\_type”))).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Row #{0}: A reorder entry already exists for warehouse {1} with reorder type {2}.”.format(d.idx, d.warehouse, d.material\_request\_type), DuplicateReorderRows).
  - If (d.warehouse\_reorder\_level and not d.warehouse\_reorder\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.warehouse\_reorder\_level → not d.warehouse\_reorder\_qty.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Please set reorder quantity”.format(d.idx)).
  - If (d.warehouse\_group and d.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.warehouse\_group → d.warehouse.
    - If \_warehouse\_before\_save.get(d.name) equals tuple(d.warehouse, d.warehouse\_group).
      - Continue with the next iteration or loop test.
    - Set child\_warehouses from get\_child\_warehouses(d.warehouse\_group).
    - If d.warehouse does not belong to child\_warehouses.
      - Call the validation error handler Platform.throw(translated “Row #{0}: The warehouse {1} is not a child warehouse of a group warehouse {2}”.format(d.idx, bold(d.warehouse), bold(d.warehouse\_group)), title = translated “Incorrect Check in ( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1139)

<a id="op-abf65c7800ee6f"></a>
### Item.stock ledger created

`operation_enterprise_stock_record_definitions_item_business_behavior_item_stock_ledger_created`

**Inputs** self.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).

**Explicit results** self.\_stock\_ledger\_created.

**Local steps**

- If not hasattr(self, “\_stock\_ledger\_created”).
  - Set self.\_stock\_ledger\_created from len(Platform.db.sql(query text (SELECT, Stock Ledger Entry), self.name)).
- Return self.\_stock\_ledger\_created.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1105)

<a id="op-0751d30630ee97"></a>
### Item.has submitted assets

`operation_enterprise_stock_record_definitions_item_business_behavior_item_has_submitted_assets`

**Inputs** self.

**Record and data access** read “Asset” via exists.

**Explicit results** bool(Platform.db.exists(“Asset”, mapping(“item\_code” → self.name, “docstatus” → 1))).

**Local steps**

- Return bool(Platform.db.exists(“Asset”, mapping(“item\_code” → self.name, “docstatus” → 1))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0732.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1098)

<a id="op-44bf061b5558c1"></a>
### Item.update item price

`operation_enterprise_stock_record_definitions_item_business_behavior_item_update_item_price`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - Return no value.
- Evaluate Platform.db.sql(multiline text in the contract, dict(item\_name = self.item\_name, item\_description = self.description, brand = self.brand, item\_code = self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1108)

<a id="op-174e2492c4f922"></a>
### Item.on trash

`operation_enterprise_stock_record_definitions_item_business_behavior_item_on_trash`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**State and service calls** execute query text (DELETE, Bin) · execute query text (DELETE, Item Price) · request delete\_doc for “Item”.

**Local steps**

- Evaluate Platform.db.sql(query text (DELETE, Bin), self.name).
- Evaluate Platform.db.sql(query text (DELETE, Item Price), self.name).
- For each variant\_of in Platform.get\_all(“Item”, filters = mapping(“variant\_of” → self.name)).
  - Evaluate Platform.delete\_doc(“Item”, variant\_of.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1099)

<a id="op-1d3fc0bc0f8088"></a>
### Item.before rename

`operation_enterprise_stock_record_definitions_item_business_behavior_item_before_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**State and service calls** request set\_value on “Item”.

**Local steps**

- If self.item\_name equals old\_name.
  - Evaluate Platform.db.set\_value(“Item”, old\_name, “item\_name”, new\_name).
- If merge.
  - Evaluate self.validate\_properties\_before\_merge(new\_name).
  - Evaluate self.validate\_duplicate\_product\_bundles\_before\_merge(old\_name, new\_name).
  - Evaluate self.validate\_duplicate\_lead\_times\_before\_merge(old\_name, new\_name).
  - Evaluate self.delete\_old\_bins(old\_name, new\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate properties before merge](operations-021.md#op-a46047ddb2916a), [validate duplicate product bundles before merge](operations-021.md#op-a8205d572dedf2), [validate duplicate lead times before merge](operations-021.md#op-842bd6cc161553), [delete old bins](operations-021.md#op-83fb7c5eb02b12).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1090)

<a id="op-eb285041f154d5"></a>
### Item.after rename

`operation_enterprise_stock_record_definitions_item_business_behavior_item_after_rename`

**Inputs** self, old\_name, new\_name, merge.

**State and service calls** msgprint with translated “It can take upto few hours for accurate stock values to be visible after merging items.” · request set\_value on “Item”.

**Local steps**

- If merge.
  - Evaluate self.validate\_duplicate\_item\_in\_stock\_reconciliation(old\_name, new\_name).
  - Evaluate Platform.msgprint(translated “It can take upto few hours for accurate stock values to be visible after merging items.”, indicator = “orange”, title = translated “Note”).
- Evaluate Platform.db.set\_value(“Item”, new\_name, “item\_code”, new\_name).
- If merge.
  - Evaluate self.set\_last\_purchase\_rate(new\_name).
  - Evaluate self.recalculate\_bin\_qty(new\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate item in stock reconciliation](operations-021.md#op-e1007ea087f5ee), [set last purchase rate](operations-021.md#op-ff260064fd596f), [recalculate bin qty](operations-021.md#op-7e1ad4e2c8a3c8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0732.json#L1028) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1088)

<a id="op-83fb7c5eb02b12"></a>
### Item.delete old bins

`operation_enterprise_stock_record_definitions_item_business_behavior_item_delete_old_bins`

**Inputs** self, old\_name, new\_name = no value.

**Record and data access** read “Bin” via get\_all.

**State and service calls** request delete on “Bin”.

**Explicit results** no value.

**Local steps**

- If not new\_name.
  - Evaluate Platform.db.delete(“Bin”, mapping(“item\_code” → old\_name)).
  - Return no value.
- Set target\_warehouses from Platform.get\_all(“Bin”, filters = mapping(“item\_code” → new\_name), pluck = “warehouse”).
- If target\_warehouses.
  - Evaluate Platform.db.delete(“Bin”, mapping(“item\_code” → old\_name, “warehouse” → tuple(“in”, target\_warehouses))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1095)

<a id="op-e1007ea087f5ee"></a>
### Item.validate duplicate item in stock reconciliation

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_duplicate_item_in_stock_reconciliation`

**Inputs** self, old\_name, new\_name.

**Record and data access** execute query text (SELECT, Stock Reconciliation Item).

**Explicit results** no value.

**Explicit failure paths** validation helper with DataValidationError — msg.

**Local steps**

- Set records from Platform.db.sql(query text (SELECT, Stock Reconciliation Item), new\_name, as\_dict = 1).
- If not records.
  - Return no value.
- Set document from translated “Stock Reconciliation” when len(records) equals 1, otherwise translated “Stock Reconciliations”.
  - Value choice on len(records) equals 1 — true gives translated “Stock Reconciliation”, false gives translated “Stock Reconciliations”.
- Set msg from translated “The items {0} and {1} are present in the following {2} :”.format(Platform.bold(old\_name), Platform.bold(new\_name), document).
- Update msg using + “ &lt;br&gt;”.
- Update msg using + (“, ”.join(list of get\_link\_to\_form(“Stock Reconciliation”, d.parent) for d drawn from records) + text in the contract).
  - Draw d from records.
- Update msg using + translated “Note: To merge the items, create a separate Stock Reconciliation for the old item {0}”.format(Platform.bold(old\_name)).
- Call the validation error handler Platform.throw(msg, title = translated “Cannot Merge”, exc = DataValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1121)

<a id="op-a46047ddb2916a"></a>
### Item.validate properties before merge

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_properties_before_merge`

**Inputs** self, new\_name.

**Record and data access** read “Item” via exists · read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Item {0} does not exist”.format(new\_name) · validation helper with DataValidationError — translated “Templates cannot be merged” · validation helper with DataValidationError — msg.

**Local steps**

- If not Platform.db.exists(“Item”, new\_name).
  - Call the validation error handler Platform.throw(translated “Item {0} does not exist”.format(new\_name)).
- Set field\_list from list(“stock\_uom”, “is\_stock\_item”, “has\_serial\_no”, “has\_batch\_no”, …).
- Set new\_properties from list of cstr(d) for d drawn from Platform.db.get\_value(“Item”, new\_name, field\_list).
  - Draw d from Platform.db.get\_value(“Item”, new\_name, field\_list).
- If (self.has\_variants or cint(Platform.db.get\_value(“Item”, new\_name, “has\_variants”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_variants → cint(Platform.db.get\_value(“Item”, new\_name, “has\_variants”)).
  - Call the validation error handler Platform.throw(translated “Templates cannot be merged”, title = translated “Cannot Merge”, exc = DataValidationError).
- If new\_properties differs from list of cstr(self.get(field)) for field drawn from field\_list.
  - Draw field from field\_list.
  - Set msg from translated “To merge, following properties must be same for both items”.
  - Update msg using + (“: \\n” + “, ”.join(list of translated nested operand in the contract.meta.get\_label(fld) for fld drawn from field\_list)).
    - Draw fld from field\_list.
  - Call the validation error handler Platform.throw(msg, title = translated “Cannot Merge”, exc = DataValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1129)

<a id="op-a8205d572dedf2"></a>
### Item.validate duplicate product bundles before merge

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_duplicate_product_bundles_before_merge`

**Inputs** self, old\_name, new\_name.

**Record and data access** read “Product Bundle” via get\_value.

**Explicit failure paths** validation helper with DataValidationError — msg.

**Local steps**

- Set old\_bundle from Platform.get\_value(“Product Bundle”, filters = mapping(“new\_item\_code” → old\_name, “disabled” → 0)).
- Set new\_bundle from Platform.get\_value(“Product Bundle”, filters = mapping(“new\_item\_code” → new\_name, “disabled” → 0)).
- If (old\_bundle and new\_bundle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_bundle → new\_bundle.
  - Set bundle\_link from get\_link\_to\_form(“Product Bundle”, old\_bundle).
  - Set tuple(old\_name, new\_name) from tuple(Platform.bold(old\_name), Platform.bold(new\_name)).
  - Set msg from translated “Please delete Product Bundle {0}, before merging {1} into {2}”.format(bundle\_link, old\_name, new\_name).
  - Call the validation error handler Platform.throw(msg, title = translated “Cannot Merge”, exc = DataValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1122)

<a id="op-842bd6cc161553"></a>
### Item.validate duplicate lead times before merge

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_validate_duplicate_lead_times_before_merge`

**Inputs** self, old\_name, new\_name.

**Record and data access** read “Item Lead Time” via get\_value · read “Item Lead Time” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper with DataValidationError — translated “Please delete Item Lead Time {0}, before merging {1} into {2}”.format(get\_link\_to\_form(“Item Lead Time”, old\_lead\_time), Platform.bold(old\_name), Platform.bold(new\_name)).

**Local steps**

- Set old\_lead\_time from Platform.db.get\_value(“Item Lead Time”, mapping(“item\_code” → old\_name)).
- If not (old\_lead\_time and Platform.db.exists(“Item Lead Time”, mapping(“item\_code” → new\_name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_lead\_time → Platform.db.exists(“Item Lead Time”, mapping(“item\_code” → new\_name)).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Please delete Item Lead Time {0}, before merging {1} into {2}”.format(get\_link\_to\_form(“Item Lead Time”, old\_lead\_time), Platform.bold(old\_name), Platform.bold(new\_name)), title  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L286)

<a id="op-ff260064fd596f"></a>
### Item.set last purchase rate

`operation_enterprise_stock_record_definitions_item_business_behavior_item_set_last_purchase_rate`

**Inputs** self, new\_name.

**State and service calls** request set\_value on “Item”.

**Local steps**

- Set last\_purchase\_rate from get\_last\_purchase\_details(new\_name).get(“base\_net\_rate”, 0).
- Evaluate Platform.db.set\_value(“Item”, new\_name, “last\_purchase\_rate”, last\_purchase\_rate, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1103)

<a id="op-7e1ad4e2c8a3c8"></a>
### Item.recalculate bin qty

`operation_enterprise_stock_record_definitions_item_business_behavior_item_recalculate_bin_quantity`

**Inputs** self, new\_name.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Stock Ledger Entry” via get\_all · read “Bin” via get\_all.

**State and service calls** request set\_single\_value on “Stock Settings” · request delete on “Bin”.

**Local steps**

- Bind dependencies repost\_stock.
- Set existing\_allow\_negative\_stock from Platform.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”).
- Evaluate Platform.db.set\_single\_value(“Stock Settings”, “allow\_negative\_stock”, 1).
- Set repost\_stock\_for\_warehouses from Platform.get\_all(“Stock Ledger Entry”, “warehouse”, filters = mapping(“item\_code” → new\_name), pluck = “warehouse”, distinct = true).
- Set bin\_warehouses from set(Platform.get\_all(“Bin”, filters = mapping(“item\_code” → new\_name), pluck = “warehouse”)).
- Evaluate Platform.db.delete(“Bin”, mapping(“item\_code” → new\_name)).
- For each warehouse in repost\_stock\_for\_warehouses.
  - Evaluate repost\_stock(new\_name, warehouse).
- For each warehouse in (bin\_warehouses − set(repost\_stock\_for\_warehouses)).
  - Evaluate repost\_stock(new\_name, warehouse, only\_bin = true).
- For each warehouse in (bin\_warehouses bitwise or set(repost\_stock\_for\_warehouses)).
  - Evaluate rebuild\_bin\_reservations(new\_name, warehouse).
- Evaluate Platform.db.set\_single\_value(“Stock Settings”, “allow\_negative\_stock”, existing\_allow\_negative\_stock).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1102)

<a id="op-e5e1da21c1eb80"></a>
### Item.update bom item desc

`operation_enterprise_stock_record_definitions_item_business_behavior_item_update_bill_of_materials_item_description`

**Inputs** self.

**State and service calls** execute query text (UPDATE, BOM) · execute a supplied database query.

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - Return no value.
- If self.db\_get(“description”) differs from self.description.
  - Evaluate Platform.db.sql(query text (UPDATE, BOM), tuple(self.description, self.name)).
  - Evaluate Platform.db.sql(multiline text in the contract, tuple(self.description, self.name)).
  - Evaluate Platform.db.sql(multiline text in the contract, tuple(self.description, self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1106)

<a id="op-26ada0bca18e51"></a>
### Item.validate item defaults

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_item_defaults`

**Inputs** self.

**Local steps**

- Evaluate validate\_item\_defaults(self.item\_defaults).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1125)
