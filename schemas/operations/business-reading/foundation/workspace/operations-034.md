# Forms, reports and navigation · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Kanban board

[Record definition](../../../../data/record-types/kanban_board.json)

<a id="op-8dada4d6ed1013"></a>
### Default group by fieldnames

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_group_by_fieldnames`

**Inputs** doctype.

**Declared result** list at str.

**Explicit results** list of df.fieldname for df drawn from meta.fields where (df.fieldtype equals “Select” and not df.hidden).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Return list of df.fieldname for df drawn from meta.fields where (df.fieldtype equals “Select” and not df.hidden).
  - Draw df from meta.fields, keep a combination only if ((df.fieldtype equals “Select” and not df.hidden)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Select” → not df.hidden.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L232) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L690)

<a id="op-d3778d5ee5cadb"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L7220) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L809)

<a id="op-ec5819c7ecf9e5"></a>
### Has permission

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L7362) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L810)

<a id="op-d6b71b39be3a88"></a>
### Get kanban boards

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_boards`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Kanban Board” via get\_list.

**Explicit results** Platform.get\_list(“Kanban Board”, fields = list(“name”, “filters”, “reference\_doctype”, “private”, …), filters = mapping(“reference\_doctype” → doctype)).

**Local steps**

- Return Platform.get\_list(“Kanban Board”, fields = list(“name”, “filters”, “reference\_doctype”, “private”, …), filters = mapping(“reference\_doctype” → doctype)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L8) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L803)

<a id="op-c862de024b61fe"></a>
### Ensure kanban board permission

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_ensure_kanban_board_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** board, ptype.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L237) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L695)

<a id="op-b4dc66b84e6b88"></a>
### Get kanban reportview args

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_reportview_arguments`

**Inputs** no declared parameters.

**Explicit results** tuple(board\_name, column\_name, kanban\_start, kanban\_page\_length, …).

**Explicit failure paths** validation helper — translated “Board name is required”.

**Local steps**

- Bind dependencies clean\_params, validate\_args.
- Set data from Platform.\_dict(Platform.local.form\_dict).
- Set board\_name from data.pop(“board\_name”, no value).
- Set column\_name from data.pop(“column\_name”, no value).
- Set kanban\_start from cint(data.pop(“kanban\_start”, data.pop(“start”, 0))).
- Set kanban\_page\_length from (cint(data.pop(“kanban\_page\_length”, 50)) or 50).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(data.pop(“kanban\_page\_length”, 50)) → 50.
- If not board\_name.
  - Call the validation error handler Platform.throw(translated “Board name is required”, title = translated “Kanban Board”).
- Evaluate clean\_params(data).
- Evaluate validate\_args(data).
- Return tuple(board\_name, column\_name, kanban\_start, kanban\_page\_length, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L163) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L807)

<a id="op-5e4cd139cd09f1"></a>
### Get kanban board context

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_board_context`

**Inputs** board\_name.

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**Explicit results** tuple(board, column\_names).

**Local steps**

- Set board from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate ensure\_kanban\_board\_permission(board, “read”).
- Evaluate Platform.has\_permission(board.reference\_doctype, “read”, throw = true).
- Set column\_names from list of col.column\_name for col drawn from board.columns where col.status differs from “Archived”.
  - Draw col from board.columns, keep a combination only if (col.status differs from “Archived”).
- Return tuple(board, column\_names).

**Values supplied outside this operation** effective access from Platform.has\_permission(board.reference\_doctype, “read”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L7) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L801)

<a id="op-e0940a0f8ca690"></a>
### Merge kanban filters

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_merge_kanban_filters`

**Inputs** board, filters.

**Declared result** list.

**Explicit results** merged.

**Local steps**

- Set merged from list((filters or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- If not board.filters.
  - Return merged.
- Set board\_filters from Platform.parse\_json(board.filters).
- If not board\_filters.
  - Return merged.
- Set existing from set of \_kanban\_filter\_key(f) for f drawn from merged.
  - Draw f from merged.
- For each filt in board\_filters.
  - If \_kanban\_filter\_key(filt) does not belong to existing.
    - Evaluate merged.append(filt).
- Return merged.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L807) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L817)

<a id="op-8496a24492275a"></a>
### Kanban filter key

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_kanban_filter_key`

