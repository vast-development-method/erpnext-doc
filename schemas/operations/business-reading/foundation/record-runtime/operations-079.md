# Record lifecycle and persistence · operations 79

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Query

<a id="op-03865d67c902aa"></a>
### Engine.get doctype link fields

`operation_foundation_database_query_business_behavior_engine_get_record_type_link_fields`

**Inputs** self, doctype = no value.

**Explicit results** doctype\_link\_fields.

**Local steps**

- Set doctype from (doctype or self.permission\_doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.permission\_doctype.
- Set meta from Platform.get\_meta(doctype).
- Set doctype\_link\_fields from list(mapping(“options” → doctype, “fieldname” → “name”)).
- Evaluate doctype\_link\_fields.extend(meta.get\_link\_fields()).
- Return doctype\_link\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L6576) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1084) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1223)

<a id="op-229e64de04b29c"></a>
### Engine.add permission conditions

`operation_foundation_database_query_business_behavior_engine_add_permission_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L98) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1196)

<a id="op-a7be455e8f74eb"></a>
### Engine.get link table alias

`operation_foundation_binding_foundation_database_query_engine_get_link_table_alias`

**Inputs** self, doctype, link\_fieldname.

**Declared result** str.

**Explicit results** self.link\_table\_aliases at key.

**Local steps**

- Set key from tuple(doctype, link\_fieldname).
- If key does not belong to self.link\_table\_aliases.
  - Set count from (self.link\_table\_counts.get(doctype, 0) + 1).
  - Set self.link\_table\_counts at doctype from count.
  - Set self.link\_table\_aliases at key from formatted text tab\_{doctype}\_{count}.
- Return self.link\_table\_aliases at key.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L664)

<a id="op-ef8343e719e239"></a>
### Engine.get permission conditions

`operation_foundation_database_query_business_behavior_engine_get_permission_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, table.

**Explicit result forms** a value selected from the current context, no value, the result of a delegated call.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L106) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1079) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1218)

<a id="op-3f499ec001e204"></a>
### Engine.get queried tables

`operation_foundation_database_query_business_behavior_engine_get_queried_tables`

**Inputs** self.

**Declared result** list at str.

**Explicit results** list(set(tables)).

**Local steps**

- Set tables from list().
- For each table in self.query.\_from.
  - Evaluate tables.append(table.get\_sql()).
- For each join in self.query.\_joins.
  - Evaluate tables.append(join.item.get\_sql()).
- Return list(set(tables)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L645) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1082) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1221)

<a id="op-0795bf4e668a01"></a>
### Engine.get permission query conditions

`operation_foundation_database_query_business_behavior_engine_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, table.

**Explicit result forms** a structured result, a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 7 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L107) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1080) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1219)

<a id="op-964611b85f8826"></a>
### Engine.get permission type

`operation_foundation_database_query_business_behavior_engine_get_permission_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, parent\_doctype.

**Explicit result forms** a scalar literal, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L1600) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1081) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1220)

<a id="op-5ae6088983c541"></a>
### Engine.requires owner constraint

`operation_foundation_database_query_business_behavior_engine_requires_owner_constraint`

**Inputs** self, role\_permissions.

**Explicit results** no value · true.

**Local steps**

- If not role\_permissions.get(“has\_if\_owner\_enabled”).
  - Return no value.
- Set if\_owner\_perms from role\_permissions.get(“if\_owner”).
- If not if\_owner\_perms.
  - Return no value.
- For each perm\_type in tuple(“select”, “read”).
  - If (role\_permissions.get(perm\_type) and perm\_type does not belong to if\_owner\_perms).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in role\_permissions.get(perm\_type) → perm\_type does not belong to if\_owner\_perms.
    - Return no value.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L1791) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1097) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1232)

<a id="op-31d0130dbfd6de"></a>
### Engine.build match conditions

`operation_foundation_database_query_business_behavior_engine_build_match_conditions`

**Inputs** self, as\_condition = true.

**Declared result** (str bitwise or list).

**Explicit results** render\_criterion(condition) when condition, otherwise empty text · match\_filters · list().

**Local steps**

- If as\_condition.
  - Set condition from self.get\_permission\_conditions(self.doctype, self.table).
  - Return render\_criterion(condition) when condition, otherwise empty text.
    - Value choice on condition — true gives render\_criterion(condition), false gives empty text.
