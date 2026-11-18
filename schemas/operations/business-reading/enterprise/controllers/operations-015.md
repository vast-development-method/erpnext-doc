# Shared transaction rules · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Buying controller

<a id="op-541496b7f9d5fc"></a>
### Get stock qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_get_stock_qty`

**Inputs** row, qty.

**Declared result** float.

**Explicit results** flt((flt(qty) × flt(row.conversion\_factor)), row.precision(“stock\_qty”)).

**Local steps**

- Return flt((flt(qty) × flt(row.conversion\_factor)), row.precision(“stock\_qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1074) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L314)

<a id="op-5f36aee65b5407"></a>
### Get transit amount

`operation_enterprise_binding_enterprise_controllers_buying_controller_get_transit_amount`

**Inputs** row, qty.

**Declared result** float.

**Explicit results** ((get\_stock\_qty(row, qty) × flt(row.sales\_incoming\_rate)) ÷ flt(row.conversion\_factor)).

**Local steps**

- Return ((get\_stock\_qty(row, qty) × flt(row.sales\_incoming\_rate)) ÷ flt(row.conversion\_factor)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1076) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L316)

<a id="op-3d18b7c96e4350"></a>
### Get stock qty status args

`operation_enterprise_binding_enterprise_controllers_buying_controller_get_stock_qty_status_args`

**Inputs** round\_total = true.

**Declared result** dict.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** mapping(“source\_field” → “stock\_qty”) · mapping(“source\_field” → “qty \* conversion\_factor”, “round\_to\_target\_precision” → round\_total).

**Local steps**

- If not Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”).
  - Return mapping(“source\_field” → “stock\_qty”).
- Return mapping(“source\_field” → “qty \* conversion\_factor”, “round\_to\_target\_precision” → round\_total).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1075) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L315)

<a id="op-362d41bd82f147"></a>
### Get received stock qty status args

`operation_enterprise_binding_enterprise_controllers_buying_controller_get_received_stock_qty_status_args`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“source\_field” → “qty \* conversion\_factor”, “round\_to\_target\_precision” → rounds\_stock\_qty).

**Local steps**

- Return mapping(“source\_field” → “qty \* conversion\_factor”, “round\_to\_target\_precision” → rounds\_stock\_qty).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1073) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L313)

<a id="op-9f937b511876f5"></a>
### Rounds stock qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_rounds_stock_qty`

**Inputs** row.

**Declared result** bool.

**Record and data access** read “Stock Settings” via get\_single\_value · read “UOM” via get\_cached\_value.

**Explicit results** bool((Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”) or Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”))).

**Local steps**

- Return bool((Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”) or Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”) → Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”), Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1077) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L317)

## Service · Item variant

<a id="op-959ba4467c9d6f"></a>
### Get variant

`operation_enterprise_controllers_item_variant_business_behavior_get_variant`

**Inputs** template, args = no value, variant = no value, manufacturer = no value, manufacturer\_part\_no = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Item” via get\_doc.

**Explicit results** make\_variant\_based\_on\_manufacturer(item\_template, manufacturer, manufacturer\_part\_no) · find\_variant(template, args, variant).

**Explicit failure paths** validation helper — translated “Please specify at least one attribute in the Attributes table”.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, doc = template, throw = true).
- Set item\_template from Platform.get\_doc(“Item”, template).
- If (item\_template.variant\_based\_on equals “Manufacturer” and manufacturer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_template.variant\_based\_on equals “Manufacturer” → manufacturer.
  - Return make\_variant\_based\_on\_manufacturer(item\_template, manufacturer, manufacturer\_part\_no).
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set attribute\_args from mapping of k → v for tuple(k, v) drawn from args.items() where k differs from “use\_template\_image”.
  - Draw tuple(k, v) from args.items(), keep a combination only if (k differs from “use\_template\_image”).
- If not attribute\_args.
  - Call the validation error handler Platform.throw(translated “Please specify at least one attribute in the Attributes table”).
- Return find\_variant(template, args, variant).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, doc = template, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L469)

<a id="op-a24fab76dc761a"></a>
### Make variant based on manufacturer

