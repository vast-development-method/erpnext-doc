# Production · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Blanket order

[Record definition](../../../../data/record-types/blanket_order.json)

<a id="op-2802de62a43822"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “blanket\_order”, “transactions” → list(mapping(“items” → list(“Purchase Order”, “Sales Order”, “Quotation”)))).

**Local steps**

- Return mapping(“fieldname” → “blanket\_order”, “transactions” → list(mapping(“items” → list(“Purchase Order”, “Sales Order”, “Quotation”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L3095) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L334)

<a id="op-a1a0d8ece7c843"></a>
### Get order type config

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_get_order_type_configuration`

**Inputs** blanket\_order\_type.

**Explicit results** \_ORDER\_TYPE\_CONFIG at blanket\_order\_type.

**Local steps**

- Return \_ORDER\_TYPE\_CONFIG at blanket\_order\_type.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L3207) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L339)

<a id="op-d667ec70f0b5e0"></a>
### Get exchange rate to company

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_get_exchange_rate_to_company`

**Inputs** doc, currency.

**Explicit results** get\_exchange\_rate(currency, get\_company\_currency(doc.company), doc.from\_date, config at “exchange\_rate\_type”).

**Local steps**

- Set config from get\_order\_type\_config(doc.blanket\_order\_type).
- Return get\_exchange\_rate(currency, get\_company\_currency(doc.company), doc.from\_date, config at “exchange\_rate\_type”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L3251) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L338)

<a id="op-8141bb5ed4a953"></a>
### Set price list

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_set_price_list`

**Inputs** doc, set\_default = false, force\_exchange\_rate = false.

**Record and data access** read “Price List” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Price List {0} is disabled or does not exist”.format(Platform.bold(price\_list)) · validation helper — translated “Price List {0} is not enabled for {1}”.format(Platform.bold(price\_list), Platform.bold(doc.blanket\_order\_type)).

**Local steps**

- Set config from get\_order\_type\_config(doc.blanket\_order\_type).
- Set fieldname from config at “price\_list\_field”.
- Evaluate doc.set(config at “opposite\_price\_list\_field”, no value).
- If (not doc.get(fieldname) and (doc.is\_new() or set\_default)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.get(fieldname) → (doc.is\_new() or set\_default).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → set\_default.
  - Evaluate doc.set(fieldname, get\_default\_price\_list(doc)).
- Set price\_list from doc.get(fieldname).
- If not price\_list.
  - Evaluate clear\_price\_list(doc).
  - Return no value.
- Set price\_list\_type from config at “price\_list\_type”.lower().
- Set price\_list\_details from Platform.get\_cached\_value(“Price List”, price\_list, list(“currency”, price\_list\_type, “enabled”), as\_dict = true).
- If (not price\_list\_details or not price\_list\_details.enabled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not price\_list\_details → not price\_list\_details.enabled.
  - Call the validation error handler Platform.throw(translated “Price List {0} is disabled or does not exist”.format(Platform.bold(price\_list))).
- If not price\_list\_details.get(price\_list\_type).
  - Call the validation error handler Platform.throw(translated “Price List {0} is not enabled for {1}”.format(Platform.bold(price\_list), Platform.bold(doc.blanket\_order\_type))).
- Set price\_list\_currency\_changed from doc.price\_list\_currency differs from price\_list\_details.currency.
- Set doc.price\_list\_currency from price\_list\_details.currency.
- Set company\_currency from get\_company\_currency(doc.company).
- If doc.price\_list\_currency equals company\_currency.
  - Set doc.plc\_conversion\_rate from 1.0.
- Otherwise.
  - If (price\_list\_currency\_changed or not doc.plc\_conversion\_rate or force\_exchange\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in price\_list\_currency\_changed → not doc.plc\_conversion\_rate → force\_exchange\_rate.
    - Set doc.plc\_conversion\_rate from get\_exchange\_rate\_to\_company(doc, doc.price\_list\_currency).
- Evaluate validate\_conversion\_rate(doc.price\_list\_currency, doc.plc\_conversion\_rate, doc.meta.get\_translated\_label(“plc\_conversion\_rate”), doc.company).
- Set doc.plc\_conversion\_rate from flt(doc.plc\_conversion\_rate, doc.precision(“plc\_conversion\_rate”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, list(“currency”, price\_list\_type, “enabled”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L3382) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L343)

<a id="op-12629636cdf764"></a>
### Clear price list

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_clear_price_list`

**Inputs** doc.

**Local steps**

- Set doc.price\_list\_currency from no value.
- Set doc.plc\_conversion\_rate from 0.
- For each item in doc.items.
  - Set item.price\_list\_rate from 0.
  - Set item.base\_price\_list\_rate from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L4353) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L336)

