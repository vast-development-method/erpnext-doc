# Forms, reports and navigation · operations 52

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Registry

<a id="op-73e21aedc1bde0"></a>
### Build custom page registry

`operation_foundation_binding_foundation_studio_ai_agent_registry_build_custom_page_registry`

**Inputs** no declared parameters.

**Declared result** ToolRegistry.

**Explicit results** registry.

**Local steps**

- Bind dependencies files, scripts, variables.
- Set registry from \_build\_shared\_registry().
- Evaluate registry.extend(variables.TOOLS).
- Evaluate registry.extend(files.TOOLS).
- Evaluate registry.extend(scripts.TOOLS).
- Return registry.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1740)

<a id="op-b1e41634090c63"></a>
### Build standard page registry

`operation_foundation_binding_foundation_studio_ai_agent_registry_build_standard_page_registry`

**Inputs** no declared parameters.

**Declared result** ToolRegistry.

**Explicit results** registry.

**Local steps**

- Bind dependencies files, scripts.
- Set registry from \_build\_shared\_registry().
- Evaluate registry.extend(files.TOOLS).
- Evaluate registry.extend(scripts.TOOLS).
- Return registry.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1742)

<a id="op-5dd6cf768a5294"></a>
### Get tool registry for mode

`operation_foundation_binding_foundation_studio_ai_agent_registry_get_tool_registry_for_mode`

**Inputs** is\_standard.

**Declared result** ToolRegistry.

**Explicit results** build\_standard\_page\_registry() when is\_standard, otherwise build\_custom\_page\_registry().

**Local steps**

- Return build\_standard\_page\_registry() when is\_standard, otherwise build\_custom\_page\_registry().
  - Value choice on is\_standard — true gives build\_standard\_page\_registry(), false gives build\_custom\_page\_registry().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1743)

## Service · Reportview

<a id="op-714658bbf1b6cf"></a>
### Get

`operation_foundation_desk_reportview_business_behavior_get`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** data.

**Local steps**

- Set args from get\_form\_params().
- Set with\_link\_titles from sbool(args.pop(“with\_link\_titles”, false)).
- If is\_virtual\_doctype(args.doctype).
  - Set controller from get\_controller(args.doctype).
  - Set data from compress(Platform.call(controller.get\_list, args = args, expanded names args)).
- Otherwise.
  - Set data from compress(execute(expanded names args), args = args).
- If with\_link\_titles.
  - Evaluate send\_compressed\_link\_titles(args, data).
- Return data.

**Values supplied outside this operation** selected callable from get\_controller(args.doctype).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L56) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1382)

<a id="op-bf88f1747b5fef"></a>
### Send compressed link titles

`operation_foundation_binding_foundation_desk_reportview_send_compressed_link_titles`

**Inputs** args, data.

**Explicit results** no value.

**Local steps**

- If not isinstance(data, dict).
  - Return no value.
- Set field\_info from mapping of get\_result\_key(field, info) → info for tuple(field, info) drawn from zip(args.fields, get\_field\_info(args.fields, args.doctype), strict = true).
  - Draw tuple(field, info) from zip(args.fields, get\_field\_info(args.fields, args.doctype), strict = true).
- Set columns from list of field\_info.get(key) for key drawn from data at “keys”.
  - Draw key from data at “keys”.
- Evaluate send\_link\_titles(get\_report\_link\_titles(columns, data at “values”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L819)

<a id="op-927e3eec62f45d"></a>
### Get list

`operation_foundation_desk_reportview_business_behavior_get_list`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** data.

**Local steps**

- Set args from get\_form\_params().
- If is\_virtual\_doctype(args.doctype).
  - Set controller from get\_controller(args.doctype).
  - Set data from Platform.call(controller.get\_list, args = args, expanded names args).
- Otherwise.
  - Set data from execute(expanded names args).
- Return data.

**Values supplied outside this operation** selected callable from get\_controller(args.doctype).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L2034) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1388)

<a id="op-b1e980342d5a68"></a>
### Get count

`operation_foundation_desk_reportview_business_behavior_get_count`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Declared result** (int bitwise or no value).

**State and service calls** execute a supplied database query.

