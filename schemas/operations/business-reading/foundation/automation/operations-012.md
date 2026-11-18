# Workflow, automation and dispatch · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Builtins

<a id="op-3cfea508d67c54"></a>
### Summarize names

`operation_foundation_binding_foundation_flow_tools_builtins_summarize_names`

**Inputs** names, limit = 6.

**Declared result** str.

**Explicit results** (shown or “—”).

**Local steps**

- Set names from (names or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in names → list().
- Set shown from “, ”.join(generator of str(n) for n drawn from names at slice no value to limit).
  - Draw n from names at slice no value to limit.
- If len(names) &gt; limit.
  - Update shown using + formatted text  … +{(len(names) − limit)} more.
- Return (shown or “—”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in shown → “—”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1403)

<a id="op-351971e3cc4758"></a>
### Doc actions

`operation_foundation_binding_foundation_flow_tools_builtins_doc_actions`

**Inputs** doc, meta.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“lifecycle” → list of a for a drawn from lifecycle where a, “workflow” → sorted(\_workflow\_actions(doc)), “methods” → \_whitelisted\_methods(doc.doctype)).

**Local steps**

- Set lifecycle from list().
- If getattr(meta, “is\_submittable”, 0).
  - Evaluate lifecycle.append(\_LIFECYCLE\_BY\_DOCSTATUS.get(int(doc.docstatus))).
- If (int(doc.docstatus) differs from 1 and Platform.has\_permission(doc.doctype, “delete”, doc.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in int(doc.docstatus) differs from 1 → Platform.has\_permission(doc.doctype, “delete”, doc.name).
  - Evaluate lifecycle.append(“delete”).
- If getattr(meta, “allow\_rename”, 0).
  - Evaluate lifecycle.append(“rename”).
- Return mapping(“lifecycle” → list of a for a drawn from lifecycle where a, “workflow” → sorted(\_workflow\_actions(doc)), “methods” → \_whitelisted\_methods(doc.doctype)).
  - Draw a from lifecycle, keep a combination only if (a).

**Values supplied outside this operation** selected callable from getattr(meta, “is\_submittable”, 0), getattr(meta, “allow\_rename”, 0) · effective access from Platform.has\_permission(doc.doctype, “delete”, doc.name).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1365)

<a id="op-e7e85b20f18b0f"></a>
### Workflow actions

`operation_foundation_binding_foundation_flow_tools_builtins_workflow_actions`

**Inputs** doc.

**Declared result** set at str.

**Explicit results** set() · set of t.get(“action”) for t drawn from get\_transitions(doc) where t.get(“action”).

**Local steps**

- Bind dependencies get\_transitions, get\_workflow\_name.
- If not get\_workflow\_name(doc.doctype).
  - Return set().
- Attempt the following.
  - Return set of t.get(“action”) for t drawn from get\_transitions(doc) where t.get(“action”).
    - Draw t from get\_transitions(doc), keep a combination only if (t.get(“action”)).
- On failure (Exception).
  - Return set().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1412)

<a id="op-f91ed25f5e9170"></a>
### Whitelisted methods

`operation_foundation_binding_foundation_flow_tools_builtins_whitelisted_methods`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a structured result, the result of a delegated call.

**Local structure** 2 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1411)

<a id="op-a63b2e306c2e39"></a>
### Resolve method

`operation_foundation_binding_foundation_flow_tools_builtins_resolve_method`

**Inputs** doc, action.

**Declared result** Any.

**Explicit results** method · no value.

**Local steps**

- Set method from getattr(doc, action, no value).
- If (callable(method) and getattr(method, “\_\_func\_\_”, method) belongs to Platform.whitelisted).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in callable(method) → getattr(method, “\_\_func\_\_”, method) belongs to Platform.whitelisted.
  - Return method.
- Return no value.

**Values supplied outside this operation** selected callable from getattr(doc, action, no value), getattr(method, “\_\_func\_\_”, method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1391)

<a id="op-433c740eb827b1"></a>
### Apply action

`operation_foundation_binding_foundation_flow_tools_builtins_apply_action`

**Inputs** doctype, name, action, args.

**Declared result** Any.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call submit on doc · call cancel on doc · request copy\_doc for doc · call insert on amended.

**Explicit results** mapping(“name” → doc.name, “docstatus” → int(doc.docstatus)) · mapping(“name” → amended.name) · mapping(“name” → doc.name, “action” → action) · doc.run\_method(action, expanded names args).

