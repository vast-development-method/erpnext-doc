# Forms, reports and navigation · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dashboard

[Record definition](../../../../data/record-types/dashboard.json)

<a id="op-9aff4a86a40f84"></a>
### Get non standard charts in dashboard

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_non_standard_charts_in_dashboard`

**Inputs** dashboard.

**Record and data access** read “Dashboard Chart” via get\_list.

**Explicit results** list of chart\_link.chart for chart\_link drawn from dashboard.charts where chart\_link.chart belongs to non\_standard\_charts.

**Local steps**

- Set non\_standard\_charts from list of doc.name for doc drawn from Platform.get\_list(“Dashboard Chart”, mapping(“is\_standard” → 0)).
  - Draw doc from Platform.get\_list(“Dashboard Chart”, mapping(“is\_standard” → 0)).
- Return list of chart\_link.chart for chart\_link drawn from dashboard.charts where chart\_link.chart belongs to non\_standard\_charts.
  - Draw chart\_link from dashboard.charts, keep a combination only if (chart\_link.chart belongs to non\_standard\_charts).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L5142) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L75) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L598)

<a id="op-bfed69804715cb"></a>
### Get non standard cards in dashboard

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_non_standard_cards_in_dashboard`

**Inputs** dashboard.

**Record and data access** read “Number Card” via get\_list.

**Explicit results** list of card\_link.card for card\_link drawn from dashboard.cards where card\_link.card belongs to non\_standard\_cards.

**Local steps**

- Set non\_standard\_cards from list of doc.name for doc drawn from Platform.get\_list(“Number Card”, mapping(“is\_standard” → 0)).
  - Draw doc from Platform.get\_list(“Number Card”, mapping(“is\_standard” → 0)).
- Return list of card\_link.card for card\_link drawn from dashboard.cards where card\_link.card belongs to non\_standard\_cards.
  - Draw card\_link from dashboard.cards, keep a combination only if (card\_link.card belongs to non\_standard\_cards).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L5308) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L74) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L597)

<a id="op-8ce01042ef1e80"></a>
### Get non standard warning message

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_non_standard_warning_message`

**Inputs** non\_standard\_docs\_map.

**Explicit results** html.

**Local steps**

- Set message from translated “Please set the following documents in this Dashboard as standard first.”.
- Bind local operation get\_html for subsequent calls.
- Set html from (message + text in the contract).
- For each doctype in non\_standard\_docs\_map.
  - If non\_standard\_docs\_map at doctype.
    - Update html using + get\_html(non\_standard\_docs\_map at doctype, doctype).
- Return html.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L5474) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L76) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L599)

<a id="op-c28caae61c3c75"></a>
### Get non standard warning message.get html

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_non_standard_warning_message_get_document_markup`

**Inputs** docs, doctype.

**Explicit results** html.

**Local steps**

- Set html from formatted text &lt;p&gt;{Platform.bold(doctype)}&lt;/p&gt;.
- For each doc in docs.
  - Update html using + formatted text &lt;div&gt;&lt;a href="/desk/Form/{doctype}/{doc}"&gt;{doc}&lt;/a&gt;&lt;/div&gt;.
- Update html using + text in the contract.
- Return html.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L5800) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L77) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L600)

## Record · Dashboard chart

[Record definition](../../../../data/record-types/dashboard_chart.json)

<a id="op-7412105c35f03c"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** effective access lookup.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L116) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L96) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L619)

<a id="op-1da525b4f26bfa"></a>
### Has permission

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L117) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L98) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L621)

