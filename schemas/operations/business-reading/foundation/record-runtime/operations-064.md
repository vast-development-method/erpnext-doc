# Record lifecycle and persistence · operations 64

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Module def

[Record definition](../../../../data/record-types/module_def.json)

<a id="op-b1f912770f9dbf"></a>
### Get installed apps

`operation_foundation_core_record_definitions_module_def_business_behavior_get_installed_apps`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** json.dumps(Platform.get\_installed\_apps()).

**Local steps**

- Return json.dumps(Platform.get\_installed\_apps()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L5947) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1662)

## Record · Module profile

[Record definition](../../../../data/record-types/module_profile.json)

<a id="op-8dba81e5d6f227"></a>
### Module Profile.onload

`operation_foundation_core_record_definitions_module_profile_business_behavior_module_profile_onload`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies has\_permission.
- Bind dependencies get\_blockable\_module\_names.
- If not has\_permission(self.doctype, “write”, self, print\_logs = false).
  - Return no value.
- Evaluate self.set\_onload(“all\_modules”, get\_blockable\_module\_names(blocked = list of d.module for d drawn from self.block\_modules)).
  - Draw d from self.block\_modules.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from has\_permission(self.doctype, “write”, self, print\_logs = false).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L82) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1699)

<a id="op-00be387c8bec6c"></a>
### Module Profile.get permission log options

`operation_foundation_core_record_definitions_module_profile_business_behavior_module_profile_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0089.json#L5118) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1697)

<a id="op-376f05a37b3cc7"></a>
### Module Profile.on update

`operation_foundation_core_record_definitions_module_profile_business_behavior_module_profile_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_cache().
- Evaluate self.queue\_action(“update\_all\_users”, now = (Platform.flags.in\_test or Platform.flags.in\_install), enqueue\_after\_commit = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_test → Platform.flags.in\_install.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0089.json#L5192) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1698)

<a id="op-3c767335d4d879"></a>
### Module Profile.update all users

`operation_foundation_core_record_definitions_module_profile_business_behavior_module_profile_update_all_users`

**Inputs** self.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Local steps**

- Set block\_module from Platform.qb.DocType(“Block Module”).
- Set user from Platform.qb.DocType(“User”).
- Set all\_current\_modules from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.module\_profile equals nested operand in the contract.name).select(user.name, block\_module.module).run().
- Set user\_modules from defaultdict(set).
- For each tuple(user, module) in all\_current\_modules.
  - Evaluate user\_modules at user.add(module).
- Set module\_profile\_modules from set of module.module for module drawn from self.block\_modules.
  - Draw module from self.block\_modules.
- For each tuple(user\_name, modules) in user\_modules.items().
  - If modules differs from module\_profile\_modules.
    - Set user from Platform.get\_doc(“User”, user\_name).
    - Set user.block\_modules from list().
    - For each module in module\_profile\_modules.
      - Evaluate user.append(“block\_modules”, mapping(“module” → module)).
    - Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0089.json#L5309) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1700)

## Service · Mysqlclient

<a id="op-99ffc524ad3a1d"></a>
### Maria DBException Util.is deadlocked

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_deadlocked`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 belongs to tuple(ER.LOCK\_DEADLOCK, ER.CHECKREAD)).

**Local steps**

- Return (e.args and e.args at 0 belongs to tuple(ER.LOCK\_DEADLOCK, ER.CHECKREAD)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 belongs to tuple(ER.LOCK\_DEADLOCK, ER.CHECKREAD).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L1763) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1277) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1394)

<a id="op-f0c9ccbac8d6c6"></a>
### Maria DBException Util.is timedout

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_timedout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.LOCK\_WAIT\_TIMEOUT).

**Local steps**

- Return (e.args and e.args at 0 equals ER.LOCK\_WAIT\_TIMEOUT).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.LOCK\_WAIT\_TIMEOUT.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L1866) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1405)

<a id="op-f5c900ae547143"></a>
### Maria DBException Util.is read only mode error

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_read_only_mode_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.CANT\_EXECUTE\_IN\_READ\_ONLY\_TRANSACTION).

**Local steps**

- Return (e.args and e.args at 0 equals ER.CANT\_EXECUTE\_IN\_READ\_ONLY\_TRANSACTION).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.CANT\_EXECUTE\_IN\_READ\_ONLY\_TRANSACTION.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L1956) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1401)

<a id="op-b3a84875cbf687"></a>
### Maria DBException Util.is table missing

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_table_missing`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.NO\_SUCH\_TABLE).

**Local steps**

- Return (e.args and e.args at 0 equals ER.NO\_SUCH\_TABLE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.NO\_SUCH\_TABLE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2046) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1404)

<a id="op-95a7f40d7b3571"></a>
### Maria DBException Util.is missing table

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_missing_table`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** MariaDBDatabase.is\_table\_missing(e).

**Local steps**

- Return MariaDBDatabase.is\_table\_missing(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2136) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1399)

<a id="op-38959160333ec1"></a>
### Maria DBException Util.is missing column

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_missing_column`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.BAD\_FIELD\_ERROR).

**Local steps**

- Return (e.args and e.args at 0 equals ER.BAD\_FIELD\_ERROR).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.BAD\_FIELD\_ERROR.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2202) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1398)

