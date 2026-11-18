# Accounting and settlement · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-cd398d5a2873f9"></a>
### Formula Calculator.evaluate formula

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_calculator_evaluate_formula`

**Inputs** self, report\_row.

**Declared result** list at float.

**Explicit results** (list(0.0) × len(self.period\_list)) · results.

**Local steps**

- Set validation\_result from self.validator.validate(report\_row).
- Set formula from (report\_row.calculation\_formula or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in report\_row.calculation\_formula → empty text.
- Set negation\_factor from negative 1 when report\_row.reverse\_sign, otherwise 1.
  - Value choice on report\_row.reverse\_sign — true gives negative 1, false gives 1.
- If validation\_result.issues.
  - Set messages from text in the contract.join(generator of str(issue) for issue drawn from validation\_result.issues).
    - Draw issue from validation\_result.issues.
  - Evaluate Platform.log\_error(formatted text Formula validation errors found: {messages}).
  - Return (list(0.0) × len(self.period\_list)).
- Set results from list().
- For each i in range(len(self.period\_list)).
  - Set result from self.\_evaluate\_for\_period(formula, i, negation\_factor).
  - Evaluate results.append(result).
- Return results.

**Methods declared on this owner** [evaluate for period](operations-041.md#op-868821a99e6d4d).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L867)

<a id="op-868821a99e6d4d"></a>
### Formula Calculator.evaluate for period

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_calculator_evaluate_for_period`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, formula, period\_index, negation\_factor.

**Explicit result forms** a scalar literal, the result of a delegated call.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 0 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L866)

<a id="op-49be3ef25c496f"></a>
### Formula Calculator.build context

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formula_calculator_build_context`

**Inputs** self, period\_index.

**Declared result** dict at tuple(str, Any).

**Explicit results** context.

**Local steps**

- Set context from mapping().
- For each tuple(code, values) in self.row\_data.items().
  - If period\_index &lt; len(values).
    - Set context at code from (values at period\_index or 0.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in values at period\_index → 0.0.
  - Otherwise.
    - Set context at code from 0.0.
- Evaluate context.update(FORMULA\_FUNCTIONS).
- Return context.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L865)

<a id="op-6517de95958429"></a>
### Data Formatter.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_formatter_initialize`

**Inputs** self, context.

**Local steps**

- Set self.context from context.
- Set self.formatting\_engine from FormattingEngine().
- Set self.organizer from SegmentOrganizer(context.processed\_rows).
- If self.organizer.is\_single\_segment.
  - Set self.formatter from SingleSegmentFormatter(context, self.formatting\_engine).
- Otherwise.
  - Set self.formatter from MultiSegmentFormatter(context, self.formatting\_engine).
- If context.show\_detailed.
  - Evaluate self.\_expand\_segments\_with\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [expand segments with details](operations-041.md#op-5661b103d66a60).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L6138) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L825)

<a id="op-35af85d0beb354"></a>
### Data Formatter.format for display

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_formatter_format_for_display`

**Inputs** self.

**Declared result** tuple at tuple(list at dict, list at dict).

**Explicit results** tuple(formatted\_data, columns).

**Local steps**

- Set formatted\_data from self.\_format\_rows().
- Set columns from self.\_generate\_columns().
- Return tuple(formatted\_data, columns).

**Methods declared on this owner** [format rows](operations-041.md#op-6577a34eae8981), [generate columns](operations-041.md#op-fb751b530a1877).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L6383) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L822)

<a id="op-6577a34eae8981"></a>
### Data Formatter.format rows

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_formatter_format_rows`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** formatted\_data.

**Local steps**

- Set formatted\_data from list().
- For each section in self.organizer.sections.
  - For each row\_index in range(self.organizer.max\_rows(section)).
    - Set formatted\_row from self.formatter.format\_row(section.segments, row\_index).
    - If formatted\_row.
      - Set formatted\_row at “\_segment\_info” from mapping(“total\_segments” → len(section.segments), “period\_keys” → list of p at “key” for p drawn from self.context.period\_list).
        - Draw p from self.context.period\_list.
      - Evaluate formatted\_data.append(formatted\_row).
- Return formatted\_data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L6519) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L823)

