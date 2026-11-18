# Workflow, automation and dispatch · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Flow handlers

<a id="op-38399107622f1b"></a>
### Relay.recheck

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_recheck`

**Inputs** self, channel, data.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set notice from parse(data).
- If (notice is identical to no value or not is\_valid\_name(notice.get(“session”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in notice is identical to no value → not is\_valid\_name(notice.get(“session”)).
  - Return no value.
- Set site from channel.removeprefix(ACCESS\_SITE).
- For each entry in list(self.subscriptions.values()).
  - If (entry.site differs from site or entry.session differs from notice at “session”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.site differs from site → entry.session differs from notice at “session”.
    - Continue with the next iteration or loop test.
  - For each socket in list(entry.sockets.values()).
    - If socket.user equals notice.get(“owner”).
      - Continue with the next iteration or loop test.
    - If (notice.get(“user”) and socket.user differs from notice at “user”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in notice.get(“user”) → socket.user differs from notice at “user”.
      - Continue with the next iteration or loop test.
    - If await socket.has\_permission(“Flow Session”, entry.session).
      - Continue with the next iteration or loop test.
    - Evaluate await self.release(socket, entry.session).
    - Evaluate await socket.emit(RESUBSCRIBE, mapping(“session” → entry.session)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [release](operations-022.md#op-475c9f5c78568d).

**Values supplied outside this operation** effective access from socket.has\_permission(“Flow Session”, entry.session) · service or queued work from socket.has\_permission(“Flow Session”, entry.session), socket.emit(RESUBSCRIBE, mapping(“session” → entry.session)).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1700)

<a id="op-f8b40e18810716"></a>
### Redis client

`operation_foundation_binding_foundation_realtime_flow_handlers_redis_client`

**Inputs** no declared parameters.

**Declared result** redis.asyncio.Redis.

**Explicit results** redis.asyncio.from\_url((conf.get(“flow\_redis\_url”) or config.redis\_queue), decode\_responses = true).

**Local steps**

- Set config from get\_config().
- Set conf from Platform.get\_common\_site\_config(sites\_path = config.sites\_path).
- Return redis.asyncio.from\_url((conf.get(“flow\_redis\_url”) or config.redis\_queue), decode\_responses = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“flow\_redis\_url”) → config.redis\_queue.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1695)

<a id="op-c3b1845c3087ac"></a>
### Parse

`operation_foundation_binding_foundation_realtime_flow_handlers_parse`

**Inputs** data.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · value when isinstance(value, dict), otherwise no value.

**Local steps**

- Attempt the following.
  - Set value from json.loads(data).
- On failure (ValueError).
  - Return no value.
- Return value when isinstance(value, dict), otherwise no value.
  - Value choice on isinstance(value, dict) — true gives value, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1694)

<a id="op-cd2438bbcdcb30"></a>
### Is valid name

`operation_foundation_binding_foundation_realtime_flow_handlers_is_valid_name`

**Inputs** session.

**Declared result** bool.

**Explicit results** (isinstance(session, str) and bool(SESSION\_NAME.fullmatch(session))).

**Local steps**

- Return (isinstance(session, str) and bool(SESSION\_NAME.fullmatch(session))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(session, str) → bool(SESSION\_NAME.fullmatch(session)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1693)

<a id="op-12cce850cc2b0a"></a>
### Subscribe

`operation_foundation_binding_foundation_realtime_flow_handlers_subscribe`

**Inputs** socket, session.

**Wrappers, in declaration order** realtime.on(“flow:subscribe”).

The declaration is asynchronous.

**Declared result** dict.

**Explicit results** mapping(“subscribed” → subscribed).

**Local steps**

- Attempt the following.
  - Set subscribed from await relay.subscribe(socket, session).
- On failure (Exception).
  - Evaluate logger.exception(“flow: subscribe failed”).
  - Set subscribed from false.
- Return mapping(“subscribed” → subscribed).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1705)

<a id="op-cf63f18c1afb6a"></a>
### Unsubscribe

`operation_foundation_binding_foundation_realtime_flow_handlers_unsubscribe`

**Inputs** socket, session.

**Wrappers, in declaration order** realtime.on(“flow:unsubscribe”).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- If is\_valid\_name(session).
  - Evaluate await relay.release(socket, session).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1706)

<a id="op-c056c40b2d4ac8"></a>
### Disconnect

`operation_foundation_binding_foundation_realtime_flow_handlers_disconnect`

**Inputs** socket.

**Wrappers, in declaration order** realtime.on(“disconnect”).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- For each session in list(socket.get(“flow\_sessions”, list())).
  - Evaluate await relay.release(socket, session).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.get(“flow\_sessions”, list()).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1692)

## Record · Flow knowledge base

<a id="op-091b52060df757"></a>
### Flow Knowledge Base.validate

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_base_flow_knowledge_base_flowknowledgebase_validate`

