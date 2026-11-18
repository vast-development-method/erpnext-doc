# Record lifecycle and persistence · operations 80

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Query

<a id="op-ba14742246e6cd"></a>
### Link Table Field.apply select

`operation_foundation_database_query_business_behavior_link_table_field_apply_select`

**Inputs** self, query, engine = no value.

**Declared result** QueryBuilder.

**Explicit results** query.select(self.field.as\_((self.alias or no value))).

**Local steps**

- Set query from self.apply\_join(query, engine = engine).
- Return query.select(self.field.as\_((self.alias or no value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.alias → no value.

**Methods declared on this owner** [apply join](operations-080.md#op-e331ba5c0d19e9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L112) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1241)

<a id="op-e331ba5c0d19e9"></a>
### Link Table Field.apply join

`operation_foundation_database_query_business_behavior_link_table_field_apply_join`

**Inputs** self, query, engine = no value.

**Declared result** QueryBuilder.

**Explicit results** query.

**Local steps**

- If engine is distinct from no value.
  - Set alias from engine.get\_link\_table\_alias(self.doctype, self.link\_fieldname).
  - Set self.table from Platform.qb.DocType(self.doctype).as\_(alias).
  - Set self.field from self.table at self.fieldname.
- Set main\_table from Platform.qb.DocType(self.parent\_doctype).
- If not query.is\_joined(self.table).
  - Set clause from self.table.name equals getattr(main\_table, self.link\_fieldname).
  - If (engine and engine.apply\_permissions).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in engine → engine.apply\_permissions.
    - If condition bound to engine.get\_permission\_conditions(self.doctype, self.table).
      - Update clause using bitwise and condition.
  - Set query from query.left\_join(self.table).on(clause).
- Return query.

**Values supplied outside this operation** selected callable from getattr(main\_table, self.link\_fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L111) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1240)

<a id="op-2a2b43831fb377"></a>
### Child Query.initialize

`operation_foundation_database_query_business_behavior_child_query_initialize`

**Inputs** self, fieldname, fields, parent\_doctype.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set field from Platform.get\_meta(parent\_doctype).get\_field(fieldname).
- If field.fieldtype does not belong to Platform.model.table\_fields.
  - Return no value.
- Set self.fieldname from fieldname.
- Set self.fields from fields.
- Set self.parent\_doctype from parent\_doctype.
- Set self.doctype from field.options.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L651) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1034) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1174)

<a id="op-16755ce2b6b18a"></a>
### Child Query.get query

`operation_foundation_database_query_business_behavior_child_query_get_query`

**Inputs** self, parent\_names = no value.

**Declared result** QueryBuilder.

**Explicit results** Platform.qb.get\_query(self.doctype, fields = list(expanded self.fields, “parent”, “parentfield”), filters = filters, order\_by = “idx asc”).

**Local steps**

- Set filters from mapping(“parenttype” → self.parent\_doctype, “parentfield” → self.fieldname, “parent” → list(“in”, parent\_names)).
- Return Platform.qb.get\_query(self.doctype, fields = list(expanded self.fields, “parent”, “parentfield”), filters = filters, order\_by = “idx asc”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L95) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1033) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1173)

<a id="op-c9a8a84082c585"></a>
### Get nested set hierarchy result

`operation_foundation_database_query_business_behavior_get_nested_set_hierarchy_result`

**Inputs** doctype, name, hierarchy.

**Declared result** list at str.

**Explicit results** result.

**Local steps**

- Set table from Platform.qb.DocType(doctype).
- Attempt the following.
  - Set tuple(lft, rgt) from nested operand in the contract.select(“lft”, “rgt”).where(table.name equals name).run() at 0.
- On failure (IndexError).
  - Set tuple(lft, rgt) from tuple(no value, no value).
- If hierarchy belongs to tuple(“descendants of”, “not descendants of”, “descendants of (inclusive)”).
  - Set result from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.rgt &lt; rgt).orderby(table.lft, order = Order.asc).run(pluck = true).
  - If hierarchy equals “descendants of (inclusive)”.
    - Update result using + list(name).
- Otherwise.
  - Set result from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.rgt &gt; rgt).orderby(table.lft, order = Order.desc).run(pluck = true).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L1126) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1238)

<a id="op-c40337a416e8e3"></a>
### Is function call

`operation_foundation_database_query_business_behavior_is_function_call`

**Inputs** field\_str.

**Declared result** bool.

