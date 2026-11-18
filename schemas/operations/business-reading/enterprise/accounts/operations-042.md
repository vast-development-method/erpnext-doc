# Accounting and settlement · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-6e937201c65f22"></a>
### Row Formatter Base.get values.get filter value

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_get_values_get_filter_value`

**Inputs** key, default = empty text.

**Declared result** Any.

**Explicit results** (getattr(self.context.filters, key, default) or default).

**Local steps**

- Return (getattr(self.context.filters, key, default) or default).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self.context.filters, key, default) → default.

**Values supplied outside this operation** selected callable from getattr(self.context.filters, key, default).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L4609) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L899)

<a id="op-42e4e338f0fa68"></a>
### Row Formatter Base.get period value

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_row_formatter_base_get_period_value`

**Inputs** self, row\_data, period\_index.

**Declared result** Any.

**Explicit results** row\_data.values at period\_index · empty text.

**Local steps**

- If period\_index &lt; len(row\_data.values).
  - Return row\_data.values at period\_index.
- Return empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L4708) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L897)

<a id="op-473174f3b5ca95"></a>
### Single Segment Formatter.format row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_single_segment_formatter_format_row`

**Inputs** self, segments, row\_index.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping() · formatted.

**Local steps**

- If (not segments or row\_index ≥ len(segments at 0.rows)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not segments → row\_index ≥ len(segments at 0.rows).
  - Return mapping().
- Set row\_data from segments at 0.rows at row\_index.
- Set formatted from self.\_get\_values(row\_data).
- Set formatting from self.formatting\_engine.get\_formatting(row\_data).
- Evaluate formatted.update(formatting).
- Return formatted.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L4828) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L921)

<a id="op-725836ea45f7a2"></a>
### Single Segment Formatter.get columns

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_single_segment_formatter_get_columns`

**Inputs** self, segments, base\_columns.

**Declared result** list at dict.

**Explicit results** base\_columns.

**Local steps**

- For each col in base\_columns.
  - If col at “fieldname” equals “account”.
    - Set col at “align” from “left”.
- Return base\_columns.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L5099) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L922)

<a id="op-7ca894a7fbb3f6"></a>
### Multi Segment Formatter.format row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_multi_segment_formatter_format_row`

**Inputs** self, segments, row\_index.

**Declared result** dict at tuple(str, Any).

**Explicit results** formatted.

**Local steps**

- Set formatted from mapping(“segment\_values” → mapping()).
- For each segment in segments.
  - If row\_index &lt; len(segment.rows).
    - Set row\_data from segment.rows at row\_index.
    - Evaluate self.\_add\_segment\_data(formatted, row\_data, segment).
  - Otherwise.
    - Evaluate self.\_add\_empty\_segment(formatted, segment).
- Return formatted.

**Methods declared on this owner** [add segment data](operations-042.md#op-2da762c077286b), [add empty segment](operations-042.md#op-5468b879d741b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L5271) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L890)

<a id="op-f1dc8734eda6fe"></a>
### Multi Segment Formatter.get columns

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_multi_segment_formatter_get_columns`

**Inputs** self, segments, base\_columns.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- For each segment in segments.
  - For each col in base\_columns.
    - Set new\_col from col.copy().
    - Set new\_col at “fieldname” from formatted text {segment.id}\_{col at “fieldname”}.
    - If col at “fieldname” equals “account”.
      - Set new\_col at “label” from (segment.label or formatted text Account (Segment {(segment.index + 1)})).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in segment.label → formatted text Account (Segment {(segment.index + 1)}).
      - Set new\_col at “align” from “left”.
    - If (segment.label and col at “fieldname” belongs to list of p at “key” for p drawn from self.period\_list).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in segment.label → col at “fieldname” belongs to list of p at “key” for p drawn from self.period\_list.
      - Draw p from self.period\_list.
      - Set new\_col at “label” from formatted text {segment.label} - {col at “label”}.
    - Evaluate columns.append(new\_col).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L5526) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L891)

<a id="op-2da762c077286b"></a>
### Multi Segment Formatter.add segment data

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_multi_segment_formatter_add_segment_data`

**Inputs** self, formatted, row\_data, segment.

**Local steps**

- Set segment\_values from self.\_get\_values(row\_data).
- For each tuple(key, value) in segment\_values.items().
  - Set formatted at formatted text {segment.id}\_{key} from value.
- Set formatting from self.formatting\_engine.get\_formatting(row\_data).
- Evaluate segment\_values.update(formatting).
- Set formatted at “segment\_values” at segment.id from segment\_values.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L6063) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L889)