**Inputs** self.

**Local steps**

- If self.is\_new().
  - Bind dependencies require\_embedding\_model.
  - Evaluate require\_embedding\_model().
- Evaluate validate\_immutable(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1026) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1002)

<a id="op-75c15494a671b8"></a>
### Flow Knowledge Base.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_base_flow_knowledge_base_flowknowledgebase_on_trash`

**Inputs** self.

**Local steps**

- Evaluate block\_delete(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1025) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1001)

<a id="op-ff39bdf9bc72f5"></a>
### Flow Knowledge Base.before rename

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_base_flow_knowledge_base_flowknowledgebase_before_rename`

**Inputs** self, old, new, merge = false.

**Declared result** no value.

**Record and data access** read “Flow Knowledge Source” via exists.

**Explicit failure paths** validation helper — translated “{0} has sources still processing. Rename it once they finish.”.format(old).

**Local steps**

- Evaluate block\_rename(self, old).
- If Platform.db.exists(“Flow Knowledge Source”, mapping(“knowledge\_base” → old, “status” → “Processing”)).
  - Call the validation error handler Platform.throw(translated “{0} has sources still processing. Rename it once they finish.”.format(old), title = translated “Sources Processing”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1000)

<a id="op-872cfe12ce94a8"></a>
### Flow Knowledge Base.after rename

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_base_flow_knowledge_base_flowknowledgebase_after_rename`

**Inputs** self, old, new, merge = false.

**Declared result** no value.

**Local steps**

- Bind dependencies store.
- Evaluate store.rename\_kb(old, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1023) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L999)

## Record · Flow knowledge settings

<a id="op-5d870ecdf49b6d"></a>
### Flow Knowledge Settings.validate

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_settings_flow_knowledge_settings_flowknowledgesettings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_validate\_chunking().
- Evaluate self.\_guard\_model\_change().
- Evaluate self.\_sync\_embedding\_dimension().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate chunking](operations-023.md#op-31407792a62a27), [guard model change](operations-023.md#op-6683755683ba2c), [sync embedding dimension](operations-023.md#op-ae76a03af80671).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1030) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1006)

<a id="op-31407792a62a27"></a>
### Flow Knowledge Settings.validate chunking

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_settings_flow_knowledge_settings_flowknowledgesettings_validate_chunking`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Chunk Size must be at least 1.” · validation helper — translated “Chunk Overlap must be smaller than Chunk Size.”.

**Local steps**

- If cint(self.chunk\_size) &lt; 1.
  - Call the validation error handler Platform.throw(translated “Chunk Size must be at least 1.”, title = translated “Invalid Chunking”).
- If cint(self.chunk\_overlap) ≥ cint(self.chunk\_size).
  - Call the validation error handler Platform.throw(translated “Chunk Overlap must be smaller than Chunk Size.”, title = translated “Invalid Chunking”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1031) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1007)

<a id="op-6683755683ba2c"></a>
### Flow Knowledge Settings.guard model change

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_settings_flow_knowledge_settings_flowknowledgesettings_guard_model_change`

**Inputs** self.

**Record and data access** read “Flow Knowledge Chunk” via count.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} knowledge chunks were embedded with the current model. Delete all knowledge sources before changing the  …”.format(chunk\_count).