`operation_enterprise_controllers_item_variant_business_behavior_make_variant_based_on_manufacturer`

**Inputs** template, manufacturer, manufacturer\_part\_no.

**Record and data access** resolve a document from “Item” via get\_doc · read “Item Manufacturer” via exists.

**State and service calls** request new\_doc for “Item” · call save on variant · request new\_doc for “Item Manufacturer” · call save on manufacturer\_doc.

**Explicit results** Platform.get\_doc(“Item”, existing\_variant) · variant.

**Local steps**

- Bind dependencies append\_number\_if\_name\_exists.
- If existing\_variant bound to get\_manufacturer\_variant(template.name, manufacturer, manufacturer\_part\_no).
  - Return Platform.get\_doc(“Item”, existing\_variant).
- Set variant from Platform.new\_doc(“Item”).
- Evaluate copy\_attributes\_to\_variant(template, variant).
- Set variant\_name from formatted text {template.name} - {manufacturer}.
- If manufacturer\_part\_no.
  - Update variant\_name using + formatted text  - {manufacturer\_part\_no}.
- Set variant.item\_code from append\_number\_if\_name\_exists(“Item”, variant\_name).
- Set variant.flags.ignore\_mandatory from true.
- Evaluate variant.save().
- If not Platform.db.exists(“Item Manufacturer”, mapping(“item\_code” → variant.name, “manufacturer” → manufacturer)).
  - Set manufacturer\_doc from Platform.new\_doc(“Item Manufacturer”).
  - Evaluate manufacturer\_doc.update(mapping(“item\_code” → variant.name, “manufacturer” → manufacturer, “manufacturer\_part\_no” → manufacturer\_part\_no)).
  - Set manufacturer\_doc.flags.ignore\_mandatory from true.
  - Evaluate manufacturer\_doc.save(ignore\_permissions = true).
- Return variant.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L470)

<a id="op-d4e9f63234b1f6"></a>
### Get manufacturer variant

`operation_enterprise_binding_enterprise_controllers_item_variant_get_manufacturer_variant`

**Inputs** template, manufacturer, manufacturer\_part\_no.

**Explicit results** variant at 0 when variant, otherwise no value.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set item\_manufacturer from Platform.qb.DocType(“Item Manufacturer”).
- Set variant from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in manufacturer\_part\_no → empty text.
- Return variant at 0 when variant, otherwise no value.
  - Value choice on variant — true gives variant at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1081) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L321)

<a id="op-418909bdae425a"></a>
### Validate item variant attributes

`operation_enterprise_controllers_item_variant_business_behavior_validate_item_variant_attributes`

**Inputs** item, args = no value.

**Record and data access** resolve a document from “Item” via get\_doc.

**Local steps**

- If isinstance(item, str).
  - Set item from Platform.get\_doc(“Item”, item).
- If not args.
  - Set args from mapping of d.attribute.lower() → d.attribute\_value for d drawn from item.attributes.
    - Draw d from item.attributes.
