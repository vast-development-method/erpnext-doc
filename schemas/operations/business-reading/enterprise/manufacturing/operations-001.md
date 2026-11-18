# Production · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Blanket order

[Record definition](../../../../data/record-types/blanket_order.json)

<a id="op-9c1878a7786247"></a>
### Blanket Order.before validate

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_before_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.blanket\_order\_type.
  - Return no value.
- Evaluate self.set\_currency().
- Evaluate self.set\_conversion\_rate().
- Evaluate blanket\_order\_pricing.set\_price\_list(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set currency](operations-001.md#op-63402f72fe691b), [set conversion rate](operations-001.md#op-7daadff107d4d5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L345)

<a id="op-6692e598e970f4"></a>
### Blanket Order.validate

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate validate\_terms\_and\_conditions(self.get(“tc\_name”), “selling” when self.blanket\_order\_type equals “Selling”, otherwise “buying”).
  - Value choice on self.blanket\_order\_type equals “Selling” — true gives “selling”, false gives “buying”.
- If not self.blanket\_order\_type.
  - Return no value.
- Evaluate self.validate\_party().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_duplicate\_items().
- Evaluate self.validate\_item\_qty().
- Evaluate self.set\_party\_item\_code().
- Evaluate self.set\_base\_rates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate party](operations-001.md#op-3fda83f32b7a72), [validate dates](operations-001.md#op-429c98ed55b28b), [validate duplicate items](operations-001.md#op-60b61410f8e985), [validate item qty](operations-001.md#op-d53897914b20bd), [set party item code](operations-001.md#op-2e27fde5651512), [set base rates](operations-001.md#op-8e08fb37a07aa3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L353)

<a id="op-16e3e25c935a4e"></a>
### Blanket Order.before update after submit

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_blanketorder_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-001.md#op-429c98ed55b28b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L610)

<a id="op-151adf287b2a9e"></a>
### Blanket Order.validate qty can be ordered

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_blanketorder_validate_qty_can_be_ordered`

**Inputs** self, item\_data, order\_doctype.

**Declared result** no value.

**Record and data access** read “Selling Settings” when order\_doctype equals “Sales Order”, otherwise “Buying Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Item {0} cannot be ordered more than {1} against Blanket Order {2}.”.format(item.item\_code, allowed\_qty, self.name).

**Local steps**

- Set allowance from flt(Platform.db.get\_single\_value(“Selling Settings” when order\_doctype equals “Sales Order”, otherwise “Buying Settings”, “blanket\_order\_allowance”)).
  - Value choice on order\_doctype equals “Sales Order” — true gives “Selling Settings”, false gives “Buying Settings”.
- For each item in self.get(“items”).
  - If item.item\_code does not belong to item\_data.
    - Continue with the next iteration or loop test.
  - Set precision from item.precision(“qty”).
  - Set allowed\_qty from flt(((item.qty + ((item.qty × allowance) ÷ 100)) − item.ordered\_qty), precision).
  - If (item.qty and allowed\_qty &lt; flt(item\_data at item.item\_code, precision)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.qty → allowed\_qty &lt; flt(item\_data at item.item\_code, precision).
    - Call the validation error handler Platform.throw(translated “Item {0} cannot be ordered more than {1} against Blanket Order {2}.”.format(item.item\_code, allowed\_qty, self.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings” when order\_doctype equals “Sales Order”, otherwise “Buying Settings”, “blanket\_order\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L614)

<a id="op-3fda83f32b7a72"></a>
### Blanket Order.validate party

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_blanketorder_validate_party`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “{0} is mandatory for a {1} Blanket Order”.format(translated self.meta.get\_label(party\_field), translated self.blanket\_order\_type).

**Local steps**

- Set party\_field from blanket\_order\_pricing.get\_order\_type\_config(self.blanket\_order\_type) at “party\_field”.
- If not self.get(party\_field).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory for a {1} Blanket Order”.format(translated self.meta.get\_label(party\_field), translated self.blanket\_order\_type), Platform.MandatoryError).
- Set other\_party\_field from “supplier” when party\_field equals “customer”, otherwise “customer”.
  - Value choice on party\_field equals “customer” — true gives “supplier”, false gives “customer”.
