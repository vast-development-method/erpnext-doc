# Production · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom

<a id="op-6c3ba70ff05e0c"></a>
### BOM.validate semi finished goods

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_semi_finished_goods`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — problems.

**Local steps**

- If (not self.track\_semi\_finished\_goods or not self.operations).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.track\_semi\_finished\_goods → not self.operations.
  - Return no value.
- Set problems from (self.get\_output\_item\_problems() + self.get\_last\_step\_problems()).
- If self.docstatus equals 1.
  - Evaluate problems.extend(self.get\_raw\_material\_problems()).
- If problems.
  - Call the validation error handler Platform.throw(problems, title = translated “Fix These Steps”, as\_list = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get output item problems](operations-003.md#op-b949a960b334f3), [get last step problems](operations-003.md#op-cf6e53a1a5459b), [get raw material problems](operations-003.md#op-54ad0c5df89a94).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L215)

<a id="op-02704e761b74df"></a>
### BOM.get step label

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_get_step_label`

**Inputs** self, row.

**Explicit results** translated “Step {0} ({1})”.format(row.idx, bold(row.operation)).

**Local steps**

- Return translated “Step {0} ({1})”.format(row.idx, bold(row.operation)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L631)

<a id="op-b949a960b334f3"></a>
### BOM.get output item problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_get_output_item_problems`

**Inputs** self.

**Explicit results** problems.

**Local steps**

- Set problems from list().
- For each row in self.operations.
  - If not row.finished\_good.
    - Evaluate problems.append(translated “{0}: choose the Output Item, that is the item this step makes.”.format(self.get\_step\_label(row))).
  - Otherwise.
    - If (row.is\_final\_finished\_good and row.finished\_good differs from self.item).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_final\_finished\_good → row.finished\_good differs from self.item.
      - Evaluate problems.append(translated “{0}: this is the Last Step, so its Output Item must be {1}.”.format(self.get\_step\_label(row), bold(self.item))).
- Return problems.

**Methods declared on this owner** [get step label](operations-003.md#op-02704e761b74df).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L629)

<a id="op-cf6e53a1a5459b"></a>
### BOM.get last step problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_get_last_step_problems`

**Inputs** self.

**Explicit results** list(translated “Tick Last Step on the step that makes {0}. Its Output Item must be {0}.”.format(bold(self.item))) · list(translated “Only one step can be the Last Step, but it is ticked on steps {0}.”.format(“, ”.join(generator of str(row.idx) for row drawn from last\_steps))) · list().

**Local steps**

- Set last\_steps from list of row for row drawn from self.operations where row.is\_final\_finished\_good.
  - Draw row from self.operations, keep a combination only if (row.is\_final\_finished\_good).
- If not last\_steps.
  - Return list(translated “Tick Last Step on the step that makes {0}. Its Output Item must be {0}.”.format(bold(self.item))).
- If len(last\_steps) &gt; 1.
  - Return list(translated “Only one step can be the Last Step, but it is ticked on steps {0}.”.format(“, ”.join(generator of str(row.idx) for row drawn from last\_steps))).
    - Draw row from last\_steps.
- Return list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L628)

<a id="op-54ad0c5df89a94"></a>
### BOM.get raw material problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_get_raw_material_problems`

**Inputs** self.

**Explicit results** list of translated “{0} has no raw materials. Click Add Raw Materials for this step in the Steps section, or select a BOM for it …”.format(self.get\_step\_label(row), bold(row.finished\_good)) for row drawn f ….

**Local steps**

- Set steps\_with\_materials from set of cint(row.operation\_row\_id) for row drawn from self.items where row.operation\_row\_id.
  - Draw row from self.items, keep a combination only if (row.operation\_row\_id).