<a id="op-fb751b530a1877"></a>
### Data Formatter.generate columns

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_formatter_generate_columns`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** self.formatter.get\_columns(self.organizer.section\_with\_max\_segments.segments, base\_columns).

**Local steps**

- Set base\_columns from get\_columns(self.context.filters.get(“periodicity”), self.context.period\_list, self.context.filters.get(“accumulated\_values”) belongs to tuple(1, no value), self.context.filters.get(“company”)).
- Return self.formatter.get\_columns(self.organizer.section\_with\_max\_segments.segments, base\_columns).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L6823) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L824)

<a id="op-5661b103d66a60"></a>
### Data Formatter.expand segments with details

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_data_formatter_expand_segments_with_details`

**Inputs** self.

**Local steps**

- For each section in self.organizer.sections.
  - For each segment in section.segments.
    - Set expanded\_rows from list().
    - For each row\_data in segment.rows.
      - Evaluate expanded\_rows.append(row\_data).
      - If row\_data.account\_details.
        - Set detail\_rows from DetailRowBuilder(self.context.filters, row\_data).build().
        - Evaluate expanded\_rows.extend(detail\_rows).
    - Set segment.rows from expanded\_rows.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L7057) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L821)

<a id="op-3f8c0997a0e930"></a>
### Formatting Engine.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formatting_engine_initialize`

**Inputs** self.

**Local steps**

- Evaluate self.initialize\_rules().

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize rules](operations-041.md#op-095da94c5d6f5a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0048.json#L7287) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L861)

<a id="op-095da94c5d6f5a"></a>
### Formatting Engine.initialize rules

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formatting_engine_initialize_rules`

**Inputs** self.

**Local steps**

- Set self.rules from list(FormattingRule(condition = deferred anonymous expression, format\_properties = mapping(“bold” → true)), FormattingRule(condition = deferred anonymous expression, format\_properties = mapping(“italic” →  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L862)

<a id="op-a89e2730b84800"></a>
### Formatting Engine.get formatting

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formatting_engine_get_formatting`

**Inputs** self, row\_data.

**Declared result** dict at tuple(str, Any).

**Explicit results** formatting.

**Local steps**

- Set formatting from mapping().
- For each rule in self.rules.
  - If rule.applies\_to(row\_data).
    - Set properties from rule.get\_properties(row\_data).
    - Evaluate formatting.update(properties).
- Return formatting.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L882) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L860)

<a id="op-ce2e571fc81f75"></a>
### Segment Organizer.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_initialize`

**Inputs** self, processed\_rows.

**Local steps**

- Set self.sections from self.\_organize\_into\_sections(processed\_rows).
- Set max\_segments from self.max\_segments.
- For each section in self.sections.
  - If len(section.segments) ≥ max\_segments.
    - Continue with the next iteration or loop test.
  - Set empty\_segments from list of SegmentData(index = i) for i drawn from range(len(section.segments), max\_segments).
    - Draw i from range(len(section.segments), max\_segments).
  - Evaluate section.segments.extend(empty\_segments).

If control reaches the end, it returns no value.

