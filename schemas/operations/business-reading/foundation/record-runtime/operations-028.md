# Record lifecycle and persistence · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-34f5364f1bc94a"></a>
### SQLite Database.get database list

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_database_list`

**Inputs** self.

**Explicit results** list(self.db\_name).

**Local steps**

- Return list(self.db\_name).

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L4899) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1479)

<a id="op-a96ce0d6b76a70"></a>
### SQLite Database.get tables

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_tables`

**Inputs** self, cached = true.

**Explicit results** tables.

**Local steps**

- Set to\_query from not cached.
- If cached.
  - Set tables from Platform.cache.get\_value(“db\_tables”).
  - Set to\_query from not tables.
- If to\_query.
  - Set tables from self.sql(query text (SELECT), pluck = true).
  - Evaluate Platform.cache.set\_value(“db\_tables”, tables).
- Return tables.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L4945) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1486)

<a id="op-7a240847d147d8"></a>
### SQLite Database.get row size

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_row_size`

**Inputs** self, doctype.

**Declared result** int.

**Explicit failure paths** NotImplementedError(“SQLite does not support getting row size directly.”).

**Local steps**

- Raise NotImplementedError(“SQLite does not support getting row size directly.”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L5203) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1484)

<a id="op-6f0465e69f2028"></a>
### SQLite Database.execute query

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_execute_query`

**Inputs** self, query, values = no value.

**Explicit results** self.\_cursor.execute(query, (values or tuple())).

**Local steps**