- Evaluate self.set(other\_party\_field, no value).
- Evaluate self.set(formatted text {other\_party\_field}\_name, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L613)

<a id="op-06566c1db0aaa8"></a>
### Blanket Order.validate order matches

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_blanketorder_validate_order_matches`

**Inputs** self, order\_doc.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Blanket Order {0} is a {1} order and cannot be used on a {2}”.format(Platform.bold(self.name), translated self.blanket\_order\_type, translated order\_doc.doctype) · validation helper — translated “Blanket Order {0} is for {1}, not {2}”.format(Platform.bold(self.name), Platform.bold(self.get(party\_field)), Platform.bold(order\_doc.get(party\_field))) · validation helper — translated “Blanket Order {0} is in {1}, not {2}”.format(Platform.bold(self.name), self.currency, order\_doc.currency).

**Local steps**

- Set tuple(order\_type, party\_field) from ORDER\_TYPE\_BY\_DOCTYPE at order\_doc.doctype.
- If self.blanket\_order\_type differs from order\_type.
  - Call the validation error handler Platform.throw(translated “Blanket Order {0} is a {1} order and cannot be used on a {2}”.format(Platform.bold(self.name), translated self.blanket\_order\_type, translated order\_doc.doctype)).
- If self.get(party\_field) differs from order\_doc.get(party\_field).
  - Call the validation error handler Platform.throw(translated “Blanket Order {0} is for {1}, not {2}”.format(Platform.bold(self.name), Platform.bold(self.get(party\_field)), Platform.bold(order\_doc.get(party\_field)))).
- If self.currency differs from order\_doc.currency.
  - Call the validation error handler Platform.throw(translated “Blanket Order {0} is in {1}, not {2}”.format(Platform.bold(self.name), self.currency, order\_doc.currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L612)

<a id="op-c6b480bd5ef490"></a>
### Blanket Order.set order rates

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_blanketorder_set_order_rates`

**Inputs** self, order\_doc.

**Declared result** no value.

**State and service calls** msgprint with translated “Row #{0}: Rate {1} differs from the rate {2} agreed in Blanket Order {3}”.format(row.idx, row.rate, expected\_rate, Platform.bold(self.name)).

**Local steps**

- Set rates from mapping of row.item\_code → flt(row.rate) for row drawn from self.items.
  - Draw row from self.items.
- For each row in order\_doc.get(“items”).
  - If (row.blanket\_order differs from self.name or row.item\_code does not belong to rates).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.blanket\_order differs from self.name → row.item\_code does not belong to rates.
    - Continue with the next iteration or loop test.
  - Set row.blanket\_order\_rate from rates at row.item\_code.
  - Set expected\_rate from flt((row.blanket\_order\_rate × (flt(row.conversion\_factor) or 1)), row.precision(“rate”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.
  - If flt(row.rate, row.precision(“rate”)) differs from expected\_rate.
    - Evaluate Platform.msgprint(translated “Row #{0}: Rate {1} differs from the rate {2} agreed in Blanket Order {3}”.format(row.idx, row.rate, expected\_rate, Platform.bold(self.name)), alert = true, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L611)

<a id="op-63402f72fe691b"></a>
### Blanket Order.set currency

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_set_currency`

**Inputs** self.

**Record and data access** read party\_type via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If self.currency.
  - Return no value.
- Set config from blanket\_order\_pricing.get\_order\_type\_config(self.blanket\_order\_type).
- Set party\_type from config at “party\_type”.
- Set party from self.get(config at “party\_field”).
- Set party\_currency from Platform.get\_cached\_value(party\_type, party, “default\_currency”) when party, otherwise no value.
  - Value choice on party — true gives Platform.get\_cached\_value(party\_type, party, “default\_currency”), false gives no value.
- Set self.currency from (party\_currency or get\_company\_currency(self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_currency → get\_company\_currency(self.company).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(party\_type, party, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L4943) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L350)

<a id="op-7daadff107d4d5"></a>
### Blanket Order.set conversion rate

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_set_conversion_rate`

**Inputs** self.

**Local steps**

- Set company\_currency from get\_company\_currency(self.company).
- If self.currency equals company\_currency.
  - Set self.conversion\_rate from 1.0.
- Otherwise.
  - If not self.conversion\_rate.
    - Set self.conversion\_rate from blanket\_order\_pricing.get\_exchange\_rate\_to\_company(self, self.currency).
- Evaluate validate\_conversion\_rate(self.currency, self.conversion\_rate, self.meta.get\_translated\_label(“conversion\_rate”), self.company).
- Set self.conversion\_rate from flt(self.conversion\_rate, self.precision(“conversion\_rate”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L5188) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L349)

<a id="op-429c98ed55b28b"></a>
### Blanket Order.validate dates

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From date cannot be greater than To date”.

**Local steps**

- If getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “From date cannot be greater than To date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L5484) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L354)

<a id="op-2e27fde5651512"></a>
### Blanket Order.set party item code

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_set_party_item_code`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set item\_ref from mapping().
- If self.blanket\_order\_type equals “Selling”.
  - Set item\_ref from self.get\_customer\_items\_ref().
- Otherwise.
  - Set item\_ref from self.get\_supplier\_items\_ref().
- If not item\_ref.
  - Return no value.
- For each row in self.items.
  - Set row.party\_item\_code from item\_ref.get(row.item\_code).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get customer items ref](operations-001.md#op-67988610ac9510), [get supplier items ref](operations-001.md#op-d5679b800d8ddf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L5611) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L351)

<a id="op-67988610ac9510"></a>
### Blanket Order.get customer items ref

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_get_customer_items_reference`

**Inputs** self.

**Record and data access** read “Item Customer Detail” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Item Customer Detail”, filters = mapping(“parent” → tuple(“in”, items), “customer\_name” → self.customer), fields = list(“parent”, “ref\_code”), as\_list = true)).

