# Workflow, automation and dispatch · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Handlers

<a id="op-5ed4764ea22673"></a>
### Doc close

`operation_foundation_realtime_handlers_business_behavior_record_close`

**Inputs** socket, doctype, docname.

**Wrappers, in declaration order** realtime.on(“doc\_close”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.leave(open\_doc\_room(doctype, docname)).
- Set tracked from socket.get(“subscribed\_documents”, list()).
- Set tracked from list of pair for pair drawn from tracked where not (pair at 0 equals doctype and pair at 1 equals docname).
  - Draw pair from tracked, keep a combination only if (not (pair at 0 equals doctype and pair at 1 equals docname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pair at 0 equals doctype → pair at 1 equals docname.
- Evaluate await socket.set(“subscribed\_documents”, tracked).
- Evaluate await notify\_doc\_viewers(socket, doctype, docname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.leave(open\_doc\_room(doctype, docname)), socket.get(“subscribed\_documents”, list()) and 1 further calls.

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L4225) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L261)

<a id="op-88befcae6f6602"></a>
### On disconnect

`operation_foundation_realtime_handlers_business_behavior_on_disconnect`

**Inputs** socket.

**Wrappers, in declaration order** realtime.on(“disconnect”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- For each tuple(doctype, docname) in socket.get(“subscribed\_documents”, list()).
  - Evaluate await notify\_doc\_viewers(socket, doctype, docname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.get(“subscribed\_documents”, list()).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L4554) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L256)

<a id="op-09c6a8a2fdb1c1"></a>
### Notify doc viewers

`operation_foundation_realtime_handlers_business_behavior_notify_record_viewers`

**Inputs** socket, doctype, docname.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not (doctype and docname).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → docname.
  - Return no value.
- Set room from open\_doc\_room(doctype, docname).
- Set users from list().
- For each sid in socket.participants(room).
  - Set user from await socket.user\_of(sid).
  - If user.
    - Evaluate users.append(user).
- If (len(users) equals 1 and users at 0 equals socket.user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(users) equals 1 → users at 0 equals socket.user.
  - Return no value.
- Evaluate await socket.emit(“doc\_viewers”, mapping(“doctype” → doctype, “docname” → docname, “users” → list(dict.fromkeys(users))), room = room).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.participants(room), socket.user\_of(sid) and 1 further calls.

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L4703) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L254)

<a id="op-73f773f4b691fc"></a>
### Open in editor

`operation_foundation_realtime_handlers_business_behavior_open_in_editor`

**Inputs** socket, data.

**Wrappers, in declaration order** realtime.on(“open\_in\_editor”).

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set config from get\_config().
- If not config.developer\_mode.
  - Return no value.
- Set client from redis.asyncio.from\_url(config.redis\_queue).
- Attempt the following.
  - Evaluate await client.publish(“open\_in\_editor”, json.dumps(data)).
- On exit, including pending return or failure.
  - Evaluate await client.aclose().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L5124) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L257)

## Service · Ingest

<a id="op-8e8b0f169703ee"></a>
### Enqueue ingestion

`operation_foundation_binding_foundation_flow_knowledge_ingest_enqueue_ingestion`

**Inputs** source, rebuild = false.

**Declared result** no value.

**State and service calls** enqueue with “Platform.flow.knowledge.ingest.ingest\_source”.

**Local steps**

- Evaluate Platform.enqueue(“Platform.flow.knowledge.ingest.ingest\_source”, queue = “long”, enqueue\_after\_commit = true, source = source, rebuild = rebuild).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.flow.knowledge.ingest.ingest\_source”, queue = “long”, enqueue\_after\_commit = true, source = source, rebuild = rebuild).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1188)

<a id="op-9993718fd9c549"></a>
### Sync due sources

`operation_foundation_binding_foundation_flow_knowledge_ingest_sync_due_sources`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read CHUNK\_DOCTYPE via exists · read “Flow Knowledge Source” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies store.
- If (not store.table\_exists() and Platform.db.exists(CHUNK\_DOCTYPE, mapping())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not store.table\_exists() → Platform.db.exists(CHUNK\_DOCTYPE, mapping()).
  - For each source in Platform.get\_all(“Flow Knowledge Source”, pluck = “name”).
    - Evaluate enqueue\_ingestion(source, rebuild = true).
  - Return no value.
- Set sources from Platform.get\_all(“Flow Knowledge Source”, filters = mapping(“source\_type” → “DocType”, “auto\_sync” → 1), pluck = “name”).
- For each source in sources.
  - Evaluate enqueue\_ingestion(source).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L223) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1201)

