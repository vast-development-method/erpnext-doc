# Forms, reports and navigation · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Kanban board

[Record definition](../../../../data/record-types/kanban_board.json)

<a id="op-6a55ef8d561385"></a>
### Add card

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_add_card`

**Inputs** board\_name, docname, colname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call insert on col\_order · call save on board.

**Explicit results** saved.

**Local steps**

- Set board from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate board.check\_permission(“read”).
- Evaluate Platform.has\_permission(board.reference\_doctype, “write”, throw = true).
- Set tuple(col\_order, col\_idx) from get\_kanban\_column\_order\_and\_index(board, colname).
- Evaluate col\_order.insert(0, docname).
- Set board.columns at col\_idx.order from Platform.as\_json(col\_order).
- Set saved from board.save(ignore\_permissions = true).
- Evaluate publish\_kanban\_board\_update(saved).
- Return saved.

**Values supplied outside this operation** effective access from board.check\_permission(“read”), Platform.has\_permission(board.reference\_doctype, “write”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L5831) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L796)

<a id="op-dde05c14df86e5"></a>
### Quick kanban board

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_quick_kanban_board`

**Inputs** doctype, board\_name, field\_name, project = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Kanban Board” · call save on doc.

**Explicit results** doc.

**Local steps**

- Set doc from Platform.new\_doc(“Kanban Board”).
- Set meta from Platform.get\_meta(doctype).
- Set doc.kanban\_board\_name from board\_name.
- Set doc.reference\_doctype from doctype.
- Set doc.field\_name from field\_name.
- If project.
  - Set doc.filters from formatted text &#91;&#91;"Task","project","=","{project}"&#93;&#93;.
- Set options from empty text.
- For each field in meta.fields.
  - If field.fieldname equals field\_name.
    - Set options from field.options.
- Set columns from list().
- If options.
  - Set columns from options.split(whitespace '\\n').
- For each column in columns.
  - If not column.
    - Continue with the next iteration or loop test.
  - Evaluate doc.append(“columns”, dict(column\_name = column)).
- If doctype belongs to list(“Note”, “ToDo”).
  - Set doc.private from 1.
- Evaluate doc.save().
- Return doc.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L6200) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L819)

<a id="op-01402e7f806947"></a>
### Get order for column

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_order_for_column`

**Inputs** board, colname.

**Record and data access** read board.reference\_doctype via get\_list.

**Explicit results** Platform.as\_json(Platform.get\_list(board.reference\_doctype, filters = filters, pluck = “name”)).

**Local steps**

- Set filters from list(list(board.reference\_doctype, board.field\_name, “=”, colname)).
- If (board.filters and parsed\_filters bound to Platform.parse\_json(board.filters)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in board.filters → parsed\_filters bound to Platform.parse\_json(board.filters).
  - Evaluate filters.append(parsed\_filters at 0).
- Return Platform.as\_json(Platform.get\_list(board.reference\_doctype, filters = filters, pluck = “name”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L6754) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L808)

<a id="op-e72e21c4a9c2c3"></a>
### Update column order

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_update_column_order`

**Inputs** board\_name, order.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call save on board.

**Explicit results** board.

**Local steps**

- Set board from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate board.check\_permission(“write”).
- Set order from Platform.parse\_json(order).
- Set old\_columns from board.columns.
- Set new\_columns from list().
- For each col in order.
  - For each column in list(old\_columns).
    - If col equals column.column\_name.
      - Evaluate new\_columns.append(column).
      - Evaluate old\_columns.remove(column).
- Evaluate new\_columns.extend(old\_columns).
- Set board.columns from list().
- For each col in new\_columns.
  - Evaluate board.append(“columns”, dict(column\_name = col.column\_name, status = col.status, order = col.order, indicator = col.indicator)).
- Evaluate board.save().
- Return board.

**Values supplied outside this operation** effective access from board.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L6988) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L822)

<a id="op-1f918da5cfd14a"></a>
### Set indicator

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_set_indicator`

**Inputs** board\_name, column\_name, indicator.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call save on board.

**Explicit results** board.

**Local steps**

- Set board from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate board.check\_permission(“write”).
- For each column in board.columns.
  - If column.column\_name equals column\_name.
    - Set column.indicator from indicator.
- Evaluate board.save().
- Return board.

**Values supplied outside this operation** effective access from board.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L7476) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L821)

<a id="op-2cc91285a8af77"></a>
### Save settings

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_save_settings`