**Local steps**

- Set items from list of d.item\_code for d drawn from self.items.
  - Draw d from self.items.
- Return Platform.\_dict(Platform.get\_all(“Item Customer Detail”, filters = mapping(“parent” → tuple(“in”, items), “customer\_name” → self.customer), fields = list(“parent”, “ref\_code”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L5811) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L346)

<a id="op-d5679b800d8ddf"></a>
### Blanket Order.get supplier items ref

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_get_supplier_items_reference`

**Inputs** self.

**Record and data access** read “Item Supplier” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Item Supplier”, filters = mapping(“parent” → tuple(“in”, items), “supplier” → self.supplier), fields = list(“parent”, “supplier\_part\_no”), as\_list = true)).

**Local steps**

- Set items from list of d.item\_code for d drawn from self.items.
  - Draw d from self.items.
- Return Platform.\_dict(Platform.get\_all(“Item Supplier”, filters = mapping(“parent” → tuple(“in”, items), “supplier” → self.supplier), fields = list(“parent”, “supplier\_part\_no”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L6021) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L347)

<a id="op-60b61410f8e985"></a>
### Blanket Order.validate duplicate items

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_validate_duplicate_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Note: Item {0} added multiple times”.format(Platform.bold(item.item\_code)).

**Local steps**

- Set item\_list from list().
- For each item in self.items.
  - If item.item\_code belongs to item\_list.
    - Call the validation error handler Platform.throw(translated “Note: Item {0} added multiple times”.format(Platform.bold(item.item\_code))).
  - Evaluate item\_list.append(item.item\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L6231) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L355)

<a id="op-9ec41f7aedbd6b"></a>
### Blanket Order.update ordered qty

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_update_ordered_quantity`

**Inputs** self.

**State and service calls** call db\_set on d.

**Local steps**

- Set ref\_doctype from “Sales Order” when self.blanket\_order\_type equals “Selling”, otherwise “Purchase Order”.
  - Value choice on self.blanket\_order\_type equals “Selling” — true gives “Sales Order”, false gives “Purchase Order”.
- Set trans from Platform.qb.DocType(ref\_doctype).
- Set trans\_item from Platform.qb.DocType(formatted text {ref\_doctype} Item).
- Set fulfilled\_qty from (IfNull(trans\_item at FULFILLED\_QTY\_FIELD at ref\_doctype, 0) × trans\_item.conversion\_factor).
- Set ordered\_qty from Case().when(trans.status.isin(list(“Stopped”, “Closed”)), fulfilled\_qty).else\_(trans\_item.stock\_qty).
- Set item\_ordered\_qty from Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(trans\_item.item\_code).run()).
- For each d in self.items.
  - Evaluate d.db\_set(“ordered\_qty”, item\_ordered\_qty.get(d.item\_code, 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L352)

<a id="op-d53897914b20bd"></a>
### Blanket Order.validate item qty

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_validate_item_quantity`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Quantity cannot be negative.”.format(d.idx).

**Local steps**

- For each d in self.items.
  - If flt(d.qty) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: Quantity cannot be negative.”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L356)

<a id="op-8e08fb37a07aa3"></a>
### Blanket Order.set base rates

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_blanket_order_set_base_rates`

**Inputs** self.

**Local steps**

- Evaluate blanket\_order\_pricing.set\_base\_rates(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L687) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L348)