**Explicit failure paths** ValueError(formatted text Unknown action {action} for {doctype}).

**Local steps**

- Set doc from Platform.get\_doc(doctype, name, check\_permission = true).
- If action equals “submit”.
  - Evaluate doc.submit().
  - Return mapping(“name” → doc.name, “docstatus” → int(doc.docstatus)).
- If action equals “cancel”.
  - Evaluate doc.cancel().
  - Return mapping(“name” → doc.name, “docstatus” → int(doc.docstatus)).
- If action equals “amend”.
  - Set amended from Platform.copy\_doc(doc).
  - Set amended.amended\_from from doc.name.
  - Evaluate amended.insert().
  - Return mapping(“name” → amended.name).
- If action belongs to \_workflow\_actions(doc).
  - Bind dependencies apply\_workflow.
  - Evaluate apply\_workflow(doc, action).
  - Return mapping(“name” → doc.name, “action” → action).
- If \_resolve\_method(doc, action) is distinct from no value.
  - Return doc.run\_method(action, expanded names args).
- Raise ValueError(formatted text Unknown action {action} for {doctype}).

**Values supplied outside this operation** selected callable from doc.run\_method(action, expanded names args).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1342)

<a id="op-8042fc5c29feb6"></a>
### Create

`operation_foundation_binding_foundation_flow_tools_builtins_create`

**Inputs** doctype, records, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = true, confirm\_prompt = deferred anonymous expression).

**Declared result** dict at tuple(str, Any).

**State and service calls** savepoint \_BATCH\_SAVEPOINT · request new\_doc for doctype · call insert on doc.

**Explicit results** mapping(“doctype” → doctype, “created” → created).

**Explicit failure paths** PermissionError(formatted text No permission to create {doctype}).

**Local steps**

- If not Platform.has\_permission(doctype, “create”).
  - Raise PermissionError(formatted text No permission to create {doctype}).
- Set created from list().
- Evaluate Platform.db.savepoint(\_BATCH\_SAVEPOINT).
- For each tuple(row, values) in enumerate(records).
  - Attempt the following.
    - Set doc from Platform.new\_doc(doctype).
    - Evaluate doc.update((values or mapping())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → mapping().
    - Evaluate doc.insert().
    - Evaluate created.append(doc.name).
  - On failure (Exception) bound to e.
    - Evaluate \_undo\_batch(formatted text Record {(row + 1)} of {len(records)}, e, ctx).
- Return mapping(“doctype” → doctype, “created” → created).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1360)

<a id="op-b815c4f2a580da"></a>
### Update

`operation_foundation_binding_foundation_flow_tools_builtins_update`

**Inputs** doctype, names, values, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = true, confirm\_prompt = deferred anonymous expression).

**Declared result** dict at tuple(str, Any).

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** savepoint \_BATCH\_SAVEPOINT · call save on doc.

**Explicit results** mapping(“doctype” → doctype, “updated” → updated).

**Explicit failure paths** Platform.PermissionError(translated “No permission to update {0} {1}.”.format(doctype, name)).

**Local steps**

- Set updated from list().
- Evaluate Platform.db.savepoint(\_BATCH\_SAVEPOINT).
- For each name in names.
  - Attempt the following.
    - If not Platform.has\_permission(doctype, “write”, name).
      - Raise Platform.PermissionError(translated “No permission to update {0} {1}.”.format(doctype, name)).
    - If Platform.get\_meta(doctype).istable.
      - Set tuple(doc, row) from \_parent\_and\_row(doctype, name).
      - Evaluate row.update((values or mapping())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → mapping().
    - Otherwise.
      - Set doc from Platform.get\_doc(doctype, name).
      - Evaluate doc.update((values or mapping())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → mapping().
    - Evaluate doc.save().
    - Evaluate updated.append(name).
  - On failure (Exception) bound to e.
    - Evaluate \_undo\_batch(name, e, ctx).
- Return mapping(“doctype” → doctype, “updated” → updated).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “write”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1408)

<a id="op-186117d9e1f9d1"></a>
### Delete

`operation_foundation_binding_foundation_flow_tools_builtins_delete`

**Inputs** doctype, names, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = true, confirm\_prompt = deferred anonymous expression).

**Declared result** dict at tuple(str, Any).

**State and service calls** savepoint \_BATCH\_SAVEPOINT · call save on parent · request delete\_doc for doctype.

