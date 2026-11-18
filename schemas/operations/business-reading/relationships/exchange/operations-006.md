# Integrations and service calls · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Doc

<a id="op-7c5a1218b84cbe"></a>
### Get quick filters

`operation_relationships_application_interface_record_business_behavior_get_quick_filters`

**Inputs** doctype, cached = true.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Global Settings” via exists · read “CRM Global Settings” via get\_value.

**State and service calls** call insert on options.

**Explicit results** quick\_filters.

**Local steps**

- Set meta from Platform.get\_meta(doctype, cached).
- Set quick\_filters from list().
- If global\_settings bound to Platform.db.exists(“CRM Global Settings”, mapping(“dt” → doctype, “type” → “Quick Filters”)).
  - Set \_quick\_filters from Platform.db.get\_value(“CRM Global Settings”, global\_settings, “json”).
  - Set \_quick\_filters from (json.loads(\_quick\_filters) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in json.loads(\_quick\_filters) → list().
  - Set fields from list().
  - For each filter in \_quick\_filters.
    - If filter equals “name”.
      - Evaluate fields.append(mapping(“label” → “Name”, “fieldname” → “name”, “fieldtype” → “Data”)).
    - Otherwise.
      - Set field from next(generator of f for f drawn from meta.fields where f.fieldname equals filter, no value).
        - Draw f from meta.fields, keep a combination only if (f.fieldname equals filter).
      - If field.
        - Evaluate fields.append(field).
- Otherwise.
  - Set fields from list of field for field drawn from meta.fields where field.in\_standard\_filter.
    - Draw field from meta.fields, keep a combination only if (field.in\_standard\_filter).
- For each field in fields.
  - Set options from field.get(“options”).
  - If (field.get(“fieldtype”) equals “Select” and options and isinstance(options, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.get(“fieldtype”) equals “Select” → options → isinstance(options, str).
    - Set options from options.split(whitespace '\\n').
    - Set options from list of mapping(“label” → option, “value” → option) for option drawn from options.
      - Draw option from options.
    - If not any(list of not option.get(“value”) for option drawn from options).
      - Draw option from options.
      - Evaluate options.insert(0, mapping(“label” → empty text, “value” → empty text)).
  - Evaluate quick\_filters.append(mapping(“label” → translated field.get(“label”), “fieldname” → field.get(“fieldname”), “fieldtype” → field.get(“fieldtype”), “options” → options)).
- If doctype equals “CRM Lead”.
  - Set quick\_filters from list of filter for filter drawn from quick\_filters where filter.get(“fieldname”) differs from “converted”.
    - Draw filter from quick\_filters, keep a combination only if (filter.get(“fieldname”) differs from “converted”).
- Return quick\_filters.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L3523) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L132) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L113)

<a id="op-3c8457bdd2c51c"></a>
### Update quick filters

`operation_relationships_application_interface_record_business_behavior_update_quick_filters`

**Inputs** quick\_filters, old\_filters, doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set quick\_filters from json.loads(quick\_filters).
- Set old\_filters from json.loads(old\_filters).
- Set new\_filters from list of filter for filter drawn from quick\_filters where filter does not belong to old\_filters.
  - Draw filter from quick\_filters, keep a combination only if (filter does not belong to old\_filters).
- Set removed\_filters from list of filter for filter drawn from old\_filters where filter does not belong to quick\_filters.
  - Draw filter from old\_filters, keep a combination only if (filter does not belong to quick\_filters).
- Evaluate create\_update\_global\_settings(doctype, quick\_filters).
- For each filter in removed\_filters.
  - Evaluate update\_in\_standard\_filter(filter, doctype, 0).
- For each filter in new\_filters.
  - Evaluate update\_in\_standard\_filter(filter, doctype, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L4703) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L141) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L122)

<a id="op-b8628cdc53929e"></a>
### Create update global settings

`operation_relationships_application_interface_record_business_behavior_create_update_global_settings`

**Inputs** doctype, quick\_filters.

**Record and data access** read “CRM Global Settings” via exists.

**State and service calls** request set\_value on “CRM Global Settings” · request new\_doc for “CRM Global Settings” · call insert on doc.

**Local steps**

- If global\_settings bound to Platform.db.exists(“CRM Global Settings”, mapping(“dt” → doctype, “type” → “Quick Filters”)).
  - Evaluate Platform.db.set\_value(“CRM Global Settings”, global\_settings, “json”, json.dumps(quick\_filters)).
