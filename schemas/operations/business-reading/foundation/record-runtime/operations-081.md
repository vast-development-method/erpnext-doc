# Record lifecycle and persistence · operations 81

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Query

<a id="op-269e6ba82a7f5b"></a>
### SQLFunction Parser.check function field permission

`operation_foundation_database_query_business_behavior_database_query_function_parser_check_function_field_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, field\_name.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L6686) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1040) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1180)

## Record · Recorder

[Record definition](../../../../data/record-types/recorder.json)

<a id="op-ccd494922b49f2"></a>
### DBColumn.from Platform ouput

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_column_from_foundation_ouput`

**Inputs** cls, data.

**Wrappers, in declaration order** classmethod.

**Declared result** “DBColumn”.

**Explicit results** cls(name = data at “column”, cardinality = data.get(“cardinality”), is\_nullable = data at “is\_nullable”, default = data at “default”, …).

**Local steps**

- Return cls(name = data at “column”, cardinality = data.get(“cardinality”), is\_nullable = data at “is\_nullable”, default = data at “default”, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L4889) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L330)

<a id="op-299f4428ecb316"></a>
### DBIndex.eq

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_index_eq`

**Inputs** self, other.

**Declared result** bool.

**Explicit results** (self.column equals other.column and self.sequence equals other.sequence and self.table equals other.table).

**Local steps**

- Return (self.column equals other.column and self.sequence equals other.sequence and self.table equals other.table).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.column equals other.column → self.sequence equals other.sequence → self.table equals other.table.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5056) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L331)

<a id="op-611be4c9e1b09a"></a>
### DBIndex.repr

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_index_representation`

**Inputs** self.

**Explicit results** formatted text DBIndex(′{self.table}′.′{self.column}′).

**Local steps**

- Return formatted text DBIndex(′{self.table}′.′{self.column}′).

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5184) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L333)

<a id="op-d6df284fd61fa7"></a>
### DBIndex.from Platform ouput

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_index_from_foundation_ouput`

**Inputs** cls, data, table.

**Wrappers, in declaration order** classmethod.

**Declared result** “DBIndex”.

**Explicit results** cls(name = data at “name”, table = table, unique = data at “unique”, cardinality = data at “cardinality”, …).

**Local steps**

- Return cls(name = data at “name”, table = table, unique = data at “unique”, cardinality = data at “cardinality”, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5264) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L332)

<a id="op-07ec0c62f312a7"></a>
### Column Stat.post init

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_column_stat_post_initialize`

**Inputs** self.

**Local steps**

- If not self.histogram.
  - Set self.histogram from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5454) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L329)

<a id="op-06a94ae0cb46c1"></a>
### Column Stat.from Platform ouput

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_column_stat_from_foundation_ouput`

**Inputs** cls, data.

**Wrappers, in declaration order** classmethod.

**Declared result** “ColumnStat”.

**Explicit results** cls(column\_name = data at “column\_name”, avg\_frequency = data at “avg\_frequency”, avg\_length = data at “avg\_length”, nulls\_ratio = data at “nulls\_ratio”, …).

**Local steps**

- Return cls(column\_name = data at “column\_name”, avg\_frequency = data at “avg\_frequency”, avg\_length = data at “avg\_length”, nulls\_ratio = data at “nulls\_ratio”, …).
  - Value choice on data at “histogram” — true gives list of flt(bin) for bin drawn from data at “histogram”.split(“,”), false gives list().
  - Draw bin from data at “histogram”.split(“,”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5519) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L328)

<a id="op-740e2774d05a94"></a>
### DBTable.post init

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_table_post_initialize`

**Inputs** self.

**Local steps**

- If not self.schema.
  - Set self.schema from list().
- If not self.indexes.
  - Set self.indexes from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5731) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L345)

