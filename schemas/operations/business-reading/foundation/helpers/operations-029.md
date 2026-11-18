# Shared value and file services · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Modules

<a id="op-38491c90c62760"></a>
### Get modules from app

`operation_foundation_utils_modules_business_behavior_get_modules_from_application`

**Inputs** app.

**Wrappers, in declaration order** redis\_cache.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** Platform.get\_all(“Module Def”, filters = mapping(“app\_name” → app), fields = list(“module\_name”, “app\_name as app”)).

**Local steps**

- Return Platform.get\_all(“Module Def”, filters = mapping(“app\_name” → app), fields = list(“module\_name”, “app\_name as app”)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L359) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L357)

<a id="op-64401c7783a48d"></a>
### Is domain

`operation_foundation_utils_modules_business_behavior_is_domain`

**Inputs** module.

**Explicit results** module.get(“category”) equals “Domains”.

**Local steps**

- Return module.get(“category”) equals “Domains”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L475) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L359)

<a id="op-34fa012ab77fe3"></a>
### Is module

`operation_foundation_utils_modules_business_behavior_is_module`

**Inputs** module.

**Explicit results** module.get(“type”) equals “module”.

**Local steps**

- Return module.get(“type”) equals “module”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L546) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L360)

## Service · Momentjs

<a id="op-6b9145b257b18f"></a>
### Update

`operation_foundation_utils_momentjs_business_behavior_update`

**Inputs** tz, out.

**Explicit results** no value.

**Local steps**

- Set ltz from data at “links”.get(tz, tz).
- Set zone from data at “zones”.get(ltz).
- If not zone.
  - Return no value.
- Set out at “zones” at ltz from zone.
- Set out at “links” at tz from ltz.
- For each z in zone.
  - Set parts from z.split(one space).
  - If parts at 1 belongs to data at “rules”.
    - Set out at “rules” at parts at 1 from data at “rules” at parts at 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L622) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L363)

<a id="op-b998e715664c6f"></a>
### Get all timezones

`operation_foundation_utils_momentjs_business_behavior_get_all_timezones`

**Inputs** no declared parameters.

**Explicit results** sorted(list(data at “zones”)).

**Local steps**

- Return sorted(list(data at “zones”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L969) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L362)

## Service · Nestedset

<a id="op-01c5624adb39d1"></a>
### Update nsm

`operation_foundation_utils_nestedset_business_behavior_update_nested_set_model`

**Inputs** doc.

**State and service calls** request set\_value on doc.doctype.

**Local steps**

- Set old\_parent\_field from “old\_parent”.
- Set parent\_field from (“parent\_” + Platform.scrub(doc.doctype)).
- If hasattr(doc, “nsm\_parent\_field”).
  - Set parent\_field from doc.nsm\_parent\_field.
- If hasattr(doc, “nsm\_oldparent\_field”).
  - Set old\_parent\_field from doc.nsm\_oldparent\_field.
