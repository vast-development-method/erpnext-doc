# Forms, reports and navigation · operations 78

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Todo

<a id="op-17d8beda0316d2"></a>
### New todo

`operation_foundation_desk_record_definitions_todo_business_behavior_new_todo`

**Inputs** description.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “ToDo”, “description” → description) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “ToDo”, “description” → description)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “ToDo”, “description” → description)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0192.json#L606) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1280)

## Report · Todo

<a id="op-f4003de3a58b5a"></a>
### Execute

`operation_foundation_desk_report_todo_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “ToDo” via get\_list.

**Explicit results** tuple(columns, result).

**Local steps**

- Set priority\_map from mapping(“High” → 3, “Medium” → 2, “Low” → 1).
- Set todo\_list from Platform.get\_list(“ToDo”, fields = list(“name”, “date”, “description”, “priority”, …), filters = mapping(“status” → “Open”)).
- Evaluate todo\_list.sort(key = deferred anonymous expression, reverse = true).
- Set columns from list((translated “ID” + “:Link/ToDo:90”), (translated “Priority” + “::60”), (translated “Date” + “:Date”), (translated “Description” + “::150”), …).
- Set result from list().
- For each todo in todo\_list.
  - If (todo.owner equals Platform.session.user or todo.assigned\_by equals Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in todo.owner equals Platform.session.user → todo.assigned\_by equals Platform.session.user.
    - If todo.reference\_type.
      - Set todo.reference from text in the contract.format(todo.reference\_type, todo.reference\_name, todo.reference\_type, todo.reference\_name).
    - Otherwise.
      - Set todo.reference from no value.
    - Evaluate result.append(list(todo.name, todo.priority, todo.date, todo.description, …)).
- Return tuple(columns, result).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L930) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1370)

## Service · Tree

<a id="op-5938584b37e9bb"></a>
### Working Tree.initialize

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_init`

**Inputs** self, root.

**Local steps**

- Set self.root from root.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1814)

<a id="op-7a8dcac9b0bdd2"></a>
### Working Tree.resolve

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_resolve`

**Inputs** self, component\_id.

**Declared result** (dict bitwise or no value).

**Explicit results** find\_block(self.root, component\_id) when (self.root and component\_id), otherwise no value.

**Local steps**

- Return find\_block(self.root, component\_id) when (self.root and component\_id), otherwise no value.
  - Value choice on (self.root and component\_id) — true gives find\_block(self.root, component\_id), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.root → component\_id.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1816)

<a id="op-4b319330df38ae"></a>
### Working Tree.parent of

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_parent_of`

**Inputs** self, component\_id.

**Declared result** (dict bitwise or no value).

**Explicit results** block · no value.

**Local steps**

- For each tuple(block, \_) in walk\_blocks(self.root).
  - For each child in child\_blocks(block).
    - If child.get(“componentId”) equals component\_id.
      - Return block.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1815)

<a id="op-87baa2324a6ac3"></a>
### Working Tree.detach

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_detach`

**Inputs** self, component\_id.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set parent from self.parent\_of(component\_id).
- If parent is identical to no value.
  - Return no value.
- If parent.get(“children”).
  - Set parent at “children” from list of c for c drawn from parent at “children” where c.get(“componentId”) differs from component\_id.
    - Draw c from parent at “children”, keep a combination only if (c.get(“componentId”) differs from component\_id).
- For each slot in (parent.get(“componentSlots”) or mapping()).values().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent.get(“componentSlots”) → mapping().
  - Set content from slot.get(“slotContent”) when isinstance(slot, dict), otherwise no value.
    - Value choice on isinstance(slot, dict) — true gives slot.get(“slotContent”), false gives no value.
  - If isinstance(content, list).
    - Set slot at “slotContent” from list of c for c drawn from content where c.get(“componentId”) differs from component\_id.
      - Draw c from content, keep a combination only if (c.get(“componentId”) differs from component\_id).

If control reaches the end, it returns no value.

**Methods declared on this owner** [parent of](operations-078.md#op-4b319330df38ae).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1812)

<a id="op-8891eb9eaedbec"></a>
### Working Tree.id hint

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_id_hint`