**Explicit results** Platform.call(controller.get\_count, args = args, expanded names args) · count\_query.run() at 0 at 0 · count.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies Count.
- Set args from get\_form\_params().
- If is\_virtual\_doctype(args.doctype).
  - Set controller from get\_controller(args.doctype).
  - Return Platform.call(controller.get\_count, args = args, expanded names args).
- Set args.distinct from sbool(args.distinct).
- Set args.limit from cint(args.limit).
- Set fieldname from formatted text ′tab{args.doctype}′.name.
- Set args.order\_by from no value.
- Set args.fields from list(fieldname).
- Set partial\_query from execute(expanded names args, run = 0).
- Set count\_query from Platform.qb.from\_(partial\_query).select(Count(“\*”)).
- If not args.limit.
  - Return count\_query.run() at 0 at 0.
- Set tuple(count\_sql, count\_params) from count\_query.walk().
- Set timeout\_clause from “SET STATEMENT max\_statement\_time=1 FOR ” when Platform.db.db\_type equals “mariadb”, otherwise empty text.
  - Value choice on Platform.db.db\_type equals “mariadb” — true gives “SET STATEMENT max\_statement\_time=1 FOR ”, false gives empty text.
- Attempt the following.
  - Set count from Platform.db.sql((timeout\_clause + count\_sql), count\_params) at 0 at 0.
- On failure (Exception) bound to e.
  - If Platform.db.is\_statement\_timeout(e).
    - Set count from no value.
  - Otherwise.
    - Propagate the active failure.
- If (count equals args.limit or count is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in count equals args.limit → count is identical to no value.
  - Evaluate Platform.local.response\_headers.set(“Cache-Control”, “private,max-age=600,stale-while-revalidate=10800”).
- Return count.

**Values supplied outside this operation** selected callable from get\_controller(args.doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L2260) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1383)

<a id="op-386387fd259bdb"></a>
### Execute

`operation_foundation_desk_reportview_business_behavior_execute`

**Inputs** doctype, remaining positional values args, remaining named values kwargs.

**Explicit results** DatabaseQuery(doctype).execute(expanded args, expanded names kwargs).

**Local steps**

- Return DatabaseQuery(doctype).execute(expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L3056) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1378)

<a id="op-c51c8e2ba9eb02"></a>
### Get form params

`operation_foundation_desk_reportview_business_behavior_get_form_parameters`

**Inputs** no declared parameters.

**Explicit results** data.

**Local steps**

- Set data from Platform.\_dict(Platform.local.form\_dict).
- Evaluate clean\_params(data).
- Evaluate validate\_args(data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L3144) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1387)

<a id="op-718c1f82722295"></a>
### Validate args

`operation_foundation_desk_reportview_business_behavior_validate_arguments`

**Inputs** data.

**Explicit results** data.

**Local steps**

- Evaluate parse\_json(data).
- Evaluate setup\_group\_by(data).
- Evaluate validate\_fields(data).
- If data.filters.
  - Evaluate validate\_filters(data, data.filters).
- If data.or\_filters.
  - Evaluate validate\_filters(data, data.or\_filters).
- Set data.strict from no value.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L3254) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1405)

<a id="op-13fe2bc1d8b14e"></a>
### Validate fields

`operation_foundation_desk_reportview_business_behavior_validate_fields`

**Inputs** data.

**Local steps**