**Inputs** board\_name, settings.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** resp.

**Local steps**

- Set settings from (Platform.parse\_json(settings) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(settings) → mapping().
- Set doc from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate doc.check\_permission(“write”).
- Set fields from settings at “fields”.
- If not isinstance(fields, str).
  - Set fields from json.dumps(fields).
- Set doc.fields from fields.
- If “show\_labels” belongs to settings.
  - Set doc.show\_labels from settings.get(“show\_labels”).
- Evaluate doc.save().
- Set resp from doc.as\_dict().
- Set resp at “fields” from Platform.parse\_json(resp at “fields”).
- Return resp.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L12) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L820)

## Service · Layers

<a id="op-ea31a85b9fa3a3"></a>
### Resolve layers

`operation_foundation_desk_layers_business_behavior_resolve_layers`

**Inputs** base, layers, key (named only), apply\_row (named only), keep\_unnamed (named only, default true).

**Declared result** tuple at tuple(list at dict, dict at tuple(str, bool)).

**Explicit results** tuple(resolved, hidden).

**Local steps**

- Set resolved from list of dict(item) for item drawn from base.
  - Draw item from base.
- Set hidden from mapping of key(item) → bool(item.get(“hidden”)) for item drawn from base.
  - Draw item from base.
- For each rows in layers.
  - Set resolved from apply\_layer(resolved, rows, hidden, key = key, apply\_row = apply\_row, keep\_unnamed = keep\_unnamed).
- Return tuple(resolved, hidden).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L292)

<a id="op-97cc627088b30a"></a>
### Apply layer

`operation_foundation_desk_layers_business_behavior_apply_layer`

**Inputs** items, rows, hidden, key (named only), apply\_row (named only), keep\_unnamed (named only, default true).

**Declared result** list at dict.

**Explicit results** items · arranged\_items · (unnamed + arranged\_items) · (arranged\_items + unnamed).

**Local steps**

- Set by\_key from mapping of key(item) → item for item drawn from items.
  - Draw item from items.
- Set base\_keys from set(by\_key).
- Set arranged from list().
- Set named from set().
- For each row in rows.
  - Set row\_key from key(row).
  - If row\_key belongs to named.
    - Continue with the next iteration or loop test.
  - Set entry from apply\_row(row, by\_key.get(row\_key)).
  - If entry is identical to no value.
    - Continue with the next iteration or loop test.
  - Set by\_key at row\_key from entry.
  - Set hidden at row\_key from bool(row.get(“hidden”)).
  - Evaluate arranged.append(row\_key).
  - Evaluate named.add(row\_key).
- If not named.
  - Return items.
- Set arranged\_items from list of by\_key at row\_key for row\_key drawn from arranged.
  - Draw row\_key from arranged.
- If not keep\_unnamed.
  - Return arranged\_items.
- Set unnamed from list of item for item drawn from items where key(item) does not belong to named.
  - Draw item from items, keep a combination only if (key(item) does not belong to named).
- If (arranged and all(generator of row\_key does not belong to base\_keys for row\_key drawn from arranged)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in arranged → all(generator of row\_key does not belong to base\_keys for row\_key drawn from arranged).
  - Draw row\_key from arranged.
  - Return (unnamed + arranged\_items).
- Return (arranged\_items + unnamed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L372) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L291)

## Service · Like

<a id="op-b575603e2c18e3"></a>
### Toggle like

`operation_foundation_desk_like_business_behavior_toggle_like`

**Inputs** doctype, name, add = false.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate \_toggle\_like(doctype, name, add).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L1091) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L295)

<a id="op-12b63eee6f3a06"></a>
### Toggle like

`operation_foundation_desk_like_business_behavior_toggle_like_2`

**Inputs** doctype, name, add, user = no value.

**Record and data access** read doctype via get\_value · read “User” via get\_cached\_value.