- Evaluate restore\_nsm\_fields(doc, old\_parent\_field).
- Set tuple(parent, old\_parent) from tuple((doc.get(parent\_field) or no value), (doc.get(old\_parent\_field) or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(parent\_field) → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(old\_parent\_field) → no value.
- If (not doc.lft and not doc.rgt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.lft → not doc.rgt.
  - Evaluate update\_add\_node(doc, (parent or empty text), parent\_field).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent → empty text.
- Otherwise.
  - If old\_parent differs from parent.
    - Evaluate update\_move\_node(doc, parent\_field).
- Evaluate doc.set(old\_parent\_field, parent).
- Evaluate Platform.db.set\_value(doc.doctype, doc.name, old\_parent\_field, (parent or empty text), update\_modified = false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent → empty text.
- Evaluate Platform.clear\_document\_cache(doc.doctype).
- Evaluate doc.reload().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L3) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L386)

<a id="op-91cb4cf3de74fb"></a>
### Restore nsm fields

`operation_foundation_binding_foundation_utils_nestedset_restore_nsm_fields`

**Inputs** doc, old\_parent\_field.

**State and service calls** request set\_value on doc.doctype.

**Explicit results** no value.

**Local steps**

- If doc.flags.in\_insert.
  - Set saved from Platform.\_dict(lft = 0, rgt = 0).
- Otherwise.
  - If not saved bound to doc.get\_doc\_before\_save().
    - Return no value.
- Set tuple(doc.lft, doc.rgt) from tuple(saved.lft, saved.rgt).
- Evaluate doc.set(old\_parent\_field, saved.get(old\_parent\_field)).
- Evaluate Platform.db.set\_value(doc.doctype, doc.name, mapping(“lft” → doc.lft, “rgt” → doc.rgt), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L61) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L219)

<a id="op-b3214d624ada2d"></a>
### Update add node

`operation_foundation_utils_nestedset_business_behavior_update_add_runtime_process`

**Inputs** doc, parent, parent\_field.

**Record and data access** read doctype via get\_value.

**Explicit results** right.

**Explicit failure paths** validation helper — translated “Nested set error. Please contact the Administrator.”.

**Local steps**

- Set doctype from doc.doctype.
- Set name from doc.name.
- Set Table from DocType(doctype).
- If parent.
  - Set tuple(left, right) from Platform.db.get\_value(doctype, mapping(“name” → parent), list(“lft”, “rgt”), for\_update = true).
  - Evaluate validate\_loop(doc.doctype, doc.name, left, right).
- Otherwise.
  - Set right from nested operand in the contract.select((nested operand in the contract + nested operand in the contract)).where(Coalesce(nested operand in the contract at nested operand in the contract, empty text) equals  … at 0.
- Set right from (right or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in right → 1.
- Evaluate nested operand in the contract(nested operand in the contract).set(Table.rgt, (nested operand in the contract.rgt + 2)).where(Table.rgt ≥ right).run().
- Evaluate nested operand in the contract(nested operand in the contract).set(Table.lft, (nested operand in the contract.lft + 2)).where(Table.lft ≥ right).run().
- If nested operand in the contract(nested operand in the contract).select(“\*”).where((Table.lft equals right bitwise or Table.rgt equals (right + 1))).run().
  - Call the validation error handler Platform.throw(translated “Nested set error. Please contact the Administrator.”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Table.rgt, (right + 1)).where(Table.name equals name).run().
- Return right.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L141) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L384)

<a id="op-2d86a42b3ce92a"></a>
### Update move node

`operation_foundation_utils_nestedset_business_behavior_update_move_runtime_process`

**Inputs** doc, parent\_field.

**Local steps**

- Set parent from doc.get(parent\_field).
- Set Table from DocType(doc.doctype).
- If parent.
  - Set new\_parent from nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).for\_update().run(as\_dict = true) at 0.
  - Evaluate validate\_loop(doc.doctype, doc.name, new\_parent.lft, new\_parent.rgt).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Table.rgt, negative nested operand in the contract.rgt).where((Table.lft ≥ doc.lft bitwise and Table.rgt ≤ …().
- Set diff from ((doc.rgt − doc.lft) + 1).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Table.rgt, (nested operand in the contract.rgt − diff)).where(Table.lft &gt; doc.rgt).run().
- Evaluate nested operand in the contract(nested operand in the contract).set(Table.rgt, (nested operand in the contract.rgt − diff)).where((Table.lft &lt; doc.lft bitwise and Table.rgt &gt; doc.rgt)).run().
- If parent.
  - Set new\_parent from nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).for\_update().run(as\_dict = true) at 0.
  - Evaluate nested operand in the contract(nested operand in the contract).set(Table.rgt, (nested operand in the contract.rgt + diff)).where(Table.name equals parent).run().
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Table.rgt, (nested operand in the contract.rgt + diff)).where(Table.lft &gt; new\_parent.rgt).run().
  - Evaluate nested operand in the contract(nested operand in the contract).set(Table.rgt, (nested operand in the contract.rgt + diff)).where((Table.lft &lt; new\_parent.lft bitwise and Table.rgt &gt; new\_parent.rgt)).run().
  - Set new\_diff from (new\_parent.rgt − doc.lft).