<a id="op-953798ce1cc733"></a>
### DBTable.update cardinality

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_table_update_cardinality`

**Inputs** self, column\_stats.

**Declared result** no value.

**Local steps**

- For each column\_stat in column\_stats.
  - For each col in self.schema.
    - If (col.name equals column\_stat.column\_name and not col.cardinality and column\_stat.avg\_frequency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.name equals column\_stat.column\_name → not col.cardinality → column\_stat.avg\_frequency.
      - Set col.cardinality from (self.total\_rows ÷ column\_stat.avg\_frequency).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L5831) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L346)

<a id="op-37b0edb79ea603"></a>
### DBTable.from Platform ouput

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_table_from_foundation_ouput`

**Inputs** cls, data.

**Wrappers, in declaration order** classmethod.

**Declared result** “DBTable”.

**Explicit results** cls(name = table\_name, total\_rows = data at “total\_rows”, schema = list of DBColumn.from\_Platform\_ouput(c) for c drawn from data at “schema”, indexes = list of DBIndex.from\_Platform\_ouput(i, table\_name) fo ….

**Local steps**

- Set table\_name from data at “table\_name”.
- Return cls(name = table\_name, total\_rows = data at “total\_rows”, schema = list of DBColumn.from\_Platform\_ouput(c) for c drawn from data at “schema”, indexes = list of DBIndex.from\_Platform\_ouput(i, table\_name) fo ….
  - Draw c from data at “schema”.
  - Draw i from data at “indexes”.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6008) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L343)

<a id="op-cfd54a97197882"></a>
### DBTable.has column

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_table_has_column`

**Inputs** self, column.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each col in self.schema.
  - If col.name equals column.
    - Return true.
- Return false.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6225) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L344)

<a id="op-9ab9a8bce0aad5"></a>
### DBOptimizer.post init

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_post_initialize`

**Inputs** self.

**Local steps**

- If not self.tables.
  - Set self.tables from mapping().
- Set self.parsed\_query from Parser(self.query).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6330) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L336)

<a id="op-21fdfbded1d701"></a>
### DBOptimizer.tables examined

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_tables_examined`

**Inputs** self.

**Declared result** list at str.

**Explicit results** self.parsed\_query.tables.

**Local steps**

- Return self.parsed\_query.tables.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6429) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L341)

<a id="op-c0ef0a4468312a"></a>
### DBOptimizer.update table data

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_update_table_data`

**Inputs** self, table.

**Local steps**

- Set self.tables at table.name from table.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6486) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L342)

<a id="op-a36efaf9293d0f"></a>
### DBOptimizer.convert to db index

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_convert_to_database_index`

**Inputs** self, column.

**Declared result** DBIndex.

**Explicit results** DBIndex(column = column\_name, name = column\_name, table = table).

**Local steps**

- Set tuple(column\_name, table) from tuple(no value, no value).
- If “.” belongs to column.
  - Set tuple(table, column\_name) from column.split(“.”).
- Otherwise.
  - Set column\_name from column.
  - For each tuple(table\_name, db\_table) in self.tables.items().
    - If db\_table.has\_column(column).
      - Set table from table\_name.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return DBIndex(column = column\_name, name = column\_name, table = table).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6558) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L334)

<a id="op-a923ec8212a61c"></a>
### DBOptimizer.remove existing indexes

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_remove_existing_indexes`

**Inputs** self, potential\_indexes.

**Declared result** list at DBIndex.

**Explicit results** potential\_indexes.

**Local steps**

- Bind local operation remove\_maximum\_indexes for subsequent calls.
- For each table in self.tables.values().
  - Set merged\_indexes from defaultdict(list).
  - For each index in table.indexes.
    - Evaluate merged\_indexes at index.name.append(index).
  - For each idx in merged\_indexes.values().
    - Evaluate idx.sort(key = deferred anonymous expression).
  - For each idx in merged\_indexes.values().
    - Evaluate remove\_maximum\_indexes(idx).
- Return potential\_indexes.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L6829) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L338)