**Inputs** filt.

**Explicit results** tuple(generator of \_hashable(part) for part drawn from parts) · tuple(\_hashable(filt)).

**Local steps**

- Bind local operation \_hashable for subsequent calls.
- If isinstance(filt, tuple(list, tuple)).
  - Set parts from list(filt at slice no value to 4) when len(filt) ≥ 4, otherwise list(filt).
    - Value choice on len(filt) ≥ 4 — true gives list(filt at slice no value to 4), false gives list(filt).
  - Return tuple(generator of \_hashable(part) for part drawn from parts).
    - Draw part from parts.
- Return tuple(\_hashable(filt)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L1105) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L815)

<a id="op-a154ffb985d754"></a>
### Kanban filter key.hashable

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_kanban_filter_key_hashable`

**Inputs** value.

**Explicit results** tuple(value) · value.

**Local steps**

- If isinstance(value, list).
  - Return tuple(value).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L1402) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L816)

<a id="op-cffb5b95916b21"></a>
### Column filter

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_column_filter`

**Inputs** doctype, field\_name, column\_name, filters.

**Declared result** list.

**Explicit results** list(expanded (filters or list()), list(doctype, field\_name, “=”, column\_name)).

**Local steps**

- Return list(expanded (filters or list()), list(doctype, field\_name, “=”, column\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L1485) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L799)

<a id="op-2e142f686d715e"></a>
### Fetch kanban column cards

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_fetch_kanban_column_cards`

**Inputs** reportview\_args, doctype, field\_name, column\_name, start, page\_length.

**Explicit results** data.

**Local steps**

- Bind dependencies compress, execute, send\_compressed\_link\_titles.
- Set query\_args from Platform.\_dict(reportview\_args.copy()).
- Set query\_args.start from cint(start).
- Set query\_args.page\_length from cint(page\_length).
- Set query\_args.filters from column\_filter(doctype, field\_name, column\_name, query\_args.filters).
- Set data from compress(execute(expanded names query\_args), args = query\_args).
- Evaluate send\_compressed\_link\_titles(query\_args, data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L800)

<a id="op-b4d39f26d68a0a"></a>
### Get kanban column counts

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_column_counts`

**Inputs** doctype, field\_name, filters, column\_names.

**Declared result** dict at tuple(str, int).

**Record and data access** read doctype via get\_list · read doctype via count.

**Explicit results** counts.

**Local steps**

- Set counts from mapping of name → 0 for name drawn from column\_names.
  - Draw name from column\_names.
- If not column\_names.
  - Return counts.
- Attempt the following.
  - Set rows from Platform.get\_list(doctype, filters = filters, group\_by = field\_name, fields = list(formatted text {field\_name} as name, mapping(“COUNT” → “\*”, “as” → “\_count”)), order\_by = no value, …).
  - For each row in rows.
    - If row.name belongs to counts.
      - Set counts at row.name from cint(row.get(“\_count”, 0)).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Kanban column count group-by failed”, message = Platform.get\_traceback()).
  - For each column\_name in column\_names.
    - Set counts at column\_name from Platform.db.count(doctype, filters = column\_filter(doctype, field\_name, column\_name, filters)).
- Return counts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L1924) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L804)

<a id="op-0453897724342a"></a>
### Get kanban board data

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_board_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** mapping(“columns” → columns).

**Local steps**