**Inputs** self, component\_id.

**Declared result** str.

**Explicit results** formatted text  — that's the HTML id; this block's ref is '{block.get(“componentId”)}'. Use the ref. · “ — not a valid ref. Call query\_blocks or re-read the page outline for real refs.”.

**Local steps**

- For each tuple(block, \_) in walk\_blocks((self.root or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.root → mapping().
  - Set attrs from (block.get(“attributes”) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“attributes”) → mapping().
  - If (component\_id and attrs.get(“id”) equals component\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in component\_id → attrs.get(“id”) equals component\_id.
    - Return formatted text  — that's the HTML id; this block's ref is '{block.get(“componentId”)}'. Use the ref..
- Return “ — not a valid ref. Call query\_blocks or re-read the page outline for real refs.”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1813)

<a id="op-5214d49820c995"></a>
### Working Tree.apply

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply`

**Inputs** self, tool\_name, args.

**Declared result** str.

**Explicit results** self.apply\_update(args.get(“component\_id”)) · self.apply\_update\_blocks(args) · self.apply\_remove(args.get(“component\_id”)) · self.apply\_move(args) · self.apply\_add(args) · 5 additional forms in the steps below.

**Local steps**

- Set args from (args or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → mapping().
- If tool\_name equals “update\_block”.
  - Return self.apply\_update(args.get(“component\_id”)).
- If tool\_name equals “update\_blocks”.
  - Return self.apply\_update\_blocks(args).
- If tool\_name equals “remove\_block”.
  - Return self.apply\_remove(args.get(“component\_id”)).
- If tool\_name equals “move\_block”.
  - Return self.apply\_move(args).
- If tool\_name equals “add\_block”.
  - Return self.apply\_add(args).
- If tool\_name equals “set\_slot”.
  - Return self.apply\_set\_slot(args).
- If tool\_name equals “remove\_slot”.
  - Return self.apply\_remove\_slot(args).
- If tool\_name belongs to tuple(“bind\_prop”, “set\_repeater\_data”, “sync\_variable”).
  - Return self.apply\_bind(tool\_name, args).
- If tool\_name belongs to tuple(“set\_event\_handler”, “set\_visibility”).
  - Return self.apply\_interactivity(tool\_name, args).
- Return “Applied.”.

**Methods declared on this owner** [apply update](operations-078.md#op-df5f873a331433), [apply update blocks](operations-078.md#op-8b643b9bb62553), [apply remove](operations-078.md#op-6ab1d1e232a606), [apply move](operations-078.md#op-47637dc5318f2b), [apply add](operations-078.md#op-f8dcef27b5ca01), [apply set slot](operations-078.md#op-3335b219292c80), [apply remove slot](operations-078.md#op-3df4a4777e6404), [apply bind](operations-078.md#op-0cedf0209a9e55), [apply interactivity](operations-078.md#op-a81f2b53f71b37).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1802)

<a id="op-df5f873a331433"></a>
### Working Tree.apply update

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_update`

**Inputs** self, component\_id.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text Applied to block {component\_id} (&lt;{(block.get(“componentName”) or “div”)}&gt;)..

**Local steps**

- Set block from self.resolve(component\_id).
- If block is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- Return formatted text Applied to block {component\_id} (&lt;{(block.get(“componentName”) or “div”)}&gt;)..
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentName”) → “div”.

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1810)

