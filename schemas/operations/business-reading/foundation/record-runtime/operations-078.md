# Record lifecycle and persistence · operations 78

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Query

<a id="op-7ca1cfbeb14d76"></a>
### Engine.apply filter

`operation_foundation_database_query_business_behavior_engine_apply_filter`

**Inputs** self, field, value, operator = “=”, doctype = no value, collect = no value.

**Local steps**

- Set criterion from self.\_build\_criterion\_for\_simple\_filter(field, value, operator, doctype).
- If criterion.
  - If collect is distinct from no value.
    - Evaluate collect.append(criterion).
  - Otherwise.
    - Set self.query from self.query.where(criterion).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build criterion for simple filter](operations-078.md#op-733ad4f79b58e3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0140.json#L704) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1060) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1200)

<a id="op-733ad4f79b58e3"></a>
### Engine.build criterion for simple filter

`operation_foundation_database_query_business_behavior_engine_build_criterion_for_simple_filter`

**Inputs** self, field, value, operator = “=”, doctype = no value.

**Declared result** “Criterion \| None”.

**Explicit results** operator\_fn(\_field, (nodes or tuple(empty text))) · func\_is(\_field, \_value, self.\_get\_is\_set\_empty\_value(filter\_doctype, \_field.name)) · operator\_fn(\_field, ValueWrapper(fallback\_value)) · \_field.isnull() · operator\_fn(\_field, \_value) · 1 additional forms in the steps below.

**Explicit failure paths** validation helper — translated “Document cannot be used as a filter value”.

**Local steps**

- Bind dependencies builtin\_operator.
- Set additional\_filters\_config from get\_additional\_filters\_from\_hooks().
- If operator.lower() belongs to additional\_filters\_config.
  - Set f from Platform.\_dict(doctype = (doctype or self.doctype), fieldname = field, operator = operator, value = value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
  - Bind dependencies get\_additional\_filter\_field.
  - Set resolved from get\_additional\_filter\_field(additional\_filters\_config, f, value).
  - Set operator from resolved.get(“operator”).
  - Set value from resolved.get(“value”, value).
- Set \_field from self.\_validate\_and\_prepare\_filter\_field(field, doctype).
- If isinstance(value, Field).
  - Set \_value from value.
- Otherwise.
  - Set \_value from convert\_to\_value(value).
- If isinstance(value, Document).
  - Call the validation error handler Platform.throw(translated “Document cannot be used as a filter value”).
- Set \_operator from operator.
- If (isinstance(field, str) and field belongs to tuple(“\_assign”, “\_liked\_by”) and \_operator belongs to tuple(“=”, “!=”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(field, str) → field belongs to tuple(“\_assign”, “\_liked\_by”) → \_operator belongs to tuple(“=”, “!=”).
  - Set \_operator from “like” when \_operator equals “=”, otherwise “not like”.
    - Value choice on \_operator equals “=” — true gives “like”, false gives “not like”.
  - If (isinstance(\_value, str) and \_value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(\_value, str) → \_value.
    - Set \_value from formatted text %{\_value}%.
- If \_operator.lower() belongs to tuple(“timespan”, “previous”, “next”).
  - Bind dependencies get\_date\_range.
  - Set \_value from get\_date\_range(\_operator.lower(), \_value).
  - Set \_operator from “between”.
- If (isinstance(\_value, datetime.datetime) or (isinstance(\_value, (list bitwise or tuple)) and any(generator of isinstance(v, datetime.datetime) for v drawn from \_value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(\_value, datetime.datetime) → (isinstance(\_value, (list bitwise or tuple)) and any(generator of isinstance(v, datetime.datetime) for v drawn from \_value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(\_value, (list bitwise or tuple)) → any(generator of isinstance(v, datetime.datetime) for v drawn from \_value).
  - Draw v from \_value.
  - Set \_value from \_apply\_date\_field\_filter\_conversion(\_value, \_operator, (doctype or self.doctype), field).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
- If \_operator.lower() equals “between”.
  - If (isinstance(\_value, (list bitwise or tuple)) and len(\_value) equals 2).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(\_value, (list bitwise or tuple)) → len(\_value) equals 2.
    - Set \_value from \_apply\_datetime\_field\_filter\_conversion(\_value, (doctype or self.doctype), field).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
  - Otherwise.
    - If isinstance(\_value, str).
      - Bind dependencies get\_between\_date\_filter.
      - Set target\_meta from Platform.get\_meta((doctype or self.doctype)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
      - Set df from target\_meta.get\_field(field).
      - Set \_value from tuple(generator of v.strip().strip(“'”) for v drawn from get\_between\_date\_filter(\_value, df).split(“ AND ”)).
        - Draw v from get\_between\_date\_filter(\_value, df).split(“ AND ”).
- If (not \_value and isinstance(\_value, ((list bitwise or tuple) bitwise or set))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not \_value → isinstance(\_value, ((list bitwise or tuple) bitwise or set)).
  - Set \_value from tuple(empty text).
- If (self.db\_query\_compat and \_value is identical to no value and \_operator.casefold() belongs to tuple(“in”, “not in”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.db\_query\_compat → \_value is identical to no value → \_operator.casefold() belongs to tuple(“in”, “not in”).
  - Set \_value from tuple(empty text).
- If \_operator.casefold() belongs to NESTED\_SET\_OPERATORS.
  - Set hierarchy from \_operator.casefold().
  - Set docname from \_value.
  - Set original\_field\_name from field when isinstance(field, str), otherwise \_field.name.
    - Value choice on isinstance(field, str) — true gives field, false gives \_field.name.
  - Set lookup\_doctype from (doctype or self.doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
  - Set lookup\_meta from Platform.get\_meta(lookup\_doctype).
  - If lookup\_meta.has\_field(original\_field\_name).
    - Set \_df from lookup\_meta.get\_field(original\_field\_name).
    - Set ref\_doctype from \_df.options when \_df, otherwise lookup\_doctype.
      - Value choice on \_df — true gives \_df.options, false gives lookup\_doctype.
  - Otherwise.
    - Set ref\_doctype from lookup\_doctype.
  - Set nodes from get\_nested\_set\_hierarchy\_result(ref\_doctype, docname, hierarchy).
  - Set operator\_fn from OPERATOR\_MAP at “not in” when hierarchy belongs to tuple(“not ancestors of”, “not descendants of”), otherwise OPERATOR\_MAP at “in”.
    - Value choice on hierarchy belongs to tuple(“not ancestors of”, “not descendants of”) — true gives OPERATOR\_MAP at “not in”, false gives OPERATOR\_MAP at “in”.
  - Return operator\_fn(\_field, (nodes or tuple(empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nodes → tuple(empty text).
- If (\_operator.casefold() equals “is” and isinstance(\_field, Field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_operator.casefold() equals “is” → isinstance(\_field, Field).
  - Set filter\_doctype from self.\_get\_field\_doctype(\_field, (doctype or self.doctype)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
  - Return func\_is(\_field, \_value, self.\_get\_is\_set\_empty\_value(filter\_doctype, \_field.name)).
- If (self.is\_postgres and \_operator.casefold() equals “like”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_postgres → \_operator.casefold() equals “like”.
  - Set operator\_fn from OPERATOR\_MAP at “ilike”.
- Otherwise.
  - Set operator\_fn from OPERATOR\_MAP at \_operator.casefold().
- If (\_value is identical to no value and isinstance(\_field, Field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_value is identical to no value → isinstance(\_field, Field).
  - If operator\_fn equals builtin\_operator.ne.
    - Set filter\_field\_name from field when isinstance(field, str), otherwise \_field.name when hasattr(\_field, “name”), otherwise str(\_field).
      - Value choice on isinstance(field, str) — true gives field, false gives \_field.name when hasattr(\_field, “name”), otherwise str(\_field).
      - Value choice on hasattr(\_field, “name”) — true gives \_field.name, false gives str(\_field).
    - If “.” belongs to filter\_field\_name.
      - Set filter\_field\_name from filter\_field\_name.split(“.”) at negative 1.
    - Set target\_doctype from (doctype or self.doctype).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
    - Set fallback\_sql from self.\_get\_ifnull\_fallback(target\_doctype, filter\_field\_name).
    - If fallback\_sql equals “''”.
      - Set fallback\_value from empty text.
    - Otherwise.
      - If (fallback\_sql.startswith(“'”) and fallback\_sql.endswith(“'”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in fallback\_sql.startswith(“'”) → fallback\_sql.endswith(“'”).
        - Set fallback\_value from fallback\_sql at slice 1 to negative 1.
      - Otherwise.
        - Attempt the following.
          - Set fallback\_value from int(fallback\_sql).
        - On failure (tuple(ValueError, TypeError)).
          - Set fallback\_value from fallback\_sql.
    - Return operator\_fn(\_field, ValueWrapper(fallback\_value)).
  - Otherwise.
    - Return \_field.isnull().
- Otherwise.
  - Set filter\_field\_name from field when isinstance(field, str), otherwise \_field.name when hasattr(\_field, “name”), otherwise str(\_field).
    - Value choice on isinstance(field, str) — true gives field, false gives \_field.name when hasattr(\_field, “name”), otherwise str(\_field).
    - Value choice on hasattr(\_field, “name”) — true gives \_field.name, false gives str(\_field).
  - If “.” belongs to filter\_field\_name.
    - Set filter\_field\_name from filter\_field\_name.split(“.”) at negative 1.
  - Set target\_doctype from (doctype or self.doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
  - If isinstance(\_field, (functions.IfNull bitwise or functions.Coalesce)).
    - Return operator\_fn(\_field, \_value).
  - If self.\_should\_apply\_ifnull(target\_doctype, filter\_field\_name, \_operator, \_value).
    - Set fallback\_sql from self.\_get\_ifnull\_fallback(target\_doctype, filter\_field\_name).
    - If fallback\_sql equals “''”.
      - Set fallback\_value from empty text.
    - Otherwise.
      - If (fallback\_sql.startswith(“'”) and fallback\_sql.endswith(“'”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in fallback\_sql.startswith(“'”) → fallback\_sql.endswith(“'”).
        - Set fallback\_value from fallback\_sql at slice 1 to negative 1.
      - Otherwise.
        - Attempt the following.
          - Set fallback\_value from int(fallback\_sql).
        - On failure (tuple(ValueError, TypeError)).
          - Set fallback\_value from fallback\_sql.
    - If fallback\_value equals \_value.
      - If \_operator equals “=”.
        - Return (\_field.isnull() bitwise or \_field.eq(\_value)).
      - Otherwise.
        - If \_operator equals “!=”.
          - Return operator\_fn(\_field, \_value).
    - Set \_field from functions.IfNull(\_field, ValueWrapper(fallback\_value)).
  - Return operator\_fn(\_field, \_value).

**Methods declared on this owner** [validate and prepare filter field](operations-078.md#op-eb4f4b576a4ebf), [get field doctype](operations-079.md#op-365f5e3b2a667e), [get is set empty value](operations-079.md#op-bd329f03932b1e), [get ifnull fallback](operations-079.md#op-c179a6f2640c9d), [should apply ifnull](operations-079.md#op-7a0bbaf75d4027).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L103) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1067) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1207)

<a id="op-f2b300f53c59e7"></a>
### Engine.parse nested filters

`operation_foundation_database_query_business_behavior_engine_parse_nested_filters`

**Inputs** self, nested\_list.

**Declared result** “Criterion \| None”.

**Explicit results** no value · current\_criterion.

**Explicit failure paths** validation helper — translated “Nested filters must be provided as a list or tuple.” · validation helper — translated “Invalid start for filter condition: {0}. Expected a list or tuple.”.format(nested\_list at 0) · validation helper with Platform.ValidationError — translated “Expected 'and' or 'or' operator, found: {0}”.format(operator\_str) · validation helper — translated “Filter condition missing after operator: {0}”.format(operator\_str) · validation helper — translated “Invalid filter condition: {0}. Expected a list or tuple.”.format(next\_condition).

**Local steps**

- If not isinstance(nested\_list, (list bitwise or tuple)).
  - Call the validation error handler Platform.throw(translated “Nested filters must be provided as a list or tuple.”).
- If not nested\_list.
  - Return no value.
- If not isinstance(nested\_list at 0, (list bitwise or tuple)).
  - Call the validation error handler Platform.throw(translated “Invalid start for filter condition: {0}. Expected a list or tuple.”.format(nested\_list at 0)).
- Set current\_criterion from self.\_condition\_to\_criterion(nested\_list at 0).
- Set idx from 1.
- While idx &lt; len(nested\_list).
  - Set operator\_str from nested\_list at idx.
  - If (not isinstance(operator\_str, str) or operator\_str.lower() does not belong to tuple(“and”, “or”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(operator\_str, str) → operator\_str.lower() does not belong to tuple(“and”, “or”).
    - Call the validation error handler Platform.throw(translated “Expected 'and' or 'or' operator, found: {0}”.format(operator\_str), Platform.ValidationError).
  - Update idx using + 1.
  - If idx ≥ len(nested\_list).
    - Call the validation error handler Platform.throw(translated “Filter condition missing after operator: {0}”.format(operator\_str)).
  - Set next\_condition from nested\_list at idx.
  - If not isinstance(next\_condition, (list bitwise or tuple)).
    - Call the validation error handler Platform.throw(translated “Invalid filter condition: {0}. Expected a list or tuple.”.format(next\_condition)).
  - Set next\_criterion from self.\_condition\_to\_criterion(next\_condition).
  - If operator\_str.lower() equals “and”.
    - Set current\_criterion from (current\_criterion bitwise and next\_criterion).
  - Otherwise.
    - If operator\_str.lower() equals “or”.
      - Set current\_criterion from (current\_criterion bitwise or next\_criterion).
  - Update idx using + 1.
- Return current\_criterion.

**Methods declared on this owner** [condition to criterion](operations-078.md#op-ef8b3850ecfd53).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0140.json#L5258) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1093) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1228)

<a id="op-ef8b3850ecfd53"></a>
### Engine.condition to criterion

`operation_foundation_database_query_business_behavior_engine_condition_to_criterion`

**Inputs** self, condition.

**Declared result** “Criterion”.

**Explicit results** self.\_parse\_nested\_filters(condition) · self.\_build\_criterion\_for\_simple\_filter(field, value, operator, doctype).

**Explicit failure paths** validation helper — translated “Invalid condition type in nested filters: {0}”.format(type(condition)) · validation helper — translated “Invalid simple filter format: {0}”.format(condition).

**Local steps**

- If not isinstance(condition, (list bitwise or tuple)).
  - Call the validation error handler Platform.throw(translated “Invalid condition type in nested filters: {0}”.format(type(condition))).
- Set is\_nested from false.
- If (len(condition) ≥ 2 and isinstance(condition at 1, str) and isinstance(condition at 0, (list bitwise or tuple))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(condition) ≥ 2 → isinstance(condition at 1, str) → isinstance(condition at 0, (list bitwise or tuple)).
  - Set is\_nested from true.
- If is\_nested.
  - Return self.\_parse\_nested\_filters(condition).
- Otherwise.
  - Set tuple(field, value, operator, doctype) from tuple(no value, no value, no value, no value).
  - Set additional\_filters\_config from get\_additional\_filters\_from\_hooks().
  - If (len(condition) equals 3 and isinstance(condition at 1, str) and (condition at 1.lower() belongs to OPERATOR\_MAP or condition at 1.lower() belongs to additional\_filters\_config)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(condition) equals 3 → isinstance(condition at 1, str) → (condition at 1.lower() belongs to OPERATOR\_MAP or condition at 1.lower() belongs to additional\_filters\_config).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition at 1.lower() belongs to OPERATOR\_MAP → condition at 1.lower() belongs to additional\_filters\_config.
    - Set tuple(field, operator, value) from condition.
  - Otherwise.
    - If (len(condition) equals 4 and isinstance(condition at 2, str) and (condition at 2.lower() belongs to OPERATOR\_MAP or condition at 2.lower() belongs to additional\_filters\_config)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(condition) equals 4 → isinstance(condition at 2, str) → (condition at 2.lower() belongs to OPERATOR\_MAP or condition at 2.lower() belongs to additional\_filters\_config).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition at 2.lower() belongs to OPERATOR\_MAP → condition at 2.lower() belongs to additional\_filters\_config.
      - Set tuple(doctype, field, operator, value) from condition.
    - Otherwise.
      - If len(condition) equals 2.
        - Set tuple(field, value) from condition.
        - Set operator from “=”.
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Invalid simple filter format: {0}”.format(condition)).
  - Return self.\_build\_criterion\_for\_simple\_filter(field, value, operator, doctype).

**Methods declared on this owner** [parse nested filters](operations-078.md#op-f2b300f53c59e7), [build criterion for simple filter](operations-078.md#op-733ad4f79b58e3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0140.json#L6124) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1075) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1214)

<a id="op-eb4f4b576a4ebf"></a>
### Engine.validate and prepare filter field

`operation_foundation_database_query_business_behavior_engine_validate_and_prepare_filter_field`

**Inputs** self, field, doctype = no value.

**Declared result** Field.

**Explicit results** field · Platform.qb.DocType(table\_name) at field\_name · dynamic\_field.field · Platform.qb.DocType(target\_doctype) at target\_fieldname · child\_field\_handler.field.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Filter fields have invalid backtick notation: {0}”.format(field) · validation helper with Platform.ValidationError — translated “Invalid filter field format: {0}. Use 'fieldname' or 'link\_fieldname.target\_fieldname'.”.format(field) · validation helper with Platform.ValidationError — translated “Invalid characters in fieldname: {0}. Only letters, numbers, and underscores are allowed.”.format(field).

**Local steps**

- If isinstance(field, Term).
  - Return field.
- If “′” belongs to field.
  - If parsed bound to self.\_parse\_backtick\_field\_notation(field).
    - Set tuple(table\_name, field\_name) from parsed.
    - Evaluate self.check\_filter\_field\_permission(table\_name, field\_name).
    - Return Platform.qb.DocType(table\_name) at field\_name.
  - Call the validation error handler Platform.throw(translated “Filter fields have invalid backtick notation: {0}”.format(field), Platform.ValidationError, title = translated “Invalid Filter”).
- If “.” belongs to field.
  - Set dynamic\_field from DynamicTableField.parse(field, self.doctype, allow\_tab\_notation = false).
  - If dynamic\_field.
    - Set target\_doctype from dynamic\_field.doctype.
    - Set target\_fieldname from dynamic\_field.fieldname.
    - Set parent\_doctype\_for\_perm from dynamic\_field.parent\_doctype when isinstance(dynamic\_field, ChildTableField), otherwise no value.
      - Value choice on isinstance(dynamic\_field, ChildTableField) — true gives dynamic\_field.parent\_doctype, false gives no value.
    - Evaluate self.check\_filter\_field\_permission(target\_doctype, target\_fieldname, parent\_doctype\_for\_perm).
    - Set self.query from dynamic\_field.apply\_join(self.query, engine = self).
    - Return dynamic\_field.field.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid filter field format: {0}. Use 'fieldname' or 'link\_fieldname.target\_fieldname'.”.format(field), Platform.ValidationError, title = translated “Invalid Filter”).
- Otherwise.
  - If not SIMPLE\_FIELD\_PATTERN.match(field).
    - Call the validation error handler Platform.throw(translated “Invalid characters in fieldname: {0}. Only letters, numbers, and underscores are allowed.”.format(field), Platform.ValidationError, title = translated “Invalid Filter”).
  - Set target\_doctype from (doctype or self.doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.doctype.
  - Set target\_fieldname from field.
  - Set parent\_doctype\_for\_perm from self.parent\_doctype when doctype, otherwise no value.
    - Value choice on doctype — true gives self.parent\_doctype, false gives no value.
  - If (doctype and doctype differs from self.doctype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → doctype differs from self.doctype.
    - Set parent\_meta from Platform.get\_meta(self.doctype).
    - Set parent\_fieldname from no value.
    - For each df in parent\_meta.get\_table\_fields().
      - If df.options equals doctype.
        - Set parent\_fieldname from df.fieldname.
        - Leave the innermost loop without its normal-exhaustion alternative.
    - If not parent\_fieldname.
      - Evaluate self.check\_filter\_field\_permission(target\_doctype, target\_fieldname, parent\_doctype\_for\_perm).
      - Return Platform.qb.DocType(target\_doctype) at target\_fieldname.
    - Set child\_field\_handler from ChildTableField(doctype = doctype, fieldname = target\_fieldname, parent\_doctype = self.doctype, parent\_fieldname = parent\_fieldname).
    - Set parent\_doctype\_for\_perm from self.doctype.
    - Evaluate self.check\_filter\_field\_permission(target\_doctype, target\_fieldname, parent\_doctype\_for\_perm).
    - Set self.query from child\_field\_handler.apply\_join(self.query, engine = self).
    - Return child\_field\_handler.field.
  - Otherwise.
    - Bind dependencies child\_table\_fields, default\_fields, optional\_fields.
    - If self.doctype belongs to CORE\_DOCTYPES.
      - Set meta from no value.
    - Otherwise.
      - Attempt the following.
        - Set meta from Platform.get\_meta(self.doctype).
      - On failure (Platform.DoesNotExistError).
        - Set meta from no value.
    - If (meta and not doctype and target\_fieldname does not belong to ((default\_fields + optional\_fields) + child\_table\_fields) and not meta.has\_field(target\_fieldname)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta → not doctype → target\_fieldname does not belong to ((default\_fields + optional\_fields) + child\_table\_fields) → not meta.has\_field(target\_fieldname).
      - For each df in meta.get\_table\_fields(include\_computed = true).
        - Attempt the following.
          - Set child\_meta from Platform.get\_meta(df.options).
        - On failure (Platform.DoesNotExistError).
          - Continue with the next iteration or loop test.
        - If child\_meta.has\_field(target\_fieldname).
          - Set child\_field\_handler from ChildTableField(doctype = df.options, fieldname = target\_fieldname, parent\_doctype = self.doctype, parent\_fieldname = df.fieldname).
          - Set parent\_doctype\_for\_perm from self.doctype.
          - Evaluate self.check\_filter\_field\_permission(df.options, target\_fieldname, parent\_doctype\_for\_perm).
          - Set self.query from child\_field\_handler.apply\_join(self.query, engine = self).
          - Return child\_field\_handler.field.
    - Evaluate self.check\_filter\_field\_permission(target\_doctype, target\_fieldname, parent\_doctype\_for\_perm).
    - Return Platform.qb.DocType(target\_doctype) at target\_fieldname.

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse backtick field notation](operations-078.md#op-721a28310f9bb1), [check filter field permission](operations-078.md#op-316384e0a2e961).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1235)

<a id="op-217650ffe2d32f"></a>
### Engine.check select field permission

`operation_foundation_database_query_business_behavior_engine_check_select_field_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, fieldname, parent\_doctype.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L1832) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1073) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1212)

<a id="op-316384e0a2e961"></a>
### Engine.check filter field permission

`operation_foundation_database_query_business_behavior_engine_check_filter_field_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, fieldname, parent\_doctype.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L1954) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1072) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1211)

<a id="op-8558aab3a250f4"></a>
### Engine.check field permission

`operation_foundation_database_query_business_behavior_engine_check_field_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, fieldname, parent\_doctype, for\_filtering.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L2076) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1071) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1210)

<a id="op-a409f219345be2"></a>
### Engine.get cached permitted fields

`operation_foundation_database_query_business_behavior_engine_get_cached_permitted_fields`

**Inputs** self, doctype, parenttype, permission\_type.

**Declared result** set.

**Explicit results** self.permitted\_fields\_cache at cache\_key.

**Local steps**

- Set cache\_key from tuple(doctype, parenttype, permission\_type).
- If cache\_key does not belong to self.permitted\_fields\_cache.
  - Set self.permitted\_fields\_cache at cache\_key from set(get\_permitted\_fields(doctype = doctype, parenttype = parenttype, permission\_type = permission\_type, ignore\_virtual = true, …)).
- Return self.permitted\_fields\_cache at cache\_key.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L2688) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1076) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1215)

<a id="op-d9c832f02f2c75"></a>
### Engine.get filterable fields

`operation_foundation_database_query_business_behavior_engine_get_filterable_fields`

**Inputs** self, doctype, parenttype = no value, permission\_type = no value.

**Declared result** set.

**Explicit results** set() · self.permitted\_fields\_cache at cache\_key · (permitted\_fields bitwise or set(“user\_type”)) · permitted\_fields.

**Local steps**

- If permission\_type is identical to no value.
  - Set permission\_type from self.get\_permission\_type(doctype, parenttype).
- If permission\_type equals “select”.
  - Set meta from Platform.get\_meta(doctype).
  - If meta.istable.
    - Return set().
  - Set cache\_key from tuple(doctype, no value, “\_filterable\_select”).
  - If cache\_key does not belong to self.permitted\_fields\_cache.
    - If (doctype belongs to PERMITTED\_CORE\_DOCTYPES and doctype differs from “User”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype belongs to PERMITTED\_CORE\_DOCTYPES → doctype differs from “User”.
      - Set self.permitted\_fields\_cache at cache\_key from set(meta.get\_valid\_columns()).
    - Otherwise.
      - Set permlevel\_0\_fields from (set(meta.default\_fields) bitwise or OPTIONAL\_FIELDS).
      - For each df in meta.get\_fieldnames\_with\_value(with\_field\_meta = true, with\_virtual\_fields = false).
        - If df.permlevel equals 0.
          - Evaluate permlevel\_0\_fields.add(df.fieldname).
      - If doctype equals “User”.
        - Evaluate permlevel\_0\_fields.add(“user\_type”).
      - Set self.permitted\_fields\_cache at cache\_key from permlevel\_0\_fields.
  - Return self.permitted\_fields\_cache at cache\_key.
- Otherwise.
  - Set permitted\_fields from self.\_get\_cached\_permitted\_fields(doctype, parenttype, permission\_type).
  - If (doctype equals “User” and “user\_type” does not belong to permitted\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “User” → “user\_type” does not belong to permitted\_fields.
    - Return (permitted\_fields bitwise or set(“user\_type”)).
  - Return permitted\_fields.

**Methods declared on this owner** [get permission type](operations-079.md#op-964611b85f8826), [get cached permitted fields](operations-078.md#op-a409f219345be2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L105) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1077) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1216)

<a id="op-a74c9419fd4d7e"></a>
### Engine.parse string field

`operation_foundation_database_query_business_behavior_engine_parse_string_field`

**Inputs** self, field.

**Explicit results** self.table.star · pypika\_field.as\_(alias) · pypika\_field.

**Explicit failure paths** validation helper — translated “Could not parse field: {0}”.format(field).

**Local steps**

- If field equals “\*”.
  - Return self.table.star.
- Set alias from no value.
- Set field\_part from field.
- If “ as ” belongs to field.lower().
  - Set parts from re.split(“\\s+as\\s+”, field, flags = re.IGNORECASE).
  - If len(parts) &gt; 1.
    - Set field\_part from parts at 0.strip().
    - Set alias from parts at 1.strip().strip(“′"'”).
- Set match from FIELD\_PARSE\_REGEX.match(field\_part).
- If not match.
  - Call the validation error handler Platform.throw(translated “Could not parse field: {0}”.format(field)).
- Set groups from match.groups().
- Set table\_name from groups at 1.
- Set field\_name from groups at 3.
- If table\_name.
  - Set doctype\_name from table\_name at slice 3 to no value when table\_name.startswith(“tab”), otherwise table\_name.
    - Value choice on table\_name.startswith(“tab”) — true gives table\_name at slice 3 to no value, false gives table\_name.
  - Set table\_obj from Platform.qb.DocType(doctype\_name).
  - Set pypika\_field from table\_obj at field\_name.
- Otherwise.
  - Set pypika\_field from self.table at field\_name.
- If alias.
  - Return pypika\_field.as\_(alias).
- Otherwise.
  - Return pypika\_field.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L3581) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1095) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1230)

<a id="op-f027552db926ff"></a>
### Engine.parse fields

`operation_foundation_database_query_business_behavior_engine_parse_fields`

**Inputs** self, fields.

**Declared result** “list&#91;Field \| AggregateFunction \| Criterion \| DynamicTableField \| ChildQuery&#93;”.

**Explicit results** list() · list(fields) · \_fields.

**Explicit failure paths** validation helper — translated “Fields must be a string, list, tuple, pypika Field, or pypika Function”.

**Local steps**

- If not fields.
  - Return list().
- If isinstance(fields, Term).
  - Return list(fields).
- Set initial\_field\_list from list().
- If isinstance(fields, str).
  - Evaluate initial\_field\_list.extend(generator of f.strip() for f drawn from COMMA\_PATTERN.split(fields) where f.strip()).
    - Draw f from COMMA\_PATTERN.split(fields), keep a combination only if (f.strip()).
- Otherwise.
  - If isinstance(fields, ((list bitwise or tuple) bitwise or set)).
    - For each item in fields.
      - If item is identical to no value.
        - Continue with the next iteration or loop test.
      - If (isinstance(item, str) and “,” belongs to item).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → “,” belongs to item.
        - Evaluate initial\_field\_list.extend(generator of f.strip() for f drawn from COMMA\_PATTERN.split(item) where f.strip()).
          - Draw f from COMMA\_PATTERN.split(item), keep a combination only if (f.strip()).
      - Otherwise.
        - Evaluate initial\_field\_list.append(item).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Fields must be a string, list, tuple, pypika Field, or pypika Function”).
- Set \_fields from list().
- For each item in initial\_field\_list.
  - If isinstance(item, str).
    - If sanitized\_item bound to \_validate\_select\_field(item.strip()).
      - Set parsed from self.\_parse\_single\_field\_item(sanitized\_item).
      - If isinstance(parsed, list).
        - Evaluate \_fields.extend(parsed).
      - Otherwise.
        - If parsed.
          - Evaluate \_fields.append(parsed).
  - Otherwise.
    - Set parsed from self.\_parse\_single\_field\_item(item).
    - If isinstance(parsed, list).
      - Evaluate \_fields.extend(parsed).
    - Otherwise.
      - If parsed.
        - Evaluate \_fields.append(parsed).
- Return \_fields.

**Methods declared on this owner** [parse single field item](operations-078.md#op-23740b1e391a5d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L4224) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1092) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1227)

<a id="op-23740b1e391a5d"></a>
### Engine.parse single field item

`operation_foundation_database_query_business_behavior_engine_parse_single_field_item`

**Inputs** self, field.

**Declared result** “list \| Criterion \| Field \| DynamicTableField \| ChildQuery \| None”.

**Explicit results** field · function\_parser.parse\_function(field) · function\_parser.parse\_operator(field) · \_parsed\_fields · parsed · 1 additional forms in the steps below.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Unsupported function or operator: {0}”.format(child\_field) · validation helper — translated “Child query fields for '{0}' must be a list or tuple.”.format(child\_field) · validation helper — translated “Invalid field type: {0}”.format(type(field)).

**Local steps**

- If isinstance(field, Term).
  - Return field.
- Otherwise.
  - If isinstance(field, dict).
    - Set function\_parser from SQLFunctionParser(engine = self).
    - If function\_parser.is\_function\_dict(field).
      - Return function\_parser.parse\_function(field).
    - Otherwise.
      - If function\_parser.is\_operator\_dict(field).
        - Return function\_parser.parse\_operator(field).
      - Otherwise.
        - Set \_parsed\_fields from list().
        - For each tuple(child\_field, child\_fields\_list) in field.items().
          - If child\_field.isupper().
            - Call the validation error handler Platform.throw(translated “Unsupported function or operator: {0}”.format(child\_field), Platform.ValidationError).
          - If not isinstance(child\_fields\_list, ((list bitwise or tuple) bitwise or set)).
            - Call the validation error handler Platform.throw(translated “Child query fields for '{0}' must be a list or tuple.”.format(child\_field)).
          - Evaluate \_parsed\_fields.append(ChildQuery(child\_field, list(child\_fields\_list), self.doctype)).
        - Return \_parsed\_fields.
- If not isinstance(field, str).
  - Call the validation error handler Platform.throw(translated “Invalid field type: {0}”.format(type(field))).
- If parsed bound to DynamicTableField.parse(field, self.doctype).
  - Return parsed.
- Otherwise.
  - Return self.parse\_string\_field(field).

**Methods declared on this owner** [parse string field](operations-078.md#op-a74c9419fd4d7e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0141.json#L5159) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1094) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1229)

<a id="op-a1d7c239525380"></a>
### Engine.apply group by

`operation_foundation_database_query_business_behavior_engine_apply_group_by`

**Inputs** self, group\_by = no value.

**Local steps**

- Set parsed\_group\_by\_fields from self.\_validate\_group\_by(group\_by).
- Set self.query from self.query.groupby(expanded parsed\_group\_by\_fields).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate group by](operations-078.md#op-f619199bfaf4a7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L101) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1062) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1202)

<a id="op-b95ce370f25456"></a>
### Engine.apply order by

`operation_foundation_database_query_business_behavior_engine_apply_order_by`

**Inputs** self, order\_by.

**Explicit results** no value.

**Local steps**

- If (not order\_by or order\_by equals DefaultOrderBy).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not order\_by → order\_by equals DefaultOrderBy.
  - Evaluate self.\_apply\_default\_order\_by().
  - Return no value.
- Set parsed\_order\_fields from self.\_validate\_order\_by(order\_by).
- For each tuple(order\_field, order\_direction) in parsed\_order\_fields.
  - Set self.query from self.query.orderby(order\_field, order = order\_direction).

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply default order by](operations-078.md#op-7d1450378b2d02), [validate order by](operations-078.md#op-38a6c5502e3af2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L102) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1066) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1206)

<a id="op-7d1450378b2d02"></a>
### Engine.apply default order by

`operation_foundation_database_query_business_behavior_engine_apply_default_order_by`

**Inputs** self.

**Local steps**

- Bind dependencies Order.
- Set tuple(sort\_field, sort\_order) from get\_doctype\_sort\_info(self.doctype).
- If “,” belongs to sort\_field.
  - For each sort\_spec in sort\_field.split(“,”).
    - If parts bound to sort\_spec.strip().split(maxsplit = 1).
      - Set field\_name from parts at 0.
      - Set spec\_order from parts at 1.lower() when len(parts) &gt; 1, otherwise sort\_order.lower().
        - Value choice on len(parts) &gt; 1 — true gives parts at 1.lower(), false gives sort\_order.lower().
      - Set field from self.table at field\_name.
      - If self.db\_query\_compat.
        - Set order\_direction from Order.desc when spec\_order equals “desc”, otherwise Order.asc.
          - Value choice on spec\_order equals “desc” — true gives Order.desc, false gives Order.asc.
      - Otherwise.
        - Set order\_direction from Order.asc when spec\_order equals “asc”, otherwise Order.desc.
          - Value choice on spec\_order equals “asc” — true gives Order.asc, false gives Order.desc.
      - Set self.query from self.query.orderby(field, order = order\_direction).
- Otherwise.
  - Set field from self.table at sort\_field.
  - If self.db\_query\_compat.
    - Set order\_direction from Order.desc when sort\_order.lower() equals “desc”, otherwise Order.asc.
      - Value choice on sort\_order.lower() equals “desc” — true gives Order.desc, false gives Order.asc.
  - Otherwise.
    - Set order\_direction from Order.asc when sort\_order.lower() equals “asc”, otherwise Order.desc.
      - Value choice on sort\_order.lower() equals “asc” — true gives Order.asc, false gives Order.desc.
  - Set self.query from self.query.orderby(field, order = order\_direction).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L99) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1057) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1197)

<a id="op-721a28310f9bb1"></a>
### Engine.parse backtick field notation

`operation_foundation_database_query_business_behavior_engine_parse_backtick_field_notation`

**Inputs** self, field\_name.

**Declared result** (tuple at tuple(str, str) bitwise or no value).

**Explicit results** no value · tuple(match.group(1), match.group(3)).

**Local steps**

- Set match from BACKTICK\_FIELD\_PARSE\_REGEX.match(field\_name.strip()).
- If not match.
  - Return no value.
- Return tuple(match.group(1), match.group(3)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L1961) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1091) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1226)

<a id="op-11789d89235aec"></a>
### Engine.validate and parse field for clause

`operation_foundation_database_query_business_behavior_engine_validate_and_parse_field_for_clause`

**Inputs** self, field\_name, clause\_name.

**Declared result** Field.

**Explicit results** field\_name · Field(field\_name) · Platform.qb.DocType(table\_name) at field\_name · dynamic\_field.field · self.table at field\_name.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “{0} has invalid backtick notation: {1}”.format(clause\_name, field\_name) · validation helper with Platform.ValidationError — translated “Invalid field format in {0}: {1}. Use 'field', 'link\_field.field', or 'child\_table.field'.”.format(clause\_name, field\_name).

**Local steps**

- If field\_name.isdigit().
  - Return field\_name.
- If (field\_name belongs to self.function\_aliases or field\_name belongs to self.field\_aliases).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field\_name belongs to self.function\_aliases → field\_name belongs to self.field\_aliases.
  - Return Field(field\_name).
- If “′” belongs to field\_name.
  - If parsed bound to self.\_parse\_backtick\_field\_notation(field\_name).
    - Set tuple(table\_name, field\_name) from parsed.
    - Evaluate self.check\_filter\_field\_permission(table\_name, field\_name).
    - Return Platform.qb.DocType(table\_name) at field\_name.
  - Call the validation error handler Platform.throw(translated “{0} has invalid backtick notation: {1}”.format(clause\_name, field\_name), Platform.ValidationError).
- Set dynamic\_field from DynamicTableField.parse(field\_name, self.doctype, allow\_tab\_notation = false).
- If dynamic\_field.
  - If isinstance(dynamic\_field, ChildTableField).
    - Evaluate self.check\_filter\_field\_permission(dynamic\_field.doctype, dynamic\_field.fieldname, dynamic\_field.parent\_doctype).
  - Otherwise.
    - If isinstance(dynamic\_field, LinkTableField).
      - Evaluate self.check\_filter\_field\_permission(self.doctype, dynamic\_field.link\_fieldname).
      - Evaluate self.check\_filter\_field\_permission(dynamic\_field.doctype, dynamic\_field.fieldname).
  - Set self.query from dynamic\_field.apply\_join(self.query, engine = self).
  - Return dynamic\_field.field.
- Otherwise.
  - If not SIMPLE\_FIELD\_PATTERN.match(field\_name).
    - Call the validation error handler Platform.throw(translated “Invalid field format in {0}: {1}. Use 'field', 'link\_field.field', or 'child\_table.field'.”.format(clause\_name, field\_name), Platform.ValidationError).
  - Evaluate self.check\_filter\_field\_permission(self.doctype, field\_name).
  - Return self.table at field\_name.

**Methods declared on this owner** [parse backtick field notation](operations-078.md#op-721a28310f9bb1), [check filter field permission](operations-078.md#op-316384e0a2e961).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L109) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1099) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1234)

<a id="op-f619199bfaf4a7"></a>
### Engine.validate group by

`operation_foundation_database_query_business_behavior_engine_validate_group_by`

**Inputs** self, group\_by.

**Declared result** list at Field.

**Explicit results** parsed\_fields.

**Explicit failure paths** validation helper with TypeError — translated “Group By must be a string”.

**Local steps**

- If not isinstance(group\_by, str).
  - Call the validation error handler Platform.throw(translated “Group By must be a string”, TypeError).
- Set parsed\_fields from list().
- For each part in group\_by.split(“,”).
  - Set field\_name from part.strip().
  - If not field\_name.
    - Continue with the next iteration or loop test.
  - Set parsed\_field from self.\_validate\_and\_parse\_field\_for\_clause(field\_name, “Group By”).
  - Evaluate parsed\_fields.append(parsed\_field).
- Return parsed\_fields.

**Methods declared on this owner** [validate and parse field for clause](operations-078.md#op-11789d89235aec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L2955) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1236)

<a id="op-38a6c5502e3af2"></a>
### Engine.validate order by

`operation_foundation_database_query_business_behavior_engine_validate_order_by`

**Inputs** self, order\_by.

**Declared result** list at tuple at tuple((Field bitwise or str), Order).

**Explicit results** parsed\_order\_fields.

**Explicit failure paths** validation helper with TypeError — translated “Order By must be a string” · validation helper with ValueError — translated “Invalid direction in Order By: {0}. Must be 'ASC' or 'DESC'.”.format(direction).

**Local steps**

- If not isinstance(order\_by, str).
  - Call the validation error handler Platform.throw(translated “Order By must be a string”, TypeError).
- Set valid\_directions from set(“asc”, “desc”).
- Set parsed\_order\_fields from list().
- For each declaration in order\_by.split(“,”).
  - If \_order\_by bound to declaration.strip().
    - Set parts from \_order\_by.split().
    - Set direction from no value.
    - Set field\_name from \_order\_by.
    - If (len(parts) &gt; 1 and parts at negative 1.lower() belongs to valid\_directions).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(parts) &gt; 1 → parts at negative 1.lower() belongs to valid\_directions.
      - Set direction from parts at negative 1.lower().
      - Set field\_name from one space.join(parts at slice no value to negative 1).
    - If self.db\_query\_compat.
      - Set order\_direction from Order.desc when direction equals “desc”, otherwise Order.asc.
        - Value choice on direction equals “desc” — true gives Order.desc, false gives Order.asc.
    - Otherwise.
      - Set order\_direction from Order.asc when direction equals “asc”, otherwise Order.desc.
        - Value choice on direction equals “asc” — true gives Order.asc, false gives Order.desc.
    - Set parsed\_field from self.\_validate\_and\_parse\_field\_for\_clause(field\_name, “Order By”).
    - Evaluate parsed\_order\_fields.append(tuple(parsed\_field, order\_direction)).
    - If (direction and direction does not belong to valid\_directions).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in direction → direction does not belong to valid\_directions.
      - Call the validation error handler Platform.throw(translated “Invalid direction in Order By: {0}. Must be 'ASC' or 'DESC'.”.format(direction), ValueError).
- Return parsed\_order\_fields.

**Methods declared on this owner** [validate and parse field for clause](operations-078.md#op-11789d89235aec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L110) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1237)

<a id="op-4810aa43ab55db"></a>
### Engine.check select permission

`operation_foundation_database_query_business_behavior_engine_check_select_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L3998) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1074) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1213)

<a id="op-a5aaf699301139"></a>
### Engine.raise permission error

`operation_foundation_database_query_business_behavior_engine_raise_permission_error`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L4123) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1096) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1231)

<a id="op-32ad8445abad8d"></a>
### Engine.apply field permissions

`operation_foundation_database_query_business_behavior_engine_apply_field_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 17 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L4295) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1058) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1198)

<a id="op-f8caa7d7616369"></a>
### Engine.get user permission conditions

`operation_foundation_database_query_business_behavior_engine_get_user_permission_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, table.

**Explicit result forms** a value selected from the current context.

**Local structure** 10 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0142.json#L5611) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1086) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1224)