- Otherwise.
  - Set max\_rgt from nested operand in the contract.from\_(Table).select(Max(Table.rgt)).run(pluck = true) at 0.
  - Set new\_diff from ((max\_rgt + 1) − doc.lft).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Table.rgt, (negative nested operand in the contract + new\_diff)).where(Table.lft &lt; 0).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L2) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L385)

<a id="op-8b288b246e499c"></a>
### Rebuild tree for doctype

`operation_foundation_utils_nestedset_business_behavior_rebuild_tree_for_record_type`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Evaluate rebuild\_tree(doctype).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L4319) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L382)

<a id="op-4bb95ea15bec3c"></a>
### Rebuild tree

`operation_foundation_utils_nestedset_business_behavior_rebuild_tree`

**Inputs** doctype.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Rebuilding of tree is not supported for {}”.format(Platform.bold(doctype)).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If (not meta.has\_field(“lft”) or not meta.has\_field(“rgt”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta.has\_field(“lft”) → not meta.has\_field(“rgt”).
  - Call the validation error handler Platform.throw(translated “Rebuilding of tree is not supported for {}”.format(Platform.bold(doctype)), title = translated “Invalid Action”).
- Set parent\_field from (meta.nsm\_parent\_field or formatted text parent\_{Platform.scrub(doctype)}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.nsm\_parent\_field → formatted text parent\_{Platform.scrub(doctype)}.
- Set right from 1.
- Set table from DocType(doctype).
- Set column from getattr(table, parent\_field).
- Set result from nested operand in the contract(nested operand in the contract).orderby(table.name, order = Order.asc).select(table.name).run().
- Set Platform.db.auto\_commit\_on\_many\_writes from 1.
- For each r in result.
  - Set right from rebuild\_node(doctype, r at 0, right, parent\_field).
- Set Platform.db.auto\_commit\_on\_many\_writes from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(table, parent\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L4419) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L381)

<a id="op-3e0b2cd1c97b0b"></a>
### Rebuild node

`operation_foundation_utils_nestedset_business_behavior_rebuild_runtime_process`

**Inputs** doctype, parent, left, parent\_field.

**State and service calls** request set\_value on doctype.

**Explicit results** (right + 1).

**Local steps**

- Set right from (left + 1).
- Set table from DocType(doctype).
- Set column from getattr(table, parent\_field).
- Set children from nested operand in the contract(nested operand in the contract).select(table.name).orderby(table.name, order = Order.asc).run(pluck = true).
- For each child in children.
  - Set right from rebuild\_node(doctype, child, right, parent\_field).
- Evaluate Platform.db.set\_value(doctype, parent, mapping(“lft” → left, “rgt” → right), update\_modified = false).
- Return (right + 1).

**Values supplied outside this operation** selected callable from getattr(table, parent\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L139) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L380)

<a id="op-28f87193740d27"></a>
### Validate loop

`operation_foundation_utils_nestedset_business_behavior_validate_loop`

**Inputs** doctype, name, lft, rgt.

**Record and data access** read doctype via get\_all.

**Explicit failure paths** validation helper with NestedSetRecursionError — translated “Item cannot be added to its own descendants”.

**Local steps**

- If name belongs to Platform.get\_all(doctype, filters = mapping(“lft” → list(“&lt;=”, lft), “rgt” → list(“&gt;=”, rgt)), pluck = “name”).
  - Call the validation error handler Platform.throw(translated “Item cannot be added to its own descendants”, NestedSetRecursionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L5476) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L387)

<a id="op-db8807bd4d7006"></a>
### Remove subtree

`operation_foundation_utils_nestedset_business_behavior_remove_subtree`

**Inputs** doctype, name, throw = true.

**Record and data access** read doctype via get\_value.

**State and service calls** request delete on doctype.

**Local steps**