- If not self.ignore\_user\_permissions.
  - Set match\_filters from list().
  - Set user\_permissions from Platform.permissions.get\_user\_permissions(self.user).
  - If not user\_permissions.
    - Return match\_filters.
  - Set permission\_filters from mapping().
  - For each df in self.get\_doctype\_link\_fields(self.doctype).
    - If df.get(“ignore\_user\_permissions”).
      - Continue with the next iteration or loop test.
    - Set options from df.get(“options”).
    - If user\_permission\_values bound to user\_permissions.get(options, mapping()).
      - Set docs from list().
      - For each permission in user\_permission\_values.
        - Set applicable\_for from permission.get(“applicable\_for”).
        - Set doc from permission.get(“doc”).
        - If not applicable\_for.
          - Evaluate docs.append(doc).
        - Otherwise.
          - If (df.get(“fieldname”) equals “name” and self.reference\_doctype).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“fieldname”) equals “name” → self.reference\_doctype.
            - If applicable\_for equals self.reference\_doctype.
              - Evaluate docs.append(doc).
          - Otherwise.
            - If applicable\_for equals self.doctype.
              - Evaluate docs.append(doc).
      - If docs.
        - Set permission\_filters at options from docs.
  - If permission\_filters.
    - Evaluate match\_filters.append(permission\_filters).
  - Return match\_filters.
- Return list().

**Methods declared on this owner** [get permission conditions](operations-079.md#op-ef8343e719e239), [get doctype link fields](operations-079.md#op-03865d67c902aa).

**Values supplied outside this operation** effective access from Platform.permissions.get\_user\_permissions(self.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L104) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1069) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1209)

<a id="op-3e05d204d9ca12"></a>
### Engine.build filter conditions

`operation_foundation_database_query_business_behavior_engine_build_filter_conditions`

**Inputs** self, filters, conditions, ignore\_permissions = no value.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not filters.
  - Return no value.
- Set original\_apply\_permissions from self.apply\_permissions.
- If ignore\_permissions is distinct from no value.
  - Set self.apply\_permissions from not ignore\_permissions.
- Attempt the following.
  - Set criteria\_list from list().
  - Evaluate self.apply\_filters(filters, collect = criteria\_list).
  - Set quote\_char from “′” when self.is\_mariadb, otherwise “"”.
    - Value choice on self.is\_mariadb — true gives “′”, false gives “"”.
  - For each c in criteria\_list.
    - If self.is\_mariadb.
      - For each node in c.nodes\_().
        - If (isinstance(node, ValueWrapper) and isinstance(node.value, str)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ValueWrapper) → isinstance(node.value, str).
          - Set node.value from node.value.replace(“\\”, “\\\\”).
    - Evaluate conditions.append(c.get\_sql(with\_namespace = true, quote\_char = quote\_char)).
- On exit, including pending return or failure.
  - Set self.apply\_permissions from original\_apply\_permissions.

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply filters](operations-077.md#op-b17efaeab4b8cd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L2815) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1068) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1208)

<a id="op-365f5e3b2a667e"></a>
### Engine.get field doctype

`operation_foundation_binding_foundation_database_query_engine_get_field_doctype`

**Inputs** self, field, default.

**Declared result** str.

**Explicit results** default · get\_doctype\_name((getattr(table, “\_table\_name”, no value) or table.get\_sql())).

**Local steps**

- Set table from getattr(field, “table”, no value).
- If table is identical to no value.
  - Return default.
- Attempt the following.
  - Return get\_doctype\_name((getattr(table, “\_table\_name”, no value) or table.get\_sql())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(table, “\_table\_name”, no value) → table.get\_sql().
- On failure (Exception).
  - Return default.

**Values supplied outside this operation** selected callable from getattr(field, “table”, no value), getattr(table, “\_table\_name”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L662)

<a id="op-bd329f03932b1e"></a>
### Engine.get is set empty value

`operation_foundation_binding_foundation_database_query_engine_get_is_set_empty_value`

**Inputs** self, doctype, fieldname.

**Declared result** ((int bitwise or str) bitwise or no value).

**Explicit results** empty text · IS\_SET\_EMPTY\_VALUES.get(docfield.fieldtype, empty text) when docfield, otherwise empty text.

**Local steps**

- Bind dependencies get\_default\_df.
- Attempt the following.
  - Set docfield from (get\_default\_df(fieldname) or Platform.get\_meta(doctype).get\_field(fieldname)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_default\_df(fieldname) → Platform.get\_meta(doctype).get\_field(fieldname).
- On failure (Platform.DoesNotExistError).
  - Return empty text.
- Return IS\_SET\_EMPTY\_VALUES.get(docfield.fieldtype, empty text) when docfield, otherwise empty text.
  - Value choice on docfield — true gives IS\_SET\_EMPTY\_VALUES.get(docfield.fieldtype, empty text), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L663)

<a id="op-2c7a32bc7969f1"></a>
### Engine.is field nullable

`operation_foundation_database_query_business_behavior_engine_is_field_nullable`

**Inputs** self, doctype, fieldname.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If fieldname belongs to tuple(“name”, “modified”, “creation”).
  - Return false.
- Attempt the following.
  - If meta bound to Platform.client\_cache.get\_value(formatted text doctype\_meta::{doctype}) is identical to no value.
    - Return true.
  - If df bound to meta.get\_field(fieldname) is identical to no value.
    - Return true.
- On failure (Exception).
  - Return true.
- If df.fieldtype belongs to tuple(“Check”, “Float”, “Int”, “Currency”, …).
  - Return false.
- If getattr(df, “not\_nullable”, false).
  - Return false.
- Return true.

**Values supplied outside this operation** selected callable from getattr(df, “not\_nullable”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L3276) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1087) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1225)