<a id="op-ef8029b7ee84d2"></a>
### Get default price list

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_get_default_price_list`

**Inputs** doc.

**Record and data access** resolve a document from party\_type via get\_cached\_doc · read config at “settings\_doctype” via get\_single\_value.

**Explicit results** party\_price\_list · Platform.db.get\_single\_value(config at “settings\_doctype”, config at “price\_list\_field”).

**Local steps**

- Set config from get\_order\_type\_config(doc.blanket\_order\_type).
- Set party\_type from config at “party\_type”.
- Set party from doc.get(config at “party\_field”).
- If party.
  - Set party\_price\_list from get\_party\_default\_price\_list(Platform.get\_cached\_doc(party\_type, party)).
  - If party\_price\_list.
    - Return party\_price\_list.
- Return Platform.db.get\_single\_value(config at “settings\_doctype”, config at “price\_list\_field”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(party\_type, party), Platform.db.get\_single\_value(config at “settings\_doctype”, config at “price\_list\_field”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L4469) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L337)

<a id="op-af4445c2b0fe61"></a>
### Get price list rates

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_get_price_list_rates`

**Inputs** doc, item\_name = no value.

**Explicit results** list() · list of mapping(“name” → item.name, “price\_list\_rate” → 0, “base\_price\_list\_rate” → 0) for item drawn from items · rates.

**Local steps**

