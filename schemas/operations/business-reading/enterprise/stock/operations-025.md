# Inventory and warehouses · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item

[Record definition](../../../../data/record-types/item.json)

<a id="op-0ff8b709162e94"></a>
### Reindex renamed item

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_reindex_renamed_item`

**Inputs** doc, method = no value, old = no value, new = no value, merge = false.

**Local steps**

- Evaluate queue\_item(doc.name, drop = old).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L314)

<a id="op-7f204cf299705d"></a>
### Queue item

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_queue_item`

**Inputs** item\_code, drop = no value.

**Explicit results** no value.

**Local steps**

- Set search from ItemSearch().
- If not (search.is\_search\_enabled() and search.index\_exists()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in search.is\_search\_enabled() → search.index\_exists().
  - Return no value.
- Attempt the following.
  - Evaluate search.index\_doc(“Item”, item\_code).
  - If drop.
    - Evaluate search.remove\_doc(“Item”, drop).
- On failure (Exception).
  - Evaluate Platform.log\_error(“Item search index update failed, dropping the index”).
  - Attempt the following.
    - Evaluate search.drop\_index().
  - On failure (Exception).
    - Evaluate Platform.log\_error(“Item search index could not be dropped”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L311)

<a id="op-debb6e11479bea"></a>
### Get item search candidates

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_get_item_search_candidates`

**Inputs** txt, searched\_fields.

**Declared result** (list at str bitwise or no value).

**Explicit results** ItemSearch().get\_candidate\_item\_codes(txt, searched\_fields) · no value.

**Local steps**

- Attempt the following.
  - Return ItemSearch().get\_candidate\_item\_codes(txt, searched\_fields).
- On failure (Exception).
  - Evaluate Platform.log\_error(“Item search index unavailable”).
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L295)

## Record · Item alternative

[Record definition](../../../../data/record-types/item_alternative.json)

<a id="op-8232cd106aea65"></a>
### Item Alternative.validate

`operation_enterprise_stock_record_definitions_item_alternative_business_behavior_item_alternative_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.item\_code and self.alternative\_item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → self.alternative\_item\_code.
  - Return no value.
- Evaluate self.has\_alternative\_item().
- Evaluate self.validate\_alternative\_item().
- Evaluate self.validate\_duplicate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has alternative item](operations-025.md#op-d4076130de6445), [validate alternative item](operations-025.md#op-13aa1332a56b82), [validate duplicate](operations-025.md#op-4ce3af9e7ae99a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1054)

<a id="op-d4076130de6445"></a>
### Item Alternative.has alternative item

`operation_enterprise_stock_record_definitions_item_alternative_business_behavior_item_alternative_has_alternative_item`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Not allow to set alternative item for the item {0}”.format(self.item\_code).

**Local steps**

- If (self.item\_code and not Platform.db.get\_value(“Item”, self.item\_code, “allow\_alternative\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → not Platform.db.get\_value(“Item”, self.item\_code, “allow\_alternative\_item”).
  - Call the validation error handler Platform.throw(translated “Not allow to set alternative item for the item {0}”.format(self.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1053)

<a id="op-13aa1332a56b82"></a>
### Item Alternative.validate alternative item

`operation_enterprise_stock_record_definitions_item_alternative_business_behavior_item_alternative_validate_alternative_item`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**State and service calls** msgprint with translated “The value of {0} differs between Items {1} and {2}”.format(Platform.bold(item\_meta.get\_label(field)), Platform.bold(self.alternative\_item\_code), Platform.bold(self.item\_code)).

**Explicit failure paths** validation helper — translated “Alternative item must not be same as item code” · validation helper — alternate\_item\_check\_msg.format(self.item\_code) · validation helper — alternate\_item\_check\_msg.format(self.alternative\_item\_code).

**Local steps**

- If self.item\_code equals self.alternative\_item\_code.
  - Call the validation error handler Platform.throw(translated “Alternative item must not be same as item code”).
- Set item\_meta from Platform.get\_meta(“Item”).
- Set fields from list(“is\_stock\_item”, “include\_item\_in\_manufacturing”, “has\_serial\_no”, “has\_batch\_no”, …).
- Set item\_data from Platform.db.get\_value(“Item”, self.item\_code, fields, as\_dict = 1).
- Set alternative\_item\_data from Platform.db.get\_value(“Item”, self.alternative\_item\_code, fields, as\_dict = 1).
- For each field in fields.
  - If item\_data.get(field) differs from alternative\_item\_data.get(field).
    - Set tuple(raise\_exception, alert) from list(1, false) when field equals “is\_stock\_item”, otherwise list(0, true).
      - Value choice on field equals “is\_stock\_item” — true gives list(1, false), false gives list(0, true).
    - Evaluate Platform.msgprint(translated “The value of {0} differs between Items {1} and {2}”.format(Platform.bold(item\_meta.get\_label(field)), Platform.bold(self.alternative\_item\_code), Platform.bold(self.item\_code)) ….
- Set alternate\_item\_check\_msg from translated “Allow Alternative Item must be checked on Item {}”.
- If not item\_data.allow\_alternative\_item.
  - Call the validation error handler Platform.throw(alternate\_item\_check\_msg.format(self.item\_code)).
- If (self.two\_way and not alternative\_item\_data.allow\_alternative\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.two\_way → not alternative\_item\_data.allow\_alternative\_item.
  - Call the validation error handler Platform.throw(alternate\_item\_check\_msg.format(self.alternative\_item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1055)

<a id="op-4ce3af9e7ae99a"></a>
### Item Alternative.validate duplicate

`operation_enterprise_stock_record_definitions_item_alternative_business_behavior_item_alternative_validate_duplicate`

**Inputs** self.

**Record and data access** read “Item Alternative” via get\_value.

**Explicit failure paths** validation helper — translated “Already record exists for the item {0}”.format(self.item\_code).

**Local steps**

- If Platform.db.get\_value(“Item Alternative”, mapping(“item\_code” → self.item\_code, “alternative\_item\_code” → self.alternative\_item\_code, “name” → tuple(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “Already record exists for the item {0}”.format(self.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1056)

<a id="op-c83c0b6ee58037"></a>
### Get alternative item pairs

`operation_enterprise_binding_enterprise_stock_doctype_item_alternative_item_alternative_get_alternative_item_pairs`

**Inputs** item\_codes.

**Declared result** set.

**Explicit results** set() · pairs.

**Local steps**

- If not item\_codes.
  - Return set().
- Set item\_alternative from Platform.qb.DocType(“Item Alternative”).
- Set rows from nested operand in the contract(nested operand in the contract).select(item\_alternative.item\_code, item\_alternative.alternative\_item\_code, item\_alternative.two\_way).where((nested operand in the contract.ite ….
- Set pairs from set().
- For each row in rows.
  - Evaluate pairs.add(tuple(row.item\_code, row.alternative\_item\_code)).
  - If row.two\_way.
    - Evaluate pairs.add(tuple(row.alternative\_item\_code, row.item\_code)).
- Return pairs.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L277)

<a id="op-73b03dd040a093"></a>
### Get alternative items

`operation_enterprise_stock_record_definitions_item_alternative_business_behavior_get_alternative_items`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text  (select alternative\_item\_code from ′tabItem Alternative′  where item\_code = %(item\_code)s and alternative\_item\_code like %(txt)s)  union  (selec, mapping(“item\_code” →  ….

**Local steps**

- Evaluate Enterprise.require\_permission(“Item”, filters.get(“item\_code”)).
- Return Platform.db.sql(formatted text  (select alternative\_item\_code from ′tabItem Alternative′  where item\_code = %(item\_code)s and alternative\_item\_code like %(txt)s)  union  (selec, mapping(“item\_code” →  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1052)

## Record · Item attribute

[Record definition](../../../../data/record-types/item_attribute.json)

<a id="op-5473c99fb2b87f"></a>
### Item Attribute.validate

`operation_enterprise_stock_record_definitions_item_attribute_business_behavior_item_attribute_validate`

**Inputs** self.

**Local steps**

- Set Platform.flags.attribute\_values from no value.
- Evaluate self.validate\_numeric\_change().
- Evaluate self.validate\_numeric().
- Evaluate self.validate\_duplication().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate numeric change](operations-025.md#op-c651385a770ef6), [validate numeric](operations-025.md#op-ec496cc6b8504e), [validate duplication](operations-025.md#op-8bb2b95478cd41).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1064)

<a id="op-151843b8fbea24"></a>
### Item Attribute.on update

`operation_enterprise_stock_record_definitions_item_attribute_business_behavior_item_attribute_on_update`

**Inputs** self.

**Local steps**

- Evaluate update\_variant\_attribute\_values(self).
- Evaluate update\_variant\_item\_codes\_for\_abbr\_renames(self).
- Evaluate self.validate\_exising\_items().
- Evaluate self.set\_enabled\_disabled\_in\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate exising items](operations-025.md#op-5c03177f7e7fdc), [set enabled disabled in items](operations-025.md#op-37954f8de0e59a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0740.json#L804) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1062)

<a id="op-37954f8de0e59a"></a>
### Item Attribute.set enabled disabled in items

`operation_enterprise_stock_record_definitions_item_attribute_business_behavior_item_attribute_set_enabled_disabled_in_items`

**Inputs** self.

**Local steps**

- Set db\_value from self.get\_doc\_before\_save().
- If (not db\_value or db\_value.disabled differs from self.disabled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not db\_value → db\_value.disabled differs from self.disabled.
  - Set item\_variant\_table from Platform.qb.DocType(“Item Variant Attribute”).
  - Set query from nested operand in the contract.qb.update(item\_variant\_table).set(item\_variant\_table.disabled, self.disabled).where(item\_variant\_table.attribute equals self.name).
  - Evaluate query.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0740.json#L917) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1063)

<a id="op-ea5c914071432d"></a>
### Item Attribute.get variants using attribute

`operation_enterprise_binding_enterprise_stock_doctype_item_attribute_item_attribute_itemattribute_get_variants_using_attribute`

**Inputs** self, limit = no value.

**Explicit results** query.limit(limit).run(as\_dict = 1) when limit, otherwise query.run(as\_dict = 1).

**Local steps**

- Set iva from Platform.qb.DocType(“Item Variant Attribute”).
- Set i from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(i.name, iva.attribute\_value.as\_(“value”)).where((( ….
- Return query.limit(limit).run(as\_dict = 1) when limit, otherwise query.run(as\_dict = 1).
  - Value choice on limit — true gives query.limit(limit).run(as\_dict = 1), false gives query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L279)

<a id="op-5c03177f7e7fdc"></a>
### Item Attribute.validate exising items

`operation_enterprise_stock_record_definitions_item_attribute_business_behavior_item_attribute_validate_exising_items`

**Inputs** self.

**Local steps**

- Set attributes\_list from list of d.attribute\_value for d drawn from self.item\_attribute\_values.
  - Draw d from self.item\_attribute\_values.
- Set removed\_values from self.get\_removed\_attribute\_values(attributes\_list).
- For each item in self.get\_variants\_using\_attribute().
  - If self.numeric\_values.
    - Evaluate validate\_is\_incremental(self, self.name, item.value, item.name).
  - Otherwise.
    - If item.value belongs to removed\_values.
      - Evaluate validate\_item\_attribute\_value(attributes\_list, self.name, item.value, item.name, from\_variant = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get removed attribute values](operations-025.md#op-851d7659c449c4), [get variants using attribute](operations-025.md#op-ea5c914071432d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1066)

<a id="op-851d7659c449c4"></a>
### Item Attribute.get removed attribute values

`operation_enterprise_binding_enterprise_stock_doctype_item_attribute_item_attribute_itemattribute_get_removed_attribute_values`

**Inputs** self, attributes\_list.

**Explicit results** set() · (set of d.attribute\_value for d drawn from previous.item\_attribute\_values − set(attributes\_list)).

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return set().
- Return (set of d.attribute\_value for d drawn from previous.item\_attribute\_values − set(attributes\_list)).
  - Draw d from previous.item\_attribute\_values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L278)

<a id="op-c651385a770ef6"></a>
### Item Attribute.validate numeric change

`operation_enterprise_binding_enterprise_stock_doctype_item_attribute_item_attribute_itemattribute_validate_numeric_change`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Numeric Values cannot be changed for Attribute {0} as it is used in variants”.format(Platform.bold(self.name)).

**Local steps**

- If (self.is\_new() or not self.has\_value\_changed(“numeric\_values”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_value\_changed(“numeric\_values”).
  - Return no value.
- If self.get\_variants\_using\_attribute(limit = 1).
  - Call the validation error handler Platform.throw(translated “Numeric Values cannot be changed for Attribute {0} as it is used in variants”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get variants using attribute](operations-025.md#op-ea5c914071432d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L280)

<a id="op-ec496cc6b8504e"></a>
### Item Attribute.validate numeric

`operation_enterprise_stock_record_definitions_item_attribute_business_behavior_item_attribute_validate_numeric`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please specify from/to range” · validation helper — translated “From Range has to be less than To Range” · validation helper with ItemAttributeIncrementError — translated “Increment must be greater than 0”.

**Local steps**

- If self.numeric\_values.
  - Evaluate self.set(“item\_attribute\_values”, list()).
  - If (self.from\_range is identical to no value or self.to\_range is identical to no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.from\_range is identical to no value → self.to\_range is identical to no value.
    - Call the validation error handler Platform.throw(translated “Please specify from/to range”).
  - Otherwise.
    - If flt(self.from\_range) ≥ flt(self.to\_range).
      - Call the validation error handler Platform.throw(translated “From Range has to be less than To Range”).
  - If flt(self.increment) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Increment must be greater than 0”, ItemAttributeIncrementError).
- Otherwise.
  - Set self.from\_range, self.to\_range, self.increment from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1067)

<a id="op-8bb2b95478cd41"></a>
### Item Attribute.validate duplication

`operation_enterprise_stock_record_definitions_item_attribute_business_behavior_item_attribute_validate_duplication`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Attribute value: {0} must appear only once”.format(d.attribute\_value.title()) · validation helper — translated “Abbreviation: {0} must appear only once”.format(d.abbr.title()).

**Local steps**

- Set tuple(values, abbrs) from tuple(list(), list()).
- For each d in self.item\_attribute\_values.
  - If d.attribute\_value.lower() belongs to map(str.lower, values).
    - Call the validation error handler Platform.throw(translated “Attribute value: {0} must appear only once”.format(d.attribute\_value.title())).
  - Evaluate values.append(d.attribute\_value).
  - If d.abbr.lower() belongs to map(str.lower, abbrs).
    - Call the validation error handler Platform.throw(translated “Abbreviation: {0} must appear only once”.format(d.abbr.title())).
  - Evaluate abbrs.append(d.abbr).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0740.json#L2053) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1065)

## Report · Item balance (simple)

<a id="op-71e9b866963f7d"></a>
### Execute

`operation_enterprise_binding_enterprise_stock_report_item_balance_simple_item_balance_simple_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data()).

**Local steps**

- Return tuple(get\_columns(), get\_data()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L964)

<a id="op-0e3d9fd75d32e9"></a>
### Get columns

`operation_enterprise_binding_enterprise_stock_report_item_balance_simple_item_balance_simple_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “Data”, ….

**Local steps**

- Return list(mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “Data”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L965)

<a id="op-0681baefb2bc56"></a>
### Get data

`operation_enterprise_binding_enterprise_stock_report_item_balance_simple_item_balance_simple_get_data`

**Inputs** no declared parameters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set bin\_table from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract(nested operand in the contract).left\_join(bin\_table).on(item.item\_code equals bin\_table.item\_code).select(item.item\_code, item.item\_name, item.item\_group, item.brand, …).
- If condition bound to get\_allowed\_masters\_condition(item.name, “Item”).
  - Set query from query.where(condition).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L966)

## Service · Item dashboard

<a id="op-ed616c5a8573be"></a>
### Make stock entry

`operation_enterprise_binding_enterprise_stock_dashboard_item_dashboard_make_stock_entry`

**Inputs** item\_code, source\_warehouse = no value, target\_warehouse = no value, stock\_entry\_type = no value, qty = no value, rate = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Warehouse” via get\_cached\_value · read “Stock Entry Type” via get\_cached\_value · read “Item” via get\_cached\_value.

**State and service calls** request new\_doc for “Stock Entry”.

**Explicit results** stock\_entry.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Set stock\_entry from Platform.new\_doc(“Stock Entry”).
- If warehouse bound to (source\_warehouse or target\_warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_warehouse → target\_warehouse.
  - Set stock\_entry.company from Platform.get\_cached\_value(“Warehouse”, warehouse, “company”).
- Set stock\_entry.stock\_entry\_type from (stock\_entry\_type or “Material Transfer” when source\_warehouse, otherwise “Material Receipt”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in stock\_entry\_type → “Material Transfer” when source\_warehouse, otherwise “Material Receipt”.
  - Value choice on source\_warehouse — true gives “Material Transfer”, false gives “Material Receipt”.
- Set stock\_entry.purpose from Platform.get\_cached\_value(“Stock Entry Type”, stock\_entry.stock\_entry\_type, “purpose”).
- Set stock\_entry.from\_warehouse from source\_warehouse.
- Set stock\_entry.to\_warehouse from target\_warehouse.
- Set stock\_uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
- Evaluate stock\_entry.append(“items”, mapping(“item\_code” → item\_code, “s\_warehouse” → source\_warehouse, “t\_warehouse” → target\_warehouse, “qty” → flt(qty), …)).
- If not Platform.has\_permission(“Stock Entry”, “create”, doc = stock\_entry).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Return stock\_entry.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, warehouse, “company”), Platform.get\_cached\_value(“Stock Entry Type”, stock\_entry.stock\_entry\_type, “purpose”) and 1 further calls · effective access from Platform.has\_permission(“Stock Entry”, “create”, doc = stock\_entry).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L191)

<a id="op-f7de8182e9c493"></a>
### Get data

`operation_enterprise_stock_dashboard_item_dashboard_business_behavior_get_data`

**Inputs** item\_code = no value, warehouse = no value, item\_group = no value, start = 0, sort\_by = “actual\_qty”, sort\_order = “desc”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item Group” via get\_value · read “Warehouse” via get\_list · read “Bin” via get\_list · read “System Settings” via get\_single\_value · read “Item” via get\_cached\_value.

**Explicit results** list() · items.

**Explicit failure paths** validation helper — translated “Invalid sort order”.

**Local steps**

- If (not Platform.has\_permission(“Bin”, “read”) or not Platform.has\_permission(“Warehouse”, “read”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.has\_permission(“Bin”, “read”) → not Platform.has\_permission(“Warehouse”, “read”).
  - Return list().
- If (sort\_by does not belong to QTY\_FIELDS or sort\_order does not belong to tuple(“asc”, “desc”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sort\_by does not belong to QTY\_FIELDS → sort\_order does not belong to tuple(“asc”, “desc”).
  - Call the validation error handler Platform.throw(translated “Invalid sort order”).
- Set filters from list().
- If item\_code.
  - Evaluate filters.append(list(“item\_code”, “=”, item\_code)).
- If warehouse.
  - Evaluate filters.append(list(“warehouse”, “descendants of (inclusive)”, warehouse)).
- If item\_group.
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Item Group”, item\_group, list(“lft”, “rgt”)).
  - Set items from Platform.db.sql\_list(query text (SELECT, Item), tuple(lft, rgt)).
  - Evaluate filters.append(list(“item\_code”, “in”, items)).
- If build\_match\_conditions(“Warehouse”, user = Platform.session.user).
  - Evaluate filters.append(list(“warehouse”, “in”, Platform.get\_list(“Warehouse”, pluck = “name”, limit\_page\_length = 0))).
- Set items from Platform.get\_list(“Bin”, fields = list(“item\_code”, “warehouse”, “projected\_qty”, “reserved\_qty”, …), or\_filters = mapping of field → list(“!=”, 0) for field drawn from QTY\_FIELDS, filters = filters, order ….
  - Draw field from QTY\_FIELDS.
- Set item\_code\_list from list(set of i.item\_code for i drawn from items).
  - Draw i from items.
- Set warehouse\_list from list(set of i.warehouse for i drawn from items).
  - Draw i from items.
- Set sre\_reserved\_stock\_details from get\_reserved\_stock\_details(item\_code\_list, warehouse\_list).
- Set precision from cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)).
- For each item in items.
  - Evaluate item.update(mapping(“item\_code” → escape\_html(item.item\_code), “item\_name” → escape\_html(Platform.get\_cached\_value(“Item”, item.item\_code, “item\_name”)), “stock\_uom” → escape\_html(Platform.get\_cached\_value ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, item.item\_code, “has\_batch\_no”) → Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”).
- Return items.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bin”, “read”), Platform.has\_permission(“Warehouse”, “read”) · configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”), Platform.get\_cached\_value(“Item”, item.item\_code, “item\_name”) and 3 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L691)

## Record · Item lead time

[Record definition](../../../../data/record-types/item_lead_time.json)

<a id="op-9088aae2b646cf"></a>
### Item Lead Time.validate

`operation_enterprise_stock_record_definitions_item_lead_time_business_behavior_item_lead_time_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_capacity\_per\_day().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set capacity per day](operations-026.md#op-c0235cdba3ba36).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1150)