- Set query from query.replace(“%s”, “?”).
- Attempt the following.
  - If isinstance(values, dict).
    - For each tuple(k, v) in values.items().
      - If (isinstance(v, str) and “'” belongs to v).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(v, str) → “'” belongs to v.
        - Set values at k from self.escape(v).
      - Otherwise.
        - Set values at k from formatted text '{v}'.
    - Set query from (query modulo or format values).
- On failure (TypeError).
  - Take no action here.
- Return self.\_cursor.execute(query, (values or tuple())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → tuple().

**Methods declared on this owner** [escape](operations-027.md#op-868a2b87b9061b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L5272) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1475)

<a id="op-8f342e2ce74942"></a>
### SQLite Database.log query

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_log_query`

**Inputs** self, query, query\_type, values, debug.

**Explicit results** mogrified\_query.

**Local steps**

- Set mogrified\_query from self.lazy\_mogrify(query, values).
- Set self.last\_query from mogrified\_query.
- Evaluate self.\_log\_query(mogrified\_query, query\_type, debug, query).
- Return mogrified\_query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L5626) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1490)

<a id="op-8d967b1a400a8f"></a>
### SQLite Database.sql

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_database_query`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** super().sql(expanded args, expanded names kwargs).

**Local steps**

- If args.
  - Set args from list(args).
  - Set args at 0 from modify\_query(args at 0).
  - Set args from tuple(args).
- Otherwise.
  - If kwargs.get(“query”).
    - Set kwargs at “query” from modify\_query(kwargs.get(“query”)).
- Return super().sql(expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L5777) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1470)

<a id="op-917f1d832686e5"></a>
### SQLite Database.sql ddl

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_database_query_data_definition_language`

**Inputs** self, query, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().sql\_ddl(query, expanded args, expanded names kwargs).
- Evaluate self.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [commit](operations-028.md#op-7d35792a43af93).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L6052) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1471)

<a id="op-6404e1c263ca7d"></a>
### SQLite Database.begin

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_begin`

**Inputs** self, read\_only (named only, default false).

**Explicit failure paths** e.

**Local steps**

- If (read\_only or Platform.flags.read\_only or self.in\_read\_only\_transaction).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in read\_only → Platform.flags.read\_only → self.in\_read\_only\_transaction.
  - If self.\_conn.
    - Evaluate self.\_conn.close().
  - Set self.\_conn from self.get\_connection(read\_only = true).
  - Set self.\_cursor from self.\_conn.cursor().
  - Set self.\_read\_only\_connection from true.
- Otherwise.
  - If getattr(self, “\_read\_only\_connection”, false).
    - Evaluate self.\_conn.close().
    - Set self.\_conn from self.get\_connection().
    - Set self.\_cursor from self.\_conn.cursor().
    - Set self.\_read\_only\_connection from false.
- Attempt the following.
  - Evaluate self.sql(“BEGIN”).
- On failure (sqlite3.OperationalError) bound to e.
  - If not self.is\_nested\_transaction\_error(e).
    - Raise e.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get connection](operations-026.md#op-a3ce78ad9016d1), [sql](operations-028.md#op-8d967b1a400a8f).

**Values supplied outside this operation** selected callable from getattr(self, “\_read\_only\_connection”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L11) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1461)

<a id="op-7d35792a43af93"></a>
### SQLite Database.commit

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_commit`

**Inputs** self, chain = no value.

**Explicit results** self.rollback() · no value.

**Local steps**

- If not self.\_conn.
  - Evaluate self.connect().
- If self.in\_read\_only\_transaction.
  - Return self.rollback().
- If self.\_disable\_transaction\_control.
  - Evaluate warnings.warn(message = TRANSACTION\_DISABLED\_MSG, stacklevel = 2).
  - Return no value.
- Evaluate self.before\_rollback.reset().
- Evaluate self.after\_rollback.reset().
- Evaluate self.before\_commit.run().
- Evaluate self.\_conn.commit().
- Set self.transaction\_writes from 0.
- Evaluate self.begin().
- Evaluate self.after\_commit.run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [rollback](operations-028.md#op-a31062d15b7ce2), [begin](operations-028.md#op-6404e1c263ca7d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L12) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1465)

<a id="op-a31062d15b7ce2"></a>
### SQLite Database.rollback

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_rollback`

**Inputs** self, save\_point (named only, default no value), chain (named only, default no value).

**Local steps**

- If not self.\_conn.
  - Evaluate self.connect().
- If save\_point.
  - Evaluate self.sql(formatted text rollback to savepoint {save\_point}).
- Otherwise.
  - If not self.\_disable\_transaction\_control.
    - Evaluate self.before\_commit.reset().
    - Evaluate self.after\_commit.reset().
    - Evaluate self.before\_rollback.run().
    - Evaluate self.\_conn.rollback().
    - Evaluate self.begin().
    - Evaluate self.after\_rollback.run().
  - Otherwise.
    - Evaluate warnings.warn(message = TRANSACTION\_DISABLED\_MSG, stacklevel = 2).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f), [begin](operations-028.md#op-6404e1c263ca7d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L6881) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1493)

<a id="op-55a40f77304c1d"></a>
### SQLite Database.get db table columns

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_database_table_columns`

**Inputs** self, table.

**Declared result** list at str.

**Explicit results** columns.

**Local steps**

- Set key from formatted text table\_columns::{table}.
- Set columns from Platform.client\_cache.get\_value(key).
- If columns is identical to no value.
  - Set columns from self.sql(formatted text PRAGMA table\_info(′{table}′), as\_dict = true).
  - Set columns from list of col at “name” for col drawn from columns.
    - Draw col from columns.
  - If columns.
    - Evaluate Platform.cache.set\_value(key, columns).
- Return columns.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L7207) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1482)

<a id="op-47504ca09dc5d4"></a>
### SQLite Database.estimate count

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_estimate_count`

**Inputs** self, doctype.

**Explicit results** cint(count at 0 at 0) · 0.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies cint.
- Set table from get\_table\_name(doctype).
- Attempt the following.
  - If count bound to self.sql(formatted text SELECT COUNT(\*) FROM ′{table}′).
    - Return cint(count at 0 at 0).
- On failure (sqlite3.OperationalError) bound to e.
  - If not self.is\_table\_missing(e).
    - Propagate the active failure.
- Return 0.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L7493) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1474)

<a id="op-6ee54bcbb39203"></a>
### SQLite Database.truncate

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_truncate`

**Inputs** self, doctype.

**Local steps**

- Set table from get\_table\_name(doctype).
- Evaluate self.sql\_ddl(formatted text DELETE FROM ′{table}′).
- Evaluate self.sql\_ddl(formatted text DELETE FROM sqlite\_sequence WHERE name='{table}').

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql ddl](operations-028.md#op-917f1d832686e5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L7762) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1496)

<a id="op-6fad6c71ce9887"></a>
### SQLite Database.check implicit commit

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_check_implicit_commit`

**Inputs** self, query, query\_type.

**Explicit failure paths** ImplicitCommitError(“This statement can cause implicit commit”, query).

**Local steps**

- If (query\_type belongs to IMPLICIT\_COMMIT\_QUERY\_TYPES and self.transaction\_writes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query\_type belongs to IMPLICIT\_COMMIT\_QUERY\_TYPES → self.transaction\_writes.
  - Raise ImplicitCommitError(“This statement can cause implicit commit”, query).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1463)

<a id="op-e6a76655ed3602"></a>
### Modify query

`operation_foundation_database_sqlite_database_business_behavior_modify_query`

**Inputs** query.

**Explicit results** query.

**Local steps**

