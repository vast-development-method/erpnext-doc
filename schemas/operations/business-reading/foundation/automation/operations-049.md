# Workflow, automation and dispatch · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Socket

<a id="op-e41143301e98ff"></a>
### Sync Socket.has permission

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, name.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L3091) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L330)

<a id="op-42200e600376f7"></a>
### Sync Socket.run

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_run`

**Inputs** self, coro.

**State and service calls** call cancel on future.

**Explicit results** future.result(LOOP\_CALL\_TIMEOUT).

**Explicit failure paths** RuntimeError(“realtime event loop is closed”) · propagate active failure.

**Local steps**

- If self.\_loop.is\_closed().
  - Evaluate coro.close().
  - Raise RuntimeError(“realtime event loop is closed”).
- Set future from asyncio.run\_coroutine\_threadsafe(coro, self.\_loop).
- Attempt the following.
  - Return future.result(LOOP\_CALL\_TIMEOUT).
- On failure (TimeoutError).
  - Evaluate future.cancel().
  - Propagate the active failure.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L3209) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L337)

## Service · Store

<a id="op-0a9b26b8ee9264"></a>
### Db path

`operation_foundation_binding_foundation_flow_knowledge_store_db_path`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** os.path.join(\_test\_db\_path(), DB\_FILE) · Platform.get\_site\_path(“private”, DB\_FILE).

**Local steps**

- If Platform.flags.in\_test.
  - Return os.path.join(\_test\_db\_path(), DB\_FILE).
- Return Platform.get\_site\_path(“private”, DB\_FILE).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1220)

<a id="op-69d954bac95be5"></a>
### Test db path

`operation_foundation_binding_foundation_flow_knowledge_store_test_db_path`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** \_test\_db.

**Local steps**

- Use module bindings \_test\_db.
- If \_test\_db is identical to no value.
  - Set \_test\_db from tempfile.mkdtemp(prefix = “flow-search-”).
  - Evaluate atexit.register(shutil.rmtree, \_test\_db, ignore\_errors = true).
- Return \_test\_db.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1234)

<a id="op-eed4ebc484e23f"></a>
### Connect

`operation_foundation_binding_foundation_flow_knowledge_store_connect`

**Inputs** write = false.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set db from sqlite3.connect(db\_path(), timeout = 30).
- Attempt the following.
  - Evaluate db.enable\_load\_extension(true).
  - Evaluate sqlite\_vec.load(db).
  - Evaluate db.enable\_load\_extension(false).
  - Within db.
    - If write.
      - Evaluate db.execute(“begin immediate”).
    - yield db.
- On exit, including pending return or failure.
  - Evaluate db.close().

On ordinary fall-through the sequence ends.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L240) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1218)

<a id="op-a4020adc7a71d8"></a>
### Table exists

`operation_foundation_binding_foundation_flow_knowledge_store_table_exists`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** \_shape(db, TABLE\_NAME) is distinct from no value.

**Local steps**

- Within \_connect() bound as db.
  - Return \_shape(db, TABLE\_NAME) is distinct from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1257) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1233)

<a id="op-1429cf7696659c"></a>
### Table dimension

`operation_foundation_binding_foundation_flow_knowledge_store_table_dimension`

**Inputs** no declared parameters.

**Declared result** (int bitwise or no value).

**Explicit results** int(shape) when shape, otherwise no value.

**Local steps**

- Within \_connect() bound as db.
  - Set shape from \_shape(db, TABLE\_NAME).
- Return int(shape) when shape, otherwise no value.
  - Value choice on shape — true gives int(shape), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1232)

<a id="op-5c8b38c55d5950"></a>
### Ensure table for dimension

`operation_foundation_binding_foundation_flow_knowledge_store_ensure_table_for_dimension`

**Inputs** dimension.

**Declared result** no value.

**Explicit failure paths** ValueError(formatted text Invalid embedding dimension: {dimension}) · validation helper — translated “Knowledge store has dimension {0} but {1} was requested. Rebuild the knowledge store.”.format(existing, dimension).

**Local steps**

- If (not isinstance(dimension, int) or dimension &lt; 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(dimension, int) → dimension &lt; 1.
  - Raise ValueError(formatted text Invalid embedding dimension: {dimension}).
- Within \_connect(write = true) bound as db.
  - Set existing from \_shape(db, TABLE\_NAME).
  - If existing is identical to no value.
    - Evaluate \_create\_table(db, TABLE\_NAME, “id integer primary key, kb text, source text”, dimension).
    - Evaluate db.execute(formatted text create index {TABLE\_NAME}\_kb on {TABLE\_NAME}(kb)).
    - Evaluate db.execute(formatted text create index {TABLE\_NAME}\_source on {TABLE\_NAME}(source)).
  - Otherwise.
    - If int(existing) differs from dimension.
      - Call the validation error handler Platform.throw(translated “Knowledge store has dimension {0} but {1} was requested. Rebuild the knowledge store.”.format(existing, dimension), title = translated “Embedding Dimension Mismatch”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1224)

<a id="op-42db0211447365"></a>
### Add

`operation_foundation_binding_foundation_flow_knowledge_store_add`

**Inputs** rows.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Knowledge store is not initialized. Configure Flow Knowledge Settings and ingest a source.”.

**Local steps**

- If not rows.
  - Return no value.
- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is identical to no value.
    - Call the validation error handler Platform.throw(translated “Knowledge store is not initialized. Configure Flow Knowledge Settings and ingest a source.”, title = translated “Knowledge Store Not Ready”).
  - Evaluate db.executemany(formatted text delete from {TABLE\_NAME} where id = ?, list of tuple(row at “id”) for row drawn from rows).
    - Draw row from rows.
  - Evaluate db.executemany(formatted text insert into {TABLE\_NAME}(id, kb, source, content, vector) values (?, ?, ?, ?, ?), list of tuple(row at “id”, row at “kb”, row at “source”, row at “content”, …) for row drawn from rows).
    - Draw row from rows.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L239) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1217)

<a id="op-6f7c4ba5e3e392"></a>
### Delete

`operation_foundation_binding_foundation_flow_knowledge_store_delete`

**Inputs** kb (named only, default no value), source (named only, default no value), ids (named only, default no value).

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** ValueError(“delete() requires at least one of kb, source, ids”).

**Local steps**

- If (kb is identical to no value and source is identical to no value and ids is identical to no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kb is identical to no value → source is identical to no value → ids is identical to no value.
  - Raise ValueError(“delete() requires at least one of kb, source, ids”).
- Set tuple(conditions, values) from tuple(list(), list()).
- If kb is distinct from no value.
  - Evaluate conditions.append(“kb = ?”).
  - Evaluate values.append(kb).
- If source is distinct from no value.
  - Evaluate conditions.append(“source = ?”).
  - Evaluate values.append(source).
- If ids.
  - Evaluate conditions.append(“id = ?”).
- If not conditions.
  - Return no value.
- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is distinct from no value.
    - Evaluate db.executemany(formatted text delete from {TABLE\_NAME} where {“ and ”.join(conditions)}, list of tuple(expanded values, int(i)) for i drawn from ids when ids, otherwise list(values)).
      - Value choice on ids — true gives list of tuple(expanded values, int(i)) for i drawn from ids, false gives list(values).
      - Draw i from ids.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1221)

<a id="op-421120d968de0c"></a>
### Rename kb

`operation_foundation_binding_foundation_flow_knowledge_store_rename_kb`

**Inputs** old, new.

**Declared result** no value.

**Local steps**

- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is distinct from no value.
    - Evaluate db.execute(formatted text update {TABLE\_NAME} set kb = ? where kb = ?, tuple(new, old)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1252) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1228)

<a id="op-0b3eeaa6b3e55a"></a>
### Move source

`operation_foundation_binding_foundation_flow_knowledge_store_move_source`

**Inputs** source, kb.

**Declared result** no value.

**Local steps**

- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is distinct from no value.
    - Evaluate db.execute(formatted text update {TABLE\_NAME} set kb = ? where source = ?, tuple(kb, source)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1226)

<a id="op-bc16f89a8394ee"></a>
### Search

`operation_foundation_binding_foundation_flow_knowledge_store_search`

**Inputs** vector, text (named only, default no value), kbs (named only, default no value), limit (named only, default 5).

**Declared result** list at dict at tuple(str, Any).

**Explicit results** list() · list of mapping(“id” → id, “kb” → kb, “source” → source, “score” → score) for tuple(id, kb, source, score) drawn from hits.

**Local steps**

- Set limit from max(1, min(int(limit), MAX\_SEARCH\_LIMIT)).
- Set tuple(where, values) from tuple(“1”, list()).
- If kbs.
  - Set tuple(where, values) from tuple(formatted text kb in ({\_placeholders(kbs)}), list(kbs)).
- Within \_connect() bound as db.
  - If \_shape(db, TABLE\_NAME) is identical to no value.
    - Return list().
  - Set hits from \_search(db, TABLE\_NAME, “id, kb, source”, where, …).
- Return list of mapping(“id” → id, “kb” → kb, “source” → source, “score” → score) for tuple(id, kb, source, score) drawn from hits.
  - Draw tuple(id, kb, source, score) from hits.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1253) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1229)

<a id="op-ad5cb1cdaa1914"></a>
### Drop table

`operation_foundation_binding_foundation_flow_knowledge_store_drop_table`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Within \_connect(write = true) bound as db.
  - Evaluate \_drop\_table(db, TABLE\_NAME).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1222)

<a id="op-c4398367460ea3"></a>
### Search

`operation_foundation_binding_foundation_flow_knowledge_store_search_0570bbc4fcb9`

**Inputs** db, table, columns, where, values, vector, text, limit.

**Declared result** list at tuple.

**Explicit results** list of tuple(expanded rows at rowid, scores at rowid) for rowid drawn from best where rowid belongs to rows.

**Local steps**

- Set nearest from db.execute(formatted text select rowid, vec\_distance\_cosine(vector, ?) as distance from {table} where ({where}) and distance is not null order by distance limit ?, list(\_vector\_bytes(vector), expanded valu …().
- If text.
  - Set scores from defaultdict(float).
  - For each ranked\_rowids in tuple(list of rowid for tuple(rowid, \_) drawn from nearest, \_keyword\_search(db, table, where, values, …)).
    - Draw tuple(rowid, \_) from nearest.
    - For each tuple(rank, rowid) in enumerate(ranked\_rowids, 1).
      - Update scores at rowid using + (1 ÷ (RRF\_K + rank)).
- Otherwise.
  - Set scores from mapping of rowid → (1.0 − distance) for tuple(rowid, distance) drawn from nearest.
    - Draw tuple(rowid, distance) from nearest.
- Set best from sorted(scores, key = scores.get, reverse = true) at slice no value to limit.
- Set rows from mapping of row at 0 → row at slice 1 to no value for row drawn from db.execute(formatted text select rowid, {columns} from {table} where rowid in ({\_placeholders(best)}) and ({where}), list(expanded best,  ….
  - Draw row from db.execute(formatted text select rowid, {columns} from {table} where rowid in ({\_placeholders(best)}) and ({where}), list(expanded best, expanded values)).
- Return list of tuple(expanded rows at rowid, scores at rowid) for rowid drawn from best where rowid belongs to rows.
  - Draw rowid from best, keep a combination only if (rowid belongs to rows).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1254) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1230)

<a id="op-fccb08a1a2bc57"></a>
### Keyword search

`operation_foundation_binding_foundation_flow_knowledge_store_keyword_search`

**Inputs** db, table, where, values, text, limit, column = “rowid”.

**Declared result** list.

**Explicit results** list() · list of row at 0 for row drawn from db.execute(query, list(match, expanded values, limit)).

**Local steps**

- Set words from dict.fromkeys(re.findall(“&#91;^\\W\_&#93;+”, text.lower())).
- Set match from “ OR ”.join(generator of formatted text "{word}" for word drawn from words where word does not belong to STOP\_WORDS).
  - Draw word from words, keep a combination only if (word does not belong to STOP\_WORDS).
- If not match.
  - Return list().
- Set fts from formatted text {table}\_fts.
- Set query from formatted text select {table}.{column} from {fts} join {table} on {table}.rowid = {fts}.rowid where {fts} match ? and ({where}) order by {fts}.rank limit ?.
- Return list of row at 0 for row drawn from db.execute(query, list(match, expanded values, limit)).
  - Draw row from db.execute(query, list(match, expanded values, limit)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1225)

<a id="op-3883788af273b7"></a>
### Create table

`operation_foundation_binding_foundation_flow_knowledge_store_create_table`

**Inputs** db, table, columns, dimension, shape = no value.

**Declared result** no value.

**Local steps**

- Set size\_check from formatted text  check(length(vector) = {(int(dimension) × 4)}) when dimension, otherwise empty text.
  - Value choice on dimension — true gives formatted text  check(length(vector) = {(int(dimension) × 4)}), false gives empty text.
- Set fts from formatted text {table}\_fts.
- Set add\_to\_fts from formatted text insert into {fts}(rowid, content) values (new.rowid, new.content);.
- Set remove\_from\_fts from formatted text insert into {fts}({fts}, rowid, content) values ('delete', old.rowid, old.content);.
- For each statement in tuple(query text (CREATE), formatted text create table {table}({columns}, content text, vector blob{size\_check}), formatted text create virtual table {fts} using fts5(content, content='{table}', tokenize=' ….
  - Evaluate db.execute(statement).
- Evaluate db.execute(query text (INSERT), tuple(table, (shape or str(dimension)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in shape → str(dimension).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1219)

<a id="op-6c63042c43fcf9"></a>
### Drop table

`operation_foundation_binding_foundation_flow_knowledge_store_drop_table_787900180a55`

**Inputs** db, table.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If \_shape(db, table) is identical to no value.
  - Return no value.
- Evaluate db.execute(formatted text drop table {table}\_fts).
- Evaluate db.execute(formatted text drop table {table}).
- Evaluate db.execute(query text (DELETE), tuple(table)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1223)

<a id="op-e021d1d6d42acf"></a>
### Shape

`operation_foundation_binding_foundation_flow_knowledge_store_shape`

**Inputs** db, table.

**Declared result** (str bitwise or no value).

**Explicit results** no value · row at 0 when row, otherwise no value.

**Local steps**

- If not db.execute(query text (SELECT)).fetchone().
  - Return no value.
- Set row from db.execute(query text (SELECT), tuple(table)).fetchone().
- Return row at 0 when row, otherwise no value.
  - Value choice on row — true gives row at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1231)

<a id="op-5b74bbf39be1fa"></a>
### Vector bytes

`operation_foundation_binding_foundation_flow_knowledge_store_vector_bytes`

**Inputs** vector.

**Declared result** bytes.

**Explicit results** sqlite\_vec.serialize\_float32(vector).

**Local steps**

- Return sqlite\_vec.serialize\_float32(vector).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1235)

<a id="op-feefb1b6a97db5"></a>
### Placeholders

`operation_foundation_binding_foundation_flow_knowledge_store_placeholders`

**Inputs** values.

**Declared result** str.

**Explicit results** “, ”.join((“?” × len(values))).

**Local steps**

- Return “, ”.join((“?” × len(values))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1251) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1227)

<a id="op-5d161bbecc939c"></a>
### Sync

`operation_foundation_binding_foundation_flow_memory_store_sync`

**Inputs** doc.

**Declared result** no value.

**Local steps**

- Set dimension from ensure\_table().
- Set rows from \_rows(list(doc), dimension) when doc.status equals “Active”, otherwise list().
  - Value choice on doc.status equals “Active” — true gives \_rows(list(doc), dimension), false gives list().
- Within \_connect(write = true) bound as db.
  - Evaluate db.execute(formatted text delete from {TABLE\_NAME} where id = ?, tuple(doc.name)).
  - Evaluate \_insert(db, rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1331)

<a id="op-c46c06342b0469"></a>
### Remove

`operation_foundation_binding_foundation_flow_memory_store_remove`

**Inputs** name.

**Declared result** no value.

**Local steps**

- Attempt the following.
  - Within \_connect(write = true) bound as db.
    - If \_shape(db, TABLE\_NAME) is distinct from no value.
      - Evaluate db.execute(formatted text delete from {TABLE\_NAME} where id = ?, tuple(name)).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Agent memory index cleanup failed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1327)

<a id="op-91438c18bcfa22"></a>
### Rename agent

`operation_foundation_binding_foundation_flow_memory_store_rename_agent`

**Inputs** old, new.

**Declared result** no value.

**Local steps**

- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is distinct from no value.
    - Evaluate db.execute(formatted text update {TABLE\_NAME} set agent = ? where agent = ?, tuple(new, old)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1328)
