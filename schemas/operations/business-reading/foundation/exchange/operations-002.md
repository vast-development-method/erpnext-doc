# Integration and transport · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Auto email report

[Record definition](../../../../data/record-types/auto_email_report.json)

<a id="op-8f175e3ab9a80e"></a>
### Auto Email Report.validate report format

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_validate_report_format`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is not a valid report format. Report format should one of the following {1}”.format(Platform.bold(self.format), Platform.bold(“, ”.join(valid\_report\_formats))).

**Local steps**

- Set valid\_report\_formats from list(“HTML”, “XLSX”, “CSV”, “PDF”).
- If self.format does not belong to valid\_report\_formats.
  - Call the validation error handler Platform.throw(translated “{0} is not a valid report format. Report format should one of the following {1}”.format(Platform.bold(self.format), Platform.bold(“, ”.join(valid\_report\_formats)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L5584) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1592)

<a id="op-0ebddefe4dbbc3"></a>
### Auto Email Report.validate mandatory fields

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_validate_mandatory_fields`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- Set filters from Platform.parse\_json(self.filters) when self.filters, otherwise mapping().
  - Value choice on self.filters — true gives Platform.parse\_json(self.filters), false gives mapping().
- Set filter\_meta from Platform.parse\_json(self.filter\_meta) when self.filter\_meta, otherwise mapping().
  - Value choice on self.filter\_meta — true gives Platform.parse\_json(self.filter\_meta), false gives mapping().
