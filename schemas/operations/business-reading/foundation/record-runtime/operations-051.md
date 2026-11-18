# Record lifecycle and persistence · operations 51

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Duckdb sync

<a id="op-14a4bccf5352c1"></a>
### Duck DBSync.sync schema

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_sync_schema`

**Inputs** self.

**Local steps**

- Set duck\_conn from self.get\_duckdb\_conn().
- Set existing from set(list of x at 0 for x drawn from duck\_conn.sql(“show tables”).fetchall()).
  - Draw x from duck\_conn.sql(“show tables”).fetchall().
- For each x in self.db\_tables.
  - Set ddbt from DuckDBTable(x.table).
  - If ddbt.table\_name does not belong to existing.
    - Evaluate ddbt.sync(duck\_conn).
- Evaluate duck\_conn.close().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get duckdb conn](operations-050.md#op-b5f13e20752182).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L5431) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1443)

<a id="op-edde9bb2b64a43"></a>
### Duck DBSync.on cancel

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_on_cancel`

**Inputs** self.

**Local steps**

- Set self.flags.ignore\_links from true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L5683) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1440)

<a id="op-04385b551891ff"></a>
### Duck DBSync.on trash

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_on_trash`

**Inputs** self.

**Local steps**

- If self.docstatus.is\_cancelled().
  - Bind dependencies delete\_duckdb\_file.
  - Evaluate delete\_duckdb\_file(self.filename).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L5734) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1442)

<a id="op-f82da4555f9153"></a>
### Duck DBSync.clear old logs

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_clear_old_logs`

**Inputs** days = 45.

**Wrappers, in declaration order** staticmethod.

**Record and data access** resolve a document from “DuckDB Sync” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“DuckDB Sync”, x) · request delete\_doc for “DuckDB Sync”.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set duckdb\_sync from Platform.qb.DocType(“DuckDB Sync”).
- Set to\_delete from nested operand in the contract(nested operand in the contract).select(duckdb\_sync.name).where(duckdb\_sync.modified &lt; (Now() − Interval(days = days))).run(as\_dict = true, pluck = “name”).
- For each x in to\_delete.
  - Evaluate Platform.get\_doc(“DuckDB Sync”, x).cancel().
  - Evaluate Platform.delete\_doc(“DuckDB Sync”, x).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L5823) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1438)

<a id="op-8279d532a50fa3"></a>
### Is data sync pending

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_is_data_sync_pending`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DuckDB Sync Item” via exists.

**Explicit results** Platform.db.exists(“DuckDB Sync Item”, mapping(“parent” → docname, “synced” → false)).

**Local steps**

- Evaluate Platform.has\_permission(“DuckDB Sync”, ptype = “write”, throw = true).
- Return Platform.db.exists(“DuckDB Sync Item”, mapping(“parent” → docname, “synced” → false)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“DuckDB Sync”, ptype = “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L6170) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1444)

<a id="op-d75b9251ddea9f"></a>
### Start data sync

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_start_data_sync`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “System Settings” via get\_single\_value.

**State and service calls** enqueue.

**Local steps**

- Evaluate Platform.has\_permission(“DuckDB Sync”, ptype = “write”, throw = true).
- Set timeout from (Platform.db.get\_single\_value(“System Settings”, “sync\_timeout”) or (25 × 60)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“System Settings”, “sync\_timeout”) → (25 × 60).
- Evaluate Platform.enqueue(method = “Platform.core.doctype.duckdb\_sync.duckdb\_sync.sync\_data\_to\_duckdb”, queue = “long”, timeout = timeout, enqueue\_after\_commit = true, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“DuckDB Sync”, ptype = “write”, throw = true) · configured or stored value from Platform.db.get\_single\_value(“System Settings”, “sync\_timeout”) · service or queued work from Platform.enqueue(method = “Platform.core.doctype.duckdb\_sync.duckdb\_sync.sync\_data\_to\_duckdb”, queue = “long”, timeout = timeout, enqueue\_after\_commit = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L6350) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1445)

