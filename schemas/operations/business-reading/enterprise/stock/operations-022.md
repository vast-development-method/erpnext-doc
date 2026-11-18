# Inventory and warehouses · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item

[Record definition](../../../../data/record-types/item.json)

<a id="op-368fb1c3a19425"></a>
### Item.update defaults from item group

`operation_enterprise_stock_record_definitions_item_business_behavior_item_update_defaults_from_item_group`

**Inputs** self.

**Record and data access** resolve a document from “Item Group” via get\_cached\_doc · read “Warehouse” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (self.item\_defaults or not self.item\_group).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.item\_defaults → not self.item\_group.
  - Return no value.
- Set item\_group from Platform.get\_cached\_doc(“Item Group”, self.item\_group).
- If item\_group.item\_group\_defaults.
  - For each item in item\_group.item\_group\_defaults.
    - Evaluate self.append(“item\_defaults”, mapping(“company” → item.company, “default\_warehouse” → item.default\_warehouse, “default\_price\_list” → item.default\_price\_list, “buying\_cost\_center” → item.buying\_cost\_center, …)).
- Otherwise.
  - Set defaults from (Platform.defaults.get\_defaults() or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.defaults.get\_defaults() → mapping().
  - If (defaults.get(“default\_warehouse”) and defaults.company and defaults.company equals Platform.get\_cached\_value(“Warehouse”, defaults.default\_warehouse, “company”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in defaults.get(“default\_warehouse”) → defaults.company → defaults.company equals Platform.get\_cached\_value(“Warehouse”, defaults.default\_warehouse, “company”).
    - Evaluate self.append(“item\_defaults”, mapping(“company” → defaults.get(“company”), “default\_warehouse” → defaults.default\_warehouse)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item Group”, self.item\_group), Platform.get\_cached\_value(“Warehouse”, defaults.default\_warehouse, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1107)

<a id="op-f14be24c9ee4fd"></a>
### Item.update variants

`operation_enterprise_stock_record_definitions_item_business_behavior_item_update_variants`

**Inputs** self.

**Record and data access** read “Item Variant Settings” via get\_single\_value · read “Item” via get\_all.

**State and service calls** msgprint with translated “Item Variants updated” · enqueue with “Enterprise.stock.doctype.item.item.update\_variants”.

**Explicit results** no value.

**Local steps**

- If (self.flags.dont\_update\_variants or Platform.db.get\_single\_value(“Item Variant Settings”, “do\_not\_update\_variants”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.dont\_update\_variants → Platform.db.get\_single\_value(“Item Variant Settings”, “do\_not\_update\_variants”).
  - Return no value.
- If self.has\_variants.
  - Set variants from Platform.db.get\_all(“Item”, fields = list(“item\_code”), filters = mapping(“variant\_of” → self.name)).
  - If variants.
    - If len(variants) ≤ 30.
      - Evaluate update\_variants(variants, self, publish\_progress = false).
      - Evaluate Platform.msgprint(translated “Item Variants updated”).
    - Otherwise.
      - Evaluate Platform.enqueue(“Enterprise.stock.doctype.item.item.update\_variants”, variants = variants, template = self, now = Platform.in\_test, timeout = 600, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Item Variant Settings”, “do\_not\_update\_variants”) · service or queued work from Platform.enqueue(“Enterprise.stock.doctype.item.item.update\_variants”, variants = variants, template = self, now = Platform.in\_test, timeout = 600, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0732.json#L4998) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1110)

<a id="op-22d1b8b1ada25d"></a>
### Item.validate variant

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_variant`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “Item Variant Attribute” via exists · read “Item Variant Attribute” via get\_value · read “Item Attribute Value” via exists.

**Explicit failure paths** validation helper — translated “Item {0} is not a template item.”.format(Platform.bold(self.variant\_of)) · validation helper — translated “Attribute {0} is not valid for the selected template.”.format(Platform.bold(d.attribute)) · validation helper — translated “Attribute {0} is disabled.”.format(Platform.bold(d.attribute)) · validation helper — translated “Attribute Value {0} is not valid for the selected attribute {1}.”.format(Platform.bold(d.attribute\_value), Platform.bold(d.attribute)).

**Local steps**

- If self.variant\_of.
  - Set tuple(has\_variants, based\_on) from Platform.get\_value(“Item”, self.variant\_of, list(“has\_variants”, “variant\_based\_on”)).
  - If not has\_variants.
    - Call the validation error handler Platform.throw(translated “Item {0} is not a template item.”.format(Platform.bold(self.variant\_of))).
  - If based\_on equals “Item Attribute”.
    - Set previous\_doc from self.get\_doc\_before\_save().
    - Set saved\_attributes from set of tuple(row.attribute, row.attribute\_value) for row drawn from previous\_doc.attributes when previous\_doc, otherwise set().
      - Value choice on previous\_doc — true gives set of tuple(row.attribute, row.attribute\_value) for row drawn from previous\_doc.attributes, false gives set().
      - Draw row from previous\_doc.attributes.
    - For each d in self.attributes.
      - If tuple(d.attribute, d.attribute\_value) belongs to saved\_attributes.
        - Continue with the next iteration or loop test.
      - If not Platform.db.exists(“Item Variant Attribute”, mapping(“attribute” → d.attribute, “parent” → self.variant\_of)).
        - Call the validation error handler Platform.throw(translated “Attribute {0} is not valid for the selected template.”.format(Platform.bold(d.attribute))).
      - Set tuple(numeric\_values, disabled) from Platform.get\_value(“Item Variant Attribute”, mapping(“attribute” → d.attribute, “parent” → self.variant\_of), list(“numeric\_values”, “disabled”)).
      - If disabled.
        - Call the validation error handler Platform.throw(translated “Attribute {0} is disabled.”.format(Platform.bold(d.attribute))).
      - If (not numeric\_values and d.attribute\_value and not Platform.db.exists(“Item Attribute Value”, mapping(“parent” → d.attribute, “attribute\_value” → d.attribute\_value))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not numeric\_values → d.attribute\_value → not Platform.db.exists(“Item Attribute Value”, mapping(“parent” → d.attribute, “attribute\_value” → d.attribute\_value)).
        - Call the validation error handler Platform.throw(translated “Attribute Value {0} is not valid for the selected attribute {1}.”.format(Platform.bold(d.attribute\_value), Platform.bold(d.attribute))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0732.json#L5456) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1136)

<a id="op-8825da78576776"></a>
### Item.validate has variants

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_has_variants`

**Inputs** self.

**Record and data access** read “Item” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item has variants.”.

**Local steps**

- If self.is\_new().
  - Return no value.
- If (not self.has\_variants and self.has\_value\_changed(“has\_variants”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_variants → self.has\_value\_changed(“has\_variants”).
  - If Platform.db.exists(“Item”, mapping(“variant\_of” → self.name)).
    - Call the validation error handler Platform.throw(translated “Item has variants.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0732.json#L6406) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1124)

<a id="op-a998600de9c36d"></a>
### Item.validate attributes in variants

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_attributes_in_variants`

**Inputs** self.

**Record and data access** read “Item” via get\_all · read “Item Variant Attribute” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If (not self.has\_variants or self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.has\_variants → self.is\_new().
  - Return no value.
- Set old\_doc from self.get\_doc\_before\_save().
- Set old\_doc\_attributes from set(list of attr.attribute for attr drawn from old\_doc.attributes).
  - Draw attr from old\_doc.attributes.
- Set own\_attributes from list of attr.attribute for attr drawn from self.attributes.
  - Draw attr from self.attributes.
- If old\_doc\_attributes.issubset(set(own\_attributes)).
  - Return no value.
- Bind dependencies defaultdict.
- Set items from list of item at “name” for item drawn from Platform.get\_all(“Item”, mapping(“variant\_of” → self.name)).
  - Draw item from Platform.get\_all(“Item”, mapping(“variant\_of” → self.name)).
- Set deleted\_attribute from list(old\_doc\_attributes.difference(set(own\_attributes))).
- Set item\_attributes from Platform.get\_all(“Item Variant Attribute”, filters = mapping(“parent” → list(“in”, items), “attribute” → list(“in”, deleted\_attribute)), fields = list(“attribute”, “parent”)).
- Set not\_included from defaultdict(list).
- For each attr in item\_attributes.
  - If attr at “attribute” does not belong to own\_attributes.
    - Evaluate not\_included at attr at “parent”.append(attr at “attribute”).
- If not len(not\_included).
  - Return no value.
- Bind local operation body for subsequent calls.
- Bind local operation table\_row for subsequent calls.
- Set rows from empty text.
- For each tuple(docname, attr\_list) in not\_included.items().
  - Set link from formatted text &lt;a href='/app/item/{docname}'&gt;{Platform.bold(docname)}&lt;/a&gt;.
  - Update rows using + table\_row(link, body(attr\_list)).
- Set error\_description from translated “The following deleted attributes exist in Variants but not in the Template. You can either delete the Varian …”.
- Set message from multiline text in the contract.format(error\_description, translated “Variant Items”, translated “Attributes”, rows).
- Call the validation error handler Platform.throw(message, title = translated “Variant Attribute Error”, is\_minimizable = true, wide = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1113)

<a id="op-497a63d54ddb65"></a>
### Item.validate attributes in variants.body

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_attributes_in_variants_body`

**Inputs** docnames.

**Explicit results** text in the contract.join(docnames).

**Local steps**

- Evaluate docnames.sort().
- Return text in the contract.join(docnames).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L1124) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1114)

<a id="op-3dd094d8d3f2b3"></a>
### Item.validate attributes in variants.table row

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_attributes_in_variants_table_row`

**Inputs** title, body.

**Explicit results** formatted text &lt;tr&gt;  &lt;td&gt;{title}&lt;/td&gt;  &lt;td&gt;{body}&lt;/td&gt;  &lt;/tr&gt;.

**Local steps**

- Return formatted text &lt;tr&gt;  &lt;td&gt;{title}&lt;/td&gt;  &lt;td&gt;{body}&lt;/td&gt;  &lt;/tr&gt;.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L1196) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1115)

<a id="op-06b02fbf1ef1d6"></a>
### Item.validate stock exists for template item

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_stock_exists_for_template_item`

**Inputs** self.

**Explicit failure paths** validation helper with StockExistsForTemplate — translated “Cannot change Variant properties after stock transaction. You will have to make a new Item to do this.”.format(self.name) · validation helper — translated “Cannot change Attributes after stock transaction. Make a new Item and transfer stock to the new Item”.

**Local steps**

- If (self.stock\_ledger\_created() and self.\_doc\_before\_save).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.stock\_ledger\_created() → self.\_doc\_before\_save.
  - If (cint(self.\_doc\_before\_save.has\_variants) differs from cint(self.has\_variants) or self.\_doc\_before\_save.variant\_of differs from self.variant\_of).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(self.\_doc\_before\_save.has\_variants) differs from cint(self.has\_variants) → self.\_doc\_before\_save.variant\_of differs from self.variant\_of.
    - Call the validation error handler Platform.throw(translated “Cannot change Variant properties after stock transaction. You will have to make a new Item to do this.”.format(self.name), StockExistsForTemplate).
  - If (self.has\_variants or self.variant\_of).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_variants → self.variant\_of.
    - If not self.is\_child\_table\_same(“attributes”).
      - Call the validation error handler Platform.throw(translated “Cannot change Attributes after stock transaction. Make a new Item and transfer stock to the new Item”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [stock ledger created](operations-021.md#op-abf65c7800ee6f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L1275) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1133)

<a id="op-c35659d0d38f08"></a>
### Item.validate variant based on change

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_variant_based_on_change`

**Inputs** self.

**Record and data access** read “Item” via get\_all · read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Variant Based On cannot be changed”.

**Local steps**

- If (not self.is\_new() and (self.variant\_of or (self.has\_variants and Platform.get\_all(“Item”, mapping(“variant\_of” → self.name))))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → (self.variant\_of or (self.has\_variants and Platform.get\_all(“Item”, mapping(“variant\_of” → self.name)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.variant\_of → (self.has\_variants and Platform.get\_all(“Item”, mapping(“variant\_of” → self.name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_variants → Platform.get\_all(“Item”, mapping(“variant\_of” → self.name)).
  - If self.variant\_based\_on differs from Platform.db.get\_value(“Item”, self.name, “variant\_based\_on”).
    - Call the validation error handler Platform.throw(translated “Variant Based On cannot be changed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L1604) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1138)

<a id="op-ac7de5a361162e"></a>
### Item.validate uom

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_unit_of_measure`

**Inputs** self.

**Record and data access** read “Item Variant Settings” via get\_cached\_value · read “Item” via get\_all · read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Default Unit of Measure for Variant '{0}' must be same as in Template '{1}'”.format(self.stock\_uom, template\_uom).

**Local steps**

- Evaluate validate\_uoms\_are\_enabled(list(self.stock\_uom, expanded generator of d.uom for d drawn from self.uoms)).
  - Draw d from self.uoms.
- Set allow\_different\_uom from Platform.get\_cached\_value(“Item Variant Settings”, “Item Variant Settings”, “allow\_different\_uom”).
- If not self.is\_new().
  - Evaluate check\_stock\_uom\_with\_bin(self.name, self.stock\_uom).
- If (self.has\_variants and not allow\_different\_uom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_variants → not allow\_different\_uom.
  - For each d in Platform.db.get\_all(“Item”, filters = mapping(“variant\_of” → self.name)).
    - Evaluate check\_stock\_uom\_with\_bin(d.name, self.stock\_uom).
- If self.variant\_of.
  - If not allow\_different\_uom.
    - Set template\_uom from Platform.db.get\_value(“Item”, self.variant\_of, “stock\_uom”).
    - If template\_uom differs from self.stock\_uom.
      - Call the validation error handler Platform.throw(translated “Default Unit of Measure for Variant '{0}' must be same as in Template '{1}'”.format(self.stock\_uom, template\_uom)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item Variant Settings”, “Item Variant Settings”, “allow\_different\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1134)

<a id="op-8e47278240a761"></a>
### Item.validate uom conversion factor

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_unit_of_measure_conversion_factor`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Conversion Factor must be greater than zero.”.format(d.idx).

**Local steps**

- For each d in self.get(“uoms”).
  - If not d.conversion\_factor.
    - Set d.conversion\_factor from get\_uom\_conv\_factor(d.uom, self.stock\_uom).
  - If flt(d.conversion\_factor) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: Conversion Factor must be greater than zero.”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1135)

<a id="op-a0d8916831df04"></a>
### Item.validate attributes

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_attributes`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Attribute table is mandatory” · validation helper — translated “Attribute {0} selected multiple times in Attributes Table”.format(d.attribute).

**Local steps**

- If not (self.has\_variants or self.variant\_of).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_variants → self.variant\_of.
  - Return no value.
- If not self.variant\_based\_on.
  - Set self.variant\_based\_on from “Item Attribute”.
- If self.variant\_based\_on equals “Item Attribute”.
  - Set attributes from list().
  - If not self.attributes.
    - Call the validation error handler Platform.throw(translated “Attribute table is mandatory”).
  - For each d in self.attributes.
    - If d.attribute belongs to attributes.
      - Call the validation error handler Platform.throw(translated “Attribute {0} selected multiple times in Attributes Table”.format(d.attribute)).
    - Otherwise.
      - Evaluate attributes.append(d.attribute).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L2442) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1112)

<a id="op-bdfa132e196be7"></a>
### Item.validate variant attributes

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_variant_attributes`

**Inputs** self.

**Explicit failure paths** validation helper with ItemVariantExistsError — translated “Item variant {0} exists with same attributes”.format(variant).

**Local steps**

- If (self.variant\_of and self.variant\_based\_on equals “Item Attribute” and (self.is\_new() or self.has\_attribute\_changes())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.variant\_of → self.variant\_based\_on equals “Item Attribute” → (self.is\_new() or self.has\_attribute\_changes()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_attribute\_changes().
  - Set self.attributes from list of d for d drawn from self.attributes where cstr(d.attribute\_value).strip().
    - Draw d from self.attributes, keep a combination only if (cstr(d.attribute\_value).strip()).
  - Set args from mapping().
  - For each tuple(i, d) in enumerate(self.attributes).
    - Set d.idx from (i + 1).
    - Set args at d.attribute from d.attribute\_value.
  - Set variant from get\_variant(self.variant\_of, args, self.name).
  - If variant.
    - Call the validation error handler Platform.throw(translated “Item variant {0} exists with same attributes”.format(variant), ItemVariantExistsError).
  - Evaluate validate\_item\_variant\_attributes(self, args).
  - For each d in self.attributes.
    - Set d.variant\_of from self.variant\_of.

If control reaches the end, it returns no value.

**Methods declared on this owner** [has attribute changes](operations-022.md#op-f717332dff4509).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1137)

<a id="op-f717332dff4509"></a>
### Item.has attribute changes

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_has_attribute_changes`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · get\_values(self) differs from get\_values(doc\_before\_save).

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return true.
- Bind local operation get\_values for subsequent calls.
- Return get\_values(self) differs from get\_values(doc\_before\_save).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L786) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L283)

<a id="op-c3811c783e756c"></a>
### Item.has attribute changes.get values

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_has_attribute_changes_get_values`

**Inputs** doc.

**Explicit results** list of tuple(d.attribute, cstr(d.attribute\_value)) for d drawn from doc.get(“attributes”).

**Local steps**

- Return list of tuple(d.attribute, cstr(d.attribute\_value)) for d drawn from doc.get(“attributes”).
  - Draw d from doc.get(“attributes”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L284)

<a id="op-58446d9d1181d0"></a>
### Item.cant change

`operation_enterprise_stock_record_definitions_item_business_behavior_item_cant_change`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If self.is\_new().
  - Return no value.
- Set restricted\_fields from tuple(“has\_serial\_no”, “is\_stock\_item”, “valuation\_method”, “has\_batch\_no”).
- Set values from Platform.db.get\_value(“Item”, self.name, restricted\_fields, as\_dict = true).
- If not values.
  - Return no value.
- If (not values.get(“valuation\_method”) and self.get(“valuation\_method”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not values.get(“valuation\_method”) → self.get(“valuation\_method”).
  - Set values at “valuation\_method” from (Platform.get\_single\_value(“Stock Settings”, “valuation\_method”) or “FIFO”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “valuation\_method”) → “FIFO”.
- Set changed\_fields from list of field for field drawn from restricted\_fields where cstr(self.get(field)) differs from cstr(values.get(field)).
  - Draw field from restricted\_fields, keep a combination only if (cstr(self.get(field)) differs from cstr(values.get(field))).
- If (self.valuation\_method equals “Moving Average” and “valuation\_method” belongs to changed\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valuation\_method equals “Moving Average” → “valuation\_method” belongs to changed\_fields.
  - Evaluate changed\_fields.remove(“valuation\_method”).
- If not changed\_fields.
  - Return no value.
- If linked\_doc bound to self.\_get\_linked\_submitted\_documents(changed\_fields).
  - Set changed\_field\_labels from list of Platform.bold(translated self.meta.get\_label(f)) for f drawn from changed\_fields.
    - Draw f from changed\_fields.
  - Set msg from translated “As there are existing submitted transactions against item {0}, you can not change the value of {1}.”.format(self.name, “, ”.join(changed\_field\_labels)).
  - If (linked\_doc and isinstance(linked\_doc, dict)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in linked\_doc → isinstance(linked\_doc, dict).
    - Update msg using + text in the contract.
    - Update msg using + translated “Example of a linked document: {0}”.format(Platform.get\_desk\_link(linked\_doc.doctype, linked\_doc.docname)).
  - Call the validation error handler Platform.throw(msg, title = translated “Linked with submitted documents”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked submitted documents](operations-022.md#op-a5a0487d6789ad).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “valuation\_method”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1091)

<a id="op-c5c157da406349"></a>
### Item.validate serial no wise valuation

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_validate_serial_no_wise_valuation`

**Inputs** self.

**Record and data access** read “Serial No” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial No Wise Valuation cannot be enabled for Item {0} because Serial Nos already exist for it. Valuation f …”.format(Platform.bold(self.name)).

**Local steps**

- If (self.is\_new() or not self.\_doc\_before\_save).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.\_doc\_before\_save.
  - Return no value.
- If (not self.use\_serial\_no\_wise\_valuation or self.\_doc\_before\_save.use\_serial\_no\_wise\_valuation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.use\_serial\_no\_wise\_valuation → self.\_doc\_before\_save.use\_serial\_no\_wise\_valuation.
  - Return no value.
- If Platform.db.exists(“Serial No”, mapping(“item\_code” → self.name)).
  - Call the validation error handler Platform.throw(translated “Serial No Wise Valuation cannot be enabled for Item {0} because Serial Nos already exist for it. Valuation f …”.format(Platform.bold(self.name)), title = translated “Serial Nos Exist”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L792) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L289)

<a id="op-c9c45c5bcd44cf"></a>
### Item.set valuation method for serial no wise valuation

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_set_valuation_method_for_serial_no_wise_valuation`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Valuation Method for Item {0} must be Moving Average because Serial No Wise Valuation is disabled. Enable Se …”.format(Platform.bold(self.name)).

**Local steps**

- If (not self.has\_serial\_no or self.use\_serial\_no\_wise\_valuation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.has\_serial\_no → self.use\_serial\_no\_wise\_valuation.
  - Return no value.
- If (self.\_doc\_before\_save and not self.\_doc\_before\_save.use\_serial\_no\_wise\_valuation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_doc\_before\_save → not self.\_doc\_before\_save.use\_serial\_no\_wise\_valuation.
  - Return no value.
- If not Platform.db.exists(“Stock Ledger Entry”, mapping(“item\_code” → self.name, “is\_cancelled” → 0)).
  - Return no value.
- If (not self.is\_new() and self.\_doc\_before\_save and self.has\_value\_changed(“valuation\_method”) and self.valuation\_method belongs to tuple(“FIFO”, “LIFO”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.\_doc\_before\_save → self.has\_value\_changed(“valuation\_method”) → self.valuation\_method belongs to tuple(“FIFO”, “LIFO”).
  - Call the validation error handler Platform.throw(translated “Valuation Method for Item {0} must be Moving Average because Serial No Wise Valuation is disabled. Enable Se …”.format(Platform.bold(self.name)), title = translated “Invalid Valu ….
- Set self.valuation\_method from “Moving Average”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L788) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L285)

<a id="op-eb6442aa99a05d"></a>
### Item.validate serialized change with bundle

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_serialized_change_with_bundle`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via count.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot change Item {0} from serialized to non-serialized because a Serial and Batch Bundle exists for it. Pl …”.format(Platform.bold(self.name)).

**Local steps**

- If (self.is\_new() or self.has\_serial\_no or not self.\_doc\_before\_save).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_serial\_no → not self.\_doc\_before\_save.
  - Return no value.
- If not self.\_doc\_before\_save.has\_serial\_no.
  - Return no value.
- If Platform.db.count(“Serial and Batch Bundle”, mapping(“item\_code” → self.name, “docstatus” → tuple(“&lt;”, 2))).
  - Call the validation error handler Platform.throw(translated “Cannot change Item {0} from serialized to non-serialized because a Serial and Batch Bundle exists for it. Pl …”.format(Platform.bold(self.name)), title = translated “Serial and B ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L4485) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1131)

<a id="op-a5a0487d6789ad"></a>
### Item.get linked submitted documents

`operation_enterprise_stock_record_definitions_item_business_behavior_item_get_linked_submitted_documents`

**Inputs** self, changed\_fields.

**Declared result** (dict at tuple(str, str) bitwise or no value).

**Record and data access** read doctype via get\_value · read “Stock Ledger Entry” via get\_value.

**Explicit results** linked\_doc.update(mapping(“doctype” → doctype)) · linked\_doc.

**Local steps**

- Set linked\_doctypes from list(“Delivery Note Item”, “Sales Invoice Item”, “POS Invoice Item”, “Purchase Receipt Item”, …).
- If “is\_stock\_item” belongs to changed\_fields.
  - Update linked\_doctypes using + list(“Sales Order Item”, “Purchase Order Item”, “Material Request Item”, “Work Order Item”, …).
- For each doctype in linked\_doctypes.
  - Set filters from mapping(“item\_code” → self.name, “docstatus” → 1).
  - If doctype belongs to tuple(“Product Bundle”, “BOM”).
    - If doctype equals “Product Bundle”.
      - Set filters from mapping(“new\_item\_code” → self.name).
      - Set fieldname from “new\_item\_code as docname”.
    - Otherwise.
      - Set filters from mapping(“item” → self.name, “docstatus” → 1).
      - Set fieldname from “name as docname”.
    - If linked\_doc bound to Platform.db.get\_value(doctype, filters, fieldname, as\_dict = true).
      - Return linked\_doc.update(mapping(“doctype” → doctype)).
  - Otherwise.
    - If (doctype belongs to tuple(“Purchase Invoice Item”, “Sales Invoice Item”) and “is\_stock\_item” does not belong to changed\_fields).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype belongs to tuple(“Purchase Invoice Item”, “Sales Invoice Item”) → “is\_stock\_item” does not belong to changed\_fields.
      - If linked\_doc bound to Platform.db.get\_value(“Stock Ledger Entry”, mapping(“item\_code” → self.name, “is\_cancelled” → 0), list(“voucher\_no as docname”, “voucher\_type as doctype”), as\_dict = true).
        - Return linked\_doc.
    - Otherwise.
      - If linked\_doc bound to Platform.db.get\_value(doctype, filters, list(“parent as docname”, “parenttype as doctype”), as\_dict = true).
        - Return linked\_doc.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1097)

<a id="op-3296f4a0d223de"></a>
### Item.validate auto reorder enabled in stock settings

`operation_enterprise_stock_record_definitions_item_business_behavior_item_validate_auto_reorder_enabled_in_stock_settings`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**State and service calls** msgprint.

**Local steps**

- If self.reorder\_levels.
  - Set enabled from Platform.get\_single\_value(“Stock Settings”, “auto\_indent”).
  - If not enabled.
    - Evaluate Platform.msgprint(msg = translated “You have to enable auto re-order in Stock Settings to maintain re-order levels.”, title = translated “Enable Auto Re-Order”, indicator = “orange”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_indent”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L5632) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1116)

<a id="op-a555df81c8423b"></a>
### Item.validate serial and batch no enabled in stock settings

`operation_enterprise_binding_enterprise_stock_doctype_item_item_item_validate_serial_and_batch_no_enabled_in_stock_settings`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot enable {0} as {1} is disabled in {2}”.format(bold(self.meta.get\_label(fieldname)), bold(translated “Activate Serial / Batch No for Item”), get\_link\_to\_form(“Stock Settings”, “Stock Settings”)).

**Local steps**

- If Platform.get\_single\_value(“Stock Settings”, “enable\_serial\_and\_batch\_no\_for\_item”).
  - Return no value.
- Set doc\_before\_save from self.get\_doc\_before\_save().
- For each fieldname in tuple(“has\_serial\_no”, “has\_batch\_no”).
  - If (cint(self.get(fieldname)) and not (doc\_before\_save and cint(doc\_before\_save.get(fieldname)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.get(fieldname)) → not (doc\_before\_save and cint(doc\_before\_save.get(fieldname))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → cint(doc\_before\_save.get(fieldname)).
    - Call the validation error handler Platform.throw(translated “Cannot enable {0} as {1} is disabled in {2}”.format(bold(self.meta.get\_label(fieldname)), bold(translated “Activate Serial / Batch No for Item”), get\_link\_to\_form(“Stock Settings ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_serial\_and\_batch\_no\_for\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L791) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L288)

<a id="op-a98cf57b746ee3"></a>
### Convert Enterprise to barcodenumber

`operation_enterprise_stock_record_definitions_item_business_behavior_convert_enterprise_to_barcodenumber`

**Inputs** Enterprise\_number, barcode.

**Explicit results** ean\_type at barcode\_length · Enterprise\_number · convert at Enterprise\_number.

**Local steps**

- If Enterprise\_number equals “EAN”.
  - Set ean\_type from mapping(8 → “EAN8”, 13 → “EAN13”).
  - Set barcode\_length from len(barcode).
  - If barcode\_length belongs to ean\_type.
    - Return ean\_type at barcode\_length.
  - Return Enterprise\_number.
- Set convert from mapping(“UPCA” → “UPC”).
- If Enterprise\_number belongs to convert.
  - Return convert at Enterprise\_number.
- Return Enterprise\_number.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1072)

<a id="op-7d36bec57b0413"></a>
### Make item price

`operation_enterprise_stock_record_definitions_item_business_behavior_make_item_price`

**Inputs** item, price\_list\_name, item\_price.

**Record and data access** resolve a document from mapping(“doctype” → “Item Price”, “price\_list” → price\_list\_name, “item\_code” → item, “price\_list\_rate” → item\_price) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Item Price”, “price\_list” → price\_list\_name, “item\_code” → item, “price\_list\_rate” → item\_price)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Item Price”, “price\_list” → price\_list\_name, “item\_code” → item, “price\_list\_rate” → item\_price)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L6078) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1140)