**Local steps**

- If self.flags.allow\_embedding\_model\_change.
  - Return no value.
- Set previous from self.get\_doc\_before\_save().
- If (previous is identical to no value or previous.embedding\_model equals self.embedding\_model).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous is identical to no value → previous.embedding\_model equals self.embedding\_model.
  - Return no value.
- Set chunk\_count from Platform.db.count(“Flow Knowledge Chunk”).
- If chunk\_count.
  - Call the validation error handler Platform.throw(translated “{0} knowledge chunks were embedded with the current model. Delete all knowledge sources before changing the  …”.format(chunk\_count), title = translated “Embedding Model In Use”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1028) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1004)

<a id="op-ae76a03af80671"></a>
### Flow Knowledge Settings.sync embedding dimension

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_settings_flow_knowledge_settings_flowknowledgesettings_sync_embedding_dimension`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.embedding\_model.
  - Set self.embedding\_dimension from 0.
  - Return no value.
- Set previous from self.get\_doc\_before\_save().
- Set model\_unchanged from (previous is distinct from no value and previous.embedding\_model equals self.embedding\_model).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous is distinct from no value → previous.embedding\_model equals self.embedding\_model.
- If (model\_unchanged and self.embedding\_dimension).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in model\_unchanged → self.embedding\_dimension.
  - Return no value.
- Bind dependencies probe\_dimension.
- Set self.embedding\_dimension from probe\_dimension(self.embedding\_model).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1029) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1005)

<a id="op-1e0d9ade2c1883"></a>
### Embeddings configured

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_settings_flow_knowledge_settings_embeddings_configured`

**Inputs** no declared parameters.

**Declared result** bool.

**Record and data access** read “Flow Knowledge Settings” via get\_cached\_value.

**Explicit results** bool(Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “embedding\_model”)).

**Local steps**

- Return bool(Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “embedding\_model”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “embedding\_model”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1027) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1003)

<a id="op-38f75edf6c8041"></a>
### Require embedding model

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_settings_flow_knowledge_settings_require_embedding_model`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Flow Knowledge Settings” via get\_cached\_doc.

**Explicit failure paths** validation helper — translated “Set an embedding model in Flow Knowledge Settings before adding knowledge bases or sources.”.

**Local steps**

- Set settings from Platform.get\_cached\_doc(“Flow Knowledge Settings”).
- If not settings.embedding\_model.
  - Call the validation error handler Platform.throw(translated “Set an embedding model in Flow Knowledge Settings before adding knowledge bases or sources.”, title = translated “Flow Knowledge Settings Required”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Flow Knowledge Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1032) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1008)

## Record · Flow knowledge source

<a id="op-b92a38a29aa561"></a>
### Flow Knowledge Source.validate

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_validate`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “{0} is required for a {1} source.”.format(translated self.meta.get\_label(fieldname), translated self.source\_type) · validation helper with Platform.MandatoryError — translated “Content Fields is required for a DocType source.” · validation helper — translated “{0} is still processing. Move it once it finishes.”.format(self.title).

**Local steps**

- If self.is\_new().
  - Bind dependencies require\_embedding\_model.
  - Evaluate require\_embedding\_model().