**Methods declared on this owner** [organize into sections](operations-041.md#op-b62974662298b5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L1059) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L913)

<a id="op-b62974662298b5"></a>
### Segment Organizer.organize into sections

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_organize_into_sections`

**Inputs** self, rows.

**Declared result** list at SectionData.

**Explicit results** sections.

**Local steps**

- Set sections from list().
- Set current\_section\_rows from list().
- Set section\_index from 0.
- Set section\_label from empty text.
- For each row\_data in rows.
  - If not self.\_should\_show\_row(row\_data).
    - Continue with the next iteration or loop test.
  - If row\_data.row.data\_source equals “Section Break”.
    - If current\_section\_rows.
      - Set section\_segments from self.\_organize\_into\_segments(current\_section\_rows, section\_label).
      - Evaluate sections.append(SectionData(segments = section\_segments, label = section\_label, index = section\_index)).
      - Update section\_index using + 1.
      - Set current\_section\_rows from list().
    - Set section\_label from (getattr(row\_data.row, “display\_name”, empty text) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(row\_data.row, “display\_name”, empty text) → empty text.
  - Otherwise.
    - Evaluate current\_section\_rows.append(row\_data).
- If (current\_section\_rows or not sections).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in current\_section\_rows → not sections.
  - Set section\_segments from self.\_organize\_into\_segments(current\_section\_rows, section\_label).
  - Evaluate sections.append(SectionData(segments = section\_segments, label = section\_label, index = section\_index)).
- Return sections.

**Methods declared on this owner** [should show row](operations-041.md#op-d9002520c3219e), [organize into segments](operations-041.md#op-32f9b2d428405d).

**Values supplied outside this operation** selected callable from getattr(row\_data.row, “display\_name”, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L1331) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L968) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L917)

<a id="op-32f9b2d428405d"></a>
### Segment Organizer.organize into segments

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_organize_into_segments`

**Inputs** self, rows, section\_label.

**Declared result** list at SegmentData.

**State and service calls** call insert on current\_rows.

**Explicit results** segments.

**Local steps**

- Set segments from list().
- Set current\_rows from list().
- Set segment\_index from 0.
- Set segment\_label from empty text.
- Set section\_header from no value.
- If section\_label.
  - Set section\_header from RowData(row = Platform.\_dict(mapping(“data\_source” → “Blank Line”, “display\_name” → section\_label, “bold\_text” → true))).
- For each row\_data in rows.
  - If row\_data.row.data\_source equals “Column Break”.
    - If (section\_header and current\_rows).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in section\_header → current\_rows.
      - Evaluate current\_rows.insert(0, section\_header).
      - Set section\_header from RowData(row = Platform.\_dict(mapping(“data\_source” → “Blank Line”))).
    - If current\_rows.
      - Evaluate segments.append(SegmentData(rows = current\_rows, label = segment\_label, index = segment\_index)).
      - Update segment\_index using + 1.
      - Set current\_rows from list().
    - Set segment\_label from (getattr(row\_data.row, “display\_name”, empty text) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(row\_data.row, “display\_name”, empty text) → empty text.
  - Otherwise.
    - Evaluate current\_rows.append(row\_data).
- If (section\_header and current\_rows).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section\_header → current\_rows.
  - Evaluate current\_rows.insert(0, section\_header).
- If (current\_rows or not segments).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in current\_rows → not segments.
  - Evaluate segments.append(SegmentData(rows = current\_rows, label = segment\_label, index = segment\_index)).
- Return segments.

**Values supplied outside this operation** selected callable from getattr(row\_data.row, “display\_name”, empty text).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L1854) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L969) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L918)

<a id="op-f6e4cf57347029"></a>
### Segment Organizer.is single segment

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_is_single_segment`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** self.max\_segments equals 1.

**Local steps**

- Return self.max\_segments equals 1.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L2555) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L914)

<a id="op-33531ee4a98be9"></a>
### Segment Organizer.max rows

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_maximum_rows`

**Inputs** self, section.

**Declared result** int.

**Explicit results** max(generator of len(seg.rows) for seg drawn from section.segments) when section.segments, otherwise 0.

**Local steps**

- Return max(generator of len(seg.rows) for seg drawn from section.segments) when section.segments, otherwise 0.
  - Value choice on section.segments — true gives max(generator of len(seg.rows) for seg drawn from section.segments), false gives 0.
  - Draw seg from section.segments.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L2615) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L915)

<a id="op-919e785a3c8034"></a>
### Segment Organizer.max segments

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_maximum_segments`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** max(generator of len(s.segments) for s drawn from self.sections).

**Local steps**

- Return max(generator of len(s.segments) for s drawn from self.sections).
  - Draw s from self.sections.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L2732) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L916)

<a id="op-124369f0808238"></a>
### Segment Organizer.section with max segments

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_section_with_maximum_segments`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** SectionData.

**Explicit results** max(self.sections, key = deferred anonymous expression).

**Local steps**

- Return max(self.sections, key = deferred anonymous expression).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L2827) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L970) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L919)