<a id="op-493b541b668ae2"></a>
### Apply price list

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_apply_price_list`

**Inputs** doc, item\_name = no value, reset\_party\_values = false, reset\_plc\_conversion\_rate = false, reset\_conversion\_rate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** blanket\_order\_pricing.apply\_price\_list(doc = doc, item\_name = item\_name, reset\_party\_values = reset\_party\_values, reset\_plc\_conversion\_rate = reset\_plc\_conversion\_rate, …).

**Local steps**

- Return blanket\_order\_pricing.apply\_price\_list(doc = doc, item\_name = item\_name, reset\_party\_values = reset\_party\_values, reset\_plc\_conversion\_rate = reset\_plc\_conversion\_rate, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L743) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L344)

<a id="op-1ed80dcbdb7439"></a>
### Make order

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_make_order`

**Inputs** source\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Blanket Order” via get\_doc.

**Explicit results** target\_doc.

**Explicit failure paths** validation helper — translated “A {0} cannot be made from a {1} Blanket Order”.format(translated doctype, translated blanket\_order.blanket\_order\_type).

**Local steps**

- Set blanket\_order from Platform.get\_doc(“Blanket Order”, source\_name, check\_permission = “read”).
- Set doctype from Platform.flags.args.doctype.
- If doctype does not belong to ORDER\_DOCTYPES\_BY\_TYPE at blanket\_order.blanket\_order\_type.
  - Call the validation error handler Platform.throw(translated “A {0} cannot be made from a {1} Blanket Order”.format(translated doctype, translated blanket\_order.blanket\_order\_type)).
- Bind local operation update\_doc for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set target\_doc from get\_mapped\_doc(“Blanket Order”, source\_name, mapping(“Blanket Order” → mapping(“doctype” → doctype, “field\_no\_map” → list(“naming\_series”), “postprocess” → update\_doc), “Blanket Order Item” → mapping(“doct ….
- If target\_doc.doctype equals “Purchase Order”.
  - Evaluate target\_doc.set\_missing\_values().
- Return target\_doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L357)

<a id="op-af8c2050f8bcdf"></a>
### Make order.update doc

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_make_order_update_record`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- If doctype equals “Quotation”.
  - Set target\_doc.quotation\_to from “Customer”.
  - Set target\_doc.party\_name from source\_doc.customer.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L1846) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L359)

<a id="op-d238706985ddf5"></a>
### Make order.update item

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_make_order_update_item`

**Inputs** source, target, source\_parent.

**Local steps**

- Set target\_qty from (source.get(“qty”) − source.get(“ordered\_qty”)).
- Set target.qty from target\_qty when flt(target\_qty) ≥ 0, otherwise 0.
  - Value choice on flt(target\_qty) ≥ 0 — true gives target\_qty, false gives 0.
- Set item from get\_item\_defaults(target.item\_code, source\_parent.company).
- If item.
  - Set target.item\_name from item.get(“item\_name”).
  - Set target.description from item.get(“description”).
  - Set target.uom from item.get(“stock\_uom”).
  - Set target.against\_blanket\_order from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L1960) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L358)

<a id="op-5193d4d4701cd2"></a>
### Validate against blanket order

`operation_enterprise_manufacturing_record_definitions_blanket_order_business_behavior_validate_against_blanket_order`

**Inputs** order\_doc.