<a id="op-c179a6f2640c9d"></a>
### Engine.get ifnull fallback

`operation_foundation_database_query_business_behavior_engine_get_ifnull_fallback`

**Inputs** self, doctype, fieldname.

**Declared result** str.

**Explicit results** “0” · “''” · “'0001-01-01'” · “'00:00:00'”.

**Local steps**

- Attempt the following.
  - Set meta from Platform.get\_meta(doctype).
  - Set df from meta.get\_field(fieldname).
- On failure (Exception).
  - If Platform.db.db\_type equals “postgres”.
    - Set target\_table from Platform.utils.get\_table\_name(doctype).
    - Set info\_schema from Platform.qb.Schema(“information\_schema”).
    - Set columns from info\_schema.columns.
    - Set current\_schema from Platform.conf.get(“db\_schema”, “public”).
    - Set res from nested operand in the contract(nested operand in the contract).select(columns.data\_type).where(((nested operand in the contract.table\_name equals target\_table bitwise and nested operand in the contract.col ….
    - Set data\_type from res at 0 when res, otherwise no value.
      - Value choice on res — true gives res at 0, false gives no value.
    - If data\_type belongs to tuple(“smallint”, “bigint”, “int”, “numeric”).
      - Return “0”.
  - Return “''”.
- If df is identical to no value.
  - Bind dependencies get\_default\_df.
  - Set df from get\_default\_df(fieldname).
  - If df is identical to no value.
    - Return “''”.
- Set fieldtype from df.fieldtype.
- If fieldtype belongs to tuple(“Link”, “Data”, “Dynamic Link”).
  - Return “''”.
- If fieldtype belongs to tuple(“Date”, “Datetime”).
  - Return “'0001-01-01'”.
- If fieldtype equals “Time”.
  - Return “'00:00:00'”.
- If fieldtype belongs to tuple(“Float”, “Int”, “Currency”, “Percent”, …).
  - Return “0”.
- Attempt the following.
  - Set db\_type\_info from Platform.db.type\_map.get(fieldtype, tuple(“varchar”)).
  - If db\_type\_info.
    - Set db\_type from db\_type\_info at 0 when isinstance(db\_type\_info, (tuple bitwise or list)), otherwise db\_type\_info.
      - Value choice on isinstance(db\_type\_info, (tuple bitwise or list)) — true gives db\_type\_info at 0, false gives db\_type\_info.
    - If db\_type belongs to tuple(“varchar”, “text”, “longtext”, “smalltext”, …).
      - Return “''”.
- On failure (Exception).
  - Take no action here.
- Return “''”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L3647) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1078) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1217)

<a id="op-7a0bbaf75d4027"></a>
### Engine.should apply ifnull

`operation_foundation_database_query_business_behavior_engine_should_apply_ifnull`

**Inputs** self, doctype, fieldname, operator, value.

**Declared result** bool.

**Explicit results** false · has\_null\_or\_empty · true.

**Local steps**

- If not self.db\_query\_compat.
  - Return false.
- If not self.\_is\_field\_nullable(doctype, fieldname).
  - Return false.
- If value is identical to no value.
  - Return false.
- If operator.lower() belongs to tuple(“like”, “is”).
  - Return false.