<a id="op-8b643b9bb62553"></a>
### Working Tree.apply update blocks

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_update_blocks`

**Inputs** self, args.

**Declared result** str.

**Explicit results** “FAILED: no component\_ids or patches supplied — nothing to update.” · formatted text Applied to {applied} of {len(ids)} blocks. NOT FOUND: {missing}. Those refs don't exist — recheck them, don't reissue the same ids. · formatted text Applied to all {applied} block(s)..

**Local steps**

- Set patches from args.get(“patches”).
- If isinstance(patches, list).
  - Set ids from list of p.get(“component\_id”) for p drawn from patches where isinstance(p, dict).
    - Draw p from patches, keep a combination only if (isinstance(p, dict)).
- Otherwise.
  - Set ids from (args.get(“component\_ids”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“component\_ids”) → list().
- If not ids.
  - Return “FAILED: no component\_ids or patches supplied — nothing to update.”.
- Set missing from list of i for i drawn from ids where self.resolve(i) is identical to no value.
  - Draw i from ids, keep a combination only if (self.resolve(i) is identical to no value).
- Set applied from (len(ids) − len(missing)).
- If missing.
  - Return formatted text Applied to {applied} of {len(ids)} blocks. NOT FOUND: {missing}. Those refs don't exist — recheck them, don't reissue the same ids..
- Return formatted text Applied to all {applied} block(s)..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1811)

<a id="op-6ab1d1e232a606"></a>
### Working Tree.apply remove

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_remove`

**Inputs** self, component\_id.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text Removed block {component\_id}..

**Local steps**

- Set block from self.resolve(component\_id).
- If block is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- Evaluate self.detach(component\_id).
- Return formatted text Removed block {component\_id}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec), [detach](operations-078.md#op-87baa2324a6ac3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1807)

<a id="op-47637dc5318f2b"></a>
### Working Tree.apply move

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_move`

**Inputs** self, args.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text FAILED: new\_parent\_component\_id '{new\_parent\_id}' not found{self.id\_hint(new\_parent\_id)} · formatted text FAILED: can't move {component\_id} into itself or its own descendant ({new\_parent\_id}). · formatted text Moved block {component\_id} under {new\_parent\_id}..

**Local steps**

- Set component\_id from args.get(“component\_id”).
- Set new\_parent\_id from args.get(“new\_parent\_component\_id”).
- Set block from self.resolve(component\_id).
- If block is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- Set new\_parent from self.resolve(new\_parent\_id).
- If new\_parent is identical to no value.
  - Return formatted text FAILED: new\_parent\_component\_id '{new\_parent\_id}' not found{self.id\_hint(new\_parent\_id)}.
- If find\_block(block, new\_parent\_id) is distinct from no value.
  - Return formatted text FAILED: can't move {component\_id} into itself or its own descendant ({new\_parent\_id})..
- Evaluate self.detach(component\_id).
- Evaluate new\_parent.setdefault(“children”, list()).append(block).
- Return formatted text Moved block {component\_id} under {new\_parent\_id}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec), [detach](operations-078.md#op-87baa2324a6ac3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1806)

<a id="op-f8dcef27b5ca01"></a>
### Working Tree.apply add

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_add`

**Inputs** self, args.

**Declared result** str.

**Explicit results** formatted text FAILED: parent\_component\_id '{parent\_id}' not found{self.id\_hint(parent\_id)} · formatted text Added the {component\_name} block under {parent\_id}..

**Local steps**

- Set parent\_id from args.get(“parent\_component\_id”).
- If self.resolve(parent\_id) is identical to no value.
  - Return formatted text FAILED: parent\_component\_id '{parent\_id}' not found{self.id\_hint(parent\_id)}.
- Set component\_name from ((args.get(“block”) or mapping()).get(“name”) or “block”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (args.get(“block”) or mapping()).get(“name”) → “block”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“block”) → mapping().
- Return formatted text Added the {component\_name} block under {parent\_id}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1803)

<a id="op-3335b219292c80"></a>
### Working Tree.apply set slot

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_set_slot`

**Inputs** self, args.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text Set the '{args.get(“slot\_name”)}' slot of block {component\_id}..

**Local steps**

- Set component\_id from args.get(“component\_id”).
- If self.resolve(component\_id) is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- Return formatted text Set the '{args.get(“slot\_name”)}' slot of block {component\_id}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1809)

<a id="op-3df4a4777e6404"></a>
### Working Tree.apply remove slot

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_remove_slot`

