# Accounting and settlement · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-ff111d53f6d0e0"></a>
### Filter Expression Parser.build logical condition

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_filter_expression_parser_build_logical_condition`

**Inputs** self, condition\_dict, table.

**Explicit results** no value · built\_conditions at 0 · reduce(deferred anonymous expression, built\_conditions).

**Local steps**

- Set logical\_op from next(iter(condition\_dict.keys())).lower().
- Set sub\_conditions from condition\_dict.get(logical\_op).
- Set built\_conditions from list().
- For each sub\_condition in sub\_conditions.
  - Set condition from self.\_build\_from\_parsed(sub\_condition, table).
  - If condition is distinct from no value.
    - Evaluate built\_conditions.append(condition).
- If not built\_conditions.
  - Return no value.
- If len(built\_conditions) equals 1.
  - Return built\_conditions at 0.
- If logical\_op equals “and”.
  - Return reduce(deferred anonymous expression, built\_conditions).
- Otherwise.
  - Return reduce(deferred anonymous expression, built\_conditions).

**Methods declared on this owner** [build from parsed](operations-039.md#op-04b652e6f0b17c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L5878) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L887) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L836)

<a id="op-5e57e135c68125"></a>
### Formula Field Extractor.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_extractor_initialize`

**Inputs** self, field\_name, exclude\_operators = no value.

**Local steps**

- Set self.field\_name from field\_name.
- Set self.exclude\_operators from list of op.lower() for op drawn from (exclude\_operators or list()).
  - Draw op from (exclude\_operators or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in exclude\_operators → list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L6314) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L871)

<a id="op-7257d00dacfc42"></a>
### Formula Field Extractor.extract from rows

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_extractor_extract_from_rows`

**Inputs** self, rows.

**Declared result** set.

**Explicit results** values.

**Local steps**

- Set values from set().
- For each row in rows.
  - If (not hasattr(row, “calculation\_formula”) or not row.calculation\_formula).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(row, “calculation\_formula”) → not row.calculation\_formula.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set parsed from ast.literal\_eval(row.calculation\_formula).
    - Evaluate self.\_extract\_recursive(parsed, values).
  - On failure (tuple(ValueError, SyntaxError)).
    - Continue with the next iteration or loop test.
- Return values.

**Methods declared on this owner** [extract recursive](operations-040.md#op-3b00f3b7251837).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L6463) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L869)

<a id="op-3b00f3b7251837"></a>
### Formula Field Extractor.extract recursive

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_extractor_extract_recursive`

**Inputs** self, parsed, values.

**Local steps**

- If (isinstance(parsed, list) and len(parsed) equals 3).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(parsed, list) → len(parsed) equals 3.
  - Set tuple(field, operator, value) from parsed.
  - If (field equals self.field\_name and operator.lower() does not belong to self.exclude\_operators).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals self.field\_name → operator.lower() does not belong to self.exclude\_operators.
    - If isinstance(value, str).
      - Evaluate values.add(value).
    - Otherwise.
      - If isinstance(value, list).
        - Evaluate values.update(generator of v for v drawn from value where isinstance(v, str)).
          - Draw v from value, keep a combination only if (isinstance(v, str)).
- Otherwise.
  - If isinstance(parsed, dict).
    - For each sub\_conditions in parsed.values().
      - If isinstance(sub\_conditions, list).
        - For each sub\_condition in sub\_conditions.
          - Evaluate self.\_extract\_recursive(sub\_condition, values).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L6701) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L870)

<a id="op-0def7f57a6356e"></a>
### Formula Field Updater.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_updater_initialize`

**Inputs** self, field\_name, value\_mapping, exclude\_operators = no value.

**Local steps**

- Set self.field\_name from field\_name.
- Set self.value\_mapping from value\_mapping.
- Set self.exclude\_operators from list of op.lower() for op drawn from (exclude\_operators or list()).
  - Draw op from (exclude\_operators or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in exclude\_operators → list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L7157) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L872)