**Explicit results** bool(FUNCTION\_CALL\_PATTERN.match(field\_str)).

**Local steps**

- Return bool(FUNCTION\_CALL\_PATTERN.match(field\_str)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L1835) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1239)

<a id="op-182dce1bee0d1c"></a>
### Validate select field

`operation_foundation_database_query_business_behavior_validate_select_field`

**Inputs** field.

**Wrappers, in declaration order** lru\_cache(maxsize = 1024).

**Explicit results** field.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “SQL functions are not allowed as strings in SELECT: {0}. Use dict syntax like {{'COUNT': '\*'}} instead.”.format(field) · validation helper with Platform.PermissionError — translated “Invalid field format for SELECT: {0}. Field names must be simple, backticked, table-qualified, aliased, or '\*'.”.format(field).

**Local steps**

- If field equals “\*”.
  - Return field.
- If field.isdigit().
  - Return field.
- If \_is\_function\_call(field).
  - Call the validation error handler Platform.throw(translated “SQL functions are not allowed as strings in SELECT: {0}. Use dict syntax like {{'COUNT': '\*'}} instead.”.format(field), Platform.ValidationError).
- If ALLOWED\_FIELD\_PATTERN.match(field).
  - Return field.
- Call the validation error handler Platform.throw(translated “Invalid field format for SELECT: {0}. Field names must be simple, backticked, table-qualified, aliased, or '\*'.”.format(field), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L1908) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1248)

<a id="op-7a664e31f7bc4a"></a>
### Raw Criterion.initialize

`operation_foundation_database_query_business_behavior_raw_criterion_initialize`

**Inputs** self, sql\_string.

**Local steps**

- Set self.sql\_string from sql\_string.
- Evaluate super().\_\_init\_\_().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2204) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1245)

<a id="op-200c42f9073c85"></a>
### Raw Criterion.get sql

`operation_foundation_database_query_business_behavior_raw_criterion_get_database_query`

**Inputs** self, remaining named values kwargs.

**Declared result** str.

**Explicit results** self.sql\_string.

**Local steps**

- Return self.sql\_string.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2289) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1244)

<a id="op-ae09b9b6ecc789"></a>
### Raw Criterion.and

`operation_foundation_database_query_business_behavior_raw_criterion_and`

**Inputs** self, other.

**Explicit results** CombinedRawCriterion(self, other, “AND”).

**Local steps**

- Return CombinedRawCriterion(self, other, “AND”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2337) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1243)

<a id="op-cc2b581c18345e"></a>
### Raw Criterion.or

`operation_foundation_database_query_business_behavior_raw_criterion_or`

**Inputs** self, other.

**Explicit results** CombinedRawCriterion(self, other, “OR”).

**Local steps**

- Return CombinedRawCriterion(self, other, “OR”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2402) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1247)

<a id="op-a1e2b4f7751d74"></a>
### Raw Criterion.invert

`operation_foundation_database_query_business_behavior_raw_criterion_invert`

**Inputs** self.

**Explicit results** RawCriterion(formatted text NOT ({self.sql\_string})).

**Local steps**

- Return RawCriterion(formatted text NOT ({self.sql\_string})).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2467) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1246)

<a id="op-354bb5c0a82b2d"></a>
### Combined Raw Criterion.initialize

`operation_foundation_database_query_business_behavior_combined_raw_criterion_initialize`

**Inputs** self, left, right, operator.

**Local steps**

- Set self.left from left.
- Set self.right from right.
- Set self.operator from operator.
- Evaluate super(RawCriterion, self).\_\_init\_\_().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2541) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1039) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1179)

<a id="op-ef7438b25632a1"></a>
### Combined Raw Criterion.get sql

`operation_foundation_database_query_business_behavior_combined_raw_criterion_get_database_query`

**Inputs** self, remaining named values kwargs.

**Declared result** str.

**Explicit results** formatted text (({left\_sql}) {self.operator} ({right\_sql})).

**Local steps**

- Set left\_sql from self.left.get\_sql(expanded names kwargs) when hasattr(self.left, “get\_sql”), otherwise str(self.left).
  - Value choice on hasattr(self.left, “get\_sql”) — true gives self.left.get\_sql(expanded names kwargs), false gives str(self.left).
- Set right\_sql from self.right.get\_sql(expanded names kwargs) when hasattr(self.right, “get\_sql”), otherwise str(self.right).
  - Value choice on hasattr(self.right, “get\_sql”) — true gives self.right.get\_sql(expanded names kwargs), false gives str(self.right).