- Set wildcard from update\_wildcard\_field\_param(data).
- For each field in list((data.fields or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.fields → list().
  - If isinstance(field, dict).
    - Continue with the next iteration or loop test.
  - Set fieldname from extract\_fieldnames(field) at 0.
  - If not fieldname.
    - Evaluate raise\_invalid\_field(fieldname).
  - If is\_standard(fieldname).
    - Continue with the next iteration or loop test.
  - Set tuple(meta, df) from get\_meta\_and\_docfield(fieldname, data).
  - If not df.
    - If wildcard.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - Evaluate raise\_invalid\_field(fieldname).
  - If (df.report\_hide and data.view equals “Report”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.report\_hide → data.view equals “Report”.
    - Evaluate data.fields.remove(field).
    - Continue with the next iteration or loop test.
  - If df.fieldname belongs to list of \_df.fieldname for \_df drawn from meta.get\_high\_permlevel\_fields().
    - Draw \_df from meta.get\_high\_permlevel\_fields().
    - If df.get(“permlevel”) does not belong to meta.get\_permlevel\_access(parenttype = data.doctype).
      - Evaluate data.fields.remove(field).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L3456) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1406)

<a id="op-1ac089dd3139bf"></a>
### Validate filters

`operation_foundation_desk_reportview_business_behavior_validate_filters`

**Inputs** data, filters.

**Local steps**

- If isinstance(filters, list).
  - For each condition in filters.
    - If len(condition) equals 3.
      - Set fieldname from condition at 0.
      - If is\_standard(fieldname).
        - Continue with the next iteration or loop test.
      - Set tuple(meta, df) from get\_meta\_and\_docfield(fieldname, data).
      - If not df.
        - Evaluate raise\_invalid\_field(condition at 0).
    - Otherwise.
      - Set fieldname from condition at 1.
      - If is\_standard(fieldname).
        - Continue with the next iteration or loop test.
      - Set meta from Platform.get\_meta(condition at 0).
      - If not meta.get\_field(fieldname).
        - Evaluate raise\_invalid\_field(fieldname).
- Otherwise.
  - For each fieldname in filters.
    - If is\_standard(fieldname).
      - Continue with the next iteration or loop test.
    - Set tuple(meta, df) from get\_meta\_and\_docfield(fieldname, data).
    - If not df.
      - Evaluate raise\_invalid\_field(fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L3997) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1407)

<a id="op-42a050c7dfd658"></a>
### Setup group by

`operation_foundation_desk_reportview_business_behavior_setup_group_by`

**Inputs** data.

**Explicit failure paths** validation helper — translated “Invalid aggregate function”.

**Local steps**

- If (data.group\_by and data.aggregate\_function).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.group\_by → data.aggregate\_function.
  - If data.aggregate\_function.lower() does not belong to tuple(“count”, “sum”, “avg”).
    - Call the validation error handler Platform.throw(translated “Invalid aggregate function”).
  - If Platform.db.has\_column(data.aggregate\_on\_doctype, data.aggregate\_on\_field).
    - Set field from formatted text ′tab{data.aggregate\_on\_doctype}′.′{data.aggregate\_on\_field}′.
    - Evaluate data.fields.append(mapping(data.aggregate\_function.upper() → field, “as” → “\_aggregate\_column”)).
  - Otherwise.
    - Evaluate raise\_invalid\_field(data.aggregate\_on\_field).
  - Evaluate data.pop(“aggregate\_on\_doctype”).
  - Evaluate data.pop(“aggregate\_on\_field”).
  - Evaluate data.pop(“aggregate\_function”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L64) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1403)

<a id="op-e2deae0b5db05b"></a>
### Raise invalid field

`operation_foundation_desk_reportview_business_behavior_raise_invalid_field`

**Inputs** fieldname.

**Explicit failure paths** validation helper with Platform.DataError — (translated “Field not permitted in query” + formatted text : {fieldname}).

**Local steps**

- Call the validation error handler Platform.throw((translated “Field not permitted in query” + formatted text : {fieldname}), Platform.DataError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L4878) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1398)

<a id="op-6e4418ef7b81b2"></a>
### Validate group by field

`operation_foundation_desk_reportview_business_behavior_validate_group_by_field`

**Inputs** raw, doctype.

**Local steps**

- If (not isinstance(raw, str) or not raw).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(raw, str) → not raw.
  - Evaluate raise\_invalid\_field(raw).
- Attempt the following.
  - Set tuple(field\_doctype, fieldname) from parse\_field(raw).
- On failure (ValueError).
  - Evaluate raise\_invalid\_field(raw).
- Set field\_doctype from (field\_doctype or doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field\_doctype → doctype.
- If not \_FIELDNAME\_RE.match(fieldname).
  - Evaluate raise\_invalid\_field(raw).
- Attempt the following.
  - Set has\_col from Platform.db.has\_column(field\_doctype, fieldname).
- On failure (Platform.db.TableMissingError).
  - Evaluate raise\_invalid\_field(raw).
- If not has\_col.
  - Evaluate raise\_invalid\_field(raw).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L4979) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1409)

