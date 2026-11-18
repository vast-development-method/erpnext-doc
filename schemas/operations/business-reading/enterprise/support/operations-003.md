# Customer support · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Issue analytics

<a id="op-15f9418dc64a44"></a>
### Issue Analytics.get common filters

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_common_filters`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filters from mapping().
- Set filters at “opening\_date” from tuple(“between”, list(self.filters.from\_date, self.filters.to\_date)).
- If self.filters.get(“assigned\_to”).
  - Set filters at “\_assign” from tuple(“like”, ((“%"” + self.filters.get(“assigned\_to”)) + “"%”)).
- For each entry in list(“company”, “status”, “priority”, “customer”, …).
  - If self.filters.get(entry).
    - Set filters at entry from self.filters.get(entry).
- Return filters.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1280)

<a id="op-bb2548deaeb18d"></a>
### Issue Analytics.get rows

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_rows`

**Inputs** self.

**Local steps**

- Set self.data from list().
- Evaluate self.get\_periodic\_data().
- For each tuple(entity, period\_data) in self.issue\_periodic\_data.items().
  - If self.filters.based\_on equals “Customer”.
    - Set row from mapping(“customer” → entity).
  - Otherwise.
    - If self.filters.based\_on equals “Assigned To”.
      - Set row from mapping(“user” → entity, “user\_doctype” → no value when entity equals translated “Not Assigned”, otherwise “User”).
        - Value choice on entity equals translated “Not Assigned” — true gives no value, false gives “User”.
    - Otherwise.
      - If self.filters.based\_on equals “Issue Type”.
        - Set row from mapping(“issue\_type” → entity).
      - Otherwise.
        - If self.filters.based\_on equals “Issue Priority”.
          - Set row from mapping(“priority” → entity).
  - Set total from 0.
  - For each end\_date in self.periodic\_daterange.
    - Set period from self.get\_period(end\_date).
    - Set amount from flt(period\_data.get(period, 0.0)).
    - Set row at scrub(period) from amount.
    - Update total using + amount.
  - Set row at “total” from total.
  - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get periodic data](operations-003.md#op-cc2910eb59e513), [get period](operations-002.md#op-ff7dcf81f769e3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1286)

<a id="op-cc2910eb59e513"></a>
### Issue Analytics.get periodic data

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_periodic_data`

**Inputs** self.

**Local steps**

- Set self.issue\_periodic\_data from Platform.\_dict().
- For each d in self.entries.
  - Set period from self.get\_period\_of(d.get(“opening\_date”)).
  - If self.filters.based\_on equals “Assigned To”.
    - For each entry in (json.loads((d.\_assign or “&#91;&#93;”)) or list(translated “Not Assigned”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in json.loads((d.\_assign or “&#91;&#93;”)) → list(translated “Not Assigned”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.\_assign → “&#91;&#93;”.
      - Evaluate self.issue\_periodic\_data.setdefault(entry, Platform.\_dict()).setdefault(period, 0.0).
      - Update self.issue\_periodic\_data at entry at period using + 1.
  - Otherwise.
    - Set field from self.field\_map.get(self.filters.based\_on).
    - Set value from d.get(field).
    - If not value.
      - Set value from translated “Not Specified”.
    - Evaluate self.issue\_periodic\_data.setdefault(value, Platform.\_dict()).setdefault(period, 0.0).
    - Update self.issue\_periodic\_data at value at period using + 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period of](operations-003.md#op-a26105ce1812a8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1285)

<a id="op-a26105ce1812a8"></a>
### Issue Analytics.get period of

`operation_enterprise_binding_enterprise_support_report_issue_analytics_issue_analytics_issueanalytics_get_period_of`

**Inputs** self, date.

**Declared result** str.

**Explicit results** self.get\_period(self.periodic\_daterange at index).

**Local steps**

- Set index from bisect\_left(self.periodic\_daterange, getdate(date)).
- Return self.get\_period(self.periodic\_daterange at index).

**Methods declared on this owner** [get period](operations-002.md#op-ff7dcf81f769e3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L6) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1287)

<a id="op-a7bbf5c1e1b6b2"></a>
### Issue Analytics.get chart data

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_chart_data`

**Inputs** self.

**Local steps**

- Set length from len(self.columns).
- Set labels from list of d.get(“label”) for d drawn from self.columns at slice 1 to (length − 1).
  - Draw d from self.columns at slice 1 to (length − 1).
- Set self.chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list()), “type” → “line”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0973.json#L5583) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1278)