- Evaluate Platform.has\_permission(doctype, ptype = “delete”, throw = throw).
- Set tuple(lft, rgt) from Platform.db.get\_value(doctype, name, list(“lft”, “rgt”)).
- Evaluate Platform.db.delete(doctype, mapping(“lft” → tuple(“&gt;=”, lft), “rgt” → tuple(“&lt;=”, rgt))).
- Set width from ((rgt − lft) + 1).
- Set table from Platform.qb.DocType(doctype).
- Evaluate nested operand in the contract(nested operand in the contract).set(table.lft, (nested operand in the contract.lft − width)).where(table.lft &gt; rgt).run().
- Evaluate nested operand in the contract(nested operand in the contract).set(table.rgt, (nested operand in the contract.rgt − width)).where(table.rgt &gt; rgt).run().
- Evaluate Platform.clear\_document\_cache(doctype).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, ptype = “delete”, throw = throw).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L140) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L383)

<a id="op-37c37642c34251"></a>
### Nested Set.setup

`operation_foundation_utils_nestedset_business_behavior_nested_set_setup`

**Inputs** self.

**Local steps**

- If self.meta.get(“nsm\_parent\_field”).
  - Set self.nsm\_parent\_field from self.meta.nsm\_parent\_field.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L6277) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L376)

<a id="op-55facbdc6b8ca2"></a>
### Nested Set.after insert

`operation_foundation_utils_nestedset_business_behavior_nested_set_after_insert`

**Inputs** self.

**Record and data access** read “User Permission” via exists.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import or Platform.flags.in\_patch or Platform.flags.in\_migrate or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.in\_patch → Platform.flags.in\_migrate → Platform.flags.in\_install.
  - Return no value.
- If Platform.db.exists(“User Permission”, mapping(“user” → Platform.session.user, “allow” → self.doctype)).
  - Evaluate Platform.cache.hdel(“user\_permissions”, Platform.session.user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L6372) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L367)

<a id="op-b0031d6c029951"></a>
### Nested Set.on update

`operation_foundation_utils_nestedset_business_behavior_nested_set_on_update`

**Inputs** self.

**Local steps**

- Evaluate update\_nsm(self).
- Evaluate self.validate\_ledger().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate ledger](operations-029.md#op-222d62bb827ab7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L6592) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L375)

<a id="op-63e48fcc11582e"></a>
### Nested Set.on trash

`operation_foundation_utils_nestedset_business_behavior_nested_set_on_trash`

**Inputs** self, allow\_root\_deletion = false.

**Explicit failure paths** validation helper — translated “Root {0} cannot be deleted”.format(translated self.doctype) · propagate active failure.

**Local steps**

- If not getattr(self, “nsm\_parent\_field”, no value).
  - Set self.nsm\_parent\_field from (Platform.scrub(self.doctype) + “\_parent”).
- Set parent from self.get(self.nsm\_parent\_field).
- If (not parent and not getattr(self, “allow\_root\_deletion”, true)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not parent → not getattr(self, “allow\_root\_deletion”, true).
  - Call the validation error handler Platform.throw(translated “Root {0} cannot be deleted”.format(translated self.doctype)).
- Evaluate self.validate\_if\_child\_exists().
- Evaluate self.set(self.nsm\_parent\_field, empty text).
- Attempt the following.
  - Evaluate update\_nsm(self).
- On failure (Platform.DoesNotExistError).
  - If self.flags.on\_rollback.
    - Evaluate Platform.clear\_last\_message().
  - Otherwise.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate if child exists](operations-029.md#op-d360edff0b2c18).

**Values supplied outside this operation** selected callable from getattr(self, “nsm\_parent\_field”, no value), getattr(self, “allow\_root\_deletion”, true).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L374)

<a id="op-d360edff0b2c18"></a>
### Nested Set.validate if child exists

`operation_foundation_utils_nestedset_business_behavior_nested_set_validate_if_child_exists`

**Inputs** self.

**Record and data access** read self.doctype via count.

**Explicit failure paths** validation helper with NestedSetChildExistsError — translated “Cannot delete {0} as it has child nodes”.format(self.name).

**Local steps**

- Set has\_children from Platform.db.count(self.doctype, filters = mapping(self.nsm\_parent\_field → self.name)).
- If has\_children.
  - Call the validation error handler Platform.throw(translated “Cannot delete {0} as it has child nodes”.format(self.name), NestedSetChildExistsError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L438) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L377)