<a id="op-a023cafa082986"></a>
### DBOptimizer.remove existing indexes.remove maximum indexes

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_remove_existing_indexes_remove_maximum_indexes`

**Inputs** idx.

**Explicit results** no value · remove\_maximum\_indexes(idx).

**Local steps**

- If not idx.
  - Return no value.
- Set matched\_sub\_index from list().
- For each idx\_part in list(idx).
  - Set matching\_part from list of i for i drawn from potential\_indexes where (i.column equals idx\_part.column and i.table equals idx\_part.table).
    - Draw i from potential\_indexes, keep a combination only if ((i.column equals idx\_part.column and i.table equals idx\_part.table)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in i.column equals idx\_part.column → i.table equals idx\_part.table.
  - If not matching\_part.
    - Evaluate idx.pop().
    - Return remove\_maximum\_indexes(idx).
  - Otherwise.
    - Evaluate matched\_sub\_index.extend(matching\_part).
- For each i in matched\_sub\_index.
  - Evaluate potential\_indexes.remove(i).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L7420) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L339)

<a id="op-a55a650b4a68b5"></a>
### DBOptimizer.potential indexes

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_potential_indexes`

**Inputs** self.

**Declared result** list at DBIndex.

**Explicit results** list() · self.\_remove\_existing\_indexes(possible\_db\_indexes).

**Local steps**

- Set possible\_indexes from list().
- If not self.parsed\_query.columns\_dict.
  - Return list().
- If where\_columns bound to self.parsed\_query.columns\_dict.get(“where”).
  - Evaluate possible\_indexes.extend(where\_columns).
- If join\_columns bound to self.parsed\_query.columns\_dict.get(“join”).
  - Evaluate possible\_indexes.extend(join\_columns).
- If order\_by\_columns bound to self.parsed\_query.columns\_dict.get(“order\_by”).
  - If self.parsed\_query.limit\_and\_offset.
    - Evaluate possible\_indexes.extend(order\_by\_columns).
- Set possible\_db\_indexes from list of self.\_convert\_to\_db\_index(i) for i drawn from possible\_indexes.
  - Draw i from possible\_indexes.
- Set possible\_db\_indexes from list of i for i drawn from possible\_db\_indexes where i.column does not belong to tuple(“\*”, “name”).
  - Draw i from possible\_db\_indexes, keep a combination only if (i.column does not belong to tuple(“\*”, “name”)).
- Evaluate possible\_db\_indexes.sort(key = deferred anonymous expression).
- Return self.\_remove\_existing\_indexes(possible\_db\_indexes).

**Methods declared on this owner** [convert to db index](operations-081.md#op-a36efaf9293d0f), [remove existing indexes](operations-081.md#op-a923ec8212a61c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L337)

<a id="op-af937fbd24b7bb"></a>
### DBOptimizer.suggest index

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_suggest_index`

**Inputs** self.

**Declared result** (DBIndex bitwise or no value).

**Explicit results** best\_index.

**Explicit failure paths** validation helper — (“DBTable infomation missing for: ” + “, ”.join(missing\_tables)).

**Local steps**

- If missing\_tables bound to (set(self.tables\_examined()) − set(self.tables.keys())).
  - Call the validation error handler Platform.throw((“DBTable infomation missing for: ” + “, ”.join(missing\_tables))).
- Set potential\_indexes from self.potential\_indexes().
- For each index in list(potential\_indexes).
  - Set table from self.tables at index.table.
  - Set column from next(generator of c for c drawn from table.schema where c.name equals index.column).
    - Draw c from table.schema, keep a combination only if (c.name equals index.column).
  - If (“text” belongs to column.data\_type.lower() or “json” belongs to column.data\_type.lower()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “text” belongs to column.data\_type.lower() → “json” belongs to column.data\_type.lower().
    - Evaluate potential\_indexes.remove(index).
  - Set index.cardinality from column.cardinality.
- For each index in potential\_indexes.
  - Set index.\_score from self.index\_score(index).
- Evaluate potential\_indexes.sort(key = deferred anonymous expression).
- If (potential\_indexes and best\_index bound to potential\_indexes at 0 and best\_index.\_score &lt; INDEX\_SCORE\_THRESHOLD).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in potential\_indexes → best\_index bound to potential\_indexes at 0 → best\_index.\_score &lt; INDEX\_SCORE\_THRESHOLD.
  - Return best\_index.

If control reaches the end, it returns no value.

**Methods declared on this owner** [tables examined](operations-081.md#op-21fdfbded1d701), [potential indexes](operations-081.md#op-a55a650b4a68b5), [index score](operations-081.md#op-3ab074b01cfd6c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L500) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L340)

<a id="op-3ab074b01cfd6c"></a>
### DBOptimizer.index score

`operation_foundation_core_record_definitions_recorder_persistent_records_optimizer_business_behavior_database_optimizer_index_score`

**Inputs** self, index.

**Declared result** float.

**Explicit results** (rows\_fetched\_on\_average ÷ total\_rows).

**Local steps**

- Set table from self.tables at index.table.
- Set cardinality from (index.cardinality or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in index.cardinality → 2.
- Set total\_rows from (table.total\_rows or cardinality or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in table.total\_rows → cardinality → 1.
- Set rows\_fetched\_on\_average from ((table.total\_rows or cardinality) ÷ cardinality).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in table.total\_rows → cardinality.
- Return (rows\_fetched\_on\_average ÷ total\_rows).

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L1099) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L335)

<a id="op-a27f5c65fcfecb"></a>
### Recorder.load from db

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_load_from_database`

**Inputs** self.

**Explicit failure paths** Platform.DoesNotExistError.

**Local steps**

- Set request\_data from get\_recorder\_data(self.name).
- If not request\_data.
  - Raise Platform.DoesNotExistError.
- Set request from serialize\_request(request\_data).
- Evaluate self.init\_from\_dict(request).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L14) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L326)

