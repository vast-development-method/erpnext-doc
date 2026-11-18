# Production · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom creator

<a id="op-7585058d428285"></a>
### BOMPlan.get bom quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_bom_quantity`

**Inputs** self, node\_id.

**Declared result** float.

**Explicit results** 1 when node\_id, otherwise (flt(self.design.qty) or 1).

**Local steps**

- Return 1 when node\_id, otherwise (flt(self.design.qty) or 1).
  - Value choice on node\_id — true gives 1, false gives (flt(self.design.qty) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.design.qty) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L220) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L709)

<a id="op-6f7482742ed679"></a>
### BOMPlan.get bom node ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_bom_node_ids`

**Inputs** self.

**Declared result** list at int.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L218) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L707)

<a id="op-a63c02a32a3e86"></a>
### BOMPlan.get problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_problems`

**Inputs** self.

**Declared result** list at str.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L223) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L712)

<a id="op-5b9d0dafe4fe5d"></a>
### BOMPlan.get bom order

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_bom_order`

**Inputs** self.

**Declared result** list at int.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L219) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L708)

<a id="op-a3abd79e0a941c"></a>
### BOMPlan.make bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_make_bom`

**Inputs** self, node\_id, boms.

**Declared result** str.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L226) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L715)

<a id="op-01f43184cf831c"></a>
### BOMPlan.validate can make boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_validate_can_make_boms`

**Inputs** self.

**Explicit failure paths** validation helper — problems.

**Local steps**

