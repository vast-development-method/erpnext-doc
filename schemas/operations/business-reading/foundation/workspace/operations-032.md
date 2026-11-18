# Forms, reports and navigation · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Grid import

<a id="op-245082c6253a8d"></a>
### Parse google sheet

`operation_foundation_binding_foundation_desk_form_grid_import_parse_google_sheet`

**Inputs** doctype, url, docname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at list at str.

**Explicit results** list of list of stringify(value) for value drawn from row for row drawn from (rows or list()).

**Local steps**

- Evaluate check\_permission(doctype, “write”, docname).
- Set content from get\_csv\_content\_from\_google\_sheets(url).
- Set rows from read\_csv\_content(content).
- Return list of list of stringify(value) for value drawn from row for row drawn from (rows or list()).
  - Draw row from (rows or list()).
  - Draw value from row.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().

**Values supplied outside this operation** effective access from check\_permission(doctype, “write”, docname).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L782)

<a id="op-006967da110304"></a>
### Get column map

`operation_foundation_binding_foundation_desk_form_grid_import_get_column_map`

**Inputs** doctype, fieldname, headers, docname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(int, str).

**Explicit results** column\_map.

**Local steps**

- Set child\_doctype from get\_child\_doctype(doctype, fieldname, docname).
- Set writable from get\_writable\_fields(doctype, child\_doctype).
- Set column\_map from mapping().
- For each tuple(i, header) in enumerate((Platform.parse\_json(headers) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(headers) → list().
  - Set header from cstr(header).strip().
  - If not header.
    - Continue with the next iteration or loop test.
  - Set df from get\_df\_for\_column\_header(child\_doctype, header).
  - If (df and df.fieldname belongs to writable).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldname belongs to writable.
    - Set column\_map at i from df.fieldname.
- Return column\_map.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L771)

<a id="op-8c4eabf25655f5"></a>
### Validate rows

`operation_foundation_binding_foundation_desk_form_grid_import_validate_rows`

**Inputs** doctype, fieldname, headers, rows, column\_map, docname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at dict.

**Explicit results** warnings.

**Explicit failure paths** validation helper — translated “Cannot import table with more than {0} rows.”.format(MAX\_IMPORT\_ROWS).

**Local steps**

- Set child\_doctype from get\_child\_doctype(doctype, fieldname, docname).
- Set rows from Platform.parse\_json(rows).
- If len(rows) &gt; MAX\_IMPORT\_ROWS.
  - Call the validation error handler Platform.throw(translated “Cannot import table with more than {0} rows.”.format(MAX\_IMPORT\_ROWS), title = translated “Too Many Rows”).
- Set writable from get\_writable\_fields(doctype, child\_doctype).
- Set meta from Platform.get\_meta(child\_doctype).
- Set date\_format from dateformats.get(get\_user\_date\_format(), “%Y-%m-%d”).
- Set columns from list of Platform.\_dict(index = int(i), column\_number = (int(i) + 1), df = meta.get\_field(field), date\_format = date\_format) for tuple(i, field) drawn from Platform.parse\_json(column\_map).items() where (fie ….
  - Draw tuple(i, field) from Platform.parse\_json(column\_map).items(), keep a combination only if ((field belongs to writable and meta.get\_field(field))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field belongs to writable → meta.get\_field(field).
- Set header from Platform.\_dict(columns = Platform.parse\_json(headers)).
- Set invalid\_cells from get\_invalid\_link\_select\_cells(columns, rows, child\_doctype).
- Set warnings from list().
- For each tuple(index, data) in enumerate(rows).
  - Set row from GridImportRow(index, data, child\_doctype, header, import\_type = no value).
  - For each col in columns.
    - Set value from cstr(get\_item\_at\_index(data, col.index)).strip().
    - If not value.
      - Continue with the next iteration or loop test.
    - If message bound to invalid\_cells.get(tuple(index, col.index)).
      - Evaluate row.warnings.append(mapping(“col” → col.index, “message” → message)).
      - Continue with the next iteration or loop test.
    - Set seen from len(row.warnings).
    - Evaluate row.validate\_value(value, col).
    - For each warning in row.warnings at slice seen to no value.
      - Set warning at “col” from col.index.
  - Evaluate warnings.extend(generator of mapping(“row” → index, “col” → warning.get(“col”), “blocking” → warning.get(“col”) is distinct from no value, “message” → html.unescape(strip\_html(warning at “message”))) for w ….
    - Draw warning from row.warnings.
- Return warnings.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L784)

<a id="op-973951eb0c87d9"></a>
### Get invalid link select cells

`operation_foundation_binding_foundation_desk_form_grid_import_get_invalid_link_select_cells`

**Inputs** columns, rows, child\_doctype.

**Declared result** dict at tuple(tuple at tuple(int, int), str).

**Explicit results** invalid\_cells.

**Local steps**

- Set invalid\_cells from mapping().
- For each col in columns.
  - If col.df.fieldtype does not belong to tuple(“Link”, “Select”).
    - Continue with the next iteration or loop test.
  - Set column from Platform.\_dict(df = col.df, doctype = child\_doctype, column\_values = list of cstr(get\_item\_at\_index(data, nested operand in the contract.index)).strip() for data drawn from rows, value\_row\_numbers = list(r ….
    - Draw data from rows.
  - For each item in get\_invalid\_link\_select\_items(column).
    - Set message from get\_invalid\_value\_message(item at “source”, col.df).
    - For each index in item at “rows”.
      - Set invalid\_cells at tuple(index, col.index) from message.
- Return invalid\_cells.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L773)

<a id="op-d5d639acf22cbd"></a>
### Get invalid value message

`operation_foundation_binding_foundation_desk_form_grid_import_get_invalid_value_message`

**Inputs** value, df.

**Declared result** str.

**Explicit results** translated “"{0}" is not a valid {1}”.format(value, translated df.label) · translated “"{0}" is not valid. Allowed: {1}”.format(value, “, ”.join(get\_select\_options(df))).

**Local steps**

- Set value from html.escape(value).
- If df.fieldtype equals “Link”.
  - Return translated “"{0}" is not a valid {1}”.format(value, translated df.label).
- Return translated “"{0}" is not valid. Allowed: {1}”.format(value, “, ”.join(get\_select\_options(df))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L774)

<a id="op-22e467c754d145"></a>
### Grid Import Row.validate value

`operation_foundation_binding_foundation_desk_form_grid_import_gridimportrow_validate_value`

**Inputs** self, value, col.

**Explicit results** value · no value · super().validate\_value(value, col).

**Local steps**

- If (col.df.fieldtype equals “Duration” and value.isdigit()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df.fieldtype equals “Duration” → value.isdigit().
  - Return value.
- If (col.df.fieldtype equals “Phone” and not self.is\_valid\_phone(value, col.df)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df.fieldtype equals “Phone” → not self.is\_valid\_phone(value, col.df).
  - Return no value.
- Return super().validate\_value(value, col).

**Methods declared on this owner** [is valid phone](operations-032.md#op-3ec51a78b9b858).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L779)

<a id="op-3ec51a78b9b858"></a>
### Grid Import Row.is valid phone

`operation_foundation_binding_foundation_desk_form_grid_import_gridimportrow_is_valid_phone`

**Inputs** self, value, df.

**Explicit results** false · true.

**Local steps**

- Attempt the following.
  - Evaluate validate\_phone\_number\_with\_country\_code(value, translated df.label).
- On failure (Platform.InvalidPhoneNumberError) bound to e.
  - Evaluate Platform.clear\_last\_message().
  - Set message from str(e) when value.startswith(“+”), otherwise translated “"{0}" needs a country code, like {1}.”.format(value, “+91-9876543210”).
    - Value choice on value.startswith(“+”) — true gives str(e), false gives translated “"{0}" needs a country code, like {1}.”.format(value, “+91-9876543210”).
  - Evaluate self.warnings.append(mapping(“row” → self.row\_number, “message” → message)).
  - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L778)

<a id="op-e5acb071a244be"></a>
### Grid Import Row.get date

`operation_foundation_binding_foundation_desk_form_grid_import_gridimportrow_get_date`

**Inputs** self, value, column.

**Explicit results** parsed.date() when isinstance(parsed, datetime.datetime), otherwise parsed.

**Local steps**

- Set parsed from parse\_datetime(value, tuple(column.date\_format, “%Y-%m-%d”, “%Y-%m-%d %H:%M:%S”)).
- Return parsed.date() when isinstance(parsed, datetime.datetime), otherwise parsed.
  - Value choice on isinstance(parsed, datetime.datetime) — true gives parsed.date(), false gives parsed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L776)

<a id="op-30038f499d2580"></a>
### Grid Import Row.get datetime

`operation_foundation_binding_foundation_desk_form_grid_import_gridimportrow_get_datetime`

**Inputs** self, value, column.

**Explicit results** parse\_datetime(value, tuple(formatted text {column.date\_format} {time\_format}, “%Y-%m-%d %H:%M:%S”)).

**Local steps**

- Set time\_format from nested operand in the contract().replace(“HH”, “%H”).replace(“mm”, “%M”).replace(“ss”, “%S”).
- Return parse\_datetime(value, tuple(formatted text {column.date\_format} {time\_format}, “%Y-%m-%d %H:%M:%S”)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L777)

<a id="op-5211ef1564c967"></a>
### Parse datetime

`operation_foundation_binding_foundation_desk_form_grid_import_parse_datetime`

**Inputs** value, formats.

**Declared result** (datetime.datetime bitwise or str).

**Explicit results** datetime.datetime.strptime(value, date\_format) · value.

**Local steps**

- For each date\_format in formats.
  - Attempt the following.
    - Return datetime.datetime.strptime(value, date\_format).
  - On failure (ValueError).
    - Continue with the next iteration or loop test.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L780)

<a id="op-9e91ead7328414"></a>
### Check permission

`operation_foundation_binding_foundation_desk_form_grid_import_check_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, ptype, docname.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L767)

<a id="op-c042fd1daae504"></a>
### Get child doctype

`operation_foundation_binding_foundation_desk_form_grid_import_get_child_doctype`

**Inputs** doctype, fieldname, docname = no value.

**Declared result** str.

**Explicit results** table\_df.options.

**Explicit failure paths** validation helper — translated “{0} is not a table field”.format(Platform.bold(fieldname)).

**Local steps**

- Evaluate check\_permission(doctype, “write”, docname).
- Set table\_df from Platform.get\_meta(doctype).get\_field(fieldname).
- If (not table\_df or table\_df.fieldtype does not belong to table\_fields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not table\_df → table\_df.fieldtype does not belong to table\_fields.
  - Call the validation error handler Platform.throw(translated “{0} is not a table field”.format(Platform.bold(fieldname))).
- Return table\_df.options.

**Values supplied outside this operation** effective access from check\_permission(doctype, “write”, docname).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L770)

<a id="op-96a72460bc10e3"></a>
### Get writable fields

`operation_foundation_binding_foundation_desk_form_grid_import_get_writable_fields`

**Inputs** doctype, child\_doctype.

**Declared result** set at str.

**Explicit results** writable.

**Local steps**

- Set permitted from set(get\_permitted\_fields(child\_doctype, parenttype = doctype, permission\_type = “write”)).
- Set writable from set of df.fieldname for df drawn from Platform.get\_meta(child\_doctype).fields where (df.fieldtype does not belong to no\_value\_fields and not df.is\_virtual and df.fieldname belongs to permitted).
  - Draw df from Platform.get\_meta(child\_doctype).fields, keep a combination only if ((df.fieldtype does not belong to no\_value\_fields and not df.is\_virtual and df.fieldname belongs to permitted)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → not df.is\_virtual → df.fieldname belongs to permitted.
- Evaluate writable.add(“name”).
- Return writable.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L775)

<a id="op-284e8b1efb4cb0"></a>
### Get extension

`operation_foundation_binding_foundation_desk_form_grid_import_get_extension`

**Inputs** filename.

**Declared result** str.

**Explicit results** (filename or empty text).rsplit(“.”, 1) at negative 1.lower().

**Local steps**

- Return (filename or empty text).rsplit(“.”, 1) at negative 1.lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filename → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L772)

<a id="op-addcade2132e9b"></a>
### Decode dataurl

`operation_foundation_binding_foundation_desk_form_grid_import_decode_dataurl`

**Inputs** dataurl.

**Declared result** bytes.

**Explicit results** base64.b64decode(payload).

**Explicit failure paths** validation helper — translated “No file content received” · validation helper — translated “Could not read the uploaded file”.

**Local steps**

- If not dataurl.
  - Call the validation error handler Platform.throw(translated “No file content received”, title = translated “Invalid File”).
- Set payload from dataurl.split(“,”, 1) at negative 1.
- Attempt the following.
  - Return base64.b64decode(payload).
- On failure (binascii.Error).
  - Call the validation error handler Platform.throw(translated “Could not read the uploaded file”, title = translated “Invalid File”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L768)

<a id="op-6065e5fd9e452b"></a>
### Stringify

`operation_foundation_binding_foundation_desk_form_grid_import_stringify`

**Inputs** value.

**Declared result** str.

**Explicit results** empty text · “1” when value, otherwise “0” · value.strftime(“%Y-%m-%d %H:%M:%S”) · value.strftime(“%Y-%m-%d”) · value.strftime(“%H:%M:%S”) · 2 additional forms in the steps below.

**Local steps**

- If value is identical to no value.
  - Return empty text.
- If isinstance(value, bool).
  - Return “1” when value, otherwise “0”.
    - Value choice on value — true gives “1”, false gives “0”.
- If isinstance(value, datetime.datetime).
  - Return value.strftime(“%Y-%m-%d %H:%M:%S”).
- If isinstance(value, datetime.date).
  - Return value.strftime(“%Y-%m-%d”).
- If isinstance(value, datetime.time).
  - Return value.strftime(“%H:%M:%S”).
- If (isinstance(value, float) and value.is\_integer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, float) → value.is\_integer().
  - Return str(int(value)).
- Return str(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L783)

## Service · Index

<a id="op-43b5cd0b4b70b3"></a>
### Get context

`operation_foundation_binding_foundation_www_flow_index_get_context`

**Inputs** context.

**Explicit results** context.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Set Platform.local.flags.redirect\_location from formatted text /login?{urlencode(mapping(“redirect-to” → Platform.request.path))}.
  - Raise Platform.Redirect.
- Bind dependencies ISLAND.
- Bind dependencies get\_messages\_for\_boot.
- Bind dependencies get\_assets\_json.
- Set assets from get\_assets\_json().
- Set context.island\_js from assets.get(formatted text {ISLAND}.island.js).
- Set context.island\_css from assets.get(formatted text {ISLAND}.island.css).
- Set context.boot from get\_boot().
- Set context.messages from get\_messages\_for\_boot().
- Return context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L78) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L471)

<a id="op-a4e10e6124cccc"></a>
### Get boot

`operation_foundation_binding_foundation_www_flow_index_get_boot`

**Inputs** no declared parameters.

**Declared result** dict.

**State and service calls** commit.

**Explicit results** mapping(“csrf\_token” → csrf\_token, “site\_name” → Platform.local.site, “socketio\_port” → Platform.conf.socketio\_port, “lang” → Platform.local.lang, …).

**Local steps**

- Bind dependencies boot.
- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Set flow\_boot from boot().
- Evaluate Platform.db.commit().
- Return mapping(“csrf\_token” → csrf\_token, “site\_name” → Platform.local.site, “socketio\_port” → Platform.conf.socketio\_port, “lang” → Platform.local.lang, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L77) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L470)

## Service · Introspect

<a id="op-e805ae3e6cbfe3"></a>
### Describe page data

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_describe_page_data`

**Inputs** page.

**Declared result** dict.

**Explicit results** mapping(“data\_sources” → sources, “variables” → variables).

**Local steps**

- Set sources from list().
- For each r in (page.resources or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.resources → list().
  - Set src from mapping(“name” → r.resource\_name, “type” → r.resource\_type).
  - If r.document\_type.
    - Set src at “doctype” from r.document\_type.
  - If fields bound to \_resource\_fields(r).
    - Set src at “fields” from fields.
  - Evaluate sources.append(src).
- Set variables from list of mapping(“name” → v.variable\_name, “type” → v.variable\_type) for v drawn from (page.variables or list()).
  - Draw v from (page.variables or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.variables → list().
- Return mapping(“data\_sources” → sources, “variables” → variables).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1778)

<a id="op-1d5f04462068ed"></a>
### Resource fields

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_resource_fields`

**Inputs** r.

**Declared result** list.

**Explicit results** raw · parsed when isinstance(parsed, list), otherwise list() · list().

**Local steps**

- Set raw from r.get(“fields”).
- If isinstance(raw, list).
  - Return raw.
- If (isinstance(raw, str) and raw.strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(raw, str) → raw.strip().
  - Set parsed from Platform.parse\_json(raw).
  - Return parsed when isinstance(parsed, list), otherwise list().
    - Value choice on isinstance(parsed, list) — true gives parsed, false gives list().
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1779)

<a id="op-acd6ff5b000bbd"></a>
### Run get page state

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_run_get_page_state`

**Inputs** ctx, args.

**Declared result** str.

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Explicit results** “No page in context.” · (“Current page data state:\\n” + BlockCodec.to\_json(state)).

**Local steps**

- Set page from Platform.get\_doc(“Studio Page”, ctx.page\_id) when ctx.page\_id, otherwise no value.
  - Value choice on ctx.page\_id — true gives Platform.get\_doc(“Studio Page”, ctx.page\_id), false gives no value.
- If page is identical to no value.
  - Return “No page in context.”.
- Set state from describe\_page\_data(page).
- Set state at “has\_page\_script” from bool((page.script or empty text).strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.script → empty text.
- Return (“Current page data state:\\n” + BlockCodec.to\_json(state)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1781)

<a id="op-607e4461db00e2"></a>
### Run list doctypes

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_run_list_doctypes`

**Inputs** ctx, args.

**Declared result** str.

**Record and data access** read “DocType” via get\_all.

**Explicit results** formatted text No readable DocTypes found{hint}. · (formatted text DocTypes (showing {len(allowed)}):  + BlockCodec.to\_json(allowed)).

**Local steps**

- Set query from (args.get(“query”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“query”) → empty text.
- Set filters from mapping(“istable” → 0).
- If query.
  - Set filters at “name” from list(“like”, formatted text %{query}%).
- Set names from Platform.get\_all(“DocType”, filters = filters, pluck = “name”, order\_by = “name asc”, limit\_page\_length = (\_MAX\_DOCTYPES × 2)).
- Set allowed from list of n for n drawn from names where Platform.has\_permission(n, “read”) at slice no value to \_MAX\_DOCTYPES.
  - Draw n from names, keep a combination only if (Platform.has\_permission(n, “read”)).
- If not allowed.
  - Set hint from formatted text  matching '{query}' when query, otherwise empty text.
    - Value choice on query — true gives formatted text  matching '{query}', false gives empty text.
  - Return formatted text No readable DocTypes found{hint}..
- Return (formatted text DocTypes (showing {len(allowed)}):  + BlockCodec.to\_json(allowed)).

**Values supplied outside this operation** effective access from Platform.has\_permission(n, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1784)

<a id="op-d1a959549ba56b"></a>
### Run get doctype fields

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_run_get_doctype_fields`

**Inputs** ctx, args.

**Declared result** str.

**Record and data access** read “DocType” via exists.

**Explicit results** formatted text DocType '{doctype}' not found. · formatted text You do not have read access to '{doctype}'. · (formatted text Fields of {doctype}:  + BlockCodec.to\_json(trimmed)).

**Local steps**

- Set doctype from (args.get(“doctype”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“doctype”) → empty text.
- If (not doctype or not Platform.db.exists(“DocType”, doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not Platform.db.exists(“DocType”, doctype).
  - Return formatted text DocType '{doctype}' not found..
- If not Platform.has\_permission(doctype, “read”).
  - Return formatted text You do not have read access to '{doctype}'..
- Bind dependencies get\_doctype\_fields.
- Set fields from get\_doctype\_fields(doctype) at slice no value to \_MAX\_FIELDS.
- Set trimmed from list of mapping of k → f.get(k) for k drawn from \_FIELD\_KEYS where f.get(k) for f drawn from fields.
  - Draw f from fields.
  - Draw k from \_FIELD\_KEYS, keep a combination only if (f.get(k)).
- Return (formatted text Fields of {doctype}:  + BlockCodec.to\_json(trimmed)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1780)

<a id="op-f9ce36e18423d4"></a>
### Run get sort fields

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_run_get_sort_fields`

**Inputs** ctx, args.

**Declared result** str.

**Record and data access** read “DocType” via exists.

**Explicit results** formatted text DocType '{doctype}' not found. · (formatted text Sortable fields of {doctype}:  + BlockCodec.to\_json(fields)).

**Local steps**

- Set doctype from (args.get(“doctype”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“doctype”) → empty text.
- If (not doctype or not Platform.db.exists(“DocType”, doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not Platform.db.exists(“DocType”, doctype).
  - Return formatted text DocType '{doctype}' not found..
- Bind dependencies get\_sort\_fields.
- Set fields from list of mapping(“fieldname” → f at “fieldname”, “label” → f.get(“label”)) for f drawn from get\_sort\_fields(doctype).
  - Draw f from get\_sort\_fields(doctype).
- Return (formatted text Sortable fields of {doctype}:  + BlockCodec.to\_json(fields)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1782)