- Return formatted text (({left\_sql}) {self.operator} ({right\_sql})).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2678) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1038) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1178)

<a id="op-a42f231db7fca6"></a>
### SQLFunction Parser.initialize

`operation_foundation_database_query_business_behavior_database_query_function_parser_initialize`

**Inputs** self, engine.

**Local steps**

- Set self.engine from engine.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2943) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1182)

<a id="op-71fa4498ac1d2b"></a>
### SQLFunction Parser.is function dict

`operation_foundation_database_query_business_behavior_database_query_function_parser_is_function_mapping`

**Inputs** self, field\_dict.

**Declared result** bool.

**Explicit results** (len(function\_keys) equals 1 and function\_keys at 0 belongs to FUNCTION\_MAPPING).

**Local steps**

- Set function\_keys from list of k for k drawn from field\_dict.keys() where k.lower() differs from “as”.
  - Draw k from field\_dict.keys(), keep a combination only if (k.lower() differs from “as”).
- Return (len(function\_keys) equals 1 and function\_keys at 0 belongs to FUNCTION\_MAPPING).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(function\_keys) equals 1 → function\_keys at 0 belongs to FUNCTION\_MAPPING.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L2997) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1183)

<a id="op-fede54d8df08b0"></a>
### SQLFunction Parser.is operator dict

`operation_foundation_database_query_business_behavior_database_query_function_parser_is_operator_mapping`

**Inputs** self, field\_dict.

**Declared result** bool.

**Explicit results** (len(operator\_keys) equals 1 and operator\_keys at 0 belongs to OPERATOR\_MAPPING).

**Local steps**

- Set operator\_keys from list of k for k drawn from field\_dict.keys() where k.lower() differs from “as”.
  - Draw k from field\_dict.keys(), keep a combination only if (k.lower() differs from “as”).
- Return (len(operator\_keys) equals 1 and operator\_keys at 0 belongs to OPERATOR\_MAPPING).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(operator\_keys) equals 1 → operator\_keys at 0 belongs to OPERATOR\_MAPPING.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L3172) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1184)

<a id="op-8351075f2ad417"></a>
### SQLFunction Parser.extract dict components

`operation_foundation_database_query_business_behavior_database_query_function_parser_extract_mapping_components`

**Inputs** self, d, valid\_keys, error\_msg.

**Declared result** tuple.

**Explicit results** tuple(name, alias, args).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid {0} dictionary format”.format(error\_msg) · validation helper with Platform.ValidationError — translated “Unsupported {0}: {1}”.format(error\_msg, name).

**Local steps**

- Set name from no value.
- Set alias from no value.
- Set args from no value.
- For each tuple(key, value) in d.items().
  - If key.lower() equals “as”.
    - Set alias from value.
  - Otherwise.
    - Set name from key.
    - Set args from value.
- If not name.
  - Call the validation error handler Platform.throw(translated “Invalid {0} dictionary format”.format(error\_msg), Platform.ValidationError).
- If name does not belong to valid\_keys.
  - Call the validation error handler Platform.throw(translated “Unsupported {0}: {1}”.format(error\_msg, name), Platform.ValidationError).
- If alias.
  - Evaluate self.\_validate\_alias(alias).
- Return tuple(name, alias, args).

**Methods declared on this owner** [validate alias](operations-080.md#op-cc7d1f1922721e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L3347) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1181)

<a id="op-b3d840a06feb5d"></a>
### SQLFunction Parser.parse function

`operation_foundation_database_query_business_behavior_database_query_function_parser_parse_function`

**Inputs** self, function\_dict.

**Declared result** Field.

**Explicit results** function\_call.as\_(alias) · function\_call.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Function {0} requires arguments but none were provided”.format(function\_name) · validation helper with Platform.ValidationError — translated “Invalid function argument type: {0}. Only strings, numbers, lists, and None are allowed.”.format(type(function\_args).\_\_name\_\_).

**Local steps**

- Set tuple(function\_name, alias, function\_args) from self.\_extract\_dict\_components(function\_dict, FUNCTION\_MAPPING, “function or invalid field name”).
- Set func\_class from FUNCTION\_MAPPING at function\_name.
- If isinstance(function\_args, str).
  - Set parsed\_arg from self.\_parse\_and\_validate\_argument(function\_args, function\_name = function\_name).
  - Set function\_call from func\_class(parsed\_arg).
- Otherwise.
  - If isinstance(function\_args, list).
    - Set parsed\_args from list().
    - For each arg in function\_args.
      - Set parsed\_arg from self.\_parse\_and\_validate\_argument(arg, function\_name = function\_name).
      - Evaluate parsed\_args.append(parsed\_arg).
    - Set function\_call from func\_class(expanded parsed\_args).
  - Otherwise.
    - If isinstance(function\_args, (int bitwise or float)).
      - Set function\_call from func\_class(function\_args).
    - Otherwise.
      - If function\_args is identical to no value.
        - Attempt the following.
          - Set function\_call from func\_class().
        - On failure (TypeError).
          - Call the validation error handler Platform.throw(translated “Function {0} requires arguments but none were provided”.format(function\_name), Platform.ValidationError).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Invalid function argument type: {0}. Only strings, numbers, lists, and None are allowed.”.format(type(function\_args).\_\_name\_\_), Platform.ValidationError).