<a id="op-d9002520c3219e"></a>
### Segment Organizer.should show row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_organizer_should_show_row`

**Inputs** self, row\_data.

**Declared result** bool.

**Explicit results** true · false · len(significant\_values) &gt; 0.

**Local steps**

- Set row from row\_data.row.
- If row.data\_source equals “Blank Line”.
  - Return true.
- If getattr(row, “hidden\_calculation”, false).
  - Return false.
- If getattr(row, “hide\_when\_empty”, false).
  - Set significant\_values from list of val for val drawn from row\_data.values where (isinstance(val, (int bitwise or float)) and abs(flt(val)) &gt; 0.01).
    - Draw val from row\_data.values, keep a combination only if ((isinstance(val, (int bitwise or float)) and abs(flt(val)) &gt; 0.01)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(val, (int bitwise or float)) → abs(flt(val)) &gt; 0.01.
  - Return len(significant\_values) &gt; 0.
- Return true.

**Values supplied outside this operation** selected callable from getattr(row, “hidden\_calculation”, false), getattr(row, “hide\_when\_empty”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L2926) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L971) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L920)

<a id="op-87e8ad92eb3583"></a>
### Row Formatter Base.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_initialize`

**Inputs** self, context, formatting\_engine.

**Local steps**

- Set self.context from context.
- Set self.period\_list from context.period\_list.
- Set self.formatting\_engine from formatting\_engine.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L3245) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L901)

<a id="op-866bdd420a7fda"></a>
### Row Formatter Base.format row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_format_row`

**Inputs** self, segments, row\_index.

**Wrappers, in declaration order** abstractmethod.

**Declared result** dict at tuple(str, Any).

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L3354) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L895)

<a id="op-b45510acae0f0d"></a>
### Row Formatter Base.get columns

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_get_columns`

**Inputs** self, segments, base\_columns.

**Wrappers, in declaration order** abstractmethod.

**Declared result** list at dict.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L3443) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L896)

<a id="op-9e63f9c3be859c"></a>
### Row Formatter Base.get values

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_get_values`

**Inputs** self, row\_data.

**Declared result** dict at tuple(str, Any).

**Explicit results** values.

**Local steps**

- Bind local operation \_get\_row\_data for subsequent calls.
- Bind local operation \_get\_filter\_value for subsequent calls.
- Set child\_accounts from list().
- If row\_data.account\_details.
  - Set child\_accounts from list(row\_data.account\_details.keys()).
- Set display\_name from \_get\_row\_data(“display\_name”, empty text).
- Set values from mapping(“account” → (\_get\_row\_data(“account”, empty text) or display\_name), “account\_name” → display\_name, “acc\_name” → \_get\_row\_data(“account\_name”, empty text), “acc\_number” → \_get\_row\_data(“account\_numb ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_get\_row\_data(“account”, empty text) → display\_name.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.context.currency → empty text.
- For each tuple(i, period) in enumerate(self.period\_list).
  - Set period\_value from self.\_get\_period\_value(row\_data, i).
  - Set values at period at “key” from period\_value.
  - If self.context.filters.get(“accumulated\_values”) equals 0.
    - Update values at “total” using + flt(period\_value).
- If (self.context.filters.get(“accumulated\_values”) equals 0 and row\_data.row.fieldtype equals “Percent”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.context.filters.get(“accumulated\_values”) equals 0 → row\_data.row.fieldtype equals “Percent”.
  - Set values at “total” from (values at “total” ÷ len(self.period\_list)).
- Return values.

**Methods declared on this owner** [get period value](operations-042.md#op-42e4e338f0fa68).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L3537) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L898)

<a id="op-d75d2165b4765c"></a>
### Row Formatter Base.get values.get row data

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_get_values_get_row_data`

**Inputs** key, default = empty text.

**Declared result** Any.

**Explicit results** (getattr(row\_data.row, key, default) or default).

**Local steps**

- Return (getattr(row\_data.row, key, default) or default).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(row\_data.row, key, default) → default.

**Values supplied outside this operation** selected callable from getattr(row\_data.row, key, default).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L4514) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L900)