- Set tuple(attribute\_values, numeric\_values) from get\_attribute\_values(item).
- For each tuple(attribute, value) in args.items().
  - If not value.
    - Continue with the next iteration or loop test.
  - If attribute.lower() belongs to numeric\_values.
    - Set numeric\_attribute from numeric\_values at attribute.lower().
    - Evaluate validate\_is\_incremental(numeric\_attribute, attribute, value, item.name).
  - Otherwise.
    - Set attributes\_list from attribute\_values.get(attribute.lower(), list()).
    - Evaluate validate\_item\_attribute\_value(attributes\_list, attribute, value, item.name, from\_variant = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0375.json#L5285) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L477)

<a id="op-23e641978528a8"></a>
### Validate is incremental

`operation_enterprise_controllers_item_variant_business_behavior_validate_is_incremental`

**Inputs** numeric\_attribute, attribute, value, item.

**Explicit failure paths** validation helper with InvalidItemAttributeValueError — translated “Value {0} for Attribute {1} must be a number for Item {2}”.format(Platform.bold(value), attribute, item) · validation helper — translated “Increment for Attribute {0} cannot be 0”.format(attribute) · validation helper with InvalidItemAttributeValueError — translated “Value for Attribute {0} must be within the range of {1} to {2} in the increments of {3} for Item {4}”.format(attribute, from\_range, to\_range, increment, …).

**Local steps**

- Set from\_range from numeric\_attribute.from\_range.
- Set to\_range from numeric\_attribute.to\_range.
- Set increment from numeric\_attribute.increment.
- Attempt the following.
  - Evaluate float(cstr(value).replace(“,”, empty text)).
- On failure (tuple(TypeError, ValueError)).
  - Call the validation error handler Platform.throw(translated “Value {0} for Attribute {1} must be a number for Item {2}”.format(Platform.bold(value), attribute, item), InvalidItemAttributeValueError, title = translated “Invalid Attribute”).
- If increment equals 0.
  - Call the validation error handler Platform.throw(translated “Increment for Attribute {0} cannot be 0”.format(attribute)).
- Set is\_in\_range from from\_range ≤ flt(value) ≤ to\_range.
  - Compare adjacent operands in order, stopping at the first false comparison in from\_range ≤ flt(value) ≤ to\_range.
- Set precision from max(generator of len(nested operand in the contract(nested operand in the contract) at negative nested operand in the contract.rstrip(“0”)) for v drawn from tuple(value, increment)).
  - Draw v from tuple(value, increment).
- Set remainder from flt(((flt(value) − from\_range) modulo or format increment), precision).
- Set is\_incremental from (remainder equals 0 or remainder equals increment).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in remainder equals 0 → remainder equals increment.
- If not (is\_in\_range and is\_incremental).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_in\_range → is\_incremental.
  - Call the validation error handler Platform.throw(translated “Value for Attribute {0} must be within the range of {1} to {2} in the increments of {3} for Item {4}”.format(attribute, from\_range, to\_range, increment, …), InvalidItemAttributeV ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L475)

<a id="op-55a405cb935595"></a>
### Get attribute value renames

`operation_enterprise_controllers_item_variant_business_behavior_get_attribute_value_renames`

**Inputs** item\_attribute.

**Explicit results** mapping() · renames.

**Local steps**

- If item\_attribute.numeric\_values.
  - Return mapping().
- Set db\_value from item\_attribute.get\_doc\_before\_save().
- If not db\_value.
  - Return mapping().
- Set old\_values from mapping of d.name → d.attribute\_value for d drawn from db\_value.item\_attribute\_values.
  - Draw d from db\_value.item\_attribute\_values.
- Set renames from mapping().
- For each row in item\_attribute.item\_attribute\_values.
  - If (row.name belongs to old\_values and old\_values at row.name differs from row.attribute\_value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.name belongs to old\_values → old\_values at row.name differs from row.attribute\_value.
    - Set renames at old\_values at row.name from row.attribute\_value.
- Return renames.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0375.json#L6315) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L467)

<a id="op-813ba54994f135"></a>
### Update variant attribute values

`operation_enterprise_controllers_item_variant_business_behavior_update_variant_attribute_values`

**Inputs** item\_attribute.

**Explicit results** no value.

**Local steps**

- Set value\_map from get\_attribute\_value\_renames(item\_attribute).
- If not value\_map.
  - Return no value.
- Set item\_variant\_table from Platform.qb.DocType(“Item Variant Attribute”).
- Set item\_table from Platform.qb.DocType(“Item”).
- Set attribute\_value from item\_variant\_table.attribute\_value.
- Set attribute\_value\_case from Case().
- For each tuple(old\_value, new\_value) in value\_map.items().
  - Set attribute\_value\_case from attribute\_value\_case.when(attribute\_value equals old\_value, new\_value).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.attribute equals nested operand in the contract.name).where(attribute\_value.isin(list(value\_map))).run().
- Set Platform.flags.attribute\_values from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L473)

<a id="op-d161e1e70c354f"></a>
### Get attribute abbr renames

`operation_enterprise_controllers_item_variant_business_behavior_get_attribute_abbreviation_renames`

**Inputs** item\_attribute.

**Explicit results** mapping() · changed\_values.

**Local steps**

- If item\_attribute.numeric\_values.
  - Return mapping().