- Otherwise.
  - Set doc from Platform.new\_doc(“CRM Global Settings”).
  - Set doc.dt from doctype.
  - Set doc.type from “Quick Filters”.
  - Set doc.json from json.dumps(quick\_filters).
  - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L5047) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L122) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L104)

<a id="op-49c0be462a1134"></a>
### Update in standard filter

`operation_relationships_application_interface_record_business_behavior_update_in_standard_filter`

**Inputs** fieldname, doctype, value.

**Record and data access** read “Property Setter” via exists.

**State and service calls** request set\_value on “Property Setter”.

**Local steps**

- If property\_name bound to Platform.db.exists(“Property Setter”, mapping(“doc\_type” → doctype, “field\_name” → fieldname, “property” → “in\_standard\_filter”)).
  - Evaluate Platform.db.set\_value(“Property Setter”, property\_name, “value”, value).
- Otherwise.
  - Evaluate make\_property\_setter(doctype, fieldname, “in\_standard\_filter”, value, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L5348) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L140) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L121)

<a id="op-3184aa42a9f615"></a>
### Apply comments filter

`operation_relationships_binding_crm_api_doc_apply_comments_filter`

**Inputs** doctype, filters.

**Record and data access** read “Comment” via get\_all · read doctype via get\_all.

**Explicit results** no value.

**Local steps**

- Set value from filters.get(“\_comments”).
- If (not isinstance(value, (list bitwise or tuple)) or len(value) differs from 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(value, (list bitwise or tuple)) → len(value) differs from 2.
  - Return no value.
- Set tuple(operator, text) from tuple(str(value at 0).lower(), value at 1).
- If operator does not belong to tuple(“like”, “not like”).
  - Return no value.
- Set commented from Platform.get\_all(“Comment”, filters = mapping(“reference\_doctype” → doctype, “comment\_type” → “Comment”, “content” → list(“like”, text)), pluck = “reference\_name”, distinct = true, limit\_page\_length = 0).
- Evaluate filters.pop(“\_comments”).
- If “name” does not belong to filters.
  - Set filters at “name” from list(“in” when operator equals “like”, otherwise “not in”, commented).
    - Value choice on operator equals “like” — true gives “in”, false gives “not in”.
  - Return no value.
- Set scoped from set(Platform.get\_all(doctype, filters = mapping(“name” → filters at “name”), pluck = “name”, limit\_page\_length = 0)).
- Set names from (scoped bitwise and set(commented)) when operator equals “like”, otherwise (scoped − set(commented)).
  - Value choice on operator equals “like” — true gives (scoped bitwise and set(commented)), false gives (scoped − set(commented)).
- Set filters at “name” from list(“in”, list(names)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L50) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L206) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L187)

<a id="op-f2d66dc4bc24d0"></a>
### Get data

`operation_relationships_application_interface_record_business_behavior_get_data`

**Inputs** doctype, filters, order\_by, page\_length = 20, page\_length\_count = 20, column\_field = no value, title\_field = no value, columns = no value, rows = no value, kanban\_columns = no value, kanban\_fields = no value, view = no value, default\_filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM View Settings” via exists · resolve a document from “CRM View Settings” via get\_doc · read doctype via get\_list · read field\_meta.options via get\_all · read “CRM View Settings” via get\_value.

**Explicit results** mapping(“data” → data, “columns” → columns, “rows” → rows, “fields” → fields, …).

**Local steps**