**Inputs** self, args.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text Removed the '{slot\_name}' slot from block {component\_id}..

**Local steps**

- Set component\_id from args.get(“component\_id”).
- Set block from self.resolve(component\_id).
- If block is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- Set slot\_name from args.get(“slot\_name”).
- If isinstance(block.get(“componentSlots”), dict).
  - Evaluate block at “componentSlots”.pop(slot\_name, no value).
- Return formatted text Removed the '{slot\_name}' slot from block {component\_id}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1808)

<a id="op-0cedf0209a9e55"></a>
### Working Tree.apply bind

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_bind`

**Inputs** self, tool\_name, args.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text Bound block {component\_id} to repeat over {{ {source}.data }}. · formatted text Synced {prop} of block {component\_id} two-way with variable '{args.get(“variable\_name”)}'. · formatted text Bound prop '{args.get(“prop”)}' of block {component\_id} to {{ {args.get(“expression”)} }}..

**Local steps**

- Set component\_id from args.get(“component\_id”).
- Set block from self.resolve(component\_id).
- If block is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- If tool\_name equals “set\_repeater\_data”.
  - Set source from args.get(“data\_source\_name”).
  - Return formatted text Bound block {component\_id} to repeat over {{ {source}.data }}..
- If tool\_name equals “sync\_variable”.
  - Set prop from (args.get(“prop”) or “modelValue”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“prop”) → “modelValue”.
  - Return formatted text Synced {prop} of block {component\_id} two-way with variable '{args.get(“variable\_name”)}'..
- Return formatted text Bound prop '{args.get(“prop”)}' of block {component\_id} to {{ {args.get(“expression”)} }}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1804)

<a id="op-a81f2b53f71b37"></a>
### Working Tree.apply interactivity

`operation_foundation_binding_foundation_studio_ai_agent_tree_workingtree_apply_interactivity`

**Inputs** self, tool\_name, args.

**Declared result** str.

**Explicit results** formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)} · formatted text Wired {args.get(“event”)} handler on block {component\_id}. · formatted text Set visibility of block {component\_id} to {{ {args.get(“expression”)} }}..

**Local steps**

- Set component\_id from args.get(“component\_id”).
- Set block from self.resolve(component\_id).
- If block is identical to no value.
  - Return formatted text FAILED: component\_id '{component\_id}' not found{self.id\_hint(component\_id)}.
- If tool\_name equals “set\_event\_handler”.
  - Return formatted text Wired {args.get(“event”)} handler on block {component\_id}..
- Return formatted text Set visibility of block {component\_id} to {{ {args.get(“expression”)} }}..

**Methods declared on this owner** [resolve](operations-078.md#op-7a8dcac9b0bdd2), [id hint](operations-078.md#op-8891eb9eaedbec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1805)

## Service · Treeview

<a id="op-982418f975b4d2"></a>
### Get all nodes

`operation_foundation_desk_treeview_business_behavior_get_all_nodes`

**Inputs** doctype, label, parent, tree\_method, remaining named values filters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** out.

**Explicit failure paths** validation helper — translated “Failed to get method for command {0} with {1}”.format(tree\_method, str(e)).

**Local steps**

- Evaluate filters.pop(“cmd”, no value).
- Evaluate filters.pop(“data”, no value).
- Attempt the following.
  - Set tree\_method from Platform.override\_whitelisted\_method(tree\_method).
  - Set callable\_tree\_method from Platform.get\_attr(tree\_method).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Failed to get method for command {0} with {1}”.format(tree\_method, str(e))).
- Evaluate Platform.is\_whitelisted(callable\_tree\_method).
- Set data from callable\_tree\_method(doctype, parent, expanded names filters).
- Set out from list(dict(parent = label, data = data)).
- Evaluate filters.pop(“is\_root”, no value).
- Set to\_check from list of d.get(“value”) for d drawn from data where d.get(“expandable”).
  - Draw d from data, keep a combination only if (d.get(“expandable”)).
- While to\_check.
  - Set parent from to\_check.pop().
  - Set data from callable\_tree\_method(doctype, parent, is\_root = false, expanded names filters).
  - Evaluate out.append(dict(parent = parent, data = data)).
  - For each d in data.
    - If d.get(“expandable”).
      - Evaluate to\_check.append(d.get(“value”)).
- Return out.

**Values supplied outside this operation** selected callable from Platform.get\_attr(tree\_method).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L4287) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1431)

<a id="op-2e58b15c06f87d"></a>
### Get children

`operation_foundation_desk_treeview_business_behavior_get_children`

**Inputs** doctype, parent = empty text, include\_disabled = false, remaining named values filters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_children(doctype, parent, include\_disabled = include\_disabled).

**Local steps**

- If isinstance(include\_disabled, str).
  - Set include\_disabled from Platform.sbool(include\_disabled).
- Return \_get\_children(doctype, parent, include\_disabled = include\_disabled).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L5025) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1432)

<a id="op-def438abd974fb"></a>
### Get children

`operation_foundation_desk_treeview_business_behavior_get_children_2`

**Inputs** doctype, parent = empty text, ignore\_permissions = false, include\_disabled = false.

**Explicit results** qb.run(as\_dict = true).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set table from Platform.qb.DocType(doctype).
- Set parent\_field from (meta.get(“nsm\_parent\_field”) or (“parent\_” + Platform.scrub(doctype))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get(“nsm\_parent\_field”) → (“parent\_” + Platform.scrub(doctype)).
- Set filters from list(list(“docstatus”, “&lt;”, 2)).
- If (Platform.db.has\_column(doctype, “disabled”) and not include\_disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.has\_column(doctype, “disabled”) → not include\_disabled.
  - Evaluate filters.append(list(“disabled”, “=”, 0)).
- Set qb from Platform.qb.get\_query(doctype, fields = list(“name as value”, formatted text {(nested operand in the contract(nested operand in the contract) or “name”)} as title, “is\_group as expandable”), filters = filt ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get(“title\_field”) → “name”.
- Return qb.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L5230) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1433)

<a id="op-5939ba3d6bcfa4"></a>
### Add node

`operation_foundation_desk_treeview_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set args from make\_tree\_args(expanded names Platform.form\_dict).
- Set doc from Platform.get\_doc(args).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L5778) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1430)

