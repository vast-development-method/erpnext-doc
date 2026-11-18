# Record lifecycle and persistence · operations 77

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Prepared report

[Record definition](../../../../data/record-types/prepared_report.json)

<a id="op-8281595bbde260"></a>
### Delete prepared reports

`operation_foundation_core_record_definitions_prepared_report_business_behavior_delete_prepared_reports`

**Inputs** reports.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Prepared Report” via get\_doc.

**Local steps**

- Set reports from Platform.parse\_json(reports).
- For each report in reports.
  - Set prepared\_report from Platform.get\_doc(“Prepared Report”, report at “name”).
  - Evaluate prepared\_report.check\_permission(“read”).
  - Evaluate prepared\_report.delete(ignore\_permissions = true, delete\_permanently = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from prepared\_report.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L93) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L50)

<a id="op-f93ebc2a1069fb"></a>
### Create json gz file

`operation_foundation_core_record_definitions_prepared_report_business_behavior_create_structured_data_gz_file`

**Inputs** data, dt, dn, report\_name.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → json\_filename, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, …) via get\_doc.

**State and service calls** call save on \_file.

**Local steps**

- Set json\_filename from “{}\_{}.json.gz”.format(Platform.scrub(report\_name), Platform.utils.data.format\_datetime(Platform.utils.now(), “Y-m-d-H-M”)).
- Set encoded\_content from Platform.safe\_encode(Platform.as\_json(data, indent = no value, separators = tuple(“,”, “:”))).
- Set compressed\_content from gzip.compress(encoded\_content, compresslevel = 5).
- Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → json\_filename, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, …)).
- Evaluate \_file.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L459) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L49)

<a id="op-08c2980614ef5c"></a>
### Download attachment

`operation_foundation_core_record_definitions_prepared_report_business_behavior_download_attachment`

**Inputs** dn.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Prepared Report” via get\_doc.

**Explicit failure paths** validation helper — Platform.\_(“Cannot Download Report due to insufficient permissions”).

**Local steps**

- Set pr from Platform.get\_doc(“Prepared Report”, dn).
- If not Platform.has\_permission(“Prepared Report”, “read”, doc = pr).
  - Call the validation error handler Platform.throw(Platform.\_(“Cannot Download Report due to insufficient permissions”)).
- Set tuple(data, file\_name) from pr.get\_prepared\_data(with\_file\_name = true).
- Set Platform.local.response.filename from file\_name at slice no value to negative 3.
- Set Platform.local.response.filecontent from data.
- Set Platform.local.response.type from “binary”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Prepared Report”, “read”, doc = pr).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L94) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L51)

<a id="op-a7a2c3d5f127fe"></a>
### Get permission query condition

`operation_foundation_core_record_definitions_prepared_report_business_behavior_get_permission_query_condition`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L97) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L56)

<a id="op-efff0fed72cb2e"></a>
### Has permission