**Explicit results** mapping(“doctype” → doctype, “deleted” → deleted).

**Explicit failure paths** Platform.PermissionError(translated “No permission to delete {0} {1}.”.format(doctype, name)).

**Local steps**

- Set deleted from list().
- Evaluate Platform.db.savepoint(\_BATCH\_SAVEPOINT).
- For each name in names.
  - Attempt the following.
    - If not Platform.has\_permission(doctype, “delete”, name).
      - Raise Platform.PermissionError(translated “No permission to delete {0} {1}.”.format(doctype, name)).
    - If Platform.get\_meta(doctype).istable.
      - Set tuple(parent, row) from \_parent\_and\_row(doctype, name).
      - Evaluate parent.remove(row).
      - Evaluate parent.save().
    - Otherwise.
      - Evaluate Platform.delete\_doc(doctype, name, ignore\_missing = false).
    - Evaluate deleted.append(name).
  - On failure (Exception) bound to e.
    - Evaluate \_undo\_batch(name, e, ctx).
- Return mapping(“doctype” → doctype, “deleted” → deleted).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “delete”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1361)

<a id="op-bdfeac960de15f"></a>
### Parent and row

`operation_foundation_binding_foundation_flow_tools_builtins_parent_and_row`

**Inputs** doctype, name.

**Declared result** tuple at tuple(Document, Document).

**Record and data access** read doctype via get\_value · resolve a document from parent.parenttype via get\_doc.

**Explicit results** tuple(doc, doc.getone(parent.parentfield, mapping(“name” → parent.name))).

**Explicit failure paths** Platform.DoesNotExistError(doctype = doctype).

**Local steps**

- Set parent from Platform.db.get\_value(doctype, name, list(“name”, “parenttype”, “parent”, “parentfield”), as\_dict = true).
- If not parent.
  - Raise Platform.DoesNotExistError(doctype = doctype).
- Set doc from Platform.get\_doc(parent.parenttype, parent.parent).
- Return tuple(doc, doc.getone(parent.parentfield, mapping(“name” → parent.name))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1380)

<a id="op-f0830ac554393d"></a>
### Call api prompt

`operation_foundation_binding_foundation_flow_tools_builtins_call_api_prompt`

**Inputs** call.

**Declared result** str.

**Record and data access** read “DocType” via exists.

**Explicit results** whitespace '\\n'.join(lines).

**Local steps**