- If (operator.lower() equals “=” and value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in operator.lower() equals “=” → value.
  - Return false.
- Attempt the following.
  - Set meta from Platform.get\_meta(doctype).
  - Set df from meta.get\_field(fieldname).
- On failure (Exception).
  - Set df from no value.
- Set is\_datetime\_field from (df and df.fieldtype belongs to tuple(“Date”, “Datetime”)) when df, otherwise false.
  - Value choice on df — true gives (df and df.fieldtype belongs to tuple(“Date”, “Datetime”)), false gives false.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype belongs to tuple(“Date”, “Datetime”).
- Set is\_creation\_or\_modified from fieldname belongs to tuple(“creation”, “modified”).
- If operator.lower() belongs to tuple(“&gt;”, “&gt;=”).
  - If (is\_datetime\_field or is\_creation\_or\_modified).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_datetime\_field → is\_creation\_or\_modified.
    - Return false.
- If operator.lower() equals “between”.
  - If (is\_datetime\_field or is\_creation\_or\_modified).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_datetime\_field → is\_creation\_or\_modified.
    - Return false.
- If operator.lower() equals “in”.
  - If isinstance(value, (list bitwise or tuple)).
    - Set has\_null\_or\_empty from any(generator of (v is identical to no value or v equals empty text) for v drawn from value).
      - Draw v from value.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in v is identical to no value → v equals empty text.
    - Return has\_null\_or\_empty.
  - Return false.
- If operator.lower() equals “not in”.
  - Return true.
- If operator.lower() equals “&lt;”.
  - If (is\_datetime\_field or is\_creation\_or\_modified).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_datetime\_field → is\_creation\_or\_modified.
    - Return true.
- Return true.

**Methods declared on this owner** [is field nullable](operations-079.md#op-2c7a32bc7969f1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L4648) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1098) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1233)

<a id="op-76bd7d67c00c1e"></a>
### Dynamic Table Field.initialize

`operation_foundation_database_query_business_behavior_dynamic_table_field_initialize`

**Inputs** self, doctype, fieldname, parent\_doctype, alias = no value.

**Declared result** no value.

**Local steps**

- Set self.doctype from doctype.
- Set self.fieldname from fieldname.
- Set self.alias from alias.
- Set self.parent\_doctype from parent\_doctype.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L5505) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1193)

<a id="op-6854961618da3d"></a>
### Dynamic Table Field.str

`operation_foundation_database_query_business_behavior_dynamic_table_field_text`

**Inputs** self.

**Declared result** str.

**Explicit results** formatted text {table\_name}.{fieldname} {alias}.strip().

**Local steps**

- Set table\_name from formatted text ′tab{self.doctype}′.
- Set fieldname from formatted text ′{self.fieldname}′.
- If Platform.db.db\_type equals “postgres”.
  - Set table\_name from table\_name.replace(“′”, “"”).
  - Set fieldname from fieldname.replace(“′”, “"”).
- Set alias from formatted text AS {self.alias} when self.alias, otherwise empty text.
  - Value choice on self.alias — true gives formatted text AS {self.alias}, false gives empty text.
- Return formatted text {table\_name}.{fieldname} {alias}.strip().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L5662) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1195)

<a id="op-e012fa6b408dc2"></a>
### Dynamic Table Field.parse

`operation_foundation_database_query_business_behavior_dynamic_table_field_parse`

**Inputs** field, doctype, allow\_tab\_notation = true.

**Wrappers, in declaration order** staticmethod.

**Explicit results** no value · ChildTableField(child\_doctype\_name, child\_field, doctype, alias = alias) · LinkTableField(linked\_doctype, target\_fieldname, doctype, potential\_parent\_fieldname, alias = alias) · ChildTableField(linked\_doctype, target\_fieldname, doctype, potential\_parent\_fieldname, alias = alias).

**Local steps**