## Report · Issue summary

<a id="op-9bd6a5b64b5ffb"></a>
### Execute

`operation_enterprise_support_report_issue_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** IssueSummary(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return IssueSummary(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1297)

<a id="op-8be85ce2524693"></a>
### Issue Summary.initialize

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0974.json#L1820) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1307)

<a id="op-3d6671c6683717"></a>
### Issue Summary.run

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data, no value, self.chart, …).

**Local steps**

- Evaluate self.get\_columns().
- Evaluate self.get\_data().
- Evaluate self.get\_chart\_data().
- Evaluate self.get\_report\_summary().
- Return tuple(self.columns, self.data, no value, self.chart, …).

**Methods declared on this owner** [get columns](operations-003.md#op-9d54f5a41434b9), [get data](operations-003.md#op-8f805ce3dd8a4b), [get chart data](operations-003.md#op-783d4c3251e00b), [get report summary](operations-003.md#op-84da8818596a5b).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0974.json#L1904) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1308)

<a id="op-9d54f5a41434b9"></a>
### Issue Summary.get columns

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- If self.filters.based\_on equals “Customer”.
  - Evaluate self.columns.append(mapping(“label” → translated “Customer”, “options” → “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, …)).
- Otherwise.
  - If self.filters.based\_on equals “Assigned To”.
    - Evaluate self.columns.append(mapping(“label” → translated “User”, “fieldname” → “user”, “fieldtype” → “Link”, “options” → “User”, …)).
  - Otherwise.
    - If self.filters.based\_on equals “Issue Type”.
      - Evaluate self.columns.append(mapping(“label” → translated “Issue Type”, “fieldname” → “issue\_type”, “fieldtype” → “Link”, “options” → “Issue Type”, …)).
    - Otherwise.
      - If self.filters.based\_on equals “Issue Priority”.
        - Evaluate self.columns.append(mapping(“label” → translated “Issue Priority”, “fieldname” → “priority”, “fieldtype” → “Link”, “options” → “Issue Priority”, …)).
- Set self.statuses from list(“Open”, “Replied”, “On Hold”, “Resolved”, …).
- For each status in self.statuses.
  - Evaluate self.columns.append(mapping(“label” → translated status, “fieldname” → scrub(status), “fieldtype” → “Int”, “width” → 80)).
- Evaluate self.columns.append(mapping(“label” → translated “Total Issues”, “fieldname” → “total\_issues”, “fieldtype” → “Int”, “width” → 100)).
- Set self.sla\_status\_map from mapping(“SLA Failed” → “failed”, “SLA Fulfilled” → “fulfilled”, “First Response Due” → “first\_response\_due”, “Resolution Due” → “resolution\_due”).
- For each tuple(label, fieldname) in self.sla\_status\_map.items().
  - Evaluate self.columns.append(mapping(“label” → translated label, “fieldname” → fieldname, “fieldtype” → “Int”, “width” → 100)).
- Set self.metrics from list(“Avg First Response Time”, “Avg Response Time”, “Avg Hold Time”, “Avg Resolution Time”, …).
- For each metric in self.metrics.
  - Evaluate self.columns.append(mapping(“label” → translated metric, “fieldname” → scrub(metric), “fieldtype” → “Duration”, “width” → 170)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0974.json#L2058) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1299)

<a id="op-8f805ce3dd8a4b"></a>
### Issue Summary.get data

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_data`

**Inputs** self.

**Local steps**