- Set args from dict((call.get(“args”) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call.get(“args”) → mapping().
- Set lines from list().
- Set tuple(doctype, name) from tuple(args.get(“doctype”), args.get(“name”)).
- If (isinstance(doctype, str) and isinstance(name, str) and Platform.db.exists(“DocType”, doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(doctype, str) → isinstance(name, str) → Platform.db.exists(“DocType”, doctype).
  - Remove args at “doctype”, args at “name”.
  - Evaluate lines.append(formatted text {translated doctype}: {\_record\_title(doctype, name)}).
  - Evaluate lines.extend(\_field\_lines(doctype, args)).
- Evaluate lines.extend(generator of formatted text {translated Platform.unscrub(key)}: {\_in\_words(value)} for tuple(key, value) drawn from args.items()).
  - Draw tuple(key, value) from args.items().
- Return whitespace '\\n'.join(lines).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1356)

<a id="op-4f58ef244128e1"></a>
### Run action prompt

`operation_foundation_binding_foundation_flow_tools_builtins_run_action_prompt`

**Inputs** call.

**Declared result** str.

**Explicit results** \_call\_api\_prompt(call) · translated “Run '{0}' on {1} {2}: {3}”.format(action, len((call.get(“names”) or list())), call.get(“doctype”, “?”), \_summarize\_names(call.get(“names”))).

**Local steps**

- Set action from call.get(“action”).
- If is\_function\_path(action).
  - Return \_call\_api\_prompt(call).
- Return translated “Run '{0}' on {1} {2}: {3}”.format(action, len((call.get(“names”) or list())), call.get(“doctype”, “?”), \_summarize\_names(call.get(“names”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call.get(“names”) → list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1394)

<a id="op-07095035c4e3fd"></a>
### Field lines

`operation_foundation_binding_foundation_flow_tools_builtins_field_lines`

**Inputs** doctype, args.

**Declared result** list at str.

**Explicit results** list() · lines.

**Local steps**

- Set fieldname from args.get(“fieldname”).
- If (isinstance(fieldname, str) and “value” belongs to args).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fieldname, str) → “value” belongs to args.
  - Set values from mapping(fieldname → args at “value”).
  - Remove args at “fieldname”, args at “value”.
- Otherwise.
  - If isinstance(fieldname, dict).
    - Set values from args.pop(“fieldname”).
  - Otherwise.
    - Return list().
- Set meta from Platform.get\_meta(doctype).
- Set lines from list().
- For each tuple(field, value) in values.items().
  - Set df from meta.get\_field(field).
  - Set label from translated df.label when (df and df.label), otherwise translated Platform.unscrub(field).
    - Value choice on (df and df.label) — true gives translated df.label, false gives translated Platform.unscrub(field).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.label.
  - Set shown from Platform.format\_value(value, df) when (df and not isinstance(value, (list bitwise or dict))), otherwise value.
    - Value choice on (df and not isinstance(value, (list bitwise or dict))) — true gives Platform.format\_value(value, df), false gives value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → not isinstance(value, (list bitwise or dict)).
  - Evaluate lines.append(formatted text {label}: {\_in\_words(shown)}).
- Return lines.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1368)

<a id="op-5aa0422451cca4"></a>
### Record title

`operation_foundation_binding_foundation_flow_tools_builtins_record_title`

**Inputs** doctype, name.

**Declared result** str.

**Record and data access** read doctype via exists · read doctype via get\_value.

**Explicit results** name · (\_in\_words(Platform.db.get\_value(doctype, name, title\_field)) or name).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set title\_field from meta.get\_title\_field().
- If (meta.issingle or title\_field equals “name” or not Platform.db.exists(doctype, name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.issingle → title\_field equals “name” → not Platform.db.exists(doctype, name).
  - Return name.
- If not Platform.has\_permission(doctype, “read”, name).
  - Return name.
- Return (\_in\_words(Platform.db.get\_value(doctype, name, title\_field)) or name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_in\_words(Platform.db.get\_value(doctype, name, title\_field)) → name.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1387)

<a id="op-2f6dc3c8dba5ce"></a>
### In words

`operation_foundation_binding_foundation_flow_tools_builtins_in_words`

**Inputs** value.

**Declared result** str.

**Explicit results** “, ”.join(generator of \_in\_words(v) for v drawn from value) · “, ”.join(generator of formatted text {translated Platform.unscrub(k)}: {\_in\_words(v)} for tuple(k, v) drawn from value.items()) · (text at slice no value to \_CONFIRM\_STR\_LIMIT + “…”) when len(text) &gt; \_CONFIRM\_STR\_LIMIT, otherwise text.

**Local steps**

- If isinstance(value, list).
  - Return “, ”.join(generator of \_in\_words(v) for v drawn from value).
    - Draw v from value.
- If isinstance(value, dict).
  - Return “, ”.join(generator of formatted text {translated Platform.unscrub(k)}: {\_in\_words(v)} for tuple(k, v) drawn from value.items()).
    - Draw tuple(k, v) from value.items().
- Set text from one space.join(Platform.utils.strip\_html\_tags(str(value when nested operand in the contract is distinct from nested operand in the contract, otherwise empty text)).split()).
  - Value choice on value is distinct from no value — true gives value, false gives empty text.
- Return (text at slice no value to \_CONFIRM\_STR\_LIMIT + “…”) when len(text) &gt; \_CONFIRM\_STR\_LIMIT, otherwise text.
  - Value choice on len(text) &gt; \_CONFIRM\_STR\_LIMIT — true gives (text at slice no value to \_CONFIRM\_STR\_LIMIT + “…”), false gives text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1373)

<a id="op-b7bfabe80c8f43"></a>
### Run action

`operation_foundation_binding_foundation_flow_tools_builtins_run_action`

**Inputs** doctype, names, action, args = no value, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = deferred anonymous expression, confirm\_prompt = \_run\_action\_prompt).

**Declared result** dict at tuple(str, Any).

**Explicit results** call\_api(method = action, args = args, ctx = ctx) · \_run\_action(doctype, names, action, args, ctx = ctx).

**Local steps**

- If is\_function\_path(action).
  - Return call\_api(method = action, args = args, ctx = ctx).
- Return \_run\_action(doctype, names, action, args, ctx = ctx).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1392)

<a id="op-da51fd25a75b11"></a>
### Call api

`operation_foundation_binding_foundation_flow_tools_builtins_call_api`

**Inputs** method, args = no value, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = deferred anonymous expression, confirm\_prompt = \_call\_api\_prompt).

**Declared result** dict at tuple(str, Any).

**Explicit results** \_call\_api(method, args, ctx = ctx) · result.

**Explicit failure paths** ValueError(translated “{0} tried to write, so it is not a read. Nothing was saved.”.format(method)).

**Local steps**

- If not is\_read\_function(method).
  - Return \_call\_api(method, args, ctx = ctx).
- Within Platform.db.read\_only().
  - Set result from \_call\_api(method, args, ctx = ctx).
  - If Platform.db.transaction\_writes.
    - Raise ValueError(translated “{0} tried to write, so it is not a read. Nothing was saved.”.format(method)).
  - Return result.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1354)