- Set custom\_view from false.
- Set filters from Platform.\_dict(filters).
- Set rows from Platform.parse\_json((rows or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → “&#91;&#93;”.
- Set columns from Platform.parse\_json((columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in columns → “&#91;&#93;”.
- Set kanban\_fields from Platform.parse\_json((kanban\_fields or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kanban\_fields → “&#91;&#93;”.
- Set kanban\_columns from Platform.parse\_json((kanban\_columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kanban\_columns → “&#91;&#93;”.
- Set custom\_view\_name from view.get(“custom\_view\_name”) when view, otherwise no value.
  - Value choice on view — true gives view.get(“custom\_view\_name”), false gives no value.
- Set view\_type from view.get(“view\_type”) when view, otherwise no value.
  - Value choice on view — true gives view.get(“view\_type”), false gives no value.
- Set group\_by\_field from view.get(“group\_by\_field”) when view, otherwise no value.
  - Value choice on view — true gives view.get(“group\_by\_field”), false gives no value.
- For each key in filters.
  - Set value from filters at key.
  - If isinstance(value, list).
    - If “@me” belongs to value.
      - Set value at value.index(“@me”) from Platform.session.user.
    - Otherwise.
      - If “%@me%” belongs to value.
        - Set index from list of i for tuple(i, v) drawn from enumerate(value) where v equals “%@me%”.
          - Draw tuple(i, v) from enumerate(value), keep a combination only if (v equals “%@me%”).
        - For each i in index.
          - Set value at i from ((“%” + Platform.session.user) + “%”).
  - Otherwise.
    - If value equals “@me”.
      - Set filters at key from Platform.session.user.
- If default\_filters.
  - Set default\_filters from Platform.parse\_json(default\_filters).
  - Evaluate filters.update(default\_filters).
- Evaluate apply\_comments\_filter(doctype, filters).
- Set is\_default from true.
- Set data from list().
- Set \_list from get\_controller(doctype).
- Set default\_rows from list().
- Set default\_column\_keys from list().
- If hasattr(\_list, “default\_list\_data”).
  - Set default\_list\_data from \_list.default\_list\_data().
  - Set default\_rows from default\_list\_data.get(“rows”).
  - Set default\_column\_keys from list of column.get(“key”) for column drawn from default\_list\_data.get(“columns”, list()).
    - Draw column from default\_list\_data.get(“columns”, list()).
- Set meta from Platform.get\_meta(doctype).
- If view\_type differs from “kanban”.
  - If (columns or rows).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in columns → rows.
    - Set custom\_view from true.
    - Set is\_default from false.
    - Set columns from Platform.parse\_json(columns).
    - Set rows from Platform.parse\_json(rows).
  - If not columns.
    - Set columns from list(mapping(“label” → “Name”, “type” → “Data”, “key” → “name”, “width” → “16rem”), mapping(“label” → “Last Modified”, “type” → “Datetime”, “key” → “modified”, “width” → “8rem”)).
  - If not rows.
    - Set rows from list(“name”).
  - Set default\_view\_filters from mapping(“dt” → doctype, “type” → (view\_type or “list”), “is\_standard” → 1, “user” → Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in view\_type → “list”.
  - If (not custom\_view and Platform.db.exists(“CRM View Settings”, default\_view\_filters)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not custom\_view → Platform.db.exists(“CRM View Settings”, default\_view\_filters).
    - Set list\_view\_settings from Platform.get\_doc(“CRM View Settings”, default\_view\_filters).
    - Set columns from Platform.parse\_json(list\_view\_settings.columns).
    - Set rows from Platform.parse\_json(list\_view\_settings.rows).
    - Set is\_default from false.
  - Otherwise.
    - If (not custom\_view or (is\_default and hasattr(\_list, “default\_list\_data”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not custom\_view → (is\_default and hasattr(\_list, “default\_list\_data”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_default → hasattr(\_list, “default\_list\_data”).
      - Set rows from default\_rows.
      - Set columns from \_list.default\_list\_data().get(“columns”).
  - Set visible\_columns from list().
  - For each column in columns.
    - Set key from column.get(“key”).
    - Set column\_meta from meta.get\_field(key).
    - If (column\_meta and column\_meta.get(“hidden”) and key does not belong to default\_column\_keys).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in column\_meta → column\_meta.get(“hidden”) → key does not belong to default\_column\_keys.
      - Continue with the next iteration or loop test.
    - If key does not belong to rows.
      - Evaluate rows.append(key).
    - Set column at “label” from translated column.get(“label”).
    - If (key equals “\_liked\_by” and column.get(“width”) equals “10rem”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in key equals “\_liked\_by” → column.get(“width”) equals “10rem”.
      - Set column at “width” from “50px”.
    - Evaluate visible\_columns.append(column).
  - Set columns from visible\_columns.
  - If (group\_by\_field and group\_by\_field does not belong to rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in group\_by\_field → group\_by\_field does not belong to rows.
    - Evaluate rows.append(group\_by\_field).
  - If (meta.track\_seen and “\_seen” does not belong to rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.track\_seen → “\_seen” does not belong to rows.
    - Evaluate rows.append(“\_seen”).
  - Set data from (Platform.get\_list(doctype, fields = rows, filters = filters, order\_by = order\_by, page\_length = page\_length) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_list(doctype, fields = rows, filters = filters, order\_by = order\_by, page\_length = page\_length) → list().
  - Set data from parse\_list\_data(data, doctype).
- If view\_type equals “kanban”.
  - If not rows.
    - Set rows from default\_rows.
  - If (not kanban\_columns and column\_field).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kanban\_columns → column\_field.
    - Set field\_meta from Platform.get\_meta(doctype).get\_field(column\_field).
    - If field\_meta.fieldtype equals “Link”.
      - Set kanban\_columns from Platform.get\_all(field\_meta.options, fields = list(“name”), order\_by = “modified asc”).
    - Otherwise.
      - If field\_meta.fieldtype equals “Select”.
        - Set kanban\_columns from list of mapping(“name” → option) for option drawn from field\_meta.options.split(whitespace '\\n').
          - Draw option from field\_meta.options.split(whitespace '\\n').
  - If not title\_field.
    - Set title\_field from “name”.
    - If hasattr(\_list, “default\_kanban\_settings”).
      - Set title\_field from \_list.default\_kanban\_settings().get(“title\_field”).
  - If title\_field does not belong to rows.
    - Evaluate rows.append(title\_field).
  - If not kanban\_fields.
    - Set kanban\_fields from list(“name”).
    - If hasattr(\_list, “default\_kanban\_settings”).
      - Set kanban\_fields from json.loads(\_list.default\_kanban\_settings().get(“kanban\_fields”)).
  - For each field in kanban\_fields.
    - If field does not belong to rows.
      - Evaluate rows.append(field).
  - For each kc in kanban\_columns.
    - Set column\_filters from mapping(column\_field → kc.get(“name”)).
    - Set order from kc.get(“order”).
    - If ((column\_field belongs to filters and filters.get(column\_field) differs from kc.get(“name”)) or kc.get(“delete”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (column\_field belongs to filters and filters.get(column\_field) differs from kc.get(“name”)) → kc.get(“delete”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in column\_field belongs to filters → filters.get(column\_field) differs from kc.get(“name”).
      - Set column\_data from list().
    - Otherwise.
      - Evaluate column\_filters.update(filters.copy()).
      - Set column\_page\_length from kc.get(“page\_length”, 20).
      - If order.
        - Set column\_data from get\_records\_based\_on\_order(doctype, rows, column\_filters, column\_page\_length, …).
      - Otherwise.
        - Set column\_data from Platform.get\_list(doctype, fields = rows, filters = convert\_filter\_to\_tuple(doctype, column\_filters), order\_by = order\_by, page\_length = column\_page\_length).
      - Set new\_filters from filters.copy().
      - Evaluate new\_filters.update(mapping(column\_field → kc.get(“name”))).
      - Set all\_count from Platform.get\_list(doctype, filters = convert\_filter\_to\_tuple(doctype, new\_filters), fields = list(COUNT\_NAME)) at 0.total\_count.
      - Set kc at “all\_count” from all\_count.
      - Set kc at “count” from len(column\_data).
      - Evaluate set\_activity\_counts(column\_data, doctype).
    - If order.
      - Set column\_data from sorted(column\_data, key = deferred anonymous expression).
    - Evaluate data.append(mapping(“column” → kc, “fields” → kanban\_fields, “data” → column\_data)).
- Set fields from Platform.get\_meta(doctype).fields.
- Set fields from list of field for field drawn from fields where field.fieldtype does not belong to no\_value\_fields.
  - Draw field from fields, keep a combination only if (field.fieldtype does not belong to no\_value\_fields).
- Set fields from list of mapping(“label” → translated field.label, “fieldtype” → field.fieldtype, “fieldname” → field.fieldname, “options” → field.options) for field drawn from fields where (field.label and field.fieldname).
  - Draw field from fields, keep a combination only if ((field.label and field.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.label → field.fieldname.
- Set std\_fields from list(mapping(“label” → “Name”, “fieldtype” → “Data”, “fieldname” → “name”), mapping(“label” → “Created On”, “fieldtype” → “Datetime”, “fieldname” → “creation”), mapping(“label” → “Last Modified”, “fieldtyp ….
- For each field in std\_fields.
  - If field.get(“fieldname”) does not belong to rows.
    - Evaluate rows.append(field.get(“fieldname”)).
  - If field does not belong to fields.
    - Set field at “label” from translated field at “label”.
    - Evaluate fields.append(field).
- If (not is\_default and custom\_view\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_default → custom\_view\_name.
  - Set is\_default from Platform.db.get\_value(“CRM View Settings”, custom\_view\_name, “load\_default\_columns”).
- If (group\_by\_field and view\_type equals “group\_by”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in group\_by\_field → view\_type equals “group\_by”.
  - Bind local operation get\_options for subsequent calls.
  - For each field in fields.
    - If field.get(“fieldname”) equals group\_by\_field.
      - Set group\_by\_field from mapping(“label” → field.get(“label”), “fieldname” → field.get(“fieldname”), “fieldtype” → field.get(“fieldtype”), “options” → get\_options(field.get(“fieldtype”), field.get(“options”))).
- Return mapping(“data” → data, “columns” → columns, “rows” → rows, “fields” → fields, …).

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L13) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L126) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L107)

<a id="op-29083a6063825c"></a>
### Get data.get options

`operation_relationships_application_interface_record_business_behavior_get_data_get_options`

**Inputs** type, options.

**Explicit results** list of option for option drawn from options.split(whitespace '\\n') · options.

**Local steps**

- If type equals “Select”.
  - Return list of option for option drawn from options.split(whitespace '\\n').
    - Draw option from options.split(whitespace '\\n').
- Otherwise.
  - Set has\_empty\_values from any(list of not d.get(group\_by\_field) for d drawn from data).
    - Draw d from data.
  - Set options from list(set(list of d.get(group\_by\_field) for d drawn from data)).
    - Draw d from data.
  - Set options from list of u for u drawn from options where u.
    - Draw u from options, keep a combination only if (u).
  - If has\_empty\_values.
    - Evaluate options.append(empty text).
  - If (order\_by and group\_by\_field belongs to order\_by).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in order\_by → group\_by\_field belongs to order\_by.
    - Set order\_by\_fields from order\_by.split(“,”).
    - Set order\_by\_fields from list of tuple(field.split(one space) at 0, field.split(one space) at 1) for field drawn from order\_by\_fields.
      - Draw field from order\_by\_fields.
    - If tuple(group\_by\_field, “asc”) belongs to order\_by\_fields.
      - Evaluate options.sort().
    - Otherwise.
      - If tuple(group\_by\_field, “desc”) belongs to order\_by\_fields.
        - Evaluate options.sort(reverse = true).
  - Otherwise.
    - Evaluate options.sort().
  - Return options.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0068.json#L1731) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L127) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L108)

<a id="op-2c6250c2beae7b"></a>
### Parse list data

`operation_relationships_application_interface_record_business_behavior_parse_list_data`

**Inputs** data, doctype.

**Explicit results** data.

**Local steps**

- Set \_list from get\_controller(doctype).
- If hasattr(\_list, “parse\_list\_data”).
  - Set data from \_list.parse\_list\_data(data).
- Return data.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0008.json#L6196) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L134) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L115)

<a id="op-59b90e4459c6fc"></a>
### Convert filter to tuple

`operation_relationships_application_interface_record_business_behavior_convert_filter_to_tuple`

**Inputs** doctype, filters.

**Explicit results** filters.

**Local steps**

- If isinstance(filters, dict).
  - Set filters\_items from filters.items().
  - Set filters from list().
  - For each tuple(key, value) in filters\_items.
    - Evaluate filters.append(make\_filter\_tuple(doctype, key, value)).
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0008.json#L6324) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L121) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L103)

<a id="op-4d8dd09424db70"></a>
### Get records based on order

`operation_relationships_application_interface_record_business_behavior_get_records_based_on_order`

**Inputs** doctype, rows, filters, page\_length, order.

**Record and data access** read doctype via get\_list.

**Explicit results** records.

**Local steps**

- Set records from list().
- Set filters from convert\_filter\_to\_tuple(doctype, filters).
- Set in\_filters from filters.copy().
- Evaluate in\_filters.append(list(doctype, “name”, “in”, order at slice no value to page\_length)).
- Set records from Platform.get\_list(doctype, fields = rows, filters = in\_filters, order\_by = “creation desc”, page\_length = page\_length).
- If len(records) &lt; page\_length.
  - Set not\_in\_filters from filters.copy().
  - Evaluate not\_in\_filters.append(list(doctype, “name”, “not in”, order)).
  - Set remaining\_records from Platform.get\_list(doctype, fields = rows, filters = not\_in\_filters, order\_by = “creation desc”, page\_length = (page\_length − len(records))).
  - For each record in remaining\_records.
    - Evaluate records.append(record).
- Return records.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0008.json#L6502) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L133) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L114)

<a id="op-a1454ecf7133ab"></a>
### Remove assignments

`operation_relationships_application_interface_record_business_behavior_remove_assignments`

**Inputs** doctype, name, assignees.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- Set assignees from Platform.parse\_json(assignees).
- If not assignees.
  - Return no value.
- For each assign\_to in assignees.
  - Evaluate set\_status(doctype, name, todo = no value, assign\_to = assign\_to, status = “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L15) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L135) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L116)

<a id="op-6eb8b0be68c4ee"></a>
### Add seen

`operation_relationships_application_interface_record_business_behavior_add_seen`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“read”).
- Evaluate doc.add\_seen().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0008.json#L7226) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L120) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L102)

<a id="op-2732c8052e1af4"></a>
### Get assigned users

`operation_relationships_application_interface_record_business_behavior_get_assigned_users`

**Inputs** doctype, name, default\_assigned\_to = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** get\_assignees(doctype, name, default\_assigned\_to).

**Local steps**

- Evaluate Platform.get\_doc(doctype, name).check\_permission(“read”).
- Return get\_assignees(doctype, name, default\_assigned\_to).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L12) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L124) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L106)

<a id="op-272e9148545e64"></a>
### Get assignees

`operation_relationships_binding_crm_api_doc_get_assignees`

**Inputs** doctype, name, default\_assigned\_to = no value.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** users.

**Local steps**

- Set assigned\_users from Platform.get\_all(“ToDo”, fields = list(“allocated\_to”), filters = mapping(“reference\_type” → doctype, “reference\_name” → name, “status” → tuple(“not in”, tuple(“Closed”, “Cancelled”))), pluck = “allocated\_to”).
- Set users from list(set(assigned\_users)).
- If (not users and default\_assigned\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not users → default\_assigned\_to.
  - Set users from list(default\_assigned\_to).
- Return users.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L51) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L207) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L188)

<a id="op-b5243498abbf5e"></a>
### Get fields

`operation_relationships_application_interface_record_business_behavior_get_fields`

**Inputs** doctype, allow\_all\_fieldtypes = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_fields.

**Local steps**

- Set not\_allowed\_fieldtypes from list(expanded list(Platform.model.no\_value\_fields), “Read Only”).
- If allow\_all\_fieldtypes.
  - Set not\_allowed\_fieldtypes from list().
- Set fields from Platform.get\_meta(doctype).fields.
- Set \_fields from list().
- For each field in fields.
  - If (field.fieldtype does not belong to not\_allowed\_fieldtypes and field.fieldname).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype does not belong to not\_allowed\_fieldtypes → field.fieldname.
    - Evaluate \_fields.append(field).
- Return \_fields.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0009.json#L338) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L128) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L109)

<a id="op-66d9db6fe19c7b"></a>
### Set activity counts

`operation_relationships_binding_crm_api_doc_set_activity_counts`

**Inputs** rows, doctype.

**Explicit results** rows.

**Local steps**

- Set names from list of d.get(“name”) for d drawn from rows.
  - Draw d from rows.
- If not names.
  - Return rows.
- Bind local operation count\_by for subsequent calls.
- Set email\_counts from count\_by(“Communication”, “reference\_name”, mapping(“communication\_type” → list(“in”, list(“Communication”, “Automated Message”)))).
- Set comment\_counts from count\_by(“Comment”, “reference\_name”, mapping(“comment\_type” → “Comment”)).
- Set task\_counts from count\_by(“CRM Task”, “reference\_docname”).
- Set note\_counts from count\_by(“FCRM Note”, “reference\_docname”).
- For each d in rows.
  - Set name from d.get(“name”).
  - Set d at “\_email\_count” from email\_counts.get(name, 0).
  - Set d at “\_comment\_count” from comment\_counts.get(name, 0).
  - Set d at “\_task\_count” from task\_counts.get(name, 0).
  - Set d at “\_note\_count” from note\_counts.get(name, 0).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L53) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L209) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L190)

<a id="op-b2d712e909a030"></a>
### Set activity counts.count by

`operation_relationships_binding_crm_api_doc_set_activity_counts_count_by`

**Inputs** activity\_doctype, link\_field, filters = no value.

**Record and data access** read activity\_doctype via get\_all.

**Explicit results** mapping of r.get(link\_field) → r.total\_count for r drawn from result.

**Local steps**

- Set result from Platform.get\_all(activity\_doctype, filters = mapping(“reference\_doctype” → doctype, link\_field → list(“in”, names), expand (filters or mapping())), fields = list(link\_field, COUNT\_NAME), group\_by = link\_field).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Return mapping of r.get(link\_field) → r.total\_count for r drawn from result.
  - Draw r from result.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L54) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L210) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L191)

<a id="op-af306dd461fda8"></a>
### Get linked docs of document

`operation_relationships_application_interface_record_business_behavior_get_linked_records_of_document`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** list() · list of d for d drawn from get\_linked\_docs\_data(doc) where Platform.has\_permission(d at “reference\_doctype”, “read”, d at “reference\_docname”).

**Local steps**

- Attempt the following.
  - Set doc from Platform.get\_doc(doctype, docname).
- On failure (Platform.DoesNotExistError).
  - Return list().
- Evaluate doc.check\_permission(“read”).
- Return list of d for d drawn from get\_linked\_docs\_data(doc) where Platform.has\_permission(d at “reference\_doctype”, “read”, d at “reference\_docname”).
  - Draw d from get\_linked\_docs\_data(doc), keep a combination only if (Platform.has\_permission(d at “reference\_doctype”, “read”, d at “reference\_docname”)).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”), Platform.has\_permission(d at “reference\_doctype”, “read”, d at “reference\_docname”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L14) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L131) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L112)

<a id="op-7978021d4b74fe"></a>
### Get linked docs data

`operation_relationships_binding_crm_api_doc_get_linked_docs_data`

**Inputs** doc.

**Record and data access** resolve a document from doc at “reference\_doctype” via get\_doc.

**Explicit results** docs\_data.

**Local steps**

- Set linked\_docs from get\_linked\_docs(doc).
- Set dynamic\_linked\_docs from get\_dynamic\_linked\_docs(doc).
- Evaluate linked\_docs.extend(dynamic\_linked\_docs).
- Set linked\_docs from list(mapping of doc at “reference\_docname” → doc for doc drawn from linked\_docs.values()).
  - Draw doc from linked\_docs.
- Set docs\_data from list().
- For each doc in linked\_docs.
  - If (not doc.get(“reference\_doctype”) or not doc.get(“reference\_docname”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.get(“reference\_doctype”) → not doc.get(“reference\_docname”).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set data from Platform.get\_doc(doc at “reference\_doctype”, doc at “reference\_docname”).
  - On failure (tuple(Platform.DoesNotExistError, Platform.ValidationError)).
    - Continue with the next iteration or loop test.
  - Set title from data.get(“title”).
  - If data.doctype equals “CRM Call Log”.
    - Set title from formatted text Call from {data.get(“from”)} to {data.get(“to”)}.
  - If data.doctype equals “CRM Deal”.
    - Set title from data.get(“organization”).
  - If data.doctype equals “CRM Notification”.
    - Set title from data.get(“message”).
  - Evaluate docs\_data.append(mapping(“doc” → data.doctype, “title” → (title or data.get(“name”)), “reference\_docname” → doc at “reference\_docname”, “reference\_doctype” → doc at “reference\_doctype”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → data.get(“name”).
- Return docs\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L52) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L208) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L189)

<a id="op-6603064ec09ce5"></a>
### Remove doc link

`operation_relationships_application_interface_record_business_behavior_remove_record_link`

**Inputs** doctype, docname.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call save on linked\_doc\_data.

**Explicit results** no value.

**Local steps**

- If (not doctype or not docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not docname.
  - Return no value.
- Attempt the following.
  - Set linked\_doc\_data from Platform.get\_doc(doctype, docname).
  - If doctype equals “CRM Notification”.
    - Set delete\_notification\_type from mapping(“notification\_type\_doctype” → empty text, “notification\_type\_doc” → empty text).
    - Set delete\_references from mapping(“reference\_doctype” → empty text, “reference\_name” → empty text).
    - If linked\_doc\_data.get(“notification\_type\_doctype”) equals linked\_doc\_data.get(“reference\_doctype”).
      - Evaluate delete\_references.update(delete\_notification\_type).
    - Evaluate linked\_doc\_data.update(delete\_references).
  - Otherwise.
    - Evaluate linked\_doc\_data.update(mapping(“reference\_doctype” → empty text, “reference\_docname” → empty text)).
  - Evaluate linked\_doc\_data.save(ignore\_permissions = true).
- On failure (tuple(Platform.DoesNotExistError, Platform.ValidationError)).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0009.json#L2172) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L138) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L119)

<a id="op-04693dc4be74a6"></a>
### Remove contact link

`operation_relationships_application_interface_record_business_behavior_remove_contact_link`

**Inputs** doctype, docname.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call save on linked\_doc\_data.

**Explicit results** no value.

**Local steps**

- If (not doctype or not docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not docname.
  - Return no value.
- Attempt the following.
  - Set linked\_doc\_data from Platform.get\_doc(doctype, docname).
  - Evaluate linked\_doc\_data.update(mapping(“contact” → no value, “contacts” → list())).
  - Evaluate linked\_doc\_data.save(ignore\_permissions = true).
- On failure (tuple(Platform.DoesNotExistError, Platform.ValidationError)).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0009.json#L2629) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L136) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L117)

<a id="op-099b77a30fe252"></a>
### Remove linked doc reference

`operation_relationships_application_interface_record_business_behavior_remove_linked_record_reference`

**Inputs** items, remove\_contact = false, delete = false.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request delete\_doc for item at “doctype”.

**Explicit results** “success”.

**Local steps**

- If isinstance(items, str).
  - Set items from Platform.parse\_json(items).
- For each item in items.
  - If (not item.get(“doctype”) or not item.get(“docname”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(“doctype”) → not item.get(“docname”).
    - Continue with the next iteration or loop test.
  - If not Platform.has\_permission(item at “doctype”, “write”, item at “docname”).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - If remove\_contact.
      - Evaluate remove\_contact\_link(item at “doctype”, item at “docname”).
    - Otherwise.
      - Evaluate remove\_doc\_link(item at “doctype”, item at “docname”).
    - If delete.
      - Evaluate Platform.delete\_doc(item at “doctype”, item at “docname”).
  - On failure (tuple(Platform.DoesNotExistError, Platform.ValidationError)).
    - Continue with the next iteration or loop test.
- Return “success”.

**Values supplied outside this operation** effective access from Platform.has\_permission(item at “doctype”, “write”, item at “docname”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0009.json#L2857) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L137) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L118)

<a id="op-fa62a427dd0e25"></a>
### Delete bulk docs

`operation_relationships_application_interface_record_business_behavior_delete_bulk_records`

**Inputs** doctype, items, delete\_linked = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc.

**State and service calls** enqueue with “Platform.desk.reportview.delete\_bulk”.

**Explicit results** “success”.

**Explicit failure paths** validation helper — translated “Doctype is required” · validation helper — translated “Items are required” · validation helper — translated “Items must be a list”.

**Local steps**

- Bind dependencies delete\_bulk.
- If not doctype.
  - Call the validation error handler Platform.throw(translated “Doctype is required”).
- If not items.
  - Call the validation error handler Platform.throw(translated “Items are required”).
- Set items from Platform.parse\_json(items).
- If not isinstance(items, list).
  - Call the validation error handler Platform.throw(translated “Items must be a list”).
- For each doc in items.
  - Attempt the following.
    - If not Platform.db.exists(doctype, doc).
      - Evaluate Platform.log\_error(formatted text Document {doctype} {doc} does not exist, “Bulk Delete Error”).
      - Continue with the next iteration or loop test.
    - Set linked\_docs from get\_linked\_docs\_data(Platform.get\_doc(doctype, doc)).
    - For each linked\_doc in linked\_docs.
      - If (not linked\_doc.get(“reference\_doctype”) or not linked\_doc.get(“reference\_docname”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not linked\_doc.get(“reference\_doctype”) → not linked\_doc.get(“reference\_docname”).
        - Continue with the next iteration or loop test.
      - Evaluate remove\_linked\_doc\_reference(list(mapping(“doctype” → linked\_doc at “reference\_doctype”, “docname” → linked\_doc at “reference\_docname”)), remove\_contact = doctype equals “Contact”, delete = delete\_linked).
  - On failure (Exception) bound to e.
    - Evaluate Platform.log\_error(formatted text Error processing linked docs for {doctype} {doc}: {e}, “Bulk Delete Error”).
- If len(items) &gt; 10.
  - Evaluate Platform.enqueue(“Platform.desk.reportview.delete\_bulk”, doctype = doctype, items = items).
- Otherwise.
  - Evaluate delete\_bulk(doctype, items).
- Return “success”.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.desk.reportview.delete\_bulk”, doctype = doctype, items = items).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L11) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L123) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L105)

## Service · Doc share

<a id="op-4cd96bfc1e1621"></a>
### Sync

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_sync`

**Inputs** doc.

**Declared result** MirrorSync.

**Explicit results** MirrorSync(doc, “share\_doctype”, “share\_name”, extra\_mirror\_flags = mapping(“ignore\_share\_permission” → true)).

**Local steps**

- Return MirrorSync(doc, “share\_doctype”, “share\_name”, extra\_mirror\_flags = mapping(“ignore\_share\_permission” → true)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L7224) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1300) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1276)
