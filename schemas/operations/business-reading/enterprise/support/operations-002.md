# Customer support · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Issue

[Record definition](../../../../data/record-types/issue.json)

<a id="op-e70e130980f426"></a>
### Get customer email

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_get_customer_email`

**Inputs** communication.

**Declared result** str.

**Explicit results** parse\_addr(recipients at 0) at 1 when recipients, otherwise empty text · (communication.sender or empty text).

**Local steps**

- If communication.sent\_or\_received equals “Sent”.
  - Set recipients from split\_emails(communication.recipients).
  - Return parse\_addr(recipients at 0) at 1 when recipients, otherwise empty text.
    - Value choice on recipients — true gives parse\_addr(recipients at 0) at 1, false gives empty text.
- Return (communication.sender or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.sender → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1251)

<a id="op-11be3522951c6c"></a>
### Get time in timedelta

`operation_enterprise_support_record_definitions_issue_business_behavior_get_time_in_timedelta`

**Inputs** time.

**Explicit results** timedelta(hours = time.hour, minutes = time.minute, seconds = time.second).

**Local steps**

- Return timedelta(hours = time.hour, minutes = time.minute, seconds = time.second).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L4095) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1109)

<a id="op-fc914e0c6ffa92"></a>
### Set first response time

`operation_enterprise_support_record_definitions_issue_business_behavior_set_first_response_time`

**Inputs** communication, method.

**State and service calls** call db\_set on issue.

**Local steps**

- If communication.get(“reference\_doctype”) equals “Issue”.
  - Set issue from get\_parent\_doc(communication).
  - If (is\_first\_response(issue) and issue.service\_level\_agreement).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_first\_response(issue) → issue.service\_level\_agreement.
    - Set first\_response\_time from calculate\_first\_response\_time(issue, get\_datetime(issue.first\_responded\_on)).
    - Evaluate issue.db\_set(“first\_response\_time”, first\_response\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L4180) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1124)

<a id="op-e8538bfae49b08"></a>
### Reopen issue without sla

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_reopen_issue_without_sla`

**Inputs** communication, method = no value.

**Declared result** no value.

**State and service calls** request set\_value on “Issue” · call save on issue.

**Explicit results** no value.

**Local steps**

- If (communication.get(“reference\_doctype”) differs from “Issue” or communication.sent\_or\_received differs from “Received”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.get(“reference\_doctype”) differs from “Issue” → communication.sent\_or\_received differs from “Received”.
  - Return no value.
- Set issue from get\_parent\_doc(communication).
- If (not issue or issue.service\_level\_agreement or not issue.sla\_resolution\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not issue → issue.service\_level\_agreement → not issue.sla\_resolution\_date.
  - Return no value.
- Set previous\_status from issue.get\_doc\_before\_save().status.
- Evaluate Platform.db.set\_value(“Issue”, issue.name, “status”, previous\_status, update\_modified = false).
- Evaluate issue.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1258)

<a id="op-92a724909c8c88"></a>
### Is first response

`operation_enterprise_support_record_definitions_issue_business_behavior_is_first_response`

**Inputs** issue.

**Record and data access** read “Communication” via get\_all.

**Explicit results** true · false.

**Local steps**

- Set responses from Platform.get\_all(“Communication”, filters = mapping(“reference\_name” → issue.name, “sent\_or\_received” → “Sent”)).
- <a id="op-92a724909c8c88-guard-5"></a>If len(responses) equals 1.
  - Return true.
- Return false.

**Derived branch illustrations**

- At the comparison len(responses) equals 1, length of responses = 1 selects the branch that returns true. With length of responses = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-92a724909c8c88-guard-5)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L4413) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1114)

<a id="op-2fe6b12f8ab30c"></a>
### Calculate first response time

`operation_enterprise_support_record_definitions_issue_business_behavior_calculate_first_response_time`

**Inputs** issue, first\_responded\_on.

**Record and data access** resolve a document from “Service Level Agreement” via get\_cached\_doc.

**Explicit results** get\_elapsed\_time(issue\_creation\_date, first\_responded\_on) · get\_elapsed\_time(issue\_creation\_time, end\_time) · get\_elapsed\_time(start\_time, first\_responded\_on\_in\_seconds) · 1.0 · first\_response\_time.

**Local steps**