<a id="op-58aab5a7beff8a"></a>
### Formula Field Updater.update in rows

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_updater_update_in_rows`

**Inputs** self, rows.

**Declared result** dict at tuple(str, dict at tuple(str, str)).

**State and service calls** request bulk\_update on “Financial Report Row”.

**Explicit results** updated\_rows.

**Local steps**

- Set updated\_rows from mapping().
- For each tuple(row\_name, formula) in rows.items().
  - If not formula.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set parsed from ast.literal\_eval(formula).
    - Set updated from self.\_update\_recursive(parsed).
    - If updated differs from parsed.
      - Set updated\_formula from json.dumps(updated).
      - Set updated\_rows at row\_name from mapping(“calculation\_formula” → updated\_formula).
  - On failure (tuple(ValueError, SyntaxError)).
    - Continue with the next iteration or loop test.
- If updated\_rows.
  - Evaluate Platform.db.bulk\_update(“Financial Report Row”, updated\_rows, update\_modified = false).
- Return updated\_rows.

**Methods declared on this owner** [update recursive](operations-040.md#op-35b0ae1ed40718).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0047.json#L7350) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L873)

<a id="op-35b0ae1ed40718"></a>
### Formula Field Updater.update recursive

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_updater_update_recursive`

**Inputs** self, parsed.

**Explicit results** list(field, operator, updated\_value) · parsed · updated\_dict.

**Local steps**

- If (isinstance(parsed, list) and len(parsed) equals 3).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(parsed, list) → len(parsed) equals 3.
  - Set tuple(field, operator, value) from parsed.
  - If (field equals self.field\_name and operator.lower() does not belong to self.exclude\_operators).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals self.field\_name → operator.lower() does not belong to self.exclude\_operators.
    - Set updated\_value from self.\_update\_value(value).
    - Return list(field, operator, updated\_value).
  - Return parsed.
- Otherwise.
  - If isinstance(parsed, dict).
    - Set updated\_dict from mapping().
    - For each tuple(key, sub\_conditions) in parsed.items().
      - Set updated\_conditions from list of self.\_update\_recursive(sub\_condition) for sub\_condition drawn from sub\_conditions.
        - Draw sub\_condition from sub\_conditions.
      - Set updated\_dict at key from updated\_conditions.
    - Return updated\_dict.
- Return parsed.

**Methods declared on this owner** [update value](operations-040.md#op-bf9ba57389d7fc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L874)

<a id="op-bf9ba57389d7fc"></a>
### Formula Field Updater.update value

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_field_updater_update_value`

**Inputs** self, value.

**Explicit results** self.value\_mapping.get(value, value) · list of self.value\_mapping.get(v, v) when isinstance(v, str), otherwise v for v drawn from value · value.

**Local steps**

- If isinstance(value, str).
  - Return self.value\_mapping.get(value, value).
- Otherwise.
  - If isinstance(value, list).
    - Return list of self.value\_mapping.get(v, v) when isinstance(v, str), otherwise v for v drawn from value.
      - Draw v from value.
      - Value choice on isinstance(v, str) — true gives self.value\_mapping.get(v, v), false gives v.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L409) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L875)

<a id="op-52cb92eb86635b"></a>
### Get filtered accounts

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_get_filtered_accounts`

**Inputs** company, account\_rows.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** DataCollector.get\_filtered\_accounts(company, account\_rows).

**Explicit failure paths** validation helper — translated “Company is required”.

**Local steps**

- If not company.
  - Call the validation error handler Platform.throw(translated “Company is required”, title = translated “Missing Company”).
- Evaluate Platform.has\_permission(“Financial Report Template”, ptype = “read”, throw = true).
- Evaluate Platform.has\_permission(“Company”, doc = company, throw = true).
- If isinstance(account\_rows, str).
  - Set account\_rows from json.loads(account\_rows, object\_hook = Platform.\_dict).
- Return DataCollector.get\_filtered\_accounts(company, account\_rows).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Financial Report Template”, ptype = “read”, throw = true), Platform.has\_permission(“Company”, doc = company, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L877)

