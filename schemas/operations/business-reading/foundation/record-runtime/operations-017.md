# Record lifecycle and persistence · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-bd4ce4722bd221"></a>
### Get duckdb

`operation_foundation_database_initialize_business_behavior_get_duckdb`

**Inputs** read\_only = true, filename = no value.

**Explicit results** no value · DuckDBConnection(duckdb.connect(formatted text {db\_with\_abs\_path}, read\_only = read\_only)).

**Local steps**

- Bind dependencies os.
- Bind dependencies duckdb.
- Bind dependencies Platform.
- Bind dependencies DuckDBConnection.
- If not filename.
  - Return no value.
- Set db\_home from os.path.realpath(Platform.utils.get\_files\_path(is\_private = true)).
- Set db\_with\_abs\_path from os.path.join(db\_home, filename).
- Return DuckDBConnection(duckdb.connect(formatted text {db\_with\_abs\_path}, read\_only = read\_only)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L6348) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1009) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1150)

<a id="op-259f687732f01c"></a>
### Delete duckdb file

`operation_foundation_database_initialize_business_behavior_delete_duckdb_file`

**Inputs** filename = no value.

**Explicit results** no value.

**Local steps**

- Bind dependencies os.
- Bind dependencies Platform.
- Set db\_home from os.path.realpath(Platform.utils.get\_files\_path(is\_private = true)).
- Set db\_with\_abs\_path from os.path.join(db\_home, filename).
- Attempt the following.
  - Evaluate os.remove(db\_with\_abs\_path).
- On failure (FileNotFoundError).
  - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L6605) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1146)

<a id="op-251b5a8c849bc3"></a>
### Get command

`operation_foundation_database_initialize_business_behavior_get_command`

**Inputs** socket = no value, host = no value, port = no value, user = no value, password = no value, db\_name = no value, extra = no value, dump = false.

**Explicit results** tuple(bin, command, bin\_name).

**Local steps**

- Bind dependencies Platform.
- If Platform.conf.db\_type equals “mariadb”.
  - If dump.
    - Set tuple(bin, bin\_name) from tuple((which(“mariadb-dump”) or which(“mysqldump”)), “mariadb-dump”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in which(“mariadb-dump”) → which(“mysqldump”).
  - Otherwise.
    - Set tuple(bin, bin\_name) from tuple((which(“mariadb”) or which(“mysql”)), “mariadb”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in which(“mariadb”) → which(“mysql”).
  - Set command from list(formatted text --user={user}).
  - If socket.
    - Evaluate command.append(formatted text --socket={socket}).
  - Otherwise.
    - If (host and port).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in host → port.
      - Evaluate command.append(formatted text --host={host}).
      - Evaluate command.append(formatted text --port={port}).
  - If password.
    - Evaluate command.append(formatted text --password={password}).
  - If dump.
    - Evaluate command.extend(list(“--single-transaction”, “--quick”, “--lock-tables=false”)).
  - Otherwise.
    - Evaluate command.extend(list(“--pager=less -SFX”, “--safe-updates”, “--no-auto-rehash”)).
  - Evaluate command.append(db\_name).
  - If extra.
    - Evaluate command.extend(extra).
- Otherwise.
  - If Platform.conf.db\_type equals “sqlite”.
    - Set tuple(bin, bin\_name) from tuple(which(“sqlite3”), “sqlite3”).
    - Set db\_path from ((Path(Platform.get\_site\_path()) ÷ “db”) ÷ formatted text {db\_name}.db).
    - Set command from list(db\_path.as\_posix()).
    - If dump.
      - Evaluate command.append(“.dump”).
  - Otherwise.
    - If dump.
      - Set tuple(bin, bin\_name) from tuple(which(“pg\_dump”), “pg\_dump”).
    - Otherwise.
      - Set tuple(bin, bin\_name) from tuple(which(“psql”), “psql”).
    - If (socket and password).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in socket → password.
      - Set conn\_string from formatted text postgresql://{user}:{password}@/{db\_name}?host={socket}.
    - Otherwise.
      - If socket.
        - Set conn\_string from formatted text postgresql://{user}@/{db\_name}?host={socket}.
      - Otherwise.
        - If password.
          - Set conn\_string from formatted text postgresql://{user}:{password}@{host}:{port}/{db\_name}.
        - Otherwise.
          - Set conn\_string from formatted text postgresql://{user}@{host}:{port}/{db\_name}.
    - Set command from list(conn\_string).
    - If extra.
      - Evaluate command.extend(extra).
- Return tuple(bin, command, bin\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L85) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1148)

<a id="op-052f9bcc026cbe"></a>
### Database.initialize

`operation_foundation_database_business_behavior_database_initialize`

**Inputs** self, socket = no value, host = no value, user = no value, password = no value, port = no value, cur\_db\_name = no value.

**Local steps**

- Evaluate self.setup\_type\_map().
- Set self.socket from socket.
- Set self.host from host.
- Set self.port from port.
- Set self.user from user.
- Set self.password from password.
- Set self.cur\_db\_name from cur\_db\_name.
- Set self.\_conn from no value.
- Set self.transaction\_writes from 0.
- Set self.auto\_commit\_on\_many\_writes from 0.
- Set self.value\_cache from recursive\_defaultdict().
- Set self.logger from Platform.logger(“database”).
- Evaluate self.logger.setLevel(“WARNING”).
- Set self.before\_commit from CallbackManager().
- Set self.after\_commit from CallbackManager().
- Set self.before\_rollback from CallbackManager().
- Set self.after\_rollback from CallbackManager().
- Set self.\_disable\_transaction\_control from 0.
- Set self.in\_read\_only\_transaction from false.

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup type map](operations-017.md#op-6625c44b380948).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L80) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1093)

<a id="op-6625c44b380948"></a>
### Database.setup type map

`operation_foundation_database_business_behavior_database_setup_type_map`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L1822) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1112)