- Set issue\_creation\_date from get\_datetime((issue.service\_level\_agreement\_creation or issue.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in issue.service\_level\_agreement\_creation → issue.creation.
- Set issue\_creation\_time from get\_time\_in\_seconds(issue\_creation\_date).
- Set first\_responded\_on\_in\_seconds from get\_time\_in\_seconds(first\_responded\_on).
- Set support\_hours from Platform.get\_cached\_doc(“Service Level Agreement”, issue.service\_level\_agreement).support\_and\_resolution.
- If getdate(issue\_creation\_date) equals getdate(first\_responded\_on).
  - If is\_work\_day(issue\_creation\_date, support\_hours).
    - Set tuple(start\_time, end\_time) from get\_working\_hours(issue\_creation\_date, support\_hours).
    - If (is\_during\_working\_hours(issue\_creation\_date, support\_hours) and is\_during\_working\_hours(first\_responded\_on, support\_hours)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_during\_working\_hours(issue\_creation\_date, support\_hours) → is\_during\_working\_hours(first\_responded\_on, support\_hours).
      - Return get\_elapsed\_time(issue\_creation\_date, first\_responded\_on).
    - Otherwise.
      - If is\_during\_working\_hours(issue\_creation\_date, support\_hours).
        - Return get\_elapsed\_time(issue\_creation\_time, end\_time).
      - Otherwise.
        - If is\_during\_working\_hours(first\_responded\_on, support\_hours).
          - Return get\_elapsed\_time(start\_time, first\_responded\_on\_in\_seconds).
        - Otherwise.
          - Return 1.0.
  - Otherwise.
    - Return 1.0.
- Otherwise.
  - If date\_diff(first\_responded\_on, issue\_creation\_date) equals 1.
    - Set first\_response\_time from 0.
  - Otherwise.
    - Set first\_response\_time from calculate\_initial\_frt(issue\_creation\_date, (date\_diff(first\_responded\_on, issue\_creation\_date) − 1), support\_hours).
  - If is\_work\_day(issue\_creation\_date, support\_hours).
    - Set tuple(start\_time, end\_time) from get\_working\_hours(issue\_creation\_date, support\_hours).
    - If is\_during\_working\_hours(issue\_creation\_date, support\_hours).
      - Update first\_response\_time using + get\_elapsed\_time(issue\_creation\_time, end\_time).
    - Otherwise.
      - If is\_before\_working\_hours(issue\_creation\_date, support\_hours).
        - Update first\_response\_time using + get\_elapsed\_time(start\_time, end\_time).
  - If is\_work\_day(first\_responded\_on, support\_hours).
    - Set tuple(start\_time, end\_time) from get\_working\_hours(first\_responded\_on, support\_hours).
    - If is\_during\_working\_hours(first\_responded\_on, support\_hours).
      - Update first\_response\_time using + get\_elapsed\_time(start\_time, first\_responded\_on\_in\_seconds).
    - Otherwise.
      - If not is\_before\_working\_hours(first\_responded\_on, support\_hours).
        - Update first\_response\_time using + get\_elapsed\_time(start\_time, end\_time).
  - If first\_response\_time.
    - Return first\_response\_time.
  - Otherwise.
    - Return 1.0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Service Level Agreement”, issue.service\_level\_agreement).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1102)

<a id="op-ba8a4bda7d3685"></a>
### Get time in seconds

`operation_enterprise_support_record_definitions_issue_business_behavior_get_time_in_seconds`

**Inputs** date.

**Explicit results** timedelta(hours = date.hour, minutes = date.minute, seconds = date.second).

**Local steps**

- Return timedelta(hours = date.hour, minutes = date.minute, seconds = date.second).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L5564) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1108)

<a id="op-615b1332fc7490"></a>
### Get working hours

`operation_enterprise_support_record_definitions_issue_business_behavior_get_working_hours`

**Inputs** date, support\_hours.

**Explicit results** tuple(day.start\_time, day.end\_time).

**Local steps**

- If is\_work\_day(date, support\_hours).
  - Set weekday from Platform.utils.get\_weekday(date).
  - For each day in support\_hours.
    - If day.workday equals weekday.
      - Return tuple(day.start\_time, day.end\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L5649) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1110)

<a id="op-a01d0fe1afdba1"></a>
### Is work day

`operation_enterprise_support_record_definitions_issue_business_behavior_is_work_day`

**Inputs** date, support\_hours.

**Explicit results** true · false.

**Local steps**

- Set weekday from Platform.utils.get\_weekday(date).
- For each day in support\_hours.
  - If day.workday equals weekday.
    - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L5815) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1115)

<a id="op-e14796ed610d95"></a>
### Is during working hours

`operation_enterprise_support_record_definitions_issue_business_behavior_is_during_working_hours`

**Inputs** date, support\_hours.

**Explicit results** true · false.

**Local steps**

- Set tuple(start\_time, end\_time) from get\_working\_hours(date, support\_hours).
- Set time from get\_time\_in\_seconds(date).
- If (time ≥ start\_time and time ≤ end\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in time ≥ start\_time → time ≤ end\_time.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L5943) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1113)

<a id="op-7d3fa206465b05"></a>
### Get elapsed time

`operation_enterprise_support_record_definitions_issue_business_behavior_get_elapsed_time`