- Return list of translated “{0} has no raw materials. Click Add Raw Materials for this step in the Steps section, or select a BOM for it …”.format(self.get\_step\_label(row), bold(row.finished\_good)) for row drawn f ….
  - Draw row from self.operations, keep a combination only if ((row.finished\_good and not row.bom\_no and row.idx does not belong to steps\_with\_materials)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.finished\_good → not row.bom\_no → row.idx does not belong to steps\_with\_materials.

**Methods declared on this owner** [get step label](operations-003.md#op-02704e761b74df).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L630)

<a id="op-80bbb333d79e64"></a>
### BOM.validate secondary items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_secondary_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is already added with the same Type in the Secondary Items table.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Finished Good Item {1} cannot be added in the Secondary Items table.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Process Loss Percentage should be less than 100% for {1} Item {2}”.format(item.idx, item.secondary\_item\_type, get\_link\_to\_form(“Item”, item.item\_code)).

**Local steps**

- Set seen\_items from set().
- For each item in self.secondary\_items.
  - Set key from tuple(item.item\_code, (item.secondary\_item\_type or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → empty text.
  - If key belongs to seen\_items.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is already added with the same Type in the Secondary Items table.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - Evaluate seen\_items.add(key).
  - If (item.valuation\_type differs from “Valuation Rate” and item.item\_code equals self.item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.valuation\_type differs from “Valuation Rate” → item.item\_code equals self.item.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item {1} cannot be added in the Secondary Items table.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - If item.process\_loss\_per ≥ 100.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Process Loss Percentage should be less than 100% for {1} Item {2}”.format(item.idx, item.secondary\_item\_type, get\_link\_to\_form(“Item”, item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L1066) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L213)

<a id="op-589792c31133c7"></a>
### BOM.set default uom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_default_unit_of_measure`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value.

**Local steps**

- If not self.get(“items”).
  - Return no value.
- Set item\_wise\_uom from Platform.\_dict(Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list of item.item\_code for item drawn from self.items)), fields = list(“name”, “stock\_uom”), as\_list = 1)).
  - Draw item from self.items.
- For each row in self.get(“items”).
  - If row.stock\_uom differs from item\_wise\_uom.get(row.item\_code).
    - Set row.stock\_uom from item\_wise\_uom.get(row.item\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L1920) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L184)

<a id="op-74cff2bc689500"></a>
### BOM.get context

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_context`

**Inputs** self, context.

**Local steps**

- Set context.parents from list(mapping(“name” → “boms”, “title” → translated “All BOMs”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L2261) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L164)

<a id="op-9639f288da056c"></a>
### BOM.on update

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache().hdel(“bom\_children”, self.name).
- Evaluate self.check\_recursion().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check recursion](operations-004.md#op-fe77e8cf67c8fa).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L2368) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L179)

<a id="op-0405d7ca00cece"></a>
### BOM.on submit

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.manage\_default\_bom().
- Evaluate self.update\_bom\_creator\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [manage default bom](operations-004.md#op-5718f55d3fd761), [update bom creator status](operations-003.md#op-b727f598a6adbf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L2464) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L178)

<a id="op-bf396c5bb068fa"></a>
### BOM.on cancel

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“is\_active”, 0).
- Evaluate self.db\_set(“is\_default”, 0).
- Evaluate self.validate\_bom\_links().
- Evaluate self.manage\_default\_bom().
- Evaluate self.update\_bom\_creator\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate bom links](operations-005.md#op-e4c2d3edc4d5b0), [manage default bom](operations-004.md#op-5718f55d3fd761), [update bom creator status](operations-003.md#op-b727f598a6adbf).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L2535) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L177)

<a id="op-b727f598a6adbf"></a>
### BOM.update bom creator status

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_update_bill_of_materials_creator_status`

**Inputs** self.

**Record and data access** resolve a document from “BOM Creator” via get\_doc.

**State and service calls** request set\_value on “BOM Creator Item”.

**Explicit results** no value.

**Local steps**

- If not self.bom\_creator.
  - Return no value.
- If self.bom\_creator\_item.
  - Evaluate Platform.db.set\_value(“BOM Creator Item”, self.bom\_creator\_item, “bom\_created”, 1 when self.docstatus equals 1, otherwise 0, update\_modified = false).
    - Value choice on self.docstatus equals 1 — true gives 1, false gives 0.
- Set doc from Platform.get\_doc(“BOM Creator”, self.bom\_creator).
- Evaluate doc.set\_status(save = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L2690) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L200)

