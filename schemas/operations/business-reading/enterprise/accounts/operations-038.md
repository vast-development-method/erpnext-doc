# Accounting and settlement · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Financial ratios

<a id="op-32cf7c22d04555"></a>
### Calculate ratio

`operation_enterprise_accounts_report_financial_ratios_business_behavior_calculate_ratio`

**Inputs** value, denominator, precision.

**Explicit results** flt((flt(value) ÷ denominator), precision) · 0.

**Local steps**

- If flt(denominator).
  - Return flt((flt(value) ÷ denominator), precision).
- Return 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0246.json#L1294) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L898)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-cbfdd73e2441e1"></a>
### Period Value.get value

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_period_value_get_value`

**Inputs** self, balance\_type.

**Declared result** float.

**Explicit results** self.opening · self.closing · self.movement · 0.0.

**Local steps**

- If balance\_type equals “Opening Balance”.
  - Return self.opening.
- Otherwise.
  - If balance\_type equals “Closing Balance”.
    - Return self.closing.
  - Otherwise.
    - If balance\_type equals “Period Movement (Debits - Credits)”.
      - Return self.movement.
- Return 0.0.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0045.json#L7692) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L893)

<a id="op-c2c8c8a1052fab"></a>
### Period Value.copy

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_period_value_copy`

**Inputs** self.

**Explicit results** PeriodValue(period\_key = self.period\_key, opening = self.opening, closing = self.closing, movement = self.movement).

**Local steps**

- Return PeriodValue(period\_key = self.period\_key, opening = self.opening, closing = self.closing, movement = self.movement).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0045.json#L7844) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L892)

<a id="op-34e7b74056b576"></a>
### Account Data.add period

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_add_period`

**Inputs** self, period\_value.

**Declared result** no value.

**Local steps**

- Set self.period\_values at period\_value.period\_key from period\_value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L806)

<a id="op-0979e36fb2cbea"></a>
### Account Data.get period

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_get_period`

**Inputs** self, period\_key.

**Declared result** (PeriodValue bitwise or no value).

**Explicit results** self.period\_values.get(period\_key).

**Local steps**

- Return self.period\_values.get(period\_key).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L809)

<a id="op-efecb097f22694"></a>
### Account Data.get values by type

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_get_values_by_type`

**Inputs** self, balance\_type.

**Declared result** list at float.

**Explicit results** list of pv.get\_value(balance\_type) for pv drawn from self.period\_values.values().

**Local steps**

- Return list of pv.get\_value(balance\_type) for pv drawn from self.period\_values.values().
  - Draw pv from self.period\_values.values().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L810)

<a id="op-78d7289f53f571"></a>
### Account Data.get ordered values

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_get_ordered_values`

**Inputs** self, period\_keys, balance\_type.

**Declared result** list at float.

**Explicit results** list of self.period\_values at key.get\_value(balance\_type) when key belongs to self.period\_values, otherwise 0.0 for key drawn from period\_keys.

**Local steps**

- Return list of self.period\_values at key.get\_value(balance\_type) when key belongs to self.period\_values, otherwise 0.0 for key drawn from period\_keys.
  - Draw key from period\_keys.
  - Value choice on key belongs to self.period\_values — true gives self.period\_values at key.get\_value(balance\_type), false gives 0.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L267) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L808)

<a id="op-0e763c28b7f20e"></a>
### Account Data.has periods

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_has_periods`

**Inputs** self.

**Declared result** bool.

**Explicit results** len(self.period\_values) &gt; 0.

**Local steps**

- Return len(self.period\_values) &gt; 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L423) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L811)

<a id="op-b6dff334a0621f"></a>
### Account Data.accumulate values

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_accumulate_values`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each period\_value in self.period\_values.values().
  - Update period\_value.movement using + period\_value.opening.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L491) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L805)

<a id="op-97ac4386b5bb5d"></a>
### Account Data.unaccumulate values

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_unaccumulate_values`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each period\_value in self.period\_values.values().
  - Update period\_value.closing using − period\_value.opening.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L572) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L813)

<a id="op-33c5b9fabebcc5"></a>
### Account Data.copy

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_copy`

**Inputs** self.

**Explicit results** copied.

**Local steps**

- Set copied from AccountData(account = self.account, account\_name = self.account\_name, account\_number = self.account\_number).
- Set copied.period\_values from mapping of k → v.copy() for tuple(k, v) drawn from self.period\_values.items().
  - Draw tuple(k, v) from self.period\_values.items().
- Return copied.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L653) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L807)

