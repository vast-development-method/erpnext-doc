# Record lifecycle and persistence · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-0b5103dfddf56d"></a>
### Build import reference sets

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_build_import_reference_sets`

**Inputs** import\_file, id\_fieldname, alias\_field.

**Declared result** tuple at tuple(set at str, set at str).

**Explicit results** tuple(set(), set()) · tuple(ids, aliases).

**Local steps**

- Set columns from import\_file.header.columns.
- Set id\_index from \_get\_import\_column\_index(columns, id\_fieldname).
- Set alias\_index from \_get\_import\_column\_index(columns, alias\_field) when alias\_field, otherwise no value.
  - Value choice on alias\_field — true gives \_get\_import\_column\_index(columns, alias\_field), false gives no value.
- If (id\_index is identical to no value and alias\_index is identical to no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in id\_index is identical to no value → alias\_index is identical to no value.
  - Return tuple(set(), set()).
- Set ids from set().
- Set aliases from set().
- For each row in import\_file.data.
  - If id\_index is distinct from no value.
    - Set value from row.get(id\_index).
    - If value does not belong to INVALID\_VALUES.
      - Evaluate ids.add(cstr(value).strip()).
  - If alias\_index is distinct from no value.
    - Set value from row.get(alias\_index).
    - If value does not belong to INVALID\_VALUES.
      - Evaluate aliases.add(cstr(value).strip()).
- Return tuple(ids, aliases).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0054.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1189)

<a id="op-9a89aacdd0611d"></a>
### Get existing tree parent refs

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_existing_tree_parent_references`

**Inputs** doctype, parent\_refs, alias\_field.

**Declared result** set.

**Explicit results** set(\_build\_db\_tree\_parent\_name\_map(doctype, parent\_refs, alias\_field)).

**Local steps**

- Return set(\_build\_db\_tree\_parent\_name\_map(doctype, parent\_refs, alias\_field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L30) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1202)

<a id="op-a3a78857f8c072"></a>
### Build db tree parent name map

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_build_database_tree_parent_name_map`

**Inputs** doctype, parent\_refs, alias\_field.

**Declared result** dict.

**Record and data access** read doctype via get\_all.

**Explicit results** mapping() · name\_map.

**Local steps**

- Set parent\_list from list(parent\_refs).
- If not parent\_list.
  - Return mapping().
- Set name\_map from mapping().
- For each name in Platform.get\_all(doctype, filters = mapping(“name” → tuple(“in”, parent\_list)), pluck = “name”, limit = len(parent\_list)).
  - Set name\_map at name from name.
- If alias\_field.
  - Set names\_by\_alias from mapping().
  - For each row in Platform.get\_all(doctype, filters = mapping(alias\_field → tuple(“in”, parent\_list)), fields = list(“name”, alias\_field)).
    - Evaluate names\_by\_alias.setdefault(cstr(nested operand in the contract at nested operand in the contract).strip(), list()).append(row.name).
  - For each tuple(alias, names) in names\_by\_alias.items().
    - If len(names) equals 1.
      - Evaluate name\_map.setdefault(alias, names at 0).
- Return name\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L22) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1186)

<a id="op-a21f3fac41e92b"></a>
### Get tree columns

`operation_foundation_binding_foundation_core_doctype_data_import_importer_get_tree_columns`

**Inputs** import\_file.

**Explicit results** tuple(parent\_field, find\_column(parent\_field), is\_group\_field, find\_column(is\_group\_field)).

**Local steps**

- Set meta from Platform.get\_meta(import\_file.doctype).
- Set parent\_field from (meta.nsm\_parent\_field or formatted text parent\_{Platform.scrub(import\_file.doctype)}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.nsm\_parent\_field → formatted text parent\_{Platform.scrub(import\_file.doctype)}.
- Set is\_group\_field from “is\_group” when meta.has\_field(“is\_group”), otherwise no value.
  - Value choice on meta.has\_field(“is\_group”) — true gives “is\_group”, false gives no value.
- Bind local operation find\_column for subsequent calls.
- Return tuple(parent\_field, find\_column(parent\_field), is\_group\_field, find\_column(is\_group\_field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L609)

<a id="op-6803401eddbd24"></a>
### Get tree columns.find column

`operation_foundation_binding_foundation_core_doctype_data_import_importer_get_tree_columns_find_column`

**Inputs** fieldname.

**Explicit results** no value · next(generator of col for col drawn from import\_file.header.columns where (col.df and col.df.fieldname equals fieldname and not col.skip\_import), no value).

**Local steps**

- If not fieldname.
  - Return no value.
- Return next(generator of col for col drawn from import\_file.header.columns where (col.df and col.df.fieldname equals fieldname and not col.skip\_import), no value).
  - Draw col from import\_file.header.columns, keep a combination only if ((col.df and col.df.fieldname equals fieldname and not col.skip\_import)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df → col.df.fieldname equals fieldname → not col.skip\_import.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L610)

<a id="op-f70fb13881123e"></a>
### Build tree preview

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_build_tree_preview`