<a id="op-ce0c5aa6a3a32b"></a>
### Database.connect

`operation_foundation_database_business_behavior_database_connect`

**Inputs** self.

**Local steps**

- Set self.\_conn from self.get\_connection().
- Set self.\_cursor from self.\_conn.cursor().
- Attempt the following.
  - If execution\_timeout bound to get\_query\_execution\_timeout().
    - Evaluate self.set\_execution\_timeout(execution\_timeout).
- On failure (Exception) bound to e.
  - Evaluate self.logger.warning(formatted text Couldn't set execution timeout {e}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get connection](operations-017.md#op-9cd91728f9fcfb), [set execution timeout](operations-017.md#op-69ca1f3c12709d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L76) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1044)

<a id="op-69ca1f3c12709d"></a>
### Database.set execution timeout

`operation_foundation_database_business_behavior_database_set_execution_timeout`

**Inputs** self, seconds.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L83) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1107)

<a id="op-f25a16e6a18369"></a>
### Database.get execution timeout

`operation_foundation_binding_foundation_database_database_database_get_execution_timeout`

**Inputs** self.

**Declared result** float.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L654)

<a id="op-82752ef27968af"></a>
### Database.execution timeout

`operation_foundation_binding_foundation_database_database_database_execution_timeout`

**Inputs** self, seconds.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set previous\_timeout from self.get\_execution\_timeout().
- Evaluate self.set\_execution\_timeout(seconds).
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Evaluate self.set\_execution\_timeout(previous\_timeout).

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [get execution timeout](operations-017.md#op-f25a16e6a18369), [set execution timeout](operations-017.md#op-69ca1f3c12709d).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L653)

<a id="op-2545609d1fd112"></a>
### Database.use

`operation_foundation_database_business_behavior_database_use`

**Inputs** self, db\_name.

**Local steps**

- Evaluate self.\_conn.select\_db(db\_name).
- Set self.cur\_db\_name from db\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L2267) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1118)

<a id="op-9cd91728f9fcfb"></a>
### Database.get connection

`operation_foundation_database_business_behavior_database_get_connection`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L2349) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1064)

<a id="op-4728b43fdcd8a6"></a>
### Database.get database size

`operation_foundation_database_business_behavior_database_get_database_size`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L2391) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1066)

<a id="op-051e274ad35e62"></a>
### Database.transform query

`operation_foundation_database_business_behavior_database_transform_query`

**Inputs** self, query, values.

**Declared result** tuple.

**Explicit results** tuple(query, values).

**Local steps**

- Return tuple(query, values).

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L2433) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1114)

<a id="op-c5ac59bae640be"></a>
### Database.transform result

`operation_foundation_database_business_behavior_database_transform_result`

**Inputs** self, result.

**Declared result** tuple at tuple.

**Explicit results** result.

**Local steps**

- Return result.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L2505) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1115)

<a id="op-b724010c6bb693"></a>
### Database.clean up

`operation_foundation_database_business_behavior_database_clean_up`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L2596) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1040)

<a id="op-eb3702e2fa04e7"></a>
### Database.sql

