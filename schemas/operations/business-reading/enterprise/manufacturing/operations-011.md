# Production · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom creator

<a id="op-92248e28525ff6"></a>
### Get code key

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_get_code_key`

**Inputs** value.

**Declared result** str.

**Explicit results** re.sub(“&#91;^0-9a-z&#93;”, empty text, (value or empty text).lower()).

**Local steps**

- Return re.sub(“&#91;^0-9a-z&#93;”, empty text, (value or empty text).lower()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L231) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L720)

<a id="op-104e9a919e4d7d"></a>
### Get name key

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_get_name_key`

**Inputs** value.

**Declared result** str.

**Explicit results** one space.join(sorted(words.split())).

**Local steps**

- Set words from re.sub(“(?&lt;=\\d)(?=&#91;a-z&#93;)\|(?&lt;=&#91;a-z&#93;)(?=\\d)”, one space, default\_process((value or empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
- Return one space.join(sorted(words.split())).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L233) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L722)

<a id="op-7ba90dbc4a106e"></a>
### Get numbers

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_get_numbers`

**Inputs** value.

**Declared result** list at str.

**Explicit results** sorted(generator of (number.lstrip(“0”) or “0”) for number drawn from re.findall(“\\d+”, value)).

**Local steps**

- Return sorted(generator of (number.lstrip(“0”) or “0”) for number drawn from re.findall(“\\d+”, value)).
  - Draw number from re.findall(“\\d+”, value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in number.lstrip(“0”) → “0”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L234) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L723)

<a id="op-dbe3885354478e"></a>
### Material Cost.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_init`

**Inputs** self, design.

**Local steps**

- Set self.design from design.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L743)

<a id="op-1163e59a6371f2"></a>
### Material Cost.set costs

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_set_costs`

**Inputs** self.

**Local steps**

- Evaluate self.set\_exchange\_rates().
- Evaluate self.set\_conversion\_factors().
- Evaluate self.set\_part\_rates().
- If self.design.track\_semi\_finished\_goods.
  - Set self.design.raw\_material\_cost from self.get\_operation\_plan\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set exchange rates](operations-011.md#op-7d0d970bb82c5c), [set conversion factors](operations-011.md#op-c6e7fd68cfa0d7), [set part rates](operations-011.md#op-5840259e4557f1), [get operation plan cost](operations-011.md#op-791cc51833e82b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L745)

<a id="op-7d0d970bb82c5c"></a>
### Material Cost.set exchange rates

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_set_exchange_rates`

**Inputs** self.