<a id="op-5e913ba2906446"></a>
### Get

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get`

**Inputs** chart\_name = no value, chart = no value, no\_cache = no value, filters = no value, from\_date = no value, to\_date = no value, timespan = no value, time\_interval = no value, heatmap\_year = no value, refresh = no value.

**Wrappers, in declaration order** Platform.whitelist(), cache\_source.

**Record and data access** resolve a document from “Dashboard Chart” via get\_doc.

**Explicit results** chart\_config.

**Local steps**

- If chart\_name.
  - Set chart from Platform.get\_doc(“Dashboard Chart”, chart\_name).
- Otherwise.
  - Set chart from Platform.\_dict(Platform.parse\_json(chart)).
- Set heatmap\_year from (heatmap\_year or chart.heatmap\_year).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in heatmap\_year → chart.heatmap\_year.
- Set timespan from (timespan or chart.timespan).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in timespan → chart.timespan.
- If timespan equals “Select Date Range”.
  - If (from\_date and len(from\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → len(from\_date).
    - Set from\_date from get\_datetime(from\_date).
  - Otherwise.
    - Set from\_date from chart.from\_date.
  - If (to\_date and len(to\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_date → len(to\_date).
    - Set to\_date from get\_datetime(to\_date).
  - Otherwise.
    - Set to\_date from get\_datetime(chart.to\_date).
- Set timegrain from (time\_interval or chart.time\_interval).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in time\_interval → chart.time\_interval.
- Set filters from (Platform.parse\_json(filters) or Platform.parse\_json(chart.filters\_json)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(filters) → Platform.parse\_json(chart.filters\_json).
- If not filters.
  - Set filters from list().
- Evaluate filters.append(list(chart.document\_type, “docstatus”, “&lt;”, 2)).
- If chart.chart\_type equals “Group By”.
  - Set chart\_config from get\_group\_by\_chart\_config(chart, filters).
- Otherwise.
  - If chart.type equals “Heatmap”.
    - Set chart\_config from get\_heatmap\_chart\_config(chart, filters, heatmap\_year).
  - Otherwise.
    - Set chart\_config from get\_chart\_config(chart, filters, timespan, timegrain, …).
- Return chart\_config.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L113) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L89) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L612)

<a id="op-bcc6dd3181ba12"></a>
### Create dashboard chart

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_create_dashboard_chart`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Dashboard Chart” via exists.

**State and service calls** request new\_doc for “Dashboard Chart” · call insert on doc.

**Explicit results** doc.

**Local steps**

- Set args from Platform.parse\_json(args).
- Set doc from Platform.new\_doc(“Dashboard Chart”).
- Evaluate doc.update(args).
- If args.get(“custom\_options”).
  - Set doc.custom\_options from json.dumps(args.get(“custom\_options”)).
- If Platform.db.exists(“Dashboard Chart”, args.chart\_name).
  - Set args.chart\_name from append\_number\_if\_name\_exists(“Dashboard Chart”, args.chart\_name).
  - Set doc.chart\_name from args.chart\_name.
- Evaluate doc.insert(ignore\_permissions = true).
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L1078) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L82) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L605)

<a id="op-449a233549b6b2"></a>
### Create report chart

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_create_report_chart`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set doc from create\_dashboard\_chart(args).
- Set args from Platform.parse\_json(args).
- Set args.chart\_name from doc.chart\_name.
- If args.dashboard.
  - Evaluate add\_chart\_to\_dashboard(json.dumps(args)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L1471) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L83) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L606)

<a id="op-d1ff7addf1823a"></a>
### Add chart to dashboard

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_add_chart_to_dashboard`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Dashboard” via get\_doc · resolve a document from “Dashboard Chart” via get\_doc.

**State and service calls** request new\_doc for “Dashboard Chart Link” · call save on chart · call save on dashboard · commit.

**Local steps**

- Set args from Platform.parse\_json(args).
- Set dashboard from Platform.get\_doc(“Dashboard”, args.dashboard).
- Set dashboard\_link from Platform.new\_doc(“Dashboard Chart Link”).
- Set dashboard\_link.chart from (args.chart\_name or args.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.chart\_name → args.name.
- If (args.set\_standard and dashboard.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.set\_standard → dashboard.is\_standard.
  - Set chart from Platform.get\_doc(“Dashboard Chart”, dashboard\_link.chart).
  - Set chart.is\_standard from 1.
  - Set chart.module from dashboard.module.
  - Evaluate chart.save().
- Evaluate dashboard.append(“charts”, dashboard\_link).
- Evaluate dashboard.save().
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L1679) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L81) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L604)