- Evaluate self.get\_issues().
- Evaluate self.get\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get issues](operations-003.md#op-83be289774a291), [get rows](operations-003.md#op-71421af0a8e178).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0974.json#L3455) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1301)

<a id="op-83be289774a291"></a>
### Issue Summary.get issues

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_issues`

**Inputs** self.

**Record and data access** read “Issue” via get\_list.

**Local steps**

- Set filters from self.get\_common\_filters().
- Set self.field\_map from mapping(“Customer” → “customer”, “Issue Type” → “issue\_type”, “Issue Priority” → “priority”, “Assigned To” → “\_assign”).
- Set self.entries from Platform.get\_list(“Issue”, fields = list(self.field\_map.get(self.filters.based\_on), “name”, “opening\_date”, “status”, …), filters = filters).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get common filters](operations-003.md#op-b0c0e0dd0c98d0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1302)

<a id="op-b0c0e0dd0c98d0"></a>
### Issue Summary.get common filters

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_common_filters`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filters from mapping().
- Set filters at “opening\_date” from tuple(“between”, list(self.filters.from\_date, self.filters.to\_date)).
- If self.filters.get(“assigned\_to”).
  - Set assigned\_to from nested operand in the contract.filters.get(“assigned\_to”).replace(“%”, “\\%”).replace(“\_”, “\\\_”).
  - Set filters at “\_assign” from tuple(“like”, formatted text %"{assigned\_to}"%).
- For each entry in list(“company”, “status”, “priority”, “customer”, …).
  - If self.filters.get(entry).
    - Set filters at entry from self.filters.get(entry).
- Return filters.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1300)

<a id="op-71421af0a8e178"></a>
### Issue Summary.get rows

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_rows`

**Inputs** self.

**Local steps**

- Set self.data from list().
- Evaluate self.get\_summary\_data().
- For each tuple(entity, data) in self.issue\_summary\_data.items().
  - If self.filters.based\_on equals “Customer”.
    - Set row from mapping(“customer” → entity).
  - Otherwise.
    - If self.filters.based\_on equals “Assigned To”.
      - Set row from mapping(“user” → entity).
    - Otherwise.
      - If self.filters.based\_on equals “Issue Type”.
        - Set row from mapping(“issue\_type” → entity).
      - Otherwise.
        - If self.filters.based\_on equals “Issue Priority”.
          - Set row from mapping(“priority” → entity).
  - For each status in self.statuses.
    - Set count from flt(data.get(status, 0.0)).
    - Set row at scrub(status) from count.
  - Set row at “total\_issues” from data.get(“total\_issues”, 0.0).
  - For each sla\_status in self.sla\_status\_map.values().
    - Set value from flt(data.get(sla\_status), 0.0).
    - Set row at sla\_status from value.
  - For each metric in self.metrics.
    - Set value from flt(data.get(scrub(metric)), 0.0).
    - Set row at scrub(metric) from value.
  - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get summary data](operations-003.md#op-2739e466b8e473).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0974.json#L4194) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1305)

<a id="op-2739e466b8e473"></a>
### Issue Summary.get summary data

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_summary_data`

**Inputs** self.

**Local steps**

- Set self.issue\_summary\_data from Platform.\_dict().
- For each d in self.entries.
  - Set status from d.status.
  - Set agreement\_status from scrub(d.agreement\_status) when d.service\_level\_agreement, otherwise no value.
    - Value choice on d.service\_level\_agreement — true gives scrub(d.agreement\_status), false gives no value.
  - If self.filters.based\_on equals “Assigned To”.
    - If d.\_assign.
      - For each entry in json.loads(d.\_assign).
        - Evaluate self.issue\_summary\_data.setdefault(entry, Platform.\_dict()).setdefault(status, 0.0).
        - Evaluate self.issue\_summary\_data.setdefault(entry, Platform.\_dict()).setdefault(“total\_issues”, 0.0).
        - Update self.issue\_summary\_data at entry at status using + 1.
        - If agreement\_status.
          - Evaluate self.issue\_summary\_data at entry.setdefault(agreement\_status, 0.0).
          - Update self.issue\_summary\_data at entry at agreement\_status using + 1.
        - Update self.issue\_summary\_data at entry at “total\_issues” using + 1.
  - Otherwise.
    - Set field from self.field\_map.get(self.filters.based\_on).
    - Set value from d.get(field).
    - If not value.
      - Set value from translated “Not Specified”.
    - Evaluate self.issue\_summary\_data.setdefault(value, Platform.\_dict()).setdefault(status, 0.0).
    - Evaluate self.issue\_summary\_data.setdefault(value, Platform.\_dict()).setdefault(“total\_issues”, 0.0).
    - Update self.issue\_summary\_data at value at status using + 1.
    - If agreement\_status.
      - Evaluate self.issue\_summary\_data at value.setdefault(agreement\_status, 0.0).
      - Update self.issue\_summary\_data at value at agreement\_status using + 1.
    - Update self.issue\_summary\_data at value at “total\_issues” using + 1.