- If alias.
  - Evaluate self.engine.function\_aliases.add(alias).
  - Return function\_call.as\_(alias).
- Otherwise.
  - Return function\_call.

**Methods declared on this owner** [extract dict components](operations-080.md#op-8351075f2ad417), [parse and validate argument](operations-080.md#op-fe50bd87c63761).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L3779) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1187)

<a id="op-94f658be07e4ec"></a>
### SQLFunction Parser.parse operator

`operation_foundation_database_query_business_behavior_database_query_function_parser_parse_operator`

**Inputs** self, operator\_dict.

**Declared result** ArithmeticExpression.

**Explicit results** expression.as\_(alias) · expression.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Operator {0} requires exactly 2 arguments (left and right operands)”.format(operator\_name).

**Local steps**

- Set tuple(operator\_name, alias, operator\_args) from self.\_extract\_dict\_components(operator\_dict, OPERATOR\_MAPPING, “operator”).
- Set operator from OPERATOR\_MAPPING at operator\_name.
- If (not isinstance(operator\_args, list) or len(operator\_args) differs from 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(operator\_args, list) → len(operator\_args) differs from 2.
  - Call the validation error handler Platform.throw(translated “Operator {0} requires exactly 2 arguments (left and right operands)”.format(operator\_name), Platform.ValidationError).
- Set left from self.\_parse\_and\_validate\_argument(operator\_args at 0).
- Set right from self.\_parse\_and\_validate\_argument(operator\_args at 1).
- If not isinstance(left, Term).
  - Set left from ValueWrapper(left).
- If not isinstance(right, Term).
  - Set right from ValueWrapper(right).
- Set expression from ArithmeticExpression(operator = operator, left = left, right = right).
- If alias.
  - Evaluate self.engine.function\_aliases.add(alias).
  - Return expression.as\_(alias).
- Otherwise.
  - Return expression.

**Methods declared on this owner** [extract dict components](operations-080.md#op-8351075f2ad417), [parse and validate argument](operations-080.md#op-fe50bd87c63761).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L97) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1188)

<a id="op-fe50bd87c63761"></a>
### SQLFunction Parser.parse and validate argument

`operation_foundation_database_query_business_behavior_database_query_function_parser_parse_and_validate_argument`

**Inputs** self, arg, function\_name (named only, default no value).

**Explicit results** arg · self.\_validate\_string\_argument(arg, function\_name = function\_name) · self.parse\_function(arg) · self.parse\_operator(arg).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid nested expression: dictionary must represent a function or operator” · validation helper with Platform.ValidationError — translated “Invalid argument type: {0}. Only strings, numbers, dicts, and None are allowed.”.format(type(arg).\_\_name\_\_).

**Local steps**

- If isinstance(arg, (int bitwise or float)).
  - Return arg.
- Otherwise.
  - If isinstance(arg, str).
    - Return self.\_validate\_string\_argument(arg, function\_name = function\_name).
  - Otherwise.
    - If isinstance(arg, dict).
      - If self.is\_function\_dict(arg).
        - Return self.parse\_function(arg).
      - Otherwise.
        - If self.is\_operator\_dict(arg).
          - Return self.parse\_operator(arg).
        - Otherwise.
          - Call the validation error handler Platform.throw(translated “Invalid nested expression: dictionary must represent a function or operator”, Platform.ValidationError).
    - Otherwise.
      - If arg is identical to no value.
        - Return arg.
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Invalid argument type: {0}. Only strings, numbers, dicts, and None are allowed.”.format(type(arg).\_\_name\_\_), Platform.ValidationError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate string argument](operations-080.md#op-f83ec84fcebe4c), [is function dict](operations-080.md#op-71fa4498ac1d2b), [parse function](operations-080.md#op-b3d840a06feb5d), [is operator dict](operations-080.md#op-fede54d8df08b0), [parse operator](operations-080.md#op-94f658be07e4ec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L5070) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1186)

<a id="op-f83ec84fcebe4c"></a>
### SQLFunction Parser.validate string argument

`operation_foundation_database_query_business_behavior_database_query_function_parser_validate_string_argument`

**Inputs** self, arg, function\_name (named only, default no value).

**Explicit results** Star() · arg at slice 1 to negative 1 · Table(formatted text tab{table\_name}) at field\_name · int(arg) · self.engine.table at arg.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Empty string arguments are not allowed” · validation helper with Platform.ValidationError — translated “'\*' is only allowed in {0} SQL function(s)”.format(“, ”.join(STAR\_ALLOWED\_FUNCTIONS)) · validation helper with Platform.ValidationError — translated “Invalid argument format: {0}. Only quoted string literals or simple field names are allowed.”.format(arg).

**Local steps**

- Set arg from arg.strip().
- If not arg.
  - Call the validation error handler Platform.throw(translated “Empty string arguments are not allowed”, Platform.ValidationError).
- If arg equals “\*”.
  - If function\_name does not belong to STAR\_ALLOWED\_FUNCTIONS.
    - Call the validation error handler Platform.throw(translated “'\*' is only allowed in {0} SQL function(s)”.format(“, ”.join(STAR\_ALLOWED\_FUNCTIONS)), Platform.ValidationError).
  - Return Star().
- If (len(arg) ≥ 2 and arg at 0 belongs to tuple(“'”, “"”) and arg at negative 1 equals arg at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(arg) ≥ 2 → arg at 0 belongs to tuple(“'”, “"”) → arg at negative 1 equals arg at 0.
  - Return arg at slice 1 to negative 1.
- Otherwise.
  - If “′” belongs to arg.
    - If parsed bound to self.engine.\_parse\_backtick\_field\_notation(arg).
      - Set tuple(table\_name, field\_name) from parsed.
      - Evaluate self.engine.check\_select\_field\_permission(table\_name, field\_name).
      - Return Table(formatted text tab{table\_name}) at field\_name.
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Invalid argument format: {0}. Only quoted string literals or simple field names are allowed.”.format(arg), Platform.ValidationError).
  - Otherwise.
    - If arg.isdigit().
      - Return int(arg).
    - Otherwise.
      - If self.\_is\_valid\_field\_name(arg).
        - Evaluate self.\_check\_function\_field\_permission(arg).
        - Return self.engine.table at arg.
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Invalid argument format: {0}. Only quoted string literals or simple field names are allowed.”.format(arg), Platform.ValidationError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is valid field name](operations-080.md#op-75a67abad88de6), [check function field permission](operations-081.md#op-269e6ba82a7f5b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L5510) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1190)

<a id="op-75a67abad88de6"></a>
### SQLFunction Parser.is valid field name

`operation_foundation_database_query_business_behavior_database_query_function_parser_is_valid_field_name`

**Inputs** self, name.

**Declared result** bool.

**Explicit results** SIMPLE\_FIELD\_PATTERN.match(name) is distinct from no value.

**Local steps**

- Return SIMPLE\_FIELD\_PATTERN.match(name) is distinct from no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L6312) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1185)

<a id="op-cc7d1f1922721e"></a>
### SQLFunction Parser.validate alias

`operation_foundation_database_query_business_behavior_database_query_function_parser_validate_alias`

**Inputs** self, alias.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Alias must be a string” · validation helper with Platform.ValidationError — translated “Empty alias is not allowed” · validation helper with Platform.ValidationError — translated “Invalid alias format: {0}. Alias must be a simple identifier.”.format(alias).

**Local steps**

- If not isinstance(alias, str).
  - Call the validation error handler Platform.throw(translated “Alias must be a string”, Platform.ValidationError).
- Set alias from alias.strip().
- If not alias.
  - Call the validation error handler Platform.throw(translated “Empty alias is not allowed”, Platform.ValidationError).
- If not SIMPLE\_FIELD\_PATTERN.match(alias).
  - Call the validation error handler Platform.throw(translated “Invalid alias format: {0}. Alias must be a simple identifier.”.format(alias), Platform.ValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L6391) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1189)