<a id="op-43895244187016"></a>
### Sync using pyarrow

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_sync_using_pyarrow`

**Inputs** conn, dt, duck\_tb.

**Local steps**

- Bind dependencies pa.
- Evaluate conn.execute(formatted text delete from "{duck\_tb.table\_name}";).fetchall().
- Set \_dt from qb.DocType(dt).
- Set columns from Platform.get\_meta(dt).get\_valid\_columns().
- Set query from qb.from\_(\_dt).
- For each col in columns.
  - Set query from query.select(\_dt at col).
- Set schema from duck\_tb.get\_arrow\_schema().
- Within Platform.db.unbuffered\_cursor().
  - Set iter from query.run(as\_dict = true, as\_iterator = true).
  - Set field\_list from “, ”.join(generator of formatted text "{c}" for c drawn from schema.names).
    - Draw c from schema.names.
  - Set time\_columns from list of name for tuple(name, dtype) drawn from zip(schema.names, schema.types, strict = false) where pa.types.is\_time(dtype).
    - Draw tuple(name, dtype) from zip(schema.names, schema.types, strict = false), keep a combination only if (pa.types.is\_time(dtype)).
  - Bind local operation timedelta\_to\_time for subsequent calls.
  - Bind local operation recordbatch\_from\_list for subsequent calls.
  - Set reader from pa.RecordBatchReader.from\_batches(schema, recordbatch\_from\_list(iter, schema)).
  - For each batch in reader.
    - Set arrow\_table from pa.Table.from\_batches(list(batch)).
    - Evaluate conn.register(“arrow\_table”, arrow\_table).
    - Evaluate conn.execute(formatted text insert into "{duck\_tb.table\_name}" ({field\_list}) select {field\_list} from arrow\_table;).fetchall().
    - Evaluate conn.unregister(“arrow\_table”).
    - Remove arrow\_table.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1448)

<a id="op-6db95847a65320"></a>
### Sync using pyarrow.timedelta to time

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_sync_using_pyarrow_timedelta_to_time`

**Inputs** td.

**Explicit results** time(hours, minutes, seconds, td.microseconds).

**Local steps**

- Set total\_seconds from (int(td.total\_seconds()) modulo or format 86400).
- Set tuple(hours, remainder) from divmod(total\_seconds, 3600).
- Set tuple(minutes, seconds) from divmod(remainder, 60).
- Return time(hours, minutes, seconds, td.microseconds).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L4270) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1450)

<a id="op-2d374e9a4dc418"></a>
### Sync using pyarrow.recordbatch from list

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_sync_using_pyarrow_recordbatch_from_list`

**Inputs** iter, schema.

**Local steps**

- Set batch\_size from 204800.
- Set rows from list().
- For each row in iter.
  - For each col in time\_columns.
    - If isinstance(row.get(col), timedelta).
      - Set row at col from timedelta\_to\_time(row at col).
  - Evaluate rows.append(row).
  - If len(rows) ≥ batch\_size.
    - Set batch from pa.RecordBatch.from\_pylist(rows, schema = schema).
    - yield batch.
    - Set rows from list().
    - Remove batch.
- If rows.
  - Set batch from pa.RecordBatch.from\_pylist(rows, schema = schema).
  - yield batch.
  - Set rows from list().
  - Remove batch.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L4455) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1449)

<a id="op-74e97e41663dd2"></a>
### Sync using extension

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_sync_using_extension`

**Inputs** conn, dt, duck\_tb.

**Explicit failure paths** Exception(sanitized).

**Local steps**

- Attempt the following.
  - Evaluate conn.execute(formatted text delete from "{duck\_tb.table\_name}";).fetchall().
  - Evaluate conn.sql(formatted text attach 'user={Platform.conf.db\_name} password={Platform.conf.db\_password} host={Platform.conf.db\_host} database={Platform.conf.db\_name} port={Platform).
  - Set columns from Platform.get\_meta(dt).get\_valid\_columns().
  - Set columns\_sql from “, ”.join(list of formatted text "{x}" for x drawn from columns).
    - Draw x from columns.
  - Set query from formatted text insert into "{duck\_tb.table\_name}" ({columns\_sql}) select {columns\_sql} from mariadb\_db."{duck\_tb.table\_name}";.
  - Evaluate conn.sql(query).
- On failure (Exception) bound to e.
  - Bind dependencies re.
  - Set sanitized from re.sub(“(user\|password)=\\S+”, deferred anonymous expression, str(e)).
  - Raise Exception(sanitized) with cause no value.
- On exit, including pending return or failure.
  - Evaluate conn.close().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L1367) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1447)