**Inputs** start\_time, end\_time.

**Explicit results** round(time\_diff\_in\_seconds(end\_time, start\_time), 2).

**Local steps**

- Return round(time\_diff\_in\_seconds(end\_time, start\_time), 2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L6106) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1104)

<a id="op-e0b02199857908"></a>
### Calculate initial frt

`operation_enterprise_support_record_definitions_issue_business_behavior_calculate_initial_frt`

**Inputs** issue\_creation\_date, days\_in\_between, support\_hours.

**Explicit results** initial\_frt.

**Local steps**

- Set initial\_frt from 0.
- For each i in range(days\_in\_between).
  - Set date from (issue\_creation\_date + timedelta(days = (i + 1))).
  - If is\_work\_day(date, support\_hours).
    - Set tuple(start\_time, end\_time) from get\_working\_hours(date, support\_hours).
    - Update initial\_frt using + get\_elapsed\_time(start\_time, end\_time).
- Return initial\_frt.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L6186) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1103)

<a id="op-e25c1560f10a23"></a>
### Is before working hours

`operation_enterprise_support_record_definitions_issue_business_behavior_is_before_working_hours`

**Inputs** date, support\_hours.

**Explicit results** true · false.

**Local steps**

- Set tuple(start\_time, end\_time) from get\_working\_hours(date, support\_hours).
- Set time from get\_time\_in\_seconds(date).
- If time &lt; start\_time.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L6423) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1112)

<a id="op-1791b73123a6fc"></a>
### Get holidays

`operation_enterprise_support_record_definitions_issue_business_behavior_get_holidays`

**Inputs** holiday\_list\_name.

**Record and data access** resolve a document from “Holiday List” via get\_cached\_doc.

**Explicit results** holidays.

**Local steps**

- Set holiday\_list from Platform.get\_cached\_doc(“Holiday List”, holiday\_list\_name).
- Set holidays from list of holiday.holiday\_date for holiday drawn from holiday\_list.holidays.
  - Draw holiday from holiday\_list.holidays.
- Return holidays.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Holiday List”, holiday\_list\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L6564) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1105)

<a id="op-d59409a7d6932c"></a>
### Get data

`operation_enterprise_support_record_definitions_issue_issue_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “issue”, “transactions” → list(mapping(“label” → translated “Activity”, “items” → list(“Task”)))).

**Local steps**

- Return mapping(“fieldname” → “issue”, “transactions” → list(mapping(“label” → translated “Activity”, “items” → list(“Task”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L6679) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1128)

## Report · Issue analytics

<a id="op-b9cec291221b4d"></a>
### Execute

`operation_enterprise_support_report_issue_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** IssueAnalytics(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return IssueAnalytics(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1277)

<a id="op-3d843dc9dfec97"></a>
### Issue Analytics.initialize

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Evaluate self.get\_period\_date\_ranges().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period date ranges](operations-002.md#op-ca0791a9833199).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0973.json#L1355) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1287)

<a id="op-37fa2d32c1f2b2"></a>
### Issue Analytics.run

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data, no value, self.chart).

**Local steps**

- Evaluate self.get\_columns().
- Evaluate self.get\_data().
- Evaluate self.get\_chart\_data().
- Return tuple(self.columns, self.data, no value, self.chart).