<a id="op-825a21974201a4"></a>
### Call api

`operation_foundation_binding_foundation_flow_tools_builtins_call_api_8e6497c8682c`

**Inputs** method, args = no value, ctx (named only).

**Declared result** dict at tuple(str, Any).

**State and service calls** savepoint \_BATCH\_SAVEPOINT.

**Explicit results** mapping(“action” → method, “title” → function\_title(method), “result” → result).

**Explicit failure paths** validation helper — translated “Pass a whitelisted API's path from find\_apis.”.

**Local steps**

- Set args from (args or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → mapping().
- Set script from \_api\_server\_script(method).
- If (not script and not is\_function\_path(method)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not script → not is\_function\_path(method).
  - Call the validation error handler Platform.throw(translated “Pass a whitelisted API's path from find\_apis.”, title = translated “Invalid API”).
- Evaluate Platform.db.savepoint(\_BATCH\_SAVEPOINT).
- Attempt the following.
  - If script.
    - Set call from partial(run\_server\_script, script).
  - Otherwise.
    - Set fn from Platform.get\_attr(Platform.override\_whitelisted\_method(method)).
    - Evaluate Platform.is\_whitelisted(fn).
    - Set call from partial(Platform.call, fn, expanded names args).
  - Set result from \_call\_as\_request(call, args).
- On failure (Exception) bound to e.
  - Evaluate \_undo\_batch(method, e, ctx).
- If isinstance(result, Document).
  - Set result from result.as\_dict(no\_nulls = true).
- Return mapping(“action” → method, “title” → function\_title(method), “result” → result).

**Values supplied outside this operation** selected callable from Platform.get\_attr(Platform.override\_whitelisted\_method(method)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1355)

<a id="op-8af0c75852e21e"></a>
### Run action

`operation_foundation_binding_foundation_flow_tools_builtins_run_action_d0110d59d36a`

**Inputs** doctype, names, action, args = no value, ctx (named only).

**Declared result** dict at tuple(str, Any).

**State and service calls** request rename\_doc for doctype · savepoint \_BATCH\_SAVEPOINT.

**Explicit results** \_call\_api(action, args, ctx = ctx) · mapping(“action” → “rename”, “old” → names at 0, “new” → Platform.rename\_doc(doctype, names at 0, new\_name)) · mapping(“action” → action, “results” → results).

**Explicit failure paths** ValueError(“rename acts on a single document; pass exactly one name.”) · ValueError(“rename requires args.new\_name.”).

**Local steps**

- Set args from (args or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → mapping().
- If is\_function\_path(action).
  - Return \_call\_api(action, args, ctx = ctx).
- If action equals “rename”.
  - If len(names) differs from 1.
    - Raise ValueError(“rename acts on a single document; pass exactly one name.”).
  - Set new\_name from args.get(“new\_name”).
  - If not new\_name.
    - Raise ValueError(“rename requires args.new\_name.”).
  - Return mapping(“action” → “rename”, “old” → names at 0, “new” → Platform.rename\_doc(doctype, names at 0, new\_name)).
- Set results from list().
- Evaluate Platform.db.savepoint(\_BATCH\_SAVEPOINT).
- For each name in names.
  - Attempt the following.
    - Evaluate results.append(mapping(“name” → name, “result” → \_apply\_action(doctype, name, action, args))).
  - On failure (Exception) bound to e.
    - Evaluate \_undo\_batch(name, e, ctx).
- Return mapping(“action” → action, “results” → results).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1393)

<a id="op-571fecf6771d8e"></a>
### Read screen

`operation_foundation_binding_foundation_flow_tools_builtins_read_screen`

**Inputs** ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** Pending.

**State and service calls** publish realtime with SCREEN\_EVENT.

**Explicit results** Pending(timeout = SCREEN\_TIMEOUT).

**Explicit failure paths** validation helper — translated “read\_screen can only answer a call that waits for a result.”.

**Local steps**

- If not ctx.result\_token.
  - Call the validation error handler Platform.throw(translated “read\_screen can only answer a call that waits for a result.”).
- Evaluate Platform.publish\_realtime(SCREEN\_EVENT, mapping(“session” → ctx.session\_id, “token” → ctx.result\_token), user = ctx.user).
- Return Pending(timeout = SCREEN\_TIMEOUT).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(SCREEN\_EVENT, mapping(“session” → ctx.session\_id, “token” → ctx.result\_token), user = ctx.user).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1385)

<a id="op-23d0070f9e59a4"></a>
### Undo batch

`operation_foundation_binding_foundation_flow_tools_builtins_undo_batch`

**Inputs** record, error, ctx.

**Declared result** NoReturn.

**State and service calls** rollback.

**Explicit failure paths** failure.

**Local steps**

- Attempt the following.
  - Evaluate Platform.db.rollback(save\_point = \_BATCH\_SAVEPOINT).
  - Set undone from “Nothing was saved.”.
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Set undone from “Some earlier changes may already be committed; check the records before retrying.”.
- Set failure from ValueError(formatted text {record}: {\_error\_text(error)} {undone}).
- Set failure.\_\_cause\_\_ from error.
- Set ctx.failure from failure.
- Raise failure.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1407)

<a id="op-6fadcf882f2bb3"></a>
### Call as request

`operation_foundation_binding_foundation_flow_tools_builtins_call_as_request`

**Inputs** call, args.

**Declared result** Any.

**Explicit results** Platform.response.get(“message”) when result is identical to no value, otherwise result.

**Explicit failure paths** ValueError(formatted text It replies with a {Platform.response.type} file, not data, so it can't run here.).

**Local steps**

- Set tuple(form\_dict, response) from tuple(Platform.local.form\_dict, Platform.local.response).
- Set tuple(Platform.local.form\_dict, Platform.local.response) from tuple(Platform.\_dict(args), Platform.\_dict(mapping(“docs” → list()))).
- Attempt the following.
  - Set result from call().
  - If Platform.response.get(“type”).
    - Raise ValueError(formatted text It replies with a {Platform.response.type} file, not data, so it can't run here.).
  - Return Platform.response.get(“message”) when result is identical to no value, otherwise result.
    - Value choice on result is identical to no value — true gives Platform.response.get(“message”), false gives result.
- On exit, including pending return or failure.
  - Set tuple(Platform.local.form\_dict, Platform.local.response) from tuple(form\_dict, response).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1357)

<a id="op-205cc75a8db8e7"></a>
### Is function path

`operation_foundation_binding_foundation_flow_tools_builtins_is_function_path`

**Inputs** action.

**Declared result** bool.

**Explicit results** (isinstance(action, str) and bool(re.fullmatch(“\\w+(\\.\\w+)+”, action))).

**Local steps**

- Return (isinstance(action, str) and bool(re.fullmatch(“\\w+(\\.\\w+)+”, action))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(action, str) → bool(re.fullmatch(“\\w+(\\.\\w+)+”, action)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1374)

<a id="op-7dd5ef391e2fed"></a>
### Is read function

`operation_foundation_binding_foundation_flow_tools_builtins_is_read_function`

**Inputs** path.

**Declared result** bool.

**Explicit results** false · (method belongs to Platform.whitelisted and getattr(method, “read\_only”, false)).

**Local steps**

- If (not is\_function\_path(path) or \_api\_server\_script(path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_function\_path(path) → \_api\_server\_script(path).
  - Return false.
- Attempt the following.
  - Set method from Platform.get\_attr(Platform.override\_whitelisted\_method(path)).
- On failure (Exception).
  - Return false.
- Return (method belongs to Platform.whitelisted and getattr(method, “read\_only”, false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method belongs to Platform.whitelisted → getattr(method, “read\_only”, false).

**Values supplied outside this operation** selected callable from Platform.get\_attr(Platform.override\_whitelisted\_method(path)), getattr(method, “read\_only”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1375)