- If “.” belongs to field.
  - Set alias from no value.
  - If “ as ” belongs to field.lower().
    - Set parts from re.split(“\\s+as\\s+”, field, flags = re.IGNORECASE).
    - If len(parts) &gt; 1.
      - Set field\_part from parts at 0.strip().
      - Set alias from parts at negative 1.strip().strip(“′"'”).
      - Set field from field\_part.
  - Set child\_match from no value.
  - If allow\_tab\_notation.
    - Set child\_match from CHILD\_TABLE\_FIELD\_PATTERN.match(field).
  - If child\_match.
    - Set child\_doctype\_name from child\_match.group(1).
    - Set child\_field from child\_match.group(3).
    - If child\_doctype\_name equals doctype.
      - Return no value.
    - Return ChildTableField(child\_doctype\_name, child\_field, doctype, alias = alias).
  - Otherwise.
    - If “.” does not belong to field.
      - Return no value.
    - Set parts from field.split(“.”, 1).
    - If len(parts) differs from 2.
      - Return no value.
    - Set tuple(potential\_parent\_fieldname, target\_fieldname) from parts.
    - If (not potential\_parent\_fieldname.replace(“\_”, empty text).isalnum() or not target\_fieldname.replace(“\_”, empty text).isalnum()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not potential\_parent\_fieldname.replace(“\_”, empty text).isalnum() → not target\_fieldname.replace(“\_”, empty text).isalnum().
      - Return no value.
    - Attempt the following.
      - Set meta from Platform.get\_meta(doctype).
      - If not meta.has\_field(potential\_parent\_fieldname).
        - Return no value.
      - Set linked\_field from meta.get\_field(potential\_parent\_fieldname).
    - On failure (Exception).
      - Return no value.
    - If linked\_field.
      - Set linked\_doctype from linked\_field.options.
      - If linked\_field.fieldtype equals “Link”.
        - Return LinkTableField(linked\_doctype, target\_fieldname, doctype, potential\_parent\_fieldname, alias = alias).
      - Otherwise.
        - If linked\_field.fieldtype belongs to Platform.model.table\_fields.
          - Return ChildTableField(linked\_doctype, target\_fieldname, doctype, potential\_parent\_fieldname, alias = alias).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L5973) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1194)

<a id="op-8e61ed3757e28d"></a>
### Dynamic Table Field.apply select

`operation_foundation_database_query_business_behavior_dynamic_table_field_apply_select`

**Inputs** self, query, engine = no value.

**Declared result** QueryBuilder.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L6979) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1192)

<a id="op-2ae4b331283601"></a>
### Dynamic Table Field.apply join

`operation_foundation_database_query_business_behavior_dynamic_table_field_apply_join`

**Inputs** self, query, engine = no value.

**Declared result** QueryBuilder.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L7053) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1191)

<a id="op-f8c5249cee9722"></a>
### Child Table Field.initialize

`operation_foundation_database_query_business_behavior_child_table_field_initialize`

**Inputs** self, doctype, fieldname, parent\_doctype, parent\_fieldname = no value, alias = no value.

**Declared result** no value.

**Local steps**

- Set self.doctype from doctype.
- Set self.fieldname from fieldname.
- Set self.alias from alias.
- Set self.parent\_doctype from parent\_doctype.
- Set self.parent\_fieldname from parent\_fieldname.
- Set self.table from Platform.qb.DocType(self.doctype).
- Set self.field from self.table at self.fieldname.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L7127) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1037) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1177)

<a id="op-1d3ec6d8714c76"></a>
### Child Table Field.apply select

`operation_foundation_database_query_business_behavior_child_table_field_apply_select`

**Inputs** self, query, engine = no value.

**Declared result** QueryBuilder.

**Explicit results** query.select(getattr(table, self.fieldname).as\_((self.alias or no value))).

**Local steps**

- Set table from Platform.qb.DocType(self.doctype).
- Set query from self.apply\_join(query, engine = engine).
- Return query.select(getattr(table, self.fieldname).as\_((self.alias or no value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.alias → no value.

**Methods declared on this owner** [apply join](operations-079.md#op-d8e6073d53a3c4).

**Values supplied outside this operation** selected callable from getattr(table, self.fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L7398) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1036) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1176)

<a id="op-d8e6073d53a3c4"></a>
### Child Table Field.apply join

`operation_foundation_database_query_business_behavior_child_table_field_apply_join`

**Inputs** self, query, engine = no value.

**Declared result** QueryBuilder.

**Explicit results** query.

**Local steps**

- Set main\_table from Platform.qb.DocType(self.parent\_doctype).
- If not query.is\_joined(self.table).
  - Set join\_conditions from (self.table.parent equals main\_table.name bitwise and self.table.parenttype equals self.parent\_doctype).
  - If self.parent\_fieldname.
    - Update join\_conditions using bitwise and self.table.parentfield equals self.parent\_fieldname.
  - Set query from query.left\_join(self.table).on(join\_conditions).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L96) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1035) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1175)

<a id="op-c7de927692cbbb"></a>
### Link Table Field.initialize

`operation_foundation_database_query_business_behavior_link_table_field_initialize`

**Inputs** self, doctype, fieldname, parent\_doctype, link\_fieldname, alias = no value.

**Declared result** no value.

**Local steps**

- Evaluate super().\_\_init\_\_(doctype, fieldname, parent\_doctype, alias = alias).
- Set self.link\_fieldname from link\_fieldname.
- Set self.table from Platform.qb.DocType(self.doctype).
- Set self.field from self.table at self.fieldname.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0143.json#L7966) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1242)
