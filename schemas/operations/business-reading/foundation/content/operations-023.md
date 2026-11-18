# Web content and issued documents · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Website analytics

<a id="op-927817b26071d6"></a>
### Website Analytics.get columns

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_get_columns`

**Inputs** self.

**Explicit results** list(mapping(“fieldname” → group\_by.fieldname, “label” → group\_by.label, “fieldtype” → “Data”, “width” → 500, …), mapping(“fieldname” → “count”, “label” → “Page Views”, “fieldtype” → “Int”, “width” → 150), ….

**Local steps**

- Set meta from Platform.get\_meta(“Web Page View”).
- Set group\_by from meta.get\_field(self.group\_by).
- Return list(mapping(“fieldname” → group\_by.fieldname, “label” → group\_by.label, “fieldtype” → “Data”, “width” → 500, …), mapping(“fieldname” → “count”, “label” → “Page Views”, “fieldtype” → “Int”, “width” → 150), ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L3166) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1509)

<a id="op-75c2af9c50d0ab"></a>
### Website Analytics.get data

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_get_data`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).groupby(self.group\_by).orderby(“count”, order = Platform.qb.desc).run().

**Local steps**

- Set WebPageView from Platform.qb.DocType(“Web Page View”).
- Set count\_all from Count(“\*”).as\_(“count”).
- Set case from Platform.qb.terms.Case().when(WebPageView.is\_unique equals “1”, “1”).
- Set count\_is\_unique from Count(case).as\_(“unique\_count”).
- Return nested operand in the contract(nested operand in the contract).groupby(self.group\_by).orderby(“count”, order = Platform.qb.desc).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L3508) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1510)

<a id="op-435c8d066028ee"></a>
### Website Analytics.get query for mariadb

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_get_query_for_relational_database`

**Inputs** self.

**Explicit results** tuple(query, values).

**Local steps**

- Set filters\_range from self.filters.range.
- Set field from “creation”.
- Set date\_format from “%Y-%m-%d”.
- If filters\_range equals “Weekly”.
  - Set field from “ADDDATE(creation, INTERVAL 1-DAYOFWEEK(creation) DAY)”.
- Otherwise.
  - If filters\_range equals “Monthly”.
    - Set date\_format from “%Y-%m-01”.
- Set query from formatted text   SELECT  DATE\_FORMAT({field}, %s) as date,  COUNT(\*) as count,  COUNT(CASE WHEN is\_unique = 1 THEN 1 END) as unique\_count  FROM ′ta.
- Set values from tuple(date\_format, self.filters.from\_date, self.filters.to\_date, date\_format).
- Return tuple(query, values).

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L3926) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1511)

<a id="op-6b39251e47d3bc"></a>
### Website Analytics.get query for postgres

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_get_query_for_relational_database_2`

**Inputs** self.

**Explicit results** tuple(query, values).

**Local steps**

- Set filters\_range from self.filters.range.
- Set field from “creation”.
- Set granularity from “day”.
- If filters\_range equals “Weekly”.
  - Set granularity from “week”.
- Otherwise.
  - If filters\_range equals “Monthly”.
    - Set granularity from “day”.
- Set query from formatted text   SELECT  DATE\_TRUNC(%s, {field}) as date,  COUNT(\*) as count,  COUNT(CASE WHEN CAST(is\_unique as Integer) = 1 THEN 1 END) as unique\_co.
- Set values from tuple(granularity, self.filters.from\_date, self.filters.to\_date, granularity).
- Return tuple(query, values).

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L4189) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1512)

<a id="op-9d81da879c4bb8"></a>
### Website Analytics.get chart data

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_get_chart_data`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** self.prepare\_chart\_data(self.chart\_data).

**Local steps**

- Set current\_dialect from (Platform.db.db\_type or “mariadb”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.db\_type → “mariadb”.
- If current\_dialect equals “mariadb”.
  - Set tuple(query, values) from self.\_get\_query\_for\_mariadb().
- Otherwise.
  - Set tuple(query, values) from self.\_get\_query\_for\_postgres().
- Set self.chart\_data from Platform.db.sql(query, values = values, as\_dict = 1).
- Return self.prepare\_chart\_data(self.chart\_data).

**Methods declared on this owner** [get query for mariadb](operations-023.md#op-435c8d066028ee), [get query for postgres](operations-023.md#op-6b39251e47d3bc), [prepare chart data](operations-023.md#op-581fab0aad02d6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L4477) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1508)

<a id="op-581fab0aad02d6"></a>
### Website Analytics.prepare chart data

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_prepare_chart_data`

**Inputs** self, data.

**Explicit results** chart.

**Local steps**

- Set date\_range from get\_dates\_from\_timegrain(self.filters.from\_date, self.filters.to\_date, self.filters.range).
- If self.filters.range equals “Monthly”.
  - Set date\_range from list of Platform.utils.add\_days(dd, 1) for dd drawn from date\_range.
    - Draw dd from date\_range.