- Evaluate self.get\_metrics\_data().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get metrics data](operations-003.md#op-8ccbf1caa98850).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1306)

<a id="op-8ccbf1caa98850"></a>
### Issue Summary.get metrics data

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_metrics_data`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- Set issues from list().
- Set metrics\_list from list(“avg\_response\_time”, “avg\_first\_response\_time”, “avg\_hold\_time”, “avg\_resolution\_time”, …).
- For each entry in self.entries.
  - Evaluate issues.append(entry.name).
- Set field from self.field\_map.get(self.filters.based\_on).
- If issues.
  - If self.filters.based\_on equals “Assigned To”.
    - Evaluate self.set\_metrics\_by\_assignee().
  - Otherwise.
    - Set data from Platform.db.sql(formatted text   SELECT  {field}, AVG(first\_response\_time) as avg\_frt,  AVG(avg\_response\_time) as avg\_resp\_time,  AVG(total\_hold\_time) as avg\_hold, mapping(“issues” → iss ….
    - For each entry in data.
      - Set value from entry.get(field).
      - If not value.
        - Set value from translated “Not Specified”.
      - For each metric in metrics\_list.
        - Evaluate self.issue\_summary\_data.setdefault(value, Platform.\_dict()).setdefault(metric, 0.0).
      - Set self.issue\_summary\_data at value at “avg\_response\_time” from (entry.get(“avg\_resp\_time”) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“avg\_resp\_time”) → 0.0.
      - Set self.issue\_summary\_data at value at “avg\_first\_response\_time” from (entry.get(“avg\_frt”) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“avg\_frt”) → 0.0.
      - Set self.issue\_summary\_data at value at “avg\_hold\_time” from (entry.get(“avg\_hold\_time”) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“avg\_hold\_time”) → 0.0.
      - Set self.issue\_summary\_data at value at “avg\_resolution\_time” from (entry.get(“avg\_resolution\_time”) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“avg\_resolution\_time”) → 0.0.
      - Set self.issue\_summary\_data at value at “avg\_user\_resolution\_time” from (entry.get(“avg\_user\_resolution\_time”) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“avg\_user\_resolution\_time”) → 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set metrics by assignee](operations-003.md#op-5fdde88b3f617b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1303)

<a id="op-5fdde88b3f617b"></a>
### Issue Summary.set metrics by assignee

`operation_enterprise_binding_enterprise_support_report_issue_summary_issue_summary_issuesummary_set_metrics_by_assignee`

**Inputs** self.

**Local steps**

- Set metric\_fields from mapping(“avg\_response\_time” → “avg\_response\_time”, “avg\_first\_response\_time” → “first\_response\_time”, “avg\_hold\_time” → “total\_hold\_time”, “avg\_resolution\_time” → “resolution\_time”, …).
- For each tuple(metric, field) in metric\_fields.items().
  - Set values\_by\_user from Platform.\_dict().
  - For each d in self.entries.
    - If d.get(field) is distinct from no value.
      - For each user in json.loads((d.\_assign or “&#91;&#93;”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.\_assign → “&#91;&#93;”.
        - Evaluate values\_by\_user.setdefault(user, list()).append(d.get(field)).
  - For each tuple(user, values) in values\_by\_user.items().
    - Set self.issue\_summary\_data.setdefault(user, Platform.\_dict()) at metric from (sum(values) ÷ len(values)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1289)

<a id="op-783d4c3251e00b"></a>
### Issue Summary.get chart data

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_chart_data`

**Inputs** self.

**Local steps**

- Set self.chart from list().
- Set labels from list().
- Set open\_issues from list().
- Set replied\_issues from list().
- Set on\_hold\_issues from list().
- Set resolved\_issues from list().
- Set closed\_issues from list().
- Set entity from self.filters.based\_on.
- Set entity\_field from self.field\_map.get(entity).
- If entity equals “Assigned To”.
  - Set entity\_field from “user”.
- For each entry in self.data.
  - Evaluate labels.append(entry.get(entity\_field)).
  - Evaluate open\_issues.append(entry.get(“open”)).
  - Evaluate replied\_issues.append(entry.get(“replied”)).
  - Evaluate on\_hold\_issues.append(entry.get(“on\_hold”)).
  - Evaluate resolved\_issues.append(entry.get(“resolved”)).
  - Evaluate closed\_issues.append(entry.get(“closed”)).
- Set self.chart from mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → “Open”, “values” → open\_issues at slice no value to 30), mapping(“name” → “Replied”, “values” → replie ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L1644) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1298)