- Set tuple(board\_name, \_, \_, kanban\_page\_length, …) from get\_kanban\_reportview\_args().
- Set tuple(board, column\_names) from get\_kanban\_board\_context(board\_name).
- Set doctype from board.reference\_doctype.
- Set field\_name from board.field\_name.
- Set filters from merge\_kanban\_filters(board, reportview\_args.filters).
- Set reportview\_args.filters from filters.
- Set counts from get\_kanban\_column\_counts(doctype, field\_name, filters, column\_names).
- Set columns from mapping().
- For each column\_name in column\_names.
  - Set cards from fetch\_kanban\_column\_cards(reportview\_args, doctype, field\_name, column\_name, …).
  - Set columns at column\_name from mapping(“total” → counts.get(column\_name, 0), “cards” → cards).
- Return mapping(“columns” → columns).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L2481) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L802)

<a id="op-06b80c82bb8489"></a>
### Validate kanban group by

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_validate_kanban_group_by`

**Inputs** board, group\_by.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Invalid group field”.

**Local steps**

- If group\_by equals “\_assign”.
  - If not cint(board.show\_assigned\_to, 1).
    - Call the validation error handler Platform.throw(translated “Invalid group field”, title = translated “Kanban Board”).
  - Return no value.
- Set allowed from set of row.fieldname for row drawn from (board.group\_by\_fields or list()) where row.fieldname.
  - Draw row from (board.group\_by\_fields or list()), keep a combination only if (row.fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in board.group\_by\_fields → list().
- If (group\_by does not belong to allowed or not Platform.get\_meta(board.reference\_doctype).get\_field(group\_by)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_by does not belong to allowed → not Platform.get\_meta(board.reference\_doctype).get\_field(group\_by).
  - Call the validation error handler Platform.throw(translated “Invalid group field”, title = translated “Kanban Board”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L253) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L711)

<a id="op-32a1193cdfa04b"></a>
### Get kanban group values

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_get_kanban_group_values`

**Inputs** board\_name, group\_by, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Record and data access** read doctype via get\_list.

**Explicit results** mapping(“lanes” → lanes, “unset” → unset).

**Local steps**

- Bind dependencies Counter.
- Set tuple(board, \_) from get\_kanban\_board\_context(board\_name).
- Set doctype from board.reference\_doctype.
- Evaluate validate\_kanban\_group\_by(board, group\_by).
- Set merged from merge\_kanban\_filters(board, Platform.parse\_json(filters) when filters, otherwise no value).
  - Value choice on filters — true gives Platform.parse\_json(filters), false gives no value.
- Set limit from 20.
- Set lanes from list().
- Set unset from 0.
- If group\_by equals “\_assign”.
  - Set counter from Counter().
  - Set assign\_scan\_limit from 5000.
  - For each raw in Platform.get\_list(doctype, filters = merged, pluck = “\_assign”, limit = assign\_scan\_limit).
    - Set users from Platform.parse\_json(raw) when raw, otherwise list().
      - Value choice on raw — true gives Platform.parse\_json(raw), false gives list().
    - If users.
      - For each user in users.
        - Update counter at user using + 1.
    - Otherwise.
      - Update unset using + 1.
  - Set lanes from list of mapping(“value” → user, “label” → user, “count” → count) for tuple(user, count) drawn from counter.most\_common(limit).
    - Draw tuple(user, count) from counter.most\_common(limit).
- Otherwise.
  - Set rows from Platform.get\_list(doctype, filters = merged, fields = list(formatted text {group\_by} as value, mapping(“COUNT” → “\*”, “as” → “\_count”)), group\_by = group\_by, order\_by = “\_count desc”, …).
  - For each row in rows.
    - Set value from row.get(“value”).
    - Set count from cint(row.get(“\_count”)).
    - If value belongs to tuple(no value, empty text).
      - Update unset using + count.
    - Otherwise.
      - Evaluate lanes.append(mapping(“value” → value, “label” → value, “count” → count)).
  - Set lanes from lanes at slice no value to limit.
  - Evaluate set\_link\_lane\_labels(doctype, group\_by, lanes).
- Return mapping(“lanes” → lanes, “unset” → unset).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L238) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L696)