<a id="op-5468b879d741b8"></a>
### Multi Segment Formatter.add empty segment

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_multi_segment_formatter_add_empty_segment`

**Inputs** self, formatted, segment.

**Local steps**

- Set formatted at formatted text account\_{segment.id} from empty text.
- For each period in self.period\_list.
  - Set formatted at formatted text {segment.id}\_{period at “key”} from empty text.
- Set formatted at “segment\_values” at segment.id from mapping(“is\_blank\_line” → true).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L6332) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L888)

<a id="op-e1ccddad41f0b7"></a>
### Detail Row Builder.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_detail_row_builder_initialize`

**Inputs** self, filters, parent\_row\_data.

**Local steps**

- Set self.filters from filters.
- Set self.parent\_row\_data from parent\_row\_data.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L6551) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L832)

<a id="op-bf25cfdb0d4232"></a>
### Detail Row Builder.build

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_detail_row_builder_build`

**Inputs** self.

**Declared result** list at RowData.

**Explicit results** list() · detail\_rows.

**Local steps**

- If not self.parent\_row\_data.account\_details.
  - Return list().
- Set detail\_rows from list().
- Set parent\_row from self.parent\_row\_data.row.
- For each account\_data in self.parent\_row\_data.account\_details.values().
  - Set detail\_row from self.\_create\_detail\_row\_object(account\_data, parent\_row).
  - Set balance\_type from getattr(parent\_row, “balance\_type”, “Closing Balance”).
  - Set values from account\_data.get\_values\_by\_type(balance\_type).
  - Set detail\_row\_data from RowData(row = detail\_row, values = values, is\_detail\_row = true, parent\_reference = parent\_row.reference\_code).
  - Evaluate detail\_rows.append(detail\_row\_data).
- Return detail\_rows.

**Methods declared on this owner** [create detail row object](operations-042.md#op-eacda48431dd71).

**Values supplied outside this operation** selected callable from getattr(parent\_row, “balance\_type”, “Closing Balance”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L6639) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L830)

<a id="op-eacda48431dd71"></a>
### Detail Row Builder.create detail row object

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_detail_row_builder_create_detail_row_object`

**Inputs** self, account\_data, parent\_row.

**Explicit results** type(“DetailRow”, tuple(), mapping(“account” → account\_data.account, “display\_name” → display\_name, “account\_name” → acc\_name, “account\_number” → acc\_number, …))().

**Local steps**

- Set acc\_name from (account\_data.account\_name or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_data.account\_name → empty text.
- Set acc\_number from (account\_data.account\_number or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_data.account\_number → empty text.
- Set display\_name from formatted text {translated acc\_number} - {translated acc\_name} when acc\_number, otherwise translated acc\_name.
  - Value choice on acc\_number — true gives formatted text {translated acc\_number} - {translated acc\_name}, false gives translated acc\_name.
- Return type(“DetailRow”, tuple(), mapping(“account” → account\_data.account, “display\_name” → display\_name, “account\_name” → acc\_name, “account\_number” → acc\_number, …))().

**Values supplied outside this operation** selected callable from getattr(parent\_row, “indentation\_level”, 0), getattr(parent\_row, “fieldtype”, no value) and 3 further calls.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L6973) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L831)

<a id="op-a7c8f9fcc6e09b"></a>
### Chart Data Generator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_chart_data_generator_initialize`

**Inputs** self, context.

**Local steps**

- Set self.context from context.
- Set self.processed\_rows from context.processed\_rows.
- Set self.period\_list from context.period\_list.
- Set self.filters from context.filters.
- Set self.currency from context.currency.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0049.json#L7534) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L815)

<a id="op-802d8e62bd3387"></a>
### Chart Data Generator.generate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_chart_data_generator_generate`

**Inputs** self.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping().

**Local steps**