<a id="op-2009a9b89691c1"></a>
### Get children accounts

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_get_children_accounts`

**Inputs** doctype, parent, company, filtered\_accounts = no value, missed = false, is\_root = false, include\_disabled = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list() · children\_accounts when missed, otherwise list() · valid\_accounts.

**Local steps**

- Evaluate Platform.has\_permission(doctype, ptype = “read”, throw = true).
- Set children\_accounts from get\_children(doctype, parent, company, is\_root = is\_root, include\_disabled = include\_disabled).
- If not children\_accounts.
  - Return list().
- If isinstance(filtered\_accounts, str).
  - Set filtered\_accounts from Platform.parse\_json(filtered\_accounts).
- If not filtered\_accounts.
  - Return children\_accounts when missed, otherwise list().
    - Value choice on missed — true gives children\_accounts, false gives list().
- Set valid\_accounts from list().
- For each account in children\_accounts.
  - If account.expandable.
    - Evaluate valid\_accounts.append(account).
    - Continue with the next iteration or loop test.
  - Set is\_in\_filtered from account.value belongs to filtered\_accounts.
  - If ((missed and not is\_in\_filtered) or (not missed and is\_in\_filtered)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (missed and not is\_in\_filtered) → (not missed and is\_in\_filtered).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in missed → not is\_in\_filtered.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not missed → is\_in\_filtered.
    - Evaluate valid\_accounts.append(account).
- Return valid\_accounts.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, ptype = “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L963) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L876)

<a id="op-1d4edb96228aa7"></a>
### Row Processor.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_initialize`

**Inputs** self, context.

**Local steps**

- Set self.context from context.
- Set self.period\_list from context.period\_list.
- Set self.row\_values from mapping().
- Set self.dependency\_resolver from DependencyResolver(context.template).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L1522) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L902)

<a id="op-e0ca1ed4f0411f"></a>
### Row Processor.process all rows

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_all_rows`

**Inputs** self.

**Declared result** list at RowData.

**Explicit results** processed\_rows.

**Local steps**

- Set processing\_order from self.dependency\_resolver.get\_processing\_order().
- Set processed\_rows from list().
- Set account\_summary from self.context.raw\_data.get(“summary”, mapping()).
- Set account\_details from self.context.raw\_data.get(“account\_details”, mapping()).
- For each row in processing\_order.
  - Set row\_data from self.\_process\_single\_row(row, account\_summary, account\_details).
  - Evaluate processed\_rows.append(row\_data).
- Evaluate processed\_rows.sort(key = deferred anonymous expression).
- Return processed\_rows.

**Methods declared on this owner** [process single row](operations-040.md#op-cc142ba95bd1d6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L1653) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L904)

<a id="op-cc142ba95bd1d6"></a>
### Row Processor.process single row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_single_row`

**Inputs** self, row, account\_summary, account\_details.

**Declared result** RowData.

**Explicit results** self.\_process\_account\_row(row, account\_summary, account\_details) · self.\_process\_api\_row(row) · self.\_process\_formula\_row(row) · self.\_process\_blank\_row(row) · self.\_process\_column\_break\_row(row) · 2 additional forms in the steps below.

**Local steps**

- If row.data\_source equals “Account Data”.
  - Return self.\_process\_account\_row(row, account\_summary, account\_details).
- Otherwise.
  - If row.data\_source equals “Custom API”.
    - Return self.\_process\_api\_row(row).
  - Otherwise.
    - If row.data\_source equals “Calculated Amount”.
      - Return self.\_process\_formula\_row(row).
    - Otherwise.
      - If row.data\_source equals “Blank Line”.
        - Return self.\_process\_blank\_row(row).
      - Otherwise.
        - If row.data\_source equals “Column Break”.
          - Return self.\_process\_column\_break\_row(row).
        - Otherwise.
          - If row.data\_source equals “Section Break”.
            - Return self.\_process\_section\_break\_row(row).
          - Otherwise.
            - Return RowData(row = row, values = (list(0.0) × len(self.period\_list))).

