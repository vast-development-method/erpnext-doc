# Record lifecycle and persistence · operations 57

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Filter

<a id="op-81d92b3f6646f1"></a>
### Filters.optimize.group key

`operation_foundation_types_filter_business_behavior_filters_optimize_group_key`

**Inputs** f.

**Declared result** tuple at tuple(str, str, bool).

**Explicit results** tuple(f.doctype, f.fieldname, f.operator equals “=”).

**Local steps**

- Return tuple(f.doctype, f.fieldname, f.operator equals “=”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L3561) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1437)

<a id="op-6deacc04f9b3bb"></a>
### Filters.optimize.values

`operation_foundation_types_filter_business_behavior_filters_optimize_values`

**Inputs** no declared parameters.

**Declared result** Generator at \_Value.

**Local steps**

- For each f in filters.
  - yield cast(\_Value, f.value).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L724) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1438)

<a id="op-d7d119391f52cc"></a>
### Filters.str

`operation_foundation_types_filter_business_behavior_filters_text`

**Inputs** self.

**Wrappers, in declaration order** override.

**Declared result** str.

**Explicit results** “Filters()” · formatted text Filters( {filters\_str} ).

**Local steps**

- If not self.
  - Return “Filters()”.
- Set filters\_str from whitespace '\\n'.join(generator of formatted text   {filter} for filter drawn from self).
  - Draw filter from self.
- Return formatted text Filters( {filters\_str} ).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L3662) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1439)

## Service · Functions

<a id="op-697f33bccdaea2"></a>
### Concat ws.initialize

`operation_foundation_query_builder_functions_business_behavior_concat_ws_initialize`

**Inputs** self, remaining positional values terms, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“CONCAT\_WS”, expanded terms, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L5765) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L156)

<a id="op-a6b69390d49766"></a>
### Locate.initialize

`operation_foundation_query_builder_functions_business_behavior_locate_initialize`

**Inputs** self, needle, haystack, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“LOCATE”, needle, haystack, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L5852) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L158)

<a id="op-6d3d7f1b3b189f"></a>
### Strpos.initialize

`operation_foundation_query_builder_functions_business_behavior_strpos_initialize`

**Inputs** self, needle, haystack, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“STRPOS”, haystack, needle, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L5949) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L167)

<a id="op-2885288001032d"></a>
### Instr.initialize

`operation_foundation_query_builder_functions_business_behavior_instr_initialize`

**Inputs** self, needle, haystack, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“INSTR”, haystack, needle, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L6046) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L157)

<a id="op-9835fbbea9d64d"></a>
### Timestamp.initialize

`operation_foundation_query_builder_functions_business_behavior_timestamp_initialize`

**Inputs** self, term, time = no value, alias = no value.

**Local steps**

- If time.
  - Evaluate super().\_\_init\_\_(“TIMESTAMP”, term, time, alias = alias).
- Otherwise.
  - Evaluate super().\_\_init\_\_(“TIMESTAMP”, term, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L6143) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L169)

<a id="op-7f19fc39c175a5"></a>
### Round.initialize

`operation_foundation_query_builder_functions_business_behavior_round_initialize`

**Inputs** self, term, decimal = 0, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“ROUND”, term, decimal, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L6307) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L166)

<a id="op-6fe68d79396367"></a>
### Truncate.initialize

`operation_foundation_query_builder_functions_business_behavior_truncate_initialize`

**Inputs** self, term, decimal, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“TRUNCATE”, term, decimal, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L6408) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L170)

<a id="op-93015836bc280f"></a>
### Postgres Timestamp.initialize

`operation_foundation_query_builder_functions_business_behavior_relational_database_timestamp_initialize`

**Inputs** self, datepart, timepart, alias = no value.

**Local steps**

- If (isinstance(timepart, time) or isinstance(datepart, time)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(timepart, time) → isinstance(datepart, time).
  - Set tuple(timepart, datepart) from tuple(str(timepart), str(datepart)).
- If isinstance(datepart, str).
  - Set datepart from Cast(datepart, “date”).
- If isinstance(timepart, str).
  - Set timepart from Cast(timepart, “time”).
- Evaluate super().\_\_init\_\_(operator = Arithmetic.add, left = datepart, right = timepart, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L6795) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L164)

<a id="op-c30bffeb9a5d79"></a>
### Year Week.initialize

`operation_foundation_query_builder_functions_business_behavior_year_week_initialize`

**Inputs** self, term.

**Local steps**

- Evaluate super().\_\_init\_\_(“YEARWEEK”, term, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L7138) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L171)

<a id="op-a0bd1eee096913"></a>
### Postgres Unix Timestamp.initialize

`operation_foundation_query_builder_functions_business_behavior_relational_database_unix_timestamp_initialize`

**Inputs** self, field, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“epoch”, field = field, alias = alias).
- Set self.field from field.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L7214) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L165)

<a id="op-dcd9044c1575ac"></a>
### Maria DBJSONExtract.initialize

`operation_foundation_query_builder_functions_business_behavior_maria_database_structured_data_extract_initialize`

**Inputs** self, field, path, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“JSON\_EXTRACT”, field, path, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L7746) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L160)

<a id="op-7ff8b0b2699f2f"></a>
### Maria DBJSONValue.initialize

`operation_foundation_query_builder_functions_business_behavior_maria_database_structured_data_value_initialize`

**Inputs** self, field, path, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“JSON\_UNQUOTE”, \_MariaDBJSONExtract(field, path), expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L7843) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L161)