**State and service calls** request set\_single\_value on doctype · request set\_value on doctype.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Evaluate Platform.has\_permission(doctype, “read”, doc = name, throw = true).
- Attempt the following.
  - Set liked\_by from Platform.db.get\_value(doctype, name, “\_liked\_by”).
  - If liked\_by.
    - Set liked\_by from json.loads(liked\_by).
  - Otherwise.
    - Set liked\_by from list().
  - If add equals “Yes”.
    - If user does not belong to liked\_by.
      - Evaluate liked\_by.append(user).
      - Evaluate add\_comment(doctype, name).
      - If Platform.get\_cached\_value(“User”, user, “follow\_liked\_documents”).
        - Evaluate \_follow\_document(doctype, name, user).
  - Otherwise.
    - If user belongs to liked\_by.
      - Evaluate liked\_by.remove(user).
      - Evaluate remove\_like(doctype, name).
  - If Platform.get\_meta(doctype).issingle.
    - Evaluate Platform.db.set\_single\_value(doctype, “\_liked\_by”, json.dumps(liked\_by), update\_modified = false).
  - Otherwise.
    - Evaluate Platform.db.set\_value(doctype, name, “\_liked\_by”, json.dumps(liked\_by), update\_modified = false).
- On failure (Platform.db.ProgrammingError) bound to e.
  - If Platform.db.is\_missing\_column(e).
    - Evaluate add\_column(doctype, “\_liked\_by”, “Text”).
    - Evaluate \_toggle\_like(doctype, name, add, user).
  - Otherwise.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, doc = name, throw = true) · configured or stored value from Platform.get\_cached\_value(“User”, user, “follow\_liked\_documents”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L76) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L296)

<a id="op-64a34432a9c251"></a>
### Remove like

`operation_foundation_desk_like_business_behavior_remove_like`

**Inputs** doctype, name.

**Record and data access** read “Comment” via get\_all.

**State and service calls** request delete\_doc for “Comment”.

**Local steps**

- Evaluate Platform.delete\_doc(“Comment”, list of c.name for c drawn from Platform.get\_all(“Comment”, filters = mapping(“comment\_type” → “Like”, “reference\_doctype” → doctype, “reference\_name” → name, “owner” → Platf ….
  - Draw c from Platform.get\_all(“Comment”, filters = mapping(“comment\_type” → “Like”, “reference\_doctype” → doctype, “reference\_name” → name, “owner” → Platform.session.user)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L2017) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L294)

<a id="op-b1ecb9c9cf6693"></a>
### Add comment

`operation_foundation_desk_like_business_behavior_add_comment`

**Inputs** doctype, name.

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name).
- Evaluate doc.add\_comment(“Like”, translated “Liked”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L2240) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L293)

## Service · Link preview

<a id="op-2fe9fe8c3d247f"></a>
### Get preview data

`operation_foundation_desk_link_preview_business_behavior_get_preview_data`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = (60 × 10)).

**Record and data access** read doctype via get\_list · resolve a document from doctype via get\_doc.

**Explicit results** no value · formatted\_preview\_data.

**Local steps**

- Set preview\_fields from list().
- Set meta from Platform.get\_meta(doctype).
- If not meta.show\_preview\_popup.
  - Return no value.