**Record and data access** read “Price List” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set design from self.design.
- Set company\_currency from Enterprise.get\_company\_currency(design.company).
- Set design.currency from (design.currency or company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in design.currency → company\_currency.
- If design.currency equals company\_currency.
  - Set design.conversion\_rate from 1.
- Otherwise.
  - If (flt(design.conversion\_rate) belongs to tuple(0, 1) or (not design.is\_new() and design.has\_value\_changed(“currency”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(design.conversion\_rate) belongs to tuple(0, 1) → (not design.is\_new() and design.has\_value\_changed(“currency”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not design.is\_new() → design.has\_value\_changed(“currency”).
    - Set design.conversion\_rate from get\_exchange\_rate(design.currency, company\_currency, args = “for\_buying”).
- If (design.rm\_cost\_as\_per differs from “Price List” or not design.buying\_price\_list).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in design.rm\_cost\_as\_per differs from “Price List” → not design.buying\_price\_list.
  - Set design.plc\_conversion\_rate from 1.
  - Return no value.
- Set design.price\_list\_currency from Platform.get\_cached\_value(“Price List”, design.buying\_price\_list, “currency”).
- If design.price\_list\_currency equals company\_currency.
  - Set design.plc\_conversion\_rate from 1.
- Otherwise.
  - If (flt(design.plc\_conversion\_rate) belongs to tuple(0, 1) or (not design.is\_new() and design.has\_value\_changed(“price\_list\_currency”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(design.plc\_conversion\_rate) belongs to tuple(0, 1) → (not design.is\_new() and design.has\_value\_changed(“price\_list\_currency”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not design.is\_new() → design.has\_value\_changed(“price\_list\_currency”).
    - Set design.plc\_conversion\_rate from get\_exchange\_rate(design.price\_list\_currency, company\_currency, args = “for\_buying”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, design.buying\_price\_list, “currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L746)

<a id="op-c6e7fd68cfa0d7"></a>
### Material Cost.set conversion factors

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_set_conversion_factors`

**Inputs** self.

**Local steps**

- Set rows from list of row for row drawn from self.design.items where row.item\_code.
  - Draw row from self.design.items, keep a combination only if (row.item\_code).
- Set uom\_factors from self.get\_uom\_factors(list of row.item\_code for row drawn from rows).
  - Draw row from rows.
- Set stock\_uoms from self.get\_stock\_uoms(list of row.item\_code for row drawn from rows).
  - Draw row from rows.
- For each row in rows.
  - Set row.stock\_uom from stock\_uoms.get(row.item\_code).
  - Set row.uom from (row.uom or row.stock\_uom).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.uom → row.stock\_uom.
  - Set row.conversion\_factor from 1.0 when row.uom equals row.stock\_uom, otherwise (flt(uom\_factors.get(tuple(row.item\_code, row.uom))) or flt(row.conversion\_factor) or 1.0).
    - Value choice on row.uom equals row.stock\_uom — true gives 1.0, false gives (flt(uom\_factors.get(tuple(row.item\_code, row.uom))) or flt(row.conversion\_factor) or 1.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(uom\_factors.get(tuple(row.item\_code, row.uom))) → flt(row.conversion\_factor) → 1.0.
  - Set row.stock\_qty from (flt(row.qty) × flt(row.conversion\_factor)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get uom factors](operations-011.md#op-0733f51e081b54), [get stock uoms](operations-011.md#op-803b62f40a1ac3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L744)

<a id="op-5840259e4557f1"></a>
### Material Cost.set part rates

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_set_part_rates`

**Inputs** self.

**Local steps**

- Set self.bom\_costs from self.get\_bom\_costs().
- Set children from defaultdict(list).
- For each row in self.design.items.
  - Set row.rate, row.amount from 0.
  - If (row.item\_code and not row.exclude\_from\_bom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.exclude\_from\_bom.
    - Evaluate children at (row.parent\_node\_id or 0).append(row).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.parent\_node\_id → 0.
- Set cost from self.get\_part\_cost(0, children, set()).
- Set self.design.raw\_material\_cost from (cost × (flt(self.design.qty) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.design.qty) → 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bom costs](operations-011.md#op-f35c7038c1f038), [get part cost](operations-011.md#op-31ae6316b22ffe).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L747)

<a id="op-31ae6316b22ffe"></a>
### Material Cost.get part cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_part_cost`

**Inputs** self, node\_id, children, visited.

**Declared result** float.

**Explicit results** cost.

**Local steps**

- Evaluate visited.add(node\_id).
- Set cost from 0.
- For each row in children.get(node\_id, list()).
  - If (children.get(row.node\_id) and row.node\_id does not belong to visited).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in children.get(row.node\_id) → row.node\_id does not belong to visited.
    - Set row.rate from (self.get\_part\_cost(row.node\_id, children, visited) × flt((row.conversion\_factor or 1))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.conversion\_factor → 1.
  - Otherwise.
    - If (row.bom\_no belongs to self.bom\_costs and not row.do\_not\_explode and not row.sourced\_by\_supplier).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.bom\_no belongs to self.bom\_costs → not row.do\_not\_explode → not row.sourced\_by\_supplier.
      - Set row.rate from ((self.bom\_costs at row.bom\_no × flt((row.conversion\_factor or 1))) ÷ flt((self.design.conversion\_rate or 1))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.conversion\_factor → 1.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.design.conversion\_rate → 1.
    - Otherwise.
      - Set row.rate from self.get\_rate(row.item\_code, row.qty, row.uom, row.stock\_uom, …).
  - Set row.amount from (flt(row.rate) × flt(row.qty)).
  - Set row.base\_rate from (flt(row.rate) × flt((self.design.conversion\_rate or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.design.conversion\_rate → 1.
  - Set row.base\_amount from (flt(row.amount) × flt((self.design.conversion\_rate or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.design.conversion\_rate → 1.
  - Update cost using + row.amount.
- Return cost.

**Methods declared on this owner** [get rate](operations-011.md#op-dafebebba9e6a4).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L739)

<a id="op-f35c7038c1f038"></a>
### Material Cost.get bom costs

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_bom_costs`

**Inputs** self.

**Declared result** dict at tuple(str, float).

**Record and data access** read “BOM” via get\_all.

**Explicit results** mapping() · mapping of bom.name → (flt(bom.base\_total\_cost) ÷ get\_good\_quantity(bom)) for bom drawn from boms.

**Local steps**

- Set bom\_nos from list(set of row.bom\_no for row drawn from self.design.items where (row.bom\_no and not row.do\_not\_explode)).
  - Draw row from self.design.items, keep a combination only if ((row.bom\_no and not row.do\_not\_explode)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.bom\_no → not row.do\_not\_explode.
- If not bom\_nos.
  - Return mapping().
- Set boms from Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“in”, bom\_nos)), fields = list(“name”, “base\_total\_cost”, “quantity”, “process\_loss\_qty”)).
- Return mapping of bom.name → (flt(bom.base\_total\_cost) ÷ get\_good\_quantity(bom)) for bom drawn from boms.
  - Draw bom from boms.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L247) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L736)

<a id="op-791cc51833e82b"></a>
### Material Cost.get operation plan cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_operation_plan_cost`

**Inputs** self.

**Declared result** float.

**Explicit results** (self.get\_material\_cost(0, materials, parts, set(0)) × (flt(self.design.qty) or 1)).

**Local steps**

- Set materials from defaultdict(list).
- For each row in self.design.materials.
  - Evaluate materials at cint(row.bom\_node\_id).append(row).
- Set parts from mapping of row.node\_id → row for row drawn from self.design.items.
  - Draw row from self.design.items.
- Set item\_codes from list of row.item\_code for row drawn from self.design.materials where row.item\_code.
  - Draw row from self.design.materials, keep a combination only if (row.item\_code).
- Set self.stock\_uoms from self.get\_stock\_uoms(item\_codes).
- Set self.uom\_factors from self.get\_uom\_factors(item\_codes).
- Return (self.get\_material\_cost(0, materials, parts, set(0)) × (flt(self.design.qty) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.design.qty) → 1.

**Methods declared on this owner** [get stock uoms](operations-011.md#op-803b62f40a1ac3), [get uom factors](operations-011.md#op-0733f51e081b54), [get material cost](operations-011.md#op-07b01e7b7f6846).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L249) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L738)

<a id="op-07b01e7b7f6846"></a>
### Material Cost.get material cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_material_cost`

**Inputs** self, node\_id, materials, parts, visited.

**Declared result** float.

**Explicit results** cost.

**Local steps**

- Set cost from 0.
- For each row in materials at node\_id.
  - Set node from cint(row.part\_node\_id).
  - If (row.from\_operation\_id or (node and not parts at node.item\_code)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.from\_operation\_id → (node and not parts at node.item\_code).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in node → not parts at node.item\_code.
    - Continue with the next iteration or loop test.
  - If (node and node belongs to materials and node does not belong to visited).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in node → node belongs to materials → node does not belong to visited.
    - Set rate from self.get\_material\_cost(node, materials, parts, (visited bitwise or set(node))).
  - Otherwise.
    - If node.
      - Set rate from flt(parts at node.rate).
    - Otherwise.
      - Set stock\_uom from self.stock\_uoms.get(row.item\_code).
      - Set factor from (flt(self.uom\_factors.get(tuple(row.item\_code, row.uom))) or 1).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.uom\_factors.get(tuple(row.item\_code, row.uom))) → 1.
      - Set rate from self.get\_rate(row.item\_code, row.qty, (row.uom or stock\_uom), stock\_uom, …).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.uom → stock\_uom.
  - Update cost using + (rate × flt(row.qty)).
- Return cost.

**Methods declared on this owner** [get rate](operations-011.md#op-dafebebba9e6a4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L248) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L737)

<a id="op-dafebebba9e6a4"></a>
### Material Cost.get rate

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_rate`

**Inputs** self, item\_code, qty, uom, stock\_uom, conversion\_factor, row = no value.

**Declared result** float.

**Explicit results** (flt(rate) ÷ flt((design.conversion\_rate or 1))).

**Local steps**

- Set design from self.design.
- Set rate from get\_bom\_item\_rate(mapping(“company” → design.company, “item\_code” → item\_code, “bom\_no” → empty text, “qty” → qty, …), design).
  - Value choice on row — true gives row.sourced\_by\_supplier, false gives 0.
- If design.rm\_cost\_as\_per equals “Price List”.
  - Set rate from (flt(rate) × flt((design.plc\_conversion\_rate or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in design.plc\_conversion\_rate → 1.
- Return (flt(rate) ÷ flt((design.conversion\_rate or 1))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in design.conversion\_rate → 1.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L740)

<a id="op-0733f51e081b54"></a>
### Material Cost.get uom factors

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_uom_factors`

**Inputs** self, item\_codes.

**Declared result** dict.

**Record and data access** read “UOM Conversion Detail” via get\_all.

**Explicit results** mapping() · mapping of tuple(row.parent, row.uom) → row.conversion\_factor for row drawn from Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, list(set(item\_codes))), “parenttype” → “I ….

**Local steps**

- If not item\_codes.
  - Return mapping().
- Return mapping of tuple(row.parent, row.uom) → row.conversion\_factor for row drawn from Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, list(set(item\_codes))), “parenttype” → “I ….
  - Draw row from Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, list(set(item\_codes))), “parenttype” → “Item”), fields = list(“parent”, “uom”, “conversion\_factor”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L742)

<a id="op-803b62f40a1ac3"></a>
### Material Cost.get stock uoms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_materialcost_get_stock_uoms`

**Inputs** self, item\_codes.

**Declared result** dict.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · dict(Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(set(item\_codes)))), fields = list(“name”, “stock\_uom”), as\_list = true)).

**Local steps**

- If not item\_codes.
  - Return mapping().
- Return dict(Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(set(item\_codes)))), fields = list(“name”, “stock\_uom”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L741)

<a id="op-3a15df1a6eef9e"></a>
### Get good quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_material_cost_get_good_quantity`

**Inputs** bom.

**Declared result** float.

**Explicit results** good\_quantity when good\_quantity &gt; 0, otherwise (flt(bom.quantity) or 1).

**Local steps**

- Set good\_quantity from (flt(bom.quantity) − flt(bom.process\_loss\_qty)).
- Return good\_quantity when good\_quantity &gt; 0, otherwise (flt(bom.quantity) or 1).
  - Value choice on good\_quantity &gt; 0 — true gives good\_quantity, false gives (flt(bom.quantity) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(bom.quantity) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L246) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L735)

<a id="op-6e4e8e6ed86447"></a>
### Operation Plan.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_init`

**Inputs** self, design.

**Local steps**

- Evaluate super().\_\_init\_\_(design).
- Set self.operations from defaultdict(list).
- Set self.materials from defaultdict(list).
- For each row in design.operations.
  - Evaluate self.operations at cint(row.bom\_node\_id).append(row).
- For each row in design.materials.
  - Evaluate self.materials at cint(row.bom\_node\_id).append(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L764)

<a id="op-9222cc429664a0"></a>
### Operation Plan.bom node ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_bom_node_ids`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at int.

**Explicit results** sorted(set(0, expanded self.operations, expanded self.materials)).

**Local steps**

- Return sorted(set(0, expanded self.operations, expanded self.materials)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L748)

<a id="op-606df85a1af8bc"></a>
### Operation Plan.get bom node ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_bom_node_ids`

**Inputs** self.

**Declared result** list at int.

**Explicit results** self.bom\_node\_ids.

**Local steps**

- Return self.bom\_node\_ids.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L750)

<a id="op-5ba6ed29a4c6a0"></a>
### Operation Plan.produces item at each operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_produces_item_at_each_operation`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** bool(self.design.track\_semi\_finished\_goods).

**Local steps**

- Return bool(self.design.track\_semi\_finished\_goods).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L766)

<a id="op-8cfe33e4b40838"></a>
### Operation Plan.validate

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_operation\_ids().
- For each row in self.design.operations.
  - Evaluate self.validate\_operation(row).
- For each row in self.design.materials.
  - Evaluate self.validate\_material(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set operation ids](operations-011.md#op-a09f884dcc7af5), [validate operation](operations-011.md#op-60e89bb38578d7), [validate material](operations-011.md#op-003019081a6d6e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L770)

<a id="op-a09f884dcc7af5"></a>
### Operation Plan.set operation ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_set_operation_ids`

**Inputs** self.

**Local steps**

- Set last\_id from max(generator of cint(row.operation\_id) for row drawn from self.design.operations, default = 0).
  - Draw row from self.design.operations.
- For each row in self.design.operations.
  - If not row.operation\_id.
    - Update last\_id using + 1.
    - Set row.operation\_id from last\_id.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L769)

<a id="op-60e89bb38578d7"></a>
### Operation Plan.validate operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_validate_operation`

**Inputs** self, row.

**Local steps**

- Evaluate self.validate\_node(row.bom\_node\_id, translated “Operations row #{0}”.format(row.idx)).
- Evaluate self.validate\_node(row.output\_node\_id, translated “Operations row #{0}”.format(row.idx)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate node](operations-012.md#op-b266bc3436f487).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L773)

<a id="op-003019081a6d6e"></a>
### Operation Plan.validate material

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_validate_material`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “{0}: choose one design part, one item or one earlier operation output.”.format(label) · validation helper — translated “{0}: the operation is not part of this BOM.”.format(label).

**Local steps**

- Set label from translated “Materials row #{0}”.format(row.idx).
- Set sources from list(row.part\_node\_id, row.item\_code, row.from\_operation\_id).
- If len(list of source for source drawn from sources where source) differs from 1.
  - Draw source from sources, keep a combination only if (source).
  - Call the validation error handler Platform.throw(translated “{0}: choose one design part, one item or one earlier operation output.”.format(label)).
- Evaluate self.validate\_node(row.bom\_node\_id, label).
- Evaluate self.validate\_node(row.part\_node\_id, label).
- Set operation\_ids from list of cint(operation.operation\_id) for operation drawn from self.operations at cint(row.bom\_node\_id).
  - Draw operation from self.operations at cint(row.bom\_node\_id).
- If (row.operation\_id and cint(row.operation\_id) does not belong to operation\_ids).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.operation\_id → cint(row.operation\_id) does not belong to operation\_ids.
  - Call the validation error handler Platform.throw(translated “{0}: the operation is not part of this BOM.”.format(label)).
- If row.from\_operation\_id.
  - Evaluate self.validate\_previous\_output(row, operation\_ids, label).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate node](operations-012.md#op-b266bc3436f487), [validate previous output](operations-012.md#op-792e713c5be460).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L771)