`operation_foundation_core_record_definitions_prepared_report_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** Boolean true, a comparison result.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L1549) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L58)

<a id="op-4f778c69be6de0"></a>
### Enqueue json to csv conversion

`operation_foundation_core_record_definitions_prepared_report_business_behavior_enqueue_structured_data_to_comma_separated_values_conversion`

**Inputs** prepared\_report\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Prepared Report” via get\_doc.

**Local steps**

- Evaluate Platform.get\_doc(“Prepared Report”, prepared\_report\_name).check\_permission(“read”).
- Evaluate \_enqueue\_json\_to\_csv\_conversion(prepared\_report\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L1764) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L52)

<a id="op-6087c4c619753a"></a>
### Enqueue json to csv conversion

`operation_foundation_core_record_definitions_prepared_report_business_behavior_enqueue_structured_data_to_comma_separated_values_conversion_2`

**Inputs** prepared\_report\_name.

**Local steps**

- Evaluate enqueue(method = convert\_json\_to\_csv, queue = “long”, prepared\_report\_name = prepared\_report\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(method = convert\_json\_to\_csv, queue = “long”, prepared\_report\_name = prepared\_report\_name).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0094.json#L1893) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L53)

<a id="op-fa28b0ed08541c"></a>
### Convert json to csv

`operation_foundation_core_record_definitions_prepared_report_business_behavior_convert_structured_data_to_comma_separated_values`

**Inputs** prepared\_report\_name.

**Record and data access** resolve a document from “Prepared Report” via get\_doc · resolve a document from mapping(“doctype” → “File”, “file\_name” → formatted text csv\_{file\_name at slice no value to negative 8}.csv, “attached\_to\_doctype” → “Prepared Report”, “attached\_to\_name” → prepared\_report\_name, …) via get\_doc · resolve a document from mapping(“doctype” → “Notification Log”, “subject” → “Your CSV file is ready for download”, “email\_content” → formatted text Click &lt;a href="{\_file.file\_url}" target="\_blank"&gt;here&lt;/a&gt; to download the file.,  … via get\_doc.

**State and service calls** call save on \_file · call insert on Platform.get\_doc(mapping(“doctype” → “Notification Log”, “subject” → “Your CSV file is ready for download”, “email\_content” → formatted text Click &lt;a href="{\_file.file\_url}" target="\_blank"&gt;here&lt;/a&gt; to dow ….

**Explicit results** no value.

**Local steps**

- Bind dependencies csv.
- Bind dependencies StringIO.
- Set doc from Platform.get\_doc(“Prepared Report”, prepared\_report\_name).
- Set tuple(json\_content, file\_name) from doc.get\_prepared\_data(with\_file\_name = true).
- If not json\_content.
  - Evaluate Platform.log\_error(formatted text No JSON content found for {prepared\_report\_name}, “CSV Conversion”).
  - Return no value.
- Set parsed from json.loads(json\_content).
- Set columns from parsed.get(“columns”, list()).
- Set result from parsed.get(“result”, list()).
- If (not columns or not result).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not columns → not result.
  - Evaluate Platform.log\_error(“Columns or result is empty”, “CSV Conversion”).
  - Return no value.
- Set fieldnames from list of col.get(“fieldname”) for col drawn from columns where col.get(“fieldname”).
  - Draw col from columns, keep a combination only if (col.get(“fieldname”)).
- Set output from StringIO().
- Set writer from csv.DictWriter(output, fieldnames = fieldnames).
- Evaluate writer.writeheader().
- For each row in result.
  - If isinstance(row, dict).
    - Evaluate writer.writerow(mapping of key → row.get(key, empty text) for key drawn from fieldnames).
      - Draw key from fieldnames.
  - Otherwise.
    - Evaluate writer.writerow(mapping of field → row at idx for tuple(idx, field) drawn from enumerate(fieldnames)).
      - Draw tuple(idx, field) from enumerate(fieldnames).
- Set csv\_content from output.getvalue().encode(“utf-8”).
- Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → formatted text csv\_{file\_name at slice no value to negative 8}.csv, “attached\_to\_doctype” → “Prepared Report”, “attached\_to\_name” → prepared\_repor ….
- Evaluate \_file.save(ignore\_permissions = true).
- Evaluate Platform.get\_doc(mapping(“doctype” → “Notification Log”, “subject” → “Your CSV file is ready for download”, “email\_content” → formatted text Click &lt;a href="{\_file.file\_url}" target="\_blank"&gt;here&lt;/a&gt; to dow ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L92) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L48)

## Report · Prepared report analytics

<a id="op-fd3411376f0947"></a>
### Execute

`operation_foundation_core_report_prepared_report_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns(filters).
- Set data from get\_data(filters = filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L3123) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L907)

<a id="op-fd8ac0f4da3628"></a>
### Get columns

`operation_foundation_core_report_prepared_report_analytics_business_behavior_get_columns`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Prepared Report”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Prepared Report”, …), mapping(“label” → translated “Report Name”, “fieldname” → “report\_name”,  ….

**Local steps**

- Return list(mapping(“label” → translated “Prepared Report”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Prepared Report”, …), mapping(“label” → translated “Report Name”, “fieldname” → “report\_name”,  ….
  - Value choice on filters.in\_minutes — true gives translated “Runtime in Minutes”, false gives translated “Runtime in Seconds”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L3246) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L908)

<a id="op-4f13253227681a"></a>
### Get data

`operation_foundation_core_report_prepared_report_analytics_business_behavior_get_data`

**Inputs** filters.

**Declared result** list at list.

**Explicit results** res.

**Local steps**

- Set pr from qb.DocType(“Prepared Report”).
- Set conditions from list(pr.status.eq(“Completed”), pr.creation.gte(add\_months(nowdate(), negative 2))).
- If filters.report.
  - Evaluate conditions.append(pr.report\_name.like(formatted text %{filters.report}%)).
- Set divisor from 1.
- If filters.in\_minutes.
  - Set divisor from 60.
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).select(nested operand in the contract.as\_(“ ….
- If filters.top\_10.
  - Set query from query.limit(10).
- Set res from query.run(as\_dict = true).
- Return res.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L3869) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L909)

## Service · Qb query

<a id="op-73bd16529b0ccd"></a>
### Database Query.initialize

`operation_foundation_model_query_builder_query_business_behavior_database_query_initialize`

**Inputs** self, doctype.

**Declared result** no value.

**Local steps**

- Set self.doctype from doctype.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L1763) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1264)

<a id="op-1f30967901832e"></a>
### Database Query.execute

`operation_foundation_model_query_builder_query_business_behavior_database_query_execute`