**Record and data access** resolve a document from “Blanket Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If order\_doc.doctype does not belong to tuple(“Sales Order”, “Purchase Order”).
  - Return no value.
- Set order\_data from mapping().
- For each item in order\_doc.get(“items”).
  - If (item.against\_blanket\_order and item.blanket\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.against\_blanket\_order → item.blanket\_order.
    - Set stock\_qty from (flt(item.qty) × (flt(item.conversion\_factor) or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.conversion\_factor) → 1.
    - Set item\_data from order\_data.setdefault(item.blanket\_order, mapping()).
    - Set item\_data at item.item\_code from (item\_data.get(item.item\_code, 0) + stock\_qty).
- For each tuple(bo\_name, item\_data) in sorted(order\_data.items()).
  - Set bo\_doc from Platform.get\_doc(“Blanket Order”, bo\_name, for\_update = true).
  - Evaluate bo\_doc.validate\_order\_matches(order\_doc).
  - Evaluate bo\_doc.validate\_qty\_can\_be\_ordered(item\_data, order\_doc.doctype).
  - Evaluate bo\_doc.set\_order\_rates(order\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L360)

<a id="op-ab73840e2769c9"></a>
### Validate reopen against blanket order

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_validate_reopen_against_blanket_order`

**Inputs** order\_doc, rows = no value.

**Record and data access** resolve a document from “Blanket Order” via get\_doc.

**Local steps**

- Set fulfilled\_field from FULFILLED\_QTY\_FIELD at order\_doc.doctype.
- If rows is identical to no value.
  - Set rows from list of item for item drawn from order\_doc.get(“items”) where not item.get(“closed”).
    - Draw item from order\_doc.get(“items”), keep a combination only if (not item.get(“closed”)).
- Set order\_data from mapping().
- For each item in rows.
  - If item.blanket\_order.
    - Set pending\_qty from ((flt(item.qty) − flt(item.get(fulfilled\_field))) × (flt(item.conversion\_factor) or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.conversion\_factor) → 1.
    - Set item\_data from order\_data.setdefault(item.blanket\_order, mapping()).
    - Set item\_data at item.item\_code from (item\_data.get(item.item\_code, 0) + max(pending\_qty, 0)).
- For each tuple(bo\_name, item\_data) in sorted(order\_data.items()).
  - Set bo\_doc from Platform.get\_doc(“Blanket Order”, bo\_name, for\_update = true).
  - Evaluate bo\_doc.validate\_qty\_can\_be\_ordered(item\_data, order\_doc.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L616)

<a id="op-cafaa1db813efb"></a>
### Refresh blanket orders of fulfilled rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_blanket_order_blanket_order_refresh_blanket_orders_of_fulfilled_rows`

**Inputs** doc.

**Record and data access** read order\_item\_doctype via get\_all · resolve a document from “Blanket Order” via get\_doc.

**Local steps**

- Set order\_rows from mapping().
- For each args in doc.status\_updater.
  - If args.get(“target\_field”) does not belong to tuple(“delivered\_qty”, “received\_qty”).
    - Continue with the next iteration or loop test.
  - If args.get(“target\_dt”) does not belong to tuple(“Sales Order Item”, “Purchase Order Item”).
    - Continue with the next iteration or loop test.
  - Set rows from order\_rows.setdefault(args at “target\_dt”, set()).
  - Evaluate rows.update(generator of d.get(args at “join\_field”) for d drawn from doc.get\_all\_children(args at “source\_dt”)).
    - Draw d from doc.get\_all\_children(args at “source\_dt”).
- For each tuple(order\_item\_doctype, rows) in order\_rows.items().
  - Evaluate rows.discard(no value).
  - If not rows.
    - Continue with the next iteration or loop test.
  - Set blanket\_orders from Platform.get\_all(order\_item\_doctype, filters = mapping(“name” → tuple(“in”, list(rows)), “blanket\_order” → tuple(“is”, “set”)), pluck = “blanket\_order”, distinct = true).
  - For each blanket\_order in sorted(blanket\_orders).
    - Evaluate Platform.get\_doc(“Blanket Order”, blanket\_order, for\_update = true).update\_ordered\_qty().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L615)