<a id="op-d2cebb9f5f10a9"></a>
### BOM.set fg cost allocation

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_finished_goods_cost_allocation`

**Inputs** self.

**Local steps**

- Set self.cost\_allocation\_per from flt(self.cost\_allocation\_per).
- Set total\_secondary\_items\_per from 0.
- Set own\_cost from 0.
- For each item in self.secondary\_items.
  - If item.valuation\_type belongs to tuple(“Valuation Rate”, “Manual”).
    - Set item.cost\_allocation\_per from 0.
    - Update own\_cost using + flt(item.cost).
  - Update total\_secondary\_items\_per using + flt(item.cost\_allocation\_per).
- Set self.cost\_allocation\_per from flt((100 − total\_secondary\_items\_per), self.precision(“cost\_allocation\_per”)).
- Set self.cost\_allocation from flt((((self.raw\_material\_cost − own\_cost) × self.cost\_allocation\_per) ÷ 100), self.precision(“cost\_allocation”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L185)

<a id="op-91cb228da29792"></a>
### BOM.validate secondary items cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_secondary_items_cost`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The cost of the secondary items cannot exceed the raw material cost of {0}.”.format(Platform.bold(flt(self.raw\_material\_cost))).

**Local steps**

- If flt(self.secondary\_items\_cost) &gt; flt(self.raw\_material\_cost).
  - Call the validation error handler Platform.throw(translated “The cost of the secondary items cannot exceed the raw material cost of {0}.”.format(Platform.bold(flt(self.raw\_material\_cost)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L3224) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L214)

<a id="op-4f7b7f02407b31"></a>
### BOM.validate total cost allocation

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_total_cost_allocation`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cost allocation between finished goods and secondary items should equal 100%”.

**Local steps**

- Set total\_cost\_allocation\_per from flt(self.cost\_allocation\_per).
- For each item in self.secondary\_items.
  - Update total\_cost\_allocation\_per using + flt(item.cost\_allocation\_per).
- If flt(total\_cost\_allocation\_per, self.precision(“cost\_allocation\_per”)) differs from 100.
  - Call the validation error handler Platform.throw(translated “Cost allocation between finished goods and secondary items should equal 100%”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L216)

<a id="op-abe8d58252a8fb"></a>
### BOM.on update after submit

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_bom\_links().
- Evaluate self.manage\_default\_bom().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate bom links](operations-005.md#op-e4c2d3edc4d5b0), [manage default bom](operations-004.md#op-5718f55d3fd761).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L3541) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L180)

<a id="op-66c87353b2ffd8"></a>
### BOM.get item det

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_item_det`

**Inputs** self, item\_code.

**Explicit results** item.

**Explicit failure paths** validation helper — translated “Item: {0} does not exist in the system”.format(item\_code).

**Local steps**

- Set item from \_get\_item\_details(item\_code).
- If not item.
  - Call the validation error handler Platform.throw(translated “Item: {0} does not exist in the system”.format(item\_code)).
- Return item.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L168)

<a id="op-b29febb882e16d"></a>
### BOM.get routing

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_routing`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If self.routing.
  - Evaluate Platform.has\_permission(“Routing”, “read”, self.routing, throw = true).
- Evaluate self.set\_operations\_from\_routing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set operations from routing](operations-003.md#op-6f80f3b70cd39f).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Routing”, “read”, self.routing, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L172)

<a id="op-6f80f3b70cd39f"></a>
### BOM.set operations from routing

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_set_operations_from_routing`

**Inputs** self.

**Record and data access** read “BOM Operation” via get\_all.

**Local steps**