<a id="op-eb34596be31222"></a>
### Account Data.reverse values

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_account_data_reverse_values`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each period\_value in self.period\_values.values().
  - Set period\_value.opening from negative period\_value.opening when period\_value.opening, otherwise 0.0.
    - Value choice on period\_value.opening — true gives negative period\_value.opening, false gives 0.0.
  - Set period\_value.closing from negative period\_value.closing when period\_value.closing, otherwise 0.0.
    - Value choice on period\_value.closing — true gives negative period\_value.closing, false gives 0.0.
  - Set period\_value.movement from negative period\_value.movement when period\_value.movement, otherwise 0.0.
    - Value choice on period\_value.movement — true gives negative period\_value.movement, false gives 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L825) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L812)

<a id="op-a4ba5919253001"></a>
### Segment Data.id

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_segment_data_identifier`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** formatted text {SEGMENT\_PREFIX}{self.index}.

**Local steps**

- Return formatted text {SEGMENT\_PREFIX}{self.index}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1006) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L912)

<a id="op-18e3785ba906f0"></a>
### Section Data.id

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_section_data_identifier`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** formatted text section\_{self.index}.

**Local steps**

- Return formatted text section\_{self.index}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1077) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L911)

<a id="op-c1780c85214d4b"></a>
### Report Context.get result

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_report_context_get_result`

**Inputs** self.

**Declared result** tuple at tuple(list at dict, list at dict).

**Explicit results** tuple(self.raw\_data.get(“columns”, list()), self.raw\_data.get(“formatted\_data”, list()), no value, self.raw\_data.get(“chart”, mapping())).

**Local steps**

- Return tuple(self.raw\_data.get(“columns”, list()), self.raw\_data.get(“formatted\_data”, list()), no value, self.raw\_data.get(“chart”, mapping())).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1141) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L894)

<a id="op-3db307e9f56ccc"></a>
### Formatting Rule.applies to

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formatting_rule_applies_to`

**Inputs** self, row\_data.

**Declared result** bool.

**Explicit results** self.condition(row\_data).

**Local steps**

- Return self.condition(row\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1312) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L863)

<a id="op-9a0812a875ab92"></a>
### Formatting Rule.get properties

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_formatting_rule_get_properties`

**Inputs** self, row\_data.

**Declared result** dict at tuple(str, Any).

**Explicit results** self.format\_properties(row\_data) · self.format\_properties.

**Local steps**

- If callable(self.format\_properties).
  - Return self.format\_properties(row\_data).
- Return self.format\_properties.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1380) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L864)

<a id="op-06b6d0dae864ce"></a>
### Financial Report Engine.execute

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_execute`

**Inputs** self, filters.

**Declared result** tuple at tuple(list at dict, list at dict).

**Explicit results** context.get\_result().

**Local steps**

- Evaluate self.\_validate\_filters(filters).
- Set context from self.\_initialize\_context(filters).
- Evaluate self.collect\_financial\_data(context).
- Evaluate self.process\_calculations(context).
- Evaluate self.format\_report\_data(context).
- Evaluate self.apply\_view\_transformation(context).
- Evaluate self.generate\_chart\_data(context).
- Return context.get\_result().

**Methods declared on this owner** [validate filters](operations-038.md#op-92fad0cb2a6430), [initialize context](operations-038.md#op-6105a9c060b43b), [collect financial data](operations-038.md#op-24477f070fdb74), [process calculations](operations-038.md#op-97e08efff33d42), [format report data](operations-038.md#op-974d1bc10abad8), [apply view transformation](operations-038.md#op-59fe254f6951ef), [generate chart data](operations-039.md#op-29b0b3b66583b7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1500) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L854)

<a id="op-92fad0cb2a6430"></a>
### Financial Report Engine.validate filters

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_validate_filters`

**Inputs** self, filters.

**Declared result** no value.

**State and service calls** msgprint.

**Explicit failure paths** validation helper.

**Local steps**

- Set filter\_labels from mapping(“report\_template” → translated “Report Template”, “filter\_based\_on” → translated “Filter Based On”, “period\_start\_date” → translated “Start Date”, “period\_end\_date” → translated “End Date”, …).
- Set required\_filters\_by\_basis from mapping(“Date Range” → tuple(“period\_start\_date”, “period\_end\_date”), “Fiscal Year” → tuple(“from\_fiscal\_year”, “to\_fiscal\_year”)).
- Set required\_filters from list(“report\_template”, “filter\_based\_on”).
- Evaluate required\_filters.extend(required\_filters\_by\_basis.get(filters.get(“filter\_based\_on”), tuple())).
- For each filter\_key in required\_filters.
  - If not filters.get(filter\_key).
    - Call the validation error handler Platform.throw(title = translated “Missing Required Filter”, msg = translated “Missing required filter: {0}”.format(Platform.bold(filter\_labels.get(filter\_key, filter\_key)))).
