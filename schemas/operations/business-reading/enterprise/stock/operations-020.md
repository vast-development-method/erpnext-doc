# Inventory and warehouses · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Inventory dimension

[Record definition](../../../../data/record-types/inventory_dimension.json)

<a id="op-ce886e7b2220de"></a>
### Get inventory dimensions

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_get_inventory_dimensions`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), request\_cache.

**Record and data access** read “Inventory Dimension” via get\_all.

**Explicit results** Platform.get\_all(“Inventory Dimension”, fields = list(“target\_fieldname as fieldname”, “source\_fieldname”, “reference\_document as doctype”, “validate\_negative\_stock”, …), order\_by = “creation”, distinct = true).

**Local steps**

- Return Platform.get\_all(“Inventory Dimension”, fields = list(“target\_fieldname as fieldname”, “source\_fieldname”, “reference\_document as doctype”, “validate\_negative\_stock”, …), order\_by = “creation”, distinct = true).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L6390) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1016)

<a id="op-46c408eb155a9f"></a>
### Delete dimension

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_delete_dimension`

**Inputs** dimension.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Inventory Dimension” via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(“Inventory Dimension”, dimension).
- Evaluate doc.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1012)

<a id="op-eac16cb65c6ed2"></a>
### Get parent fields

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_get_parent_fields`

**Inputs** child\_doctype, dimension\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** fields.

**Local steps**

- Evaluate Platform.has\_permission(“Inventory Dimension”, “read”, throw = true).
- Set parent\_doctypes from Platform.get\_all(“DocField”, fields = list(“parent”), filters = mapping(“options” → child\_doctype)).
- Set fields from list().
- Evaluate fields.extend(Platform.get\_all(“DocField”, fields = list(“fieldname as value”, “label”), filters = mapping(“options” → dimension\_name, “parent” → tuple(“in”, list of d.parent for d drawn from parent\_doctypes)))).
  - Draw d from parent\_doctypes.
- Evaluate fields.extend(Platform.get\_all(“Custom Field”, fields = list(“fieldname as value”, “label”), filters = mapping(“options” → dimension\_name, “dt” → tuple(“in”, list of d.parent for d drawn from parent\_doctypes)))).
  - Draw d from parent\_doctypes.
- Return fields.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Inventory Dimension”, “read”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1018)

<a id="op-d2713f104e0193"></a>
### Create dimension custom fields

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_create_dimension_custom_fields`

**Inputs** custom\_fields.

**Local steps**

- Set Platform.flags.in\_create\_custom\_fields from true.
- Attempt the following.
  - For each tuple(doctype, fields) in custom\_fields.items().
    - For each df in fields.
      - Evaluate save\_dimension\_custom\_field(doctype, df).
- On exit, including pending return or failure.
  - Set Platform.flags.in\_create\_custom\_fields from false.
- For each doctype in custom\_fields.
  - Evaluate Platform.clear\_cache(doctype = doctype).
  - Evaluate Platform.db.updatedb(doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L268)

<a id="op-0f43751ebe6cd4"></a>
### Save dimension custom field

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_save_dimension_custom_field`

**Inputs** doctype, df.

**Record and data access** read “Custom Field” via get\_value · resolve a document from “Custom Field” via get\_doc · resolve a document from mapping(“doctype” → “Custom Field”, “dt” → doctype, “permlevel” → 0, “fieldtype” → “Data”, …) via get\_doc.

**State and service calls** call save on custom\_field.

**Explicit results** no value.

**Local steps**

- Set name from Platform.db.get\_value(“Custom Field”, mapping(“dt” → doctype, “fieldname” → df at “fieldname”)).
- If name.
  - Set custom\_field from Platform.get\_doc(“Custom Field”, name).
  - Set original\_values from custom\_field.as\_dict().
  - Evaluate custom\_field.update(df).
  - If custom\_field.as\_dict() equals original\_values.
    - Return no value.
- Otherwise.
  - Set custom\_field from Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → doctype, “permlevel” → 0, “fieldtype” → “Data”, …)).
- Set custom\_field.flags.ignore\_permissions from true.
- Evaluate custom\_field.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L276)

<a id="op-2b7a2a606d2426"></a>
### Delete dimension custom field

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_delete_dimension_custom_field`

**Inputs** name.

**Record and data access** read “Custom Field” via get\_value.

