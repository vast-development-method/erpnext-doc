# Record lifecycle and persistence · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Db query

<a id="op-ebaeeca9e28d31"></a>
### Database Query.extract tables

`operation_foundation_model_persistent_records_query_business_behavior_database_query_extract_tables`

**Inputs** self.

**Local steps**

- Set self.tables from list(formatted text ′tab{self.doctype}′).
- Set sql\_functions from list(“dayofyear(”, “extract(”, “locate(”, “strpos(”, …).
- If self.fields.
  - For each field in self.fields.
    - If (“tab” does not belong to field or “.” does not belong to field or any(generator of x for x drawn from sql\_functions where x belongs to field)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in “tab” does not belong to field → “.” does not belong to field → any(generator of x for x drawn from sql\_functions where x belongs to field).
      - Draw x from sql\_functions, keep a combination only if (x belongs to field).
      - Continue with the next iteration or loop test.
    - Set table\_name from field.split(“.”, 1) at 0.
    - For each linked\_table in self.link\_tables.
      - If linked\_table.table\_alias equals table\_name.
        - Set table\_name from linked\_table.table\_name.
        - Leave the innermost loop without its normal-exhaustion alternative.
    - If table\_name.lower().startswith(“group\_concat(”).
      - Set table\_name from table\_name at slice 13 to no value.
    - If table\_name.lower().startswith(“distinct”).
      - Set table\_name from table\_name at slice 8 to no value.strip().
    - If table\_name at 0 differs from “′”.
      - Set table\_name from formatted text ′{table\_name}′.
    - If (table\_name does not belong to self.query\_tables and table\_name does not belong to self.linked\_table\_aliases.values()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_name does not belong to self.query\_tables → table\_name does not belong to self.linked\_table\_aliases.values().
      - Evaluate self.append\_table(table\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append table](operations-030.md#op-1c634647802e34).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L5221) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1222)

<a id="op-1c634647802e34"></a>
### Database Query.append table

`operation_foundation_model_persistent_records_query_business_behavior_database_query_append_table`

**Inputs** self, table\_name.

**Local steps**

- Evaluate self.tables.append(table\_name).
- Set doctype from table\_name at slice 4 to negative 1.
- Evaluate self.check\_read\_permission(doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check read permission](operations-030.md#op-35c46e6a0c453f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L5868) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1213)

<a id="op-5aaf1d39580d19"></a>
### Database Query.append link table

`operation_foundation_model_persistent_records_query_business_behavior_database_query_append_link_table`

**Inputs** self, doctype, fieldname.

**Explicit results** linked\_table.

**Local steps**

- For each linked\_table in self.link\_tables.
  - If (linked\_table.doctype equals doctype and linked\_table.fieldname equals fieldname).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in linked\_table.doctype equals doctype → linked\_table.fieldname equals fieldname.
    - Return linked\_table.
- Evaluate self.check\_read\_permission(doctype).
- Evaluate self.linked\_table\_counter.update(tuple(doctype)).
- Set linked\_table from Platform.\_dict(doctype = doctype, fieldname = fieldname, table\_name = formatted text ′tab{doctype}′, table\_alias = formatted text ′tab{doctype}\_{self.linked\_table\_counter at doctype}′).
- Set self.linked\_table\_aliases at linked\_table.table\_alias.replace(“′”, empty text) from linked\_table.table\_name.
- Evaluate self.link\_tables.append(linked\_table).
- Return linked\_table.

**Methods declared on this owner** [check read permission](operations-030.md#op-35c46e6a0c453f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L5993) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1212)

<a id="op-35c46e6a0c453f"></a>
### Database Query.check read permission

`operation_foundation_model_persistent_records_query_business_behavior_database_query_check_read_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, parent\_doctype.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L6387) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1220)

<a id="op-ba802e007fbe6d"></a>
### Database Query.set permission map

`operation_foundation_model_persistent_records_query_business_behavior_database_query_set_permission_map`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, parent\_doctype.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L6567) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1247)

<a id="op-1a15dc1b722e15"></a>
### Database Query.set field tables

`operation_foundation_model_persistent_records_query_business_behavior_database_query_set_field_tables`

**Inputs** self.

**Local steps**

- Bind local operation \_in\_standard\_sql\_methods for subsequent calls.
- If (len(self.tables) &gt; 1 or len(self.link\_tables) &gt; 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(self.tables) &gt; 1 → len(self.link\_tables) &gt; 0.
  - For each tuple(idx, field) in enumerate(self.fields).
    - If (field is distinct from no value and “.” does not belong to field and not \_in\_standard\_sql\_methods(field)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in field is distinct from no value → “.” does not belong to field → not \_in\_standard\_sql\_methods(field).
      - Set self.fields at idx from formatted text {self.tables at 0}.{field}.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L6785) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1243)

<a id="op-85b8a4fced50af"></a>
### Database Query.set field tables.in standard sql methods

`operation_foundation_model_persistent_records_query_business_behavior_database_query_set_field_tables_in_standard_database_query_methods`

**Inputs** field.

**Explicit results** field.lower().startswith(methods).

**Local steps**

- Set methods from tuple(“count(”, “avg(”, “sum(”, “extract(”, …).
- Return field.lower().startswith(methods).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L7144) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1244)

<a id="op-12822d54a64f99"></a>
### Database Query.cast name fields

`operation_foundation_model_persistent_records_query_business_behavior_database_query_cast_name_fields`

**Inputs** self.

**Local steps**

- For each tuple(i, field) in enumerate(self.fields).
  - If field is distinct from no value.
    - Set self.fields at i from cast\_name(field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L7243) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1219)

<a id="op-4607c9b36ef962"></a>
### Database Query.get table columns

`operation_foundation_model_persistent_records_query_business_behavior_database_query_get_table_columns`

**Inputs** self.

**Explicit results** get\_table\_columns(self.doctype) · no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Return get\_table\_columns(self.doctype).
- On failure (Platform.db.TableMissingError).
  - If self.ignore\_ddl.
    - Return no value.
  - Otherwise.
    - Propagate the active failure.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L7374) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1227)

<a id="op-64f96ca1260884"></a>
### Database Query.set optional columns

`operation_foundation_model_persistent_records_query_business_behavior_database_query_set_optional_columns`

**Inputs** self.

**Local steps**

- Set self.fields at slice no value to no value from list of f for f drawn from self.fields where (f does not belong to OPTIONAL\_FIELDS or f belongs to self.columns).
  - Draw f from self.fields, keep a combination only if ((f does not belong to OPTIONAL\_FIELDS or f belongs to self.columns)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f does not belong to OPTIONAL\_FIELDS → f belongs to self.columns.
- Set self.filters at slice no value to no value from list of f for f drawn from self.filters where (f.fieldname does not belong to OPTIONAL\_FIELDS or f.fieldname belongs to self.columns).
  - Draw f from self.filters, keep a combination only if ((f.fieldname does not belong to OPTIONAL\_FIELDS or f.fieldname belongs to self.columns)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.fieldname does not belong to OPTIONAL\_FIELDS → f.fieldname belongs to self.columns.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0271.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1245)

<a id="op-137ddc8a2ffa57"></a>
### Database Query.build conditions

`operation_foundation_model_persistent_records_query_business_behavior_database_query_build_conditions`

**Inputs** self.

**Local steps**

- Set self.conditions from list().
- Set self.grouped\_or\_conditions from list().
- Evaluate self.build\_filter\_conditions(self.filters, self.conditions).
- Evaluate self.build\_filter\_conditions(self.or\_filters, self.grouped\_or\_conditions).
- If not self.flags.ignore\_permissions.
  - Set match\_conditions from self.build\_match\_conditions().
  - If match\_conditions.
    - Evaluate self.conditions.append(formatted text ({match\_conditions})).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build filter conditions](operations-030.md#op-fb46c59699a5e6), [build match conditions](operations-030.md#op-1fab21ab32b782).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L129) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1216)

<a id="op-fb46c59699a5e6"></a>
### Database Query.build filter conditions

`operation_foundation_model_persistent_records_query_business_behavior_database_query_build_filter_conditions`

**Inputs** self, filters, conditions, ignore\_permissions = no value.

**Local steps**

- If ignore\_permissions is distinct from no value.
  - Set self.flags.ignore\_permissions from ignore\_permissions.
- For each f in filters.
  - Evaluate conditions.append(self.prepare\_filter\_condition(f)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare filter condition](operations-030.md#op-ff43e8cefe3fc2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0271.json#L2526) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1217)

<a id="op-6d3e975e5b591f"></a>
### Database Query.remove field

`operation_foundation_model_persistent_records_query_business_behavior_database_query_remove_field`

**Inputs** self, idx.

**Local steps**

- If self.as\_list.
  - Set self.fields at idx from no value.
- Otherwise.
  - Evaluate self.fields.pop(idx).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0271.json#L2690) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1236)

<a id="op-98805c4c4b2fd3"></a>
### Database Query.apply fieldlevel read permissions

`operation_foundation_model_persistent_records_query_business_behavior_database_query_apply_fieldlevel_read_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Locally raised failures** PermissionError.

**Local structure** 16 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0271.json#L2798) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1214)

<a id="op-ff43e8cefe3fc2"></a>
### Database Query.prepare filter condition

`operation_foundation_model_persistent_records_query_business_behavior_database_query_prepare_filter_condition`

**Inputs** self, ft.

**Declared result** str.

**Record and data access** read ref\_doctype via get\_value · read ref\_doctype via get\_all.

**Explicit results** condition.

**Local steps**

- Bind dependencies get\_additional\_filters\_from\_hooks.
- Set additional\_filters\_config from get\_additional\_filters\_from\_hooks().
- Set f from get\_filter(self.doctype, ft, additional\_filters\_config).
- Set tname from ((“′tab” + f.doctype) + “′”).
- If tname does not belong to self.tables.
  - Evaluate self.append\_table(tname).
- Set column\_name from cast\_name(f.fieldname when “ifnull(” belongs to f.fieldname, otherwise formatted text {tname}.′{f.fieldname}′).
  - Value choice on “ifnull(” belongs to f.fieldname — true gives f.fieldname, false gives formatted text {tname}.′{f.fieldname}′.
- If f.operator.lower() belongs to additional\_filters\_config.
  - Evaluate f.update(get\_additional\_filter\_field(additional\_filters\_config, f, f.value)).
- Set meta from self.get\_meta(f.doctype).
- Set df from meta.get(“fields”, mapping(“fieldname” → f.fieldname)).
- Set df from df at 0 when df, otherwise no value.
  - Value choice on df — true gives df at 0, false gives no value.
- If (f.fieldname belongs to tuple(“\_assign”, “\_liked\_by”) and f.operator belongs to tuple(“=”, “!=”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.fieldname belongs to tuple(“\_assign”, “\_liked\_by”) → f.operator belongs to tuple(“=”, “!=”).
  - Set f.operator from “like” when f.operator equals “=”, otherwise “not like”.
    - Value choice on f.operator equals “=” — true gives “like”, false gives “not like”.
  - If (isinstance(f.value, str) and f.value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f.value, str) → f.value.
    - Set f.value from formatted text %{f.value}%.
- Set can\_be\_null from f.fieldname does not belong to tuple(“name”, “modified”, “creation”).
- Set value from no value.
- If f.operator.lower() belongs to NestedSetHierarchy.
  - Set field from meta.get\_field(f.fieldname).
  - Set ref\_doctype from field.options when field, otherwise f.doctype.
    - Value choice on field — true gives field.options, false gives f.doctype.
  - Set tuple(lft, rgt) from tuple(empty text, empty text).
  - If f.value.
    - Set tuple(lft, rgt) from (Platform.db.get\_value(ref\_doctype, f.value, list(“lft”, “rgt”)) or tuple(0, 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(ref\_doctype, f.value, list(“lft”, “rgt”)) → tuple(0, 0).
  - If f.operator.lower() belongs to tuple(“descendants of”, “not descendants of”, “descendants of (inclusive)”).
    - Set nodes from Platform.get\_all(ref\_doctype, filters = mapping(“lft” → list(“&gt;”, lft), “rgt” → list(“&lt;”, rgt)), order\_by = “lft ASC”, pluck = “name”).
    - If f.operator.lower() equals “descendants of (inclusive)”.
      - Update nodes using + list(f.value).
  - Otherwise.
    - Set nodes from Platform.get\_all(ref\_doctype, filters = mapping(“lft” → list(“&lt;”, lft), “rgt” → list(“&gt;”, rgt)), order\_by = “lft DESC”, pluck = “name”).
  - Set fallback from “''”.
  - Set value from list of Platform.db.escape(cstr(v).strip(), percent = false) for v drawn from nodes.
    - Draw v from nodes.
  - If len(value).
    - Set value from formatted text ({“, ”.join(value)}).
  - Otherwise.
    - Set value from “('')”.
  - Set f.operator from “not in” when f.operator.lower() belongs to tuple(“not ancestors of”, “not descendants of”), otherwise “in”.
    - Value choice on f.operator.lower() belongs to tuple(“not ancestors of”, “not descendants of”) — true gives “not in”, false gives “in”.
- If f.operator.lower() belongs to tuple(“in”, “not in”).
  - Update can\_be\_null using bitwise and not getattr(df, “not\_nullable”, false).
  - If f.operator.lower() equals “in”.
    - Update can\_be\_null using bitwise and (not f.value or any(generator of (v is identical to no value or v equals empty text) for v drawn from f.value)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not f.value → any(generator of (v is identical to no value or v equals empty text) for v drawn from f.value).
      - Draw v from f.value.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in v is identical to no value → v equals empty text.
  - If value is identical to no value.
    - Set values from (f.value or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.value → empty text.
    - If isinstance(values, str).
      - Attempt the following.
        - Set parsed from json.loads(values).
        - Set values from parsed when isinstance(parsed, list), otherwise list(parsed).
          - Value choice on isinstance(parsed, list) — true gives parsed, false gives list(parsed).
      - On failure (ValueError).
        - Set values from values.split(“,”).
    - Set fallback from “''”.
    - Set value from list of Platform.db.escape((cstr(v) or empty text).strip(), percent = false) for v drawn from values.
      - Draw v from values.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(v) → empty text.
    - If len(value).
      - Set value from formatted text ({“, ”.join(value)}).
    - Otherwise.
      - Set value from “('')”.
- Otherwise.
  - Set escape from true.
  - If (df and (df.fieldtype belongs to tuple(“Check”, “Float”, “Int”, “Currency”, …) or getattr(df, “not\_nullable”, false))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → (df.fieldtype belongs to tuple(“Check”, “Float”, “Int”, “Currency”, …) or getattr(df, “not\_nullable”, false)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype belongs to tuple(“Check”, “Float”, “Int”, “Currency”, …) → getattr(df, “not\_nullable”, false).
    - Set can\_be\_null from false.
  - If f.operator.lower() belongs to tuple(“previous”, “next”, “timespan”).
    - Set date\_range from get\_date\_range(f.operator.lower(), f.value).
    - Set f.operator from “between”.
    - Set f.value from date\_range.
    - Set fallback from formatted text '{FallBackDateTimeStr}'.
  - If (f.operator.lower() belongs to tuple(“&gt;”, “&gt;=”) and (f.fieldname belongs to tuple(“creation”, “modified”) or (df and (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.operator.lower() belongs to tuple(“&gt;”, “&gt;=”) → (f.fieldname belongs to tuple(“creation”, “modified”) or (df and (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.fieldname belongs to tuple(“creation”, “modified”) → (df and (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype equals “Date” → df.fieldtype equals “Datetime”.
    - Set can\_be\_null from false.
  - If (f.operator belongs to tuple(“&gt;”, “&lt;”, “&gt;=”, “&lt;=”) and f.fieldname belongs to tuple(“creation”, “modified”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.operator belongs to tuple(“&gt;”, “&lt;”, “&gt;=”, “&lt;=”) → f.fieldname belongs to tuple(“creation”, “modified”).
    - Set value from cstr(f.value).
    - Set can\_be\_null from false.
    - Set fallback from formatted text '{FallBackDateTimeStr}'.
  - Otherwise.
    - If (f.operator.lower() belongs to “between” and (f.fieldname belongs to tuple(“creation”, “modified”) or (df and (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”)))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.operator.lower() belongs to “between” → (f.fieldname belongs to tuple(“creation”, “modified”) or (df and (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.fieldname belongs to tuple(“creation”, “modified”) → (df and (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype equals “Date” → df.fieldtype equals “Datetime”.
      - Set escape from false.
      - Set can\_be\_null from false.
      - Set value from get\_between\_date\_filter(f.value, df).
      - Set fallback from formatted text '{FallBackDateTimeStr}'.
    - Otherwise.
      - If f.operator.lower() equals “is”.
        - Set fallback from “''”.
        - If f.value equals “set”.
          - Set f.operator from “!=”.
          - Set can\_be\_null from false.
        - Otherwise.
          - If f.value equals “not set”.
            - Set f.operator from “=”.
            - Set can\_be\_null from not getattr(df, “not\_nullable”, false).
        - Set f.value, value from empty text.
      - Otherwise.
        - If (df and df.fieldtype equals “Date”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Date”.
          - Set value from Platform.db.format\_date(f.value).
          - Set fallback from “'0001-01-01'”.
        - Otherwise.
          - If ((df and df.fieldtype equals “Datetime”) or isinstance(f.value, datetime.datetime)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in (df and df.fieldtype equals “Datetime”) → isinstance(f.value, datetime.datetime).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Datetime”.
            - Set value from Platform.db.format\_datetime(f.value).
            - Set fallback from formatted text '{FallBackDateTimeStr}'.
          - Otherwise.
            - If (df and df.fieldtype equals “Time”).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Time”.
              - Set value from get\_time(f.value).strftime(“%H:%M:%S.%f”).
              - Set fallback from “'00:00:00'”.
            - Otherwise.
              - If (f.operator.lower() belongs to tuple(“like”, “not like”) or (isinstance(f.value, str) and (not df or df.fieldtype does not belong to list(“Float”, “Int”, “Currency”, “Percent”, …)))).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.operator.lower() belongs to tuple(“like”, “not like”) → (isinstance(f.value, str) and (not df or df.fieldtype does not belong to list(“Float”, “Int”, “Currency”, “Percent”, …))).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f.value, str) → (not df or df.fieldtype does not belong to list(“Float”, “Int”, “Currency”, “Percent”, …)).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → df.fieldtype does not belong to list(“Float”, “Int”, “Currency”, “Percent”, …).
                - Set value from empty text when f.value is identical to no value, otherwise f.value.
                  - Value choice on f.value is identical to no value — true gives empty text, false gives f.value.
                - Set fallback from “''”.
                - If (f.operator.lower() belongs to tuple(“like”, “not like”) and isinstance(value, str)).
                  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.operator.lower() belongs to tuple(“like”, “not like”) → isinstance(value, str).
                  - Set value from value.replace(“\\”, “\\\\”).replace(“%”, “%%”).
              - Otherwise.
                - If (f.operator equals “=” and df and df.fieldtype belongs to tuple(“Link”, “Data”, “Dynamic Link”)).
                  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.operator equals “=” → df → df.fieldtype belongs to tuple(“Link”, “Data”, “Dynamic Link”).
                  - Set value from cstr(f.value).
                  - Set fallback from “''”.
                - Otherwise.
                  - If f.fieldname equals “name”.
                    - Set value from f.value when f.value is distinct from no value, otherwise empty text.
                      - Value choice on f.value is distinct from no value — true gives f.value, false gives empty text.
                    - Set fallback from “''”.
                  - Otherwise.
                    - If ((df and db\_type bound to cstr(nested operand in the contract.get(nested operand in the contract.fieldtype, one space) at 0) and db\_type belongs to tuple(“varchar”, “text”, “longtext”, “smalltext”, …)) or  ….
                      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (df and db\_type bound to cstr(nested operand in the contract.type\_map.get(df.fieldtype, one space) at 0) and db\_type belongs to tuple(“varchar”, “text”, “longtext”, “smalltext”, …)) → f.fieldname belongs to tuple(“owner”, “modified\_by”, “parent”, “parentfield”, …).
                      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → db\_type bound to cstr(nested operand in the contract.db.type\_map.get(df.fieldtype, one space) at 0) → db\_type belongs to tuple(“varchar”, “text”, “longtext”, “smalltext”, …).
                      - Set value from cstr(f.value).
                      - Set fallback from “''”.
                    - Otherwise.
                      - Set value from flt(f.value).
                      - Set fallback from 0.
  - If isinstance(f.value, Column).
    - Set can\_be\_null from false.
    - Set quote from “"” when Platform.conf.db\_type equals “postgres”, otherwise “′”.
      - Value choice on Platform.conf.db\_type equals “postgres” — true gives “"”, false gives “′”.
    - Set value from formatted text {tname}.{quote}{f.value.name}{quote}.
  - Otherwise.
    - If (escape and isinstance(value, str)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in escape → isinstance(value, str).
      - Set value from formatted text {Platform.db.escape(value, percent = false)}.
- If (self.ignore\_ifnull or not can\_be\_null or (f.value and f.operator.lower() belongs to tuple(“=”, “like”)) or “ifnull(” belongs to column\_name.lower()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.ignore\_ifnull → not can\_be\_null → (f.value and f.operator.lower() belongs to tuple(“=”, “like”)) → “ifnull(” belongs to column\_name.lower().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.value → f.operator.lower() belongs to tuple(“=”, “like”).
  - If (f.operator.lower() equals “like” and Platform.conf.get(“db\_type”) equals “postgres”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.operator.lower() equals “like” → Platform.conf.get(“db\_type”) equals “postgres”.
    - Set f.operator from “ilike”.
  - Set condition from formatted text {column\_name} {f.operator} {value}.
- Otherwise.
  - If (fallback equals value and f.operator equals “=”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fallback equals value → f.operator equals “=”.
    - Set condition from formatted text ( {column\_name} is NULL OR {column\_name} {f.operator} {value} ).
  - Otherwise.
    - If (fallback equals value and f.operator equals “!=”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fallback equals value → f.operator equals “!=”.
      - Set condition from formatted text {column\_name} {f.operator} {value}.
    - Otherwise.
      - Set condition from formatted text ifnull({column\_name}, {fallback}) {f.operator} {value}.
- Return condition.

**Methods declared on this owner** [append table](operations-030.md#op-1c634647802e34), [get meta](operations-029.md#op-79800d6d423b9a).

**Values supplied outside this operation** selected callable from getattr(df, “not\_nullable”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L2) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1232)

<a id="op-1fab21ab32b782"></a>
### Database Query.build match conditions

`operation_foundation_model_persistent_records_query_business_behavior_database_query_build_match_conditions`

**Inputs** self, as\_condition = true.

**Declared result** (str bitwise or list).

**Explicit results** conditions · self.match\_filters.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “No permission to read {0}”.format(translated self.doctype).

**Local steps**

- Set self.match\_filters from list().
- Set self.match\_conditions from list().
- Set only\_if\_shared from false.
- If not self.user.
  - Set self.user from Platform.session.user.
- If not self.tables.
  - Evaluate self.extract\_tables().
- Set role\_permissions from Platform.permissions.get\_role\_permissions(self.doctype\_meta, user = self.user).
- If (not self.doctype\_meta.istable and not role\_permissions.get(“select”) and not role\_permissions.get(“read”) and not self.flags.ignore\_permissions and not has\_any\_user\_permission\_for\_doctype(self.doctype, se ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.doctype\_meta.istable → not role\_permissions.get(“select”) → not role\_permissions.get(“read”) → not self.flags.ignore\_permissions → not has\_any\_user\_permission\_for\_doctype(self.doctype, self.user, self.reference\_doctype).
  - Set only\_if\_shared from true.
  - Set self.shared from Platform.share.get\_shared(self.doctype, self.user).
  - If not self.shared.
    - Call the validation error handler Platform.throw(translated “No permission to read {0}”.format(translated self.doctype), Platform.PermissionError).
  - Otherwise.
    - Evaluate self.conditions.append(self.get\_share\_condition()).
- Otherwise.
  - If requires\_owner\_constraint(role\_permissions).
    - Set self.\_fetch\_shared\_documents from true.
    - Evaluate self.match\_conditions.append(formatted text ′tab{self.doctype}′.′owner′ = {Platform.db.escape(self.user, percent = false)}).
  - Otherwise.
    - If (role\_permissions.get(“read”) or role\_permissions.get(“select”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in role\_permissions.get(“read”) → role\_permissions.get(“select”).
      - Set user\_permissions from Platform.permissions.get\_user\_permissions(self.user).
      - Evaluate self.add\_user\_permissions(user\_permissions).
  - If self.\_fetch\_shared\_documents.
    - Set self.shared from Platform.share.get\_shared(self.doctype, self.user).
- If as\_condition.
  - Set conditions from empty text.
  - If self.match\_conditions.
    - Set conditions from ((“((” + “) or (”.join(self.match\_conditions)) + “))”).
  - Set doctype\_conditions from self.get\_permission\_query\_conditions().
  - If doctype\_conditions.
    - Update conditions using + (“ and ” + doctype\_conditions) when conditions, otherwise doctype\_conditions.
      - Value choice on conditions — true gives (“ and ” + doctype\_conditions), false gives doctype\_conditions.
  - If (not only\_if\_shared and self.shared and conditions).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not only\_if\_shared → self.shared → conditions.
    - Set conditions from formatted text (({conditions}) or ({self.get\_share\_condition()})).
  - Return conditions.
- Otherwise.
  - Return self.match\_filters.

**Methods declared on this owner** [extract tables](operations-030.md#op-ebaeeca9e28d31), [get share condition](operations-030.md#op-da2c720387e2af), [add user permissions](operations-030.md#op-6cca087d4b1584), [get permission query conditions](operations-030.md#op-3bd2b30f9b60f6).

**Values supplied outside this operation** effective access from Platform.permissions.get\_user\_permissions(self.user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0272.json#L5584) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1218)

<a id="op-da2c720387e2af"></a>
### Database Query.get share condition

`operation_foundation_model_persistent_records_query_business_behavior_database_query_get_share_condition`

**Inputs** self.

**Explicit results** (cast\_name(formatted text ′tab{self.doctype}′.name) + formatted text  in ({“, ”.join(generator of nested operand in the contract.db.escape(s, percent = false) for s drawn from self.shared)})).

**Local steps**

- Return (cast\_name(formatted text ′tab{self.doctype}′.name) + formatted text  in ({“, ”.join(generator of nested operand in the contract.db.escape(s, percent = false) for s drawn from self.shared)})).
  - Draw s from self.shared.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0272.json#L6747) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1226)

<a id="op-6cca087d4b1584"></a>
### Database Query.add user permissions

`operation_foundation_model_persistent_records_query_business_behavior_database_query_add_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, user\_permissions.

**Local structure** 10 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L616) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1211)

<a id="op-3bd2b30f9b60f6"></a>
### Database Query.get permission query conditions

`operation_foundation_model_persistent_records_query_business_behavior_database_query_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 7 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L1156) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1225)

<a id="op-1f96cd8d9daa09"></a>
### Database Query.render permission criterion

`operation_foundation_model_persistent_records_query_business_behavior_database_query_render_permission_criterion`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, criterion.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L3) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1237)

<a id="op-f6b7a53a66a725"></a>
### Database Query.set order by

`operation_foundation_model_persistent_records_query_business_behavior_database_query_set_order_by`

**Inputs** self, args.

**Local steps**

- If (self.order\_by and self.order\_by differs from DefaultOrderBy).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.order\_by → self.order\_by differs from DefaultOrderBy.
  - Set args.order\_by from self.order\_by.
- Otherwise.
  - Set args.order\_by from empty text.
  - Set group\_function\_without\_group\_by from (len(self.fields) equals 1 and (nested operand in the contract at nested operand in the contract.lower().startswith(“count(”) or nested operand in the contract at nested operand in the contract.lower().sta ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(self.fields) equals 1 → (nested operand in the contract.fields at 0.lower().startswith(“count(”) or nested operand in the contract.fields at 0.lower().startswith(“min(”) or nested operand in the contract.fields at 0.lower().start … → not self.group\_by.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.fields at 0.lower().startswith(“count(”) → self.fields at 0.lower().startswith(“min(”) → self.fields at 0.lower().startswith(“max(”) → self.fields at 0.lower().startswith(“sum(”) → self.fields at 0.lower().startswith(“avg(”).
  - If not group\_function\_without\_group\_by.
    - Set sort\_field, sort\_order from no value.
    - If (self.doctype\_meta.sort\_field and “,” belongs to self.doctype\_meta.sort\_field).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype\_meta.sort\_field → “,” belongs to self.doctype\_meta.sort\_field.
      - Set args.order\_by from “, ”.join(generator of formatted text ′tab{self.doctype}′.′{f\_split at 0.strip()}′ {f\_split at 1.strip()} for f drawn from self.doctype\_meta.sort\_field.split(“,”) where f\_split bound to f.split(maxsplit = 2)).
        - Draw f from self.doctype\_meta.sort\_field.split(“,”), keep a combination only if (f\_split bound to f.split(maxsplit = 2)).
    - Otherwise.
      - Set sort\_field from (self.doctype\_meta.sort\_field or “creation”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype\_meta.sort\_field → “creation”.
      - Set sort\_order from ((self.doctype\_meta.sort\_field and self.doctype\_meta.sort\_order) or “desc”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.doctype\_meta.sort\_field and self.doctype\_meta.sort\_order) → “desc”.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype\_meta.sort\_field → self.doctype\_meta.sort\_order.
      - If self.order\_by.
        - Set args.order\_by from formatted text ′tab{self.doctype}′.′{(sort\_field or “creation”)}′ {(sort\_order or “desc”)}.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in sort\_field → “creation”.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in sort\_order → “desc”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L4) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1246)

<a id="op-5df0c62cf89449"></a>
### Database Query.validate order by and group by

`operation_foundation_model_persistent_records_query_business_behavior_database_query_validate_order_by_and_group_by`

**Inputs** self, parameters.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Illegal SQL Query” · validation helper — translated “Cannot use sub-query here.” · validation helper — translated query text (SELECT).format(tbl) · validation helper — translated “Cannot use {0} in order/group by”.format(field).

**Local steps**

- If not parameters.
  - Return no value.
- Set \_lower from parameters.lower().
- If ORDER\_GROUP\_PATTERN.match(\_lower).
  - Call the validation error handler Platform.throw(translated “Illegal SQL Query”).
- Set subquery\_indicators from set(“union”, “intersect”, “select\\b.\*\\bfrom”).
- Set sanitized from re.sub(“′tab&#91;^′&#93;\*′”, “ doc ”, \_lower).
- If any(generator of re.search(((“\\b” + pattern) + “\\b”), sanitized) for pattern drawn from subquery\_indicators).
  - Draw pattern from subquery\_indicators.
  - Call the validation error handler Platform.throw(translated “Cannot use sub-query here.”).
- Set blacklisted\_sql\_functions from set(“sleep”, “benchmark”, “extractvalue”, “database”, …).
- For each field in parameters.split(“,”).
  - Set field from field.strip().
  - Set full\_field\_name from (“.” belongs to field and field.startswith(“′tab”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in “.” belongs to field → field.startswith(“′tab”).
  - If full\_field\_name.
    - Set tbl from field.split(“.”, 1) at 0.
    - If tbl does not belong to self.tables.
      - If tbl.startswith(“′”).
        - Set tbl from tbl at slice 4 to negative 1.
      - Call the validation error handler Platform.throw(translated query text (SELECT).format(tbl)).
  - For each func in blacklisted\_sql\_functions.
    - If re.search(((“\\b” + re.escape(func)) + “\\W\*\\(”), field.lower()).
      - Call the validation error handler Platform.throw(translated “Cannot use {0} in order/group by”.format(field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L3016) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1249)

<a id="op-a3a8f02e420241"></a>
### Database Query.add limit

`operation_foundation_model_persistent_records_query_business_behavior_database_query_add_limit`

**Inputs** self.

**Explicit results** formatted text limit {self.limit\_page\_length} offset {self.limit\_start} · empty text.

**Local steps**

- If self.limit\_page\_length.
  - Return formatted text limit {self.limit\_page\_length} offset {self.limit\_start}.
- Otherwise.
  - Return empty text.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L3903) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1210)

<a id="op-01ba2fd253a881"></a>
### Database Query.add comment count

`operation_foundation_model_persistent_records_query_business_behavior_database_query_add_comment_count`

**Inputs** self, result.

**Local steps**

- For each r in result.
  - Set comments from r.pop(“\_comments”, no value).
  - If not (self.has\_own\_name or r.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_own\_name → r.name.
    - Continue with the next iteration or loop test.
  - Set r.\_comment\_count from comments.count(“"name"”) when comments, otherwise 0.
    - Value choice on comments — true gives comments.count(“"name"”), false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L127) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1209)