<a id="op-4d9366a83bdfd5"></a>
### Nested Set.before rename

`operation_foundation_utils_nestedset_business_behavior_nested_set_before_rename`

**Inputs** self, olddn, newdn, merge = false, group\_fname = “is\_group”.

**Record and data access** read self.doctype via get\_value.

**Explicit failure paths** validation helper with NestedSetInvalidMergeError — translated “Merging is only possible between Group-to-Group or Leaf Node-to-Leaf Node”.

**Local steps**

- If (merge and hasattr(self, group\_fname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in merge → hasattr(self, group\_fname).
  - Set is\_group from Platform.db.get\_value(self.doctype, newdn, group\_fname).
  - If self.get(group\_fname) differs from is\_group.
    - Call the validation error handler Platform.throw(translated “Merging is only possible between Group-to-Group or Leaf Node-to-Leaf Node”, NestedSetInvalidMergeError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L616) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L369)

<a id="op-f868653e893437"></a>
### Nested Set.after rename

`operation_foundation_utils_nestedset_business_behavior_nested_set_after_rename`

**Inputs** self, olddn, newdn, merge = false.

**State and service calls** request set\_value on self.doctype.

**Local steps**

- If not self.nsm\_parent\_field.
  - Set parent\_field from (“parent\_” + self.doctype.replace(one space, “\_”).lower()).
- Otherwise.
  - Set parent\_field from self.nsm\_parent\_field.
- Evaluate Platform.db.set\_value(self.doctype, mapping(parent\_field → newdn), mapping(“old\_parent” → newdn), update\_modified = false).
- If merge.
  - Evaluate rebuild\_tree(self.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L851) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L368)

<a id="op-f92b57e51442ed"></a>
### Nested Set.validate one root

`operation_foundation_utils_nestedset_business_behavior_nested_set_validate_one_root`

**Inputs** self.

**Explicit failure paths** validation helper with NestedSetMultipleRootsError — translated “Multiple root nodes not allowed.”.

**Local steps**

- If not self.get(self.nsm\_parent\_field).
  - If self.get\_root\_node\_count() &gt; 1.
    - Call the validation error handler Platform.throw(translated “Multiple root nodes not allowed.”, NestedSetMultipleRootsError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get root node count](operations-029.md#op-0086f22992870c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1117) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L379)

<a id="op-0086f22992870c"></a>
### Nested Set.get root node count

`operation_foundation_utils_nestedset_business_behavior_nested_set_get_root_runtime_process_count`

**Inputs** self.

**Record and data access** read self.doctype via count.

**Explicit results** Platform.db.count(self.doctype, mapping(self.nsm\_parent\_field → empty text)).

**Local steps**

- Return Platform.db.count(self.doctype, mapping(self.nsm\_parent\_field → empty text)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1263) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L373)

<a id="op-222d62bb827ab7"></a>
### Nested Set.validate ledger

`operation_foundation_utils_nestedset_business_behavior_nested_set_validate_ledger`

**Inputs** self, group\_identifier = “is\_group”.

**Record and data access** read self.doctype via get\_all.

**Explicit failure paths** validation helper — translated “{0} {1} cannot be a leaf node as it has children”.format(translated self.doctype, self.name).

**Local steps**

- If (hasattr(self, group\_identifier) and not bool(self.get(group\_identifier))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, group\_identifier) → not bool(self.get(group\_identifier)).
  - If Platform.get\_all(self.doctype, mapping(self.nsm\_parent\_field → self.name, “docstatus” → tuple(“!=”, 2))).
    - Call the validation error handler Platform.throw(translated “{0} {1} cannot be a leaf node as it has children”.format(translated self.doctype, self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1347) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L378)
