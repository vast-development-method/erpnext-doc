# Record lifecycle and persistence · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-c6dbe019591167"></a>
### Savepoint

`operation_foundation_database_business_behavior_savepoint`

**Inputs** catch = Exception.

**Wrappers, in declaration order** contextmanager.

**State and service calls** savepoint savepoint · rollback · release savepoint savepoint.

**Local steps**

- Attempt the following.
  - Set savepoint from empty text.join(random.sample(string.ascii\_lowercase, 10)).
  - Evaluate Platform.db.savepoint(savepoint).
  - yield no value.
- On failure (catch).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
- When the protected block completes normally.
  - Evaluate Platform.db.release\_savepoint(savepoint).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6446) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1121)

<a id="op-685d3edf020570"></a>
### Get query execution timeout

`operation_foundation_database_business_behavior_get_query_execution_timeout`

**Inputs** no declared parameters.

**Declared result** int.

**Explicit results** 0 · int((cint(timeout) × 1.5)).

**Local steps**

- Bind dependencies get\_current\_job.
- If not Platform.conf.get(“enable\_db\_statement\_timeout”).
  - Return 0.
- Set timeout from 0.
- Within suppress(Exception).
  - If getattr(Platform.local, “request”, no value).
    - Set timeout from (Platform.conf.http\_timeout or 300).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.http\_timeout → 300.
  - Otherwise.
    - If job bound to get\_current\_job().
      - Set timeout from job.timeout.
- Return int((cint(timeout) × 1.5)).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6687) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1120)

<a id="op-e6d90293494a55"></a>
### Get print sql flag

`operation_foundation_database_business_behavior_get_print_database_query_flag`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** flag\_value.

**Local steps**

- Set flag\_value from Platform.client\_cache.get\_value(“flag\_print\_sql”).
- If flag\_value is identical to no value.
  - Set flag\_value from false.
  - Evaluate Platform.client\_cache.set\_value(“flag\_print\_sql”, flag\_value).
- Return flag\_value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6953) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1119)

<a id="op-c8c30ca7230879"></a>
### Get type map

`operation_foundation_database_duckdb_database_business_behavior_get_type_map`

**Inputs** no declared parameters.

**Explicit results** mapping(“Currency” → tuple(“decimal”, “21,9”), “Int” → tuple(“int”, empty text), “Long Int” → tuple(“bigint”, “20”), “Float” → tuple(“decimal”, “21,9”), …).

**Local steps**

- Return mapping(“Currency” → tuple(“decimal”, “21,9”), “Int” → tuple(“int”, empty text), “Long Int” → tuple(“bigint”, “20”), “Float” → tuple(“decimal”, “21,9”), …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L1337) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1133)

<a id="op-5d675c2f4db410"></a>
### Get pyarrow type map

`operation_foundation_database_duckdb_database_business_behavior_get_pyarrow_type_map`

**Inputs** no declared parameters.

**Explicit results** mapping(“Currency” → pa.float64(), “Int” → pa.int32(), “Long Int” → pa.int64(), “Float” → pa.float64(), …).

**Local steps**

- Bind dependencies pa.
- Return mapping(“Currency” → pa.float64(), “Int” → pa.int32(), “Long Int” → pa.int64(), “Float” → pa.float64(), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L2149) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1132)

<a id="op-5ccc724f0d9e34"></a>
### Get latest sync

`operation_foundation_database_duckdb_database_business_behavior_get_latest_sync`

**Inputs** doctype = no value.

**Explicit results** get\_duckdb(true, sync.filename) · no value.

**Local steps**

- If (doctype and sync bound to get\_latest\_complete\_sync(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → sync bound to get\_latest\_complete\_sync(doctype).
  - Return get\_duckdb(true, sync.filename).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L84) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L990) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1131)

<a id="op-07c713cf6c41bc"></a>
### Get latest complete sync

`operation_foundation_binding_foundation_database_duckdb_database_get_latest_complete_sync`

**Inputs** doctype.

**Explicit results** syncs at 0 when syncs, otherwise no value.

**Local steps**