- Set price\_list from doc.get(get\_order\_type\_config(doc.blanket\_order\_type) at “price\_list\_field”).
- Set items from list of item for item drawn from doc.items where (item.item\_code and (not item\_name or item.name equals item\_name)).
  - Draw item from doc.items, keep a combination only if ((item.item\_code and (not item\_name or item.name equals item\_name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code → (not item\_name or item.name equals item\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_name → item.name equals item\_name.
- If not items.
  - Return list().
- If not price\_list.
  - Return list of mapping(“name” → item.name, “price\_list\_rate” → 0, “base\_price\_list\_rate” → 0) for item drawn from items.
    - Draw item from items.
- Set ctx from Platform.\_dict(mapping(“price\_list” → price\_list, “customer” → doc.customer, “supplier” → doc.supplier, “transaction\_date” → doc.from\_date)).
- Set item\_prices from get\_item\_prices\_for\_stock\_uom(ctx, list(dict.fromkeys(generator of item.item\_code for item drawn from items))).
  - Draw item from items.
- Set rates from list().
- For each item in items.
  - Set item\_price from item\_prices.get(item.item\_code).
  - Set qty from (flt(item.qty) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.qty) → 1.
  - Set packing\_unit from flt(item\_price.packing\_unit) when item\_price, otherwise 0.
    - Value choice on item\_price — true gives flt(item\_price.packing\_unit), false gives 0.
  - Set price\_list\_rate from item\_price.price\_list\_rate when (item\_price and (not packing\_unit or (qty modulo or format packing\_unit) equals 0)), otherwise no value.
    - Value choice on (item\_price and (not packing\_unit or (qty modulo or format packing\_unit) equals 0)) — true gives item\_price.price\_list\_rate, false gives no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_price → (not packing\_unit or (qty modulo or format packing\_unit) equals 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not packing\_unit → (qty modulo or format packing\_unit) equals 0.
  - Set rate\_details from mapping(“name” → item.name, “price\_list\_rate” → 0, “base\_price\_list\_rate” → 0).
  - If price\_list\_rate is distinct from no value.
    - Set rate from ((flt(price\_list\_rate) × flt(doc.plc\_conversion\_rate)) ÷ flt(doc.conversion\_rate)).
    - Set tuple(price\_list\_rate, base\_price\_list\_rate) from get\_rate\_and\_base\_amount(doc, item, “price\_list\_rate”, rate).
    - Set tuple(rate, base\_rate) from get\_rate\_and\_base\_amount(doc, item, “rate”, rate).
    - Evaluate rate\_details.update(mapping(“price\_list\_rate” → price\_list\_rate, “base\_price\_list\_rate” → base\_price\_list\_rate, “rate” → rate, “base\_rate” → base\_rate)).
  - Evaluate rates.append(rate\_details).
- Return rates.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L340)

<a id="op-00013dd7a7ddc9"></a>
### Set base rates

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_set_base_rates`

**Inputs** doc.

**Local steps**

- For each item in doc.items.
  - For each fieldname in tuple(“price\_list\_rate”, “rate”).
    - Set tuple(rate, base\_rate) from get\_rate\_and\_base\_amount(doc, item, fieldname, item.get(fieldname)).
    - Evaluate item.set(fieldname, rate).
    - Evaluate item.set(formatted text base\_{fieldname}, base\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L5861) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L342)

<a id="op-5573fb2f73a7f4"></a>
### Get rate and base amount

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_get_rate_and_base_amount`

**Inputs** doc, item, fieldname, rate.

**Explicit results** tuple(rate, base\_rate).

**Local steps**

- Set rate from flt(rate, item.precision(fieldname)).
- Set base\_fieldname from formatted text base\_{fieldname}.
- Set base\_rate from flt((rate × flt(doc.conversion\_rate)), item.precision(base\_fieldname)).
- Return tuple(rate, base\_rate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0452.json#L6079) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L341)

<a id="op-d5edf414ab48d8"></a>
### Apply price list

`operation_enterprise_manufacturing_record_definitions_blanket_order_blanket_order_pricing_business_behavior_apply_price_list`

**Inputs** doc, item\_name = no value, reset\_party\_values = false, reset\_plc\_conversion\_rate = false, reset\_conversion\_rate = false.

**Record and data access** resolve a document from Platform.parse\_json(doc) via get\_doc.

**Explicit results** mapping(“parent” → mapping(“currency” → doc.currency, “conversion\_rate” → doc.conversion\_rate, “selling\_price\_list” → doc.selling\_price\_list, “buying\_price\_list” → doc.buying\_price\_list, …), “children” → g ….

**Local steps**

- Set doc from Platform.get\_doc(Platform.parse\_json(doc)).
- Evaluate doc.check\_permission(“read”).
- Evaluate validate\_pricing\_parties(doc).
- Set reset\_party\_values from cint(reset\_party\_values).
- Set reset\_plc\_conversion\_rate from cint(reset\_plc\_conversion\_rate).
- Set reset\_conversion\_rate from cint(reset\_conversion\_rate).
- If reset\_party\_values.
  - Set doc.currency from no value.
  - Set doc.conversion\_rate from 0.
  - Set doc.selling\_price\_list from no value.
  - Set doc.buying\_price\_list from no value.
  - Set doc.price\_list\_currency from no value.
  - Set doc.plc\_conversion\_rate from 0.
- Otherwise.
  - If reset\_conversion\_rate.
    - Set doc.conversion\_rate from 0.
  - If reset\_plc\_conversion\_rate.
    - Set doc.plc\_conversion\_rate from 0.
- Evaluate doc.set\_currency().
- Evaluate doc.set\_conversion\_rate().
- Evaluate set\_price\_list(doc, set\_default = reset\_party\_values, force\_exchange\_rate = (reset\_party\_values or reset\_plc\_conversion\_rate)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reset\_party\_values → reset\_plc\_conversion\_rate.
- Return mapping(“parent” → mapping(“currency” → doc.currency, “conversion\_rate” → doc.conversion\_rate, “selling\_price\_list” → doc.selling\_price\_list, “buying\_price\_list” → doc.buying\_price\_list, …), “children” → g ….

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L335)

## Record · Bom

<a id="op-c6dd248af089ce"></a>
### BOMTree.initialize

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_tree_initialize`

**Inputs** self, name, is\_bom = true, exploded\_qty = 1.0, qty = 1.

**Declared result** no value.

**Local steps**

- Set self.name from name.
- Set self.child\_items from list().
- Set self.is\_bom from is\_bom.
- Set self.item\_code from no value.
- Set self.qty from qty.
- Set self.exploded\_qty from exploded\_qty.
- If not self.is\_bom.
  - Set self.item\_code from self.name.
- Otherwise.
  - Evaluate self.\_\_create\_tree().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create tree](operations-002.md#op-94212474314931).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L3189) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L195)

<a id="op-94212474314931"></a>
### BOMTree.create tree

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_tree_create_tree`

**Inputs** self.

**Record and data access** resolve a document from “BOM” via get\_cached\_doc.

**Local steps**

- Set bom from Platform.get\_cached\_doc(“BOM”, self.name).
- Set self.item\_code from bom.item.
- Set self.bom\_qty from bom.quantity.
- For each item in bom.get(“items”, list()).
  - Set qty from (item.stock\_qty ÷ bom.quantity).
  - Set exploded\_qty from (self.exploded\_qty × qty).
  - If item.bom\_no.
    - Set child from BOMTree(item.bom\_no, exploded\_qty = exploded\_qty, qty = qty).
    - Evaluate self.child\_items.append(child).
  - Otherwise.
    - Evaluate self.child\_items.append(BOMTree(item.item\_code, is\_bom = false, exploded\_qty = exploded\_qty, qty = qty)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“BOM”, self.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L3451) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L194)

<a id="op-205ece294df7e8"></a>
### BOMTree.level order traversal

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_tree_level_order_traversal`

**Inputs** self.

**Declared result** list at “BOMTree”.

**Explicit results** traversal.

**Local steps**

- Set traversal from list().
- Set q from deque().
- Evaluate q.append(self).
- While q.
  - Set node from q.popleft().
  - For each child in node.child\_items.
    - Evaluate traversal.append(child).
    - Evaluate q.append(child).
- Return traversal.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L3821) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L196)

<a id="op-d2ed47bebb51b6"></a>
### BOMTree.str

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_tree_text`

**Inputs** self.

**Declared result** str.

**Explicit results** formatted text {self.item\_code}{(“ - ” + self.name) when self.is\_bom, otherwise empty text} qty(per unit): {self.qty} exploded\_qty: {self.exploded\_qty}.

**Local steps**

- Return formatted text {self.item\_code}{(“ - ” + self.name) when self.is\_bom, otherwise empty text} qty(per unit): {self.qty} exploded\_qty: {self.exploded\_qty}.
  - Value choice on self.is\_bom — true gives (“ - ” + self.name), false gives empty text.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L4028) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L198)

<a id="op-b5b75a2d72d4f8"></a>
### BOMTree.repr

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_tree_representation`

**Inputs** self, level = 0.

**Declared result** str.

**Explicit results** rep.

**Local steps**

- Set rep from ((((“┃  ” × (level − 1)) + (“┣━ ” × level &gt; 0)) + str(self)) + whitespace '\\n').
- For each child in self.child\_items.
  - Update rep using + child.\_\_repr\_\_(level = (level + 1)).
- Return rep.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L4167) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L197)

<a id="op-bdbb0c5c59aa87"></a>
### BOM.autoname

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_autoname`

**Inputs** self.

**Record and data access** read “BOM” via get\_all · read “BOM” via exists.

**Local steps**

- Set search\_key from formatted text {self.doctype}-{self.item}%.
- Set existing\_boms from Platform.get\_all(“BOM”, filters = mapping(“name” → search\_key, “amended\_from” → list(“is”, “not set”)), pluck = “name”).
- Set index from self.get\_index\_for\_bom(existing\_boms).
- Set prefix from self.doctype.
- Set suffix from (“%.3i” modulo or format index).
- Set bom\_name from formatted text {prefix}-{self.item}-{suffix}.
- If len(bom\_name) ≤ 140.
  - Set name from bom\_name.
- Otherwise.
  - Set truncated\_length from (140 − ((len(prefix) + len(suffix)) + 2)).
  - Set truncated\_item\_name from self.item at slice no value to truncated\_length.
  - Set truncated\_item\_name from truncated\_item\_name.rsplit(one space, 1) at 0.
  - Set name from formatted text {prefix}-{truncated\_item\_name}-{suffix}.
- If Platform.db.exists(“BOM”, name).
  - Set existing\_boms from Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“like”, search\_key), “amended\_from” → list(“is”, “not set”)), pluck = “name”).
  - Set index from self.get\_index\_for\_bom(existing\_boms).
  - Set suffix from (“%.3i” modulo or format index).
  - Set name from formatted text {prefix}-{self.item}-{suffix}.
- Set self.name from name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get index for bom](operations-002.md#op-cf21c5bdd290ed).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L150)

<a id="op-cf21c5bdd290ed"></a>
### BOM.get index for bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_index_for_bill_of_materials`

**Inputs** self, existing\_boms.

**Explicit results** index.

**Local steps**

- Set index from 1.
- If existing\_boms.
  - Set index from self.get\_next\_version\_index(existing\_boms).
- Return index.

**Methods declared on this owner** [get next version index](operations-002.md#op-f6632fe8a3e4ea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L5242) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L166)

<a id="op-68824790c7a65c"></a>
### BOM.onload

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_onload`

**Inputs** self.

**Local steps**

- Evaluate super().onload().
- Evaluate self.set\_onload\_for\_multi\_level\_bom().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set onload for multi level bom](operations-002.md#op-8aadd57db44c30).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L5341) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L181)

<a id="op-8aadd57db44c30"></a>
### BOM.set onload for multi level bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_onload_for_multi_level_bill_of_materials`

**Inputs** self.

**Record and data access** read “Property Setter” via get\_value.

**Local steps**

- Set use\_multi\_level\_bom from Platform.db.get\_value(“Property Setter”, mapping(“field\_name” → “use\_multi\_level\_bom”, “doc\_type” → “Work Order”, “property” → “default”), “value”).
- If use\_multi\_level\_bom is identical to no value.
  - Set use\_multi\_level\_bom from 1.
- Evaluate self.set\_onload(“use\_multi\_level\_bom”, cint(use\_multi\_level\_bom)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L5418) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L187)

<a id="op-f6632fe8a3e4ea"></a>
### BOM.get next version index

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_next_version_index`

**Inputs** existing\_boms.

**Wrappers, in declaration order** staticmethod.

**Declared result** int.

**Explicit results** index.

**Local steps**

- Set delimiters from list(“/”, “-”).
- Set pattern from “\|”.join(map(re.escape, delimiters)).
- Set bom\_parts from list of re.split(pattern, bom\_name) for bom\_name drawn from existing\_boms.
  - Draw bom\_name from existing\_boms.
- Set valid\_bom\_parts from list(filter(deferred anonymous expression, bom\_parts)).
- If valid\_bom\_parts.
  - Set indexes from list of cint(part at negative 1) for part drawn from valid\_bom\_parts.
    - Draw part from valid\_bom\_parts.
  - Set index from (max(indexes) + 1).
- Otherwise.
  - Set index from 1.
- Return index.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L5645) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L169)

<a id="op-69f994e191206b"></a>
### BOM.before validate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_before_validate`

**Inputs** self.

**Record and data access** read “UOM Conversion Detail” via get\_value.

**Local steps**

- For each item in self.items.
  - If not item.conversion\_factor.
    - Set item.conversion\_factor from (Platform.get\_value(“UOM Conversion Detail”, mapping(“parent” → item.item\_code, “uom” → item.uom), “conversion\_factor”) or 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_value(“UOM Conversion Detail”, mapping(“parent” → item.item\_code, “uom” → item.uom), “conversion\_factor”) → 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0454.json#L6039) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L151)

<a id="op-4a48b105c1b4fe"></a>
### BOM.validate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select a Company first.”.

**Local steps**

- Set self.route from Platform.scrub(self.name).replace(“\_”, “-”).
- If not self.company.
  - Call the validation error handler Platform.throw(translated “Please select a Company first.”, title = translated “Mandatory”).
- Evaluate self.clear\_operations().
- Evaluate self.clear\_inspection().
- Evaluate self.validate\_main\_item().
- Evaluate self.validate\_currency().
- Evaluate self.set\_operation\_finished\_goods().
- Evaluate self.set\_materials\_based\_on\_operation\_bom().
- Evaluate self.set\_conversion\_rate().
- Evaluate self.set\_plc\_conversion\_rate().
- Evaluate self.validate\_uom\_is\_interger().
- Evaluate self.set\_bom\_material\_details().
- Evaluate self.set\_secondary\_items\_details().
- Evaluate self.validate\_materials().
- Evaluate self.validate\_transfer\_against().
- Evaluate self.set\_routing\_operations().
- Evaluate self.validate\_operations().
- Evaluate self.update\_stock\_qty().
- Evaluate self.calculate\_cost().
- Evaluate self.update\_exploded\_items(save = false).
- Evaluate self.update\_cost(update\_parent = false, from\_child\_bom = true, update\_hour\_rate = false, save = false).
- Evaluate self.set\_process\_loss\_qty().
- Evaluate self.validate\_uoms().
- Evaluate self.set\_default\_uom().
- Evaluate self.validate\_semi\_finished\_goods().
- Evaluate self.validate\_secondary\_items().
- Evaluate self.validate\_secondary\_items\_cost().
- Evaluate self.validate\_total\_cost\_allocation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear operations](operations-004.md#op-138e1223070aba), [clear inspection](operations-004.md#op-c1abbe469b9d82), [validate main item](operations-004.md#op-6d1e90684e9adc), [validate currency](operations-004.md#op-ff60beef71204c), [set operation finished goods](operations-002.md#op-1047ca55ee0d6b), [set materials based on operation bom](operations-004.md#op-6bdcb38e2bc9e4), [set conversion rate](operations-004.md#op-2ea08a92d23a47), [set plc conversion rate](operations-004.md#op-afcec7fccd031c), [validate uom is interger](operations-004.md#op-cdb478fec9f2da), [set bom material details](operations-003.md#op-d76d1cc2bd2e28), [set secondary items details](operations-003.md#op-bccb041dd8f211), [validate materials](operations-004.md#op-09224d1a506b48), [validate transfer against](operations-005.md#op-234550e01075c7), [set routing operations](operations-005.md#op-6a54ad541f54ba), [validate operations](operations-005.md#op-7c81b185fa5b7c), [update stock qty](operations-004.md#op-ff59a363479ac1), [calculate cost](operations-005.md#op-0154f61889ef02), [update exploded items](operations-005.md#op-ff5f728a71231c), [update cost](operations-004.md#op-c4372c2b24970d), [set process loss qty](operations-006.md#op-84602c279c691c), [validate uoms](operations-006.md#op-3d35030e004353), [set default uom](operations-003.md#op-589792c31133c7), [validate semi finished goods](operations-003.md#op-6c3ba70ff05e0c), [validate secondary items](operations-003.md#op-80bbb333d79e64), [validate secondary items cost](operations-003.md#op-91cb228da29792), [validate total cost allocation](operations-003.md#op-4f7b7f02407b31).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L206)

<a id="op-1047ca55ee0d6b"></a>
### BOM.set operation finished goods

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_operation_finished_goods`

**Inputs** self.

**Record and data access** read “BOM” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not self.track\_semi\_finished\_goods.
  - Return no value.
- For each row in self.operations.
  - If (row.bom\_no and not row.finished\_good).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.bom\_no → not row.finished\_good.
    - Set row.finished\_good from Platform.get\_cached\_value(“BOM”, row.bom\_no, “item”).
- Evaluate self.set\_default\_last\_step().
- For each row in self.operations.
  - If (row.is\_final\_finished\_good and not row.finished\_good).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_final\_finished\_good → not row.finished\_good.
    - Set row.finished\_good from self.item.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default last step](operations-002.md#op-b72e2a4258b469).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, row.bom\_no, “item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L188)

<a id="op-b72e2a4258b469"></a>
### BOM.set default last step

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_set_default_last_step`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.operations or any(generator of row.is\_final\_finished\_good for row drawn from self.operations)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.operations → any(generator of row.is\_final\_finished\_good for row drawn from self.operations).
  - Draw row from self.operations.
  - Return no value.
- Set makes\_bom\_item from list of row for row drawn from self.operations where row.finished\_good equals self.item.
  - Draw row from self.operations, keep a combination only if (row.finished\_good equals self.item).
- If len(makes\_bom\_item) equals 1.
  - Set makes\_bom\_item at 0.is\_final\_finished\_good from 1.
- Otherwise.
  - If (not makes\_bom\_item and not self.operations at negative 1.finished\_good).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not makes\_bom\_item → not self.operations at negative 1.finished\_good.
    - Set self.operations at negative 1.is\_final\_finished\_good from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L636)
