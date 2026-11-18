# Forms, reports and navigation · operations 50

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Qrcode

<a id="op-8bd1f14c1f7bdd"></a>
### Get user svg from cache

`operation_foundation_public_pages_qrcode_business_behavior_get_user_scalable_vector_graphics_from_cache`

**Inputs** no declared parameters.

**Record and data access** read “User” via exists · resolve a document from “User” via get\_doc.

**Explicit results** tuple(user, svg.decode()).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Page has expired!” · validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set key from get\_query\_key().
- Set totp\_uri from Platform.cache.get\_value(formatted text {key}\_uri).
- Set user from Platform.cache.get\_value(formatted text {key}\_user).
- If (not totp\_uri or not user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not totp\_uri → not user.
  - Call the validation error handler Platform.throw(translated “Page has expired!”, Platform.PermissionError).
- If not Platform.db.exists(“User”, user).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set user from Platform.get\_doc(“User”, user).
- Set svg from get\_qr\_svg\_code(totp\_uri).
- Return tuple(user, svg.decode()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L84) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L87)

## Service · Query

<a id="op-f59099481b5120"></a>
### Run query blocks

`operation_foundation_binding_foundation_studio_ai_agent_tools_query_run_query_blocks`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “The page is empty — nothing to select.” · formatted text No block found with id {scope}. · “No blocks matched. Loosen the filters or check the page outline.” · (header + BlockCodec.to\_json(matches)).

**Local steps**

- Set root from ctx.\_page\_root().
- If root is identical to no value.
  - Return “The page is empty — nothing to select.”.
- Set scope from args.get(“within”).
- Set start from root.
- If scope.
  - Set start from find\_block(root, scope).
  - If start is identical to no value.
    - Return formatted text No block found with id {scope}..
- Set component from args.get(“component”).
- Set text\_only from bool(args.get(“text\_only”)).
- Set contains from args.get(“contains”).
- Set matches from list().
- For each tuple(block, \_depth) in walk\_blocks(start).
  - If not match\_block(block, component = component, text\_only = text\_only, contains = contains).
    - Continue with the next iteration or loop test.
  - Set component\_id from block.get(“componentId”).
  - If not component\_id.
    - Continue with the next iteration or loop test.
  - Set entry from mapping(“id” → component\_id, “name” → (block.get(“componentName”) or “div”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentName”) → “div”.
  - If text bound to block\_text(block).
    - Set entry at “text” from text.
  - Evaluate matches.append(entry).
- If not matches.
  - Return “No blocks matched. Loosen the filters or check the page outline.”.
- Set header from formatted text {len(matches)} block(s) matched (page as it was at the start of this turn):.
- Return (header + BlockCodec.to\_json(matches)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1789)

<a id="op-b146987f749d5f"></a>
### Run read block

`operation_foundation_binding_foundation_studio_ai_agent_tools_query_run_read_block`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “The page is empty.” · formatted text No block found with id {component\_id}. · formatted text Block {component\_id} (full props/styles/children, as of the start of this turn): {detail}.

**Local steps**

- Set root from ctx.\_page\_root().
- If root is identical to no value.
  - Return “The page is empty.”.
- Set component\_id from args.get(“component\_id”).
- Set block from find\_block(root, component\_id) when component\_id, otherwise no value.
  - Value choice on component\_id — true gives find\_block(root, component\_id), false gives no value.
- If block is identical to no value.
  - Return formatted text No block found with id {component\_id}..
- Set detail from BlockCodec.to\_json(BlockCodec.compress(block)).
- Return formatted text Block {component\_id} (full props/styles/children, as of the start of this turn): {detail}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1790)

## Service · Query report

<a id="op-faf709e4f1f79b"></a>
### Get report doc

`operation_foundation_desk_query_report_business_behavior_get_report_record`

**Inputs** report\_name.

**Record and data access** resolve a document from “Report” via get\_doc.

**Explicit results** doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You don't have access to Report: {0}”.format(translated doc.name) · validation helper with Platform.PermissionError — translated “You don't have permission to get a report on: {0}”.format(translated doc.ref\_doctype) · validation helper — translated “Report {0} is disabled”.format(translated report\_name).

**Local steps**

- Set doc from Platform.get\_doc(“Report”, report\_name).
- Set doc.custom\_columns from list().
- Set doc.custom\_filters from list().
- If doc.report\_type equals “Custom Report”.
  - Set custom\_report\_doc from doc.
  - Set doc from get\_reference\_report(doc).
  - Set doc.custom\_report from report\_name.
  - If custom\_report\_doc.json.
    - Set data from json.loads(custom\_report\_doc.json).
    - If data.
      - Set doc.custom\_columns from data.get(“columns”).
      - Set doc.custom\_filters from data.get(“filters”).
  - Set doc.is\_custom\_report from true.
  - Set doc.prepared\_report from custom\_report\_doc.prepared\_report.