<a id="op-94836882269353"></a>
### Enqueue reconciliation

`operation_foundation_binding_foundation_flow_knowledge_ingest_enqueue_reconciliation`

**Inputs** source.

**Declared result** no value.

**State and service calls** enqueue with “Platform.flow.knowledge.ingest.reconcile\_source”.

**Local steps**

- Evaluate Platform.enqueue(“Platform.flow.knowledge.ingest.reconcile\_source”, queue = “long”, enqueue\_after\_commit = true, source = source).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.flow.knowledge.ingest.reconcile\_source”, queue = “long”, enqueue\_after\_commit = true, source = source).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1189)

<a id="op-9050a30eca1262"></a>
### Ingest source

`operation_foundation_binding_foundation_flow_knowledge_ingest_ingest_source`

**Inputs** source, rebuild = false.

**Declared result** no value.

**Local steps**

- Bind dependencies get\_queues\_timeout.
- Bind dependencies filelock.
- Within filelock(formatted text flow\_knowledge\_source\_{source}, timeout = get\_queues\_timeout() at “long”).
  - Evaluate \_ingest\_source(source, rebuild).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1192)

<a id="op-99bbf050d0f7c8"></a>
### Ingest source

`operation_foundation_binding_foundation_flow_knowledge_ingest_ingest_source_5236fd19e4d4`

**Inputs** source, rebuild.

**Declared result** no value.

**Record and data access** resolve a document from “Flow Knowledge Source” via get\_doc · resolve a document from “Flow Knowledge Settings” via get\_cached\_doc · read CHUNK\_DOCTYPE via count.

**State and service calls** call db\_set on doc · commit · rollback.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set doc from Platform.get\_doc(“Flow Knowledge Source”, source).
- Evaluate doc.db\_set(“status”, “Processing”, update\_modified = false).
- Evaluate Platform.db.commit().
- Attempt the following.
  - Set settings from Platform.get\_cached\_doc(“Flow Knowledge Settings”).
  - If doc.source\_type equals “DocType”.
    - If rebuild.
      - Evaluate purge\_source(doc.name).
      - Evaluate doc.db\_set(“last\_synced\_at”, no value, update\_modified = false).
      - Evaluate Platform.db.commit().
    - Evaluate \_sync\_doctype(doc, settings).
  - Otherwise.
    - Evaluate \_rebuild\_single(doc, settings).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate \_mark\_failed(source).
  - Propagate the active failure.
- Set count from Platform.db.count(CHUNK\_DOCTYPE, mapping(“source” → doc.name)).
- Evaluate doc.db\_set(mapping(“status” → “Completed”, “chunk\_count” → count, “error\_log” → no value), update\_modified = false).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Flow Knowledge Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1193)

<a id="op-6148b99142fd55"></a>
### Purge source

`operation_foundation_binding_foundation_flow_knowledge_ingest_purge_source`

**Inputs** source.

**Declared result** no value.

**State and service calls** request delete on CHUNK\_DOCTYPE.

**Local steps**

- Bind dependencies store.
- Evaluate store.delete(source = source).
- Evaluate Platform.db.delete(CHUNK\_DOCTYPE, mapping(“source” → source)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L218) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1196)

<a id="op-6b53df02cc8aa6"></a>
### Rebuild single

`operation_foundation_binding_foundation_flow_knowledge_ingest_rebuild_single`

**Inputs** doc, settings.

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → CHUNK\_DOCTYPE, “knowledge\_base” → doc.knowledge\_base, “source” → doc.name, “chunk\_index” → index, …) via get\_doc.

**State and service calls** commit · call insert on Platform.get\_doc(mapping(“doctype” → CHUNK\_DOCTYPE, “knowledge\_base” → doc.knowledge\_base, “source” → doc.name, “chunk\_index” → index, …)).

**Explicit results** no value.

**Local steps**

- Bind dependencies store.
- Bind dependencies chunk\_text.
- Bind dependencies embed\_texts.
- Bind dependencies extract.
- Set tuple(size, overlap) from \_chunk\_params(doc, settings).
- Set pieces from list().
- For each extracted in extract(doc).
  - Evaluate pieces.extend(chunk\_text(extracted.text, chunk\_size = size, overlap = overlap)).
- Set vectors from embed\_texts(pieces).
- Evaluate purge\_source(doc.name).
- Evaluate Platform.db.commit().
- If not pieces.
  - Return no value.