<a id="op-77b20c30ffe0f8"></a>
### Validate group by args

`operation_foundation_desk_reportview_business_behavior_validate_group_by_arguments`

**Inputs** group\_by, doctype.

**Explicit failure paths** validation helper with Platform.DataError — translated “Invalid aggregate function: {0}”.format(raw\_func) · validation helper with Platform.DataError — translated “Invalid aggregate function: {0}”.format(func).

**Local steps**

- Set raw\_func from group\_by.get(“aggregate\_function”).
- If not isinstance(raw\_func, str).
  - Call the validation error handler Platform.throw(translated “Invalid aggregate function: {0}”.format(raw\_func), Platform.DataError).
- Set func from raw\_func.lower().
- If func does not belong to SUPPORTED\_AGGREGATE\_FUNCTIONS.
  - Call the validation error handler Platform.throw(translated “Invalid aggregate function: {0}”.format(func), Platform.DataError).
- Evaluate \_validate\_group\_by\_field(group\_by.get(“group\_by”, empty text), doctype).
- If func differs from “count”.
  - Evaluate \_validate\_group\_by\_field(group\_by.get(“aggregate\_on”, empty text), doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L5361) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1408)

<a id="op-43717394b56215"></a>
### Is standard

`operation_foundation_desk_reportview_business_behavior_is_standard`

**Inputs** fieldname.

**Explicit results** (fieldname belongs to default\_fields or fieldname belongs to optional\_fields or fieldname belongs to child\_table\_fields).

**Local steps**

- If “.” belongs to fieldname.
  - Set fieldname from fieldname.split(“.”) at 1.strip(“′”).
- Return (fieldname belongs to default\_fields or fieldname belongs to optional\_fields or fieldname belongs to child\_table\_fields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname belongs to default\_fields → fieldname belongs to optional\_fields → fieldname belongs to child\_table\_fields.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L5748) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1395)

<a id="op-03cb0deec55608"></a>
### Extract fieldnames

`operation_foundation_desk_reportview_business_behavior_extract_fieldnames`

**Inputs** field.

**Wrappers, in declaration order** lru\_cache(maxsize = 1024).

**Explicit results** list(field) · list(“\*”) · columns.

**Local steps**

- Bind dependencies Parser.
- Bind dependencies SPECIAL\_CHAR\_PATTERN.
- If not SPECIAL\_CHAR\_PATTERN.findall(field).
  - Return list(field).