- Set sync from qb.DocType(“DuckDB Sync”).
- Set item from qb.DocType(“DuckDB Sync Item”).
- Set pending from qb.from\_(item).select(item.parent).where(item.synced equals 0).
- Set syncs from nested operand in the contract(nested operand in the contract).orderby(sync.creation, order = Order.desc).limit(1).run(as\_dict = true).
- Return syncs at 0 when syncs, otherwise no value.
  - Value choice on syncs — true gives syncs at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L657)

<a id="op-3d167eff00d819"></a>
### Duck DBConnection.initialize

`operation_foundation_database_duckdb_database_business_behavior_duck_database_connection_initialize`

**Inputs** self, conn.

**Local steps**

- Set self.\_conn from conn.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3152) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1125)

<a id="op-43dfeea09c19ae"></a>
### Duck DBConnection.getattr

`operation_foundation_database_duckdb_database_business_behavior_duck_database_connection_getattr`

**Inputs** self, name.

**Explicit results** getattr(self.\_conn, name).

**Local steps**

- Return getattr(self.\_conn, name).

**Values supplied outside this operation** selected callable from getattr(self.\_conn, name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3206) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1124)

<a id="op-547b5d274f35a9"></a>
### Duck DBConnection.execute

`operation_foundation_database_duckdb_database_business_behavior_duck_database_connection_execute`

**Inputs** self, query, parameters = no value.

**Explicit results** DuckDBRelation(rel).

**Local steps**

- Set rel from self.\_conn.execute(query, parameters) when parameters is distinct from no value, otherwise self.\_conn.execute(query).
  - Value choice on parameters is distinct from no value — true gives self.\_conn.execute(query, parameters), false gives self.\_conn.execute(query).
- Return DuckDBRelation(rel).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3271) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1123)

<a id="op-8e2cf760dc8bfc"></a>
### Duck DBConnection.sql

`operation_foundation_database_duckdb_database_business_behavior_duck_database_connection_database_query`

**Inputs** self, query.

**Explicit results** DuckDBRelation(self.\_conn.sql(query)).

**Local steps**

- Return DuckDBRelation(self.\_conn.sql(query)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3416) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1122)

<a id="op-63e1baa4d8e788"></a>
### Duck DBRelation.initialize

`operation_foundation_database_duckdb_database_business_behavior_duck_database_relation_initialize`

**Inputs** self, rel.

**Local steps**

- Set self.\_rel from rel.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3493) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1130)

<a id="op-6ef5baf2257fcf"></a>
### Duck DBRelation.getattr

`operation_foundation_database_duckdb_database_business_behavior_duck_database_relation_getattr`

**Inputs** self, name.

**Explicit results** getattr(self.\_rel, name).

**Local steps**

- Return getattr(self.\_rel, name).

**Values supplied outside this operation** selected callable from getattr(self.\_rel, name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3547) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1129)

<a id="op-38168b38dedaa2"></a>
### Duck DBRelation.fetchall

`operation_foundation_database_duckdb_database_business_behavior_duck_database_relation_fetchall`

**Inputs** self.

**Explicit results** list of tuple(generator of float(v) when isinstance(v, Decimal), otherwise v for v drawn from row) for row drawn from self.\_rel.fetchall().

**Local steps**

- Bind dependencies Decimal.
- Return list of tuple(generator of float(v) when isinstance(v, Decimal), otherwise v for v drawn from row) for row drawn from self.\_rel.fetchall().
  - Draw row from self.\_rel.fetchall().
  - Draw v from row.
  - Value choice on isinstance(v, Decimal) — true gives float(v), false gives v.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3612) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1126)

<a id="op-87d5cb0067c450"></a>
### Duck DBRelation.fetchone

`operation_foundation_database_duckdb_database_business_behavior_duck_database_relation_fetchone`

**Inputs** self.

**Explicit results** no value · tuple(generator of float(v) when isinstance(v, Decimal), otherwise v for v drawn from row).

**Local steps**

- Bind dependencies Decimal.
- Set row from self.\_rel.fetchone().
- If row is identical to no value.
  - Return no value.