- Set query from str(query).
- Set query from convert\_backtick\_identifiers(query).
- Set query from replace\_locate\_with\_instr(query).
- If re.search(“from tab”, query, flags = re.IGNORECASE).
  - Set query from re.sub(“from tab(&#91;a-zA-Z&#93;\*)”, “from "tab\\1"”, query, flags = re.IGNORECASE).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L125) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1455)

<a id="op-94c303a54e96eb"></a>
### Replace locate with instr

`operation_foundation_database_sqlite_database_business_behavior_replace_locate_with_instr`

**Inputs** query.

**Declared result** str.

**Explicit results** query.

**Local steps**

- If re.search(“locate\\(”, query, flags = re.IGNORECASE).
  - Set query from re.sub(“locate\\((&#91;^,&#93;+),(&#91;^)&#93;+)\\)”, “instr(\\2, \\1)”, query, flags = re.IGNORECASE).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L338) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1458)

<a id="op-bd3ce27555cfdd"></a>
### Regexp

`operation_foundation_database_sqlite_database_business_behavior_regular_expression`

**Inputs** expr, item.

**Declared result** bool.

**Explicit results** re.search(expr, item) is distinct from no value.

**Local steps**

- Return re.search(expr, item) is distinct from no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L478) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1456)

<a id="op-71c665938b9799"></a>
### Regexp replace

`operation_foundation_database_sqlite_database_business_behavior_regular_expression_replace`

**Inputs** item, pattern, repl.

**Declared result** str.

**Explicit results** re.sub(pattern, repl, item).

**Local steps**

- Return re.sub(pattern, repl, item).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L566) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1457)

## Report · Database storage usage by tables

<a id="op-940ef57f08f80e"></a>
### Execute

`operation_foundation_core_report_database_storage_usage_by_tables_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(COLUMNS, data).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set data from Platform.db.multisql(mapping(“mariadb” → query text (SELECT), “postgres” → query text (SELECT), “sqlite” → query text (WITH)), as\_dict = 1).
- Return tuple(COLUMNS, data).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L1878) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L900)

<a id="op-3276874652f7a9"></a>
### Optimize doctype

`operation_foundation_core_report_database_storage_usage_by_tables_business_behavior_optimize_record_type`

**Inputs** doctype\_name.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** enqueue with optimize\_doctype\_job.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Evaluate Platform.enqueue(optimize\_doctype\_job, queue = “long”, job\_id = formatted text optimize-{doctype\_name}, doctype\_name = doctype\_name, deduplicate = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · service or queued work from Platform.enqueue(optimize\_doctype\_job, queue = “long”, job\_id = formatted text optimize-{doctype\_name}, doctype\_name = doctype\_name, deduplicate = true).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L3106) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L901)

<a id="op-647be9e1727ccd"></a>
### Optimize doctype job

`operation_foundation_core_report_database_storage_usage_by_tables_business_behavior_optimize_record_type_job`

**Inputs** doctype\_name.

**State and service calls** execute a supplied database query.

**Local steps**

- Bind dependencies get\_table\_name.
- Set doctype\_table from get\_table\_name(doctype\_name, wrap\_in\_backticks = true).
- If Platform.db.db\_type equals “mariadb”.
  - Set query from formatted text OPTIMIZE TABLE {doctype\_table};.
- Otherwise.
  - Set query from formatted text VACUUM (ANALYZE) {doctype\_table};.
- Evaluate Platform.db.sql(query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L3262) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L902)

## Service · Db manager

<a id="op-b03b1d93adeab6"></a>
### Db Manager.initialize

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_initialize`

**Inputs** self, db = no value.

**Local steps**

- If db.
  - Set self.db from db.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L7083) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1028) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1169)

<a id="op-cfd5870423adb0"></a>
### Db Manager.get current host

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_get_current_host`

**Inputs** self.

**Explicit results** nested operand in the contract.sql(“select user()”) at 0 at 0.split(“@”) at 1.

**Local steps**

- Return nested operand in the contract.sql(“select user()”) at 0 at 0.split(“@”) at 1.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L7163) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1025) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1166)

<a id="op-c4bb556e13f5c1"></a>
### Db Manager.create user

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_create_user`

**Inputs** self, user, password, host = no value.

**Local steps**

- Set host from (host or self.get\_current\_host()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in host → self.get\_current\_host().
- Set password\_predicate from formatted text  IDENTIFIED BY '{password}' when password, otherwise empty text.
  - Value choice on password — true gives formatted text  IDENTIFIED BY '{password}', false gives empty text.
- Evaluate self.db.sql(formatted text CREATE USER IF NOT EXISTS '{user}'@'{host}'{password\_predicate}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current host](operations-028.md#op-cfd5870423adb0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L7258) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1021) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1162)