**State and service calls** request delete\_doc for “Custom Field”.

**Local steps**

- Set field from Platform.db.get\_value(“Custom Field”, name, list(“dt”, “fieldname”), as\_dict = true).
- Evaluate Platform.delete\_doc(“Custom Field”, name, ignore\_permissions = true, ignore\_on\_trash = true).
- Evaluate delete\_property\_setter(field.dt, field\_name = field.fieldname).
- Evaluate remove\_field\_from\_doctype\_layouts(field.dt, field.fieldname).
- Evaluate Platform.clear\_cache(doctype = field.dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L772) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L269)

<a id="op-a87d80bd7fb03e"></a>
### Remove field from doctype layouts

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_remove_field_from_doctype_layouts`

**Inputs** doctype, fieldname.

**Record and data access** read “DocType Layout” via get\_all · resolve a document from “DocType Layout” via get\_doc.

**State and service calls** call save on layout\_doc.

**Local steps**

- For each layout in Platform.get\_all(“DocType Layout”, filters = mapping(“document\_type” → doctype), pluck = “name”).
  - Set layout\_doc from Platform.get\_doc(“DocType Layout”, layout).
  - Set rows from list of row for row drawn from layout\_doc.fields where row.fieldname equals fieldname.
    - Draw row from layout\_doc.fields, keep a combination only if (row.fieldname equals fieldname).
  - If rows.
    - Evaluate layout\_doc.remove(rows at 0).
    - Set layout\_doc.flags.ignore\_permissions from true.
    - Evaluate layout\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L778) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L275)

## Record · Item

[Record definition](../../../../data/record-types/item.json)

<a id="op-7903f0eb128e63"></a>
### Item.onload

`operation_enterprise_stock_record_definitions_item_business_behavior_item_onload`

**Inputs** self.

**Local steps**

- Evaluate self.set\_onload(“stock\_exists”, self.stock\_ledger\_created()).
- Evaluate self.set\_onload(“asset\_naming\_series”, get\_asset\_naming\_series()).
- Evaluate self.set\_onload(“current\_valuation\_method”, get\_valuation\_method(self.name, Enterprise.get\_default\_company())).
- Evaluate self.set\_onload(“asset\_exists”, self.has\_submitted\_assets()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [stock ledger created](operations-021.md#op-abf65c7800ee6f), [has submitted assets](operations-021.md#op-0751d30630ee97).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1101)

<a id="op-9f86a3cfe4e02f"></a>
### Item.autoname

`operation_enterprise_stock_record_definitions_item_business_behavior_item_autoname`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Local steps**

- If Platform.db.get\_default(“item\_naming\_by”) equals “Naming Series”.
  - If self.variant\_of.
    - If not self.item\_code.
      - Set template\_item\_name from Platform.db.get\_value(“Item”, self.variant\_of, “item\_name”).
      - Evaluate make\_variant\_item\_code(self.variant\_of, template\_item\_name, self).
  - Otherwise.
    - Bind dependencies set\_name\_by\_naming\_series.
    - Evaluate set\_name\_by\_naming\_series(self).
    - Set self.item\_code from self.name.
- Set self.item\_code from strip(self.item\_code).
- Set self.name from self.item\_code.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0730.json#L5122) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1089)

<a id="op-3ebde3b23884ba"></a>
### Item.after insert

`operation_enterprise_stock_record_definitions_item_business_behavior_item_after_insert`

**Inputs** self.

**Record and data access** resolve a document from “Item Group” via get\_cached\_doc · resolve a document from “Brand” via get\_cached\_doc.

**State and service calls** msgprint with translated “Item Price created at rate {0}”.format(Platform.format(self.standard\_rate, mapping(“fieldtype” → “Currency”))) · enqueue with self.set\_opening\_stock · msgprint with translated “Opening stock creation has been queued and will be created in the background. Please check the Stock Reconci …”.

**Local steps**

- If (self.standard\_rate and not self.has\_variants).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.standard\_rate → not self.has\_variants.
  - Bind dependencies get\_brand\_defaults.
  - Bind dependencies get\_item\_group\_defaults.
  - Set group\_rows from Platform.get\_cached\_doc(“Item Group”, self.item\_group).item\_group\_defaults.
  - Set brand\_rows from Platform.get\_cached\_doc(“Brand”, self.brand).brand\_defaults when self.brand, otherwise list().
    - Value choice on self.brand — true gives Platform.get\_cached\_doc(“Brand”, self.brand).brand\_defaults, false gives list().
  - Set companies from set of row.company for row drawn from tuple(expanded self.item\_defaults, expanded group\_rows, expanded brand\_rows).
    - Draw row from tuple(expanded self.item\_defaults, expanded group\_rows, expanded brand\_rows).
  - Set price\_lists from set of self.get\_selling\_price\_list((get\_item\_defaults(nested operand in the contract.name, company).get(“default\_price\_list”) or get\_item\_group\_defaults(nested operand in the contract.name, company).get(“d ….
    - Draw company from (companies or set(no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(self.name, company).get(“default\_price\_list”) → get\_item\_group\_defaults(self.name, company).get(“default\_price\_list”) → get\_brand\_defaults(self.name, company).get(“default\_price\_list”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in companies → set(no value).
  - If list of price\_list for price\_list drawn from price\_lists where self.add\_price(price\_list).
    - Draw price\_list from price\_lists, keep a combination only if (self.add\_price(price\_list)).
    - Evaluate Platform.msgprint(translated “Item Price created at rate {0}”.format(Platform.format(self.standard\_rate, mapping(“fieldtype” → “Currency”))), indicator = “green”, alert = true).
- If self.opening\_stock.
  - If (self.opening\_stock &gt; 10000 and self.has\_serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.opening\_stock &gt; 10000 → self.has\_serial\_no.
    - Evaluate Platform.enqueue(self.set\_opening\_stock, queue = “long”, timeout = 600, job\_name = formatted text set\_opening\_stock\_for\_{self.name}, enqueue\_after\_commit = true).
    - Evaluate Platform.msgprint(translated “Opening stock creation has been queued and will be created in the background. Please check the Stock Reconci …”, indicator = “orange”, alert = true).
  - Otherwise.
    - Evaluate self.set\_opening\_stock().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get selling price list](operations-020.md#op-80d71d342c1c3c), [add price](operations-020.md#op-de233a7286ecaf), [set opening stock](operations-020.md#op-872b8466a0c0cf).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item Group”, self.item\_group), Platform.get\_cached\_doc(“Brand”, self.brand) · service or queued work from Platform.enqueue(self.set\_opening\_stock, queue = “long”, timeout = 600, job\_name = formatted text set\_opening\_stock\_for\_{self.name}, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1087)

<a id="op-c497d9aa8e9c7f"></a>
### Item.validate

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**Local steps**

- If not self.item\_name.
  - Set self.item\_name from self.item\_code.
- Evaluate self.validate\_uom().
- Evaluate self.validate\_description().
- Evaluate self.add\_default\_uom\_in\_conversion\_factor\_table().
- Evaluate self.validate\_conversion\_factor().
- Evaluate self.validate\_item\_type().
- Evaluate self.validate\_naming\_series().
- If self.is\_new().
  - Evaluate self.validate\_opening\_stock().
- Evaluate self.validate\_shelf\_life().
- Evaluate self.check\_for\_active\_boms().
- Evaluate self.fill\_customer\_code().
- Evaluate self.check\_item\_tax().
- Evaluate self.validate\_barcode().
- Evaluate self.validate\_warehouse\_for\_reorder().
- Evaluate self.update\_bom\_item\_desc().
- Evaluate self.validate\_variant().
- Evaluate self.validate\_has\_variants().
- Evaluate self.validate\_attributes\_in\_variants().
- Evaluate self.validate\_stock\_exists\_for\_template\_item().
- Evaluate self.validate\_attributes().
- Evaluate self.validate\_variant\_attributes().
- Evaluate self.validate\_variant\_based\_on\_change().
- Evaluate self.validate\_fixed\_asset().
- Evaluate self.clear\_retain\_sample().
- Evaluate self.validate\_retain\_sample().
- Evaluate self.validate\_uom\_conversion\_factor().
- Evaluate self.validate\_customer\_provided\_part().
- Evaluate self.update\_defaults\_from\_item\_group().
- Evaluate self.validate\_item\_defaults().
- Evaluate self.validate\_auto\_reorder\_enabled\_in\_stock\_settings().
- Evaluate self.validate\_serial\_and\_batch\_no\_enabled\_in\_stock\_settings().
- Evaluate self.cant\_change().
- Evaluate self.validate\_serialized\_change\_with\_bundle().
- Evaluate self.validate\_serial\_no\_wise\_valuation().
- Evaluate self.set\_valuation\_method\_for\_serial\_no\_wise\_valuation().
- Evaluate self.validate\_item\_tax\_net\_rate\_range().
- If not self.is\_new().
  - Set self.old\_item\_group from Platform.db.get\_value(self.doctype, self.name, “item\_group”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate uom](operations-022.md#op-ac7de5a361162e), [validate description](operations-020.md#op-5995b32de337c1), [add default uom in conversion factor table](operations-020.md#op-8235864930bf7c), [validate conversion factor](operations-021.md#op-53f939702d3995), [validate item type](operations-021.md#op-95b90bebcf4323), [validate naming series](operations-021.md#op-75bb239bd857f5), [validate opening stock](operations-020.md#op-55f7bfe536daf8), [validate shelf life](operations-020.md#op-8e652ef2bf10fb), [check for active boms](operations-021.md#op-05079363241a04), [fill customer code](operations-021.md#op-b3b22ac834f1d1), [check item tax](operations-021.md#op-233eb1242cdf83), [validate barcode](operations-021.md#op-d0ac9e027dc852), [validate warehouse for reorder](operations-021.md#op-c271a1f91794f0), [update bom item desc](operations-021.md#op-e5e1da21c1eb80), [validate variant](operations-022.md#op-22d1b8b1ada25d), [validate has variants](operations-022.md#op-8825da78576776), [validate attributes in variants](operations-022.md#op-a998600de9c36d), [validate stock exists for template item](operations-022.md#op-06b02fbf1ef1d6), [validate attributes](operations-022.md#op-a0d8916831df04), [validate variant attributes](operations-022.md#op-bdfa132e196be7), [validate variant based on change](operations-022.md#op-c35659d0d38f08), [validate fixed asset](operations-020.md#op-631f0f1e02e3ef), [clear retain sample](operations-020.md#op-8ab35aa7b21c81), [validate retain sample](operations-020.md#op-461851a0687f15), [validate uom conversion factor](operations-022.md#op-8e47278240a761), [validate customer provided part](operations-020.md#op-3fe2279af81718), [update defaults from item group](operations-022.md#op-368fb1c3a19425), [validate item defaults](operations-021.md#op-26ada0bca18e51), [validate auto reorder enabled in stock settings](operations-022.md#op-3296f4a0d223de), [validate serial and batch no enabled in stock settings](operations-022.md#op-a555df81c8423b), [cant change](operations-022.md#op-58446d9d1181d0), [validate serialized change with bundle](operations-022.md#op-eb6442aa99a05d), [validate serial no wise valuation](operations-022.md#op-c5c157da406349), [set valuation method for serial no wise valuation](operations-022.md#op-c9c45c5bcd44cf), [validate item tax net rate range](operations-020.md#op-0d6b398f56760a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1111)

<a id="op-435098f5718e2d"></a>
### Item.on update

`operation_enterprise_stock_record_definitions_item_business_behavior_item_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_valuation\_method\_cache.
- Evaluate self.update\_variants().
- Evaluate self.update\_item\_price().
- Evaluate clear\_valuation\_method\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update variants](operations-022.md#op-f14be24c9ee4fd), [update item price](operations-021.md#op-44bf061b5558c1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1100)

<a id="op-5995b32de337c1"></a>
### Item.validate description

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_description`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Image in the description has been removed. To disable this behavior, uncheck "{0}" in {1}.”.format(Platform.get\_meta(“Stock Settings”).get\_label(“clean\_description\_html”), get\_link\_to\_form(“Sto ….

**Local steps**

- If (cint(Platform.get\_single\_value(“Stock Settings”, “clean\_description\_html”)) and self.description differs from self.item\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(Platform.get\_single\_value(“Stock Settings”, “clean\_description\_html”)) → self.description differs from self.item\_name.
  - Set old\_desc from self.description.
  - Set self.description from clean\_html(self.description).
  - If (old\_desc and self.description and “&lt;img src” belongs to old\_desc and “&lt;img src” does not belong to self.description).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_desc → self.description → “&lt;img src” belongs to old\_desc → “&lt;img src” does not belong to self.description.
    - Evaluate Platform.msgprint(translated “Image in the description has been removed. To disable this behavior, uncheck "{0}" in {1}.”.format(Platform.get\_meta(“Stock Settings”).get\_label(“clean\_description\_html”), get ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “clean\_description\_html”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1120)

<a id="op-3fe2279af81718"></a>
### Item.validate customer provided part

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_customer_provided_part`

**Inputs** self.

**Explicit failure paths** validation helper — translated “"Customer Provided Item" cannot be Purchase Item also” · validation helper — translated “"Customer Provided Item" cannot have Valuation Rate”.

**Local steps**

- If self.is\_customer\_provided\_item.
  - If self.is\_purchase\_item.
    - Call the validation error handler Platform.throw(translated “"Customer Provided Item" cannot be Purchase Item also”).
  - If self.valuation\_rate.
    - Call the validation error handler Platform.throw(translated “"Customer Provided Item" cannot have Valuation Rate”).
  - Set self.default\_material\_request\_type from “Customer Provided”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0730.json#L7110) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1119)

<a id="op-80d71d342c1c3c"></a>
### Item.get selling price list

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_get_selling_price_list`

**Inputs** self, price\_list = no value.

**Record and data access** read “Price List” via get\_cached\_value · read “Selling Settings” via get\_single\_value · read “Price List” via get\_value.

**Explicit results** price\_list · (Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”) or Platform.db.get\_value(“Price List”, “Standard Selling”)).

**Local steps**

- If (price\_list and Platform.get\_cached\_value(“Price List”, price\_list, “selling”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list → Platform.get\_cached\_value(“Price List”, price\_list, “selling”).
  - Return price\_list.
- Return (Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”) or Platform.db.get\_value(“Price List”, “Standard Selling”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”) → Platform.db.get\_value(“Price List”, “Standard Selling”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, “selling”), Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L282)

<a id="op-de233a7286ecaf"></a>
### Item.add price

`operation_enterprise_stock_record_definitions_item_business_behavior_item_add_price`

**Inputs** self, price\_list = no value.

**Record and data access** read “Price List” via get\_cached\_value · resolve a document from mapping(“doctype” → “Item Price”, “price\_list” → price\_list, “item\_code” → self.name, “uom” → self.stock\_uom, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Item Price”, “price\_list” → price\_list, “item\_code” → self.name, “uom” → self.stock\_uom, …)).

**Explicit results** false · true.

**Local steps**

- Set price\_list from self.get\_selling\_price\_list(price\_list).
- If not price\_list.
  - Return false.
- Set default\_currency from Enterprise.get\_default\_currency().
- Set currency from (Platform.get\_cached\_value(“Price List”, price\_list, “currency”) or default\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Price List”, price\_list, “currency”) → default\_currency.
- Set price\_list\_rate from flt(self.standard\_rate).
- If (default\_currency and currency differs from default\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_currency → currency differs from default\_currency.
  - Set exchange\_rate from flt(get\_exchange\_rate(currency, default\_currency, args = “for\_selling”)).
  - If not exchange\_rate.
    - Return false.
  - Set price\_list\_rate from flt((price\_list\_rate ÷ exchange\_rate), Platform.get\_precision(“Item Price”, “price\_list\_rate”, currency)).
- Evaluate Platform.get\_doc(mapping(“doctype” → “Item Price”, “price\_list” → price\_list, “item\_code” → self.name, “uom” → self.stock\_uom, …)).insert().
- Return true.

**Methods declared on this owner** [get selling price list](operations-020.md#op-80d71d342c1c3c).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, “currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1086)

<a id="op-55f7bfe536daf8"></a>
### Item.validate opening stock

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_validate_opening_stock`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial Number Series is mandatory when entering Opening Stock for a serialized item.” · validation helper — translated “Enable Automatically Create New Batch when entering Opening Stock for a batched item.”.

**Local steps**

- If (not self.is\_stock\_item or not self.opening\_stock).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_stock\_item → not self.opening\_stock.
  - Return no value.
- If (self.has\_serial\_no and not self.serial\_no\_series).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → not self.serial\_no\_series.
  - Call the validation error handler Platform.throw(translated “Serial Number Series is mandatory when entering Opening Stock for a serialized item.”).
- If (self.has\_batch\_no and not self.create\_new\_batch).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_batch\_no → not self.create\_new\_batch.
  - Call the validation error handler Platform.throw(translated “Enable Automatically Create New Batch when entering Opening Stock for a batched item.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L790) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L287)