- Set db\_value from item\_attribute.get\_doc\_before\_save().
- If not db\_value.
  - Return mapping().
- Set old\_abbrs from mapping of d.name → d.abbr for d drawn from db\_value.item\_attribute\_values.
  - Draw d from db\_value.item\_attribute\_values.
- Set changed\_values from mapping().
- For each row in item\_attribute.item\_attribute\_values.
  - If (row.name belongs to old\_abbrs and old\_abbrs at row.name differs from row.abbr).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.name belongs to old\_abbrs → old\_abbrs at row.name differs from row.abbr.
    - Set changed\_values at row.attribute\_value from old\_abbrs at row.name.
- Return changed\_values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L778) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L466)

<a id="op-fa57e8c334b836"></a>
### Update variant item codes for abbr renames

`operation_enterprise_controllers_item_variant_business_behavior_update_variant_item_codes_for_abbreviation_renames`

**Inputs** item\_attribute.

**Explicit results** no value.

**Local steps**

- Set changed\_values from get\_attribute\_abbr\_renames(item\_attribute).
- If not changed\_values.
  - Return no value.
- Set item\_variant\_table from Platform.qb.DocType(“Item Variant Attribute”).
- Set variant\_names from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(nested operand in the contract))).distinct().run(pluck = true).
- Set old\_abbrs from mapping of tuple(item\_attribute.name, value) → abbr for tuple(value, abbr) drawn from changed\_values.items().
  - Draw tuple(value, abbr) from changed\_values.items().
- For each variant\_name in variant\_names.
  - Evaluate rename\_variant\_item\_code(variant\_name, old\_abbrs).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L786) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L474)

<a id="op-8d1db8d6178c63"></a>
### Rename variant item code

`operation_enterprise_controllers_item_variant_business_behavior_rename_variant_item_code`

**Inputs** variant\_name, old\_abbrs = no value.

**Record and data access** resolve a document from “Item” via get\_doc · resolve a document from “Item” via get\_cached\_doc.

**State and service calls** request rename\_doc for “Item” · request set\_value on “Item”.

**Explicit results** no value.

**Local steps**

- Set variant from Platform.get\_doc(“Item”, variant\_name).
- If not variant.variant\_of.
  - Return no value.