**Methods declared on this owner** [get columns](operations-002.md#op-5cb8498055ff76), [get data](operations-002.md#op-e3d0f686d8b4d5), [get chart data](operations-003.md#op-a7bbf5c1e1b6b2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0973.json#L1460) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1288)

<a id="op-5cb8498055ff76"></a>
### Issue Analytics.get columns

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- If self.filters.based\_on equals “Customer”.
  - Evaluate self.columns.append(mapping(“label” → translated “Customer”, “options” → “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, …)).
- Otherwise.
  - If self.filters.based\_on equals “Assigned To”.
    - Evaluate self.columns.append(mapping(“label” → translated “User”, “fieldname” → “user”, “fieldtype” → “Dynamic Link”, “options” → “user\_doctype”, …)).
  - Otherwise.
    - If self.filters.based\_on equals “Issue Type”.
      - Evaluate self.columns.append(mapping(“label” → translated “Issue Type”, “fieldname” → “issue\_type”, “fieldtype” → “Link”, “options” → “Issue Type”, …)).
    - Otherwise.
      - If self.filters.based\_on equals “Issue Priority”.
        - Evaluate self.columns.append(mapping(“label” → translated “Issue Priority”, “fieldname” → “priority”, “fieldtype” → “Link”, “options” → “Issue Priority”, …)).
- For each end\_date in self.periodic\_daterange.
  - Set period from self.get\_period(end\_date).
  - Evaluate self.columns.append(mapping(“label” → translated period, “fieldname” → scrub(period), “fieldtype” → “Int”, “width” → 120)).
- Evaluate self.columns.append(mapping(“label” → translated “Total”, “fieldname” → “total”, “fieldtype” → “Int”, “width” → 120)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period](operations-002.md#op-ff7dcf81f769e3).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1279)

<a id="op-e3d0f686d8b4d5"></a>
### Issue Analytics.get data

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_data`

**Inputs** self.

**Local steps**

- Evaluate self.get\_issues().
- Evaluate self.get\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get issues](operations-002.md#op-7bdeef32b72da1), [get rows](operations-003.md#op-bb2548deaeb18d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0973.json#L2592) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1281)

<a id="op-ff7dcf81f769e3"></a>
### Issue Analytics.get period

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_period`

**Inputs** self, date.

**Explicit results** self.get\_week(date) · period.

**Local steps**

- If self.filters.range equals “Weekly”.
  - Return self.get\_week(date).
- Set months from list(“Jan”, “Feb”, “Mar”, “Apr”, …).
- If self.filters.range equals “Monthly”.
  - Set period from str(months at (date.month − 1)).
- Otherwise.
  - If self.filters.range equals “Quarterly”.
    - Set period from (“Quarter ” + str((((date.month − 1) floor divide 3) + 1))).
  - Otherwise.
    - Set year from get\_fiscal\_year(date, self.filters.company).
    - Set period from str(year at 0).
- If (getdate(self.filters.from\_date).year differs from getdate(self.filters.to\_date).year and self.filters.range differs from “Yearly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(self.filters.from\_date).year differs from getdate(self.filters.to\_date).year → self.filters.range differs from “Yearly”.
  - Update period using + (one space + str(date.year)).
- Return period.

**Methods declared on this owner** [get week](operations-002.md#op-83c6f29ef48374).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1283)

<a id="op-83c6f29ef48374"></a>
### Issue Analytics.get week

`operation_enterprise_binding_enterprise_support_report_issue_analytics_issue_analytics_issueanalytics_get_week`

**Inputs** self, date.

**Declared result** str.

**Explicit results** formatted text Week {week} {iso\_year} · formatted text Week {week}.

**Local steps**

- Set tuple(iso\_year, week) from date.isocalendar() at slice no value to 2.
- If self.weeks\_span\_years.
  - Return formatted text Week {week} {iso\_year}.
- Return formatted text Week {week}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L7) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1288)

<a id="op-ca0791a9833199"></a>
### Issue Analytics.get period date ranges

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_period_date_ranges`

**Inputs** self.

**Local steps**

- Bind dependencies MO, relativedelta.
- Set tuple(from\_date, to\_date) from tuple(getdate(self.filters.from\_date), getdate(self.filters.to\_date)).
- Set increment from mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(self.filters.range, 1).
- If self.filters.range equals “Monthly”.
  - Set from\_date from from\_date.replace(day = 1).
- Otherwise.
  - If self.filters.range equals “Quarterly”.
    - Set from\_date from from\_date.replace(month = ((((from\_date.month − 1) floor divide 3) × 3) + 1), day = 1).
  - Otherwise.
    - If self.filters.range equals “Yearly”.
      - Set from\_date from get\_fiscal\_year(from\_date) at 1.
    - Otherwise.
      - Set from\_date from (from\_date + relativedelta(from\_date, weekday = MO(negative 1))).
- Set self.periodic\_daterange from list().
- While true.
  - If self.filters.range equals “Weekly”.
    - Set period\_end\_date from add\_days(from\_date, 6).
  - Otherwise.
    - Set period\_end\_date from add\_to\_date(from\_date, months = increment, days = negative 1).
  - If period\_end\_date &gt; to\_date.
    - Set period\_end\_date from to\_date.
  - Evaluate self.periodic\_daterange.append(period\_end\_date).
  - Set from\_date from add\_days(period\_end\_date, 1).
  - If period\_end\_date equals to\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set self.weeks\_span\_years from len(set of date.isocalendar() at 0 for date drawn from self.periodic\_daterange) &gt; 1.
  - Draw date from self.periodic\_daterange.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1284)

<a id="op-7bdeef32b72da1"></a>
### Issue Analytics.get issues

`operation_enterprise_support_report_issue_analytics_business_behavior_issue_analytics_get_issues`

**Inputs** self.

**Record and data access** read “Issue” via get\_list.

**Local steps**

- Set filters from self.get\_common\_filters().
- Set self.field\_map from mapping(“Customer” → “customer”, “Issue Type” → “issue\_type”, “Issue Priority” → “priority”, “Assigned To” → “\_assign”).
- Set self.entries from Platform.get\_list(“Issue”, fields = list(self.field\_map.get(self.filters.based\_on), “name”, “opening\_date”), filters = filters).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get common filters](operations-003.md#op-15f9418dc64a44).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1282)