<a id="op-e65c38f45736c6"></a>
### Set link lane labels

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_set_link_lane_labels`

**Inputs** doctype, group\_by, lanes.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_link\_title\_field, get\_link\_titles.
- Set df from Platform.get\_meta(doctype).get\_field(group\_by).
- If (not lanes or df.fieldtype differs from “Link”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not lanes → df.fieldtype differs from “Link”.
  - Return no value.
- Set title\_field from get\_link\_title\_field(df.options).
- If not title\_field.
  - Return no value.
- Set titles from get\_link\_titles(df.options, title\_field, set of lane at “value” for lane drawn from lanes).
  - Draw lane from lanes.
- For each lane in lanes.
  - Set lane at “label” from (titles.get(lane at “value”) or lane at “value”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in titles.get(lane at “value”) → lane at “value”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L252) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L710)

<a id="op-76691993f273ce"></a>
### Get kanban column page

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_column_page`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Record and data access** read doctype via count.

**Explicit results** mapping(“total” → total, “cards” → cards).

**Explicit failure paths** validation helper — translated “Column name is required” · validation helper — translated “Invalid column”.

**Local steps**

- Set tuple(board\_name, column\_name, kanban\_start, kanban\_page\_length, …) from get\_kanban\_reportview\_args().
- If not column\_name.
  - Call the validation error handler Platform.throw(translated “Column name is required”, title = translated “Kanban Board”).
- Set tuple(board, column\_names) from get\_kanban\_board\_context(board\_name).
- If column\_name does not belong to column\_names.
  - Call the validation error handler Platform.throw(translated “Invalid column”, title = translated “Kanban Board”).
- Set doctype from board.reference\_doctype.
- Set field\_name from board.field\_name.
- Set filters from merge\_kanban\_filters(board, reportview\_args.filters).
- Set reportview\_args.filters from filters.
- Set col\_filters from column\_filter(doctype, field\_name, column\_name, filters).
- Set cards from fetch\_kanban\_column\_cards(reportview\_args, doctype, field\_name, column\_name, …).
- Set total from Platform.db.count(doctype, filters = col\_filters).
- Return mapping(“total” → total, “cards” → cards).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L2916) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L806)

<a id="op-eed434fa1df96e"></a>
### Add column

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_add_column`

**Inputs** board\_name, column\_title.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.columns.

**Explicit failure paths** validation helper — translated “Column &lt;b&gt;{0}&lt;/b&gt; already exist.”.format(column\_title).

**Local steps**

- Set doc from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate doc.check\_permission(“write”).
- For each col in doc.columns.
  - If column\_title equals col.column\_name.
    - Call the validation error handler Platform.throw(translated “Column &lt;b&gt;{0}&lt;/b&gt; already exist.”.format(column\_title)).
- Evaluate doc.append(“columns”, dict(column\_name = column\_title)).
- Evaluate doc.save().
- Return doc.columns.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L3479) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L797)

<a id="op-450a431bea4a7f"></a>
### Archive restore column

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_archive_restore_column`

**Inputs** board\_name, column\_title, status.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.columns.

**Local steps**

- Set doc from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate doc.check\_permission(“write”).
- For each col in doc.columns.
  - If column\_title equals col.column\_name.
    - Set col.status from status.
- Evaluate doc.save().
- Return doc.columns.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L3790) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L798)