<a id="op-01893dd92a78cc"></a>
### Sync data to duckdb

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_sync_data_to_duckdb`

**Inputs** docname.

**Record and data access** read “System Settings” via get\_single\_value · resolve a document from “DuckDB Sync” via get\_doc.

**State and service calls** request set\_value on “DuckDB Sync Item” · enqueue.

**Local steps**

- Set sync\_dt from qb.DocType(“DuckDB Sync Item”).
- If unsynced bound to nested operand in the contract.limit(1).for\_update(skip\_locked = true).run(as\_dict = true).
  - Set dt from unsynced at 0 at “table”.
  - Set name from unsynced at 0 at “name”.
  - Set duck\_tb from DuckDBTable(dt).
  - Set timeout from (Platform.db.get\_single\_value(“System Settings”, “sync\_timeout”) or (25 × 60)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“System Settings”, “sync\_timeout”) → (25 × 60).
  - Set sync\_in\_batch from Platform.db.get\_single\_value(“System Settings”, “sync\_in\_batch”).
  - Set conn from Platform.get\_doc(“DuckDB Sync”, docname).get\_duckdb\_conn().
  - If sync\_in\_batch.
    - Evaluate sync\_using\_pyarrow(conn, dt, duck\_tb).
    - Evaluate conn.close().
  - Otherwise.
    - Evaluate sync\_using\_extension(conn, dt, duck\_tb).
  - Evaluate Platform.db.set\_value(“DuckDB Sync Item”, name, “synced”, true).
  - Evaluate Platform.enqueue(method = “Platform.core.doctype.duckdb\_sync.duckdb\_sync.sync\_data\_to\_duckdb”, queue = “long”, timeout = timeout, is\_async = true, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “sync\_timeout”), Platform.db.get\_single\_value(“System Settings”, “sync\_in\_batch”) · service or queued work from Platform.enqueue(method = “Platform.core.doctype.duckdb\_sync.duckdb\_sync.sync\_data\_to\_duckdb”, queue = “long”, timeout = timeout, is\_async = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L2020) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1446)

## Record · Dynamic link

[Record definition](../../../../data/record-types/dynamic_link.json)

<a id="op-7f34d14d02ae8e"></a>
### On doctype update

`operation_foundation_core_record_definitions_dynamic_link_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Dynamic Link”.

**Local steps**

- Evaluate Platform.db.add\_index(“Dynamic Link”, list(“link\_doctype”, “link\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L2819) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1452)

<a id="op-60e90cc602c9a0"></a>
### Deduplicate dynamic links

`operation_foundation_core_record_definitions_dynamic_link_business_behavior_deduplicate_dynamic_links`

**Inputs** doc.

**Local steps**

- Set tuple(links, duplicate) from tuple(list(), false).
- For each l in (doc.links or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.links → list().
  - Set t from tuple(l.link\_doctype, l.link\_name).
  - If t does not belong to links.
    - Evaluate links.append(t).
  - Otherwise.
    - Set duplicate from true.
- If duplicate.
  - Set doc.links from list().
  - For each l in links.
    - Evaluate doc.append(“links”, dict(link\_doctype = l at 0, link\_name = l at 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L2897) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1451)

## Service · Dynamic links

<a id="op-7f0529fe3e705a"></a>
### Get dynamic link map

`operation_foundation_model_dynamic_links_business_behavior_get_dynamic_link_map`

**Inputs** for\_delete = false.

**Explicit results** Platform.local.dynamic\_link\_map.

**Local steps**

- If (getattr(Platform.local, “dynamic\_link\_map”, no value) is identical to no value or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(Platform.local, “dynamic\_link\_map”, no value) is identical to no value → Platform.in\_test.
  - Set dynamic\_link\_map from mapping().
  - For each df in get\_dynamic\_links().
    - Set meta from Platform.get\_meta(df.parent).
    - If meta.issingle.
      - Evaluate dynamic\_link\_map.setdefault(meta.name, list()).append(df).
    - Otherwise.
      - Attempt the following.
        - Set links from fetch\_distinct\_link\_doctypes(df.parent, df.options).
        - For each doctype in links.
          - Evaluate dynamic\_link\_map.setdefault(doctype, list()).append(df).
      - On failure (Platform.db.TableMissingError).
        - Take no action here.
  - Set Platform.local.dynamic\_link\_map from dynamic\_link\_map.
- Return Platform.local.dynamic\_link\_map.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “dynamic\_link\_map”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L1834) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1086)

<a id="op-388d6bff30534b"></a>
### Get dynamic links

`operation_foundation_model_dynamic_links_business_behavior_get_dynamic_links`

**Inputs** no declared parameters.

**State and service calls** execute a supplied database query.

**Explicit results** df.

**Local steps**

- Set df from list().
- For each query in dynamic\_link\_queries.
  - Update df using + Platform.db.sql(query, as\_dict = true).
- Return df.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L2228) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1087)

<a id="op-36343598a9ac57"></a>
### Dynamic link map key

`operation_foundation_model_dynamic_links_business_behavior_dynamic_link_map_key`

**Inputs** doctype, fieldname.

**Explicit results** formatted text dynamic\_link\_map::{doctype}::{fieldname}.