- Return tuple(generator of float(v) when isinstance(v, Decimal), otherwise v for v drawn from row).
  - Draw v from row.
  - Value choice on isinstance(v, Decimal) — true gives float(v), false gives v.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3762) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L987) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1128)

<a id="op-8bcaa0eb0ebcc4"></a>
### Duck DBRelation.fetchmany

`operation_foundation_database_duckdb_database_business_behavior_duck_database_relation_fetchmany`

**Inputs** self, size = 1.

**Explicit results** list of tuple(generator of float(v) when isinstance(v, Decimal), otherwise v for v drawn from row) for row drawn from self.\_rel.fetchmany(size).

**Local steps**

- Bind dependencies Decimal.
- Return list of tuple(generator of float(v) when isinstance(v, Decimal), otherwise v for v drawn from row) for row drawn from self.\_rel.fetchmany(size).
  - Draw row from self.\_rel.fetchmany(size).
  - Draw v from row.
  - Value choice on isinstance(v, Decimal) — true gives float(v), false gives v.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L3934) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L986) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1127)

<a id="op-877a71bf554edf"></a>
### Start duckdb sync

`operation_foundation_database_duckdb_database_business_behavior_start_duckdb_sync`

**Inputs** no declared parameters.

**Record and data access** resolve a document from mapping(“doctype” → “DuckDB Sync”, “doc\_type” → x) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “DuckDB Sync”, “doc\_type” → x)) · call submit on doc.

**Local steps**

- Set \_dt from qb.DocType(“Doctype To Sync”).
- Set to\_sync from nested operand in the contract(nested operand in the contract).distinct().where((nested operand in the contract.parenttype.eq(“Report”) bitwise and nested operand in the contract.parentfield.eq(“doctype\_to ….
- For each x in to\_sync.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “DuckDB Sync”, “doc\_type” → x)).insert().
  - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L4100) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1134)

<a id="op-7a40a72de37204"></a>
### Maria DBException Util.is deadlocked

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_deadlocked`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 belongs to tuple(ER.LOCK\_DEADLOCK, ER.CHECKREAD)).

**Local steps**

- Return (e.args and e.args at 0 belongs to tuple(ER.LOCK\_DEADLOCK, ER.CHECKREAD)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 belongs to tuple(ER.LOCK\_DEADLOCK, ER.CHECKREAD).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L336) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1341)

<a id="op-bafbb7265ef408"></a>
### Maria DBException Util.is timedout

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_timedout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.LOCK\_WAIT\_TIMEOUT).

**Local steps**

- Return (e.args and e.args at 0 equals ER.LOCK\_WAIT\_TIMEOUT).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.LOCK\_WAIT\_TIMEOUT.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L439) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1352)

<a id="op-45e69f20a22e5f"></a>
### Maria DBException Util.is read only mode error

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_read_only_mode_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals 1792).

**Local steps**

- Return (e.args and e.args at 0 equals 1792).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals 1792.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L529) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1348)

<a id="op-c3c106ff58ffda"></a>
### Maria DBException Util.is table missing

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_table_missing`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.NO\_SUCH\_TABLE).

**Local steps**

- Return (e.args and e.args at 0 equals ER.NO\_SUCH\_TABLE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.NO\_SUCH\_TABLE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L615) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1351)

<a id="op-672dd2434fc5a1"></a>
### Maria DBException Util.is missing table

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_missing_table`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** MariaDBDatabase.is\_table\_missing(e).

**Local steps**

- Return MariaDBDatabase.is\_table\_missing(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L705) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1346)

<a id="op-e7f108a39cfe2a"></a>
### Maria DBException Util.is missing column

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_missing_column`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.BAD\_FIELD\_ERROR).

**Local steps**

- Return (e.args and e.args at 0 equals ER.BAD\_FIELD\_ERROR).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.BAD\_FIELD\_ERROR.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L771) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1345)

<a id="op-61dee021861589"></a>
### Maria DBException Util.is duplicate fieldname

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_duplicate_fieldname`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.DUP\_FIELDNAME).

**Local steps**

- Return (e.args and e.args at 0 equals ER.DUP\_FIELDNAME).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.DUP\_FIELDNAME.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L861) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1343)