<a id="op-0c53bef73acb9e"></a>
### Update order

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_update_order`

**Inputs** board\_name, order.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc · read doctype via get\_value.

**State and service calls** call save on board.

**Explicit results** tuple(board, list()) · tuple(saved, list()).

**Local steps**

- Set board from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate board.check\_permission(“read”).
- Set doctype from board.reference\_doctype.
- If not Platform.has\_permission(doctype, “write”).
  - Return tuple(board, list()).
- Set fieldname from board.field\_name.
- Set order\_dict from Platform.parse\_json(order).
- For each tuple(col\_name, cards) in order\_dict.items().
  - Set valid\_cards from list of card for card drawn from cards where Platform.db.get\_value(doctype, card, fieldname) equals col\_name.
    - Draw card from cards, keep a combination only if (Platform.db.get\_value(doctype, card, fieldname) equals col\_name).
  - For each column in board.columns.
    - If column.column\_name equals col\_name.
      - Set column.order from json.dumps(valid\_cards).
- Set saved from board.save(ignore\_permissions = true).
- Evaluate publish\_kanban\_board\_update(saved).
- Return tuple(saved, list()).

**Values supplied outside this operation** effective access from board.check\_permission(“read”), Platform.has\_permission(doctype, “write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L13) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L823)

<a id="op-9083fd342d80d2"></a>
### Update order for single card

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_update_order_for_single_card`

**Inputs** board\_name, docname, from\_colname, to\_colname, old\_index = no value, new\_index = no value, from\_order = no value, to\_order = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Kanban Board” via get\_doc.

**State and service calls** call insert on to\_col\_order · call save on board.

**Explicit results** saved.

**Local steps**

- Set board from Platform.get\_doc(“Kanban Board”, board\_name).
- Evaluate board.check\_permission(“read”).
- Set doctype from board.reference\_doctype.
- Evaluate Platform.has\_permission(doctype, “write”, throw = true).
- Set fieldname from board.field\_name.
- Set tuple(from\_col\_order, from\_col\_idx) from get\_kanban\_column\_order\_and\_index(board, from\_colname).
- Set tuple(to\_col\_order, to\_col\_idx) from get\_kanban\_column\_order\_and\_index(board, to\_colname).
- If (from\_order is distinct from no value and to\_order is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_order is distinct from no value → to\_order is distinct from no value.
  - Set from\_col\_order from Platform.parse\_json(from\_order).
  - Set to\_col\_order from Platform.parse\_json(to\_order).
- Otherwise.
  - Set old\_index from Platform.parse\_json(old\_index).
  - Set new\_index from Platform.parse\_json(new\_index).
  - If from\_colname equals to\_colname.
    - Set from\_col\_order from to\_col\_order.
  - If from\_col\_order.
    - Evaluate to\_col\_order.insert(new\_index, from\_col\_order.pop(old\_index)).
- Set board.columns at from\_col\_idx.order from Platform.as\_json(from\_col\_order).
- Set board.columns at to\_col\_idx.order from Platform.as\_json(to\_col\_order).
- Set saved from board.save(ignore\_permissions = true).
- Evaluate publish\_kanban\_board\_update(saved).
- Evaluate Platform.set\_value(doctype, docname, fieldname, to\_colname).
- Return saved.

**Values supplied outside this operation** effective access from board.check\_permission(“read”), Platform.has\_permission(doctype, “write”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L4665) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L824)

<a id="op-18ab001ef472b3"></a>
### Get kanban column order and index

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_get_kanban_column_order_and_index`

**Inputs** board, colname.

**Explicit results** tuple(Platform.parse\_json(col.order), i).

**Explicit failure paths** validation helper — translated “Invalid column”.

**Local steps**

- For each tuple(i, col) in enumerate(board.columns).
  - If col.column\_name equals colname.
    - Return tuple(Platform.parse\_json(col.order), i).
- Call the validation error handler Platform.throw(translated “Invalid column”, title = translated “Kanban Board”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L9) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L805)

<a id="op-f4f8a63d8a69bf"></a>
### Publish kanban board update

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_publish_kanban_board_update`

**Inputs** board.

**State and service calls** publish realtime with “kanban\_board\_update”.

**Local steps**

- Evaluate Platform.publish\_realtime(“kanban\_board\_update”, mapping(“board\_name” → board.name, “reference\_doctype” → board.reference\_doctype), doctype = board.reference\_doctype, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“kanban\_board\_update”, mapping(“board\_name” → board.name, “reference\_doctype” → board.reference\_doctype), doctype = board.reference\_doctype, after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0174.json#L5712) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L818)