- Set chart\_rows from list of row for row drawn from self.processed\_rows where (getattr(row.row, “include\_in\_charts”, false) and row.row.data\_source does not belong to list(“Blank Line”, “Column Break”, “Section Break”)).
  - Draw row from self.processed\_rows, keep a combination only if ((getattr(row.row, “include\_in\_charts”, false) and row.row.data\_source does not belong to list(“Blank Line”, “Column Break”, “Section Break”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(row.row, “include\_in\_charts”, false) → row.row.data\_source does not belong to list(“Blank Line”, “Column Break”, “Section Break”).
- If not chart\_rows.
  - Return mapping().
- Set labels from list of p.get(“label”) for p drawn from self.period\_list.
  - Draw p from self.period\_list.
- Set datasets from list().
- For each row\_data in chart\_rows.
  - Set display\_name from getattr(row\_data.row, “display\_name”, empty text).
  - Set values from list().
  - For each tuple(i, \_period) in enumerate(self.period\_list).
    - If i &lt; len(row\_data.values).
      - Set value from row\_data.values at i.
      - Evaluate values.append(flt(value, 2)).
    - Otherwise.
      - Evaluate values.append(0.0).
  - If any(generator of v differs from 0 for v drawn from values).
    - Draw v from values.
    - Evaluate datasets.append(mapping(“name” → display\_name, “values” → values)).
- If not datasets.
  - Return mapping().
- If (not self.filters.get(“accumulated\_values”) or len(labels) ≤ 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.filters.get(“accumulated\_values”) → len(labels) ≤ 1.
  - Set chart\_type from “bar”.
- Otherwise.
  - Set chart\_type from “line”.
- Set self.context.raw\_data at “chart” from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → chart\_type, “fieldtype” → “Currency”, “options” → “currency”, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(row.row, “include\_in\_charts”, false), getattr(row\_data.row, “display\_name”, empty text).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L814)

<a id="op-a44683c7f0f1c6"></a>
### Growth View Transformer.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_growth_view_transformer_initialize`

**Inputs** self, context.

**Local steps**

- Set self.context from context.
- Set self.formatted\_rows from context.raw\_data.get(“formatted\_data”, list()).
- Set self.period\_list from context.period\_list.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L858) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L884)

<a id="op-7582a6f27a0b6c"></a>
### Growth View Transformer.transform

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_growth_view_transformer_transform`

**Inputs** self.

**Local steps**

- For each row\_data in self.formatted\_rows.
  - If row\_data.get(“is\_blank\_line”).
    - Continue with the next iteration or loop test.
  - If row\_data.get(“segment\_values”).
    - Evaluate self.\_transform\_segmented\_row(row\_data).
  - Otherwise.
    - Evaluate self.\_transform\_single\_row(row\_data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [transform segmented row](operations-042.md#op-2987b22e523ada), [transform single row](operations-042.md#op-258f01a9e80396).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L980) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L885)

<a id="op-7ccdb9d669f564"></a>
### Growth View Transformer.compute growth values

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_growth_view_transformer_compute_growth_values`

**Inputs** self, source.

**Declared result** dict.

**Explicit results** transformed.

**Local steps**

- Set transformed from mapping().
- For each tuple(i, period) in enumerate(self.period\_list).
  - Set current\_period from period at “key”.
  - Set current\_value from source.get(current\_period).
  - If current\_value belongs to tuple(no value, empty text).
    - Continue with the next iteration or loop test.
  - If i equals 0.
    - Set transformed at current\_period from current\_value.
  - Otherwise.
    - Set previous\_period from self.period\_list at (i − 1) at “key”.
    - Set previous\_value from (source.get(previous\_period) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.get(previous\_period) → 0.
    - Set transformed at current\_period from self.\_calculate\_growth(previous\_value, current\_value).
- Return transformed.

**Methods declared on this owner** [calculate growth](operations-042.md#op-d21ac48b8c22c7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L1136) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L883)

<a id="op-258f01a9e80396"></a>
### Growth View Transformer.transform single row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_growth_view_transformer_transform_single_row`

**Inputs** self, row\_data.

**Local steps**

- Evaluate row\_data.update(self.\_compute\_growth\_values(row\_data)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [compute growth values](operations-042.md#op-7ccdb9d669f564).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L1496) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L887)

<a id="op-2987b22e523ada"></a>
### Growth View Transformer.transform segmented row

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_growth_view_transformer_transform_segmented_row`

**Inputs** self, row\_data.

**Local steps**

- For each tuple(seg\_id, seg\_data) in row\_data.get(“segment\_values”, mapping()).items().
  - If seg\_data.get(“is\_blank\_line”).
    - Continue with the next iteration or loop test.
  - Set transformed from self.\_compute\_growth\_values(seg\_data).
  - Evaluate seg\_data.update(transformed).
  - For each tuple(period\_key, value) in transformed.items().
    - Set row\_data at formatted text {seg\_id}\_{period\_key} from value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [compute growth values](operations-042.md#op-7ccdb9d669f564).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L1581) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L937) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L886)

<a id="op-d21ac48b8c22c7"></a>
### Growth View Transformer.calculate growth

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_growth_view_transformer_calculate_growth`

**Inputs** self, previous\_value, current\_value.

**Declared result** (float bitwise or no value).

**Explicit results** no value · 100.0 · 0.0 · flt((((current\_value − previous\_value) ÷ abs(previous\_value)) × 100), 2).

**Local steps**

- If current\_value belongs to tuple(no value, empty text).
  - Return no value.
- If (previous\_value equals 0 and current\_value &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_value equals 0 → current\_value &gt; 0.
  - Return 100.0.
- Otherwise.
  - If (previous\_value equals 0 and current\_value ≤ 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_value equals 0 → current\_value ≤ 0.
    - Return 0.0.
  - Otherwise.
    - Return flt((((current\_value − previous\_value) ÷ abs(previous\_value)) × 100), 2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L1845) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L882)

<a id="op-8759206754af56"></a>
### Get xlsx styles

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_get_spreadsheet_workbook_styles`

**Inputs** metadata.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · builder.result.

**Local steps**

- If not metadata.filters.get(“report\_template”).
  - Return no value.
- Set builder from XLSXStyleBuilder(metadata, default\_styling = false).
- Evaluate builder.apply\_default\_styles(currency\_formatting = false).
- Set currency from get\_company\_currency(metadata.filters.get(“company”)).
- Set styles from mapping(“bold” → builder.register\_style(mapping(“bold” → true)), “italic” → builder.register\_style(mapping(“italic” → true)), “warning” → builder.register\_style(mapping(“font\_color” → “#dc3545”))).
- Set fieldtype\_formats from mapping(“Int” → builder.register\_style(mapping(“num\_format” → “General”)), “Float” → builder.register\_style(mapping(“num\_format” → builder.get\_number\_format(“Float”))), “Percent” → builder.register\_style(m ….
- Set style\_cell from builder.style\_cell.
- Bind local operation get\_color\_style for subsequent calls.
- Bind local operation get\_prefix\_style for subsequent calls.
- Bind local operation get\_indent\_style for subsequent calls.
- For each tuple(col\_idx, col) in metadata.column\_map.items().
  - If col.get(“fieldtype”) differs from “Currency”.
    - Continue with the next iteration or loop test.
  - Evaluate builder.style\_column(col\_idx, fieldtype\_formats at “Currency”).
- For each tuple(row\_idx, row) in metadata.row\_map.items().
  - If (metadata.has\_total\_row and row\_idx equals builder.last\_row\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in metadata.has\_total\_row → row\_idx equals builder.last\_row\_index.
    - Continue with the next iteration or loop test.
  - Set is\_segmented from (row.get(“\_segment\_info”, mapping()).get(“total\_segments”, 1) or 1) &gt; 1.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“\_segment\_info”, mapping()).get(“total\_segments”, 1) → 1.
  - Set segment\_values from (row.get(“segment\_values”, mapping()) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“segment\_values”, mapping()) → mapping().
  - For each tuple(col\_idx, col) in metadata.column\_map.items().
    - Set fieldname from col.get(“fieldname”).
    - Set is\_account from fieldname equals “account”.
    - If (is\_segmented and fieldname.startswith(SEGMENT\_PREFIX)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_segmented → fieldname.startswith(SEGMENT\_PREFIX).
      - Set formatting from row.copy().
      - Set tuple(\_, seg\_idx, seg\_fieldname) from fieldname.split(“\_”, 2).
      - Set is\_account from seg\_fieldname equals “account”.
      - Evaluate formatting.update((segment\_values.get(formatted text {SEGMENT\_PREFIX}{seg\_idx}, mapping()) or mapping())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in segment\_values.get(formatted text {SEGMENT\_PREFIX}{seg\_idx}, mapping()) → mapping().
    - Otherwise.
      - Set formatting from row.
    - If (not is\_account and formatting.get(“is\_blank\_line”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_account → formatting.get(“is\_blank\_line”).
      - Continue with the next iteration or loop test.
    - Set col\_fieldtype from col.get(“fieldtype”).
    - Set cell\_fieldtype from (formatting.get(“fieldtype”) or col\_fieldtype).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in formatting.get(“fieldtype”) → col\_fieldtype.
    - Set cell\_value from row.get(fieldname).
    - If cell\_value belongs to tuple(no value, empty text).
      - Continue with the next iteration or loop test.
    - If is\_account.
      - If (formatting.get(“is\_detail”) or prefix bound to formatting.get(“prefix”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in formatting.get(“is\_detail”) → prefix bound to formatting.get(“prefix”).
        - Evaluate style\_cell(row\_idx, col\_idx, get\_prefix\_style(prefix)).
      - If (is\_segmented and indent bound to formatting.get(“indent”) and indent &gt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_segmented → indent bound to formatting.get(“indent”) → indent &gt; 0.
        - Evaluate style\_cell(row\_idx, col\_idx, get\_indent\_style(indent)).
    - Otherwise.
      - If (col\_fieldtype differs from cell\_fieldtype and cell\_fieldtype belongs to fieldtype\_formats).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in col\_fieldtype differs from cell\_fieldtype → cell\_fieldtype belongs to fieldtype\_formats.
        - Evaluate style\_cell(row\_idx, col\_idx, fieldtype\_formats at cell\_fieldtype).
    - For each style\_key in tuple(“bold”, “italic”).
      - If formatting.get(style\_key).
        - Evaluate style\_cell(row\_idx, col\_idx, styles at style\_key).
    - If (formatting.get(“warn\_if\_negative”) and cell\_fieldtype belongs to Platform.model.numeric\_fieldtypes and flt(cell\_value) &lt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in formatting.get(“warn\_if\_negative”) → cell\_fieldtype belongs to Platform.model.numeric\_fieldtypes → flt(cell\_value) &lt; 0.
      - Evaluate style\_cell(row\_idx, col\_idx, styles at “warning”).
    - Otherwise.
      - If color bound to formatting.get(“color”).
        - Evaluate style\_cell(row\_idx, col\_idx, get\_color\_style(color)).
- Return builder.result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L2109) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L878)

<a id="op-f47065b5ef27de"></a>
### Get xlsx styles.get color style

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_get_spreadsheet_workbook_styles_get_color_style`

**Inputs** color.

**Wrappers, in declaration order** cache.

**Declared result** int.

**Explicit results** builder.register\_style(mapping(“font\_color” → color)).

**Local steps**

- Return builder.register\_style(mapping(“font\_color” → color)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L4356) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L879)

<a id="op-eb57354324c31b"></a>
### Get xlsx styles.get prefix style

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_get_spreadsheet_workbook_styles_get_prefix_style`

**Inputs** prefix.

**Wrappers, in declaration order** cache.

**Declared result** int.

**Explicit results** builder.register\_style(mapping(“num\_format” → prefix)).

**Local steps**

- Set prefix from formatted text {(prefix or DEFAULT\_BULLET\_PREFIX)}@.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in prefix → DEFAULT\_BULLET\_PREFIX.
- Return builder.register\_style(mapping(“num\_format” → prefix)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L4434) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L932) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L881)

<a id="op-322d4e13dce822"></a>
### Get xlsx styles.get indent style

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_engine_business_behavior_get_spreadsheet_workbook_styles_get_indent_style`

**Inputs** indent.

**Wrappers, in declaration order** cache.

**Declared result** int.

**Explicit results** builder.register\_style(mapping(“align” → “left”, “indent” → indent)).

**Local steps**

- Return builder.register\_style(mapping(“align” → “left”, “indent” → indent)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L4551) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L880)

<a id="op-59d6330458eb1d"></a>
### Financial Report Template.before validate

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_hidden\_fields().
- For each row in self.rows.
  - If row.reference\_code.
    - Set row.reference\_code from row.reference\_code.strip().
  - If row.calculation\_formula.
    - Set row.calculation\_formula from row.calculation\_formula.strip().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear hidden fields](operations-043.md#op-2e89f530f37526).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L846) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L795)
