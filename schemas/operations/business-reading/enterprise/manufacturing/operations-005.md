# Production · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom

<a id="op-3e99612fb18c1b"></a>
### BOM.add materials from bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_add_materials_from_bill_of_materials`

**Inputs** self, finished\_good, bom\_no, operation\_row\_id, qty = no value, replace = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “BOM” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “BOM {0} not found for the item {1}”.format(bom\_no, finished\_good).

**Local steps**

- If not Platform.db.exists(“BOM”, mapping(“item” → finished\_good, “name” → bom\_no, “docstatus” → 1)).
  - Call the validation error handler Platform.throw(translated “BOM {0} not found for the item {1}”.format(bom\_no, finished\_good)).
- If replace.
  - Evaluate self.remove\_operation\_materials(operation\_row\_id).
- If (self.items and not self.items at 0.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.items → not self.items at 0.item\_code.
  - Evaluate self.set(“items”, list()).
- If not qty.
  - Set qty from 1.
- For each row in self.items.
  - If row.operation\_row\_id equals operation\_row\_id.
    - Return no value.
- Set bom\_items from get\_bom\_items(bom\_no, self.company, qty = qty, fetch\_exploded = 0).
- For each row in bom\_items.
  - Set row.uom from row.stock\_uom.
  - Set row.operation\_row\_id from operation\_row\_id.
  - Set row.idx from no value.
  - Set row.do\_not\_explode from 1.
  - Set row.is\_sub\_assembly\_item from self.is\_sub\_assembly\_item(row.item\_code).
  - Evaluate self.append(“items”, row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove operation materials](operations-004.md#op-0db60429d9e112), [is sub assembly item](operations-004.md#op-a172e82f9b8289).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L147)

<a id="op-df25f2b27230a6"></a>
### BOM.traverse tree

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_traverse_tree`

**Inputs** self, bom\_list = no value.

**Explicit results** bom\_list.

**Local steps**

- Bind local operation \_get\_children for subsequent calls.
- Set count from 0.
- If not bom\_list.
  - Set bom\_list from list().
- If self.name does not belong to bom\_list.
  - Evaluate bom\_list.append(self.name).
- While count &lt; len(bom\_list).
  - For each child\_bom in \_get\_children(bom\_list at count).
    - If child\_bom does not belong to bom\_list.
      - Evaluate bom\_list.append(child\_bom).
  - Update count using + 1.
- Evaluate bom\_list.reverse().
- Return bom\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L193)

<a id="op-7af90dd0076e8f"></a>
### BOM.traverse tree.get children

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_traverse_tree_get_children`

**Inputs** bom\_no.

**Explicit results** children.

**Local steps**

- Set children from Platform.cache().hget(“bom\_children”, bom\_no).
- If children is identical to no value.
  - Set children from Platform.db.sql\_list(query text (SELECT, BOM Item), bom\_no).
  - Evaluate Platform.cache().hset(“bom\_children”, bom\_no, children).
- Return children.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L639)

<a id="op-0154f61889ef02"></a>
### BOM.calculate cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_calculate_cost`

**Inputs** self, save\_updates = false, update\_hour\_rate = false.

**Local steps**

- Evaluate self.calculate\_op\_cost(update\_hour\_rate, save = save\_updates).
- Evaluate self.calculate\_rm\_cost(save = save\_updates).
- Evaluate self.calculate\_secondary\_items\_costs(save = save\_updates).
- Evaluate self.set\_fg\_cost\_allocation().
- If save\_updates.
  - Evaluate self.calculate\_exploded\_cost().
- Set old\_cost from self.total\_cost.
- Set self.total\_cost from ((self.operating\_cost + self.raw\_material\_cost) − self.secondary\_items\_cost).
- Set self.base\_total\_cost from ((self.base\_operating\_cost + self.base\_raw\_material\_cost) − self.base\_secondary\_items\_cost).
- If self.total\_cost differs from old\_cost.
  - Set self.flags.cost\_updated from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate op cost](operations-005.md#op-7503569d7b8304), [calculate rm cost](operations-005.md#op-8d1e8cd30c83ab), [calculate secondary items costs](operations-005.md#op-05308e91fd84cf), [set fg cost allocation](operations-003.md#op-d2cebb9f5f10a9), [calculate exploded cost](operations-005.md#op-9ec8e1a0df32f9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L152)

<a id="op-7503569d7b8304"></a>
### BOM.calculate op cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_calculate_operating_profit_cost`

**Inputs** self, update\_hour\_rate = false, save = true.

**Local steps**

- Set self.operating\_cost from 0.
- Set self.base\_operating\_cost from 0.
- If self.get(“with\_operations”).
  - For each d in self.get(“operations”).
    - If (d.workstation or d.workstation\_type).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.workstation → d.workstation\_type.
      - Evaluate self.update\_rate\_and\_time(d, update\_hour\_rate, save).
    - Set operating\_cost from d.operating\_cost.
    - Set base\_operating\_cost from d.base\_operating\_cost.
    - If d.set\_cost\_based\_on\_bom\_qty.
      - Set operating\_cost from (flt(d.cost\_per\_unit) × flt(self.quantity)).
      - Set base\_operating\_cost from (flt(d.base\_cost\_per\_unit) × flt(self.quantity)).
    - Update self.operating\_cost using + flt(operating\_cost).
    - Update self.base\_operating\_cost using + flt(base\_operating\_cost).
- Otherwise.
  - If self.get(“fg\_based\_operating\_cost”).
    - Set total\_operating\_cost from (flt(self.get(“quantity”)) × flt(self.get(“operating\_cost\_per\_bom\_quantity”))).
    - Set self.operating\_cost from total\_operating\_cost.
    - Set self.base\_operating\_cost from flt((total\_operating\_cost × self.conversion\_rate), 2).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update rate and time](operations-005.md#op-9d042e6a834865).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L154)

<a id="op-9d042e6a834865"></a>
### BOM.update rate and time

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_update_rate_and_time`

**Inputs** self, row, update\_hour\_rate = false, save = true.

**Record and data access** read “Workstation” via get\_cached\_value · read “Workstation Type” via get\_cached\_value.

**State and service calls** call db\_update on row.

**Local steps**

- If (not row.hour\_rate or update\_hour\_rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.hour\_rate → update\_hour\_rate.
  - Set hour\_rate from 0.
  - If row.workstation.
    - Set hour\_rate from flt(Platform.get\_cached\_value(“Workstation”, row.workstation, “hour\_rate”)).
  - Otherwise.
    - If row.workstation\_type.
      - Set hour\_rate from flt(Platform.get\_cached\_value(“Workstation Type”, row.workstation\_type, “hour\_rate”)).
  - If hour\_rate.
    - Set row.hour\_rate from (hour\_rate ÷ flt(self.conversion\_rate)) when (self.conversion\_rate and hour\_rate), otherwise hour\_rate.
      - Value choice on (self.conversion\_rate and hour\_rate) — true gives (hour\_rate ÷ flt(self.conversion\_rate)), false gives hour\_rate.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.conversion\_rate → hour\_rate.
- If row.hour\_rate.
  - Set row.base\_hour\_rate from (flt(row.hour\_rate) × flt(self.conversion\_rate)).
  - If row.time\_in\_mins.
    - Set row.operating\_cost from ((flt(row.hour\_rate) × flt(row.time\_in\_mins)) ÷ 60.0).
    - Set row.base\_operating\_cost from (flt(row.operating\_cost) × flt(self.conversion\_rate)).
    - Set row.cost\_per\_unit from (row.operating\_cost ÷ (row.batch\_size or 1.0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_size → 1.0.
    - Set row.base\_cost\_per\_unit from (row.base\_operating\_cost ÷ (row.batch\_size or 1.0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_size → 1.0.
- If (update\_hour\_rate and save).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_hour\_rate → save.
  - Evaluate row.db\_update().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Workstation”, row.workstation, “hour\_rate”), Platform.get\_cached\_value(“Workstation Type”, row.workstation\_type, “hour\_rate”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L204)

<a id="op-8d1e8cd30c83ab"></a>
### BOM.calculate rm cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_calculate_raw_material_cost`

**Inputs** self, save = false.

**State and service calls** call db\_update on d.

**Local steps**

- Set total\_rm\_cost from 0.
- Set base\_total\_rm\_cost from 0.
- For each d in self.get(“items”).
  - Set old\_rate from d.rate.
  - If (d.is\_stock\_item or d.is\_phantom\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.is\_stock\_item → d.is\_phantom\_item.
    - Set d.rate from self.get\_rm\_rate(mapping(“company” → self.company, “item\_code” → d.item\_code, “bom\_no” → d.bom\_no, “qty” → d.qty, …), notify = false).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.source\_warehouse → self.default\_source\_warehouse.
  - Set d.base\_rate from (flt(d.rate) × flt(self.conversion\_rate)).
  - Set d.amount from flt((flt(d.rate, d.precision(“rate”)) × flt(d.qty, d.precision(“qty”))), d.precision(“amount”)).
  - Set d.base\_amount from (d.amount × flt(self.conversion\_rate)).
  - Set d.qty\_consumed\_per\_unit from (flt(d.stock\_qty, d.precision(“stock\_qty”)) ÷ flt(self.quantity, self.precision(“quantity”))).
  - Update total\_rm\_cost using + d.amount.
  - Update base\_total\_rm\_cost using + d.base\_amount.
  - If (save and old\_rate differs from d.rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in save → old\_rate differs from d.rate.
    - Evaluate d.db\_update().
- Set self.raw\_material\_cost from total\_rm\_cost.
- Set self.base\_raw\_material\_cost from base\_total\_rm\_cost.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rm rate](operations-003.md#op-dd866eb6dfadc9).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L155)

<a id="op-05308e91fd84cf"></a>
### BOM.calculate secondary items costs

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_calculate_secondary_items_costs`

**Inputs** self, save = false.

**State and service calls** call db\_update on d.

**Local steps**

- Set total\_sm\_cost from 0.
- Set base\_total\_sm\_cost from 0.
- Set precision from self.precision(“raw\_material\_cost”).
- Set allocation\_basis from (flt(self.raw\_material\_cost) − self.\_set\_own\_cost\_secondary\_items(precision, save)).
- For each d in self.get(“secondary\_items”).
  - If d.valuation\_type does not belong to tuple(“Valuation Rate”, “Manual”).
    - Set d.cost from flt((allocation\_basis × (flt(d.cost\_allocation\_per) ÷ 100)), precision).
    - Set d.base\_cost from flt((d.cost × self.conversion\_rate), precision).
    - If save.
      - Evaluate d.db\_update().
  - Update total\_sm\_cost using + d.cost.
  - Update base\_total\_sm\_cost using + d.base\_cost.
- Set self.secondary\_items\_cost from total\_sm\_cost.
- Set self.base\_secondary\_items\_cost from base\_total\_sm\_cost.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set own cost secondary items](operations-005.md#op-ec01409e772344).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L156)

<a id="op-ec01409e772344"></a>
### BOM.set own cost secondary items

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_set_own_cost_secondary_items`

**Inputs** self, precision, save.

**Declared result** float.

**State and service calls** call db\_update on d.

**Explicit results** total.

**Local steps**

- Set total from 0.0.
- For each d in self.get(“secondary\_items”).
  - If d.valuation\_type equals “Valuation Rate”.
    - Set rate from self.get\_rm\_rate(self.\_secondary\_item\_rate\_args(d)).
    - Set d.cost from flt((flt(rate) × flt(d.stock\_qty)), precision).
  - Otherwise.
    - If d.valuation\_type equals “Manual”.
      - Set d.cost from flt(d.cost, precision).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Set d.base\_cost from flt((d.cost × self.conversion\_rate), precision).
  - Update total using + d.cost.
  - If save.
    - Evaluate d.db\_update().
- Return total.

**Methods declared on this owner** [get rm rate](operations-003.md#op-dd866eb6dfadc9), [secondary item rate args](operations-005.md#op-5f8fd215190a2a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L638)

<a id="op-5f8fd215190a2a"></a>
### BOM.secondary item rate args

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_secondary_item_rate_args`

**Inputs** self, d.

**Explicit results** mapping(“item\_code” → d.item\_code, “company” → self.company, “warehouse” → self.default\_target\_warehouse, “set\_rate\_based\_on\_warehouse” → 1, …).

**Local steps**

- Return mapping(“item\_code” → d.item\_code, “company” → self.company, “warehouse” → self.default\_target\_warehouse, “set\_rate\_based\_on\_warehouse” → 1, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L635)

<a id="op-9ec8e1a0df32f9"></a>
### BOM.calculate exploded cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_calculate_exploded_cost`

**Inputs** self.

**State and service calls** call db\_update on row.

**Local steps**

- Set rm\_rate\_map from self.get\_rm\_rate\_map().
- For each row in self.get(“exploded\_items”).
  - Set old\_rate from flt(row.rate).
  - Set row.rate from rm\_rate\_map.get(row.item\_code).
  - Set row.amount from (flt(row.stock\_qty) × flt(row.rate)).
  - If old\_rate differs from row.rate.
    - Evaluate row.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rm rate map](operations-005.md#op-9c4f5196459988).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L153)

<a id="op-9c4f5196459988"></a>
### BOM.get rm rate map

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_raw_material_rate_map`

**Inputs** self.

**Declared result** dict at tuple(str, float).

**Record and data access** read “BOM Explosion Item” via get\_all.

**Explicit results** rm\_rate\_map.

**Local steps**

- Set rm\_rate\_map from mapping().
- For each item in self.get(“items”).
  - If item.bom\_no.
    - Set explosion\_items from Platform.get\_all(“BOM Explosion Item”, filters = mapping(“parent” → item.bom\_no), fields = list(“item\_code”, “rate”), order\_by = no value).
    - Set explosion\_item\_rate from mapping of item.item\_code → flt(item.rate) for item drawn from explosion\_items.
      - Draw item from explosion\_items.
    - Evaluate rm\_rate\_map.update(explosion\_item\_rate).
  - Otherwise.
    - Set rm\_rate\_map at item.item\_code from (flt(item.base\_rate) ÷ flt((item.conversion\_factor or 1.0))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.0.
- Return rm\_rate\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L171)

<a id="op-ff5f728a71231c"></a>
### BOM.update exploded items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_update_exploded_items`

**Inputs** self, save = true.

**Local steps**

- Evaluate self.get\_exploded\_items().
- Evaluate self.add\_exploded\_items(save = save).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get exploded items](operations-005.md#op-9bcb044d60ddd8), [add exploded items](operations-005.md#op-3c86ec9b20374d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L202)

<a id="op-9bcb044d60ddd8"></a>
### BOM.get exploded items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_exploded_items`

**Inputs** self.

**Local steps**

- Set self.cur\_exploded\_items from mapping().
- For each d in self.get(“items”).
  - If d.bom\_no.
    - Evaluate self.get\_child\_exploded\_items(d.bom\_no, d.stock\_qty, d.operation).
  - Otherwise.
    - If d.item\_code.
      - Evaluate self.add\_to\_cur\_exploded\_items(Platform.\_dict(mapping(“item\_code” → d.item\_code, “item\_name” → d.item\_name, “operation” → d.operation, “is\_sub\_assembly\_item” → d.is\_sub\_assembly\_item, …))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.conversion\_factor) → 1.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get child exploded items](operations-005.md#op-536d0ea38d36d3), [add to cur exploded items](operations-005.md#op-172e79ec6ec2fd).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L165)

<a id="op-748c84316a0566"></a>
### BOM.company currency

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_company_currency`

**Inputs** self.

**Explicit results** Enterprise.get\_company\_currency(self.company).

**Local steps**

- Return Enterprise.get\_company\_currency(self.company).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0457.json#L580) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L160)

<a id="op-172e79ec6ec2fd"></a>
### BOM.add to cur exploded items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_add_to_cur_exploded_items`

**Inputs** self, args.

**Local steps**

- Set key from args.item\_code.
- If args.operation.
  - Set key from tuple(args.item\_code, args.operation).
- If self.cur\_exploded\_items.get(key).
  - Update self.cur\_exploded\_items at key at “stock\_qty” using + args.stock\_qty.
- Otherwise.
  - Set self.cur\_exploded\_items at key from args.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L149)

<a id="op-536d0ea38d36d3"></a>
### BOM.get child exploded items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_child_exploded_items`

**Inputs** self, bom\_no, stock\_qty, operation = no value.

**Record and data access** execute query text (SELECT, BOM Explosion Item).

**Local steps**

- Set child\_fb\_items from Platform.db.sql(query text (SELECT, BOM Explosion Item), bom\_no, as\_dict = 1).
- For each d in child\_fb\_items.
  - Set good\_qty from (flt(d.quantity) or 1) when d.is\_phantom\_bom, otherwise get\_good\_qty(d).
    - Value choice on d.is\_phantom\_bom — true gives (flt(d.quantity) or 1), false gives get\_good\_qty(d).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.quantity) → 1.
  - Set d.qty\_consumed\_per\_unit from (flt(d.stock\_qty) ÷ good\_qty).
  - Evaluate self.add\_to\_cur\_exploded\_items(Platform.\_dict(mapping(“item\_code” → d at “item\_code”, “item\_name” → d at “item\_name”, “source\_warehouse” → d at “source\_warehouse”, “operation” → (d at “operation” or operation), …))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d at “operation” → operation.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add to cur exploded items](operations-005.md#op-172e79ec6ec2fd).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L163)

<a id="op-3c86ec9b20374d"></a>
### BOM.add exploded items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_add_exploded_items`

**Inputs** self, save = true.

**State and service calls** execute query text (DELETE, BOM Explosion Item) · call db\_insert on ch.

**Local steps**

- Evaluate self.set(“exploded\_items”, list()).
- If save.
  - Evaluate Platform.db.sql(query text (DELETE, BOM Explosion Item), self.name).
- For each d in sorted(self.cur\_exploded\_items, key = itemgetter(0)).
  - Set ch from self.append(“exploded\_items”, mapping()).
  - For each i in self.cur\_exploded\_items at d.keys().
    - Evaluate ch.set(i, self.cur\_exploded\_items at d at i).
  - Set ch.amount from (flt(ch.stock\_qty) × flt(ch.rate)).
  - Set ch.qty\_consumed\_per\_unit from (flt(ch.stock\_qty) ÷ flt(self.quantity)).
  - Set ch.docstatus from self.docstatus.
  - If save.
    - Evaluate ch.db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L146)

<a id="op-f7005e04eca08a"></a>
### BOM.validate child boms on reactivation

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_validate_child_boms_on_reactivation`

**Inputs** self.

**Record and data access** read “BOM” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot activate BOM {0} because sub-assembly BOMs {1} are not active”.format(Platform.bold(self.name), “, ”.join(generator of Platform.bold(bom) for bom drawn from unusable)).

**Local steps**

- If (not self.is\_active or not self.has\_value\_changed(“is\_active”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_active → not self.has\_value\_changed(“is\_active”).
  - Return no value.
- Set child\_boms from set of row.bom\_no for row drawn from (self.items + self.operations) where row.get(“bom\_no”).
  - Draw row from (self.items + self.operations), keep a combination only if (row.get(“bom\_no”)).
- If not child\_boms.
  - Return no value.
- Set unusable from Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“in”, list(child\_boms))), or\_filters = mapping(“is\_active” → 0, “docstatus” → tuple(“!=”, 1)), pluck = “name”).
- If unusable.
  - Call the validation error handler Platform.throw(translated “Cannot activate BOM {0} because sub-assembly BOMs {1} are not active”.format(Platform.bold(self.name), “, ”.join(generator of Platform.bold(bom) for bom drawn from unusable))).
    - Draw bom from unusable.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L642)

<a id="op-e4c2d3edc4d5b0"></a>
### BOM.validate bom links

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_bill_of_materials_links`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot deactivate or cancel BOM as it is linked with other BOMs”.

**Local steps**

- Evaluate self.validate\_child\_boms\_on\_reactivation().
- If not self.is\_active.
  - Set bom from Platform.qb.DocType(“BOM”).
  - For each doctype in tuple(“BOM Item”, “BOM Operation”).
    - Set child from Platform.qb.DocType(doctype).
    - Set act\_pbom from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….run().
    - If (act\_pbom and act\_pbom at 0 at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in act\_pbom → act\_pbom at 0 at 0.
      - Call the validation error handler Platform.throw(translated “Cannot deactivate or cancel BOM as it is linked with other BOMs”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate child boms on reactivation](operations-005.md#op-f7005e04eca08a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L208)

<a id="op-234550e01075c7"></a>
### BOM.validate transfer against

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_transfer_against`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Setting {0} is required”.format(translated self.meta.get\_label(“transfer\_material\_against”)).

**Local steps**

- If not self.with\_operations.
  - Set self.transfer\_material\_against from “Work Order”.
- If (not self.transfer\_material\_against and not self.track\_semi\_finished\_goods and not self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.transfer\_material\_against → not self.track\_semi\_finished\_goods → not self.is\_new().
  - Call the validation error handler Platform.throw(translated “Setting {0} is required”.format(translated self.meta.get\_label(“transfer\_material\_against”)), title = translated “Missing value”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L217)

<a id="op-6a54ad541f54ba"></a>
### BOM.set routing operations

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_routing_operations`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_routing().
- If (self.routing and self.with\_operations and not self.operations).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.routing → self.with\_operations → not self.operations.
  - Evaluate self.set\_operations\_from\_routing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate routing](operations-005.md#op-f47eeeece2b8c2), [set operations from routing](operations-003.md#op-6f80f3b70cd39f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L191)

<a id="op-f47eeeece2b8c2"></a>
### BOM.validate routing

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_validate_routing`

**Inputs** self.

**Record and data access** read “Routing” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Routing {0} is disabled”.format(get\_link\_to\_form(“Routing”, self.routing)).

**Local steps**

- If (not self.routing or not self.has\_value\_changed(“routing”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.routing → not self.has\_value\_changed(“routing”).
  - Return no value.
- If Platform.db.get\_value(“Routing”, self.routing, “disabled”).
  - Call the validation error handler Platform.throw(translated “Routing {0} is disabled”.format(get\_link\_to\_form(“Routing”, self.routing))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L643)

<a id="op-7c81b185fa5b7c"></a>
### BOM.validate operations

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_operations`

**Inputs** self.

**Record and data access** read “Operation” via get\_value.

**Explicit failure paths** validation helper — translated “Operations cannot be left blank” · validation helper — translated “Row {0}: Workstation or Workstation Type is mandatory for an operation {1}”.format(d.idx, d.operation) · validation helper — translated “Row {0}: Operation time should be greater than 0 for operation {1}”.format(d.idx, d.operation).

**Local steps**

- If (self.with\_operations and not self.get(“operations”) and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.with\_operations → not self.get(“operations”) → self.docstatus equals 1.
  - Call the validation error handler Platform.throw(translated “Operations cannot be left blank”).
- If self.with\_operations.
  - For each d in self.operations.
    - If not d.description.
      - Set d.description from Platform.db.get\_value(“Operation”, d.operation, “description”).
    - If (not d.batch\_size or d.batch\_size ≤ 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.batch\_size → d.batch\_size ≤ 0.
      - Set d.batch\_size from 1.
    - If (not d.workstation and not d.workstation\_type).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.workstation → not d.workstation\_type.
      - Call the validation error handler Platform.throw(translated “Row {0}: Workstation or Workstation Type is mandatory for an operation {1}”.format(d.idx, d.operation)).
    - If (not d.time\_in\_mins or d.time\_in\_mins ≤ 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.time\_in\_mins → d.time\_in\_mins ≤ 0.
      - Call the validation error handler Platform.throw(translated “Row {0}: Operation time should be greater than 0 for operation {1}”.format(d.idx, d.operation)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L212)