**Inputs** self, fields = no value, filters = no value, or\_filters = no value, group\_by = no value, order\_by = DefaultOrderBy, limit = no value, offset = no value, limit\_start = 0, limit\_page\_length = no value, as\_list = false, with\_childnames = false, debug = false, ignore\_permissions = false, user = no value, with\_comment\_count = false, join = “left join”, distinct = false, start = no value, page\_length = no value, ignore\_ifnull = false, save\_user\_settings = false, save\_user\_settings\_fields = false, update = no value, user\_settings = no value, reference\_doctype = no value, run = true, strict = true, pluck = no value, ignore\_ddl = false, parent\_doctype (named only, default no value), ignore\_user\_permissions (named only, default false).

**Declared result** list.

**Explicit results** self.\_handle\_virtual\_doctype(fields, filters, or\_filters, start, …) · list() · query · result.

**Explicit failure paths** propagate active failure.

**Local steps**

- If (isinstance(fields, dict) or (fields and isinstance(fields, list) and isinstance(fields at 0, list))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(fields, dict) → (fields and isinstance(fields, list) and isinstance(fields at 0, list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → isinstance(fields, list) → isinstance(fields at 0, list).
  - Set tuple(filters, fields) from tuple(fields, filters).
- Otherwise.
  - If (fields and isinstance(filters, list) and len(filters) &gt; 1 and isinstance(filters at 0, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → isinstance(filters, list) → len(filters) &gt; 1 → isinstance(filters at 0, str).
    - Set tuple(filters, fields) from tuple(fields, filters).
- If not fields.
  - Set fields from list((pluck or “name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pluck → “name”.
- Set self.fields from fields.
- If is\_virtual\_doctype(self.doctype).
  - If not ignore\_permissions.
    - Set ptype from “select” when Platform.only\_has\_select\_perm(self.doctype, user = user), otherwise “read”.
      - Value choice on Platform.only\_has\_select\_perm(self.doctype, user = user) — true gives “select”, false gives “read”.
    - Evaluate Platform.has\_permission(self.doctype, ptype = ptype, parent\_doctype = parent\_doctype, throw = true, user = user).
  - Return self.\_handle\_virtual\_doctype(fields, filters, or\_filters, start, …).
- If limit\_start.
  - Evaluate record a compatibility advisory for the invoked interface.
  - If offset is identical to no value.
    - Set offset from limit\_start.
- If limit\_page\_length.
  - Evaluate record a compatibility advisory for the invoked interface.
  - If limit is identical to no value.
    - Set limit from limit\_page\_length.
- If start.
  - Evaluate record a compatibility advisory for the invoked interface.
  - If offset is identical to no value.
    - Set offset from start.
- If page\_length.
  - Evaluate record a compatibility advisory for the invoked interface.
  - If limit is identical to no value.
    - Set limit from page\_length.
- Bind dependencies get\_table\_columns.
- Attempt the following.
  - Set columns from get\_table\_columns(self.doctype).
- On failure (Platform.db.TableMissingError).
  - If ignore\_ddl.
    - Return list().
  - Otherwise.
    - Propagate the active failure.
- Set kwargs from mapping(“table” → self.doctype, “fields” → fields, “filters” → filters, “or\_filters” → or\_filters, …).
- Set query from Platform.qb.get\_query(expanded names kwargs).
- If not run.
  - Return query.
- Set with\_comment\_count from (sbool(with\_comment\_count) and not as\_list and bool(self.doctype) and (not distinct or getattr(query, “\_selects\_own\_name”, false))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sbool(with\_comment\_count) → not as\_list → bool(self.doctype) → (not distinct or getattr(query, “\_selects\_own\_name”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not distinct → getattr(query, “\_selects\_own\_name”, false).
- If (with\_comment\_count and not group\_by and “\_comments” belongs to columns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in with\_comment\_count → not group\_by → “\_comments” belongs to columns.
  - Set query from query.select(Platform.qb.DocType(self.doctype).\_comments).
- If pluck.
  - Set result from query.run(debug = debug, as\_dict = true, pluck = pluck).
- Otherwise.
  - Set result from query.run(debug = debug, as\_dict = not as\_list, update = update).
- If with\_comment\_count.
  - Evaluate self.\_add\_comment\_count(result).
- If save\_user\_settings.
  - Set user\_settings\_fields from copy.deepcopy(fields) when save\_user\_settings\_fields, otherwise no value.
    - Value choice on save\_user\_settings\_fields — true gives copy.deepcopy(fields), false gives no value.
  - If (user\_settings and isinstance(user\_settings, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user\_settings → isinstance(user\_settings, str).
    - Set user\_settings from json.loads(user\_settings).
  - Evaluate self.\_save\_user\_settings(user\_settings, user\_settings\_fields, save\_user\_settings\_fields).
- Return result.

**Methods declared on this owner** [handle virtual doctype](operations-077.md#op-ab5febf8c395a7), [add comment count](operations-077.md#op-a5b5d60cf1ca24), [save user settings](operations-077.md#op-82485365d099c1).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, ptype = ptype, parent\_doctype = parent\_doctype, throw = true, user = user) · selected callable from getattr(query, “\_selects\_own\_name”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1262)

<a id="op-a5b5d60cf1ca24"></a>
### Database Query.add comment count

`operation_foundation_model_query_builder_query_business_behavior_database_query_add_comment_count`

**Inputs** self, result.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not result.
  - Return no value.
- For each row in result.
  - If not isinstance(row, dict).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set comments\_data from json.loads((row.pop(“\_comments”, no value) or “&#91;&#93;”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.pop(“\_comments”, no value) → “&#91;&#93;”.
    - Set row at “\_comment\_count” from len(comments\_data) when isinstance(comments\_data, list), otherwise 0.
      - Value choice on isinstance(comments\_data, list) — true gives len(comments\_data), false gives 0.
  - On failure (tuple(json.JSONDecodeError, TypeError)).
    - Set row at “\_comment\_count” from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L5) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1261)

<a id="op-82485365d099c1"></a>
### Database Query.save user settings

`operation_foundation_model_query_builder_query_business_behavior_database_query_save_user_settings`

**Inputs** self, user\_settings, user\_settings\_fields, save\_user\_settings\_fields.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not self.doctype.
  - Return no value.
- Attempt the following.
  - Set current\_settings from (get\_user\_settings(self.doctype) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_user\_settings(self.doctype) → mapping().
  - If user\_settings.
    - Evaluate current\_settings.update(user\_settings).
  - If (save\_user\_settings\_fields and user\_settings\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in save\_user\_settings\_fields → user\_settings\_fields.
    - Set current\_settings at “fields” from user\_settings\_fields.
  - If current\_settings.
    - Evaluate update\_user\_settings(self.doctype, current\_settings).
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L4584) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1265)

<a id="op-ab5febf8c395a7"></a>
### Database Query.handle virtual doctype

`operation_foundation_model_query_builder_query_business_behavior_database_query_handle_virtual_record_type`

**Inputs** self, fields, filters, or\_filters, start, offset, limit\_start, page\_length, limit, limit\_page\_length, order\_by, as\_list, with\_comment\_count, save\_user\_settings, save\_user\_settings\_fields, pluck, parent\_doctype.

**Declared result** list.

**Explicit results** list() · Platform.call(controller.get\_list, args = kwargs, expanded names kwargs).

**Local steps**

- Bind dependencies get\_controller.
- Bind dependencies Filters.
- Set controller from get\_controller(self.doctype).
- If not hasattr(controller, “get\_list”).
  - Return list().
- Set filters from (filters or Filters()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → Filters().
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- If not isinstance(filters, Filters).
  - Set filters from Filters(filters, doctype = self.doctype).
- Set or\_filters from (or\_filters or Filters()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in or\_filters → Filters().
- If isinstance(or\_filters, str).
  - Set or\_filters from json.loads(or\_filters).
- If not isinstance(or\_filters, Filters).
  - Set or\_filters from Filters(or\_filters, doctype = self.doctype).
- Set \_page\_length from (page\_length or limit or limit\_page\_length or 20).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_length → limit → limit\_page\_length → 20.
- Set kwargs from mapping(“fields” → fields, “filters” → filters, “or\_filters” → or\_filters, “start” → (start or offset or limit\_start or 0), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in start → offset → limit\_start → 0.
- Return Platform.call(controller.get\_list, args = kwargs, expanded names kwargs).

**Values supplied outside this operation** selected callable from get\_controller(self.doctype).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L7) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1263)

## Service · Query

<a id="op-be587f0da7471c"></a>
### Apply date field filter conversion

`operation_foundation_database_query_business_behavior_apply_date_field_filter_conversion`

**Inputs** value, operator, doctype, field.

**Explicit results** value · tuple(from\_val, to\_val) · value.date().

**Local steps**

- Attempt the following.
  - If “.” belongs to str(field).
    - Set field from field.split(“.”) at negative 1.
  - If doctype belongs to CORE\_DOCTYPES.
    - Set meta from no value.
  - Otherwise.
    - Set meta from Platform.get\_meta(doctype).
  - If meta is identical to no value.
    - Return value.
  - Set df from meta.get\_field(field).
  - If (df is identical to no value or df.fieldtype differs from “Date”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df is identical to no value → df.fieldtype differs from “Date”.
    - Return value.
  - If (operator.lower() equals “between” and isinstance(value, (list bitwise or tuple)) and len(value) equals 2).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in operator.lower() equals “between” → isinstance(value, (list bitwise or tuple)) → len(value) equals 2.
    - Set tuple(from\_val, to\_val) from value.
    - If isinstance(from\_val, datetime.datetime).
      - Set from\_val from from\_val.date().
    - If isinstance(to\_val, datetime.datetime).
      - Set to\_val from to\_val.date().
    - Return tuple(from\_val, to\_val).
  - Otherwise.
    - If isinstance(value, datetime.datetime).
      - Return value.date().
- On failure (tuple(AttributeError, TypeError, KeyError)).
  - Take no action here.
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0139.json#L900) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1030) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1171)

<a id="op-2de97c98988818"></a>
### Apply datetime field filter conversion

`operation_foundation_database_query_business_behavior_apply_datetime_field_filter_conversion`

**Inputs** between\_values, doctype, field.

**Declared result** tuple.

**Explicit results** between\_values · tuple(from\_val, to\_val).

**Local steps**

- Bind dependencies convert\_type\_for\_between\_filters.
- Set field\_name from field.
- If “.” belongs to str(field).
  - Set field\_name from field.split(“.”) at negative 1.
- If doctype belongs to CORE\_DOCTYPES.
  - Set df from no value.
- Otherwise.
  - Set meta from Platform.get\_meta(doctype).
  - Set df from meta.get\_field(field\_name) when meta, otherwise no value.
    - Value choice on meta — true gives meta.get\_field(field\_name), false gives no value.
- If not (field\_name belongs to tuple(“creation”, “modified”) or (df and df.fieldtype equals “Datetime”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field\_name belongs to tuple(“creation”, “modified”) → (df and df.fieldtype equals “Datetime”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Datetime”.
  - Return between\_values.
- Set tuple(from\_val, to\_val) from between\_values.
- Set from\_val from convert\_type\_for\_between\_filters(from\_val, set\_time = datetime.time()).
- Set to\_val from convert\_type\_for\_between\_filters(to\_val, set\_time = datetime.time(23, 59, 59, 999999)).
- Return tuple(from\_val, to\_val).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0139.json#L1541) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1031) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1172)

<a id="op-ca01ade1564210"></a>
### Engine.get query

`operation_foundation_database_query_business_behavior_engine_get_query`

**Inputs** self, table, fields = no value, filters = no value, order\_by = no value, group\_by = no value, limit = no value, offset = no value, distinct = false, for\_update = false, update = false, into = false, delete = false, validate\_filters (named only, default false), skip\_locked (named only, default false), wait (named only, default true), ignore\_permissions (named only, default true), ignore\_user\_permissions (named only, default false), user (named only, default no value), parent\_doctype (named only, default no value), reference\_doctype (named only, default no value), or\_filters (named only, default no value), db\_query\_compat (named only, default false).

**Declared result** QueryBuilder.

**Explicit results** self.query.

**Explicit failure paths** validation helper with TypeError — translated “Limit must be a non-negative integer” · validation helper with TypeError — translated “Offset must be a non-negative integer” · validation helper with Platform.ValidationError — translated “Child table fields need 'name' in ′fields′ when using distinct or aggregate queries.”.

**Local steps**

- Set qb from Platform.local.qb.
- Set db\_type from Platform.local.db.db\_type.
- Set self.is\_mariadb from db\_type equals “mariadb”.
- Set self.is\_postgres from db\_type equals “postgres”.
- Set self.is\_sqlite from db\_type equals “sqlite”.
- Set self.user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set self.parent\_doctype from parent\_doctype.
- Set self.reference\_doctype from reference\_doctype.
- Set self.apply\_permissions from not ignore\_permissions.
- Set self.ignore\_user\_permissions from ignore\_user\_permissions.
- Set self.function\_aliases from set().
- Set self.field\_aliases from set().
- Set self.db\_query\_compat from db\_query\_compat.
- Set self.permitted\_fields\_cache from mapping().
- Set self.link\_table\_aliases from mapping().
- Set self.link\_table\_counts from mapping().
- If isinstance(table, Table).
  - Set self.table from table.
  - Set self.doctype from get\_doctype\_name(table.get\_sql()).
- Otherwise.
  - Set self.doctype from table.
  - Set self.table from qb.DocType(table).
- If Platform.flags.get(“ignore\_user\_permissions\_for\_doctype”) equals self.doctype.
  - Set self.ignore\_user\_permissions from true.
- If self.apply\_permissions.
  - Evaluate self.check\_select\_permission().
  - Set self.permission\_doctype from (parent\_doctype or self.doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doctype → self.doctype.
  - Set self.permission\_table from qb.DocType(self.permission\_doctype) when self.permission\_doctype differs from self.doctype, otherwise self.table.
    - Value choice on self.permission\_doctype differs from self.doctype — true gives qb.DocType(self.permission\_doctype), false gives self.table.
- Set is\_select from false.
- If update.
  - Set self.query from qb.update(self.table, immutable = false).
- Otherwise.
  - If into.
    - Set self.query from qb.into(self.table, immutable = false).
  - Otherwise.
    - If delete.
      - Set self.query from qb.from\_(self.table, immutable = false).delete().
    - Otherwise.
      - Set self.query from qb.from\_(self.table, immutable = false).
      - Evaluate self.apply\_fields(fields).
      - Set is\_select from true.
- Evaluate self.apply\_filters(filters).
- Evaluate self.apply\_or\_filters(or\_filters).
- If limit.
  - If (not isinstance(limit, int) or limit &lt; 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(limit, int) → limit &lt; 0.
    - Call the validation error handler Platform.throw(translated “Limit must be a non-negative integer”, TypeError).
  - Set self.query from self.query.limit(limit).
- If offset.
  - If (not isinstance(offset, int) or offset &lt; 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(offset, int) → offset &lt; 0.
    - Call the validation error handler Platform.throw(translated “Offset must be a non-negative integer”, TypeError).
  - If (not self.is\_postgres and not limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_postgres → not limit.
    - Set self.query from self.query.limit(MAX\_LIMIT).
  - Set self.query from self.query.offset(offset).
- If distinct.
  - Set self.query from self.query.distinct().
- If for\_update.
  - Set self.query from self.query.for\_update(skip\_locked = skip\_locked, nowait = not wait).
- If group\_by.
  - Evaluate self.apply\_group\_by(group\_by).
- If order\_by.
  - If not (self.is\_postgres and is\_select and (distinct or group\_by)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_postgres → is\_select → (distinct or group\_by).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in distinct → group\_by.
    - Evaluate self.apply\_order\_by(order\_by).
  - Otherwise.
    - Evaluate warnings.warn(“ORDER BY fields have been ignored because PostgreSQL requires them to appear in the SELECT list when using D …”, UserWarning, stacklevel = 2).
- Evaluate self.add\_permission\_conditions().
- If self.apply\_permissions.
  - Set self.query.\_doctype from self.doctype.
  - Set self.query.\_parent\_doctype from self.parent\_doctype.
  - Set self.query.\_fields\_list from getattr(self, “fields”, list()).
- If (getattr(self.query, “\_name\_field\_injected”, false) and (distinct or group\_by or any(generator of getattr(f, “is\_aggregate”, false) for f drawn from getattr(self, “fields”, list())))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(self.query, “\_name\_field\_injected”, false) → (distinct or group\_by or any(generator of getattr(f, “is\_aggregate”, false) for f drawn from getattr(self, “fields”, list()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in distinct → group\_by → any(generator of getattr(f, “is\_aggregate”, false) for f drawn from getattr(self, “fields”, list())).
  - Draw f from getattr(self, “fields”, list()).
  - Call the validation error handler Platform.throw(translated “Child table fields need 'name' in ′fields′ when using distinct or aggregate queries.”, exc = Platform.ValidationError).
- Set self.query.immutable from true.
- Return self.query.

**Methods declared on this owner** [check select permission](operations-078.md#op-4810aa43ab55db), [apply fields](operations-077.md#op-4dd11e2227227e), [apply filters](operations-077.md#op-b17efaeab4b8cd), [apply or filters](operations-077.md#op-d35f4362d07573), [apply group by](operations-078.md#op-a1d7c239525380), [apply order by](operations-078.md#op-b95ce370f25456), [add permission conditions](operations-079.md#op-229e64de04b29c).

**Values supplied outside this operation** selected callable from getattr(self, “fields”, list()), getattr(self.query, “\_name\_field\_injected”, false) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L108) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1083) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1222)

<a id="op-4dd11e2227227e"></a>
### Engine.apply fields

`operation_foundation_database_query_business_behavior_engine_apply_fields`

**Inputs** self, fields.

**Local steps**

- Set self.fields from self.parse\_fields(fields).
- For each field in self.fields.
  - If (isinstance(field, (Field bitwise or DynamicTableField)) and field.alias).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(field, (Field bitwise or DynamicTableField)) → field.alias.
    - Evaluate self.field\_aliases.add(field.alias).
- If self.apply\_permissions.
  - Set self.fields from self.apply\_field\_permissions().
- If not self.fields.
  - Set self.fields from list(self.table.name).
- Set self.query.\_child\_queries from list().
- Set self.query.\_name\_field\_injected from false.
- Set has\_select\_field from false.
- Set has\_child\_queries from false.
- Set has\_name\_field from false.
- Set selects\_own\_name from false.
- For each field in self.fields.
  - If isinstance(field, DynamicTableField).
    - Set self.query from field.apply\_select(self.query, engine = self).
    - Set has\_select\_field from true.
  - Otherwise.
    - If isinstance(field, ChildQuery).
      - Evaluate self.query.\_child\_queries.append(field).
      - Set has\_child\_queries from true.
    - Otherwise.
      - Set self.query from self.query.select(field).
      - Set has\_select\_field from true.
      - Set is\_source\_name from getattr(field, “name”, no value) equals “name”.
      - Set alias from getattr(field, “alias”, no value).
      - If (isinstance(field, Star) or (is\_source\_name and alias belongs to tuple(no value, “name”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(field, Star) → (is\_source\_name and alias belongs to tuple(no value, “name”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_source\_name → alias belongs to tuple(no value, “name”).
        - Set has\_name\_field from true.
      - If (isinstance(field, Star) or is\_source\_name).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(field, Star) → is\_source\_name.
        - Set selects\_own\_name from (selects\_own\_name or getattr(field, “table”, no value) belongs to tuple(no value, self.table)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in selects\_own\_name → getattr(field, “table”, no value) belongs to tuple(no value, self.table).
- If not has\_select\_field.
  - Set self.query from self.query.select(self.table.name).
  - Set has\_name\_field, selects\_own\_name from true.
- Set self.query.\_selects\_own\_name from selects\_own\_name.
- If (has\_child\_queries and not has\_name\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_child\_queries → not has\_name\_field.
  - Set self.query from self.query.select(self.table.name).
  - Set self.query.\_name\_field\_injected from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse fields](operations-078.md#op-f027552db926ff), [apply field permissions](operations-078.md#op-32ad8445abad8d).

**Values supplied outside this operation** selected callable from getattr(field, “name”, no value), getattr(field, “alias”, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L100) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1059) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1199)

<a id="op-b17efaeab4b8cd"></a>
### Engine.apply filters

`operation_foundation_database_query_business_behavior_engine_apply_filters`

**Inputs** self, filters = no value, collect = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with e — translated “Error parsing nested filters: {0}. {1}”.format(filters, str(e)) · ValueError(formatted text Invalid item type in filter list: {type(filter\_item).\_\_name\_\_}. Expected list, tuple, dict, or Criterion.) · ValueError(formatted text Unsupported filters type: {type(filters).\_\_name\_\_}).

**Local steps**

- If filters is identical to no value.
  - Return no value.
- If isinstance(filters, FilterValue).
  - Set filters from mapping(“name” → convert\_to\_value(filters)).
- If isinstance(filters, Criterion).
  - Set self.query from self.query.where(filters).
  - Return no value.
- If isinstance(filters, dict).
  - Evaluate self.apply\_dict\_filters(filters, collect = collect).
  - Return no value.
- If isinstance(filters, (list bitwise or tuple)).
  - If not filters.
    - Return no value.
  - If (len(filters) belongs to tuple(3, 4) and isinstance(filters at 1, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(filters) belongs to tuple(3, 4) → isinstance(filters at 1, str).
    - If (filters at 1.lower() belongs to OPERATOR\_MAP or filters at 1.lower() belongs to get\_additional\_filters\_from\_hooks()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters at 1.lower() belongs to OPERATOR\_MAP → filters at 1.lower() belongs to get\_additional\_filters\_from\_hooks().
      - Evaluate self.apply\_list\_filters(filters, collect = collect).
      - Return no value.
  - If all(generator of isinstance(d, FilterValue) for d drawn from filters).
    - Draw d from filters.
    - Evaluate self.apply\_dict\_filters(mapping(“name” → tuple(“in”, tuple(generator of convert\_to\_value(f) for f drawn from filters))), collect = collect).
      - Draw f from filters.
    - Return no value.
  - Set is\_nested\_structure from false.
  - Set potential\_nested\_list from filters.
  - Set is\_single\_group from false.
  - If (len(filters) equals 1 and isinstance(filters at 0, (list bitwise or tuple))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(filters) equals 1 → isinstance(filters at 0, (list bitwise or tuple)).
    - Set inner\_list from filters at 0.
    - If (len(inner\_list) ≥ 3 and isinstance(inner\_list at 1, str) and inner\_list at 1.lower() belongs to tuple(“and”, “or”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(inner\_list) ≥ 3 → isinstance(inner\_list at 1, str) → inner\_list at 1.lower() belongs to tuple(“and”, “or”).
      - Set is\_nested\_structure from true.
      - Set potential\_nested\_list from inner\_list.
      - Set is\_single\_group from true.
  - Otherwise.
    - If ((len(filters) ≥ 2 and isinstance(filters at 0, (list bitwise or tuple)) and any(generator of isinstance(item, str) for tuple(i, item) drawn from enumerate(filters) where (i modulo or format 2) differs fro ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (len(filters) ≥ 2 and isinstance(filters at 0, (list bitwise or tuple)) and any(generator of isinstance(item, str) for tuple(i, item) drawn from enumerate(filters) where (i modulo or format 2) differs from 0)) → (len(filters) &gt; 0 and isinstance(filters at 0, str)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(filters) ≥ 2 → isinstance(filters at 0, (list bitwise or tuple)) → any(generator of isinstance(item, str) for tuple(i, item) drawn from enumerate(filters) where (i modulo or format 2) differs from 0).
      - Draw tuple(i, item) from enumerate(filters), keep a combination only if ((i modulo or format 2) differs from 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(filters) &gt; 0 → isinstance(filters at 0, str).
      - Set is\_nested\_structure from true.
  - If is\_nested\_structure.
    - Attempt the following.
      - If is\_single\_group.
        - Set combined\_criterion from self.\_condition\_to\_criterion(potential\_nested\_list).
      - Otherwise.
        - Set combined\_criterion from self.\_parse\_nested\_filters(potential\_nested\_list).
      - If combined\_criterion.
        - If collect is distinct from no value.
          - Evaluate collect.append(combined\_criterion).
        - Otherwise.
          - Set self.query from self.query.where(combined\_criterion).
    - On failure (Exception) bound to e.
      - Call the validation error handler Platform.throw(translated “Error parsing nested filters: {0}. {1}”.format(filters, str(e)), exc = e).
  - Otherwise.
    - For each filter\_item in filters.
      - If isinstance(filter\_item, (list bitwise or tuple)).
        - Evaluate self.apply\_list\_filters(filter\_item, collect = collect).
      - Otherwise.
        - If isinstance(filter\_item, (dict bitwise or Criterion)).
          - Evaluate self.apply\_filters(filter\_item, collect = collect).
        - Otherwise.
          - Raise ValueError(formatted text Invalid item type in filter list: {type(filter\_item).\_\_name\_\_}. Expected list, tuple, dict, or Criterion.).
  - Return no value.
- Raise ValueError(formatted text Unsupported filters type: {type(filters).\_\_name\_\_}).

**Methods declared on this owner** [apply dict filters](operations-077.md#op-19e270f2709be2), [apply list filters](operations-077.md#op-d7f65f89e51914), [condition to criterion](operations-078.md#op-ef8b3850ecfd53), [parse nested filters](operations-078.md#op-f2b300f53c59e7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0139.json#L5575) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1061) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1201)

<a id="op-d35f4362d07573"></a>
### Engine.apply or filters

`operation_foundation_database_query_business_behavior_engine_apply_or_filters`

**Inputs** self, or\_filters = no value.

**Explicit results** no value.

**Local steps**

- If or\_filters is identical to no value.
  - Return no value.
- Set criteria from list().
- Evaluate self.apply\_filters(or\_filters, collect = criteria).
- If criteria.
  - Bind dependencies reduce.
  - Set combined from reduce(deferred anonymous expression, criteria).
  - Set self.query from self.query.where(combined).

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply filters](operations-077.md#op-b17efaeab4b8cd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0139.json#L7439) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1065) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1205)

<a id="op-d7f65f89e51914"></a>
### Engine.apply list filters

`operation_foundation_database_query_business_behavior_engine_apply_list_filters`

**Inputs** self, filter, collect = no value.

**Explicit failure paths** ValueError(formatted text Unknown filter format: {filter}).

**Local steps**

- Select the first matching pattern against filter.
  - Pattern sequence field, value.
    - Evaluate self.\_apply\_filter(field, value, collect = collect).
  - Pattern sequence field, operator, value.
    - Evaluate self.\_apply\_filter(field, value, operator, collect = collect).
  - Pattern sequence doctype, field, operator, value.
    - Evaluate self.\_apply\_filter(field, value, operator, doctype, collect = collect).
  - Pattern sequence doctype, field, operator, value, ….
    - Evaluate self.\_apply\_filter(field, value, operator, doctype, collect = collect).
  - Pattern any value.
    - Raise ValueError(formatted text Unknown filter format: {filter}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply filter](operations-078.md#op-7ca1cfbeb14d76).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0140.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1063) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1203)

<a id="op-19e270f2709be2"></a>
### Engine.apply dict filters

`operation_foundation_database_query_business_behavior_engine_apply_mapping_filters`

**Inputs** self, filters, collect = no value.

**Local steps**

- For each tuple(field, value) in filters.items().
  - Set operator from “=”.
  - If isinstance(value, (list bitwise or tuple)).
    - Set tuple(operator, value) from value.
  - Evaluate self.\_apply\_filter(field, value, operator, collect = collect).

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply filter](operations-078.md#op-7ca1cfbeb14d76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0140.json#L464) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1064) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1204)