- Set preview\_fields from list of field.fieldname for field drawn from meta.fields where (field.in\_preview and field.fieldtype does not belong to no\_value\_fields and field.fieldtype does not belong to table\_fields).
  - Draw field from meta.fields, keep a combination only if ((field.in\_preview and field.fieldtype does not belong to no\_value\_fields and field.fieldtype does not belong to table\_fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.in\_preview → field.fieldtype does not belong to no\_value\_fields → field.fieldtype does not belong to table\_fields.
- If not preview\_fields.
  - Set preview\_fields from list of field.fieldname for field drawn from meta.fields where (field.reqd and field.fieldtype does not belong to table\_fields).
    - Draw field from meta.fields, keep a combination only if ((field.reqd and field.fieldtype does not belong to table\_fields)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.reqd → field.fieldtype does not belong to table\_fields.
- Set title\_field from meta.get\_title\_field().
- Set image\_field from meta.image\_field.
- Evaluate preview\_fields.append(title\_field).
- If image\_field.
  - Evaluate preview\_fields.append(image\_field).
- Evaluate preview\_fields.append(“name”).
- Set preview\_data from Platform.get\_list(doctype, filters = mapping(“name” → docname), fields = preview\_fields, limit = 1).
- If not preview\_data.
  - Return no value.
- Set preview\_data from preview\_data at 0.
- Set formatted\_preview\_data from mapping(“preview\_image” → preview\_data.get(image\_field), “preview\_title” → preview\_data.get(title\_field), “name” → preview\_data.get(“name”)).
- Set doc from no value.
- If (meta.show\_title\_field\_in\_link and meta.title\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.show\_title\_field\_in\_link → meta.title\_field.
  - Set doc from Platform.get\_doc(doctype, docname).
  - Evaluate set\_title\_values\_for\_link\_and\_dynamic\_link\_fields(meta, doc).
- For each tuple(key, val) in preview\_data.items().
  - If (val and meta.has\_field(key) and key does not belong to list(image\_field, title\_field, “name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in val → meta.has\_field(key) → key does not belong to list(image\_field, title\_field, “name”).
    - Set formatted\_preview\_data at meta.get\_field(key).label from Platform.format(value = val, doc = doc, df = meta.get\_field(key), translated = true).
- Return formatted\_preview\_data.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L2353) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L297)

## Service · Link title

<a id="op-bca7e6c1c3cbc6"></a>
### Get link title field

`operation_foundation_binding_foundation_desk_link_title_get_link_title_field`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Explicit results** no value · title\_field.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If not (meta.show\_title\_field\_in\_link and meta.title\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.show\_title\_field\_in\_link → meta.title\_field.
  - Return no value.
- Set title\_field from meta.title\_field.strip().
- If (title\_field equals “name” or not Platform.has\_permission(doctype, “select”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title\_field equals “name” → not Platform.has\_permission(doctype, “select”).
  - Return no value.
- If title\_field does not belong to get\_permitted\_fields(doctype, ignore\_virtual = true).
  - Return no value.
- Return title\_field.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “select”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L788)

<a id="op-2c9467dbcd8016"></a>
### Get link titles

`operation_foundation_binding_foundation_desk_link_title_get_link_titles`

**Inputs** doctype, title\_field, names.

**Declared result** dict at tuple(str, str).

**Record and data access** read doctype via get\_list.

**Explicit results** titles.

**Local steps**

- Set titles from mapping().
- For each names\_batch in create\_batch(list(names), TITLE\_BATCH\_SIZE).
  - Set rows from Platform.get\_list(doctype, filters = mapping(“name” → tuple(“in”, names\_batch)), fields = list(“name”, title\_field), limit = len(names\_batch)).
  - Evaluate titles.update(mapping of row.name → row.get(title\_field) for row drawn from rows).
    - Draw row from rows.
- Return titles.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L789)

<a id="op-0f2b464524cd39"></a>
### Send link titles

`operation_foundation_binding_foundation_desk_link_title_send_link_titles`

**Inputs** link\_titles.

**Local steps**

- If “\_link\_titles” does not belong to Platform.local.response.
  - Set Platform.local.response at “\_link\_titles” from mapping().
- Evaluate Platform.local.response at “\_link\_titles”.update(link\_titles).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L791)

<a id="op-e44dbc0f1b38c5"></a>
### Get report link titles

`operation_foundation_binding_foundation_desk_link_title_get_report_link_titles`

**Inputs** columns, rows.

**Declared result** dict at tuple(str, str).

**Explicit results** titles.

**Local steps**

- Set titles from mapping().
- Set names\_by\_doctype from get\_link\_names\_by\_doctype((columns or list()), (rows or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in columns → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().
- For each tuple(doctype, names) in names\_by\_doctype.items().
  - Set title\_field from get\_link\_title\_field(doctype).
  - If not title\_field.
    - Continue with the next iteration or loop test.
  - For each tuple(name, title) in get\_link\_titles(doctype, title\_field, names).items().
    - Set titles at formatted text {doctype}::{name} from title.
- Return titles.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L790)

<a id="op-f78a429391442d"></a>
### Get link names by doctype

`operation_foundation_binding_foundation_desk_link_title_get_link_names_by_doctype`

**Inputs** columns, rows.

**Declared result** dict at tuple(str, set).

**Explicit results** names\_by\_doctype.

**Local steps**

- Set link\_columns from list of tuple(index, column at “fieldname”, column at “options”) for tuple(index, column) drawn from enumerate(columns) where (isinstance(column, dict) and column.get(“fieldtype”) equals “Link” and column. ….
  - Draw tuple(index, column) from enumerate(columns), keep a combination only if ((isinstance(column, dict) and column.get(“fieldtype”) equals “Link” and column.get(“fieldname”) and column.get(“options”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(column, dict) → column.get(“fieldtype”) equals “Link” → column.get(“fieldname”) → column.get(“options”).
- Set names\_by\_doctype from mapping().
- For each row in rows.
  - For each tuple(index, fieldname, doctype) in link\_columns.
    - If isinstance(row, dict).
      - Set name from row.get(fieldname).
    - Otherwise.
      - Set name from row at index when index &lt; len(row), otherwise no value.
        - Value choice on index &lt; len(row) — true gives row at index, false gives no value.
    - If name.
      - Evaluate names\_by\_doctype.setdefault(doctype, set()).add(name).
- Return names\_by\_doctype.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L787)

## Service · Linked with

<a id="op-f439a4266692ee"></a>
### Get submitted linked docs

`operation_foundation_desk_form_linked_with_business_behavior_get_submitted_linked_records`

**Inputs** doctype, name, ignore\_doctypes\_on\_cancel\_all = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at tuple.

**Explicit results** mapping(“docs” → docs, “count” → len(docs), “truncated” → truncated).

**Local steps**

- Evaluate Platform.has\_permission(doctype, doc = name, throw = true).
- Set tuple(docs, truncated) from collect\_cancellation\_blockers(doctype, name, ignore\_doctypes\_on\_cancel\_all, limit = MAX\_LINKED\_DOCUMENTS\_LISTED).
- Return mapping(“docs” → docs, “count” → len(docs), “truncated” → truncated).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L2625) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L210)

<a id="op-b5bd32368405bf"></a>
### Collect cancellation blockers

`operation_foundation_desk_form_linked_with_business_behavior_collect_cancellation_blockers`

**Inputs** doctype, name, ignore\_doctypes\_on\_cancel\_all = no value, limit = no value.

**Declared result** tuple at tuple(list, bool).

**Explicit results** tuple(list(), true) · tuple(docs, false).

**Local steps**

- Set ignore\_doctypes\_on\_cancel\_all from (Platform.parse\_json(ignore\_doctypes\_on\_cancel\_all) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(ignore\_doctypes\_on\_cancel\_all) → list().
- Set tree from SubmittableDocumentTree(doctype, name).
- Set visited\_documents from tree.get\_all\_children(ignore\_doctypes\_on\_cancel\_all, limit = limit).
- If tree.truncated.
  - Return tuple(list(), true).
- Set docs from list().
- For each tuple(dt, names) in visited\_documents.items().
  - Evaluate docs.extend(list of mapping(“doctype” → dt, “name” → docname, “docstatus” → 1) for docname drawn from names).
    - Draw docname from names.
- Evaluate docs.sort(key = deferred anonymous expression, reverse = true).
- Return tuple(docs, false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L2900) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L189)

<a id="op-6d7623aaca0072"></a>
### Submittable Document Tree.initialize

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_initialize`

**Inputs** self, doctype, name.

**Local steps**

- Set self.root\_doctype from doctype.
- Set self.root\_docname from name.
- Set self.to\_be\_visited\_documents from mapping(doctype → list(name)).
- Set self.visited\_documents from defaultdict(list).
- Set self.depth\_by\_document from mapping(tuple(doctype, name) → 0).
- Set self.truncated from false.
- Set self.fetch\_limit from no value.
- Set self.\_submittable\_doctypes from no value.
- Set self.\_references\_across\_doctypes from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L3382) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L224)

<a id="op-a9cd64d89cead9"></a>
### Submittable Document Tree.get all children

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_get_all_children`

**Inputs** self, ignore\_doctypes\_on\_cancel\_all, limit = no value.

**Explicit results** defaultdict(list) · self.visited\_documents.

**Local steps**

- Set self.fetch\_limit from (limit + 1) when limit, otherwise no value.
  - Value choice on limit — true gives (limit + 1), false gives no value.
- Set depth from 0.
- While self.to\_be\_visited\_documents.
  - Update depth using + 1.
  - Set current\_level from self.visit\_current\_level(ignore\_doctypes\_on\_cancel\_all).
  - Set next\_level\_children from defaultdict(list).
  - For each tuple(parent\_dt, parent\_docs) in current\_level.items().
    - Attempt the following.
      - Set child\_docs from self.get\_next\_level\_children(parent\_dt, parent\_docs).
    - On failure (LinkedDocumentsOverflow).
      - Set self.truncated from true.
      - Return defaultdict(list).
    - For each tuple(linked\_dt, linked\_names) in child\_docs.items().
      - Set new\_child\_docs from ((set(linked\_names) − set(self.visited\_documents.get(linked\_dt, list()))) − set(next\_level\_children at linked\_dt)).
      - Evaluate next\_level\_children at linked\_dt.extend(new\_child\_docs).
      - For each linked\_name in new\_child\_docs.
        - Set self.depth\_by\_document at tuple(linked\_dt, linked\_name) from depth.
  - Set self.to\_be\_visited\_documents from next\_level\_children.
  - If (limit and (len(self.depth\_by\_document) − 1) &gt; limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → (len(self.depth\_by\_document) − 1) &gt; limit.
    - Set self.truncated from true.
    - Return defaultdict(list).
- If self.root\_docname belongs to self.visited\_documents.get(self.root\_doctype, list()).
  - Evaluate self.visited\_documents at self.root\_doctype.remove(self.root\_docname).
- Return self.visited\_documents.

**Methods declared on this owner** [visit current level](operations-035.md#op-404ffb3f0cb26f), [get next level children](operations-035.md#op-b4d0e048769c41).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L61) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L218)

<a id="op-404ffb3f0cb26f"></a>
### Submittable Document Tree.visit current level

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_visit_current_level`

**Inputs** self, ignore\_doctypes\_on\_cancel\_all.

**Explicit results** current\_level.

**Local steps**

- Set current\_level from mapping().
- For each tuple(parent\_dt, parent\_docs) in self.to\_be\_visited\_documents.items().
  - If (not parent\_docs or (ignore\_doctypes\_on\_cancel\_all and parent\_dt belongs to ignore\_doctypes\_on\_cancel\_all)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent\_docs → (ignore\_doctypes\_on\_cancel\_all and parent\_dt belongs to ignore\_doctypes\_on\_cancel\_all).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_doctypes\_on\_cancel\_all → parent\_dt belongs to ignore\_doctypes\_on\_cancel\_all.
    - Continue with the next iteration or loop test.
  - Set current\_level at parent\_dt from parent\_docs.
  - Evaluate self.visited\_documents at parent\_dt.extend(parent\_docs).
- Return current\_level.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L4417) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L225)

<a id="op-b4d0e048769c41"></a>
### Submittable Document Tree.get next level children

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_get_next_level_children`

**Inputs** self, parent\_dt, parent\_names.

**Explicit results** child\_docs.

**Local steps**

- Set referencing\_fields from self.get\_doctype\_references(parent\_dt).
- Set child\_docs from defaultdict(list).
- For each field in referencing\_fields.
  - If field at “fieldname” equals “amended\_from”.
    - Continue with the next iteration or loop test.
  - Set links from (get\_referencing\_documents(parent\_dt, parent\_names.copy(), field, get\_parent\_if\_child\_table\_doc = true, parent\_filters = list(tuple(“docstatus”, “=”, 1)), allowed\_parents = self.get\_link\_sources(), limit = ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_referencing\_documents(parent\_dt, parent\_names.copy(), field, get\_parent\_if\_child\_table\_doc = true, parent\_filters = list(tuple(“docstatus”, “=”, 1)), allowed\_parents = self.get\_link\_sources(), limit =  … → mapping().
  - For each tuple(dt, names) in links.items().
    - Evaluate child\_docs at dt.extend(names).
- Return child\_docs.

**Methods declared on this owner** [get doctype references](operations-036.md#op-53ea6e704f16be), [get link sources](operations-036.md#op-50fe7d40cb8787).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L4617) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L221)