- Set labels from list().
- Set total\_dataset from list().
- Set unique\_dataset from list().
- Bind local operation get\_data\_for\_date for subsequent calls.
- For each date in date\_range.
  - Evaluate labels.append(date.strftime(“%b %d %Y”)).
  - Set match from get\_data\_for\_date(date).
  - Evaluate total\_dataset.append(match.get(“count”, 0)).
  - Evaluate unique\_dataset.append(match.get(“unique\_count”, 0)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Total Views”, “type” → “line”, “values” → total\_dataset), mapping(“name” → “Unique Visits”, “type” → “line”, “values” → uniqu ….
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L4718) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1515)

<a id="op-cf22c44c17bd60"></a>
### Website Analytics.prepare chart data.get data for date

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_prepare_chart_data_get_data_for_date`

**Inputs** date.

**Explicit results** item · mapping(“count” → 0, “unique\_count” → 0).

**Local steps**

- For each item in data.
  - Set item\_date from getdate(item.get(“date”)).
  - If item\_date equals date.
    - Return item.
- Return mapping(“count” → 0, “unique\_count” → 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L5496) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1516)

<a id="op-2007009df4141b"></a>
### Website Analytics.get report summary

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_get_report_summary`

**Inputs** self.

**Explicit results** list(mapping(“value” → total\_count, “label” → “Total Page Views”, “datatype” → “Int”), mapping(“value” → unique\_count, “label” → “Unique Page Views”, “datatype” → “Int”)).

**Local steps**

- Set total\_count from 0.
- Set unique\_count from 0.
- For each data in self.chart\_data.
  - Update unique\_count using + data.get(“unique\_count”).
  - Update total\_count using + data.get(“count”).
- Return list(mapping(“value” → total\_count, “label” → “Total Page Views”, “datatype” → “Int”), mapping(“value” → unique\_count, “label” → “Unique Page Views”, “datatype” → “Int”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L5655) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1513)

## Service · Website generator

<a id="op-e0581590052fb1"></a>
### Website Generator.initialize