<a id="op-5b5340c9d70642"></a>
### Get chart config

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_chart_configuration`

**Inputs** chart, filters, timespan, timegrain, from\_date, to\_date.

**Record and data access** read doctype via get\_list.

**Explicit results** mapping(“labels” → list of format\_date(get\_period(r at 0, timegrain), parse\_day\_first = true) when timegrain belongs to tuple(“Daily”, “Weekly”), otherwise get\_period(r at 0, timegrain) for r drawn from re ….

**Local steps**

- If not from\_date.
  - Set from\_date from get\_from\_date\_from\_timespan(to\_date, timespan).
  - Set from\_date from get\_period\_beginning(from\_date, timegrain).
- If not to\_date.
  - Set to\_date from now\_datetime().
- Set doctype from chart.document\_type.
- Set datefield from chart.based\_on.
- Set value\_field from (chart.value\_based\_on or “1”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in chart.value\_based\_on → “1”.
- Set from\_date from from\_date.strftime(“%Y-%m-%d”).
- Set to\_date from to\_date.
- Evaluate filters.append(list(doctype, datefield, “&gt;=”, from\_date)).
- Evaluate filters.append(list(doctype, datefield, “&lt;=”, to\_date)).
- Set data from Platform.get\_list(doctype, fields = list(datefield, mapping(“SUM” → value\_field), mapping(“COUNT” → “\*”)), filters = filters, group\_by = datefield, order\_by = datefield, …).
- Set result from get\_result(data, timegrain, from\_date, to\_date, …).
- Return mapping(“labels” → list of format\_date(get\_period(r at 0, timegrain), parse\_day\_first = true) when timegrain belongs to tuple(“Daily”, “Weekly”), otherwise get\_period(r at 0, timegrain) for r drawn from re ….
  - Draw r from result.
  - Value choice on timegrain belongs to tuple(“Daily”, “Weekly”) — true gives format\_date(get\_period(r at 0, timegrain), parse\_day\_first = true), false gives get\_period(r at 0, timegrain).
  - Draw r from result.
  - Draw r from result.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L114) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L91) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L614)

<a id="op-5edcd347cef2bb"></a>
### Get heatmap chart config

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_heatmap_chart_configuration`

**Inputs** chart, filters, heatmap\_year.

**Explicit results** mapping(“labels” → list(), “dataPoints” → data).

**Local steps**

- Set aggregate\_function from get\_aggregate\_function(chart.chart\_type).
- Set value\_field from (chart.value\_based\_on or “1”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in chart.value\_based\_on → “1”.
- Set doctype from chart.document\_type.
- Set datefield from chart.based\_on.
- Set year from cint(heatmap\_year) when heatmap\_year, otherwise getdate(nowdate()).year.
  - Value choice on heatmap\_year — true gives cint(heatmap\_year), false gives getdate(nowdate()).year.
- Evaluate filters.append(list(doctype, datefield, “&gt;”, formatted text {year}-01-01)).
- Evaluate filters.append(list(doctype, datefield, “&lt;”, formatted text {(year + 1)}-01-01)).
- Set day\_timestamp from UnixTimestamp(Date(Platform.qb.DocType(doctype) at datefield)).
- Set query from Platform.qb.get\_query(doctype, fields = list(day\_timestamp, mapping(aggregate\_function → value\_field)), filters = filters).
- Set data from dict(nested operand in the contract.groupby(day\_timestamp).orderby(day\_timestamp).run(as\_list = true)).
- Return mapping(“labels” → list(), “dataPoints” → data).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L115) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L94) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L617)

<a id="op-f79899d287daf9"></a>
### Get group by chart config

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_group_by_chart_configuration`

**Inputs** chart, filters.

**Declared result** (dict bitwise or no value).

**Record and data access** read doctype via get\_list · read group\_by\_field\_field.options via get\_value.

**Explicit results** mapping(“labels” → list of item.name for item drawn from data, “datasets” → list(mapping(“name” → translated chart.name, “values” → list of item at “count” for item drawn from data))) · no value.

**Local steps**

- Set aggregate\_function from get\_aggregate\_function(chart.group\_by\_type).
- Set value\_field from (chart.aggregate\_function\_based\_on or “1”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in chart.aggregate\_function\_based\_on → “1”.
- Set group\_by\_field from chart.group\_by\_based\_on.
- Set doctype from chart.document\_type.
- Set data from Platform.get\_list(doctype, fields = list(formatted text {group\_by\_field} as name, mapping(aggregate\_function → value\_field, “as” → “count”)), filters = filters, parent\_doctype = chart.parent\_document\_type, ….
  - Value choice on “.” belongs to group\_by\_field — true gives group\_by\_field, false gives formatted text ′tab{doctype}′.′{group\_by\_field}′.
- Set group\_by\_field\_field from Platform.get\_meta(doctype).get\_field(group\_by\_field).
- If (data and group\_by\_field\_field.fieldtype equals “Link”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → group\_by\_field\_field.fieldtype equals “Link”.
  - Set meta from Platform.get\_meta(group\_by\_field\_field.options).
  - For each item in data.
    - If meta.title\_field.
      - Set item.name from Platform.get\_value(group\_by\_field\_field.options, item.name, meta.title\_field).
    - Otherwise.
      - If meta.translated\_doctype.
        - Set item.name from translated item.get(“name”, “Not Specified”).
- If data.
  - Return mapping(“labels” → list of item.name for item drawn from data, “datasets” → list(mapping(“name” → translated chart.name, “values” → list of item at “count” for item drawn from data))).
    - Draw item from data.
    - Draw item from data.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L3565) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L93) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L616)

<a id="op-66c50cf8f3053a"></a>
### Get aggregate function

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_aggregate_function`

