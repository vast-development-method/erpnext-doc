# Workflow, automation and dispatch · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Builtins

<a id="op-db3917f5dc9c71"></a>
### Run report

`operation_foundation_binding_foundation_flow_tools_builtins_run_report`

**Inputs** report\_name, filters = no value, limit = 20, ctx (named only).

**Wrappers, in declaration order** tool(background = deferred anonymous expression).

**Declared result** dict at tuple(str, Any).

**Explicit results** result.

**Explicit failure paths** ValueError(formatted text {report\_name} is a Report Builder report; read its DocType with read\_records.) · ValueError(formatted text Missing filters: {“, ”.join(sorted(missing))}) · ValueError(formatted text {\_error\_text(cause)} The report's filters {\_describe\_filters(specs)}).

**Local steps**

- Bind dependencies get\_report\_doc, run.
- Set report from get\_report\_doc(report\_name).
- If report.report\_type equals “Report Builder”.
  - Raise ValueError(formatted text {report\_name} is a Report Builder report; read its DocType with read\_records.).
- Set specs from \_report\_filter\_specs(report\_name).
- Set defaults from mapping of f at “fieldname” → f at “default” for f drawn from specs where f at “default” does not belong to tuple(no value, empty text).
  - Draw f from specs, keep a combination only if (f at “default” does not belong to tuple(no value, empty text)).
- Set given from ((not filters and report.custom\_filters) or mapping(expand defaults, expand (filters or mapping()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not filters and report.custom\_filters) → mapping(expand defaults, expand (filters or mapping())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters → report.custom\_filters.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If report.report\_type equals “Query Report”.
  - If missing bound to (set(re.findall(“%\\((\\w+)\\)s”, (report.query or empty text))) − set(given)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in report.query → empty text.
    - Raise ValueError(formatted text Missing filters: {“, ”.join(sorted(missing))}).
- Set limit from max(int(limit), 1).
- Attempt the following.
  - Set data from run(report\_name, filters = given, ignore\_prepared\_report = true, are\_default\_filters = not filters).
- On failure (Exception) bound to e.
  - Set cause from e.
  - If isinstance(e, Platform.InReadOnlyMode).
    - While cause.\_\_context\_\_.
      - Set cause from cause.\_\_context\_\_.
  - Raise ValueError(formatted text {\_error\_text(cause)} The report's filters {\_describe\_filters(specs)}) with cause e.
- Set fieldnames from list of c at “fieldname” for c drawn from data at “columns”.
  - Draw c from data at “columns”.
- Set columns from list of mapping(“fieldname” → c at “fieldname”, “label” → c.get(“label”)) for c drawn from data at “columns” where not c.get(“hidden”).
  - Draw c from data at “columns”, keep a combination only if (not c.get(“hidden”)).
- Set rows from (data at “result” or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data at “result” → list().
- Set total\_row from rows at negative 1 when (data.get(“add\_total\_row”) and rows), otherwise no value.
  - Value choice on (data.get(“add\_total\_row”) and rows) — true gives rows at negative 1, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“add\_total\_row”) → rows.
- Set row\_count from (len(rows) − 1) when total\_row is distinct from no value, otherwise len(rows).
  - Value choice on total\_row is distinct from no value — true gives (len(rows) − 1), false gives len(rows).
- Set result from mapping(“columns” → columns, “row\_count” → row\_count).
- If total\_row is distinct from no value.
  - Set result at “total\_row” from \_report\_row(total\_row, fieldnames, columns).
- Set result at “rows” from list of \_report\_row(row, fieldnames, columns) for row drawn from rows at slice no value to min(limit, row\_count).
  - Draw row from rows at slice no value to min(limit, row\_count).
- If not row\_count.
  - Set result at “available\_filters” from \_describe\_filters(specs).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1396)

<a id="op-b7753bf95522cc"></a>
### Report row

`operation_foundation_binding_foundation_flow_tools_builtins_report_row`

**Inputs** row, fieldnames, columns.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping of c at “fieldname” → cells.get(c at “fieldname”) for c drawn from columns.

**Local steps**

- Set cells from row when isinstance(row, dict), otherwise dict(zip(fieldnames, row, strict = true)).
  - Value choice on isinstance(row, dict) — true gives row, false gives dict(zip(fieldnames, row, strict = true)).
- Return mapping of c at “fieldname” → cells.get(c at “fieldname”) for c drawn from columns.
  - Draw c from columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1389)

<a id="op-8f86c8b5571b90"></a>
### Describe filters

`operation_foundation_binding_foundation_flow_tools_builtins_describe_filters`

**Inputs** specs.

**Declared result** str.

**Explicit results** “none found (may be incomplete)” · (“(\* = required) ” + “, ”.join(described)).

**Local steps**

- If not specs.
  - Return “none found (may be incomplete)”.
- Set described from list().
- For each f in specs.
  - Set details from list().
  - If (f at “fieldtype” equals “Link” and f at “options”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in f at “fieldtype” equals “Link” → f at “options”.
    - Evaluate details.append(formatted text link to {f at “options”}).
  - Otherwise.
    - If (isinstance(f at “options”, list) and f at “options”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f at “options”, list) → f at “options”.
      - Evaluate details.append(“ \| ”.join(generator of str(choice) for choice drawn from f at “options”)).
        - Draw choice from f at “options”.
  - If f at “default” does not belong to tuple(no value, empty text).
    - Evaluate details.append(formatted text default {f at “default”}).
  - Set name from (f at “fieldname” + “\*” when f at “reqd”, otherwise empty text).
    - Value choice on f at “reqd” — true gives “\*”, false gives empty text.
  - Evaluate described.append(formatted text {name} ({“; ”.join(details)}) when details, otherwise name).
    - Value choice on details — true gives formatted text {name} ({“; ”.join(details)}), false gives name.
- Return (“(\* = required) ” + “, ”.join(described)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1364)

<a id="op-86be1487175084"></a>
### Report filter specs

`operation_foundation_binding_foundation_flow_tools_builtins_report_filter_specs`

**Inputs** report\_name.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** list(first.values()).

**Local steps**

- Bind dependencies get\_script.
- Set script from get\_script(report\_name).
- Set specs from list of mapping(“fieldname” → f.fieldname, “fieldtype” → f.fieldtype, “options” → \_choices(f.options) when f.fieldtype equals “Select”, otherwise f.options, “default” → f.default, …) for f drawn from scrip ….
  - Draw f from script at “filters”.
  - Value choice on f.fieldtype equals “Select” — true gives \_choices(f.options), false gives f.options.
- Set parts from re.split(“fieldname&#91;"'&#93;?\\s\*:\\s\*&#91;"'&#93;(\\w+)”, script at “script”).
- Set cuts from list of chunk.rpartition(“{”) for chunk drawn from parts at slice 0 to no value with step 2.
  - Draw chunk from parts at slice 0 to no value with step 2.
- Set cuts at negative 1 from tuple(parts at negative 1, empty text, empty text).
- Set specs from (list of \_js\_filter(name, formatted text {before at 2} {after at 0}) for tuple(name, before, after) drawn from zip(parts at slice 1 to no value with step 2, cuts at slice no value to negative 1, cuts at sl ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of \_js\_filter(name, formatted text {before at 2} {after at 0}) for tuple(name, before, after) drawn from zip(parts at slice 1 to no value with step 2, cuts at slice no value to negative 1, cuts at sli … → specs.
  - Draw tuple(name, before, after) from zip(parts at slice 1 to no value with step 2, cuts at slice no value to negative 1, cuts at slice 1 to no value, strict = true).
- Set first from mapping().
- For each spec in specs.
  - Evaluate first.setdefault(spec at “fieldname”, spec).
- Return list(first.values()).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1388)

<a id="op-a1c9804978f9cb"></a>
### Js filter

`operation_foundation_binding_foundation_flow_tools_builtins_js_filter`

**Inputs** fieldname, js.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“fieldname” → fieldname, “fieldtype” → fieldtype.group(1) when fieldtype, otherwise no value, “options” → choices, “default” → literal, …).

**Local steps**

- Bind local operation value for subsequent calls.
- Set string from “(&#91;"'′&#93;)(.\*?)(?&lt;!\\\\)\\1”.
- Set number from “(-?\\d+(?:\\.\\d+)?)(?=\\s\*&#91;,}\\n&#93;)”.
- Set fieldtype from value(“fieldtype”, “&#91;"'&#93;(&#91;\\w &#93;+)&#91;"'&#93;”).
- Set options from value(“options”, formatted text {string}\|\\&#91;(&#91;^\\&#93;&#93;\*)\\&#93;).
- Set default from value(“default”, formatted text {string}\|{number}).
- Set choices from no value.
- If (options and options.group(3) is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in options → options.group(3) is distinct from no value.
  - Set items from options.group(3).
  - If “{” belongs to items.
    - Set choices from (re.findall(“\\bvalue&#91;"'&#93;?\\s\*:\\s\*&#91;"'′&#93;(&#91;^"'′&#93;\*)&#91;"'′&#93;”, items) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in re.findall(“\\bvalue&#91;"'&#93;?\\s\*:\\s\*&#91;"'′&#93;(&#91;^"'′&#93;\*)&#91;"'′&#93;”, items) → no value.
  - Otherwise.
    - Set choices from list of c.strip().strip(“"'′”) for c drawn from items.split(“,”) where c.strip().
      - Draw c from items.split(“,”), keep a combination only if (c.strip()).
- Otherwise.
  - If options.
    - Set choices from options.group(2).
- If (fieldtype and fieldtype.group(1) equals “Select” and isinstance(choices, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype → fieldtype.group(1) equals “Select” → isinstance(choices, str).
  - Set choices from \_choices(choices.replace(“\\n”, whitespace '\\n')).
- Set literal from no value.
- If (default and default.group(3) is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in default → default.group(3) is distinct from no value.
  - Set literal from float(default.group(3)) when “.” belongs to default.group(3), otherwise int(default.group(3)).
    - Value choice on “.” belongs to default.group(3) — true gives float(default.group(3)), false gives int(default.group(3)).
- Otherwise.
  - If default.
    - Set literal from default.group(2).
- Return mapping(“fieldname” → fieldname, “fieldtype” → fieldtype.group(1) when fieldtype, otherwise no value, “options” → choices, “default” → literal, …).
  - Value choice on fieldtype — true gives fieldtype.group(1), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1376)

<a id="op-5b4f172b020247"></a>
### Js filter.value

`operation_foundation_binding_foundation_flow_tools_builtins_js_filter_value`

**Inputs** key, pattern.

**Declared result** (re.Match bitwise or no value).

**Explicit results** re.search(formatted text \\b{key}&#91;"'&#93;?\\s\*:\\s\*(?:{pattern}), js, re.S).

**Local steps**

- Return re.search(formatted text \\b{key}&#91;"'&#93;?\\s\*:\\s\*(?:{pattern}), js, re.S).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1377)

<a id="op-2c9ce2a84df9fc"></a>
### Choices

`operation_foundation_binding_foundation_flow_tools_builtins_choices`

**Inputs** options.

**Declared result** list at str.

**Explicit results** list of line.strip() for line drawn from (options or empty text).split(whitespace '\\n') where line.strip().

**Local steps**

- Return list of line.strip() for line drawn from (options or empty text).split(whitespace '\\n') where line.strip().
  - Draw line from (options or empty text).split(whitespace '\\n'), keep a combination only if (line.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1358)

<a id="op-a3574f9db04160"></a>
### Search docs

`operation_foundation_binding_foundation_flow_tools_builtins_search_docs`

**Inputs** query, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“results” → results) · mapping(“results” → list(), “note” → note).

**Explicit failure paths** validation helper — translated “docs.Platform.io answered HTTP {0}”.format(response.status\_code).

**Local steps**

- Bind dependencies requests.
- Set response from requests.get(\_DOCS\_SEARCH\_API, params = mapping(“query” → query), timeout = 20, allow\_redirects = false, headers = mapping(“User-Agent” → “Platform Flow”)).
- If response.status\_code differs from 200.
  - Call the validation error handler Platform.throw(translated “docs.Platform.io answered HTTP {0}”.format(response.status\_code)).
- Set results from list of mapping(“title” → \_plain(hit at “title”), “url” → formatted text {\_DOCS\_URL}/{hit at “route”}, “snippet” → \_plain(hit at “content”) at slice no value to \_DOCS\_SNIPPET\_LIMIT) for hit drawn from resp ….
  - Draw hit from response.json() at “message” at “results”, keep a combination only if (hit.get(“route”)).
- If results.
  - Return mapping(“results” → results).
- Set note from formatted text No docs page has every word of {query}. Search again with fewer, plainer words..
- Return mapping(“results” → list(), “note” → note).

**Values supplied outside this operation** service or queued work from requests.get(\_DOCS\_SEARCH\_API, params = mapping(“query” → query), timeout = 20, allow\_redirects = false, headers = mapping(“User-Agent” → “Platform Flow”)).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1398)

<a id="op-bd8e4aefe3b1f4"></a>
### Plain

`operation_foundation_binding_foundation_flow_tools_builtins_plain`

**Inputs** text.

**Declared result** str.

**Explicit results** one space.join(html.unescape(\_HTML\_TAG.sub(empty text, text)).split()).

**Local steps**

- Return one space.join(html.unescape(\_HTML\_TAG.sub(empty text, text)).split()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1382)

<a id="op-c5a32f9098656e"></a>
### Bind search knowledge

`operation_foundation_binding_foundation_flow_tools_builtins_bind_search_knowledge`

**Inputs** kbs.

**Declared result** Tool.

**Explicit results** tool(search\_knowledge, description = \_knowledge\_search\_description(kbs)).

**Local steps**

- Bind local operation search\_knowledge for subsequent calls.
- Return tool(search\_knowledge, description = \_knowledge\_search\_description(kbs)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1349)

<a id="op-95b376e1e3ef21"></a>
### Bind search knowledge.search knowledge

`operation_foundation_binding_foundation_flow_tools_builtins_bind_search_knowledge_search_knowledge`

**Inputs** query, ctx (named only).

**Declared result** list at dict at tuple(str, Any).

**Explicit results** retrieve(query, kbs = kbs).

**Local steps**

- Bind dependencies retrieve.
- Return retrieve(query, kbs = kbs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1350)

<a id="op-78e75cf30cfe2b"></a>
### Knowledge search description

`operation_foundation_binding_foundation_flow_tools_builtins_knowledge_search_description`

**Inputs** kbs.

**Declared result** str.

**Record and data access** read “Flow Knowledge Base” via get\_all.

**Explicit results** \_KNOWLEDGE\_SEARCH\_DESCRIPTION · formatted text {\_KNOWLEDGE\_SEARCH\_DESCRIPTION}  This agent's knowledge bases: {listed}.

**Local steps**

- If not kbs.
  - Return \_KNOWLEDGE\_SEARCH\_DESCRIPTION.
- Set rows from Platform.get\_all(“Flow Knowledge Base”, filters = mapping(“name” → list(“in”, kbs), “enabled” → 1), fields = list(“title”, “description”)).
- Set listed from whitespace '\\n'.join(generator of formatted text - {r.title}: {r.description} for r drawn from rows where r.description).
  - Draw r from rows, keep a combination only if (r.description).
- If not listed.
  - Return \_KNOWLEDGE\_SEARCH\_DESCRIPTION.
- Return formatted text {\_KNOWLEDGE\_SEARCH\_DESCRIPTION}  This agent's knowledge bases: {listed}.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1378)

<a id="op-92c9d253cb0443"></a>
### Bind search attachments

`operation_foundation_binding_foundation_flow_tools_builtins_bind_search_attachments`

**Inputs** session.

**Declared result** Tool.

**Explicit results** tool(search\_attachments, description = \_ATTACHMENT\_SEARCH\_DESCRIPTION).

**Local steps**

- Bind local operation search\_attachments for subsequent calls.
- Return tool(search\_attachments, description = \_ATTACHMENT\_SEARCH\_DESCRIPTION).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1347)

<a id="op-47434784a2f68a"></a>
### Bind search attachments.search attachments

`operation_foundation_binding_foundation_flow_tools_builtins_bind_search_attachments_search_attachments`

**Inputs** query, ctx (named only).

**Declared result** list at dict at tuple(str, Any).

**Record and data access** read “Flow Session Attachment” via get\_all.

**Explicit results** list() · list of mapping(“file” → names.get(hit at “attachment”), “content” → hit at “content”, “score” → hit at “score”) for hit drawn from retrieve\_attachments(query, session = session).

**Local steps**

- Bind dependencies retrieve\_attachments.
- If not session.
  - Return list().
- Set names from dict(Platform.get\_all(“Flow Session Attachment”, filters = mapping(“parent” → session), fields = list(“file”, “file\_name”), as\_list = true)).
- Return list of mapping(“file” → names.get(hit at “attachment”), “content” → hit at “content”, “score” → hit at “score”) for hit drawn from retrieve\_attachments(query, session = session).
  - Draw hit from retrieve\_attachments(query, session = session).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1348)

<a id="op-4551d8f21385a9"></a>
### Bind read attachment

`operation_foundation_binding_foundation_flow_tools_builtins_bind_read_attachment`

**Inputs** session.

**Declared result** Tool.

**Explicit results** tool(read\_attachment, description = \_ATTACHMENT\_READ\_DESCRIPTION).

**Local steps**

- Bind local operation read\_attachment for subsequent calls.
- Return tool(read\_attachment, description = \_ATTACHMENT\_READ\_DESCRIPTION).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1345)

<a id="op-2b20839d3cef3a"></a>
### Bind read attachment.read attachment

`operation_foundation_binding_foundation_flow_tools_builtins_bind_read_attachment_read_attachment`

**Inputs** file = no value, offset = 1, limit = no value, ctx (named only).

**Declared result** Any.

**Explicit results** list() · read(session, file, offset, limit).

**Local steps**

- Bind dependencies read.
- If not session.
  - Return list().
- Return read(session, file, offset, limit).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1346)

<a id="op-9f80c7c787ebac"></a>
### Bind update memory

`operation_foundation_binding_foundation_flow_tools_builtins_bind_update_memory`

**Inputs** agent, session = no value.

**Declared result** Tool.

**Explicit results** tool(update\_memory, description = \_UPDATE\_MEMORY\_DESCRIPTION).

**Local steps**

- Bind local operation update\_memory for subsequent calls.
- Return tool(update\_memory, description = \_UPDATE\_MEMORY\_DESCRIPTION).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1351)

<a id="op-c820ff4e567c3e"></a>
### Bind update memory.update memory

`operation_foundation_binding_foundation_flow_tools_builtins_bind_update_memory_update_memory`

**Inputs** content, scope, memory\_id = no value, ctx (named only).

**Declared result** dict at tuple(str, Any).

**Explicit results** save\_memory(agent, content = content, scope = scope, memory\_id = memory\_id, session = session).

**Explicit failure paths** validation helper — translated “Memory is not configured for this agent.”.

**Local steps**

- Bind dependencies save\_memory.
- If not agent.
  - Call the validation error handler Platform.throw(translated “Memory is not configured for this agent.”, title = translated “Memory Unavailable”).
- Return save\_memory(agent, content = content, scope = scope, memory\_id = memory\_id, session = session).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1352)

<a id="op-7d42868e31f14e"></a>
### Bind load skill

`operation_foundation_binding_foundation_flow_tools_builtins_bind_load_skill`

**Inputs** agent.

**Declared result** Tool.

**Explicit results** tool(load\_skill, description = \_LOAD\_SKILL\_DESCRIPTION).

**Local steps**

- Bind local operation load\_skill for subsequent calls.
- Return tool(load\_skill, description = \_LOAD\_SKILL\_DESCRIPTION).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1343)

<a id="op-0c62ed2253a24e"></a>
### Bind load skill.load skill

`operation_foundation_binding_foundation_flow_tools_builtins_bind_load_skill_load_skill`

**Inputs** name, file = no value, ctx (named only).

**Declared result** str.

**Record and data access** resolve a document from “Flow Agent” via get\_doc · read “Flow Skill” via get\_value.

**Explicit results** skill\_file(name, file) · Platform.db.get\_value(“Flow Skill”, name, “instructions”).

**Explicit failure paths** validation helper — translated “Skills are not configured for this agent.” · validation helper — translated “No skill named {0}. Available: {1}”.format(name, (“, ”.join(sorted(available)) or “none”)).

**Local steps**

- Bind dependencies skill\_file.
- If not agent.
  - Call the validation error handler Platform.throw(translated “Skills are not configured for this agent.”, title = translated “Skill Unavailable”).
- Set available from set of row.name for row drawn from Platform.get\_doc(“Flow Agent”, agent).visible\_skills().
  - Draw row from Platform.get\_doc(“Flow Agent”, agent).visible\_skills().
- If name does not belong to available.
  - Call the validation error handler Platform.throw(translated “No skill named {0}. Available: {1}”.format(name, (“, ”.join(sorted(available)) or “none”)), title = translated “Unknown Skill”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “, ”.join(sorted(available)) → “none”.
- If file.
  - Return skill\_file(name, file).
- Return Platform.db.get\_value(“Flow Skill”, name, “instructions”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1344)

<a id="op-36bd62cce10f4c"></a>
### Execute

`operation_foundation_binding_foundation_flow_tools_builtins_execute`

**Inputs** code, description, read\_only = false, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = deferred anonymous expression, confirm\_prompt = deferred anonymous expression).

**Declared result** Any.

**Explicit results** \_run\_code(code, ctx) · result.

**Explicit failure paths** Platform.InReadOnlyMode(translated “It tried to write.”) · propagate active failure · ValueError(((\_error\_text(e) + whitespace '\\n') + translated “This code changes something, so it can't run as read\_only. Call execute again without read\_only; the user ap …”)).

**Local steps**

- If not read\_only.
  - Return \_run\_code(code, ctx).
- Set ctx.read\_only from true.
- Attempt the following.
  - Within Platform.db.read\_only().
    - Set result from \_run\_code(code, ctx).
    - If Platform.db.transaction\_writes.
      - Raise Platform.InReadOnlyMode(translated “It tried to write.”).
    - Return result.
- On failure (Exception) bound to e.
  - If not \_needs\_approval(e).
    - Propagate the active failure.
  - Raise ValueError(((\_error\_text(e) + whitespace '\\n') + translated “This code changes something, so it can't run as read\_only. Call execute again without read\_only; the user ap …”)) with cause e.
- On exit, including pending return or failure.
  - Set ctx.read\_only from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1367)

<a id="op-164c5e0fca21fd"></a>
### Run code

`operation_foundation_binding_foundation_flow_tools_builtins_run_code`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** code, ctx.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** ValueError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1395)

<a id="op-0089957dfd6dd7"></a>
### Needs approval

`operation_foundation_binding_foundation_flow_tools_builtins_needs_approval`

**Inputs** error.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Bind dependencies NeedsApproval.
- Set seen from set().
- While (error is distinct from no value and id(error) does not belong to seen).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in error is distinct from no value → id(error) does not belong to seen.
  - If isinstance(error, (Platform.InReadOnlyMode bitwise or NeedsApproval)).
    - Return true.
  - Evaluate seen.add(id(error)).
  - Set error from (error.\_\_cause\_\_ or error.\_\_context\_\_).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in error.\_\_cause\_\_ → error.\_\_context\_\_.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1379)

<a id="op-f4f34a1fa22d20"></a>
### Error text

`operation_foundation_binding_foundation_flow_tools_builtins_error_text`

**Inputs** e.

**Declared result** str.

**Explicit results** (str(e).strip() or e.\_\_class\_\_.\_\_name\_\_) at slice no value to \_ERROR\_LIMIT.

**Local steps**

- Return (str(e).strip() or e.\_\_class\_\_.\_\_name\_\_) at slice no value to \_ERROR\_LIMIT.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(e).strip() → e.\_\_class\_\_.\_\_name\_\_.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1366)