- Evaluate store.ensure\_table\_for\_dimension(cint(settings.embedding\_dimension)).
- Set rows from list().
- For each tuple(index, tuple(piece, vector)) in enumerate(zip(pieces, vectors, strict = true)).
  - Set chunk\_doc from Platform.get\_doc(mapping(“doctype” → CHUNK\_DOCTYPE, “knowledge\_base” → doc.knowledge\_base, “source” → doc.name, “chunk\_index” → index, …)).insert(ignore\_permissions = true).
  - Evaluate rows.append(mapping(“id” → int(chunk\_doc.name), “kb” → doc.knowledge\_base, “source” → doc.name, “content” → piece, …)).
- Evaluate store.add(rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1197)

<a id="op-c4904d4b5fcbe9"></a>
### Sync doctype

`operation_foundation_binding_foundation_flow_knowledge_ingest_sync_doctype`

**Inputs** doc, settings.

**Declared result** no value.

**Record and data access** read CHUNK\_DOCTYPE via exists · read ref via get\_all · read CHUNK\_DOCTYPE via get\_all.

**State and service calls** commit · call db\_set on doc.

**Local steps**

- Bind dependencies \_parse\_filters, resolve\_content\_fields.
- Set ref from doc.reference\_doctype.
- Set meta from Platform.get\_meta(ref).
- Set fields from resolve\_content\_fields(meta, doc.content\_fields).
- Set user\_filters from \_parse\_filters(doc.filters).
- Set watermark from doc.last\_synced\_at.
- Set sweep\_start from now\_datetime().
- Set first\_run from not watermark.
- Set retried\_first\_run from (first\_run and bool(Platform.db.exists(CHUNK\_DOCTYPE, mapping(“source” → doc.name)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in first\_run → bool(Platform.db.exists(CHUNK\_DOCTYPE, mapping(“source” → doc.name))).
- Set filters from list of make\_filter\_tuple(ref, key, value) for tuple(key, value) drawn from user\_filters.items().
  - Draw tuple(key, value) from user\_filters.items().
- If not first\_run.
  - Evaluate filters.append(list(ref, “modified”, “&gt;”, watermark)).
- Set matched\_refs from set().
- Set last from no value.
- While true.
  - Set after from list(list(ref, “name”, “&gt;”, last)) when last is distinct from no value, otherwise list().
    - Value choice on last is distinct from no value — true gives list(list(ref, “name”, “&gt;”, last)), false gives list().
  - Set page from Platform.get\_all(ref, filters = (filters + after), fields = list(“name”, expanded fields), order\_by = “name asc”, limit\_page\_length = BATCH).
  - If not page.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate \_upsert\_page(doc, settings, meta, fields, track\_exits = (not first\_run or retried\_first\_run), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not first\_run → retried\_first\_run.
  - Evaluate Platform.db.commit().
  - Set last from page at negative 1 at “name”.
  - If len(page) &lt; BATCH.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If retried\_first\_run.
  - Set matched from set of str(name) for name drawn from matched\_refs.
    - Draw name from matched\_refs.
  - Set indexed from Platform.get\_all(CHUNK\_DOCTYPE, mapping(“source” → doc.name), pluck = “reference\_name”, distinct = true).
  - Evaluate \_purge\_refs(doc.name, list of name for name drawn from indexed where name does not belong to matched).
    - Draw name from indexed, keep a combination only if (name does not belong to matched).
- Otherwise.
  - If not first\_run.
    - Evaluate \_remove\_stale(doc, ref, watermark, matched\_refs).
- Evaluate doc.db\_set(“last\_synced\_at”, sweep\_start, update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L222) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1200)

<a id="op-0cc4a8a75a51a9"></a>
### Upsert page

`operation_foundation_binding_foundation_flow_knowledge_ingest_upsert_page`

**Inputs** doc, settings, meta, fields, page, matched\_refs, track\_exits (named only).

**Declared result** no value.

**Local steps**

- Bind dependencies \_row\_to\_text.
- Set to\_embed from list().
- Set stale from list().
- For each row in page.
  - Set name from row at “name”.
  - If track\_exits.
    - Evaluate matched\_refs.add(name).
  - Set existing from \_existing\_chunk\_state(doc.name, name).
  - Set text from \_row\_to\_text(row, fields, meta).
  - If not text.
    - If existing at “ids”.
      - Evaluate stale.append(name).
    - Continue with the next iteration or loop test.
  - Set new\_hash from \_content\_hash(text).
  - If existing at “hash” equals new\_hash.
    - Continue with the next iteration or loop test.
  - If existing at “ids”.
    - Evaluate stale.append(name).
  - Set pieces from \_chunk(text, doc, settings).
  - If pieces.
    - Evaluate to\_embed.append(tuple(name, new\_hash, pieces)).
- If stale.
  - Evaluate \_purge\_refs(doc.name, stale).
- If to\_embed.
  - Evaluate \_embed\_and\_insert(doc, settings, to\_embed).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L224) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1202)

<a id="op-86b350541be4d8"></a>
### Embed and insert

`operation_foundation_binding_foundation_flow_knowledge_ingest_embed_and_insert`

**Inputs** doc, settings, to\_embed.

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → CHUNK\_DOCTYPE, “knowledge\_base” → doc.knowledge\_base, “source” → doc.name, “chunk\_index” → index, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → CHUNK\_DOCTYPE, “knowledge\_base” → doc.knowledge\_base, “source” → doc.name, “chunk\_index” → index, …)).

