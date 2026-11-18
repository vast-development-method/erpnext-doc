# Record lifecycle and persistence · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-4d814e1f1d32e8"></a>
### Database.get table columns

`operation_foundation_database_business_behavior_database_get_table_columns`

**Inputs** self, doctype.

**Explicit results** columns.

**Explicit failure paths** self.TableMissingError(“DocType”, doctype).

**Local steps**

- Set columns from self.get\_db\_table\_columns((“tab” + doctype)).
- If not columns.
  - Raise self.TableMissingError(“DocType”, doctype).
- Return columns.

**Methods declared on this owner** [get db table columns](operations-019.md#op-b7ff16cdf13339).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3110) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1083)

<a id="op-bccfb4b0b27b7f"></a>
### Database.has column

`operation_foundation_database_business_behavior_database_has_column`

**Inputs** self, doctype, column.

**Explicit results** column belongs to self.get\_table\_columns(doctype).

**Local steps**

- Return column belongs to self.get\_table\_columns(doctype).

**Methods declared on this owner** [get table columns](operations-020.md#op-4d814e1f1d32e8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3246) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1090)

<a id="op-c3cce27b7113bb"></a>
### Database.has index

`operation_foundation_database_business_behavior_database_has_index`

**Inputs** self, table\_name, index\_name.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3328) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1091)

<a id="op-41d2bf584cd362"></a>
### Database.add index

`operation_foundation_database_business_behavior_database_add_index`

**Inputs** self, doctype, fields, index\_name = no value.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L72) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1032)

<a id="op-e28d823b9cd1eb"></a>
### Database.add unique

`operation_foundation_database_business_behavior_database_add_unique`

**Inputs** self, doctype, fields, constraint\_name = no value.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3480) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1033)

<a id="op-686b01f458272e"></a>
### Database.get index name

`operation_foundation_database_business_behavior_database_get_index_name`

**Inputs** fields.

**Wrappers, in declaration order** staticmethod.

**Explicit results** INDEX\_PATTERN.sub(empty text, index\_name).

**Local steps**

- Set index\_name from (“\_”.join(fields) + “\_index”).
- Return INDEX\_PATTERN.sub(empty text, index\_name).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3546) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1073)

<a id="op-1dd4942d79bd33"></a>
### Database.get system setting

`operation_foundation_database_business_behavior_database_get_system_setting`

**Inputs** self, key.

**Explicit results** Platform.get\_system\_settings(key).

**Local steps**

- Return Platform.get\_system\_settings(key).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(key).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3646) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1082)

<a id="op-d5690c8ca61851"></a>
### Database.close

`operation_foundation_database_business_behavior_database_close`

**Inputs** self.

**Local steps**

- If self.\_conn.
  - Evaluate self.\_conn.close().
  - Set self.\_cursor from no value.
  - Set self.\_conn from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3707) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1042)

<a id="op-38aa36b877c34d"></a>
### Database.escape

`operation_foundation_database_business_behavior_database_escape`

**Inputs** s, percent = true.

**Wrappers, in declaration order** staticmethod.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3806) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1052)

<a id="op-0093f591ac31ca"></a>
### Database.get descendants

`operation_foundation_database_business_behavior_database_get_descendants`

**Inputs** self, doctype, name.

**Explicit results** get\_descendants\_of(doctype, name, ignore\_permissions = true) · list().

**Local steps**

- Bind dependencies get\_descendants\_of.
- Attempt the following.
  - Return get\_descendants\_of(doctype, name, ignore\_permissions = true).
- On failure (Exception).
  - Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3864) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1070)

<a id="op-7888ff4fde0582"></a>
### Database.is missing table or column

`operation_foundation_database_business_behavior_database_is_missing_table_or_column`

**Inputs** self, e.

**Explicit results** (self.is\_missing\_column(e) or self.is\_table\_missing(e)).

**Local steps**

- Return (self.is\_missing\_column(e) or self.is\_table\_missing(e)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_missing\_column(e) → self.is\_table\_missing(e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L3979) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1094)

<a id="op-7a5cf058f37df5"></a>
### Database.multisql

`operation_foundation_database_business_behavior_database_multisql`

**Inputs** self, sql\_dict, values = tuple(), remaining named values kwargs.

**Explicit results** self.sql(query, values, expanded names kwargs).

**Local steps**

