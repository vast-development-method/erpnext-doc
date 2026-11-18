# Supporting services · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Youtube interactions

<a id="op-4b9315d5a1c7f8"></a>
### Get chart summary data

`operation_enterprise_utilities_report_youtube_interactions_business_behavior_get_chart_summary_data`

**Inputs** data.

**Explicit results** tuple(chart\_data, summary).

**Local steps**

- Set tuple(labels, likes, views) from tuple(list(), list(), list()).
- Set total\_views from 0.
- For each row in data.
  - Evaluate labels.append(row.get(“title”)).
  - Evaluate likes.append(row.get(“like\_count”)).
  - Evaluate views.append(row.get(“view\_count”)).
  - Update total\_views using + flt(row.get(“view\_count”)).
- Set chart\_data from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Likes”, “values” → likes), mapping(“name” → “Views”, “values” → views))), “type” → “bar”, “barOptions” → mapping(“stacked” → 1)).
- Set summary from list(mapping(“value” → total\_views, “indicator” → “Blue”, “label” → translated “Total Views”, “datatype” → “Float”)).
- Return tuple(chart\_data, summary).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0990.json#L6512) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L93)