`operation_foundation_database_business_behavior_database_database_query`

**Inputs** self, query, values = EmptyQueryValues, as\_dict (named only, default 0), as\_list (named only, default 0), debug (named only, default 0), ignore\_ddl (named only, default 0), auto\_commit (named only, default 0), update (named only, default no value), explain (named only, default false), run (named only, default true), pluck (named only, default false), as\_iterator (named only, default false).

**Explicit results** query · no value · tuple() · self.\_return\_as\_iterator(pluck = pluck, as\_dict = as\_dict, as\_list = as\_list, update = update) · last\_result.

**Explicit failure paths** Platform.QueryDeadlockError(e) · Platform.QueryTimeoutError(e) · validation helper with Platform.InReadOnlyMode — translated “This runs in a read-only transaction, so it can not write.” when self.in\_read\_only\_transaction, otherwise translated “Site is running in read only mode for maintenance or site update, this acti … · propagate active failure.

**Local steps**

- If isinstance(query, QueryBuilder).
  - Evaluate Platform.log(“Use run method to execute SQL queries generated by Query Builder”).
- Set debug from (debug or getattr(self, “debug”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in debug → getattr(self, “debug”, false).
- Set query from str(query).
- If not run.
  - Return query.
- Set query\_type from get\_query\_type(query).
- If explain.
  - If (debug and query\_type equals “select”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in debug → query\_type equals “select”.
    - Evaluate self.explain\_query(query, values).
  - Return no value.
- Set query from IFNULL\_PATTERN.sub(“coalesce(”, query.strip()).
- If not self.\_conn.
  - Evaluate self.connect().
- Evaluate self.check\_transaction\_status(query, query\_type).
- Evaluate self.clear\_db\_table\_cache(query\_type).
- If auto\_commit.
  - Evaluate self.commit().
- If debug.
  - Set time\_start from time().
- If values equals EmptyQueryValues.
  - Set values from no value.
- Otherwise.
  - If not isinstance(values, ALLOWED\_TYPES\_FOR\_VALUES).
    - Set values from tuple(values).
- Set tuple(query, values) from self.\_transform\_query(query, values).
- If (trace\_id bound to get\_trace\_id() and TRACE\_ID\_PATTERN.fullmatch(trace\_id)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in trace\_id bound to get\_trace\_id() → TRACE\_ID\_PATTERN.fullmatch(trace\_id).
  - Update query using + formatted text  /\* Platform\_TRACE\_ID: {trace\_id} \*/.
- Attempt the following.
  - Evaluate self.execute\_query(query, values).
- On failure (Exception) bound to e.
  - If self.is\_syntax\_error(e).
    - Evaluate Platform.log(formatted text Syntax error in query: {query} {(values or empty text)}).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → empty text.
  - Otherwise.
    - If self.is\_deadlocked(e).
      - Raise Platform.QueryDeadlockError(e) with cause e.
    - Otherwise.
      - If self.is\_timedout(e).
        - Raise Platform.QueryTimeoutError(e) with cause e.
      - Otherwise.
        - If self.is\_read\_only\_mode\_error(e).
          - Call the validation error handler Platform.throw(translated “This runs in a read-only transaction, so it can not write.” when self.in\_read\_only\_transaction, otherwise translated “Site is running in read only mode for maintenance or site up ….
            - Value choice on self.in\_read\_only\_transaction — true gives translated “This runs in a read-only transaction, so it can not write.”, false gives translated “Site is running in read only mode for maintenance or site update, this action can not be performed right now …”.
        - Otherwise.
          - If self.db\_type equals “postgres”.
            - Evaluate traceback.print\_stack().
            - Evaluate Platform.log(formatted text Error in query: {e}).
            - Propagate the active failure.
          - Otherwise.
            - If isinstance(e, self.ProgrammingError).
              - If Platform.conf.developer\_mode.
                - Evaluate traceback.print\_stack().
                - Evaluate Platform.log(formatted text Error in query: {tuple(query, values)}).
              - Propagate the active failure.
  - If not (ignore\_ddl and (self.is\_missing\_column(e) or self.is\_table\_missing(e) or self.cant\_drop\_field\_or\_key(e))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_ddl → (self.is\_missing\_column(e) or self.is\_table\_missing(e) or self.cant\_drop\_field\_or\_key(e)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_missing\_column(e) → self.is\_table\_missing(e) → self.cant\_drop\_field\_or\_key(e).
    - Propagate the active failure.
- Evaluate self.log\_query(query, query\_type, values, debug).
- If debug.
  - Set time\_end from time().
  - Evaluate Platform.log(formatted text Execution time: {((time\_end − time\_start) × 1000)} ms).
- If auto\_commit.
  - Evaluate self.commit().
- If (self.db\_type equals “postgres” and getattr(self.\_cursor, “name”, no value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.db\_type equals “postgres” → getattr(self.\_cursor, “name”, no value).
  - Evaluate self.\_cursor.fetchmany(0).
- If not self.\_cursor.description.
  - Return tuple().
- If as\_iterator.
  - Return self.\_return\_as\_iterator(pluck = pluck, as\_dict = as\_dict, as\_list = as\_list, update = update).
- Set last\_result from self.\_transform\_result(self.\_cursor.fetchall()).
- If pluck.
  - Set last\_result from list of r at 0 for r drawn from last\_result.
    - Draw r from last\_result.
  - Evaluate self.\_clean\_up().
  - Return last\_result.
- If as\_dict.
  - Set last\_result from self.fetch\_as\_dict(last\_result).
  - If update.
    - For each r in last\_result.
      - Evaluate r.update(update).
- Otherwise.
  - If as\_list.
    - Set last\_result from self.convert\_to\_lists(last\_result).
- Evaluate self.\_clean\_up().
- Return last\_result.

**Methods declared on this owner** [explain query](operations-017.md#op-83faab3278db2f), [connect](operations-017.md#op-ce0c5aa6a3a32b), [check transaction status](operations-018.md#op-8bae13939a865b), [clear db table cache](operations-018.md#op-32431aabdc7c0a), [commit](operations-019.md#op-618c1b0592a4e5), [transform query](operations-017.md#op-051e274ad35e62), [execute query](operations-017.md#op-9317bad24abf75), [log query](operations-017.md#op-aa70b17cc08fed), [return as iterator](operations-017.md#op-34a701f55ad85a), [transform result](operations-017.md#op-c5ac59bae640be), [clean up](operations-017.md#op-b724010c6bb693), [fetch as dict](operations-018.md#op-0bad9587030196), [convert to lists](operations-018.md#op-a9e772c08b0f89).

**Values supplied outside this operation** selected callable from getattr(self, “debug”, false), getattr(self.\_cursor, “name”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L77) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1048)

<a id="op-34a701f55ad85a"></a>
### Database.return as iterator

`operation_foundation_database_business_behavior_database_return_as_iterator`

**Inputs** self, pluck (named only), as\_dict (named only), as\_list (named only), update (named only).

**Explicit failure paths** validation helper — translated “′as\_iterator′ only works with ′as\_list=True′ or ′as\_dict=True′”.

**Local steps**

- While result bound to self.\_transform\_result(self.\_cursor.fetchmany(SQL\_ITERATOR\_BATCH\_SIZE)).
  - If pluck.
    - For each row in result.
      - yield row at 0.
  - Otherwise.
    - If as\_dict.
      - Set keys from list of column at 0 for column drawn from self.\_cursor.description.
        - Draw column from self.\_cursor.description.
      - For each row in result.
        - Set row from \_dict(zip(keys, row, strict = false)).
        - If update.
          - Evaluate row.update(update).
        - yield row.
    - Otherwise.
      - If as\_list.
        - For each row in result.
          - yield list(row).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “′as\_iterator′ only works with ′as\_list=True′ or ′as\_dict=True′”).
- Evaluate self.\_clean\_up().

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [transform result](operations-017.md#op-c5ac59bae640be), [clean up](operations-017.md#op-b724010c6bb693).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L4886) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1103)

<a id="op-9317bad24abf75"></a>
### Database.execute query

`operation_foundation_database_business_behavior_database_execute_query`

**Inputs** self, query, values = no value.

**Explicit results** self.\_cursor.execute(query, values).

**Local steps**

- Return self.\_cursor.execute(query, values).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L5315) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1055)

<a id="op-bafb3a2b6eed5f"></a>
### Database.log query

`operation_foundation_database_business_behavior_database_log_query`

**Inputs** self, mogrified\_query, query\_type, debug = false, unmogrified\_query = empty text.

**Declared result** no value.

**Local steps**

- Set \_query from no value.
- Set conf from Platform.local.conf.
- If (conf.allow\_tests and get\_print\_sql\_flag()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in conf.allow\_tests → get\_print\_sql\_flag().
  - Set \_query from (\_query or str(mogrified\_query)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_query → str(mogrified\_query).
  - Evaluate print(\_query).
- If debug.
  - Set \_query from (\_query or str(mogrified\_query)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_query → str(mogrified\_query).
  - Evaluate Platform.log(\_query).
- If conf.logging equals 2.
  - Set \_query from (\_query or str(mogrified\_query)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_query → str(mogrified\_query).
  - Evaluate Platform.log(formatted text #### query {\_query} ####).
- If query\_type belongs to DDL\_QUERY\_TYPES.
  - Set \_query from (\_query or str(mogrified\_query)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_query → str(mogrified\_query).
  - Evaluate self.logger.warning((“DDL Query made to DB:\\n” + \_query)).
- If Platform.local.flags.in\_migrate.
  - Set \_query from (\_query or str(mogrified\_query)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_query → str(mogrified\_query).
  - Evaluate self.log\_touched\_tables(\_query, query\_type).

If control reaches the end, it returns no value.

**Methods declared on this owner** [log touched tables](operations-020.md#op-e2c92e10b53e14).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L5394) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1096)

<a id="op-aa70b17cc08fed"></a>
### Database.log query

`operation_foundation_database_business_behavior_database_log_query_2`

**Inputs** self, query, query\_type, values = no value, debug = false.

**Declared result** str.

**Explicit results** mogrified\_query.

**Local steps**

- Set mogrified\_query from self.lazy\_mogrify(query, values).
- Evaluate self.\_log\_query(mogrified\_query, query\_type, debug, query).
- Return mogrified\_query.

**Methods declared on this owner** [lazy mogrify](operations-017.md#op-33eee522891119), [log query](operations-017.md#op-bafb3a2b6eed5f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L5947) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1097)

<a id="op-42a5c53ee86354"></a>
### Database.mogrify

`operation_foundation_database_business_behavior_database_mogrify`

**Inputs** self, query, values.

**Explicit results** query · self.\_cursor.mogrify(query, values) · (query modulo or format mapping of k → Platform.db.escape(v) when isinstance(v, str), otherwise v for tuple(k, v) drawn from values.items()) · (query modulo or format tuple(generator of nested operand in the contract.db.escape(v) when isinstance(v, str), otherwise v for v drawn from values)) · tuple(query, values).

**Local steps**

- If not values.
  - Return query.
- Attempt the following.
  - Return self.\_cursor.mogrify(query, values).
- On failure (AttributeError).
  - If isinstance(values, dict).
    - Return (query modulo or format mapping of k → Platform.db.escape(v) when isinstance(v, str), otherwise v for tuple(k, v) drawn from values.items()).
      - Draw tuple(k, v) from values.items().
      - Value choice on isinstance(v, str) — true gives Platform.db.escape(v), false gives v.
  - Otherwise.
    - If isinstance(values, (list bitwise or tuple)).
      - Return (query modulo or format tuple(generator of nested operand in the contract.db.escape(v) when isinstance(v, str), otherwise v for v drawn from values)).
        - Draw v from values.
        - Value choice on isinstance(v, str) — true gives Platform.db.escape(v), false gives v.
  - Return tuple(query, values).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L6114) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1099)

<a id="op-33eee522891119"></a>
### Database.lazy mogrify

`operation_foundation_database_business_behavior_database_lazy_mogrify`

**Inputs** self, query, values.

**Declared result** LazyMogrify.

**Explicit results** LazyMogrify(query, values).

**Local steps**

- Return LazyMogrify(query, values).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L6510) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1095)

<a id="op-83faab3278db2f"></a>
### Database.explain query

`operation_foundation_database_business_behavior_database_explain_query`

**Inputs** self, query, values = EmptyQueryValues.

**Local steps**

- Evaluate Platform.log(“--- query explain ---”).
- Attempt the following.
  - Set results from self.sql(formatted text EXPLAIN {query}, values, as\_dict = 1).
- On failure (Exception) bound to e.
  - Evaluate Platform.log(formatted text error in query explain: {e}).
- When the protected block completes normally.
  - Evaluate Platform.log(json.dumps(results, indent = 1)).
  - Evaluate Platform.log(“--- query explain end ---”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L6590) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1057)

<a id="op-ca644bac64d66f"></a>
### Database.sql list

`operation_foundation_database_business_behavior_database_database_query_list`

**Inputs** self, query, values = tuple(), debug = false, remaining named values kwargs.

**Explicit results** self.sql(query, values, expanded names kwargs, debug = debug, pluck = true).

**Local steps**

- Return self.sql(query, values, expanded names kwargs, debug = debug, pluck = true).

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L6854) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1050)