`operation_foundation_website_website_generator_business_behavior_website_generator_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set self.route from no value.
- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3420) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1588)

<a id="op-6a1b23f76549ab"></a>
### Website Generator.get website properties

`operation_foundation_website_website_generator_business_behavior_website_generator_get_website_properties`

**Inputs** self, key = no value, default = no value.

**Explicit results** out.get(key, default) · out.

**Local steps**

- Set out from (getattr(self, “\_website”, no value) or getattr(self, “website”, no value) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self, “\_website”, no value) → getattr(self, “website”, no value) → mapping().
- If not isinstance(out, dict).
  - Set out from mapping().
- If key.
  - Return out.get(key, default).
- Otherwise.
  - Return out.

**Values supplied outside this operation** selected callable from getattr(self, “\_website”, no value), getattr(self, “website”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3519) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1587)

<a id="op-2cf407ec0c7c38"></a>
### Website Generator.autoname

`operation_foundation_website_website_generator_business_behavior_website_generator_autoname`

**Inputs** self.

**Local steps**

- If (not self.name and self.meta.autoname differs from “hash”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.name → self.meta.autoname differs from “hash”.
  - Set self.name from self.scrubbed\_title().

If control reaches the end, it returns no value.

**Methods declared on this owner** [scrubbed title](operations-023.md#op-57589f3029c28f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3727) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1581)

<a id="op-737125cd99bf1e"></a>
### Website Generator.onload

`operation_foundation_website_website_generator_business_behavior_website_generator_onload`

**Inputs** self.

**Local steps**

- Evaluate self.get(“\_\_onload”).update(mapping(“is\_website\_generator” → true, “published” → self.is\_website\_published())).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is website published](operations-023.md#op-856cb5d1297c8c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3840) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1594)

<a id="op-534edc12b99787"></a>
### Website Generator.validate

`operation_foundation_website_website_generator_business_behavior_website_generator_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_route().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set route](operations-023.md#op-823bbc3951d9a5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3952) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1601)

<a id="op-823bbc3951d9a5"></a>
### Website Generator.set route

`operation_foundation_website_website_generator_business_behavior_website_generator_set_route`

**Inputs** self.

**Local steps**

- If (self.is\_website\_published() and not self.route).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_website\_published() → not self.route.
  - Set self.route from self.make\_route().
- If self.route.
  - Set self.route from self.route.strip(“/.”) at slice no value to 139.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is website published](operations-023.md#op-856cb5d1297c8c), [make route](operations-023.md#op-8c92f4f412c192).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4003) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1599)

<a id="op-8c92f4f412c192"></a>
### Website Generator.make route

`operation_foundation_website_website_generator_business_behavior_website_generator_make_route`

**Inputs** self.

**Explicit results** ((self.meta.route + “/”) + from\_title) · from\_title.

**Local steps**

- Set from\_title from self.scrubbed\_title().
- If self.meta.route.
  - Return ((self.meta.route + “/”) + from\_title).
- Otherwise.
  - Return from\_title.

**Methods declared on this owner** [scrubbed title](operations-023.md#op-57589f3029c28f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4173) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1590)

<a id="op-57589f3029c28f"></a>
### Website Generator.scrubbed title

`operation_foundation_website_website_generator_business_behavior_website_generator_scrubbed_title`

**Inputs** self.

**Explicit results** self.scrub(self.get(self.get\_title\_field())).

**Local steps**

- Return self.scrub(self.get(self.get\_title\_field())).

**Methods declared on this owner** [scrub](operations-023.md#op-48a37057e6f0ba), [get title field](operations-023.md#op-a524e4f57c3916).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4287) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1597)

<a id="op-a524e4f57c3916"></a>
### Website Generator.get title field

`operation_foundation_website_website_generator_business_behavior_website_generator_get_title_field`

**Inputs** self.

**Explicit results** title\_field.

**Local steps**

- Set title\_field from self.get\_website\_properties(“page\_title\_field”).
- If not title\_field.
  - If self.meta.title\_field.
    - Set title\_field from self.meta.title\_field.
  - Otherwise.
    - If self.meta.has\_field(“title”).
      - Set title\_field from “title”.
    - Otherwise.
      - Set title\_field from “name”.
- Return title\_field.

**Methods declared on this owner** [get website properties](operations-023.md#op-6a1b23f76549ab).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4373) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1586)

<a id="op-19f1ffa411c839"></a>
### Website Generator.clear cache

`operation_foundation_website_website_generator_business_behavior_website_generator_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- Evaluate clear\_cache(self.route).
- Evaluate Platform.db.after\_commit.add(deferred anonymous expression).
- Evaluate Platform.db.after\_rollback.add(deferred anonymous expression).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4569) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1582)

<a id="op-48a37057e6f0ba"></a>
### Website Generator.scrub

`operation_foundation_website_website_generator_business_behavior_website_generator_scrub`

**Inputs** self, text.

**Explicit results** cleanup\_page\_name(text).replace(“\_”, “-”).

**Local steps**

- Return cleanup\_page\_name(text).replace(“\_”, “-”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4755) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1596)

<a id="op-efa210a3bdaba0"></a>
### Website Generator.get parents

`operation_foundation_website_website_generator_business_behavior_website_generator_get_parents`

**Inputs** self, context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4835) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1585)

<a id="op-05cbd3e1550e6b"></a>
### Website Generator.on update

`operation_foundation_website_website_generator_business_behavior_website_generator_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.send\_indexing\_request().
- Evaluate self.remove\_old\_route\_from\_index().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send indexing request](operations-024.md#op-f124b4fbc0b8df), [remove old route from index](operations-024.md#op-2c64aa256682a7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4875) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1593)

<a id="op-4c3187d222a829"></a>
### Website Generator.on change

`operation_foundation_website_website_generator_business_behavior_website_generator_on_change`

**Inputs** self.

**Local steps**

- Evaluate self.update\_website\_search\_index().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update website search index](operations-024.md#op-3425e2500fe408).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4946) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1591)

<a id="op-4c7236622d8194"></a>
### Website Generator.on trash

`operation_foundation_website_website_generator_business_behavior_website_generator_on_trash`

**Inputs** self.

**State and service calls** enqueue with remove\_document\_from\_index.

**Local steps**

- Evaluate self.clear\_cache().
- Evaluate self.send\_indexing\_request(“URL\_DELETED”).
- If self.allow\_website\_search\_indexing().
  - Bind dependencies remove\_document\_from\_index.
  - Evaluate Platform.enqueue(remove\_document\_from\_index, path = self.route, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-023.md#op-19f1ffa411c839), [send indexing request](operations-024.md#op-f124b4fbc0b8df), [allow website search indexing](operations-024.md#op-15ec7d6faf8300).

**Values supplied outside this operation** service or queued work from Platform.enqueue(remove\_document\_from\_index, path = self.route, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L4997) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1592)

<a id="op-856cb5d1297c8c"></a>
### Website Generator.is website published

`operation_foundation_website_website_generator_business_behavior_website_generator_is_website_published`

**Inputs** self.

**Explicit results** (self.get(condition\_field) or false) · true.

**Local steps**

- If condition\_field bound to self.get\_condition\_field().
  - Return (self.get(condition\_field) or false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(condition\_field) → false.
- Otherwise.
  - Return true.

**Methods declared on this owner** [get condition field](operations-024.md#op-7f922c446941bd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L5153) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1589)