**Methods declared on this owner** [process account row](operations-040.md#op-af22662c580ace), [process api row](operations-040.md#op-b85841de861188), [process formula row](operations-040.md#op-69c369f19ab250), [process blank row](operations-040.md#op-1d614c8e906598), [process column break row](operations-040.md#op-227a9e14a9c30f), [process section break row](operations-040.md#op-53648e6111c384).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L1987) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L910)

<a id="op-af22662c580ace"></a>
### Row Processor.process account row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_account_row`

**Inputs** self, row, account\_summary, account\_details.

**Declared result** RowData.

**Explicit results** RowData(row = row, values = values, account\_details = details).

**Local steps**

- Set ref\_code from row.reference\_code.
- Set values from account\_summary.get(ref\_code, (list(0.0) × len(self.period\_list))).
- Set details from account\_details.get(ref\_code, mapping()).
- If ref\_code.
  - Set self.row\_values at ref\_code from values.
- Return RowData(row = row, values = values, account\_details = details).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L2434) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L903)

<a id="op-b85841de861188"></a>
### Row Processor.process api row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_application_programming_interface_row`

**Inputs** self, row.

**Declared result** RowData.

**Explicit results** RowData(row = row, values = values).

**Local steps**

- Set api\_path from row.calculation\_formula.
- Set method from get\_valid\_api\_method(api\_path).
- Attempt the following.
  - Set values from Platform.call(method, filters = self.context.filters, periods = self.period\_list, row = row).
  - If row.reverse\_sign.
    - Set values from list of (negative 1 × v) for v drawn from values.
      - Draw v from values.
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(formatted text Custom API Error: {api\_path} - {e}).
  - Set values from (list(0.0) × len(self.period\_list)).
- If row.reference\_code.
  - Set self.row\_values at row.reference\_code from values.
- Return RowData(row = row, values = values).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L2686) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L905)

<a id="op-69c369f19ab250"></a>
### Row Processor.process formula row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_formula_row`

**Inputs** self, row.

**Declared result** RowData.

**Explicit results** RowData(row = row, values = values).

**Local steps**

- Set calculator from FormulaCalculator(self.row\_values, self.period\_list).
- Set values from calculator.evaluate\_formula(row).
- If row.reference\_code.
  - Set self.row\_values at row.reference\_code from values.
- Return RowData(row = row, values = values).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3090) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L908)

<a id="op-1d614c8e906598"></a>
### Row Processor.process blank row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_blank_row`

**Inputs** self, row.

**Declared result** RowData.

**Explicit results** RowData(row = row, values = (list(empty text) × len(self.period\_list))).

**Local steps**

- Return RowData(row = row, values = (list(empty text) × len(self.period\_list))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3271) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L906)

<a id="op-227a9e14a9c30f"></a>
### Row Processor.process column break row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_column_break_row`

**Inputs** self, row.

**Declared result** RowData.

**Explicit results** RowData(row = row, values = list()).

**Local steps**

- Return RowData(row = row, values = list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3373) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L907)

<a id="op-53648e6111c384"></a>
### Row Processor.process section break row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_processor_process_section_break_row`

**Inputs** self, row.

**Declared result** RowData.

**Explicit results** RowData(row = row, values = list()).

**Local steps**

- Return RowData(row = row, values = list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3446) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L960) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L909)

<a id="op-96de1da4b42bf1"></a>
### Dependency Resolver.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_dependency_resolver_initialize`

**Inputs** self, template.

**Local steps**

- Set self.template from template.
- Set self.rows from template.rows.
- Set self.row\_map from mapping of row.reference\_code → row for row drawn from self.rows where row.reference\_code.
  - Draw row from self.rows, keep a combination only if (row.reference\_code).