**Local steps**

- Return formatted text dynamic\_link\_map::{doctype}::{fieldname}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L2328) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1084)

<a id="op-91a73e0ae1df29"></a>
### Fetch distinct link doctypes

`operation_foundation_model_dynamic_links_business_behavior_fetch_distinct_link_record_types`

**Inputs** doctype, fieldname.

**State and service calls** execute a supplied database query.

**Explicit results** doctypes.

**Local steps**

- Set key from \_dynamic\_link\_map\_key(doctype, fieldname).
- Set doctypes from Platform.cache.get\_value(key).
- If doctypes is identical to no value.
  - Set doctypes from Platform.db.sql(formatted text select distinct ′{fieldname}′ from ′tab{doctype}′, pluck = true).
  - Evaluate Platform.cache.set\_value(key, doctypes, expires\_in\_sec = ((12 × 60) × 60)).
- Return doctypes.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L2403) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1085)

<a id="op-859c0057f335bf"></a>
### Invalidate distinct link doctypes

`operation_foundation_model_dynamic_links_business_behavior_invalidate_distinct_link_record_types`

**Inputs** doctype, fieldname, linked\_doctype.

**Explicit results** no value.

**Local steps**

- Set key from \_dynamic\_link\_map\_key(doctype, fieldname).
- Set doctypes from Platform.cache.get\_value(key).
- If (doctypes is identical to no value or not isinstance(doctypes, list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctypes is identical to no value → not isinstance(doctypes, list).
  - Return no value.
- If linked\_doctype does not belong to doctypes.
  - Evaluate Platform.cache.delete\_value(key).
  - Set Platform.local.dynamic\_link\_map from no value.
  - Evaluate Platform.db.after\_commit.add(deferred anonymous expression).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L95) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1088)

## Service · Edit profile

<a id="op-3746980a26e385"></a>
### Get context

`operation_foundation_core_web_form_edit_profile_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L574) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L922)

## Record · Error log

[Record definition](../../../../data/record-types/error_log.json)

<a id="op-ebb98bf09c38c1"></a>
### Error Log.validate

`operation_foundation_core_record_definitions_error_log_business_behavior_error_log_validate`

**Inputs** self.

**Local steps**

- Set self.method from str(self.method).
- Set self.error from str(self.error).
- If len(self.method) &gt; 140.
  - Set self.error from formatted text {self.method} {self.error}.
  - Set self.method from self.method at slice no value to 140.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L3191) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1456)

<a id="op-e9af3c6b6b2f8e"></a>
### Error Log.onload

`operation_foundation_core_record_definitions_error_log_business_behavior_error_log_onload`

**Inputs** self.

**State and service calls** call db\_set on self · commit.

**Local steps**

- If (not self.seen and not Platform.flags.read\_only).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.seen → not Platform.flags.read\_only.
  - Evaluate self.db\_set(“seen”, 1, update\_modified = 0).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L3414) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1455)

<a id="op-45a5fa938a27dd"></a>
### Error Log.clear old logs

`operation_foundation_core_record_definitions_error_log_business_behavior_error_log_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Set table from Platform.qb.DocType(“Error Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L3549) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1454)

<a id="op-8d63104f3c0c17"></a>
### Clear error logs

`operation_foundation_core_record_definitions_error_log_business_behavior_clear_error_logs`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request truncate on “Error Log”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Evaluate Platform.db.truncate(“Error Log”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L3714) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1453)

<a id="op-da06dbadb81e12"></a>
### Get fingerprint stats

`operation_foundation_core_record_definitions_error_log_business_behavior_get_fingerprint_stats`

**Inputs** fingerprint.

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = (5 × 60)).

**Declared result** dict.

**Explicit results** mapping(“count” → (summary.count or 0), “first\_seen” → summary.first\_seen, “last\_seen” → summary.last\_seen, “timeline” → timeline).

**Local steps**

- Evaluate Platform.has\_permission(“Error Log”, throw = true).
- Set table from Platform.qb.DocType(“Error Log”).
- Set summary from nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).select(nested operand in the contract(nested operand in the contract).as\_(“count”), nested operand … at 0.
- Set timeline from nested operand in the contract(nested operand in the contract).orderby(Date(nested operand in the contract.creation)).select(Date(nested operand in the contract.creation).as\_(“day”), Count(“\*”).as\_(“count” ….
- Return mapping(“count” → (summary.count or 0), “first\_seen” → summary.first\_seen, “last\_seen” → summary.last\_seen, “timeline” → timeline).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in summary.count → 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Error Log”, throw = true) · clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L4062) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1457)