<a id="op-6d727b616dbbc2"></a>
### Recorder.get list

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_get_list`

**Inputs** filters = no value, start = 0, page\_length = 20, order\_by = “duration desc”.

**Wrappers, in declaration order** staticmethod.

**Explicit results** requests at slice start to (start + page\_length).

**Local steps**

- Set requests from Recorder.get\_filtered\_requests(filters).
- If order\_by\_statment bound to order\_by.
  - Set order\_by\_statment from order\_by\_statment.split(“,”) at 0.
  - If “.” belongs to order\_by\_statment.
    - Set order\_by\_statment from order\_by\_statment.split(“.”) at 1.
  - If one space belongs to order\_by\_statment.
    - Set tuple(sort\_key, sort\_order) from order\_by\_statment.split(one space, 1).
  - Otherwise.
    - Set sort\_key from order\_by\_statment.
    - Set sort\_order from “desc”.
  - Set sort\_key from sort\_key.replace(“′”, empty text).
  - Evaluate requests.sort(key = deferred anonymous expression, reverse = sort\_order equals “desc”).
- Otherwise.
  - Evaluate requests.sort(key = deferred anonymous expression, reverse = true).
- Return requests at slice start to (start + page\_length).

**Values supplied outside this operation** service or queued work from requests.sort(key = deferred anonymous expression, reverse = sort\_order equals “desc”), requests.sort(key = deferred anonymous expression, reverse = true).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L13) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L324)

<a id="op-ed7393bcf5e583"></a>
### Recorder.get count

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_get_count`

**Inputs** filters = no value.

**Wrappers, in declaration order** staticmethod.

**Explicit results** len(Recorder.get\_filtered\_requests(filters)).

**Local steps**

- Return len(Recorder.get\_filtered\_requests(filters)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L1955) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L322)

<a id="op-d07d8253e5ba36"></a>
### Recorder.get filtered requests

`operation_foundation_core_record_definitions_recorder_business_behavior_recorder_get_filtered_remote_requests`

**Inputs** filters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of req for req drawn from requests where evaluate\_filters(req, filters).

**Local steps**

- Set requests from list of serialize\_request(request) for request drawn from get\_recorder\_data().
  - Draw request from get\_recorder\_data().
- Return list of req for req drawn from requests where evaluate\_filters(req, filters).
  - Draw req from requests, keep a combination only if (evaluate\_filters(req, filters)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0095.json#L2032) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L323)