- Set template from Platform.get\_cached\_doc(“Item”, variant.variant\_of).
- If (old\_abbrs and variant.item\_code differs from get\_variant\_code(template.item\_code, variant.attributes, old\_abbrs)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_abbrs → variant.item\_code differs from get\_variant\_code(template.item\_code, variant.attributes, old\_abbrs).
  - Return no value.
- Set new\_code from Platform.\_dict(mapping(“item\_code” → no value, “item\_name” → no value, “attributes” → variant.attributes)).
- Evaluate make\_variant\_item\_code(template.item\_code, template.item\_name, new\_code).
- If (not new\_code.item\_code or new\_code.item\_code equals variant.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not new\_code.item\_code → new\_code.item\_code equals variant.item\_code.
  - Return no value.
- Evaluate Platform.rename\_doc(“Item”, variant.item\_code, new\_code.item\_code).
- If (new\_code.item\_name and new\_code.item\_name differs from variant.item\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_code.item\_name → new\_code.item\_name differs from variant.item\_name.
  - Evaluate Platform.db.set\_value(“Item”, new\_code.item\_code, “item\_name”, new\_code.item\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, variant.variant\_of).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L472)

<a id="op-cd7d2129c60364"></a>
### Validate item attribute value

`operation_enterprise_controllers_item_variant_business_behavior_validate_item_attribute_value`

**Inputs** attributes\_list, attribute, attribute\_value, item, from\_variant = true.

**Record and data access** read “Item Variant Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidItemAttributeValueError — translated “{0} is not a valid Value for Attribute {1} of Item {2}.”.format(Platform.bold(attribute\_value), Platform.bold(attribute), Platform.bold(item)) · validation helper with InvalidItemAttributeValueError — msg.

**Local steps**

- Set allow\_rename\_attribute\_value from Platform.db.get\_single\_value(“Item Variant Settings”, “allow\_rename\_attribute\_value”).
- If (attribute\_value belongs to attributes\_list or (allow\_rename\_attribute\_value and from\_variant)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in attribute\_value belongs to attributes\_list → (allow\_rename\_attribute\_value and from\_variant).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allow\_rename\_attribute\_value → from\_variant.
  - Return no value.
- If from\_variant.
  - Call the validation error handler Platform.throw(translated “{0} is not a valid Value for Attribute {1} of Item {2}.”.format(Platform.bold(attribute\_value), Platform.bold(attribute), Platform.bold(item)), InvalidItemAttributeValueError, ti ….
- If allow\_rename\_attribute\_value.
  - Set msg from translated “The value {0} cannot be removed as it is assigned to an existing Item {1}.”.format(Platform.bold(attribute\_value), Platform.bold(item)).
- Otherwise.
  - Set msg from translated “The value {0} is already assigned to an existing Item {1}.”.format(Platform.bold(attribute\_value), Platform.bold(item)).
  - Update msg using + (text in the contract + translated “To still proceed with editing this Attribute Value, enable {0} in Item Variant Settings.”.format(Platform.bold(translated “Allow Rename Attribute Value”))).
- Call the validation error handler Platform.throw(msg, InvalidItemAttributeValueError, title = translated “Edit Not Allowed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Item Variant Settings”, “allow\_rename\_attribute\_value”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L788) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L476)

<a id="op-dfcecc20c80b4d"></a>
### Get attribute values

`operation_enterprise_controllers_item_variant_business_behavior_get_attribute_values`

**Inputs** item.

**Record and data access** read “Item Attribute Value” via get\_all · read “Item Variant Attribute” via get\_all.

**Explicit results** tuple(Platform.flags.attribute\_values, Platform.flags.numeric\_values at item.variant\_of).

**Local steps**

- If not Platform.flags.attribute\_values.
  - Set attribute\_values from mapping().
  - For each t in Platform.get\_all(“Item Attribute Value”, fields = list(“parent”, “attribute\_value”)).
    - Evaluate attribute\_values.setdefault(t.parent.lower(), list()).append(t.attribute\_value).
  - Set Platform.flags.attribute\_values from attribute\_values.
  - Set Platform.flags.numeric\_values from mapping().
- If item.variant\_of does not belong to Platform.flags.numeric\_values.
  - Set Platform.flags.numeric\_values at item.variant\_of from mapping of t.attribute.lower() → t for t drawn from Platform.get\_all(“Item Variant Attribute”, fields = list(“attribute”, “from\_range”, “to\_range”, “increment”), filters = mapping(“numeric\_values” → 1, “pa ….
    - Draw t from Platform.get\_all(“Item Variant Attribute”, fields = list(“attribute”, “from\_range”, “to\_range”, “increment”), filters = mapping(“numeric\_values” → 1, “parent” → item.variant\_of)).
- Return tuple(Platform.flags.attribute\_values, Platform.flags.numeric\_values at item.variant\_of).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L468)

<a id="op-d09497c92bd9c5"></a>
### Find variant

`operation_enterprise_controllers_item_variant_business_behavior_find_variant`

**Inputs** template, args, variant\_item\_code = no value.

**Record and data access** resolve a document from “Item” via get\_doc.

**Explicit results** variant.name.

**Local steps**

- Set possible\_variants from list of i for i drawn from get\_item\_codes\_by\_attributes(args, template) where i differs from variant\_item\_code.
  - Draw i from get\_item\_codes\_by\_attributes(args, template), keep a combination only if (i differs from variant\_item\_code).
- For each variant in possible\_variants.
  - Set variant from Platform.get\_doc(“Item”, variant).
  - If len(args.keys()) equals len(variant.get(“attributes”)).
    - Set match\_count from 0.
    - For each tuple(attribute, value) in args.items().
      - For each row in variant.attributes.
        - If (row.attribute equals translated attribute and row.attribute\_value equals cstr(value)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.attribute equals translated attribute → row.attribute\_value equals cstr(value).
          - Update match\_count using + 1.
          - Leave the innermost loop without its normal-exhaustion alternative.
    - If match\_count equals len(args.keys()).
      - Return variant.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0376.json#L1745) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L464)

<a id="op-df5d9e4174523b"></a>
### Create variant

`operation_enterprise_controllers_item_variant_business_behavior_create_variant`

**Inputs** item, args, use\_template\_image = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Item” via get\_doc.

**State and service calls** request new\_doc for “Item”.

**Explicit results** variant.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “create”, throw = true).
- Evaluate Platform.has\_permission(“Item”, doc = item, throw = true).
- Set use\_template\_image from Platform.parse\_json(use\_template\_image).
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set template from Platform.get\_doc(“Item”, item).
- Set variant from Platform.new\_doc(“Item”).
- Set variant.variant\_based\_on from “Item Attribute”.
- Set variant\_attributes from list().
- For each d in template.attributes.
  - Set attribute\_value from (args.get(translated d.attribute) or args.get(d.attribute)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(translated d.attribute) → args.get(d.attribute).
  - If attribute\_value.
    - Evaluate variant\_attributes.append(mapping(“attribute” → d.attribute, “attribute\_value” → attribute\_value)).
- Evaluate variant.set(“attributes”, variant\_attributes).
- Evaluate copy\_attributes\_to\_variant(template, variant).
- If (use\_template\_image and template.image).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in use\_template\_image → template.image.
  - Set variant.image from template.image.
- Evaluate make\_variant\_item\_code(template.item\_code, template.item\_name, variant).
- Return variant.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “create”, throw = true), Platform.has\_permission(“Item”, doc = item, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L773) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L461)

<a id="op-3f8afb40433ca2"></a>
### Enqueue multiple variant creation

`operation_enterprise_controllers_item_variant_business_behavior_enqueue_multiple_variant_creation`

**Inputs** item, args, use\_template\_image = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with “Enterprise.controllers.item\_variant.create\_multiple\_variants”.

**Explicit results** no value · create\_multiple\_variants(item, args, use\_template\_image) · “queued”.

**Explicit failure paths** validation helper — translated “Please select at least one attribute value” · validation helper — translated “Please do not create more than 500 items at a time”.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “create”, throw = true).
- Set use\_template\_image from Platform.parse\_json(use\_template\_image).
- If isinstance(args, str).
  - Set variants from json.loads(args).
- Otherwise.
  - Set variants from args.
- Set variants from mapping of key → values for tuple(key, values) drawn from variants.items() where values.
  - Draw tuple(key, values) from variants.items(), keep a combination only if (values).
- If not variants.
  - Call the validation error handler Platform.throw(translated “Please select at least one attribute value”).
- Set total\_variants from 1.
- For each key in variants.
  - Update total\_variants using × len(variants at key).
- <a id="op-3f8afb40433ca2-guard-16"></a>If total\_variants ≥ 600.
  - Call the validation error handler Platform.throw(translated “Please do not create more than 500 items at a time”).
  - Return no value.
- If total\_variants &lt; 10.
  - Return create\_multiple\_variants(item, args, use\_template\_image).
- Otherwise.
  - Evaluate Platform.enqueue(“Enterprise.controllers.item\_variant.create\_multiple\_variants”, item = item, args = args, use\_template\_image = use\_template\_image, now = Platform.in\_test).
  - Return “queued”.

**Derived branch illustrations**

- At the comparison total\_variants ≥ 600, total\_variants = 600 selects the branch that calls the validation-error handler with translated “Please do not create more than 500 items at a time”. With total\_variants = 599, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3f8afb40433ca2-guard-16)

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “create”, throw = true) · service or queued work from Platform.enqueue(“Enterprise.controllers.item\_variant.create\_multiple\_variants”, item = item, args = args, use\_template\_image = use\_template\_image, now = Platform.in\_test).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L463)