- If filters.get(“presentation\_currency”).
  - Evaluate Platform.msgprint(indicator = “orange”, title = translated “Not Supported”, msg = translated “Currency filters are currently unsupported in Custom Financial Report”).
- Set supported\_views from tuple(“Report”, “Growth”).
- If (view bound to filters.get(“selected\_view”) and view does not belong to supported\_views).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in view bound to filters.get(“selected\_view”) → view does not belong to supported\_views.
  - Evaluate Platform.msgprint(indicator = “orange”, title = translated “Not Supported”, msg = translated “{0} view is currently unsupported in Custom Financial Report”.format(view)).
- If filters.get(“group\_by\_dimension”).
  - Evaluate Platform.msgprint(indicator = “orange”, title = translated “Not Supported”, msg = translated “Dimension-based grouping is currently unsupported in Custom Financial Report”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L1795) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L859)

<a id="op-6105a9c060b43b"></a>
### Financial Report Engine.initialize context

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_initialize_context`

**Inputs** self, filters.

**Declared result** ReportContext.

**Record and data access** resolve a document from “Financial Report Template” via get\_doc.

**Explicit results** context.

**Explicit failure paths** validation helper — translated “Financial Report Template {0} not found”.format(template\_name) · validation helper — translated “Financial Report Template {0} is disabled”.format(template\_name).

**Local steps**

- Set template\_name from filters.get(“report\_template”).
- Set template from Platform.get\_doc(“Financial Report Template”, template\_name).
- If not template.
  - Call the validation error handler Platform.throw(translated “Financial Report Template {0} not found”.format(template\_name)).
- If template.disabled.
  - Call the validation error handler Platform.throw(translated “Financial Report Template {0} is disabled”.format(template\_name)).
- Set period\_list from get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters.period\_start\_date, filters.period\_end\_date, company = filters.company, …).
- Set show\_detailed from filters.get(“show\_account\_details”) equals “Account Breakdown”.
- Set context from ReportContext(template = template, filters = filters, period\_list = period\_list, show\_detailed = show\_detailed, …).
- Set context.raw\_data at “period\_keys” from list of p at “key” for p drawn from period\_list.
  - Draw p from period\_list.
- Return context.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L2733) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L857)

<a id="op-24477f070fdb74"></a>
### Financial Report Engine.collect financial data

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_collect_financial_data`

**Inputs** self, context.

**Declared result** ReportContext.

**Explicit results** context.

**Local steps**

- Set collector from DataCollector(context.filters, context.period\_list).
- For each row in context.template.rows.
  - If row.data\_source equals “Account Data”.
    - Evaluate collector.add\_account\_request(row).
- Set all\_data from collector.collect\_all\_data().
- Set context.account\_data from all\_data at “account\_data”.
- Evaluate context.raw\_data.update(all\_data).
- Return context.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L3267) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L853)

<a id="op-97e08efff33d42"></a>
### Financial Report Engine.process calculations

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_process_calculations`

**Inputs** self, context.

**Declared result** ReportContext.

**Explicit results** context.

**Local steps**

- Set processor from RowProcessor(context).
- Set context.processed\_rows from processor.process\_all\_rows().
- Return context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L3503) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L858)

<a id="op-974d1bc10abad8"></a>
### Financial Report Engine.format report data

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_format_report_data`

**Inputs** self, context.

**Declared result** ReportContext.

**Explicit results** context.

**Local steps**

- Set formatter from DataFormatter(context).
- Set tuple(formatted\_data, columns) from formatter.format\_for\_display().
- Set context.raw\_data at “formatted\_data” from formatted\_data.
- Set context.raw\_data at “columns” from columns.
- Return context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L3608) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L855)

<a id="op-59fe254f6951ef"></a>
### Financial Report Engine.apply view transformation

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_financial_report_engine_apply_view_transformation`

**Inputs** self, context.

**Declared result** ReportContext.

**Explicit results** context.

**Local steps**

- If context.filters.get(“selected\_view”) equals “Growth”.
  - Set transformer from GrowthViewTransformer(context).
  - Evaluate transformer.transform().
- Return context.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0046.json#L3771) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L852)