<a id="op-84da8818596a5b"></a>
### Issue Summary.get report summary

`operation_enterprise_support_report_issue_summary_business_behavior_issue_summary_get_report_summary`

**Inputs** self.

**Local steps**

- Set self.report\_summary from list().
- Set open\_issues from 0.
- Set replied from 0.
- Set on\_hold from 0.
- Set resolved from 0.
- Set closed from 0.
- For each entry in self.data.
  - Update open\_issues using + entry.get(“open”).
  - Update replied using + entry.get(“replied”).
  - Update on\_hold using + entry.get(“on\_hold”).
  - Update resolved using + entry.get(“resolved”).
  - Update closed using + entry.get(“closed”).
- Set self.report\_summary from list(mapping(“value” → open\_issues, “indicator” → “Red”, “label” → translated “Open”, “datatype” → “Int”), mapping(“value” → replied, “indicator” → “Grey”, “label” → translated “Replied”, “datatype” → “Int ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L2475) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1304)

## Service · Issues

<a id="op-3be09944eb3df5"></a>
### Get context

`operation_enterprise_support_web_form_issues_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L6247) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1314)

## Record · Service level agreement

[Record definition](../../../../data/record-types/service_level_agreement.json)

<a id="op-e9bc751efb6442"></a>
### Service Level Agreement.validate

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_selected\_doctype().
- Evaluate self.validate\_doc().
- Evaluate self.validate\_status\_field().
- Evaluate self.check\_priorities().
- Evaluate self.check\_support\_and\_resolution().
- Evaluate self.validate\_condition().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate selected doctype](operations-003.md#op-0d2bc13e87808b), [validate doc](operations-003.md#op-d63535b219149d), [validate status field](operations-004.md#op-2186a9afc64849), [check priorities](operations-003.md#op-7ce19f4679fb33), [check support and resolution](operations-003.md#op-cfbb3886c9e8a4), [validate condition](operations-004.md#op-4846bb2307e6dd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L1560) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1238)

<a id="op-7ce19f4679fb33"></a>
### Service Level Agreement.check priorities

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_check_priorities`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Set Response Time for Priority {0} in row {1}.”.format(priority.priority, priority.idx) · validation helper — translated “Response Time for {0} priority in row {1} can't be greater than Resolution Time.”.format(priority.priority, priority.idx) · validation helper — translated “Priority {0} has been repeated.”.format(repeated\_priority) · validation helper — translated “Select a Default Priority.”.

**Local steps**

- Set priorities from list().
- For each priority in self.priorities.
  - If not priority.response\_time.
    - Call the validation error handler Platform.throw(translated “Set Response Time for Priority {0} in row {1}.”.format(priority.priority, priority.idx)).
  - If self.apply\_sla\_for\_resolution.
    - If not priority.resolution\_time.
      - Call the validation error handler Platform.throw(translated “Set Response Time for Priority {0} in row {1}.”.format(priority.priority, priority.idx)).
    - Set response from priority.response\_time.
    - Set resolution from priority.resolution\_time.
    - If response &gt; resolution.
      - Call the validation error handler Platform.throw(translated “Response Time for {0} priority in row {1} can't be greater than Resolution Time.”.format(priority.priority, priority.idx)).
  - Evaluate priorities.append(priority.priority).
- If len(set(priorities)) differs from len(priorities).
  - Set repeated\_priority from get\_repeated(priorities).
  - Call the validation error handler Platform.throw(translated “Priority {0} has been repeated.”.format(repeated\_priority)).
- Attempt the following.
  - Set self.default\_priority from next(generator of d.priority for d drawn from self.priorities where d.default\_priority).
    - Draw d from self.priorities, keep a combination only if (d.default\_priority).
- On failure (Exception).
  - Call the validation error handler Platform.throw(translated “Select a Default Priority.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L1711) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1229)