- Set fieldname from REQUIRED\_INPUT.get(self.source\_type).
- If (fieldname and not self.get(fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname → not self.get(fieldname).
  - Call the validation error handler Platform.throw(translated “{0} is required for a {1} source.”.format(translated self.meta.get\_label(fieldname), translated self.source\_type), Platform.MandatoryError).
- If (self.source\_type equals “DocType” and not (self.content\_fields or empty text).strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.source\_type equals “DocType” → not (self.content\_fields or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.content\_fields → empty text.
  - Call the validation error handler Platform.throw(translated “Content Fields is required for a DocType source.”, Platform.MandatoryError).
- Evaluate self.\_validate\_chunking().
- Evaluate validate\_immutable(self, tuple(“source\_type”, “knowledge\_base”)).
- Set before from self.get\_doc\_before\_save().
- If (before and before.knowledge\_base differs from self.knowledge\_base and before.status equals “Processing”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → before.knowledge\_base differs from self.knowledge\_base → before.status equals “Processing”.
  - Call the validation error handler Platform.throw(translated “{0} is still processing. Move it once it finishes.”.format(self.title), title = translated “Source Processing”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate chunking](operations-023.md#op-b9612b751a76ed).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1038) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1014)

<a id="op-b9612b751a76ed"></a>
### Flow Knowledge Source.validate chunking

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_validate_chunking`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Chunk Overlap must be smaller than Chunk Size.”.

**Local steps**

- If (self.chunk\_size and self.chunk\_overlap and cint(self.chunk\_overlap) ≥ cint(self.chunk\_size)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.chunk\_size → self.chunk\_overlap → cint(self.chunk\_overlap) ≥ cint(self.chunk\_size).
  - Call the validation error handler Platform.throw(translated “Chunk Overlap must be smaller than Chunk Size.”, title = translated “Invalid Chunking”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1039) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1015)

<a id="op-97b10b8f9b4ed4"></a>
### Flow Knowledge Source.after insert

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_after_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.skip\_auto\_ingest.
  - Return no value.
- Bind dependencies enqueue\_ingestion.
- Evaluate enqueue\_ingestion(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1033) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1009)

<a id="op-4075074b961fc2"></a>
### Flow Knowledge Source.on update

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_on_update`

**Inputs** self.

**State and service calls** request set\_value on “Flow Knowledge Chunk”.

**Explicit results** no value.

**Local steps**

- If (self.flags.in\_insert or self.flags.skip\_auto\_ingest).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.in\_insert → self.flags.skip\_auto\_ingest.
  - Return no value.
- If self.has\_value\_changed(“knowledge\_base”).
  - Bind dependencies store.
  - Evaluate Platform.db.set\_value(“Flow Knowledge Chunk”, mapping(“source” → self.name), “knowledge\_base”, self.knowledge\_base, update\_modified = false).
  - Evaluate store.move\_source(self.name, self.knowledge\_base).
- If any(generator of self.has\_value\_changed(field) for field drawn from EXTRACTION\_INPUTS).
  - Draw field from EXTRACTION\_INPUTS.
  - Evaluate self.resync(rebuild = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [resync](operations-023.md#op-580ef22f603a9c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1035) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1011)

<a id="op-87260da526cb2b"></a>
### Flow Knowledge Source.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_on_trash`

**Inputs** self.

**Local steps**

- Evaluate block\_delete(self).
- Bind dependencies purge\_source.
- Evaluate purge\_source(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1034) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1010)

<a id="op-580ef22f603a9c"></a>
### Flow Knowledge Source.resync

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_resync`

**Inputs** self, rebuild = false.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies enqueue\_ingestion.
- Evaluate Platform.has\_permission(self.doctype, “write”, self.name, throw = true).
- Evaluate self.db\_set(“status”, “Pending”, update\_modified = false).
- Evaluate enqueue\_ingestion(self.name, rebuild = bool(rebuild)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “write”, self.name, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1037) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1013)

<a id="op-5fffbbc490cb8b"></a>
### Flow Knowledge Source.reconcile

`operation_foundation_binding_foundation_flow_doctype_flow_knowledge_source_flow_knowledge_source_flowknowledgesource_reconcile`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Bind dependencies enqueue\_reconciliation.
- Evaluate Platform.has\_permission(self.doctype, “write”, self.name, throw = true).
- Evaluate enqueue\_reconciliation(self.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “write”, self.name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1036) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1012)