<a id="op-1a0c61a43186e7"></a>
### Maria DBException Util.is duplicate fieldname

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_duplicate_fieldname`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.DUP\_FIELDNAME).

**Local steps**

- Return (e.args and e.args at 0 equals ER.DUP\_FIELDNAME).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.DUP\_FIELDNAME.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2292) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1396)

<a id="op-568b118f7aa313"></a>
### Maria DBException Util.is duplicate entry

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_duplicate_entry`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.DUP\_ENTRY).

**Local steps**

- Return (e.args and e.args at 0 equals ER.DUP\_ENTRY).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.DUP\_ENTRY.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2382) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1395)

<a id="op-2f97c3fa248613"></a>
### Maria DBException Util.is access denied

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_access_denied`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.ACCESS\_DENIED\_ERROR).

**Local steps**

- Return (e.args and e.args at 0 equals ER.ACCESS\_DENIED\_ERROR).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.ACCESS\_DENIED\_ERROR.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2472) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1273) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1390)

<a id="op-083e20e19e0713"></a>
### Maria DBException Util.cant drop field or key

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_cant_drop_field_or_key`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.CANT\_DROP\_FIELD\_OR\_KEY).

**Local steps**

- Return (e.args and e.args at 0 equals ER.CANT\_DROP\_FIELD\_OR\_KEY).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.CANT\_DROP\_FIELD\_OR\_KEY.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2562) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1272) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1389)

<a id="op-782f0357aebc42"></a>
### Maria DBException Util.is syntax error

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_syntax_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.PARSE\_ERROR).

**Local steps**

- Return (e.args and e.args at 0 equals ER.PARSE\_ERROR).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.PARSE\_ERROR.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2652) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1403)

<a id="op-423c1471abe49f"></a>
### Maria DBException Util.is statement timeout

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_statement_timeout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER\_STATEMENT\_TIMEOUT).

**Local steps**

- Return (e.args and e.args at 0 equals ER\_STATEMENT\_TIMEOUT).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER\_STATEMENT\_TIMEOUT.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2742) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1402)

<a id="op-2d031491e38846"></a>
### Maria DBException Util.is data too long

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_data_too_long`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.DATA\_TOO\_LONG).

**Local steps**

- Return (e.args and e.args at 0 equals ER.DATA\_TOO\_LONG).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.DATA\_TOO\_LONG.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L2828) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1274) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1391)

<a id="op-9dd9e5ec4b2e22"></a>
### Maria DBException Util.is data truncated

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_data_truncated`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.TRUNCATED\_WRONG\_VALUE).

**Local steps**

- Return (e.args and e.args at 0 equals ER.TRUNCATED\_WRONG\_VALUE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.TRUNCATED\_WRONG\_VALUE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L134) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1275) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1392)

<a id="op-9c015fcac1e0a4"></a>
### Maria DBException Util.is db table size limit

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_database_table_size_limit`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.TOO\_BIG\_ROWSIZE).

**Local steps**

- Return (e.args and e.args at 0 equals ER.TOO\_BIG\_ROWSIZE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.TOO\_BIG\_ROWSIZE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3021) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1276) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1393)

<a id="op-3230f087629f3e"></a>
### Maria DBException Util.is primary key violation

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_primary_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (isinstance(e, MySQLdb.IntegrityError) and MariaDBExceptionUtil.is\_duplicate\_entry(e) and “PRIMARY” belongs to e.args at 1).

**Local steps**

- Return (isinstance(e, MySQLdb.IntegrityError) and MariaDBExceptionUtil.is\_duplicate\_entry(e) and “PRIMARY” belongs to e.args at 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(e, MySQLdb.IntegrityError) → MariaDBExceptionUtil.is\_duplicate\_entry(e) → “PRIMARY” belongs to e.args at 1.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3111) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1400)

<a id="op-e07755ed3f873f"></a>
### Maria DBException Util.is unique key violation

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_unique_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (isinstance(e, MySQLdb.IntegrityError) and MariaDBExceptionUtil.is\_duplicate\_entry(e) and “Duplicate” belongs to e.args at 1).

**Local steps**

- Return (isinstance(e, MySQLdb.IntegrityError) and MariaDBExceptionUtil.is\_duplicate\_entry(e) and “Duplicate” belongs to e.args at 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(e, MySQLdb.IntegrityError) → MariaDBExceptionUtil.is\_duplicate\_entry(e) → “Duplicate” belongs to e.args at 1.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3237) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1289) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1406)

<a id="op-e9b3ad171e2fe5"></a>
### Maria DBException Util.is interface error

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_exception_utility_is_interface_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** isinstance(e, MySQLdb.InterfaceError).

**Local steps**

- Return isinstance(e, MySQLdb.InterfaceError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3363) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1397)

<a id="op-9c56b31f56b902"></a>
### Maria DBConnection Util.get connection

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_connection_utility_get_connection`

**Inputs** self.

**Explicit results** conn.

**Local steps**

- Set conn from self.\_get\_connection().
- Set conn.auto\_reconnect from true.
- Return conn.

**Methods declared on this owner** [get connection](operations-065.md#op-b651883c1ddeea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3431) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1358)