<a id="op-15a41282bb41ab"></a>
### Create multiple variants

`operation_enterprise_controllers_item_variant_business_behavior_create_multiple_variants`

**Inputs** item, args, use\_template\_image = false.

**Record and data access** resolve a document from “Item” via get\_doc.

**State and service calls** call save on variant.

**Explicit results** count.

**Local steps**

- Set count from 0.
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set args from mapping of key → values for tuple(key, values) drawn from args.items() where values.
  - Draw tuple(key, values) from args.items(), keep a combination only if (values).
- Set template\_item from Platform.get\_doc(“Item”, item).
- Set args\_set from generate\_keyed\_value\_combinations(args).
- For each attribute\_values in args\_set.
  - If not get\_variant(item, args = attribute\_values).
    - Set variant from create\_variant(item, attribute\_values).
    - If (use\_template\_image and template\_item.image).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in use\_template\_image → template\_item.image.
      - Set variant.image from template\_item.image.
    - Evaluate variant.save().
    - Update count using + 1.
- Return count.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L772) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L460)

<a id="op-db00fa135b87a6"></a>
### Generate keyed value combinations

`operation_enterprise_controllers_item_variant_business_behavior_generate_keyed_value_combinations`

**Inputs** args.

**Explicit results** list() · results.

**Local steps**