- Set self.dependencies from mapping().
- Evaluate self.\_validate\_dependencies().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dependencies](operations-040.md#op-463a1cc0ea2db8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3519) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L827)

<a id="op-463a1cc0ea2db8"></a>
### Dependency Resolver.validate dependencies

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_dependency_resolver_validate_dependencies`

**Inputs** self.

**Local steps**

- Set validator from DependencyValidator(self.template).
- Set result from validator.validate().
- Evaluate result.notify\_user().
- Set self.dependencies from validator.dependencies.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3688) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L829)

<a id="op-07d475f33d1ef0"></a>
### Dependency Resolver.get processing order

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_dependency_resolver_get_processing_order`

**Inputs** self.

**Declared result** list.

**Explicit results** ordered\_rows.

**Local steps**

- Set api\_rows from list().
- Set account\_rows from list().
- Set formula\_rows from list().
- Set other\_rows from list().
- For each row in self.rows.
  - If row.data\_source equals “Custom API”.
    - Evaluate api\_rows.append(row).
  - Otherwise.
    - If row.data\_source equals “Account Data”.
      - Evaluate account\_rows.append(row).
    - Otherwise.
      - If row.data\_source equals “Calculated Amount”.
        - Evaluate formula\_rows.append(row).
      - Otherwise.
        - Evaluate other\_rows.append(row).
- Set ordered\_rows from (api\_rows + account\_rows).
- If formula\_rows.
  - Set ordered\_formula\_rows from self.\_topological\_sort(formula\_rows).
  - Evaluate ordered\_rows.extend(ordered\_formula\_rows).
- Evaluate ordered\_rows.extend(other\_rows).
- Return ordered\_rows.

**Methods declared on this owner** [topological sort](operations-040.md#op-3603c78b76a501).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L3811) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L826)

<a id="op-3603c78b76a501"></a>
### Dependency Resolver.topological sort

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_dependency_resolver_topological_sort`

**Inputs** self, formula\_rows.

**Declared result** list.

**Explicit results** result.

**Local steps**

- Set formula\_row\_map from mapping of row.reference\_code → row for row drawn from formula\_rows where row.reference\_code.
  - Draw row from formula\_rows, keep a combination only if (row.reference\_code).
- Set adj\_list from mapping of code → list() for code drawn from formula\_row\_map.
  - Draw code from formula\_row\_map.
- Set in\_degree from mapping of code → 0 for code drawn from formula\_row\_map.
  - Draw code from formula\_row\_map.
- For each code in formula\_row\_map.
  - Set deps from self.dependencies.get(code, list()).
  - For each dep in deps.
    - If dep belongs to formula\_row\_map.
      - Evaluate adj\_list at dep.append(code).
      - Update in\_degree at code using + 1.
- Set queue from list of code for tuple(code, degree) drawn from in\_degree.items() where degree equals 0.
  - Draw tuple(code, degree) from in\_degree.items(), keep a combination only if (degree equals 0).
- Set result from list().
- While queue.
  - Set current from queue.pop(0).
  - Evaluate result.append(formula\_row\_map at current).
  - For each neighbor in adj\_list at current.
    - Update in\_degree at neighbor using − 1.
    - If in\_degree at neighbor equals 0.
      - Evaluate queue.append(neighbor).
- Set result\_set from set(result).
- For each row in formula\_rows.
  - If row does not belong to result\_set.
    - Evaluate result.append(row).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L4203) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L828)

<a id="op-4dcecdaaa3d8de"></a>
### Formula Calculator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_calculator_initialize`

**Inputs** self, row\_data, period\_list.

**Local steps**

- Set self.row\_data from row\_data.
- Set self.period\_list from period\_list.
- Set self.precision from get\_currency\_precision().
- Set self.validator from CalculationFormulaValidator(set(row\_data.keys())).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L868)