**Inputs** import\_file.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** no value · Platform.\_dict(nodes = display\_nodes, tree\_warnings = tree\_warnings, total\_nodes = len(nodes), editable = editable, …).

**Local steps**

- Set meta from Platform.get\_meta(import\_file.doctype).
- If not meta.is\_nested\_set().
  - Return no value.
- Set tuple(parent\_field, parent\_column, is\_group\_field, is\_group\_column) from \_get\_tree\_columns(import\_file).
- Set id\_fieldname from (getattr(import\_file.header, “id\_fieldname”, no value) or \_get\_id\_fieldname\_from\_meta(meta)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(import\_file.header, “id\_fieldname”, no value) → \_get\_id\_fieldname\_from\_meta(meta).
- Set alias\_field from getattr(import\_file.header, “tree\_alias\_field”, no value).
- Set label\_fieldname from (meta.title\_field or id\_fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.title\_field → id\_fieldname.
- Set editable from bool(parent\_column).
- Set is\_group\_editable from bool(is\_group\_column).
- Set overrides from (getattr(import\_file, “tree\_parent\_overrides”, no value) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(import\_file, “tree\_parent\_overrides”, no value) → mapping().
- Set nodes from list().
- Set id\_to\_rows from mapping().
- For each row in import\_file.data.
  - Set doc from row.parse\_doc(import\_file.doctype).
  - If not doc.
    - Continue with the next iteration or loop test.
  - Set node\_id from \_get\_tree\_node\_key(doc, id\_fieldname, alias\_field).
  - If not node\_id.
    - Continue with the next iteration or loop test.
  - Set orig\_parent from \_get\_tree\_parent\_value(row, parent\_column, doc, parent\_field).
  - Set orig\_is\_group from cint(doc.get(is\_group\_field)) when is\_group\_field, otherwise 0.
    - Value choice on is\_group\_field — true gives cint(doc.get(is\_group\_field)), false gives 0.
  - Set override from (overrides.get(row.row\_number) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in overrides.get(row.row\_number) → mapping().
  - Set parent from orig\_parent.
  - Set is\_group from orig\_is\_group.
  - If “parent” belongs to override.
    - Set value from override.get(“parent”).
    - Set parent from cstr(value).strip() when value does not belong to INVALID\_VALUES, otherwise no value.
      - Value choice on value does not belong to INVALID\_VALUES — true gives cstr(value).strip(), false gives no value.
  - If “is\_group” belongs to override.
    - Set is\_group from cint(override.get(“is\_group”)).
  - Set label from (doc.get(label\_fieldname) or node\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(label\_fieldname) → node\_id.
  - Set label from cstr(label).strip() when label does not belong to INVALID\_VALUES, otherwise node\_id.
    - Value choice on label does not belong to INVALID\_VALUES — true gives cstr(label).strip(), false gives node\_id.
  - Evaluate id\_to\_rows.setdefault(node\_id, list()).append(row.row\_number).
  - Evaluate nodes.append(Platform.\_dict(id = node\_id, label = label, parent = parent, row\_number = row.row\_number, …)).
- Set tree\_warnings from list().
- Set nodes\_by\_id from mapping of node.id → node for node drawn from nodes.
  - Draw node from nodes.
- Set duplicate\_messages from mapping().
- Set parent\_refs from set of node.parent for node drawn from nodes.
  - Draw node from nodes.
- For each tuple(node\_id, row\_numbers) in id\_to\_rows.items().
  - If (len(row\_numbers) &gt; 1 and (node\_id does not belong to import\_file.header.import\_aliases or node\_id belongs to parent\_refs)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(row\_numbers) &gt; 1 → (node\_id does not belong to import\_file.header.import\_aliases or node\_id belongs to parent\_refs).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in node\_id does not belong to import\_file.header.import\_aliases → node\_id belongs to parent\_refs.
    - Set message from translated “Duplicate ID {0} in rows {1}”.format(Platform.bold(escape\_html(cstr(node\_id))), format\_row\_numbers\_for\_warning(row\_numbers)).
    - Evaluate tree\_warnings.append(mapping(“message” → message, “type” → “duplicate\_id”, “duplicate\_id” → cstr(node\_id), “rows” → row\_numbers)).
    - Set duplicate\_messages at node\_id from message.
- For each node in nodes.
  - If message bound to duplicate\_messages.get(node.id).
    - Evaluate node.warnings.append(message).
- For each node in nodes.
  - Set parent\_id from node.parent.
  - If (not parent\_id or parent\_id does not belong to nodes\_by\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent\_id → parent\_id does not belong to nodes\_by\_id.
    - Continue with the next iteration or loop test.
  - If \_has\_parent\_cycle(node.id, nodes\_by\_id).
    - Set message from translated “Circular parent reference for {0}”.format(Platform.bold(escape\_html(cstr(node.id)))).
    - Evaluate node.warnings.append(message).
    - If not any(generator of w.get(“message”) equals message for w drawn from tree\_warnings).
      - Draw w from tree\_warnings.
      - Evaluate tree\_warnings.append(mapping(“row” → node.row\_number, “message” → message)).
- Set parents\_needing\_db\_check from set of node.parent for node drawn from nodes where (node.parent and node.parent does not belong to nodes\_by\_id and not \_is\_same\_file\_tree\_reference(node.parent, import\_file.header)).
  - Draw node from nodes, keep a combination only if ((node.parent and node.parent does not belong to nodes\_by\_id and not \_is\_same\_file\_tree\_reference(node.parent, import\_file.header))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in node.parent → node.parent does not belong to nodes\_by\_id → not \_is\_same\_file\_tree\_reference(node.parent, import\_file.header).
- Set existing\_parents\_in\_db from \_get\_existing\_tree\_parent\_refs(import\_file.doctype, parents\_needing\_db\_check, alias\_field).
- Set allow\_any\_existing\_parent from import\_file.import\_type equals UPDATE.
- For each node in nodes.
  - Set parent\_id from node.parent.
  - If (not parent\_id or parent\_id belongs to nodes\_by\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent\_id → parent\_id belongs to nodes\_by\_id.
    - Continue with the next iteration or loop test.
  - If \_is\_same\_file\_tree\_reference(parent\_id, import\_file.header).
    - Continue with the next iteration or loop test.
  - If (allow\_any\_existing\_parent or parent\_id belongs to existing\_parents\_in\_db).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in allow\_any\_existing\_parent → parent\_id belongs to existing\_parents\_in\_db.
    - Continue with the next iteration or loop test.
  - Set message from translated “Parent {0} not found in file”.format(Platform.bold(escape\_html(cstr(parent\_id)))).
  - Evaluate node.warnings.append(message).
  - Evaluate tree\_warnings.append(mapping(“row” → node.row\_number, “message” → message)).
- If is\_group\_field.
  - Evaluate \_append\_non\_group\_parent\_warnings(nodes, nodes\_by\_id, tree\_warnings, is\_group\_field).
- Set display\_nodes from \_order\_tree\_preview\_nodes(nodes).
- Return Platform.\_dict(nodes = display\_nodes, tree\_warnings = tree\_warnings, total\_nodes = len(nodes), editable = editable, …).

**Values supplied outside this operation** selected callable from getattr(import\_file.header, “id\_fieldname”, no value), getattr(import\_file.header, “tree\_alias\_field”, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L24) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1190)

<a id="op-423be652cf683b"></a>
### Append non group parent warnings

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_append_non_group_parent_warnings`

**Inputs** nodes, nodes\_by\_id, tree\_warnings, is\_group\_field.

**Local steps**

- Set children\_by\_parent from mapping().
- For each node in nodes.
  - If (node.parent and node.parent belongs to nodes\_by\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in node.parent → node.parent belongs to nodes\_by\_id.
    - Evaluate children\_by\_parent.setdefault(node.parent, list()).append(node).
- For each tuple(parent\_id, \_children) in children\_by\_parent.items().
  - Set parent from nodes\_by\_id.get(parent\_id).
  - If (not parent or parent.is\_group).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → parent.is\_group.
    - Continue with the next iteration or loop test.
  - Set display\_name from (parent.label or parent.id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent.label → parent.id.
  - Set message from translated “{0} has children but Is Group is 0 — parent must be a group node”.format(Platform.bold(escape\_html(cstr(display\_name)))).
  - If message does not belong to parent.warnings.
    - Evaluate parent.warnings.append(message).
  - If not any(generator of w.get(“message”) equals message for w drawn from tree\_warnings).
    - Draw w from tree\_warnings.
    - Evaluate tree\_warnings.append(mapping(“row” → parent.row\_number, “message” → message)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L21) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1185)

<a id="op-7c77f410b0306e"></a>
### Get tree parent value

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_tree_parent_value`

**Inputs** row, parent\_column, doc, parent\_field.

**Explicit results** cstr(value).strip() · cstr(value).strip() when value does not belong to INVALID\_VALUES, otherwise no value.

**Local steps**

- If parent\_column.
  - Set value from row.get(parent\_column.index).
  - If value does not belong to INVALID\_VALUES.
    - Return cstr(value).strip().
- Set value from doc.get(parent\_field).
- Return cstr(value).strip() when value does not belong to INVALID\_VALUES, otherwise no value.
  - Value choice on value does not belong to INVALID\_VALUES — true gives cstr(value).strip(), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0054.json#L4145) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1211)

<a id="op-fa734f37724a6e"></a>
### Has parent cycle

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_has_parent_cycle`

**Inputs** node\_id, nodes\_by\_id.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set seen from set().
- Set current from node\_id.
- While current.
  - If current belongs to seen.
    - Return true.
  - Evaluate seen.add(current).
  - Set node from nodes\_by\_id.get(current).
  - If (not node or not node.parent or node.parent does not belong to nodes\_by\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not node → not node.parent → node.parent does not belong to nodes\_by\_id.
    - Return false.
  - Set current from node.parent.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0054.json#L4394) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1215)

<a id="op-ab45eea38c3dec"></a>
### Sort tree payloads

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_sort_tree_payloads`

**Inputs** payloads, doctype, import\_type.

**Declared result** list.

**Explicit results** payloads · ordered.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If (import\_type does not belong to tuple(INSERT, UPSERT) or not meta.is\_nested\_set() or not payloads).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in import\_type does not belong to tuple(INSERT, UPSERT) → not meta.is\_nested\_set() → not payloads.
  - Return payloads.
- Set parent\_field from (meta.nsm\_parent\_field or formatted text parent\_{Platform.scrub(doctype)}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.nsm\_parent\_field → formatted text parent\_{Platform.scrub(doctype)}.
- Set id\_fieldname from \_get\_id\_fieldname\_from\_meta(meta).
- Set alias\_field from \_get\_tree\_alias\_field\_from\_meta(meta).
- Set payload\_keys from list().
- For each payload in payloads.
  - Set node\_id from \_get\_tree\_node\_key(payload.doc, id\_fieldname, alias\_field).
  - Set parent from payload.doc.get(parent\_field).
  - Set parent from cstr(parent).strip() when parent does not belong to INVALID\_VALUES, otherwise no value.
    - Value choice on parent does not belong to INVALID\_VALUES — true gives cstr(parent).strip(), false gives no value.
  - Evaluate payload\_keys.append(tuple(payload, node\_id, parent)).
- Set payload\_by\_id from mapping of node\_id → payload for tuple(payload, node\_id, \_parent) drawn from payload\_keys where node\_id.
  - Draw tuple(payload, node\_id, \_parent) from payload\_keys, keep a combination only if (node\_id).
- Set children\_by\_parent from mapping().
- Set roots from list().
- For each tuple(payload, node\_id, parent) in payload\_keys.
  - If not node\_id.
    - Continue with the next iteration or loop test.
  - If (parent and parent belongs to payload\_by\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → parent belongs to payload\_by\_id.
    - Evaluate children\_by\_parent.setdefault(parent, list()).append(payload).
  - Otherwise.
    - Evaluate roots.append(payload).
- For each children in children\_by\_parent.values().
  - Evaluate children.sort(key = deferred anonymous expression).
- Evaluate roots.sort(key = deferred anonymous expression).
- Set ordered from list().
- Set seen from set().
- Set payload\_id\_by\_payload from mapping of id(payload) → node\_id for tuple(payload, node\_id, \_parent) drawn from payload\_keys.
  - Draw tuple(payload, node\_id, \_parent) from payload\_keys.
- Set stack from list(reversed(roots)).
- While stack.
  - Set payload from stack.pop().
  - Set node\_id from payload\_id\_by\_payload at id(payload).
  - If id(payload) belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(id(payload)).
  - Evaluate ordered.append(payload).
  - Evaluate stack.extend(reversed(children\_by\_parent.get(node\_id, list()))).
- For each tuple(payload, \_node\_id, \_parent) in payload\_keys.
  - If id(payload) does not belong to seen.
    - Evaluate ordered.append(payload).
- Return ordered.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L50) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1271) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1263)

<a id="op-ef1b5add0d55b2"></a>
### Order tree preview nodes

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_order_tree_preview_nodes`

**Inputs** nodes.

**Declared result** list.

**Explicit results** ordered.

**Local steps**

- Set in\_file\_ids from set of node.id for node drawn from nodes.
  - Draw node from nodes.
- Set children\_by\_parent from mapping().
- For each node in nodes.
  - Set parent\_key from node.parent when node.parent belongs to in\_file\_ids, otherwise no value.
    - Value choice on node.parent belongs to in\_file\_ids — true gives node.parent, false gives no value.
  - Evaluate children\_by\_parent.setdefault(parent\_key, list()).append(node).
- For each children in children\_by\_parent.values().
  - Evaluate children.sort(key = deferred anonymous expression).
- Bind local operation get\_display\_key for subsequent calls.
- Set ordered from list().
- Set seen from set().
- Set stack from list of tuple(node, 0) for node drawn from reversed(children\_by\_parent.get(no value, list())).
  - Draw node from reversed(children\_by\_parent.get(no value, list())).
- While stack.
  - Set tuple(node, depth) from stack.pop().
  - If get\_display\_key(node) belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(get\_display\_key(node)).
  - Set node.depth from depth.
  - Evaluate ordered.append(node).
  - Evaluate stack.extend(generator of tuple(child, (depth + 1)) for child drawn from reversed(children\_by\_parent.get(node.id, list()))).
    - Draw child from reversed(children\_by\_parent.get(node.id, list())).
- For each node in nodes.
  - If get\_display\_key(node) does not belong to seen.
    - Set node.depth from 0.
    - Set node.orphan from true.
    - Evaluate ordered.append(node).
- Return ordered.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L48) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1252)

<a id="op-652a94a9858b26"></a>
### Order tree preview nodes.get display key

`operation_foundation_binding_foundation_core_doctype_data_import_importer_order_tree_preview_nodes_get_display_key`

**Inputs** node.

**Explicit results** node.id when node.id belongs to children\_by\_parent, otherwise node.row\_number.

**Local steps**

- Return node.id when node.id belongs to children\_by\_parent, otherwise node.row\_number.
  - Value choice on node.id belongs to children\_by\_parent — true gives node.id, false gives node.row\_number.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L618)

<a id="op-4c1d699f159ea4"></a>
### Row.initialize

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_initialize`

**Inputs** self, index, row, doctype, header, import\_type.

**Local steps**

- Set self.index from index.
- Set self.row\_number from (index + 1).
- Set self.doctype from doctype.
- Set self.data from row.
- Set self.header from header.
- Set self.import\_type from import\_type.
- Set self.warnings from list().
- Set len\_row from len(self.data).
- Set len\_columns from len(self.header.columns).
- If len\_row differs from len\_columns.
  - Set less\_than\_columns from len\_row &lt; len\_columns.
  - Set message from translated “This row has fewer cells than the header — check for missing commas or columns” when less\_than\_columns, otherwise translated “This row has more cells than the header — check for extra commas or columns”.
    - Value choice on less\_than\_columns — true gives translated “This row has fewer cells than the header — check for missing commas or columns”, false gives translated “This row has more cells than the header — check for extra commas or columns”.
  - Evaluate self.warnings.append(mapping(“row” → self.row\_number, “message” → message)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0054.json#L6627) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1258)

<a id="op-2ad9f42366a65d"></a>
### Row.parse doc

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_parse_record`

**Inputs** self, doctype, parent\_doc = no value, table\_df = no value.

**Explicit results** no value · self.\_parse\_doc(doctype, columns, values, parent\_doc, …).

**Local steps**

- Set col\_indexes from self.header.get\_column\_indexes(doctype, table\_df).
- Set values from self.get\_values(col\_indexes).
- If all(generator of v belongs to INVALID\_VALUES for v drawn from values).
  - Draw v from values.
  - Return no value.
- Set columns from self.header.get\_columns(col\_indexes).
- Return self.\_parse\_doc(doctype, columns, values, parent\_doc, …).

**Methods declared on this owner** [get values](operations-014.md#op-00a9120bbfdf63), [parse doc](operations-014.md#op-95e27483b71b48).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0054.json#L7039) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1259)

<a id="op-95e27483b71b48"></a>
### Row.parse doc

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_parse_record_2`

**Inputs** self, doctype, columns, values, parent\_doc = no value, table\_df = no value.

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc.

**State and service calls** request new\_doc for doctype.

**Explicit results** doc.

**Local steps**

- Set doc from Platform.\_dict().
- If self.import\_type equals INSERT.
  - Set doc from Platform.new\_doc(doctype, parent\_doc = parent\_doc, parentfield = table\_df.fieldname when table\_df, otherwise no value, as\_dict = true).
    - Value choice on table\_df — true gives table\_df.fieldname, false gives no value.
- For each key in ((Platform.model.default\_fields + Platform.model.child\_table\_fields) + tuple(“\_\_islocal”)).
  - Evaluate doc.pop(key, no value).
- For each tuple(col, value) in zip(columns, values, strict = false).
  - Set df from col.df.
  - If value belongs to INVALID\_VALUES.
    - Set value from no value.
  - If value is distinct from no value.
    - Set value from self.validate\_value(value, col).
  - If value is distinct from no value.
    - Set doc at df.fieldname from self.parse\_value(value, col).
- Set is\_table from Platform.get\_meta(doctype).istable.
- Set is\_update from self.import\_type belongs to tuple(UPDATE, UPSERT).
- If (is\_table and is\_update).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_table → is\_update.
  - Set id\_field from get\_id\_field(doctype).
  - Set id\_value from doc.get(id\_field.fieldname).
  - If (id\_value and Platform.db.exists(doctype, id\_value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in id\_value → Platform.db.exists(doctype, id\_value).
    - Set existing\_doc from Platform.get\_doc(doctype, id\_value).
    - Evaluate existing\_doc.update(doc).
    - Set doc from existing\_doc.
  - Otherwise.
    - Set new\_doc from Platform.new\_doc(doctype, as\_dict = true).
    - Evaluate new\_doc.update(doc).
    - Set doc from new\_doc.
- Return doc.

**Methods declared on this owner** [validate value](operations-014.md#op-a7e3e9420b7eac), [parse value](operations-014.md#op-edbe0fa1c85193).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0054.json#L7298) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1260)

<a id="op-a7e3e9420b7eac"></a>
### Row.validate value

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_validate_value`

**Inputs** self, value, col.

**Explicit results** value · no value.

**Local steps**

- If Platform.flags.in\_import.
  - Bind dependencies resolve\_import\_value.
  - Set value from resolve\_import\_value(value, col.df, self.header.reference\_doctype, self.header.value\_lookup).
- Set df from col.df.
- If df.fieldtype belongs to tuple(“Select”, “Link”).
  - Return value.
- If df.fieldtype equals “Date”.
  - Set value from self.get\_date(value, col).
  - If isinstance(value, str).
    - Evaluate self.warnings.append(mapping(“row” → self.row\_number, “col” → col.column\_number, “field” → df\_as\_json(df), “message” → translated “"{0}" is not a valid date. Use {1}”.format(Platform.bold(escape\_html(cstr( ….
    - Return no value.
- Otherwise.
  - If df.fieldtype equals “Datetime”.
    - Set value from self.get\_datetime(value, col).
    - If isinstance(value, str).
      - Evaluate self.warnings.append(mapping(“row” → self.row\_number, “col” → col.column\_number, “field” → df\_as\_json(df), “message” → translated “"{0}" is not a valid datetime. Use {1}”.format(Platform.bold(escape\_html(c ….
      - Return no value.
  - Otherwise.
    - If df.fieldtype equals “Duration”.
      - If not DURATION\_PATTERN.match(value).
        - Evaluate self.warnings.append(mapping(“row” → self.row\_number, “col” → col.column\_number, “field” → df\_as\_json(df), “message” → translated “"{0}" is not valid. Use duration format: d h m s”.format(Platform.bold(esc ….
    - Otherwise.
      - If (df.fieldtype belongs to tuple(“Int”, “Float”, “Currency”, “Percent”) and isinstance(value, str)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype belongs to tuple(“Int”, “Float”, “Currency”, “Percent”) → isinstance(value, str).
        - Set number\_format from get\_number\_format().
        - Set number from \_parse\_number(value, number\_format).
        - If number is identical to no value.
          - Set example from formatted text 1234{number\_format.decimal\_separator}56 when number\_format.decimal\_separator, otherwise “1234”.
            - Value choice on number\_format.decimal\_separator — true gives formatted text 1234{number\_format.decimal\_separator}56, false gives “1234”.
          - Evaluate self.warnings.append(mapping(“row” → self.row\_number, “col” → col.column\_number, “field” → df\_as\_json(df), “message” → translated “"{0}" is not a valid number, or could mean two numbers. Write it like {1}” ….
          - Return no value.
        - Set value from number.
- Return value.

**Methods declared on this owner** [get date](operations-014.md#op-8f8213ceb544b1), [get datetime](operations-014.md#op-2475b3f8bee562).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L49) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1262)

<a id="op-edbe0fa1c85193"></a>
### Row.parse value

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_parse_value`

**Inputs** self, value, col.

**Explicit results** value.

**Local steps**

- Set df from col.df.
- If (isinstance(value, (datetime bitwise or date)) and df.fieldtype belongs to list(“Date”, “Datetime”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, (datetime bitwise or date)) → df.fieldtype belongs to list(“Date”, “Datetime”).
  - Return value.
- Set value from cstr(value).
- Set valid\_check\_values from list(“t”, “f”, “true”, “false”, …).
- If (df.fieldtype equals “Check” and value.lower().strip() belongs to valid\_check\_values).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Check” → value.lower().strip() belongs to valid\_check\_values.
  - Set value from value.lower().strip().
  - Set value from 1 when value belongs to list(“t”, “true”, “y”, “yes”), otherwise 0.
    - Value choice on value belongs to list(“t”, “true”, “y”, “yes”) — true gives 1, false gives 0.
- If df.fieldtype belongs to list(“Int”, “Check”).
  - Set value from cint(value).
- Otherwise.
  - If df.fieldtype belongs to list(“Float”, “Percent”, “Currency”).
    - Set value from flt(value).
  - Otherwise.
    - If df.fieldtype equals “Date”.
      - Set value from self.get\_date(value, col).
    - Otherwise.
      - If df.fieldtype equals “Datetime”.
        - Set value from self.get\_datetime(value, col).
      - Otherwise.
        - If df.fieldtype equals “Duration”.
          - Set value from duration\_to\_seconds(value).
- Return value.

**Methods declared on this owner** [get date](operations-014.md#op-8f8213ceb544b1), [get datetime](operations-014.md#op-2475b3f8bee562).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L1782) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1261)

<a id="op-8f8213ceb544b1"></a>
### Row.get date

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_get_date`

**Inputs** self, value, column.

**Declared result** date.

**Explicit results** value · datetime.strptime(value, date\_format).date().

**Local steps**

- If isinstance(value, date).
  - Return value.
- Set date\_format from column.date\_format.
- If date\_format.
  - Attempt the following.
    - Return datetime.strptime(value, date\_format).date().
  - On failure (ValueError).
    - Take no action here.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L2467) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1255)

<a id="op-2475b3f8bee562"></a>
### Row.get datetime

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_get_datetime`

**Inputs** self, value, column.

**Declared result** datetime.

**Explicit results** value · datetime.strptime(value, date\_format).

**Local steps**

- If isinstance(value, datetime).
  - Return value.
- Set date\_format from column.date\_format.
- If date\_format.
  - Attempt the following.
    - Return datetime.strptime(value, date\_format).
  - On failure (ValueError).
    - Take no action here.
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L2642) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1256)

<a id="op-00a9120bbfdf63"></a>
### Row.get values

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_get_values`

**Inputs** self, indexes.

**Explicit results** list of get\_item\_at\_index(self.data, i) for i drawn from indexes.

**Local steps**

- Return list of get\_item\_at\_index(self.data, i) for i drawn from indexes.
  - Draw i from indexes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L2806) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1257)

<a id="op-7b3b80140c0cd9"></a>
### Row.get

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_get`

**Inputs** self, index.

**Explicit results** self.data at index.

**Local steps**

- Return self.data at index.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L2891) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1254)

<a id="op-eca6e9933fd30d"></a>
### Row.as list

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_row_as_list`

**Inputs** self.

**Explicit results** self.data.

**Local steps**

- Return self.data.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L2946) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1253)

<a id="op-159d5093b8d7bd"></a>
### Header.initialize

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_header_initialize`

**Inputs** self, index, row, doctype, raw\_data, column\_to\_field\_map = no value, value\_lookup = no value, reference\_doctype = no value, column\_to\_date\_format\_map = no value.

**Local steps**

- Set self.index from index.
- Set self.row\_number from (index + 1).
- Set self.data from row.
- Set self.doctype from doctype.
- Set self.reference\_doctype from (reference\_doctype or doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doctype → doctype.
- Set self.value\_lookup from (value\_lookup or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value\_lookup → mapping().
- Set column\_to\_field\_map from (column\_to\_field\_map or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in column\_to\_field\_map → Platform.\_dict().
- Set column\_to\_date\_format\_map from (column\_to\_date\_format\_map or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in column\_to\_date\_format\_map → Platform.\_dict().
- Set self.seen from list().
- Set self.columns from list().
- Set value\_row\_numbers from list of ((self.index + data\_idx) + 2) for data\_idx drawn from range(len(raw\_data)).
  - Draw data\_idx from range(len(raw\_data)).
- For each tuple(j, header) in enumerate(row).
  - Set column\_values from list of get\_item\_at\_index(r, j) for r drawn from raw\_data.
    - Draw r from raw\_data.
  - Set map\_to\_field from column\_to\_field\_map.get(str(j)).
  - Set column from Column(j, header, self.doctype, column\_values, …).
  - Evaluate self.seen.append(header).
  - Evaluate self.columns.append(column).
- Set doctypes from list().
- For each col in self.columns.
  - If not col.df.
    - Continue with the next iteration or loop test.
  - If col.df.parent equals self.doctype.
    - Evaluate doctypes.append(tuple(col.df.parent, no value)).
  - Otherwise.
    - Evaluate doctypes.append(tuple(col.df.parent, col.df.child\_table\_df)).
- Set self.doctypes from sorted(list(set(doctypes)), key = deferred anonymous expression).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L33) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1219)

<a id="op-e152fbfb7d98a5"></a>
### Header.get column indexes

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_header_get_column_indexes`

**Inputs** self, doctype, tablefield = no value.

**Explicit results** list of col.index for col drawn from self.columns where (not col.skip\_import and col.df and col.df.parent equals doctype and is\_table\_field(col.df)).

**Local steps**

- Bind local operation is\_table\_field for subsequent calls.
- Return list of col.index for col drawn from self.columns where (not col.skip\_import and col.df and col.df.parent equals doctype and is\_table\_field(col.df)).
  - Draw col from self.columns, keep a combination only if ((not col.skip\_import and col.df and col.df.parent equals doctype and is\_table\_field(col.df))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not col.skip\_import → col.df → col.df.parent equals doctype → is\_table\_field(col.df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L3880) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1216)