**Local steps**

- Bind dependencies store.
- Bind dependencies embed\_texts.
- Set all\_pieces from list().
- For each tuple(\_, \_, pieces) in to\_embed.
  - Evaluate all\_pieces.extend(pieces).
- Set vectors from embed\_texts(all\_pieces).
- Evaluate store.ensure\_table\_for\_dimension(cint(settings.embedding\_dimension)).
- Set rows from list().
- Set cursor from 0.
- For each tuple(reference\_name, content\_hash, pieces) in to\_embed.
  - For each tuple(index, piece) in enumerate(pieces).
    - Set vector from vectors at cursor.
    - Update cursor using + 1.
    - Set chunk\_doc from Platform.get\_doc(mapping(“doctype” → CHUNK\_DOCTYPE, “knowledge\_base” → doc.knowledge\_base, “source” → doc.name, “chunk\_index” → index, …)).insert(ignore\_permissions = true).
    - Evaluate rows.append(mapping(“id” → int(chunk\_doc.name), “kb” → doc.knowledge\_base, “source” → doc.name, “content” → piece, …)).
- Evaluate store.add(rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L209) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1187)

<a id="op-c6523b2076a948"></a>
### Remove stale

`operation_foundation_binding_foundation_flow_knowledge_ingest_remove_stale`

**Inputs** doc, ref, watermark, matched\_refs.

**Declared result** no value.

**Record and data access** read ref via get\_all · read “Deleted Document” via get\_all.

**Local steps**

- Set touched from set of row at “name” for row drawn from Platform.get\_all(ref, filters = mapping(“modified” → list(“&gt;”, watermark)), fields = list(“name”)).
  - Draw row from Platform.get\_all(ref, filters = mapping(“modified” → list(“&gt;”, watermark)), fields = list(“name”)).
- Set exits from (touched − matched\_refs).
- Set deleted from set(Platform.get\_all(“Deleted Document”, filters = mapping(“deleted\_doctype” → ref, “creation” → list(“&gt;”, watermark)), pluck = “deleted\_name”)).
- Set to\_remove from (exits bitwise or deleted).
- If to\_remove.
  - Evaluate \_purge\_refs(doc.name, list(to\_remove)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L221) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1199)

<a id="op-c0ff1ea1ec07fe"></a>
### Existing chunk state

`operation_foundation_binding_foundation_flow_knowledge_ingest_existing_chunk_state`

**Inputs** source, reference\_name.

**Declared result** dict.

**Record and data access** read CHUNK\_DOCTYPE via get\_all.

**Explicit results** mapping(“ids” → list of int(r at “name”) for r drawn from rows, “hash” → rows at 0 at “content\_hash” when rows, otherwise no value).

**Local steps**

- Set rows from Platform.get\_all(CHUNK\_DOCTYPE, filters = mapping(“source” → source, “reference\_name” → reference\_name), fields = list(“name”, “content\_hash”)).
- Return mapping(“ids” → list of int(r at “name”) for r drawn from rows, “hash” → rows at 0 at “content\_hash” when rows, otherwise no value).
  - Draw r from rows.
  - Value choice on rows — true gives rows at 0 at “content\_hash”, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1190)

<a id="op-6468d598c1ef3a"></a>
### Purge refs

`operation_foundation_binding_foundation_flow_knowledge_ingest_purge_refs`

**Inputs** source, reference\_names.

**Declared result** no value.

**Record and data access** read CHUNK\_DOCTYPE via get\_all.

**State and service calls** request delete on CHUNK\_DOCTYPE.

**Local steps**