<a id="op-7beee0df3ed52f"></a>
### Maria DBJSONContains.initialize

`operation_foundation_query_builder_functions_business_behavior_maria_database_structured_data_contains_initialize`

**Inputs** self, target, candidate, remaining named values kwargs.

**Local steps**

- Bind dependencies JSON.
- If not isinstance(candidate, Term).
  - Set candidate from JSON(candidate).
- Evaluate super().\_\_init\_\_(“JSON\_CONTAINS”, target, candidate, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L159)

<a id="op-42dab29814c35c"></a>
### Cast.initialize

`operation_foundation_query_builder_functions_business_behavior_cast_initialize`

**Inputs** self, value, as\_type, alias = no value.

**Local steps**

- If (Platform.db.db\_type equals “mariadb” and ((hasattr(as\_type, “get\_sql”) and nested operand in the contract().lower() equals “varchar”) or str(as\_type).lower() equals “varchar”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.db\_type equals “mariadb” → ((hasattr(as\_type, “get\_sql”) and nested operand in the contract.get\_sql().lower() equals “varchar”) or str(as\_type).lower() equals “varchar”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (hasattr(as\_type, “get\_sql”) and as\_type.get\_sql().lower() equals “varchar”) → str(as\_type).lower() equals “varchar”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(as\_type, “get\_sql”) → as\_type.get\_sql().lower() equals “varchar”.
  - Evaluate super().\_\_init\_\_(“CONCAT”, value, empty text, alias = alias).
- Otherwise.
  - Evaluate super().\_\_init\_\_(“CAST”, value, alias = alias).
  - Set self.as\_type from as\_type.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L168) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L155)

<a id="op-3c8290b0ba07c2"></a>
### Cast.get special params sql

`operation_foundation_query_builder_functions_business_behavior_cast_get_special_parameters_database_query`

**Inputs** self, remaining named values kwargs.

**Explicit results** formatted text AS {type\_sql}.

**Local steps**

- If self.name.lower() equals “cast”.
  - Set type\_sql from self.as\_type.get\_sql(expanded names kwargs) when hasattr(self.as\_type, “get\_sql”), otherwise str(self.as\_type).upper().
    - Value choice on hasattr(self.as\_type, “get\_sql”) — true gives self.as\_type.get\_sql(expanded names kwargs), false gives str(self.as\_type).upper().
  - Return formatted text AS {type\_sql}.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L475) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L154)

<a id="op-86ce619fe6329e"></a>
### Aggregate

`operation_foundation_query_builder_functions_business_behavior_aggregate`

**Inputs** function, dt, fieldname, filters, remaining named values kwargs.

**Explicit results** (nested operand in the contract.get\_query(dt, filters = filters, fields = list(nested operand in the contract)).run(expanded names kwargs) at 0 at 0 or 0).

**Local steps**

- Return (nested operand in the contract.get\_query(dt, filters = filters, fields = list(nested operand in the contract)).run(expanded names kwargs) at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract.qb.get\_query(dt, filters = filters, fields = list(nested operand in the contract(nested operand in the contract))).run(expanded names kwargs) at 0 at 0 → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L668) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L152)

<a id="op-1b5de0799bf731"></a>
### Max

`operation_foundation_query_builder_functions_business_behavior_maximum`

**Inputs** dt, fieldname, filters = no value, remaining named values kwargs.

**Explicit results** \_aggregate(Max, dt, fieldname, filters, expanded names kwargs).

**Local steps**

- Return \_aggregate(Max, dt, fieldname, filters, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L844) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L162)

<a id="op-c0b3cec324962d"></a>
### Min

`operation_foundation_query_builder_functions_business_behavior_minimum`

**Inputs** dt, fieldname, filters = no value, remaining named values kwargs.

**Explicit results** \_aggregate(Min, dt, fieldname, filters, expanded names kwargs).

**Local steps**

- Return \_aggregate(Min, dt, fieldname, filters, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L939) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L163)

<a id="op-70f1c68bf703f7"></a>
### Avg

`operation_foundation_query_builder_functions_business_behavior_average`

**Inputs** dt, fieldname, filters = no value, remaining named values kwargs.

**Explicit results** \_aggregate(Avg, dt, fieldname, filters, expanded names kwargs).

**Local steps**

- Return \_aggregate(Avg, dt, fieldname, filters, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L1034) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L153)

<a id="op-31f8d8e8992a09"></a>
### Sum

`operation_foundation_query_builder_functions_business_behavior_sum`

**Inputs** dt, fieldname, filters = no value, remaining named values kwargs.

**Explicit results** \_aggregate(Sum, dt, fieldname, filters, expanded names kwargs).

**Local steps**

- Return \_aggregate(Sum, dt, fieldname, filters, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L1129) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L168)

## Record · Has role

[Record definition](../../../../data/record-types/has_role.json)

<a id="op-b002b3ea0637e2"></a>
### Has Role.before insert

`operation_foundation_core_record_definitions_has_role_business_behavior_has_role_before_insert`

**Inputs** self.

**Record and data access** read “Has Role” via exists.

**Explicit failure paths** validation helper — Platform.\_(“User '{0}' already has the role '{1}'”).format(self.parent, self.role).

**Local steps**

- If Platform.db.exists(“Has Role”, mapping(“parent” → self.parent, “role” → self.role)).
  - Call the validation error handler Platform.throw(Platform.\_(“User '{0}' already has the role '{1}'”).format(self.parent, self.role)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L3037) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1624)
