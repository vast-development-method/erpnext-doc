# Accounting and settlement · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-d27ee5f5783159"></a>
### Template Structure Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_template_structure_validator_validate`

**Inputs** self, template.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- Evaluate result.merge(self.\_validate\_reference\_codes(template)).
- Evaluate result.merge(self.\_validate\_required\_fields(template)).
- Return result.

**Methods declared on this owner** [validate reference codes](operations-044.md#op-2689081bdcc4a6), [validate required fields](operations-044.md#op-9bac87e7e73dc5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L1202) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L943)

<a id="op-2689081bdcc4a6"></a>
### Template Structure Validator.validate reference codes

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_template_structure_validator_validate_reference_codes`

**Inputs** self, template.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- Set used\_codes from set().
- For each row in template.rows.
  - If not row.reference\_code.
    - Continue with the next iteration or loop test.
  - Set ref\_code from row.reference\_code.
  - If not re.match(“^&#91;A-Za-z&#93;&#91;A-Za-z0-9\_&#93;\*$”, ref\_code).
    - Evaluate result.add\_error(ValidationIssue(message = translated “Invalid line reference format: '{0}'. Must start with a letter and contain only letters, numbers and underscores”.format(ref\_code), row\_idx = row.idx)).
  - Otherwise.
    - If (keyword.iskeyword(ref\_code) or ref\_code belongs to FORMULA\_FUNCTIONS).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in keyword.iskeyword(ref\_code) → ref\_code belongs to FORMULA\_FUNCTIONS.
      - Evaluate result.add\_error(ValidationIssue(message = translated “'{0}' is a reserved name and cannot be used as a line reference”.format(ref\_code), row\_idx = row.idx)).
  - If ref\_code belongs to used\_codes.
    - Evaluate result.add\_error(ValidationIssue(message = translated “Duplicate line reference: '{0}'”.format(ref\_code), row\_idx = row.idx)).
  - Evaluate used\_codes.add(ref\_code).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L944)

<a id="op-9bac87e7e73dc5"></a>
### Template Structure Validator.validate required fields

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_template_structure_validator_validate_required_fields`

**Inputs** self, template.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- For each row in template.rows.
  - If (row.data\_source equals “Account Data” and not row.balance\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.data\_source equals “Account Data” → not row.balance\_type.
    - Evaluate result.add\_error(ValidationIssue(message = translated “Balance Type is required for Account Data”, row\_idx = row.idx)).
  - If row.data\_source belongs to list(“Account Data”, “Calculated Amount”, “Custom API”).
    - If not row.calculation\_formula.
      - Evaluate result.add\_error(ValidationIssue(message = translated “{0} is required when {1} is {2}”.format(get\_formula\_field\_label(row.data\_source), row.meta.get\_translated\_label(“data\_source”), translated row.data\_so ….
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L1752) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L945)

<a id="op-f417a028fedcf0"></a>
### Dependency Validator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_dependency_validator_initialize`

**Inputs** self, template.

**Local steps**

- Set self.template from template.
- Set self.dependencies from self.\_build\_dependency\_graph().

If control reaches the end, it returns no value.

**Methods declared on this owner** [build dependency graph](operations-044.md#op-d914663db677e3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L2159) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L933)

<a id="op-b2a5a6e136d56c"></a>
### Dependency Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_dependency_validator_validate`

**Inputs** self, context = no value.

**Declared result** ValidationResult.

**Explicit results** self.\_validate\_circular\_dependencies().

**Local steps**

- Return self.\_validate\_circular\_dependencies().

**Methods declared on this owner** [validate circular dependencies](operations-044.md#op-5cbf1a7e440287).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L934)

<a id="op-d914663db677e3"></a>
### Dependency Validator.build dependency graph

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_dependency_validator_build_dependency_graph`

**Inputs** self.

**Declared result** dict at tuple(str, list at str).

**Explicit results** graph.

**Local steps**

- Set graph from mapping().
- Set available\_codes from set of row.reference\_code for row drawn from self.template.rows where row.reference\_code.
  - Draw row from self.template.rows, keep a combination only if (row.reference\_code).
- For each row in self.template.rows.
  - If (row.reference\_code and row.data\_source equals “Calculated Amount” and row.calculation\_formula).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_code → row.data\_source equals “Calculated Amount” → row.calculation\_formula.
    - Set deps from list of code for code drawn from extract\_reference\_codes\_from\_formula(row.calculation\_formula, list(available\_codes)) where code differs from row.reference\_code.
      - Draw code from extract\_reference\_codes\_from\_formula(row.calculation\_formula, list(available\_codes)), keep a combination only if (code differs from row.reference\_code).
    - If deps.
      - Set graph at row.reference\_code from deps.
- Return graph.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L2386) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L932)

<a id="op-5cbf1a7e440287"></a>
### Dependency Validator.validate circular dependencies

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_dependency_validator_validate_circular_dependencies`

**Inputs** self.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- Set tuple(WHITE, GRAY, BLACK) from tuple(0, 1, 2).
- Set colors from mapping of node → WHITE for node drawn from self.dependencies.
  - Draw node from self.dependencies.
- Bind local operation dfs for subsequent calls.
- For each node in self.dependencies.
  - If colors at node equals WHITE.
    - Evaluate dfs(node, list()).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L2708) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L935)

<a id="op-c1d53864e5f627"></a>
### Dependency Validator.validate circular dependencies.dfs

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_dependency_validator_validate_circular_dependencies_depth_first_search`

**Inputs** node, path.

**Explicit results** no value.

**Local steps**

- If node does not belong to colors.
  - Return no value.
- If colors at node equals GRAY.
  - Set cycle\_start from path.index(node).
  - Set cycle from list(expanded path at slice cycle\_start to no value, node).
  - Evaluate result.add\_error(ValidationIssue(message = translated “Circular dependency detected: {0}”.format(“ → ”.join(cycle)))).
  - Return no value.
- If colors at node equals BLACK.
  - Return no value.
- Set colors at node from GRAY.
- Evaluate path.append(node).
- For each neighbor in self.dependencies.get(node, list()).
  - Evaluate dfs(neighbor, path.copy()).
- Set colors at node from BLACK.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L3335) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L936)

<a id="op-767f6c2fccb916"></a>
### Calculation Formula Validator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_calculation_formula_validator_initialize`

**Inputs** self, reference\_codes.

**Local steps**

- Set self.reference\_codes from reference\_codes.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L4240) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L928)

<a id="op-68184f0e9ed674"></a>
### Calculation Formula Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_calculation_formula_validator_validate`

**Inputs** self, row.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- If row.data\_source differs from “Calculated Amount”.
  - Return result.
- Set formula from self.\_preprocess\_formula(row.calculation\_formula).
- If not self.\_are\_parentheses\_balanced(formula).
  - Evaluate result.add\_error(ValidationIssue(message = translated “Formula has unbalanced parentheses”, row\_idx = row.idx)).
  - Return result.
- Set available\_codes from list(self.reference\_codes).
- Set refs from extract\_reference\_codes\_from\_formula(formula, available\_codes).
- If (row.reference\_code and row.reference\_code belongs to refs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_code → row.reference\_code belongs to refs.
  - Evaluate result.add\_error(ValidationIssue(message = translated “Formula references itself ('{0}')”.format(row.reference\_code), row\_idx = row.idx)).
- Set eval\_error from self.\_test\_formula\_evaluation(formula, available\_codes).
- If eval\_error.
  - Evaluate result.add\_error(ValidationIssue(message = translated “Formula evaluation error: {0}”.format(eval\_error), row\_idx = row.idx)).
- Return result.

**Methods declared on this owner** [preprocess formula](operations-044.md#op-734f6a85040f31), [are parentheses balanced](operations-044.md#op-35e95cf98b6add), [test formula evaluation](operations-044.md#op-e62c0c1108a0e0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L931)

<a id="op-734f6a85040f31"></a>
### Calculation Formula Validator.preprocess formula

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_calculation_formula_validator_preprocess_formula`

**Inputs** self, formula.

**Declared result** str.

**Explicit results** empty text · formula.strip().

**Local steps**

- If (not formula or not isinstance(formula, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not formula → not isinstance(formula, str).
  - Return empty text.
- Return formula.strip().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L4882) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L929)

<a id="op-35e95cf98b6add"></a>
### Calculation Formula Validator.are parentheses balanced

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_calculation_formula_validator_are_parentheses_balanced`

**Inputs** formula.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** formula.count(“(”) equals formula.count(“)”).

**Local steps**

- Return formula.count(“(”) equals formula.count(“)”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L4996) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L927)

<a id="op-e62c0c1108a0e0"></a>
### Calculation Formula Validator.test formula evaluation

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_calculation_formula_validator_test_formula_evaluation`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, formula, available\_codes.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L930)

<a id="op-0d5f4b196ac514"></a>
### Account Filter Validator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_account_filter_validator_initialize`

**Inputs** self, account\_fields = no value.

**Local steps**

- Set self.account\_meta from Platform.get\_meta(“Account”).
- Set self.account\_fields from (account\_fields or set(self.account\_meta.\_valid\_columns)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_fields → set(self.account\_meta.\_valid\_columns).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L5578) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L923)

<a id="op-e87da7d43859d2"></a>
### Account Filter Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_account_filter_validator_validate`

**Inputs** self, row.

**Declared result** ValidationResult.

**Explicit results** ValidationResult() · self.validate\_filter(row).

**Local steps**

- If row.data\_source differs from “Account Data”.
  - Return ValidationResult().
- Return self.validate\_filter(row).

**Methods declared on this owner** [validate filter](operations-044.md#op-c4afd93c4b5ee5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L5717) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L924)

<a id="op-c4afd93c4b5ee5"></a>
### Account Filter Validator.validate filter

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_account_filter_validator_validate_filter`

**Inputs** self, row.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- Attempt the following.
  - Set filter\_config from json.loads(row.calculation\_formula).
  - Set error from self.\_validate\_filter\_structure(filter\_config, self.account\_fields, row.advanced\_filtering).
  - If error.
    - Evaluate result.add\_error(ValidationIssue(message = \_(“&#91;{0}&#93; {1}”, context = “Financial Report Template”).format(get\_formula\_field\_label(“Account Data”), error), row\_idx = row.idx)).
- On failure (json.JSONDecodeError) bound to e.
  - Evaluate result.add\_error(ValidationIssue(message = \_(“&#91;{0}&#93; {1}”, context = “Financial Report Template”).format(get\_formula\_field\_label(“Account Data”), translated “Invalid JSON format: {0}”.format(str(e))), row\_i ….
- Return result.

**Methods declared on this owner** [validate filter structure](operations-044.md#op-439feeb6d1d6bb).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L5823) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L925)

<a id="op-439feeb6d1d6bb"></a>
### Account Filter Validator.validate filter structure

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_account_filter_validator_validate_filter_structure`

**Inputs** self, filter\_config, account\_fields, advanced\_filtering = false.

**Declared result** (str bitwise or no value).

**Explicit results** translated “Filter must be &#91;field, operator, value&#93;” · translated “Field and operator must be strings” · translated “Field '{0}' is not a valid Account field”.format(field) · translated “Invalid operator '{0}'”.format(operator) · translated “Operator '{0}' requires a list value”.format(operator) · 6 additional forms in the steps below.

**Local steps**

- If isinstance(filter\_config, list).
  - If len(filter\_config) differs from 3.
    - Return translated “Filter must be &#91;field, operator, value&#93;”.
  - Set tuple(field, operator, value) from filter\_config.
  - If (not isinstance(field, str) or not isinstance(operator, str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(field, str) → not isinstance(operator, str).
    - Return translated “Field and operator must be strings”.
  - If field does not belong to account\_fields.
    - Return translated “Field '{0}' is not a valid Account field”.format(field).
  - Set normalized\_operator from operator.casefold().
  - If normalized\_operator does not belong to OPERATOR\_MAP.
    - Return translated “Invalid operator '{0}'”.format(operator).
  - If (normalized\_operator belongs to list(“in”, “not in”) and not isinstance(value, list)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in normalized\_operator belongs to list(“in”, “not in”) → not isinstance(value, list).
    - Return translated “Operator '{0}' requires a list value”.format(operator).
- Otherwise.
  - If isinstance(filter\_config, dict).
    - If len(filter\_config) differs from 1.
      - Return translated “Logical condition must have exactly one operator”.
    - Set op from next(iter(filter\_config.keys())).lower().
    - If op does not belong to list(“and”, “or”).
      - Return translated “Logical operators must be 'and' or 'or'”.
    - Set conditions from filter\_config at next(iter(filter\_config.keys())).
    - If (not isinstance(conditions, list) or len(conditions) &lt; 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(conditions, list) → len(conditions) &lt; 1.
      - Return translated “Logical conditions need at least 1 sub-condition”.
    - For each condition in conditions.
      - Set error from self.\_validate\_filter\_structure(condition, account\_fields, advanced\_filtering).
      - If error.
        - Return error.
  - Otherwise.
    - Return translated “Filter must be a list or dict”.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L926)

<a id="op-a2970e4890982d"></a>
### Formula Validator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_formula_validator_initialize`

**Inputs** self, template.

**Local steps**

- Set self.template from template.
- Set reference\_codes from set of row.reference\_code for row drawn from template.rows where row.reference\_code.
  - Draw row from template.rows, keep a combination only if (row.reference\_code).
- Set self.calculation\_validator from CalculationFormulaValidator(reference\_codes).
- Set self.account\_filter\_validator from AccountFilterValidator().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0052.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L938)

<a id="op-c9f53dea2c02d2"></a>
### Formula Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_formula_validator_validate`

**Inputs** self, row.

**Declared result** ValidationResult.

**Explicit results** result · self.calculation\_validator.validate(row) · self.account\_filter\_validator.validate(row).

**Local steps**

- Set result from ValidationResult().
- If not row.calculation\_formula.
  - Return result.
- If row.data\_source equals “Calculated Amount”.
  - Return self.calculation\_validator.validate(row).
- Otherwise.
  - If row.data\_source equals “Account Data”.
    - Return self.account\_filter\_validator.validate(row).
  - Otherwise.
    - If row.data\_source equals “Custom API”.
      - Evaluate result.merge(self.\_validate\_custom\_api(row)).
- Return result.

**Methods declared on this owner** [validate custom api](operations-044.md#op-3073ad376b21f8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0052.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L939)

<a id="op-3073ad376b21f8"></a>
### Formula Validator.validate custom api

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_formula_validator_validate_custom_application_programming_interface`

**Inputs** self, row.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult().
- Set api\_path from row.calculation\_formula.
- If “.” does not belong to api\_path.
  - Evaluate result.add\_error(ValidationIssue(message = translated “{0} should be in format: app.module.method”.format(get\_formula\_field\_label(row.data\_source)), row\_idx = row.idx)).
  - Return result.
- Attempt the following.
  - Evaluate get\_valid\_api\_method(api\_path).
- On failure (Exception) bound to e.
  - If isinstance(e, (Platform.PermissionError bitwise or Platform.ValidationError)).
    - Evaluate Platform.clear\_last\_message().
  - If isinstance(e, Platform.PermissionError).
    - Set message from \_(“&#91;{0}&#93; {1}”, context = “Financial Report Template”).format(get\_formula\_field\_label(row.data\_source), translated “Method '{0}' must be whitelisted and permit GET requests”.format(api\_path)).
  - Otherwise.
    - Set message from translated “Could not validate {0}: {1}”.format(get\_formula\_field\_label(row.data\_source), str(e)).
  - Evaluate result.add\_error(ValidationIssue(message = message, row\_idx = row.idx)).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0052.json#L430) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L940)

<a id="op-f49bf3692cc7a2"></a>
### Extract reference codes from formula

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_extract_reference_codes_from_formula`

**Inputs** formula, available\_codes.

**Declared result** list at str.

**Explicit results** found\_codes.

**Local steps**

- Set found\_codes from list().
- For each code in available\_codes.
  - Set pattern from ((“\\b” + re.escape(code)) + “\\b”).
  - If re.search(pattern, formula).
    - Evaluate found\_codes.append(code).
- Return found\_codes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0052.json#L1013) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L937)

## Service · Financial statements

<a id="op-5108c064ad932b"></a>
### Get dimension values

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_dimension_values`

**Inputs** filters.

**Declared result** tuple at tuple((str bitwise or no value), list).

**Explicit results** tuple(no value, list()) · tuple(fieldname, query.run(pluck = true)).

**Local steps**

- If not filters.group\_by\_dimension.
  - Return tuple(no value, list()).
- Set dim\_doctype from filters.group\_by\_dimension.
- Set fieldname from get\_dimension\_fieldname(dim\_doctype).
- Set meta from Platform.get\_meta(dim\_doctype).
- Set is\_tree from bool(meta.is\_tree).
- Set dim from Platform.qb.DocType(dim\_doctype).
- Set query from Platform.qb.from\_(dim).select(dim.name).
- If (is\_tree and meta.has\_field(“is\_group”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_tree → meta.has\_field(“is\_group”).
  - Set query from query.where(dim.is\_group equals 0).
- If meta.has\_field(“company”).
  - Set query from query.where(dim.company equals filters.company).
- If selected bound to filters.get(fieldname).
  - If isinstance(selected, str).
    - Set selected from Platform.parse\_json(selected).
  - If is\_tree.
    - Set selected from get\_dimension\_with\_children(dim\_doctype, selected).
  - Set query from query.where(dim.name.isin(selected)).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(dim\_doctype).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set query from query.orderby(dim.name).
- Return tuple(fieldname, query.run(pluck = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L2636) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L929)

<a id="op-37f53410555ef8"></a>
### Get dimension period list

`operation_enterprise_accounts_report_financial_statements_business_behavior_get_dimension_period_list`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** list() · period\_list.

**Local steps**

- Set tuple(fieldname, dimensions) from get\_dimension\_values(filters).
- If (not fieldname or not dimensions).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fieldname → not dimensions.
  - Return list().
- Set period\_buckets from get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters.period\_start\_date, filters.period\_end\_date, accumulated\_values = filters.accumulated\_values, company = filters.company, …).
- If not period\_buckets.
  - Return list().
- Set period\_list from list().
- Set used\_keys from set().
- For each dimension in dimensions.
  - Set dim\_key\_base from Platform.scrub(dimension).
  - For each period in period\_buckets.
    - Set key from formatted text {dim\_key\_base}\_{period.key}.
    - If key belongs to used\_keys.
      - Set key from formatted text {key}\_{len(used\_keys)}.
    - Evaluate used\_keys.add(key).
    - Set cell from Platform.\_dict(period).
    - Evaluate cell.update(mapping(“key” → key, “label” → formatted text {dimension} - {period.label}, “dimension\_field” → fieldname, “dimension\_value” → dimension, …)).
    - Evaluate period\_list.append(cell).
- Return period\_list.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L3427) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L928)

<a id="op-875178c8b30e12"></a>
### Build period list

`operation_enterprise_accounts_report_financial_statements_business_behavior_build_period_list`

**Inputs** filters, accumulated\_values = false.

**Declared result** list at dict.

**Explicit results** get\_dimension\_period\_list(filters) · get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters.period\_start\_date, filters.period\_end\_date, accumulated\_values = accumulated\_values, company = filters.company, …).

**Local steps**

- If (filters.group\_by\_dimension and not filters.report\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.group\_by\_dimension → not filters.report\_template.
  - Return get\_dimension\_period\_list(filters).
- Return get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters.period\_start\_date, filters.period\_end\_date, accumulated\_values = accumulated\_values, company = filters.company, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L913)