<a id="op-cfbb3886c9e8a4"></a>
### Service Level Agreement.check support and resolution

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_check_support_and_resolution`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Start Time can't be greater than or equal to End Time for {0}.”.format(support\_and\_resolution.workday) · validation helper — translated “Workday {0} has been repeated.”.format(repeated\_days).

**Local steps**

- Set week from get\_weekdays().
- Set support\_days from list().
- For each support\_and\_resolution in self.support\_and\_resolution.
  - Evaluate support\_days.append(support\_and\_resolution.workday).
  - Set support\_and\_resolution.idx from (week.index(support\_and\_resolution.workday) + 1).
  - If to\_timedelta(support\_and\_resolution.start\_time) ≥ to\_timedelta(support\_and\_resolution.end\_time).
    - Call the validation error handler Platform.throw(translated “Start Time can't be greater than or equal to End Time for {0}.”.format(support\_and\_resolution.workday)).
- If len(set(support\_days)) differs from len(support\_days).
  - Set repeated\_days from get\_repeated(support\_days).
  - Call the validation error handler Platform.throw(translated “Workday {0} has been repeated.”.format(repeated\_days)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L2366) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1230)

<a id="op-d63535b219149d"></a>
### Service Level Agreement.validate doc

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_validate_record`

**Inputs** self.

**Record and data access** read “Support Settings” via get\_single\_value · read “Service Level Agreement” via exists.

**Explicit failure paths** validation helper — translated “{0} is not enabled in {1}”.format(Platform.bold(translated “Track Service Level Agreement”), get\_link\_to\_form(“Support Settings”, “Support Settings”)) · validation helper — translated “Default Service Level Agreement for {0} already exists.”.format(self.document\_type) · validation helper — translated “Service Level Agreement for {0} {1} already exists.”.format(Platform.bold(self.entity\_type), Platform.bold(self.entity)).

**Local steps**

- If (self.enabled and not Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enabled → not Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”).
  - Call the validation error handler Platform.throw(translated “{0} is not enabled in {1}”.format(Platform.bold(translated “Track Service Level Agreement”), get\_link\_to\_form(“Support Settings”, “Support Settings”))).
- If (self.default\_service\_level\_agreement and Platform.db.exists(“Service Level Agreement”, mapping(“document\_type” → self.document\_type, “default\_service\_level\_agreement” → “1”, “name” → list(“!=”, self.name)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default\_service\_level\_agreement → Platform.db.exists(“Service Level Agreement”, mapping(“document\_type” → self.document\_type, “default\_service\_level\_agreement” → “1”, “name” → list(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “Default Service Level Agreement for {0} already exists.”.format(self.document\_type)).
- If (self.start\_date and self.end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.start\_date → self.end\_date.
  - Evaluate self.validate\_from\_to\_dates(self.start\_date, self.end\_date).
- If (self.entity\_type and self.entity and Platform.db.exists(“Service Level Agreement”, mapping(“entity\_type” → self.entity\_type, “entity” → self.entity, “name” → list(“!=”, self.name)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.entity\_type → self.entity → Platform.db.exists(“Service Level Agreement”, mapping(“entity\_type” → self.entity\_type, “entity” → self.entity, “name” → list(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “Service Level Agreement for {0} {1} already exists.”.format(Platform.bold(self.entity\_type), Platform.bold(self.entity))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L3) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1240)

<a id="op-0d2bc13e87808b"></a>
### Service Level Agreement.validate selected doctype

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_validate_selected_record_type`

**Inputs** self.

**Record and data access** read “DocType” via get\_all.

**Explicit failure paths** validation helper.

**Local steps**

- Set invalid\_doctypes from list(Platform.model.core\_doctypes\_list).
- Evaluate invalid\_doctypes.extend(list(“Cost Center”, “Company”)).
- Set valid\_document\_types from Platform.get\_all(“DocType”, mapping(“issingle” → 0, “istable” → 0, “is\_submittable” → 0, “name” → list(“not in”, invalid\_doctypes), …), pluck = “name”).
- If self.document\_type does not belong to valid\_document\_types.
  - Call the validation error handler Platform.throw(msg = translated “Please select valid document type.”, title = translated “Invalid Document Type”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L4) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1241)