- If self.routing.
  - Evaluate self.set(“operations”, list()).
  - Set fields from list(“sequence\_id”, “operation”, “workstation”, “workstation\_type”, …).
  - For each row in Platform.get\_all(“BOM Operation”, fields = fields, filters = mapping(“parenttype” → “Routing”, “parent” → self.routing), order\_by = “sequence\_id, idx”).
    - Set child from self.append(“operations”, row).
    - Set child.hour\_rate from flt((row.hour\_rate ÷ self.conversion\_rate), child.precision(“hour\_rate”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L637)

<a id="op-d76d1cc2bd2e28"></a>
### BOM.set bom material details

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_bill_of_materials_material_details`

**Inputs** self.

**Local steps**

- For each item in self.get(“items”).
  - Evaluate self.validate\_bom\_currency(item).
  - If item.do\_not\_explode.
    - Set item.bom\_no from empty text.
  - Set ret from self.get\_bom\_material\_detail(mapping(“company” → self.company, “item\_code” → item.item\_code, “item\_name” → item.item\_name, “bom\_no” → item.bom\_no, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.source\_warehouse → self.default\_source\_warehouse.
  - For each r in ret.
    - If not item.get(r).
      - Evaluate item.set(r, ret at r).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate bom currency](operations-003.md#op-ae27d2018fee2a), [get bom material detail](operations-003.md#op-db1808b79a8110).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L4232) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L182)

<a id="op-bccb041dd8f211"></a>
### BOM.set secondary items details

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_secondary_items_details`

**Inputs** self.

**Local steps**

- For each item in self.get(“secondary\_items”).
  - Set args from mapping(“item\_code” → item.item\_code, “company” → self.company, “uom” → item.uom, “fetch\_rate” → false).
  - Set ret from self.get\_bom\_material\_detail(args).
  - For each tuple(key, value) in ret.items().
    - If item.get(key) is identical to no value.
      - Evaluate item.set(key, value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bom material detail](operations-003.md#op-db1808b79a8110).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0455.json#L4758) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L192)

<a id="op-db1808b79a8110"></a>
### BOM.get bom material detail

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_bill_of_materials_material_detail`

**Inputs** self, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “BOM” via get\_value.

**Explicit results** ret\_item.

**Local steps**

- If not args.
  - Set args from Platform.form\_dict.get(“args”).
- If isinstance(args, str).
  - Bind dependencies json.
  - Set args from json.loads(args).
- Set item from self.get\_item\_det(args at “item\_code”).
- Set args at “bom\_no” from (args.get(“bom\_no”) or (item and cstr(item at “default\_bom”)) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“bom\_no”) → (item and cstr(item at “default\_bom”)) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → cstr(item at “default\_bom”).
- Set args at “transfer\_for\_manufacture” from (cstr(args.get(“include\_item\_in\_manufacturing”, empty text)) or (item and item.include\_item\_in\_manufacturing) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(args.get(“include\_item\_in\_manufacturing”, empty text)) → (item and item.include\_item\_in\_manufacturing) → 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item.include\_item\_in\_manufacturing.
- Evaluate args.update(item).
- Set rate from self.get\_rm\_rate(args) when args.get(“fetch\_rate”), otherwise 0.
  - Value choice on args.get(“fetch\_rate”) — true gives self.get\_rm\_rate(args), false gives 0.
- Set ret\_item from mapping(“item\_name” → ((item and args at “item\_name”) or empty text), “description” → ((item and args at “description”) or empty text), “image” → ((item and args at “image”) or empty text), “stock\_uom” → ( ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and args at “item\_name”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → args at “item\_name”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and args at “description”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → args at “description”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and args at “image”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → args at “image”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and args at “stock\_uom”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → args at “stock\_uom”.
  - Value choice on args.get(“uom”) — true gives args at “uom”, false gives ((item and args at “stock\_uom”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item and args at “stock\_uom”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → args at “stock\_uom”.
  - Value choice on args.get(“conversion\_factor”) — true gives args at “conversion\_factor”, false gives 1.
  - Value choice on args at “bom\_no” — true gives Platform.get\_value(“BOM”, args at “bom\_no”, “is\_phantom\_bom”), false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“qty”) → args.get(“stock\_qty”) → 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“stock\_qty”) → args.get(“qty”) → 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.conversion\_rate) → 1.
- If ret\_item at “is\_phantom\_item”.
  - Set ret\_item at “do\_not\_explode” from 0.
- If args.get(“do\_not\_explode”).
  - Set ret\_item at “bom\_no” from empty text.
- Return ret\_item.

**Methods declared on this owner** [get item det](operations-003.md#op-66c87353b2ffd8), [get rm rate](operations-003.md#op-dd866eb6dfadc9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L161)

<a id="op-ae27d2018fee2a"></a>
### BOM.validate bom currency

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_bill_of_materials_currency`

**Inputs** self, item.

**Record and data access** read “BOM” via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Currency of the BOM #{1} should be equal to the selected currency {2}”.format(item.idx, item.bom\_no, self.currency).

**Local steps**

- If (item.get(“bom\_no”) and Platform.db.get\_value(“BOM”, item.get(“bom\_no”), “currency”) differs from self.currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“bom\_no”) → Platform.db.get\_value(“BOM”, item.get(“bom\_no”), “currency”) differs from self.currency.
  - Call the validation error handler Platform.throw(translated “Row {0}: Currency of the BOM #{1} should be equal to the selected currency {2}”.format(item.idx, item.bom\_no, self.currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L207)

<a id="op-dd866eb6dfadc9"></a>
### BOM.get rm rate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_raw_material_rate`

**Inputs** self, arg, notify = true.

**Record and data access** read “Item” via get\_value.

**State and service calls** msgprint with translated “Price not found for item {0} in price list {1}”.format(arg at “item\_code”, self.buying\_price\_list) · msgprint with translated “{0} not found for item {1}”.format(self.rm\_cost\_as\_per, arg at “item\_code”).

**Explicit results** (flt(rate) ÷ (self.conversion\_rate or 1)).

**Local steps**

- Set rate from 0.
- If not self.rm\_cost\_as\_per.
  - Set self.rm\_cost\_as\_per from “Valuation Rate”.
- If (arg and arg.get(“force\_valuation\_rate”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in arg → arg.get(“force\_valuation\_rate”).
  - Set rate from get\_valuation\_rate(arg).
- Otherwise.
  - If arg.
    - If (not Platform.db.get\_value(“Item”, arg at “item\_code”, “is\_customer\_provided\_item”) and not arg.get(“sourced\_by\_supplier”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.get\_value(“Item”, arg at “item\_code”, “is\_customer\_provided\_item”) → not arg.get(“sourced\_by\_supplier”).
      - If (arg.get(“bom\_no”) and (self.set\_rate\_of\_sub\_assembly\_item\_based\_on\_bom or arg.get(“is\_phantom\_item”))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in arg.get(“bom\_no”) → (self.set\_rate\_of\_sub\_assembly\_item\_based\_on\_bom or arg.get(“is\_phantom\_item”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.set\_rate\_of\_sub\_assembly\_item\_based\_on\_bom → arg.get(“is\_phantom\_item”).
        - Set rate from (flt(self.get\_bom\_unitcost(arg at “bom\_no”)) × (arg.get(“conversion\_factor”) or 1)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in arg.get(“conversion\_factor”) → 1.
      - Otherwise.
        - Set rate from get\_bom\_item\_rate(arg, self).
        - If self.rm\_cost\_as\_per equals “Price List”.
          - Set rate from (flt(rate) × flt((self.plc\_conversion\_rate or 1))).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.plc\_conversion\_rate → 1.
        - If not rate.
          - If self.rm\_cost\_as\_per equals “Price List”.
            - Evaluate Platform.msgprint(translated “Price not found for item {0} in price list {1}”.format(arg at “item\_code”, self.buying\_price\_list), alert = true).
          - Otherwise.
            - If notify.
              - Evaluate Platform.msgprint(translated “{0} not found for item {1}”.format(self.rm\_cost\_as\_per, arg at “item\_code”), alert = true).
- Return (flt(rate) ÷ (self.conversion\_rate or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.conversion\_rate → 1.

**Methods declared on this owner** [get bom unitcost](operations-004.md#op-324e71b1370efc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L170)