- Set throw\_list from list of meta at “label” for meta drawn from filter\_meta where ((meta.get(“reqd”) and not meta.get(“hidden”)) and not filters.get(meta at “fieldname”)).
  - Draw meta from filter\_meta, keep a combination only if (((meta.get(“reqd”) and not meta.get(“hidden”)) and not filters.get(meta at “fieldname”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (meta.get(“reqd”) and not meta.get(“hidden”)) → not filters.get(meta at “fieldname”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.get(“reqd”) → not meta.get(“hidden”).
- If throw\_list.
  - Call the validation error handler Platform.throw(title = translated “Missing Filters Required”, msg = (((translated “Following Report Filters have missing values:” + text in the contract) + “ &lt;li&gt;”.join(throw\_list)) + “&lt;/ul&gt;”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L5786) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1590)

<a id="op-85c6b13a4610ba"></a>
### Auto Email Report.get report content

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_get_report_content`

**Inputs** self.

**Record and data access** resolve a document from “Report” via get\_doc.

**State and service calls** call insert on columns.

**Explicit results** no value · self.get\_html\_table(columns, data) · xlsx\_file.getvalue() · to\_csv(xlsx\_data) · get\_pdf(html, options, smart\_shrinking = true).

**Explicit failure paths** validation helper — translated “Invalid Output Format”.

**Local steps**

- Set report from Platform.get\_doc(“Report”, self.report).
- Set self.filters from Platform.parse\_json(self.filters) when self.filters, otherwise mapping().
  - Value choice on self.filters — true gives Platform.parse\_json(self.filters), false gives mapping().
- If (self.report\_type equals “Report Builder” and self.data\_modified\_till).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.report\_type equals “Report Builder” → self.data\_modified\_till.
  - Set self.filters at “modified” from tuple(“&gt;”, (now\_datetime() − timedelta(hours = self.data\_modified\_till))).
- If (self.report\_type differs from “Report Builder” and self.dynamic\_date\_filters\_set()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.report\_type differs from “Report Builder” → self.dynamic\_date\_filters\_set().
  - Evaluate self.prepare\_dynamic\_filters().
- Set tuple(columns, data) from report.get\_data(limit = (self.no\_of\_rows or 100), user = self.user, filters = self.filters, as\_dict = true, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.no\_of\_rows → 100.
- Evaluate columns.insert(0, Platform.\_dict(fieldname = “sr”, label = translated “Sr”, fieldtype = “Int”, width = “30px”)).
- For each i in range(len(data)).
  - Set data at i at “sr” from (i + 1).
- If (len(data) equals 0 and self.send\_if\_data).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(data) equals 0 → self.send\_if\_data.
  - Return no value.
- If self.format equals “HTML”.
  - Set tuple(columns, data) from make\_links(columns, data).
  - Set columns from update\_field\_types(columns).
  - Return self.get\_html\_table(columns, data).
- Otherwise.
  - If self.format belongs to tuple(“XLSX”, “CSV”).
    - Set report\_data from Platform.\_dict(mapping(“report\_name” → self.report, “filters” → self.filters, “columns” → columns, “result” → data)).
    - Set is\_excel from self.format equals “XLSX”.
    - Set tuple(xlsx\_data, column\_widths, styles) from build\_xlsx\_data(report\_data, list(), 1, ignore\_visible\_idx = true, build\_styles = is\_excel).
    - If is\_excel.
      - Set xlsx\_file from make\_xlsx(xlsx\_data, “Auto Email Report”, column\_widths = column\_widths, styles = styles).
      - Return xlsx\_file.getvalue().
    - Otherwise.
      - Return to\_csv(xlsx\_data).
  - Otherwise.
    - If self.format equals “PDF”.
      - Set tuple(columns, data) from make\_links(columns, data).
      - Set columns from update\_field\_types(columns).
      - Set options from mapping().
      - If len(columns) &gt; 8.
        - Set options at “orientation” from “landscape”.
      - Set html from get\_formatted\_html(subject = self.name, message = self.get\_html\_table(columns, data)).
      - Return get\_pdf(html, options, smart\_shrinking = true).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Invalid Output Format”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [dynamic date filters set](operations-002.md#op-256015c582687c), [prepare dynamic filters](operations-002.md#op-4a5fda4e00cdea), [get html table](operations-002.md#op-c4b6ae282341a9).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L6176) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1583)

<a id="op-c4b6ae282341a9"></a>
### Auto Email Report.get html table

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_get_document_markup_table`

**Inputs** self, columns = no value, data = no value.

**Record and data access** read “Report” via get\_value.

**Explicit results** Platform.render\_template(“Platform/templates/emails/auto\_email\_report.html”, mapping(“title” → self.name, “description” → self.description, “date\_time” → date\_time, “columns” → columns, …)).

**Local steps**

- Set date\_time from ((global\_date\_format(now()) + one space) + format\_time(now())).
- Set report\_doctype from Platform.db.get\_value(“Report”, self.report, “ref\_doctype”).
- Return Platform.render\_template(“Platform/templates/emails/auto\_email\_report.html”, mapping(“title” → self.name, “description” → self.description, “date\_time” → date\_time, “columns” → columns, …)).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1581)

<a id="op-287e1534dcb61a"></a>
### Auto Email Report.get file name

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_get_file_name`

**Inputs** self.

**Explicit results** “{}.{}”.format(self.report.replace(one space, “-”).replace(“/”, “-”), self.format.lower()).

**Local steps**

- Return “{}.{}”.format(self.report.replace(one space, “-”).replace(“/”, “-”), self.format.lower()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L403) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1582)

<a id="op-4a5fda4e00cdea"></a>
### Auto Email Report.prepare dynamic filters

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_prepare_dynamic_filters`

**Inputs** self.

**Local steps**

- Set self.filters from Platform.parse\_json(self.filters).
- Set to\_date from today().
- If self.use\_first\_day\_of\_period.
  - Set from\_date from to\_date.
  - If self.dynamic\_date\_period equals “Daily”.
    - Set from\_date from add\_to\_date(to\_date, days = negative 1).
  - Otherwise.
    - If self.dynamic\_date\_period equals “Weekly”.
      - Set from\_date from get\_first\_day\_of\_week(from\_date, as\_str = true).
    - Otherwise.
      - If self.dynamic\_date\_period equals “Monthly”.
        - Set from\_date from get\_first\_day(from\_date, as\_str = true).
      - Otherwise.
        - If self.dynamic\_date\_period equals “Quarterly”.
          - Set from\_date from get\_quarter\_start(from\_date, as\_str = true).
        - Otherwise.
          - If self.dynamic\_date\_period equals “Half Yearly”.
            - Set from\_date from get\_half\_year\_start(as\_str = true).
          - Otherwise.
            - If self.dynamic\_date\_period equals “Yearly”.
              - Set from\_date from get\_year\_start(from\_date, as\_str = true).
  - Evaluate self.set\_date\_filters(from\_date, to\_date).
- Otherwise.
  - Set from\_date\_value from mapping(“Daily” → tuple(“days”, negative 1), “Weekly” → tuple(“weeks”, negative 1), “Monthly” → tuple(“months”, negative 1), “Quarterly” → tuple(“months”, negative 3), …) at self.dynamic\_date\_period.
  - Set from\_date from add\_to\_date(to\_date, expanded names mapping(from\_date\_value at 0 → from\_date\_value at 1)).
  - Evaluate self.set\_date\_filters(from\_date, to\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set date filters](operations-002.md#op-14ce91dc56bc01).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L520) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1584)

<a id="op-14ce91dc56bc01"></a>
### Auto Email Report.set date filters

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_set_date_filters`

**Inputs** self, from\_date, to\_date.

**Local steps**

- Set self.filters at self.from\_date\_field from from\_date.
- Set self.filters at self.to\_date\_field from to\_date.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L1302) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1587)

<a id="op-3bc42b05e39541"></a>
### Auto Email Report.send

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_send`

**Inputs** self.

**State and service calls** sendmail.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please set filters value in Report Filter table.”.

**Local steps**

- If (self.filter\_meta and not self.filters).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filter\_meta → not self.filters.
  - Call the validation error handler Platform.throw(translated “Please set filters value in Report Filter table.”).
- Set data from self.get\_report\_content().
- If not data.
  - Return no value.
- Set attachments from no value.
- If self.format equals “HTML”.
  - Set message from data.
- Otherwise.
  - Set message from self.get\_html\_table().
- If self.format differs from “HTML”.
  - Set attachments from list(mapping(“fname” → self.get\_file\_name(), “fcontent” → data)).
- Evaluate Platform.sendmail(recipients = self.email\_to.split(), sender = formataddr(tuple(self.sender, self.sender\_email)) when self.sender, otherwise empty text, subject = self.name, message = message, …).
  - Value choice on self.sender — true gives formataddr(tuple(self.sender, self.sender\_email)), false gives empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get report content](operations-002.md#op-85c6b13a4610ba), [get html table](operations-002.md#op-c4b6ae282341a9), [get file name](operations-002.md#op-287e1534dcb61a).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.email\_to.split(), sender = formataddr(tuple(self.sender, self.sender\_email)) when self.sender, otherwise empty text, subject = self.name, message = message, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L1402) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1585)

<a id="op-256015c582687c"></a>
### Auto Email Report.dynamic date filters set

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_dynamic_date_filters_set`

**Inputs** self.

**Explicit results** (self.dynamic\_date\_period and self.from\_date\_field and self.to\_date\_field).

**Local steps**

- Return (self.dynamic\_date\_period and self.from\_date\_field and self.to\_date\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.dynamic\_date\_period → self.from\_date\_field → self.to\_date\_field.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L1875) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1580)

<a id="op-57378da3dfaaea"></a>
### Download

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_download`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Auto Email Report” via get\_doc.

**State and service calls** msgprint with translated “No Data”.

**Explicit results** no value.

**Local steps**

- Set auto\_email\_report from Platform.get\_doc(“Auto Email Report”, name).
- Evaluate auto\_email\_report.check\_permission().
- Set data from auto\_email\_report.get\_report\_content().
- If not data.
  - Evaluate Platform.msgprint(translated “No Data”).
  - Return no value.
- Set Platform.local.response.filecontent from data.
- Set Platform.local.response.type from “download”.
- Set Platform.local.response.filename from auto\_email\_report.get\_file\_name().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from auto\_email\_report.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L1938) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1593)

<a id="op-3747b88c7d3f5c"></a>
### Send now

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_send_now`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Auto Email Report” via get\_doc.

**Local steps**

- Set auto\_email\_report from Platform.get\_doc(“Auto Email Report”, name).
- Evaluate auto\_email\_report.check\_permission().
- Evaluate auto\_email\_report.send().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from auto\_email\_report.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L2218) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1599)

<a id="op-d3fb6c3bf95a2d"></a>
### Send daily

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_send_daily`

**Inputs** no declared parameters.

**Record and data access** read “Auto Email Report” via get\_all.

**State and service calls** enqueue with “Platform.email.doctype.auto\_email\_report.auto\_email\_report.process\_auto\_email\_report”.

**Local steps**

- Set enabled\_reports from Platform.get\_all(“Auto Email Report”, filters = mapping(“enabled” → 1, “frequency” → tuple(“in”, tuple(“Daily”, “Weekdays”, “Weekly”)))).
- For each report in enabled\_reports.
  - Evaluate Platform.enqueue(“Platform.email.doctype.auto\_email\_report.auto\_email\_report.process\_auto\_email\_report”, report = report, queue = “long”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.email.doctype.auto\_email\_report.auto\_email\_report.process\_auto\_email\_report”, report = report, queue = “long”).

**Boundaries to resolve** stored data, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L2347) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1597)