- If not args.
  - Return list().
- Set args from mapping of key → values for tuple(key, values) drawn from args.items() where values.
  - Draw tuple(key, values) from args.items(), keep a combination only if (values).
- If not args.
  - Return list().
- Set key\_value\_lists from list of list of tuple(key, val) for val drawn from args at key for key drawn from args.keys().
  - Draw key from args.keys().
  - Draw val from args at key.
- Set results from key\_value\_lists.pop(0).
- Set results from list of mapping(d at 0 → d at 1) for d drawn from results.
  - Draw d from results.
- For each l in key\_value\_lists.
  - Set new\_results from list().
  - For each res in results.
    - For each key\_val in l.
      - Set obj from copy.deepcopy(res).
      - Set obj at key\_val at 0 from key\_val at 1.
      - Evaluate new\_results.append(obj).
  - Set results from new\_results.
- Return results.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0376.json#L3771) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L465)

<a id="op-5440a5faa7bc9f"></a>
### Copy attributes to variant

`operation_enterprise_controllers_item_variant_business_behavior_copy_attributes_to_variant`

**Inputs** item, variant.

**Record and data access** read “Variant Field” via get\_all.

**Local steps**

- Set exclude\_fields from get\_fields\_excluded\_from\_variant\_copy(item, variant).
- Set allow\_fields from list of d.field\_name for d drawn from Platform.get\_all(“Variant Field”, fields = list(“field\_name”)).
  - Draw d from Platform.get\_all(“Variant Field”, fields = list(“field\_name”)).
- If “variant\_based\_on” does not belong to allow\_fields.
  - Evaluate allow\_fields.append(“variant\_based\_on”).
- For each field in item.meta.fields.
  - If ((field.reqd or field.fieldname belongs to allow\_fields) and field.fieldname does not belong to exclude\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (field.reqd or field.fieldname belongs to allow\_fields) → field.fieldname does not belong to exclude\_fields.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.reqd → field.fieldname belongs to allow\_fields.
    - Evaluate copy\_field\_to\_variant(item, variant, field).
- Set variant.variant\_of from item.name.
- Evaluate set\_variant\_description(item, variant, allow\_fields).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L459)

<a id="op-02ce755b638f66"></a>
### Get fields excluded from variant copy

`operation_enterprise_binding_enterprise_controllers_item_variant_get_fields_excluded_from_variant_copy`

**Inputs** item, variant.

**Record and data access** read “Item Variant Settings” via get\_single\_value.

**Explicit results** exclude\_fields.

**Local steps**

- Set exclude\_fields from list(“naming\_series”, “item\_code”, “item\_name”, “published\_in\_website”, …).
- If item.variant\_based\_on equals “Manufacturer”.
  - Update exclude\_fields using + list(“manufacturer”, “manufacturer\_part\_no”).
- If (not variant.is\_new() and Platform.get\_single\_value(“Item Variant Settings”, “allow\_different\_uom”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not variant.is\_new() → Platform.get\_single\_value(“Item Variant Settings”, “allow\_different\_uom”).
  - Update exclude\_fields using + list(“stock\_uom”, “uoms”, “sales\_uom”, “purchase\_uom”).
- Return exclude\_fields.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Item Variant Settings”, “allow\_different\_uom”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1080) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L320)