- Set problems from self.get\_problems().
- If problems.
  - Call the validation error handler Platform.throw(problems, title = translated “Fix These Before Creating BOMs”, as\_list = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get problems](operations-010.md#op-a63c02a32a3e86).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L230) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L719)

<a id="op-0b8959caf5067b"></a>
### BOMPlan.make boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_make_boms`

**Inputs** self.

**Declared result** dict at tuple(str, str).

**Explicit results** boms.

**Local steps**

- Evaluate self.validate\_can\_make\_boms().
- Set boms from self.get\_existing\_boms().
- For each node\_id in self.get\_bom\_order().
  - Set item\_code from self.get\_node\_item(node\_id).
  - If item\_code does not belong to boms.
    - Set boms at item\_code from self.make\_bom(node\_id, boms).
- Return boms.

**Methods declared on this owner** [validate can make boms](operations-010.md#op-01f43184cf831c), [get existing boms](operations-010.md#op-06a6f1c89e52df), [get bom order](operations-010.md#op-5b9d0dafe4fe5d), [get node item](operations-009.md#op-40ce466de7f081), [make bom](operations-010.md#op-a3abd79e0a941c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L227) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L716)

<a id="op-06a6f1c89e52df"></a>
### BOMPlan.get existing boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_existing_boms`

**Inputs** self.

**Declared result** dict at tuple(str, str).

**Record and data access** read “BOM” via get\_all.

**Explicit results** mapping() · dict(Platform.get\_all(“BOM”, filters = mapping(“bom\_creator” → self.design.name, “docstatus” → 1), fields = list(“item”, “name”), order\_by = “creation”, as\_list = true)).

**Local steps**

- If self.design.is\_new().
  - Return mapping().
- Return dict(Platform.get\_all(“BOM”, filters = mapping(“bom\_creator” → self.design.name, “docstatus” → 1), fields = list(“item”, “name”), order\_by = “creation”, as\_list = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L221) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L710)

<a id="op-99b66e894c7beb"></a>
### BOMPlan.has all boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_has_all_boms`

**Inputs** self.

**Declared result** bool.

**Explicit results** (all(items) and items ≤ set(self.get\_existing\_boms())).

**Local steps**

- Set items from set of self.get\_node\_item(node\_id) for node\_id drawn from self.get\_bom\_node\_ids().
  - Draw node\_id from self.get\_bom\_node\_ids().
- Return (all(items) and items ≤ set(self.get\_existing\_boms())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in all(items) → items ≤ set(self.get\_existing\_boms()).

**Methods declared on this owner** [get node item](operations-009.md#op-40ce466de7f081), [get bom node ids](operations-010.md#op-6f7482742ed679), [get existing boms](operations-010.md#op-06a6f1c89e52df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L224) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L713)

<a id="op-7a19c5869d4dd6"></a>
### BOMPlan.new bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_new_bom`

**Inputs** self, node\_id.

**State and service calls** request new\_doc for “BOM”.

**Explicit results** bom.

**Local steps**

- Set part from self.parts.get(node\_id).
- Set bom from Platform.new\_doc(“BOM”).
- Evaluate bom.update(mapping(“item” → self.get\_node\_item(node\_id), “quantity” → self.get\_bom\_quantity(node\_id), “bom\_type” → “Production”, “allow\_alternative\_item” → 1, …)).
  - Value choice on part — true gives part.name, false gives empty text.
  - Value choice on part — true gives part.is\_phantom\_item, false gives self.design.is\_phantom.
- For each field in BOM\_FIELDS.
  - If self.design.get(field).
    - Evaluate bom.set(field, self.design.get(field)).
- If self.design.default\_warehouse.
  - Set bom.default\_source\_warehouse from self.design.default\_warehouse.
- Return bom.

**Methods declared on this owner** [get node item](operations-009.md#op-40ce466de7f081), [get bom quantity](operations-010.md#op-7585058d428285).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L228) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L717)

<a id="op-c43dc791483da8"></a>
### BOMPlan.get bom item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_bom_item`

**Inputs** self, item\_code, qty, uom, boms, part = no value.

**Declared result** dict.

**Explicit results** bom\_item.

**Local steps**

- Set bom\_item from mapping(“item\_code” → item\_code, “qty” → qty, “uom” → uom, “allow\_alternative\_item” → 1, …).
- If item\_code belongs to boms.
  - Evaluate bom\_item.update(mapping(“bom\_no” → boms at item\_code, “do\_not\_explode” → 0)).
- Otherwise.
  - If part.
    - Evaluate bom\_item.update(mapping(“do\_not\_explode” → part.do\_not\_explode, “bom\_no” → empty text when part.do\_not\_explode, otherwise part.bom\_no)).
      - Value choice on part.do\_not\_explode — true gives empty text, false gives part.bom\_no.
- If part.
  - Evaluate bom\_item.update(mapping(“is\_phantom\_item” → part.is\_phantom\_item when item\_code belongs to boms, otherwise 0, “sourced\_by\_supplier” → part.sourced\_by\_supplier, “conversion\_factor” → part.conversion\_factor  ….
    - Value choice on item\_code belongs to boms — true gives part.is\_phantom\_item, false gives 0.
    - Value choice on uom equals part.uom — true gives part.conversion\_factor, false gives 0.
- Return bom\_item.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L706)

<a id="op-c6ce39c3704fd1"></a>
### BOMPlan.submit bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_submit_bom`

**Inputs** self, bom.

**Declared result** str.

**State and service calls** call insert on bom · call submit on bom.

**Explicit results** bom.name.

**Local steps**

- Set bom.flags.ignore\_permissions from true.
- Evaluate bom.insert().
- Evaluate bom.submit().
- Return bom.name.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L229) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L718)

<a id="op-431e889db9f3e2"></a>
### Item Matcher.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_init`

**Inputs** self, parts.

**Local steps**

- Set self.parts from list of part for part drawn from parts where (part.part\_number or part.part\_name).
  - Draw part from parts, keep a combination only if ((part.part\_number or part.part\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part.part\_number → part.part\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L244) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L733)

<a id="op-d67b37115e387f"></a>
### Item Matcher.get matches

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_matches`

**Inputs** self.

**Declared result** dict at tuple(str, dict).

**Explicit results** mapping() · mapping of part.name → matches at get\_part\_key(part) for part drawn from self.parts where matches at get\_part\_key(part).

**Local steps**

- If not self.parts.
  - Return mapping().
- Evaluate self.set\_items().
- Set earlier\_items from self.get\_earlier\_items().
- Set parts from mapping of get\_part\_key(part) → part for part drawn from self.parts.
  - Draw part from self.parts.
- Set known from mapping of key → self.get\_known\_match(part, earlier\_items) for tuple(key, part) drawn from parts.items().
  - Draw tuple(key, part) from parts.items().
- Set candidates from mapping of key → self.get\_candidates(part) for tuple(key, part) drawn from parts.items() where not known at key.
  - Draw tuple(key, part) from parts.items(), keep a combination only if (not known at key).
- Set self.descriptions from self.get\_descriptions(candidates).
- Set matches from mapping of key → (known at key or self.get\_best\_match(part, candidates at key)) for tuple(key, part) drawn from parts.items().
  - Draw tuple(key, part) from parts.items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in known at key → self.get\_best\_match(part, candidates at key).
- Return mapping of part.name → matches at get\_part\_key(part) for part drawn from self.parts where matches at get\_part\_key(part).
  - Draw part from self.parts, keep a combination only if (matches at get\_part\_key(part)).

**Methods declared on this owner** [set items](operations-010.md#op-1b7630d6385075), [get earlier items](operations-010.md#op-d7e5728ff4b225), [get known match](operations-010.md#op-d2dc2b68b2d7a2), [get candidates](operations-010.md#op-9e34a208ae9924), [get descriptions](operations-010.md#op-9212308888d945), [get best match](operations-010.md#op-d140cc11955ad3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L243) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L732)

<a id="op-1b7630d6385075"></a>
### Item Matcher.set items

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_set_items`

**Inputs** self.

**Record and data access** read “Item” via get\_list.

**Local steps**

- Set items from Platform.get\_list(“Item”, filters = mapping(“disabled” → 0, “has\_variants” → 0), fields = list(“name”, “item\_name”), limit\_page\_length = 0).
- Set self.item\_codes from set of item.name for item drawn from items.
  - Draw item from items.
- Set self.items\_by\_code\_key from defaultdict(list).
- For each item in items.
  - Evaluate self.items\_by\_code\_key at get\_code\_key(item.name).append(item.name).
- Set self.codes from tuple(list of item.name for item drawn from items, list of get\_code\_key(item.name) for item drawn from items).
  - Draw item from items.
  - Draw item from items.
- Set named\_items from list of item for item drawn from items where item.item\_name.
  - Draw item from items, keep a combination only if (item.item\_name).
- Set self.names from tuple(list of item.name for item drawn from named\_items, list of get\_name\_key(item.item\_name) for item drawn from named\_items).
  - Draw item from named\_items.
  - Draw item from named\_items.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L245) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L734)

<a id="op-d7e5728ff4b225"></a>
### Item Matcher.get earlier items

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_earlier_items`

**Inputs** self.

**Declared result** dict at tuple(str, str).

**Record and data access** read “BOM Creator” via get\_list.

**Explicit results** mapping() · mapping of row.part\_number → row.item\_code for row drawn from rows where row.item\_code belongs to self.item\_codes.

**Local steps**

- Set part\_numbers from list of row.part\_number for row drawn from self.parts where row.part\_number.
  - Draw row from self.parts, keep a combination only if (row.part\_number).
- If not part\_numbers.
  - Return mapping().
- Set rows from Platform.get\_list(“BOM Creator”, filters = list(list(“BOM Creator”, “docstatus”, “&lt;”, 2), list(“BOM Creator Item”, “part\_number”, “in”, part\_numbers), list(“BOM Creator Item”, “item\_code”, “is”, “set”)), f ….
- Return mapping of row.part\_number → row.item\_code for row drawn from rows where row.item\_code belongs to self.item\_codes.
  - Draw row from rows, keep a combination only if (row.item\_code belongs to self.item\_codes).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L241) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L730)

<a id="op-d2dc2b68b2d7a2"></a>
### Item Matcher.get known match

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_known_match`

**Inputs** self, part, earlier\_items.

**Declared result** (dict bitwise or no value).

**Explicit results** get\_match(earlier\_items at part.part\_number, 100, “Earlier Design”, true) · get\_match(part.part\_number, 100, “Item Code”, true) · get\_match(same\_code at 0, 100, “Item Code”, true).

**Local steps**

- If part.part\_number belongs to earlier\_items.
  - Return get\_match(earlier\_items at part.part\_number, 100, “Earlier Design”, true).
- If part.part\_number belongs to self.item\_codes.
  - Return get\_match(part.part\_number, 100, “Item Code”, true).
- Set same\_code from self.items\_by\_code\_key.get(get\_code\_key(part.part\_number), list()).
- If len(same\_code) equals 1.
  - Return get\_match(same\_code at 0, 100, “Item Code”, true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L242) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L731)

<a id="op-9e34a208ae9924"></a>
### Item Matcher.get candidates

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_candidates`

**Inputs** self, part.

**Declared result** dict at tuple(str, tuple at tuple(float, str)).

**Explicit results** candidates.

**Local steps**

- Set candidates from mapping().
- Set code\_key from get\_code\_key(part.part\_number).
- For each tuple(item\_code, score) in self.get\_closest(code\_key, self.codes, fuzz.ratio).
  - Set candidates at item\_code from tuple(score, “Item Code”).
- Set name\_key from get\_name\_key(part.part\_name).
- For each tuple(item\_code, score) in self.get\_closest(name\_key, self.names, fuzz.ratio).
  - If score &gt; candidates.get(item\_code, tuple(0)) at 0.
    - Set candidates at item\_code from tuple(score, “Item Name”).
- Return candidates.

**Methods declared on this owner** [get closest](operations-010.md#op-858dfbc3471dac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L237) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L726)

<a id="op-858dfbc3471dac"></a>
### Item Matcher.get closest

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_closest`

**Inputs** self, query, choices, scorer.

**Declared result** list at tuple at tuple(str, float).

**Explicit results** list() · list of tuple(item\_codes at index, score when get\_numbers(key) equals numbers, otherwise min(score, (HIGH\_SCORE − 1))) for tuple(key, score, index) drawn from results.

**Local steps**

- If not query.
  - Return list().
- Set tuple(item\_codes, keys) from choices.
- Set results from process.extract(query, keys, scorer = scorer, limit = CANDIDATE\_LIMIT, score\_cutoff = CANDIDATE\_SCORE).
- Set numbers from get\_numbers(query).
- Return list of tuple(item\_codes at index, score when get\_numbers(key) equals numbers, otherwise min(score, (HIGH\_SCORE − 1))) for tuple(key, score, index) drawn from results.
  - Draw tuple(key, score, index) from results.
  - Value choice on get\_numbers(key) equals numbers — true gives score, false gives min(score, (HIGH\_SCORE − 1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L238) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L727)

<a id="op-9212308888d945"></a>
### Item Matcher.get descriptions

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_descriptions`

**Inputs** self, candidates.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · mapping of item.name → strip\_html((item.description or empty text)) for item drawn from items.

**Local steps**

- Set item\_codes from list(set of item\_code for rows drawn from candidates.values(), then item\_code drawn from rows).
  - Draw rows from candidates.values().
  - Draw item\_code from rows.
- If not item\_codes.
  - Return mapping().
- Set items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, item\_codes)), fields = list(“name”, “description”)).
- Return mapping of item.name → strip\_html((item.description or empty text)) for item drawn from items.
  - Draw item from items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.description → empty text.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L240) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L729)

<a id="op-d140cc11955ad3"></a>
### Item Matcher.get best match

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_best_match`

**Inputs** self, part, candidates.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · get\_match(item\_code, score, matched\_on, (score ≥ HIGH\_SCORE and is\_unique)).

**Local steps**

- Set part\_text from one space.join(filter(no value, list(part.part\_name, strip\_html((part.description or empty text))))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part.description → empty text.
- Set scores from list().
- For each tuple(item\_code, tuple(score, matched\_on)) in candidates.items().
  - Set description\_score from self.get\_description\_score(part\_text, item\_code).
  - If description\_score &gt; score.
    - Set tuple(score, matched\_on) from tuple(description\_score, “Description”).
  - Evaluate scores.append(tuple(score, item\_code, matched\_on)).
- Evaluate scores.sort(reverse = true).
- If (not scores or scores at 0 at 0 &lt; MIN\_SCORE).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not scores → scores at 0 at 0 &lt; MIN\_SCORE.
  - Return no value.
- Set tuple(score, item\_code, matched\_on) from scores at 0.
- Set is\_unique from (len(scores) equals 1 or scores at 1 at 0 &lt; score).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(scores) equals 1 → scores at 1 at 0 &lt; score.
- Return get\_match(item\_code, score, matched\_on, (score ≥ HIGH\_SCORE and is\_unique)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in score ≥ HIGH\_SCORE → is\_unique.

**Methods declared on this owner** [get description score](operations-010.md#op-4c5287a026ab99).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L236) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L725)

<a id="op-4c5287a026ab99"></a>
### Item Matcher.get description score

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_itemmatcher_get_description_score`

**Inputs** self, part\_text, item\_code.

**Declared result** float.

**Explicit results** 0 · min(score, (HIGH\_SCORE − 1)).

**Local steps**

- Set description from self.descriptions.get(item\_code).
- If (not part\_text or not description).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not part\_text → not description.
  - Return 0.
- Set score from fuzz.token\_set\_ratio(part\_text, description, processor = default\_process).
- Return min(score, (HIGH\_SCORE − 1)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L239) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L728)

<a id="op-d110d6b9948d99"></a>
### Get match

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_get_match`

**Inputs** item\_code, score, matched\_on, is\_selected.

**Declared result** dict.

**Explicit results** mapping(“item\_code” → item\_code, “score” → round(score), “matched\_on” → matched\_on, “is\_selected” → is\_selected).

**Local steps**

- Return mapping(“item\_code” → item\_code, “score” → round(score), “matched\_on” → matched\_on, “is\_selected” → is\_selected).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L232) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L721)

<a id="op-05e848a79f1aa3"></a>
### Get part key

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_item_matcher_get_part_key`

**Inputs** part.

**Declared result** tuple.

**Explicit results** tuple(part.part\_number, part.part\_name, part.description).

**Local steps**

- Return tuple(part.part\_number, part.part\_name, part.description).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L235) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L724)