- Set columns from Parser(formatted text select {field} from \_dummy).columns.
- If not columns.
  - Set f from field.lower().
  - If ((“count(” belongs to f or “sum(” belongs to f or “avg(” belongs to f) and “\*” belongs to f).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (“count(” belongs to f or “sum(” belongs to f or “avg(” belongs to f) → “\*” belongs to f.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “count(” belongs to f → “sum(” belongs to f → “avg(” belongs to f.
    - Return list(“\*”).
- Return columns.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L55) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1381)

<a id="op-66adb2e32467b5"></a>
### Get meta and docfield

`operation_foundation_desk_reportview_business_behavior_get_meta_and_record_field`

**Inputs** fieldname, data.

**Explicit results** tuple(meta, df).

**Local steps**

- Set tuple(parenttype, fieldname) from get\_parenttype\_and\_fieldname(fieldname, data).
- Set meta from Platform.get\_meta(parenttype).
- Set df from meta.get\_field(fieldname).
- Return tuple(meta, df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L6203) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1390)

<a id="op-fc5b277c4167d3"></a>
### Update wildcard field param

`operation_foundation_desk_reportview_business_behavior_update_wildcard_field_parameter`

**Inputs** data.

**Explicit results** true · false.

**Local steps**

- If ((isinstance(data.fields, str) and data.fields equals “\*”) or (isinstance(data.fields, (list bitwise or tuple)) and len(data.fields) equals 1 and data.fields at 0 equals “\*”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (isinstance(data.fields, str) and data.fields equals “\*”) → (isinstance(data.fields, (list bitwise or tuple)) and len(data.fields) equals 1 and data.fields at 0 equals “\*”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(data.fields, str) → data.fields equals “\*”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(data.fields, (list bitwise or tuple)) → len(data.fields) equals 1 → data.fields at 0 equals “\*”.
  - Set parent\_type from (data.parenttype or data.parent\_doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.parenttype → data.parent\_doctype.
  - Set data.fields from get\_permitted\_fields(data.doctype, parenttype = parent\_type, ignore\_virtual = true).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L6356) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1404)

<a id="op-28a6077d62bf0e"></a>
### Clean params

`operation_foundation_desk_reportview_business_behavior_clean_parameters`

**Inputs** data.

**Local steps**

- For each param in DISALLOWED\_PARAMS.
  - If param belongs to data.
    - Remove data at param.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L6649) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1373)

<a id="op-c8ef7f8eaa8d36"></a>
### Parse json

`operation_foundation_desk_reportview_business_behavior_parse_structured_data`

**Inputs** data.

**Local steps**

- If (filters bound to data.get(“filters”) and isinstance(filters, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters bound to data.get(“filters”) → isinstance(filters, str).
  - Set data at “filters” from json.loads(filters).
- If (applied\_filters bound to data.get(“applied\_filters”) and isinstance(applied\_filters, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in applied\_filters bound to data.get(“applied\_filters”) → isinstance(applied\_filters, str).
  - Set data at “applied\_filters” from json.loads(applied\_filters).
- If (or\_filters bound to data.get(“or\_filters”) and isinstance(or\_filters, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in or\_filters bound to data.get(“or\_filters”) → isinstance(or\_filters, str).
  - Set data at “or\_filters” from json.loads(or\_filters).
- If (fields bound to data.get(“fields”) and isinstance(fields, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields bound to data.get(“fields”) → isinstance(fields, str).
  - Set data at “fields” from list(“\*”) when fields equals “\*”, otherwise json.loads(fields).
    - Value choice on fields equals “\*” — true gives list(“\*”), false gives json.loads(fields).
- If isinstance(data.get(“docstatus”), str).
  - Set data at “docstatus” from json.loads(data at “docstatus”).
- If isinstance(data.get(“save\_user\_settings”), str).
  - Set data at “save\_user\_settings” from json.loads(data at “save\_user\_settings”).
- Otherwise.
  - Set data at “save\_user\_settings” from true.
- If isinstance(data.get(“start”), str).
  - Set data at “start” from cint(data.get(“start”)).
- If isinstance(data.get(“page\_length”), str).
  - Set data at “page\_length” from cint(data.get(“page\_length”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L61) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1397)

<a id="op-c613102dfc7e71"></a>
### Get parenttype and fieldname

`operation_foundation_desk_reportview_business_behavior_get_parenttype_and_fieldname`

**Inputs** field, data.

**Explicit results** tuple(parenttype, fieldname).

**Local steps**

- If “.” belongs to field.
  - Set parts from field.split(“.”).
  - Set parenttype from parts at 0.
  - Set fieldname from parts at 1.
  - Set df from Platform.get\_meta(data.doctype).get\_field(parenttype).
  - If (not df and parenttype.startswith(“tab”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not df → parenttype.startswith(“tab”).
    - Set parenttype from parenttype at slice 3 to no value.
  - Otherwise.
    - Set parenttype from df.options.
- Otherwise.
  - Set parenttype from data.doctype.
  - Set fieldname from field.strip(“′”).
- Return tuple(parenttype, fieldname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0213.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1391)

<a id="op-2bcf2e62a7ca3f"></a>
### Get result key

`operation_foundation_binding_foundation_desk_reportview_get_result_key`

**Inputs** field, info.

**Declared result** str.

**Explicit results** field.split(“ as ”, 1) at 1.strip(“ '′"”) · info.get(“fieldname”).

**Local steps**

- If (isinstance(field, str) and “ as ” belongs to field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(field, str) → “ as ” belongs to field.
  - Return field.split(“ as ”, 1) at 1.strip(“ '′"”).
- Return info.get(“fieldname”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L818)