<a id="op-872b8466a0c0cf"></a>
### Item.set opening stock

`operation_enterprise_stock_record_definitions_item_business_behavior_item_set_opening_stock`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “Warehouse” via get\_value · read “Account” via get\_value.

**State and service calls** msgprint with translated “Opening Stock reconciliation created with zero valuation rate: {0}”.format(stock\_reco\_link) · msgprint with translated “Opening Stock reconciliation created: {0}”.format(stock\_reco\_link).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Valuation Rate is mandatory if Opening Stock entered” · validation helper — translated “Please set a Temporary Opening account for company {0} to create an Opening Stock reconciliation.”.format(Platform.bold(default.company)).

**Local steps**

- If not self.is\_stock\_item.
  - Return no value.
- If (self.valuation\_rate is identical to no value and not self.is\_customer\_provided\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valuation\_rate is identical to no value → not self.is\_customer\_provided\_item.
  - Call the validation error handler Platform.throw(translated “Valuation Rate is mandatory if Opening Stock entered”).
- For each default in (self.item\_defaults or list(Platform.\_dict(mapping(“company” → nested operand in the contract.get\_defaults().company)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.item\_defaults → list(Platform.\_dict(mapping(“company” → nested operand in the contract.defaults.get\_defaults().company))).
  - Set default\_warehouse from default.default\_warehouse.
  - If (not default\_warehouse and default.company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not default\_warehouse → default.company.
    - Set default\_warehouse from Platform.get\_cached\_value(“Company”, default.company, “default\_warehouse”).
  - If not default\_warehouse.
    - Set default\_warehouse from Platform.db.get\_value(“Warehouse”, mapping(“warehouse\_name” → translated “Stores”, “company” → default.company)).
  - If default\_warehouse.
    - Set opening\_account from Platform.db.get\_value(“Account”, mapping(“company” → default.company, “account\_type” → “Temporary”, “is\_group” → 0), “name”).
    - If not opening\_account.
      - Call the validation error handler Platform.throw(translated “Please set a Temporary Opening account for company {0} to create an Opening Stock reconciliation.”.format(Platform.bold(default.company))).
    - Set stock\_reco from create\_opening\_stock\_reconciliation(item\_code = self.name, company = default.company, qty = self.opening\_stock, valuation\_rate = self.valuation\_rate, …).
    - Evaluate stock\_reco.add\_comment(“Comment”, translated “Opening Stock”).
    - Set stock\_reco\_link from Platform.utils.get\_link\_to\_form(“Stock Reconciliation”, stock\_reco.name).
    - <a id="op-872b8466a0c0cf-guard-45"></a>If self.valuation\_rate equals 0.
      - Evaluate Platform.msgprint(translated “Opening Stock reconciliation created with zero valuation rate: {0}”.format(stock\_reco\_link), indicator = “orange”, alert = true).
    - Otherwise.
      - Evaluate Platform.msgprint(translated “Opening Stock reconciliation created: {0}”.format(stock\_reco\_link), indicator = “green”, alert = true).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.valuation\_rate equals 0, self.valuation\_rate = 0 selects the branch that requests a message with translated “Opening Stock reconciliation created with zero valuation rate: {0}”.format(stock\_reco\_link). With self.valuation\_rate = 1, the alternative requests a message with translated “Opening Stock reconciliation created: {0}”.format(stock\_reco\_link). [Local guard](#op-872b8466a0c0cf-guard-45)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, default.company, “default\_warehouse”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1104)

<a id="op-631f0f1e02e3ef"></a>
### Item.validate fixed asset

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_fixed_asset`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Fixed Asset Item must be a non-stock item.” · validation helper — translated “Asset Category is mandatory for Fixed Asset item” · validation helper — translated “Cannot be a fixed asset item as Stock Ledger is created.” · validation helper — translated “"Is Fixed Asset" cannot be unchecked, as Asset record exists against the item”.

**Local steps**

- If self.is\_fixed\_asset.
  - If self.is\_stock\_item.
    - Call the validation error handler Platform.throw(translated “Fixed Asset Item must be a non-stock item.”).
  - If not self.asset\_category.
    - Call the validation error handler Platform.throw(translated “Asset Category is mandatory for Fixed Asset item”).
  - If self.stock\_ledger\_created().
    - Call the validation error handler Platform.throw(translated “Cannot be a fixed asset item as Stock Ledger is created.”).
- If (not self.is\_fixed\_asset and not self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_fixed\_asset → not self.is\_new().
  - If self.has\_submitted\_assets().
    - Call the validation error handler Platform.throw(translated “"Is Fixed Asset" cannot be unchecked, as Asset record exists against the item”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [stock ledger created](operations-021.md#op-abf65c7800ee6f), [has submitted assets](operations-021.md#op-0751d30630ee97).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L1426) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1123)

<a id="op-461851a0687f15"></a>
### Item.validate retain sample

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_retain_sample`

**Inputs** self.

**Record and data access** read “Company” via exists.

**Explicit failure paths** validation helper — translated “Please select Sample Retention Warehouse in Company first” · validation helper — translated “{0} Retain Sample is based on batch, please check Has Batch No to retain sample of item”.format(self.item\_code).

**Local steps**

- If (self.retain\_sample and not Platform.db.exists(“Company”, mapping(“sample\_retention\_warehouse” → tuple(“is”, “set”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.retain\_sample → not Platform.db.exists(“Company”, mapping(“sample\_retention\_warehouse” → tuple(“is”, “set”))).
  - Call the validation error handler Platform.throw(translated “Please select Sample Retention Warehouse in Company first”).
- If (self.retain\_sample and not self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.retain\_sample → not self.has\_batch\_no.
  - Call the validation error handler Platform.throw(translated “{0} Retain Sample is based on batch, please check Has Batch No to retain sample of item”.format(self.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L1743) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1130)

<a id="op-8e652ef2bf10fb"></a>
### Item.validate shelf life

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_shelf_life`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} must be greater than zero.”.format(self.get\_label\_from\_fieldname(“shelf\_life\_in\_days”)).

**Local steps**

- If (self.has\_batch\_no and self.has\_expiry\_date and self.create\_new\_batch and cint(self.shelf\_life\_in\_days) ≤ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_batch\_no → self.has\_expiry\_date → self.create\_new\_batch → cint(self.shelf\_life\_in\_days) ≤ 0.
  - Call the validation error handler Platform.throw(translated “{0} must be greater than zero.”.format(self.get\_label\_from\_fieldname(“shelf\_life\_in\_days”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L1986) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1132)

<a id="op-8ab35aa7b21c81"></a>
### Item.clear retain sample

`operation_enterprise_stock_record_definitions_item_business_behavior_item_clear_retain_sample`

**Inputs** self.

**Local steps**

- If not self.has\_batch\_no.
  - Set self.retain\_sample from false.
- If not self.retain\_sample.
  - Set self.sample\_quantity from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L2164) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1094)

<a id="op-8235864930bf7c"></a>
### Item.add default uom in conversion factor table

`operation_enterprise_stock_record_definitions_item_business_behavior_item_add_default_unit_of_measure_in_conversion_factor_table`

**Inputs** self.

**State and service calls** msgprint with translated “Successfully changed Stock UOM, please redefine conversion factors for new UOM.”.

**Local steps**

- If (not self.is\_new() and self.has\_value\_changed(“stock\_uom”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“stock\_uom”).
  - Set self.uoms from list().
  - Evaluate Platform.msgprint(translated “Successfully changed Stock UOM, please redefine conversion factors for new UOM.”, alert = true).
- Set uoms\_list from list of d.uom for d drawn from self.get(“uoms”).
  - Draw d from self.get(“uoms”).
- If self.stock\_uom does not belong to uoms\_list.
  - Evaluate self.append(“uoms”, mapping(“uom” → self.stock\_uom, “conversion\_factor” → 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0731.json#L2264) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1085)

<a id="op-0d6b398f56760a"></a>
### Item.validate item tax net rate range

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_item_tax_net_rate_range`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Taxes row #{0}: {1} cannot be smaller than {2}”.format(tax.idx, bold(translated tax.meta.get\_label(“maximum\_net\_rate”)), bold(translated tax.meta.get\_label(“minimum\_net\_rate”))).

**Local steps**

- For each tax in self.get(“taxes”).
  - If flt(tax.maximum\_net\_rate) &lt; flt(tax.minimum\_net\_rate).
    - Call the validation error handler Platform.throw(translated “Taxes row #{0}: {1} cannot be smaller than {2}”.format(tax.idx, bold(translated nested operand in the contract.meta.get\_label(“maximum\_net\_rate”)), bold(translated nested operand ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1126)