- Set current\_dialect from (self.db\_type or “mariadb”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.db\_type → “mariadb”.
- Set query from (sql\_dict.get(current\_dialect) or sql\_dict.get(“\*”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sql\_dict.get(current\_dialect) → sql\_dict.get(“\*”).
- Return self.sql(query, values, expanded names kwargs).

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L82) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1100)

<a id="op-f576c1110163b7"></a>
### Database.delete

`operation_foundation_database_business_behavior_database_delete`

**Inputs** self, doctype, filters = no value, debug = false, remaining named values kwargs.

**Explicit results** query.run(expanded names kwargs).

**Local steps**

- Set filters from (filters or kwargs.get(“conditions”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → kwargs.get(“conditions”).
- Set query from Platform.qb.get\_query(table = doctype, filters = filters, delete = true).
- If “debug” does not belong to kwargs.
  - Set kwargs at “debug” from debug.
- Return query.run(expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L4283) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1051)

<a id="op-f6090a1e565d19"></a>
### Database.truncate

`operation_foundation_database_business_behavior_database_truncate`

**Inputs** self, doctype.

**Explicit results** self.sql\_ddl(formatted text truncate ′{get\_table\_name(doctype)}′).

**Local steps**

- Return self.sql\_ddl(formatted text truncate ′{get\_table\_name(doctype)}′).

**Methods declared on this owner** [sql ddl](operations-018.md#op-bd7b8b43be038a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L4544) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1116)

<a id="op-fd09667befac5a"></a>
### Database.get last created

`operation_foundation_database_business_behavior_database_get_last_created`

**Inputs** self, doctype.

**Explicit results** get\_datetime(last\_record at 0.creation) · no value.

**Local steps**

- Set last\_record from self.get\_all(doctype, “creation”, limit = 1, order\_by = “creation desc”).
- If last\_record.
  - Return get\_datetime(last\_record at 0.creation).
- Otherwise.
  - Return no value.

**Methods declared on this owner** [get all](operations-018.md#op-0899a51e063d58).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L4646) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1074)

<a id="op-e2c92e10b53e14"></a>
### Database.log touched tables

`operation_foundation_database_business_behavior_database_log_touched_tables`

**Inputs** self, query, query\_type.

**Explicit results** no value.

**Local steps**

- If query\_type does not belong to QUERY\_TYPES\_FOR\_LOG\_TOUCHED\_TABLES.
  - Return no value.
- Set tables from list().
- For each regex in tuple(SINGLE\_WORD\_PATTERN, MULTI\_WORD\_PATTERN).
  - Update tables using + list of groups at 1 for groups drawn from regex.findall(query).
    - Draw groups from regex.findall(query).
- Set touched\_tables from Platform.local.flags.touched\_tables.
- If touched\_tables is identical to no value.
  - Set touched\_tables from set().
  - Set Platform.local.flags.touched\_tables from touched\_tables.
- Evaluate touched\_tables.update(tables).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L81) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L955) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1098)

<a id="op-6e5a15cb7dd1e9"></a>
### Database.bulk insert

`operation_foundation_database_business_behavior_database_bulk_insert`

**Inputs** self, doctype, fields, values, ignore\_duplicates = false, chunk\_size (named only, default 1000).

**State and service calls** call insert on query.

**Local steps**

- Set table from Platform.qb.DocType(doctype).
- Set query from Platform.qb.into(table).columns(fields).
- If ignore\_duplicates.
  - If Platform.conf.db\_type belongs to tuple(“mariadb”, “sqlite”).
    - Set query from query.ignore().
  - Otherwise.
    - If Platform.conf.db\_type equals “postgres”.
      - Set query from query.on\_conflict().do\_nothing().
- Set value\_iterator from iter(values).
- While value\_chunk bound to tuple(itertools.islice(value\_iterator, chunk\_size)).
  - Evaluate query.insert(expanded value\_chunk).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L5103) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1036)

<a id="op-1e5d5b7a3d2610"></a>
### Database.create sequence

`operation_foundation_database_business_behavior_database_create_sequence`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** create\_sequence(expanded args, expanded names kwargs).

**Local steps**

- Bind dependencies create\_sequence.
- Return create\_sequence(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L5781) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1047)

<a id="op-a0c02f9b5a13c9"></a>
### Database.set next sequence val

`operation_foundation_database_business_behavior_database_set_next_sequence_val`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Bind dependencies set\_next\_val.
- Evaluate set\_next\_val(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L5863) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1109)

<a id="op-a2c91a2ad835e2"></a>
### Database.get next sequence val

`operation_foundation_database_business_behavior_database_get_next_sequence_val`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** get\_next\_val(expanded args, expanded names kwargs).

**Local steps**

- Bind dependencies get\_next\_val.
- Return get\_next\_val(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L5945) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1076)

<a id="op-9c9d924b38e6ff"></a>
### Database.get row size

`operation_foundation_database_business_behavior_database_get_row_size`

**Inputs** self, doctype.

**Declared result** int.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6027) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1078)

<a id="op-eb556a5ff89719"></a>
### Database.rename column

`operation_foundation_database_business_behavior_database_rename_column`

**Inputs** self, doctype, old\_column\_name, new\_column\_name.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6083) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1102)

<a id="op-d6ab39c293dd76"></a>
### Database.unbuffered cursor

`operation_foundation_database_business_behavior_database_unbuffered_cursor`

**Inputs** self.

**Wrappers, in declaration order** contextmanager.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6161) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1117)

<a id="op-44a72d30ff1db3"></a>
### Database.get routines

`operation_foundation_database_business_behavior_database_get_routines`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.routines.routine\_name).where((nested operand in the contract.routine\_type.isin(list(“FUNCTION”, “PROCEDU ….

**Local steps**

- Set information\_schema from Platform.qb.Schema(“information\_schema”).
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.routines.routine\_name).where((nested operand in the contract.routine\_type.isin(list(“FUNCTION”, “PROCEDU ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L6208) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1077)