- Bind dependencies store.
- For each start in range(0, len(reference\_names), BATCH).
  - Set criterion from mapping(“source” → source, “reference\_name” → list(“in”, reference\_names at slice start to (start + BATCH))).
  - Set ids from list of int(name) for name drawn from Platform.get\_all(CHUNK\_DOCTYPE, filters = criterion, pluck = “name”).
    - Draw name from Platform.get\_all(CHUNK\_DOCTYPE, filters = criterion, pluck = “name”).
  - If ids.
    - Evaluate store.delete(ids = ids).
    - Evaluate Platform.db.delete(CHUNK\_DOCTYPE, criterion).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L217) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1195)

<a id="op-3dcb6279bbf6b4"></a>
### Reconcile source

`operation_foundation_binding_foundation_flow_knowledge_ingest_reconcile_source`

**Inputs** source.

**Declared result** no value.

**Record and data access** resolve a document from “Flow Knowledge Source” via get\_doc · read CHUNK\_DOCTYPE via get\_all · read CHUNK\_DOCTYPE via count.

**State and service calls** call db\_set on doc.

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(“Flow Knowledge Source”, source).
- If doc.source\_type differs from “DocType”.
  - Return no value.
- Set indexed from set(Platform.get\_all(CHUNK\_DOCTYPE, filters = mapping(“source” → source), pluck = “reference\_name”, distinct = true)).
- Evaluate indexed.discard(no value).
- If not indexed.
  - Return no value.
- Set orphaned from list((indexed − \_existing\_names(doc.reference\_doctype, indexed))).
- If orphaned.
  - Evaluate \_purge\_refs(source, orphaned).
  - Set count from Platform.db.count(CHUNK\_DOCTYPE, mapping(“source” → source)).
  - Evaluate doc.db\_set(“chunk\_count”, count, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1198)

<a id="op-e143ff099a3589"></a>
### Existing names

`operation_foundation_binding_foundation_flow_knowledge_ingest_existing_names`

**Inputs** doctype, names.

**Declared result** set at str.

**Record and data access** read doctype via get\_all.

**Explicit results** found.

**Local steps**

- Set found from set().
- Set ordered from list(names).
- For each start in range(0, len(ordered), BATCH).
  - Set batch from ordered at slice start to (start + BATCH).
  - Evaluate found.update(Platform.get\_all(doctype, filters = mapping(“name” → list(“in”, batch)), pluck = “name”)).
- Return found.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1191)

<a id="op-cc670ef006281f"></a>
### Chunk

`operation_foundation_binding_foundation_flow_knowledge_ingest_chunk`

**Inputs** text, doc, settings.

**Declared result** list at str.

**Explicit results** chunk\_text(text, chunk\_size = size, overlap = overlap).

**Local steps**

- Bind dependencies chunk\_text.
- Set tuple(size, overlap) from \_chunk\_params(doc, settings).
- Return chunk\_text(text, chunk\_size = size, overlap = overlap).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1184)

<a id="op-32afd7163a8678"></a>
### Chunk params

`operation_foundation_binding_foundation_flow_knowledge_ingest_chunk_params`

**Inputs** doc, settings.

**Declared result** tuple at tuple(int, int).

**Explicit results** tuple(size, overlap).

**Local steps**

- Set size from (cint(doc.chunk\_size) or cint(settings.chunk\_size)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(doc.chunk\_size) → cint(settings.chunk\_size).
- Set overlap from (cint(doc.chunk\_overlap) or cint(settings.chunk\_overlap)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(doc.chunk\_overlap) → cint(settings.chunk\_overlap).
- Return tuple(size, overlap).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1185)

<a id="op-3b32ec1925dbc0"></a>
### Content hash

`operation_foundation_binding_foundation_flow_knowledge_ingest_content_hash`

**Inputs** text.

**Declared result** str.

**Explicit results** hashlib.sha256(text.encode(“utf-8”)).hexdigest().

**Local steps**

- Return hashlib.sha256(text.encode(“utf-8”)).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1186)

<a id="op-2dc87206a37be3"></a>
### Mark failed

`operation_foundation_binding_foundation_flow_knowledge_ingest_mark_failed`

**Inputs** source.

**Declared result** no value.

**State and service calls** request set\_value on “Flow Knowledge Source” · commit.

**Local steps**

- Set error from Platform.get\_traceback(with\_context = true).
- Evaluate Platform.db.set\_value(“Flow Knowledge Source”, source, mapping(“status” → “Failed”, “error\_log” → error), update\_modified = false).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1194)

## Service · Knowledge

<a id="op-c36ecc6420eac2"></a>
### Knowledge.initialize

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_init`

**Inputs** self, title, description (named only, default no value).

**Declared result** no value.

**Local steps**

- Set self.name from \_ensure\_kb(title, description).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L232) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1210)