- If not doc.is\_permitted().
  - Call the validation error handler Platform.throw(translated “You don't have access to Report: {0}”.format(translated doc.name), Platform.PermissionError).
- If not Platform.has\_permission(doc.ref\_doctype, “report”).
  - Call the validation error handler Platform.throw(translated “You don't have permission to get a report on: {0}”.format(translated doc.ref\_doctype), Platform.PermissionError).
- If doc.disabled.
  - Call the validation error handler Platform.throw(translated “Report {0} is disabled”.format(translated report\_name)).
- Return doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(doc.ref\_doctype, “report”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L101) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L404)

<a id="op-f55d159c7d88c8"></a>
### Get permitted report print format

`operation_foundation_binding_foundation_desk_query_report_get_permitted_report_print_format`

**Inputs** print\_format.

**Declared result** Platform.\_dict.

**Record and data access** read “Print Format” via get\_value.

**Explicit results** pf.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “{0} is not an enabled Print Format for a Report”.format(Platform.bold(print\_format)) · validation helper with Platform.PermissionError — translated “You don't have permission to print: {0}”.format(translated report.ref\_doctype).

**Local steps**

- Set pf from Platform.db.get\_value(“Print Format”, mapping(“name” → print\_format, “disabled” → 0, “print\_format\_for” → “Report”), list(“report”, “html”, “css”, “print\_format\_type”), as\_dict = true).
- If not pf.
  - Call the validation error handler Platform.throw(translated “{0} is not an enabled Print Format for a Report”.format(Platform.bold(print\_format)), Platform.DoesNotExistError).
- Set report from get\_report\_doc(pf.report).
- If not Platform.has\_permission(report.ref\_doctype, “print”).
  - Call the validation error handler Platform.throw(translated “You don't have permission to print: {0}”.format(translated report.ref\_doctype), Platform.PermissionError).
- Return pf.

**Values supplied outside this operation** effective access from Platform.has\_permission(report.ref\_doctype, “print”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L816)

<a id="op-7280e1a7be114a"></a>
### Get print format data

`operation_foundation_desk_query_report_business_behavior_get_print_format_data`

**Inputs** print\_format.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“print\_format\_type” → pf.print\_format\_type) · mapping(“html” → pf.html, “css” → pf.css, “print\_format\_type” → pf.print\_format\_type).

**Local steps**

- Set pf from get\_permitted\_report\_print\_format(print\_format).
- If pf.print\_format\_type equals “Jinja”.
  - Return mapping(“print\_format\_type” → pf.print\_format\_type).
- Return mapping(“html” → pf.html, “css” → pf.css, “print\_format\_type” → pf.print\_format\_type).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L100) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L402)

<a id="op-4917de00d68554"></a>
### Get report result

`operation_foundation_desk_query_report_business_behavior_get_report_result`

**Inputs** report, filters.

**Explicit results** res.

**Local steps**

- Set res from no value.
- If report.report\_type equals “Query Report”.
  - Set res from report.execute\_query\_report(filters).
- Otherwise.
  - If report.report\_type equals “Script Report”.
    - Set res from report.execute\_script\_report(filters).
  - Otherwise.
    - If report.report\_type equals “Custom Report”.
      - Set ref\_report from get\_report\_doc(report.report\_name).
      - Set res from get\_report\_result(ref\_report, filters).
- Return res.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0209.json#L1865) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L405)

<a id="op-0c3747e81d3540"></a>
### Generate report result

`operation_foundation_desk_query_report_business_behavior_generate_report_result`

**Inputs** report, filters = no value, user = no value, custom\_columns = no value, is\_tree = false, parent\_field = no value.

**Wrappers, in declaration order** Platform.read\_only().

**State and service calls** call insert on columns.