<a id="op-a7d92cc4882c84"></a>
### Process auto email report

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_process_auto_email_report`

**Inputs** report.

**Record and data access** resolve a document from “Auto Email Report” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set current\_day from calendar.day\_name at now\_datetime().weekday().
- Set auto\_email\_report from Platform.get\_doc(“Auto Email Report”, report.name).
- If auto\_email\_report.frequency equals “Weekdays”.
  - If current\_day belongs to tuple(“Saturday”, “Sunday”).
    - Return no value.
- Otherwise.
  - If auto\_email\_report.frequency equals “Weekly”.
    - If auto\_email\_report.day\_of\_week differs from current\_day.
      - Return no value.
- Attempt the following.
  - Evaluate auto\_email\_report.send().
- On failure (Exception).
  - Evaluate auto\_email\_report.log\_error(formatted text Failed to send {auto\_email\_report.name} Auto Email Report).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L2590) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1596)

<a id="op-8a5f65dcec8ef6"></a>
### Send monthly

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_send_monthly`

**Inputs** no declared parameters.

**Record and data access** read “Auto Email Report” via get\_all · resolve a document from “Auto Email Report” via get\_doc.

**Local steps**

- For each report in Platform.get\_all(“Auto Email Report”, mapping(“enabled” → 1, “frequency” → “Monthly”)).
  - Evaluate Platform.get\_doc(“Auto Email Report”, report.name).send().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L86) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1598)

