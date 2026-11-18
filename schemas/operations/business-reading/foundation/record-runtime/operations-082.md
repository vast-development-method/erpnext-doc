# Record lifecycle and persistence · operations 82

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Recorder

[Record definition](../../../../data/record-types/recorder.json)

<a id="op-84f831baac951a"></a>
### Recorder.get stats

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_get_stats`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L2170) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L325)

<a id="op-09dcb35076d1a5"></a>
### Recorder.delete

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_delete`

**Inputs** self.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L2208) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L321)

<a id="op-5b66b3cdd612cd"></a>
### Recorder.db insert

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L2246) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L319)

<a id="op-2cd25c9656f568"></a>
### Recorder.db update

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_database_update`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L2289) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L320)

<a id="op-057882d3445c17"></a>
### Serialize request

`operation_foundation_core_record_definitions_recorder_business_behavior_serialize_request`

**Inputs** request.

**Explicit results** request.

**Local steps**

- Set request from Platform.\_dict(request).
- If request.get(“calls”).
  - For each i in request.calls.
    - Set i at “stack” from Platform.as\_json(i at “stack”).
    - Set i at “explain\_result” from Platform.as\_json(i at “explain\_result”).
- Set events from (request.get(“events”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.get(“events”) → list().
- For each event in events.
  - Set indent from (whitespace '\\xa0\\xa0\\xa0\\xa0' × event.get(“depth”, 0)).
  - Set event at “label” from (indent + (event.get(“method”) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in event.get(“method”) → empty text.
  - If isinstance(event.get(“apps”), list).
    - Set event at “apps” from “, ”.join(event at “apps”).
  - If isinstance(event.get(“handlers”), list).
    - Set event at “handlers” from whitespace '\\n'.join(event at “handlers”).
- Evaluate request.update(name = request.get(“uuid”), number\_of\_queries = request.get(“queries”), time\_in\_queries = request.get(“time\_queries”), number\_of\_events = (request.get(“number\_of\_events”) or len(events)), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.get(“number\_of\_events”) → len(events).
- Return request.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L2322) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L327)

<a id="op-9237c488f46357"></a>
### Add indexes

`operation_foundation_core_record_definitions_recorder_business_behavior_add_indexes`

**Inputs** indexes.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** enqueue with \_add\_index · msgprint with translated “Enqueued creation of indexes”.

**Local steps**

- Evaluate Platform.only\_for(“Administrator”).
- Set indexes from json.loads(indexes).
- For each index in indexes.
  - Evaluate Platform.enqueue(\_add\_index, table = index at “table”, column = index at “column”).
- Evaluate Platform.msgprint(translated “Enqueued creation of indexes”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“Administrator”) · service or queued work from Platform.enqueue(\_add\_index, table = index at “table”, column = index at “column”).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L10) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L311)

<a id="op-3419afcd2a653a"></a>
### Add index

`operation_foundation_core_record_definitions_recorder_business_behavior_add_index`

**Inputs** table, column.

**State and service calls** request add\_index on doctype · msgprint with translated “Index created successfully on column {0} of doctype {1}”.format(column, doctype).

**Local steps**

- Set doctype from get\_doctype\_name(table).
- Evaluate Platform.db.add\_index(doctype, list(column)).
- Evaluate Platform.msgprint(translated “Index created successfully on column {0} of doctype {1}”.format(column, doctype), alert = true, realtime = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L3580) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L310)

<a id="op-f6e5372dd8ba73"></a>
### Optimize

`operation_foundation_core_record_definitions_recorder_business_behavior_optimize`

**Inputs** recorder\_id.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** enqueue with \_optimize.

**Local steps**

- Evaluate Platform.only\_for(“Administrator”).
- Evaluate Platform.enqueue(\_optimize, recorder\_id = recorder\_id, queue = “long”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“Administrator”) · service or queued work from Platform.enqueue(\_optimize, recorder\_id = recorder\_id, queue = “long”).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L3762) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L316)

<a id="op-83dea326e953be"></a>
### Optimize

`operation_foundation_core_record_definitions_recorder_business_behavior_optimize_2`

**Inputs** recorder\_id.

**Record and data access** resolve a document from “Recorder” via get\_doc.

**State and service calls** msgprint with translated “No automatic optimization suggestions available.” · publish realtime with “recorder-analysis-complete” · msgprint with translated “Query analysis complete. Check suggested indexes.”.

**Explicit results** no value.

**Local steps**

- Set record from Platform.get\_doc(“Recorder”, recorder\_id).
- Set total\_duration from record.time\_in\_queries.
- Set PERCENT\_DURATION\_THRESHOLD\_OVERALL from 0.05.
- Set PERCENT\_DURATION\_THRESHOLD\_QUERY from 0.005.
- Set index\_suggestions from Counter().
- For each tuple(idx, captured\_query) in enumerate(record.sql\_queries, start = 1).
  - Set query from cstr(captured\_query.query).
  - Evaluate Platform.publish\_progress(((idx ÷ len(record.sql\_queries)) × 100), title = “Analyzing Queries”, doctype = record.doctype, docname = record.name, description = formatted text Analyzing query: {query at slic ….
  - If captured\_query.duration &lt; (total\_duration × PERCENT\_DURATION\_THRESHOLD\_QUERY).
    - Continue with the next iteration or loop test.
  - If not nested operand in the contract.lower().strip().startswith(tuple(“select”, “update”, “delete”)).
    - Continue with the next iteration or loop test.
  - If index bound to \_optimize\_query(query).
    - Update index\_suggestions at tuple(index.table, index.column) using + captured\_query.duration.
- Set suggested\_indexes from index\_suggestions.most\_common(3).
- Set suggested\_indexes from list of idx for idx drawn from suggested\_indexes where idx at 1 &gt; (total\_duration × PERCENT\_DURATION\_THRESHOLD\_OVERALL).
  - Draw idx from suggested\_indexes, keep a combination only if (idx at 1 &gt; (total\_duration × PERCENT\_DURATION\_THRESHOLD\_OVERALL)).
- If not suggested\_indexes.
  - Evaluate Platform.msgprint(translated “No automatic optimization suggestions available.”, title = translated “No Suggestions”, realtime = true).
  - Return no value.
- Set data from Platform.cache.hget(RECORDER\_REQUEST\_HASH, record.name).
- Set data at “suggested\_indexes” from list of mapping(“table” → idx at 0 at 0, “column” → idx at 0 at 1) for idx drawn from suggested\_indexes.
  - Draw idx from suggested\_indexes.
- Evaluate Platform.cache.hset(RECORDER\_REQUEST\_HASH, record.name, data).
- Evaluate Platform.publish\_realtime(“recorder-analysis-complete”, user = Platform.session.user).
- Evaluate Platform.msgprint(translated “Query analysis complete. Check suggested indexes.”, realtime = true, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“recorder-analysis-complete”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L3884) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L317)

<a id="op-41b276dbada5d7"></a>
### Optimize query

`operation_foundation_core_record_definitions_recorder_business_behavior_optimize_query`

**Inputs** query.

**Explicit results** no value · optimizer.suggest\_index().

**Local steps**

- Set optimizer from DBOptimizer(query = query).
- Set tables from optimizer.tables\_examined().
- For each table in tables.
  - Set doctype from get\_doctype\_name(table).
  - Set stats from \_fetch\_table\_stats(doctype, columns = list()).
  - If not stats.
    - Return no value.
  - Set db\_table from DBTable.from\_Platform\_ouput(stats).
  - Evaluate optimizer.update\_table\_data(db\_table).
- Set potential\_indexes from optimizer.potential\_indexes().
- Set tablewise\_columns from defaultdict(list).
- For each idx in potential\_indexes.
  - Evaluate tablewise\_columns at idx.table.append(idx.column).
- For each table in tables.
  - Set doctype from get\_doctype\_name(table).
  - Set stats from \_fetch\_table\_stats(doctype, columns = tablewise\_columns at table).
  - If not stats.
    - Return no value.
  - Set db\_table from DBTable.from\_Platform\_ouput(stats).
  - Evaluate optimizer.update\_table\_data(db\_table).
- Return optimizer.suggest\_index().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L4899) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L318)

<a id="op-36c1c2e6bde3e5"></a>
### Fetch table stats

`operation_foundation_core_record_definitions_recorder_business_behavior_fetch_table_stats`

**Inputs** doctype, columns.

**Declared result** (dict bitwise or no value).

**State and service calls** execute a supplied database query.

**Explicit results** no value · mapping(“table\_name” → table.strip(“′”), “total\_rows” → total\_rows, “schema” → schema, “indexes” → indexes).

**Local steps**

- Bind local operation sql\_bool for subsequent calls.
- If not Platform.db.table\_exists(doctype).
  - Return no value.
- Set table from get\_table\_name(doctype, wrap\_in\_backticks = true).
- Set schema from list().
- For each field in Platform.db.sql(formatted text describe {table}, as\_dict = true).
  - Evaluate schema.append(mapping(“column” → field at “Field”, “type” → field at “Type”, “is\_nullable” → sql\_bool(field at “Null”), “default” → field at “Default”)).
- Bind local operation update\_cardinality for subsequent calls.
- Set indexes from list().
- For each idx in Platform.db.sql(formatted text show index from {table}, as\_dict = true).
  - Evaluate indexes.append(mapping(“unique” → not sql\_bool(idx at “Non\_unique”), “cardinality” → idx at “Cardinality”, “name” → idx at “Key\_name”, “sequence” → idx at “Seq\_in\_index”, …)).
  - If idx at “Seq\_in\_index” equals 1.
    - Evaluate update\_cardinality(idx at “Column\_name”, idx at “Cardinality”).
- Set total\_rows from cint(Platform.db.sql(formatted text select table\_rows     from  information\_schema.tables     where table\_name = 'tab{doctype}') at 0 at 0).
- For each column in columns.
  - Set cardinality from \_get\_column\_cardinality(table, column).
  - Evaluate update\_cardinality(column, cardinality).
- Return mapping(“table\_name” → table.strip(“′”), “total\_rows” → total\_rows, “schema” → schema, “indexes” → indexes).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L11) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L312)

<a id="op-bcbf7839cde81a"></a>
### Fetch table stats.sql bool

`operation_foundation_binding_foundation_core_doctype_recorder_recorder_fetch_table_stats_sql_bool`

**Inputs** val.

**Explicit results** cstr(val).lower() belongs to tuple(“yes”, “1”, “true”).

**Local steps**

- Return cstr(val).lower() belongs to tuple(“yes”, “1”, “true”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L638)

<a id="op-08d7d0bf9cce5f"></a>
### Fetch table stats.update cardinality

`operation_foundation_core_record_definitions_recorder_business_behavior_fetch_table_stats_update_cardinality`

**Inputs** column, value.

**Local steps**

- For each col in schema.
  - If col at “column” equals column.
    - Set col at “cardinality” from value.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L6062) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L313)

<a id="op-907f94a202c623"></a>
### Get column cardinality

`operation_foundation_core_record_definitions_recorder_business_behavior_get_column_cardinality`

**Inputs** table, column.

**Wrappers, in declaration order** redis\_cache.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text select count(distinct {column}) from {table}) at 0 at 0.

**Local steps**

- Return Platform.db.sql(formatted text select count(distinct {column}) from {table}) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L12) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L314)

<a id="op-8fe02ae9b660a1"></a>
### Get doctype name

`operation_foundation_core_record_definitions_recorder_business_behavior_get_record_type_name`

**Inputs** table\_name.

**Declared result** str.

**Explicit results** table\_name.removeprefix(“tab”).

**Local steps**

- Return table\_name.removeprefix(“tab”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L7170) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L315)

## Record · Recorder query

[Record definition](../../../../data/record-types/recorder_query.json)

<a id="op-a2e1af90a2a600"></a>
### Recorder Query.db insert

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L5933) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L347)

<a id="op-cd4e42d23d0997"></a>
### Recorder Query.load from db

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_load_from_database`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L5976) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L353)

<a id="op-a44fcf5de92ddc"></a>
### Recorder Query.db update

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_database_update`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6009) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L348)

<a id="op-35b3313f6678c3"></a>
### Recorder Query.get list

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_get_list`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6042) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L351)

<a id="op-829e5ed2748f90"></a>
### Recorder Query.get count

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_get_count`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6072) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L350)

<a id="op-249ec4aebd33eb"></a>
### Recorder Query.get stats

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_get_stats`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6102) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L352)

<a id="op-32f8542d0a6c67"></a>
### Recorder Query.delete

`operation_foundation_core_record_definitions_recorder_query_business_behavior_recorder_query_delete`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6132) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L349)

## Record · Recorder suggested index

[Record definition](../../../../data/record-types/recorder_suggested_index.json)

<a id="op-8ef65bf9661409"></a>
### Recorder Suggested Index.db insert

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6165) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L354)

<a id="op-65062cc6d8a1df"></a>
### Recorder Suggested Index.load from db

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_load_from_database`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6217) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L360)