**Inputs** chart\_type.

**Explicit results** mapping(“Sum” → “SUM”, “Count” → “COUNT”, “Average” → “AVG”) at chart\_type.

**Local steps**

- Return mapping(“Sum” → “SUM”, “Count” → “COUNT”, “Average” → “AVG”) at chart\_type.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L4333) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L90) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L613)

<a id="op-54c4661d252484"></a>
### Get result

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_result`

**Inputs** data, timegrain, from\_date, to\_date, chart\_type.

**Explicit results** result.

**Local steps**

- Set dates from get\_dates\_from\_timegrain(from\_date, to\_date, timegrain).
- Set result from list of list(date, 0) for date drawn from dates.
  - Draw date from dates.
- Set data\_index from 0.
- If data.
  - For each d in result.
    - Set count from 0.
    - While (data\_index &lt; len(data) and getdate(data at data\_index at 0) ≤ d at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in data\_index &lt; len(data) → getdate(data at data\_index at 0) ≤ d at 0.
      - Update d at 1 using + flt(data at data\_index at 1).
      - Update count using + flt(data at data\_index at 2).
      - Update data\_index using + 1.
    - If (chart\_type equals “Average” and count differs from 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in chart\_type equals “Average” → count differs from 0.
      - Set d at 1 from (d at 1 ÷ count).
    - If chart\_type equals “Count”.
      - Set d at 1 from count.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L4411) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L97) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L620)

<a id="op-af99708c6100e2"></a>
### Get charts for user

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_charts_for_user`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Dashboard Chart” via get\_list.

**Explicit results** Platform.db.get\_list(“Dashboard Chart”, fields = list(“name”), filters = filters, or\_filters = or\_filters, as\_list = 1).

**Local steps**

- Set or\_filters from mapping(“owner” → Platform.session.user, “is\_public” → 1).
- Return Platform.db.get\_list(“Dashboard Chart”, fields = list(“name”), filters = filters, or\_filters = or\_filters, as\_list = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L4910) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L92) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L615)

<a id="op-0896a90b89b696"></a>
### Dashboard Chart.on update

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_dashboard_chart_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_key(formatted text chart-data:{self.name}).
- If (Platform.conf.developer\_mode and self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.is\_standard.
  - Evaluate export\_to\_files(record\_list = list(list(“Dashboard Chart”, self.name)), record\_module = self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L5201) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L86) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L609)

<a id="op-133f489c3bcd0f"></a>
### Dashboard Chart.validate

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_dashboard_chart_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot edit Standard charts”.

**Local steps**