<a id="op-cc39bf5d726d06"></a>
### Make links

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_make_links`

**Inputs** columns, data.

**Record and data access** read col.parent via exists · resolve a document from col.parent via get\_doc.

**Explicit results** tuple(columns, data).

**Local steps**

- For each row in data.
  - Set doc\_name from row.get(“name”).
  - For each col in columns.
    - If not row.get(col.fieldname).
      - Continue with the next iteration or loop test.
    - If col.fieldtype equals “Link”.
      - If (col.options and col.options differs from “Currency”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.options → col.options differs from “Currency”.
        - Set row at col.fieldname from get\_link\_to\_form(col.options, row at col.fieldname).
    - Otherwise.
      - If col.fieldtype equals “Dynamic Link”.
        - If (col.options and row.get(col.options)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.options → row.get(col.options).
          - Set row at col.fieldname from get\_link\_to\_form(row at col.options, row at col.fieldname).
      - Otherwise.
        - If col.fieldtype equals “Currency”.
          - Set doc from no value.
          - If (doc\_name and col.get(“parent”) and not Platform.get\_meta(col.parent).istable).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_name → col.get(“parent”) → not Platform.get\_meta(col.parent).istable.
            - If Platform.db.exists(col.parent, doc\_name).
              - Set doc from Platform.get\_doc(col.parent, doc\_name).
          - Set row at col.fieldname from Platform.format\_value(row at col.fieldname, col, doc = doc).
- Return tuple(columns, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L3039) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1595)

<a id="op-c973d111507194"></a>
### Update field types

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_update_field_types`