<a id="op-8b8f03c61ca6c0"></a>
### Make tree args

`operation_foundation_desk_treeview_business_behavior_make_tree_arguments`

**Inputs** remaining named values kwarg.

**Explicit results** Platform.\_dict(kwarg).

**Local steps**

- Evaluate kwarg.pop(“cmd”, no value).
- Set doctype from kwarg at “doctype”.
- Set parent\_field from (“parent\_” + Platform.scrub(doctype)).
- If kwarg at “is\_root” equals “false”.
  - Set kwarg at “is\_root” from false.
- If kwarg at “is\_root” equals “true”.
  - Set kwarg at “is\_root” from true.
- Set parent from (kwarg.get(“parent”) or kwarg.get(parent\_field)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwarg.get(“parent”) → kwarg.get(parent\_field).
- If doctype differs from parent.
  - Evaluate kwarg.update(mapping(parent\_field → parent)).
- Return Platform.\_dict(kwarg).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L5902) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1434)

## Service · Update password

<a id="op-ae6800be6a46f2"></a>
### Get context

`operation_foundation_public_pages_update_password_business_behavior_get_context`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L2986) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L101)

## Service · Utils

<a id="op-ad532e3ff91308"></a>
### Remove attach

`operation_foundation_desk_form_utils_business_behavior_remove_attach`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“DELETE”, “POST”)).

**State and service calls** request delete\_doc for “File”.

**Local steps**

- Set fid from Platform.form\_dict.get(“fid”).
- Evaluate Platform.delete\_doc(“File”, fid).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L4616) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L286)