- If (not Platform.conf.developer\_mode and self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → self.is\_standard.
  - Call the validation error handler Platform.throw(translated “Cannot edit Standard charts”).
- If (self.chart\_type differs from “Custom” and self.chart\_type differs from “Report”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.chart\_type differs from “Custom” → self.chart\_type differs from “Report”.
  - Evaluate self.check\_required\_field().
  - Evaluate self.check\_document\_type().
- Evaluate self.validate\_custom\_options().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check required field](operations-018.md#op-67df7106b3ac84), [check document type](operations-018.md#op-663ff230768a60), [validate custom options](operations-018.md#op-7b64e4dcebe077).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L5380) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L87) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L610)

<a id="op-67df7106b3ac84"></a>
### Dashboard Chart.check required field

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_dashboard_chart_check_required_field`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Document type is required to create a dashboard chart” · validation helper — translated “Parent document type is required to create a dashboard chart” · validation helper — translated “Group By field is required to create a dashboard chart” · validation helper — translated “Aggregate Function field is required to create a dashboard chart” · validation helper — translated “Time series based on is required to create a dashboard chart” · 1 additional forms in the steps below.

**Local steps**

- If not self.document\_type.
  - Call the validation error handler Platform.throw(translated “Document type is required to create a dashboard chart”).
- If (self.document\_type and Platform.get\_meta(self.document\_type).istable and not self.parent\_document\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.document\_type → Platform.get\_meta(self.document\_type).istable → not self.parent\_document\_type.
  - Call the validation error handler Platform.throw(translated “Parent document type is required to create a dashboard chart”).
- If self.chart\_type equals “Group By”.
  - If not self.group\_by\_based\_on.
    - Call the validation error handler Platform.throw(translated “Group By field is required to create a dashboard chart”).
  - If (self.group\_by\_type belongs to list(“Sum”, “Average”) and not self.aggregate\_function\_based\_on).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.group\_by\_type belongs to list(“Sum”, “Average”) → not self.aggregate\_function\_based\_on.
    - Call the validation error handler Platform.throw(translated “Aggregate Function field is required to create a dashboard chart”).
- Otherwise.
  - If not self.based\_on.
    - Call the validation error handler Platform.throw(translated “Time series based on is required to create a dashboard chart”).
  - If (self.chart\_type belongs to list(“Sum”, “Average”) and not self.value\_based\_on).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.chart\_type belongs to list(“Sum”, “Average”) → not self.value\_based\_on.
    - Call the validation error handler Platform.throw(translated “Value Based On field is required to create a dashboard chart”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L5603) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L85) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L608)

<a id="op-663ff230768a60"></a>
### Dashboard Chart.check document type

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_dashboard_chart_check_document_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You cannot create a dashboard chart from single DocTypes”.

**Local steps**

- If Platform.get\_meta(self.document\_type).issingle.
  - Call the validation error handler Platform.throw(translated “You cannot create a dashboard chart from single DocTypes”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L6106) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L84) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L607)

<a id="op-7b64e4dcebe077"></a>
### Dashboard Chart.validate custom options

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_dashboard_chart_validate_custom_options`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Invalid json added in the custom options: {0}”.format(str(error)).

**Local steps**

- If self.custom\_options.
  - Attempt the following.
    - Evaluate json.loads(self.custom\_options).
  - On failure (ValueError) bound to error.
    - Call the validation error handler Platform.throw(translated “Invalid json added in the custom options: {0}”.format(str(error))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L6211) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L88) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L611)

<a id="op-bb624a97cf9cea"></a>
### Get parent doctypes

`operation_foundation_desk_record_definitions_dashboard_chart_business_behavior_get_parent_record_types`

**Inputs** child\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** (standard + custom).

**Local steps**

- Require isinstance(child\_type, str) or raise an assertion failure.
- Set standard from Platform.get\_all(“DocField”, fields = “parent”, filters = mapping(“fieldtype” → “Table”, “options” → child\_type), pluck = “parent”).
- Set custom from Platform.get\_all(“Custom Field”, fields = “dt”, filters = mapping(“fieldtype” → “Table”, “options” → child\_type), pluck = “dt”).
- Return (standard + custom).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0163.json#L6371) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L95) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L618)

## Record · Dashboard chart source

[Record definition](../../../../data/record-types/dashboard_chart_source.json)

<a id="op-2336cfb86661c7"></a>
### Get config

`operation_foundation_desk_record_definitions_dashboard_chart_source_business_behavior_get_configuration`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** resolve a document from “Dashboard Chart Source” via get\_doc.

**Explicit results** doc.read\_config().

**Local steps**

- Set doc from Platform.get\_doc(“Dashboard Chart Source”, name).
- Return doc.read\_config().

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0164.json#L6451) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L627)

<a id="op-21eede09ebe137"></a>
### Dashboard Chart Source.on update

`operation_foundation_desk_record_definitions_dashboard_chart_source_business_behavior_dashboard_chart_source_on_update`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Creation of this document is only permitted in developer mode.”.

**Local steps**

- If not Platform.request.
  - Return no value.
- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Creation of this document is only permitted in developer mode.”).
- Evaluate export\_to\_files(record\_list = list(list(self.doctype, self.name)), record\_module = self.module, create\_init = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0164.json#L6564) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L625)