**Inputs** columns.

**Explicit results** columns.

**Local steps**

- For each col in columns.
  - If (col.fieldtype belongs to tuple(“Link”, “Dynamic Link”, “Currency”) and col.options differs from “Currency”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.fieldtype belongs to tuple(“Link”, “Dynamic Link”, “Currency”) → col.options differs from “Currency”.
    - Set col.fieldtype from “Data”.
    - Set col.options from empty text.
- Return columns.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L3723) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1600)

<a id="op-771cd8f96779f1"></a>
### Get half year start

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_get_half_year_start`

**Inputs** as\_str = false.

**Explicit results** result\_date when not as\_str, otherwise result\_date.strftime(DATE\_FORMAT).

**Local steps**

- Set today\_date from getdate(today()).
- Set half\_year from 1 when today\_date.month ≤ 6, otherwise 2.
  - Value choice on today\_date.month ≤ 6 — true gives 1, false gives 2.
- Set year from today\_date.year when half\_year equals 1, otherwise (today\_date.year + 1).
  - Value choice on half\_year equals 1 — true gives today\_date.year, false gives (today\_date.year + 1).
- Set month from 1 when half\_year equals 1, otherwise 7.
  - Value choice on half\_year equals 1 — true gives 1, false gives 7.
- Set day from 1.
- Set result\_date from datetime.date(year, month, day).
- Return result\_date when not as\_str, otherwise result\_date.strftime(DATE\_FORMAT).
  - Value choice on not as\_str — true gives result\_date, false gives result\_date.strftime(DATE\_FORMAT).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L3889) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1594)

## Service · Cloud billing

<a id="op-1b1f43d3918497"></a>
### Summary

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_summary`

**Inputs** client.

**Declared result** dict.

**Explicit results** client.get(\_path(client, “get\_billing\_summary”)).

**Local steps**

- Return client.get(\_path(client, “get\_billing\_summary”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6501) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L567)

<a id="op-0bee3b35c33e30"></a>
### Get plan options

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_get_plan_options`

**Inputs** client.

**Declared result** dict.

**Explicit results** client.get(\_path(client, “get\_plan\_options”)).

**Local steps**

- Return client.get(\_path(client, “get\_plan\_options”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6576) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L561)

<a id="op-4c4ce5d4e25510"></a>
### Change plan

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_change_plan`

**Inputs** client, plan.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “change\_plan”), mapping(“plan” → plan)).

**Local steps**

- Return client.post(\_path(client, “change\_plan”), mapping(“plan” → plan)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6651) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L554)

<a id="op-0ac7c4f49957a9"></a>
### Get profile

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_get_profile`

**Inputs** client.

**Declared result** dict.

**Explicit results** client.get(\_path(client, “get\_billing\_profile”)).

**Local steps**

- Return client.get(\_path(client, “get\_billing\_profile”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6759) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L562)

<a id="op-cc09e5844b21ae"></a>
### Save profile

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_save_profile`

**Inputs** client, fields.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “save\_billing\_profile”), fields).

**Local steps**

- Return client.post(\_path(client, “save\_billing\_profile”), fields).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6834) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L566)

<a id="op-76156be7a85831"></a>
### Get gateways

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_get_gateways`

**Inputs** client.

**Declared result** list.

**Explicit results** client.get(\_path(client, “get\_payment\_gateways”)).

**Local steps**

- Return client.get(\_path(client, “get\_payment\_gateways”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6925) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L560)

<a id="op-44039a982800c6"></a>
### Add payment method

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_add_payment_method`

**Inputs** client, method\_type, contact = no value, gateway = no value.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “add\_payment\_method”), mapping(“method\_type” → method\_type, “contact” → contact, “gateway” → gateway)).

**Local steps**

- Return client.post(\_path(client, “add\_payment\_method”), mapping(“method\_type” → method\_type, “contact” → contact, “gateway” → gateway)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L553)