**Explicit results** return\_dict.

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set filters from (filters or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- If (filters and isinstance(filters, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → isinstance(filters, str).
  - Set filters from json.loads(filters).
- Set res from (get\_report\_result(report, filters) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_report\_result(report, filters) → list().
- Set tuple(columns, result, message, chart, …) from ljust\_list(res, 6).
- Set columns from list of get\_column\_as\_dict(col) for col drawn from (columns or list()).
  - Draw col from (columns or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in columns → list().
- Set report\_column\_names from list of col at “fieldname” for col drawn from columns.
  - Draw col from columns.
- Set result from normalize\_result(result, columns).
- If report.get(“custom\_columns”).
  - Set columns from list of column for column drawn from report.custom\_columns where (column.get(“link\_field”) or column at “fieldname” belongs to report\_column\_names).
    - Draw column from report.custom\_columns, keep a combination only if ((column.get(“link\_field”) or column at “fieldname” belongs to report\_column\_names)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in column.get(“link\_field”) → column at “fieldname” belongs to report\_column\_names.
- If custom\_columns.
  - For each custom\_column in custom\_columns.
    - Evaluate columns.insert((custom\_column at “insert\_after\_index” + 1), custom\_column).
- Set report\_custom\_columns from list of column for column drawn from columns where column at “fieldname” does not belong to report\_column\_names.
  - Draw column from columns, keep a combination only if (column at “fieldname” does not belong to report\_column\_names).
- If report\_custom\_columns.
  - Set result from add\_custom\_column\_data(report\_custom\_columns, result).
- If result.
  - Set result from get\_filtered\_data(report.ref\_doctype, columns, result, user).
- Set has\_total\_row from (cint(report.add\_total\_row) and result and not skip\_total\_row).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(report.add\_total\_row) → result → not skip\_total\_row.
- If has\_total\_row.
  - Set result from add\_total\_row(result, columns, is\_tree = is\_tree, parent\_field = parent\_field).
- If (isinstance(filters, dict) and filters.get(“translate\_data”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(filters, dict) → filters.get(“translate\_data”).
  - Set result from translate\_report\_data(result, has\_total\_row).
- Set return\_dict from mapping(“result” → result, “columns” → columns, “message” → message, “chart” → chart, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in skip\_total\_row → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.hget(“report\_execution\_time”, report.name) → 0.
- If (report.snapshot\_report and report.doctype\_to\_sync).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report.snapshot\_report → report.doctype\_to\_sync.
  - If latest\_sync bound to get\_latest\_complete\_sync(report.doctype\_to\_sync at 0.doc\_type).
    - Evaluate return\_dict.update(mapping(“snapshot\_report” → true, “snapshot\_at” → latest\_sync.creation)).
- Return return\_dict.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L96) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L393)

<a id="op-78739ba1309020"></a>
### Normalize result

`operation_foundation_desk_query_report_business_behavior_normalize_result`

**Inputs** result, columns.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set column\_names from list of column at “fieldname” for column drawn from columns.
  - Draw column from columns.
- If (result and isinstance(result at 0, (list bitwise or tuple))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in result → isinstance(result at 0, (list bitwise or tuple)).
  - For each row in result.
    - Set row\_obj from mapping().
    - For each tuple(idx, column\_name) in enumerate(column\_names).
      - Set row\_obj at column\_name from row at idx.
    - Evaluate data.append(row\_obj).
- Otherwise.
  - Set data from result.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0209.json#L3555) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L411)

<a id="op-45390f7463ad9f"></a>
### Get script

`operation_foundation_desk_query_report_business_behavior_get_script`

**Inputs** report\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via get\_value · read “Module Def” via get\_cached\_value.

**Explicit results** mapping(“script” → render\_include(script), “html\_format” → html\_format, “execution\_time” → (Platform.cache.hget(“report\_execution\_time”, report\_name) or 0), “filters” → report.filters, …).

**Local steps**

- Set report from get\_report\_doc(report\_name).
- Set module from (report.module or Platform.db.get\_value(“DocType”, report.ref\_doctype, “module”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in report.module → Platform.db.get\_value(“DocType”, report.ref\_doctype, “module”).
- Set is\_custom\_module from Platform.get\_cached\_value(“Module Def”, module, “custom”).
- Set module\_path from empty text when is\_custom\_module, otherwise get\_module\_path(module).
  - Value choice on is\_custom\_module — true gives empty text, false gives get\_module\_path(module).
- Set report\_folder from (module\_path and os.path.join(module\_path, “report”, scrub(report.name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in module\_path → os.path.join(module\_path, “report”, scrub(report.name)).
- Set script\_path from (report\_folder and os.path.join(report\_folder, (scrub(report.name) + “.js”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_folder → os.path.join(report\_folder, (scrub(report.name) + “.js”)).
- Set print\_path from (report\_folder and os.path.join(report\_folder, (scrub(report.name) + “.html”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_folder → os.path.join(report\_folder, (scrub(report.name) + “.html”)).
- Set script from no value.
- If os.path.exists(script\_path).
  - Within open(script\_path) bound as f.
    - Set script from f.read().
    - Update script using + formatted text   //# sourceURL={scrub(report.name)}.js.
- Set html\_format from get\_html\_format(print\_path).
- If (not script and report.javascript).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not script → report.javascript.
  - Set script from report.javascript.
  - Update script using + formatted text   //# sourceURL={scrub(report.name)}\_\_custom.
- If not script.
  - Set script from formatted text Platform.query\_reports&#91;{json.dumps(report\_name)}&#93;={}.
- Return mapping(“script” → render\_include(script), “html\_format” → html\_format, “execution\_time” → (Platform.cache.hget(“report\_execution\_time”, report\_name) or 0), “filters” → report.filters, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.hget(“report\_execution\_time”, report\_name) → 0.
  - Value choice on report.get(“is\_custom\_report”) — true gives report.name, false gives no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Module Def”, module, “custom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L102) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L406)

<a id="op-b90b59b70d3624"></a>
### Get reference report

`operation_foundation_desk_query_report_business_behavior_get_reference_report`

**Inputs** report.

**Record and data access** resolve a document from “Report” via get\_doc.

**Explicit results** report · get\_reference\_report(reference\_report).

**Local steps**

- If report.report\_type differs from “Custom Report”.
  - Return report.
- Set reference\_report from Platform.get\_doc(“Report”, report.reference\_report).
- Return get\_reference\_report(reference\_report).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0209.json#L4804) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L403)

<a id="op-b9b7c15516f95e"></a>
### Run

`operation_foundation_desk_query_report_business_behavior_run`

**Inputs** report\_name, filters = no value, user = no value, ignore\_prepared\_report = false, custom\_columns = no value, is\_tree = false, parent\_field = no value, are\_default\_filters = true, js\_filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Declared result** dict.

**Explicit results** \_run(report\_name = report\_name, filters = filters, ignore\_prepared\_report = ignore\_prepared\_report, custom\_columns = custom\_columns, …).

**Local steps**

- Return \_run(report\_name = report\_name, filters = filters, ignore\_prepared\_report = ignore\_prepared\_report, custom\_columns = custom\_columns, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0209.json#L4932) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L412)

<a id="op-99e8bfc2832813"></a>
### Run

`operation_foundation_desk_query_report_business_behavior_run_2`

**Inputs** report\_name (named only), filters (named only, default no value), user (named only, default no value), ignore\_prepared\_report (named only, default false), custom\_columns (named only, default no value), is\_tree (named only, default false), parent\_field (named only, default no value), are\_default\_filters (named only, default true), js\_filters (named only, default no value).

**Declared result** dict.

**Record and data access** read “Prepared Report” via get\_value · read “Report” via exists · resolve a document from “Report” via get\_doc.

**State and service calls** msgprint with translated “Must have report permission to access this report.”.

**Explicit results** result.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Evaluate validate\_filters\_permissions(report\_name, filters, user, js\_filters).
- Set report from get\_report\_doc(report\_name).
- If not Platform.has\_permission(report.ref\_doctype, “report”).
  - Evaluate Platform.msgprint(translated “Must have report permission to access this report.”, raise\_exception = true).
- Set result from no value.
- If (sbool(are\_default\_filters) and report.get(“custom\_filters”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sbool(are\_default\_filters) → report.get(“custom\_filters”).
  - Set filters from report.custom\_filters.
- Set is\_prepared\_report from (report.prepared\_report and not sbool(ignore\_prepared\_report) and not custom\_columns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report.prepared\_report → not sbool(ignore\_prepared\_report) → not custom\_columns.
- Attempt the following.
  - If is\_prepared\_report.
    - If filters.
      - If isinstance(filters, str).
        - Set filters from json.loads(filters).
      - Set dn from filters.pop(“prepared\_report\_name”, no value).
      - If dn.
        - Set prepared\_for from Platform.db.get\_value(“Prepared Report”, mapping(“name” → dn, “owner” → user), “report\_name”).
        - If (prepared\_for differs from report\_name and (not prepared\_for or not Platform.db.exists(“Report”, prepared\_for) or get\_reference\_report(nested operand in the contract.get\_doc(“Report”, prepared\_for)).name d ….
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in prepared\_for differs from report\_name → (not prepared\_for or not Platform.db.exists(“Report”, prepared\_for) or get\_reference\_report(Platform.get\_doc(“Report”, prepared\_for)).name differs from report.name).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not prepared\_for → not Platform.db.exists(“Report”, prepared\_for) → get\_reference\_report(Platform.get\_doc(“Report”, prepared\_for)).name differs from report.name.
          - Evaluate Platform.has\_permission(“Prepared Report”, “read”, dn, throw = true).
    - Otherwise.
      - Set dn from empty text.
    - Set result from get\_prepared\_report\_result(report, filters, dn, user).
  - Otherwise.
    - Set result from generate\_report\_result(report, filters, user, custom\_columns, …).
    - Evaluate add\_data\_to\_monitor(report = (report.reference\_report or report.name)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in report.reference\_report → report.name.
- On failure (Exception).
  - Evaluate Platform.log\_error(“Report execution failed for: {}”.format(report\_name)).
  - Propagate the active failure.
- Set result at “add\_total\_row” from (report.add\_total\_row and not result.get(“skip\_total\_row”, false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report.add\_total\_row → not result.get(“skip\_total\_row”, false).
- If (sbool(are\_default\_filters) and report.get(“custom\_filters”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sbool(are\_default\_filters) → report.get(“custom\_filters”).
  - Set result at “custom\_filters” from report.custom\_filters.
- Set columns from list of get\_column\_as\_dict(column) for column drawn from (result.get(“columns”) or list()).
  - Draw column from (result.get(“columns”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.get(“columns”) → list().
- Evaluate send\_link\_titles(get\_report\_link\_titles(columns, result.get(“result”))).
- Return result.

**Values supplied outside this operation** effective access from Platform.has\_permission(report.ref\_doctype, “report”), Platform.has\_permission(“Prepared Report”, “read”, dn, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L103) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L413)

<a id="op-d761cb535c4158"></a>
### Add custom column data

`operation_foundation_desk_query_report_business_behavior_add_custom_column_data`

**Inputs** custom\_columns, result.

**Explicit results** result.

**Local steps**

- Set pending\_columns from custom\_columns.
- While pending\_columns.
  - Set custom\_column\_data from get\_data\_for\_custom\_report(pending\_columns, result).
  - Set unresolved\_columns from list().
  - For each column in pending\_columns.
    - Set key from tuple(column.get(“doctype”), column.get(“fieldname”)).
    - If key does not belong to custom\_column\_data.
      - Evaluate unresolved\_columns.append(column).
      - Continue with the next iteration or loop test.
    - For each row in result.
      - Set link\_field from column.get(“link\_field”).
      - If isinstance(link\_field, str).
        - Set link\_field from Platform.\_dict(mapping(“fieldname” → link\_field, “names” → list())).
      - Set row\_reference from row.get(link\_field.get(“fieldname”)).
      - If not row\_reference.
        - Continue with the next iteration or loop test.
      - Set row at column.get(“fieldname”) from custom\_column\_data.get(key).get(row\_reference).
  - If len(unresolved\_columns) equals len(pending\_columns).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set pending\_columns from unresolved\_columns.
- Return result.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L93) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L386)

<a id="op-0046608ef8a1e1"></a>
### Get user facing error

`operation_foundation_binding_foundation_desk_query_report_get_user_facing_error`

**Inputs** traceback, keep\_line\_breaks = false.

**Declared result** str.

**Explicit results** empty text · unescape(message.strip()).

**Local steps**

- If not traceback.
  - Return empty text.
- Set lines from traceback.strip().splitlines().
- Set message from lines at negative 1.
- If len(lines) &gt; 1.
  - Set message from message.partition(“: ”) at 2.
- If keep\_line\_breaks.
  - Set message from re.sub(text in the contract, whitespace '\\n', message, flags = re.IGNORECASE).
- Set message from re.sub(“&lt;&#91;^&gt;&#93;\*&gt;”, one space, message).
- Set message from whitespace '\\n'.join(generator of one space.join(line.split()) for line drawn from message.split(whitespace '\\n')).
  - Draw line from message.split(whitespace '\\n').
- Return unescape(message.strip()).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L817)

<a id="op-4fce8dfd014a71"></a>
### Get prepared report result

`operation_foundation_desk_query_report_business_behavior_get_prepared_report_result`

**Inputs** report, filters, dn = empty text, user = no value.

**Record and data access** resolve a document from “Prepared Report” via get\_doc.

**State and service calls** msgprint with (translated “Prepared report render failed” + formatted text : {e}).

**Explicit results** mapping(“prepared\_report” → true, “doc” → doc, “error” → error) · (report\_data bitwise or mapping(“prepared\_report” → true, “doc” → doc)).

**Local steps**

- Bind dependencies get\_last\_processed\_prepared\_report.
- Bind local operation get\_report\_data for subsequent calls.
- Set report\_data from mapping().
- If not dn.
  - Set dn from get\_last\_processed\_prepared\_report(filters, user, (report.get(“custom\_report”) or report.get(“report\_name”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in report.get(“custom\_report”) → report.get(“report\_name”).
- Set doc from Platform.get\_doc(“Prepared Report”, dn) when dn, otherwise no value.
  - Value choice on dn — true gives Platform.get\_doc(“Prepared Report”, dn), false gives no value.
- If (doc and doc.status equals “Error”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.status equals “Error”.
  - Set error from get\_user\_facing\_error(doc.error\_message, keep\_line\_breaks = true).
  - Set doc.error\_message from no value.
  - Return mapping(“prepared\_report” → true, “doc” → doc, “error” → error).
- If doc.
  - Attempt the following.
    - If data bound to json.loads(doc.get\_prepared\_data().decode(“utf-8”)).
      - Set report\_data from get\_report\_data(doc, data).
  - On failure (Exception) bound to e.
    - Evaluate doc.log\_error(“Prepared report render failed”).
    - Evaluate Platform.msgprint((translated “Prepared report render failed” + formatted text : {e})).
    - Set doc from no value.
- Return (report\_data bitwise or mapping(“prepared\_report” → true, “doc” → doc)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L99) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L400)

<a id="op-f6eab82caeeeee"></a>
### Get prepared report result.get report data

`operation_foundation_desk_query_report_business_behavior_get_prepared_report_result_get_report_data`

**Inputs** doc, data.

**Explicit results** (data bitwise or mapping(“columns” → columns)).

**Local steps**

- If (doc.get(“columns”) or isinstance(data, list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“columns”) → isinstance(data, list).
  - Set columns from ((doc.get(“columns”) and json.loads(doc.columns)) or data at 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (doc.get(“columns”) and json.loads(doc.columns)) → data at 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“columns”) → json.loads(doc.columns).
  - Set data from mapping(“result” → data).
- Otherwise.
  - Set columns from data.get(“columns”).
- For each column in columns.
  - If (isinstance(column, dict) and column.get(“label”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(column, dict) → column.get(“label”).
    - Set column at “label” from translated column at “label”.
- Return (data bitwise or mapping(“columns” → columns)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L868) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L401)

<a id="op-c4fdb78500a2dd"></a>
### Export query

`operation_foundation_desk_query_report_business_behavior_export_query`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Report” via get\_cached\_value · read “User” via get\_cached\_value.

**State and service calls** enqueue with “Platform.desk.query\_report.run\_export\_query\_job” · msgprint with translated “Your report is being generated in the background. You will receive an email on {0} with a download link once …”.format(user\_email).

**Explicit results** no value · \_export\_query(form\_params, csv\_params).

**Local steps**

- Bind dependencies pop\_csv\_params.
- Set form\_params from Platform.\_dict(Platform.local.form\_dict).
- Set csv\_params from pop\_csv\_params(form\_params).
- Evaluate clean\_params(form\_params).
- Evaluate parse\_json(form\_params).
- Set report\_name from form\_params.report\_name.
- Evaluate Platform.permissions.can\_export(Platform.get\_cached\_value(“Report”, report\_name, “ref\_doctype”), raise\_exception = true).
- Set export\_in\_background from int((form\_params.export\_in\_background or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in form\_params.export\_in\_background → 0.
- If export\_in\_background.
  - Set user from Platform.session.user.
  - Set user\_email from Platform.get\_cached\_value(“User”, user, “email”).
  - Evaluate Platform.enqueue(“Platform.desk.query\_report.run\_export\_query\_job”, user\_email = user\_email, form\_params = form\_params, csv\_params = csv\_params, queue = “long”, …).
  - Evaluate Platform.msgprint(translated “Your report is being generated in the background. You will receive an email on {0} with a download link once …”.format(user\_email)).
  - Return no value.
- Return \_export\_query(form\_params, csv\_params).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Report”, report\_name, “ref\_doctype”), Platform.get\_cached\_value(“User”, user, “email”) · service or queued work from Platform.enqueue(“Platform.desk.query\_report.run\_export\_query\_job”, user\_email = user\_email, form\_params = form\_params, csv\_params = csv\_params, queue = “long”, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L1263) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L389)

<a id="op-38528e3cd36a2f"></a>
### Run export query job

`operation_foundation_desk_query_report_business_behavior_run_export_query_job`

**Inputs** user\_email, form\_params, csv\_params.

**Local steps**

- Bind dependencies send\_report\_email.
- Set tuple(report\_name, file\_extension, content) from \_export\_query(form\_params, csv\_params, populate\_response = false).
- Evaluate send\_report\_email(user\_email, report\_name, file\_extension, content, attached\_to\_name = form\_params.report\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L1827) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L414)

<a id="op-354af42e75237d"></a>
### Export query

`operation_foundation_desk_query_report_business_behavior_export_query_2`

**Inputs** form\_params, csv\_params, populate\_response = true.

**Explicit results** no value · tuple(report\_name, file\_extension, content).

**Explicit failure paths** validation helper.

**Local steps**

- Bind dependencies get\_csv\_bytes, provide\_binary\_file.
- Bind dependencies handle\_html, make\_xlsx.
- Set report\_name from form\_params.report\_name.
- Set file\_format\_type from form\_params.file\_format\_type.
- Set custom\_columns from Platform.parse\_json((form\_params.custom\_columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in form\_params.custom\_columns → “&#91;&#93;”.
- Set include\_indentation from form\_params.include\_indentation.
- Set include\_filters from form\_params.include\_filters.
- Set visible\_idx from (form\_params.visible\_idx or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in form\_params.visible\_idx → list().
- Set ignore\_visible\_idx from sbool(form\_params.get(“ignore\_visible\_idx”)).
- Set include\_hidden\_columns from form\_params.include\_hidden\_columns.
- If isinstance(visible\_idx, str).
  - Set visible\_idx from json.loads(visible\_idx).
- Set data from run(report\_name, form\_params.filters, custom\_columns = custom\_columns, are\_default\_filters = false).
- Set data from Platform.\_dict(data).
- Set data.report\_name from report\_name.
- Set data.filters from form\_params.filters.
- Set data.applied\_filters from form\_params.applied\_filters.
- If not data.columns.
  - Evaluate Platform.respond\_as\_web\_page(translated “No data to export”, translated “You can try changing the filters of your report.”).
  - Return no value.
- Set has\_total\_row from cint(data.get(“add\_total\_row”)).
- If (visible\_idx and not ignore\_visible\_idx).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in visible\_idx → not ignore\_visible\_idx.
  - Set row\_count from len(data.result).
  - Set filtered\_result from list of data.result at idx for idx drawn from visible\_idx where 0 ≤ idx &lt; row\_count.
    - Draw idx from visible\_idx, keep a combination only if (0 ≤ idx &lt; row\_count).
    - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ idx &lt; row\_count.
  - If has\_total\_row.
    - Set filtered\_result from add\_total\_row(filtered\_result, data.columns).
  - Set data at “result” from filtered\_result.
- Evaluate format\_fields(data, file\_format\_type).
- Set tuple(xlsx\_data, column\_widths, styles) from build\_xlsx\_data(data, include\_indentation = include\_indentation, include\_filters = include\_filters, include\_hidden\_columns = include\_hidden\_columns, build\_styles = file\_format\_type equals “Excel”).
- If file\_format\_type equals “CSV”.
  - Set file\_extension from “csv”.
  - Set content from get\_csv\_bytes(list of list of handle\_html(v) when isinstance(v, str), otherwise v for v drawn from r for r drawn from xlsx\_data, csv\_params).
    - Draw r from xlsx\_data.
    - Draw v from r.
    - Value choice on isinstance(v, str) — true gives handle\_html(v), false gives v.
- Otherwise.
  - If file\_format\_type equals “Excel”.
    - Set file\_extension from “xlsx”.
    - Set content from make\_xlsx(xlsx\_data, report\_name, column\_widths = column\_widths, styles = styles).getvalue().
  - Otherwise.
    - Call the validation error handler Platform.throw(title = translated “Unsupported file format: {0}”.format(file\_format\_type), msg = translated “Only CSV and Excel formats are supported for export”).
- If include\_filters.
  - For each value in (data.filters or mapping()).values().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.filters → mapping().
    - Set suffix from empty text.
    - If isinstance(value, list).
      - Set suffix from (“\_” + “,”.join(value)).
    - Otherwise.
      - If (isinstance(value, str) and value does not belong to set(“Yes”, “No”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → value does not belong to set(“Yes”, “No”).
        - Set suffix from formatted text \_{value}.
    - If valid\_report\_name(report\_name, suffix).
      - Update report\_name using + suffix.
- If not populate\_response.
  - Return tuple(report\_name, file\_extension, content).
- Evaluate provide\_binary\_file(translated report\_name, file\_extension, content).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L94) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L390)

<a id="op-6f17d835f32540"></a>
### Valid report name

`operation_foundation_desk_query_report_business_behavior_valid_report_name`

**Inputs** report\_name, suffix.

**Explicit results** true · false.

**Local steps**

- If (len(report\_name) + len(suffix)) &lt; 200.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L3577) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L417)

<a id="op-580082cbdf3b2f"></a>
### Format fields

`operation_foundation_desk_query_report_business_behavior_format_fields`

**Inputs** data, file\_format\_type = no value.

**Declared result** no value.

**Local steps**

- Set stringify\_dates from file\_format\_type differs from “Excel”.
- For each tuple(i, col) in enumerate(data.columns).
  - If col.get(“fieldtype”) equals “Duration”.
    - For each row in data.result.
      - Set index from col.get(“fieldname”) when isinstance(row, dict), otherwise i.
        - Value choice on isinstance(row, dict) — true gives col.get(“fieldname”), false gives i.
      - Set val from row.get(index) when isinstance(row, dict), otherwise row at index.
        - Value choice on isinstance(row, dict) — true gives row.get(index), false gives row at index.
      - If val.
        - Set row at index from format\_duration(val).
  - Otherwise.
    - If (col.get(“fieldtype”) equals “Currency” and col.get(“precision”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.get(“fieldtype”) equals “Currency” → col.get(“precision”).
      - For each row in data.result.
        - Set index from col.get(“fieldname”) when isinstance(row, dict), otherwise i.
          - Value choice on isinstance(row, dict) — true gives col.get(“fieldname”), false gives i.
        - Set val from row.get(index) when isinstance(row, dict), otherwise row at index.
          - Value choice on isinstance(row, dict) — true gives row.get(index), false gives row at index.
        - If val.
          - Set row at index from round(val, col.get(“precision”)).
    - Otherwise.
      - If (col.get(“fieldtype”) equals “Date” and stringify\_dates).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.get(“fieldtype”) equals “Date” → stringify\_dates.
        - For each row in data.result.
          - Set index from col.get(“fieldname”) when isinstance(row, dict), otherwise i.
            - Value choice on isinstance(row, dict) — true gives col.get(“fieldname”), false gives i.
          - Set val from row.get(index) when isinstance(row, dict), otherwise row at index.
            - Value choice on isinstance(row, dict) — true gives row.get(index), false gives row at index.
          - If val.
            - Set row at index from formatdate(val).
      - Otherwise.
        - If (col.get(“fieldtype”) equals “Datetime” and stringify\_dates).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.get(“fieldtype”) equals “Datetime” → stringify\_dates.
          - For each row in data.result.
            - Set index from col.get(“fieldname”) when isinstance(row, dict), otherwise i.
              - Value choice on isinstance(row, dict) — true gives col.get(“fieldname”), false gives i.
            - Set val from row.get(index) when isinstance(row, dict), otherwise row at index.
              - Value choice on isinstance(row, dict) — true gives row.get(index), false gives row at index.
            - If val.
              - Set row at index from format\_datetime(val).
        - Otherwise.
          - If col.get(“fieldtype”) belongs to tuple(“Link”, “Dynamic Link”).
            - For each row in data.result.
              - Set index from col.get(“fieldname”) when isinstance(row, dict), otherwise i.
                - Value choice on isinstance(row, dict) — true gives col.get(“fieldname”), false gives i.
              - Set val from row.get(index) when isinstance(row, dict), otherwise row at index.
                - Value choice on isinstance(row, dict) — true gives row.get(index), false gives row at index.
              - If (isinstance(val, str) and val.startswith(“'”) and val.endswith(“'”)).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(val, str) → val.startswith(“'”) → val.endswith(“'”).
                - Set row at index from val at slice 1 to negative 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L95) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L391)

<a id="op-72bf98c2076070"></a>
### Format filter value

`operation_foundation_desk_query_report_business_behavior_format_filter_value`

**Inputs** value.

**Explicit results** “, ”.join(list of cstr(x) for x drawn from value) when isinstance(value, list), otherwise cstr(value).

**Local steps**

- Return “, ”.join(list of cstr(x) for x drawn from value) when isinstance(value, list), otherwise cstr(value).
  - Value choice on isinstance(value, list) — true gives “, ”.join(list of cstr(x) for x drawn from value), false gives cstr(value).
  - Draw x from value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L4788) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L392)

<a id="op-00ee4594419bc9"></a>
### Build xlsx data

`operation_foundation_desk_query_report_business_behavior_build_spreadsheet_workbook_data`

**Inputs** data, visible\_idx = no value, include\_indentation = false, include\_filters = false, ignore\_visible\_idx = false, include\_hidden\_columns = false, build\_styles (named only, default false).

**Declared result** tuple at tuple(list at list at Any, list at int, (dict bitwise or no value)).

**Explicit results** tuple(result, column\_widths, get\_xlsx\_styles(metadata, data.report\_name) when build\_styles, otherwise no value).

**Local steps**

- Bind dependencies XLSXMetadata.
- Set metadata from no value.
- Set EXCEL\_TYPES from tuple(str, bool, type(no value), int, …).
- If (visible\_idx or ignore\_visible\_idx).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in visible\_idx → ignore\_visible\_idx.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
- If (not visible\_idx or len(visible\_idx) equals len(data.result)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not visible\_idx → len(visible\_idx) equals len(data.result).
  - Set ignore\_visible\_idx from true.
- Otherwise.
  - Set visible\_idx from set(visible\_idx).
- Set result from list().
- Set column\_data from list().
- Set column\_widths from list().
- Set excel\_row\_idx from 0.
- Set include\_filters from cint(include\_filters).
- Set include\_indentation from cint(include\_indentation).
- Set include\_hidden\_columns from cint(include\_hidden\_columns).
- Set has\_total\_row from sbool(data.get(“add\_total\_row”)).
- If build\_styles.
  - Set metadata from XLSXMetadata(report\_name = data.report\_name, filters = data.filters, has\_total\_row = has\_total\_row, has\_indentation = include\_indentation).
- If (include\_filters and data.applied\_filters).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in include\_filters → data.applied\_filters.
  - Set filter\_data from list().
  - For each tuple(filter\_name, filter\_value) in data.applied\_filters.items().
    - If not filter\_value.
      - Continue with the next iteration or loop test.
    - Set applied\_filter from list(cstr(filter\_name), format\_filter\_value(filter\_value)).
    - If build\_styles.
      - Set metadata.applied\_filters\_map at excel\_row\_idx from applied\_filter.
      - Update excel\_row\_idx using + 1.
    - Evaluate filter\_data.append(applied\_filter).
  - Evaluate filter\_data.append(list()).
  - Update excel\_row\_idx using + 1.
  - Update result using + filter\_data.
- Set column\_idx from 0.
- For each column in data.columns.
  - If (column.get(“hidden”) and not include\_hidden\_columns).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in column.get(“hidden”) → not include\_hidden\_columns.
    - Continue with the next iteration or loop test.
  - If build\_styles.
    - Set metadata.column\_map at column\_idx from column.
    - Update column\_idx using + 1.
  - Evaluate column\_data.append(translated column.get(“label”)).
  - Set column\_width from cint(column.get(“width”, 0)).
  - Update column\_width using ÷ 10.
  - Evaluate column\_widths.append(column\_width).
- Evaluate result.append(column\_data).
- Update excel\_row\_idx using + 1.
- Set handle\_indentation from (include\_indentation and not build\_styles).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in include\_indentation → not build\_styles.
- For each tuple(row\_idx, row) in enumerate(data.result).
  - If not (ignore\_visible\_idx or row\_idx belongs to visible\_idx).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_visible\_idx → row\_idx belongs to visible\_idx.
    - Continue with the next iteration or loop test.
  - Set row\_data from list().
  - Set row\_is\_dict from isinstance(row, dict).
  - Set indent from 0.
  - If (row\_is\_dict and handle\_indentation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row\_is\_dict → handle\_indentation.
    - Set indent from (row.get(“indent”) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“indent”) → 0.
    - If indent.
      - Set indent from cint(indent).
  - If build\_styles.
    - Set metadata.row\_map at excel\_row\_idx from row.
    - Update excel\_row\_idx using + 1.
  - For each tuple(col\_idx, column) in enumerate(data.columns).
    - If (column.get(“hidden”) and not include\_hidden\_columns).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in column.get(“hidden”) → not include\_hidden\_columns.
      - Continue with the next iteration or loop test.
    - Set label from column.get(“label”).
    - Set fieldname from column.get(“fieldname”).
    - Set cell\_value from row.get(fieldname, row.get(label, empty text)) when row\_is\_dict, otherwise row at col\_idx.
      - Value choice on row\_is\_dict — true gives row.get(fieldname, row.get(label, empty text)), false gives row at col\_idx.
    - If not isinstance(cell\_value, EXCEL\_TYPES).
      - Set cell\_value from cstr(cell\_value).
    - If (handle\_indentation and indent and col\_idx equals 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in handle\_indentation → indent → col\_idx equals 0.
      - Set cell\_value from ((4 spaces × indent) + cstr(cell\_value)).
    - Evaluate row\_data.append(cell\_value).
  - Evaluate result.append(row\_data).
- Return tuple(result, column\_widths, get\_xlsx\_styles(metadata, data.report\_name) when build\_styles, otherwise no value).
  - Value choice on build\_styles — true gives get\_xlsx\_styles(metadata, data.report\_name), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L4915) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L388)
