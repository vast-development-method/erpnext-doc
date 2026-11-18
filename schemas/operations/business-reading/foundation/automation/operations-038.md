# Workflow, automation and dispatch · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Reminder

[Record definition](../../../../data/record-types/reminder.json)

<a id="op-fb41eaf5037d50"></a>
### Reminder.validate

`operation_foundation_automation_record_definitions_reminder_business_behavior_reminder_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Reminder cannot be created in past.”.

**Local steps**

- Set self.user from Platform.session.user.
- If get\_datetime(self.remind\_at) &lt; now\_datetime().
  - Call the validation error handler Platform.throw(translated “Reminder cannot be created in past.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L3037) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L257)

<a id="op-ffc32341762de3"></a>
### Reminder.send reminder

`operation_foundation_automation_record_definitions_reminder_business_behavior_reminder_send_reminder`

**Inputs** self.

**State and service calls** call db\_set on self · request new\_doc for “Notification Log” · call insert on notification.

**Explicit results** no value.

**Local steps**

- If self.notified.
  - Return no value.
- Evaluate self.db\_set(“notified”, 1, update\_modified = false).
- Attempt the following.
  - Set notification from Platform.new\_doc(“Notification Log”).
  - Set notification.for\_user from self.user.
  - Evaluate notification.set(“type”, “Alert”).
  - Set notification.document\_type from self.reminder\_doctype.
  - Set notification.document\_name from self.reminder\_docname.
  - Set notification.subject from self.description.
  - Evaluate notification.insert().
- On failure (Exception).
  - Evaluate self.log\_error(“Failed to send reminder”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L3181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L256)

<a id="op-98ba25084360bf"></a>
### Create new reminder

`operation_foundation_automation_record_definitions_reminder_business_behavior_create_new_reminder`

**Inputs** remind\_at, description, reminder\_doctype = no value, reminder\_docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Reminder” · call insert on reminder.

**Explicit results** reminder.insert().

**Local steps**

- Set reminder from Platform.new\_doc(“Reminder”).
- Set reminder.description from description.
- Set reminder.remind\_at from remind\_at.
- Set reminder.reminder\_doctype from reminder\_doctype.
- Set reminder.reminder\_docname from reminder\_docname.
- Return reminder.insert().

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L3485) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L254)

<a id="op-1a7843ea5a8ee6"></a>
### Send reminders

`operation_foundation_automation_record_definitions_reminder_business_behavior_send_reminders`

**Inputs** no declared parameters.

**Record and data access** read “Reminder” via get\_all · resolve a document from “Reminder” via get\_doc.

**Local steps**

- Set job\_freq from (15 × 60).
- Set upper\_threshold from add\_to\_date(now\_datetime(), seconds = job\_freq, as\_string = true, as\_datetime = true).
- Set lower\_threshold from add\_to\_date(now\_datetime(), hours = negative 1, as\_string = true, as\_datetime = true).
- Set pending\_reminders from Platform.get\_all(“Reminder”, filters = list(tuple(“remind\_at”, “&lt;=”, upper\_threshold), tuple(“remind\_at”, “&gt;=”, lower\_threshold), tuple(“notified”, “=”, 0)), pluck = “name”, ignore\_ifnull = true).
- For each reminder in pending\_reminders.
  - Evaluate Platform.get\_doc(“Reminder”, reminder).send\_reminder().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L3718) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L258)

## Service · Resolver

<a id="op-bb93ec0a189b5b"></a>
### Resolve tool

`operation_foundation_binding_foundation_flow_lib_resolver_resolve_tool`

**Inputs** doc, restrict\_commit\_rollback (named only, default false).

**Declared result** Tool.

**Explicit results** \_resolve\_module(doc) · \_resolve\_script(doc, restrict\_commit\_rollback = restrict\_commit\_rollback).

**Local steps**

- If doc.type equals “Imported”.
  - Return \_resolve\_module(doc).
- Return \_resolve\_script(doc, restrict\_commit\_rollback = restrict\_commit\_rollback).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1291) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1267)

<a id="op-edb4032a2d52d5"></a>
### Resolve module

`operation_foundation_binding_foundation_flow_lib_resolver_resolve_module`

**Inputs** doc.

**Declared result** Tool.

**Explicit results** \_build\_tool(doc, obj.parameters, obj.func, requires\_confirmation = obj.requires\_confirmation, confirm\_prompt = obj.confirm\_prompt, background = obj.background, needs\_user = obj.needs\_user, …) · \_build\_tool(doc, build\_schema(obj), obj).

**Explicit failure paths** validation helper — translated “Could not import tool from {0}: {1}”.format(doc.import\_path, str(e)) · validation helper — translated “Import path {0} is not a Tool or callable.”.format(doc.import\_path).

**Local steps**

- Attempt the following.
  - Set obj from Platform.get\_attr(doc.import\_path).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Could not import tool from {0}: {1}”.format(doc.import\_path, str(e)), title = translated “Tool Import Failed”).
- If isinstance(obj, Tool).
  - Return \_build\_tool(doc, obj.parameters, obj.func, requires\_confirmation = obj.requires\_confirmation, confirm\_prompt = obj.confirm\_prompt, background = obj.background, needs\_user = obj.needs\_user, …).
- If callable(obj).
  - Return \_build\_tool(doc, build\_schema(obj), obj).
- Call the validation error handler Platform.throw(translated “Import path {0} is not a Tool or callable.”.format(doc.import\_path), title = translated “Invalid Tool”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(doc.import\_path).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1289) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1265)

<a id="op-67fde59cde1a0e"></a>
### Resolve script

`operation_foundation_binding_foundation_flow_lib_resolver_resolve_script`

**Inputs** doc, restrict\_commit\_rollback (named only, default false).

**Declared result** Tool.

**Explicit results** \_build\_tool(doc, schema, runner).

**Local steps**

- Set schema from schema\_from\_code(doc.code).
- Set runner from \_make\_script\_runner(doc.code, doc.slug, set(schema at “properties”), restrict\_commit\_rollback = restrict\_commit\_rollback).
- Return \_build\_tool(doc, schema, runner).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1290) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1266)

<a id="op-370f5b045855bd"></a>
### Build tool

`operation_foundation_binding_foundation_flow_lib_resolver_build_tool`

**Inputs** doc, parameters, func, requires\_confirmation (named only, default no value), confirm\_prompt (named only, default no value), background (named only, default no value), needs\_user (named only, default false), display\_template (named only, default no value).

**Declared result** Tool.

**Explicit results** Tool(name = tool\_call\_name(doc.name), description = doc.description, parameters = parameters, func = func, …).

**Local steps**

- Return Tool(name = tool\_call\_name(doc.name), description = doc.description, parameters = parameters, func = func, …).
  - Value choice on (callable(requires\_confirmation) and doc.requires\_confirmation) — true gives requires\_confirmation, false gives bool(doc.requires\_confirmation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in callable(requires\_confirmation) → doc.requires\_confirmation.
  - Value choice on callable(background) — true gives background, false gives bool(doc.background).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1258)

<a id="op-d2522a14e2ca64"></a>
### Make script runner

`operation_foundation_binding_foundation_flow_lib_resolver_make_script_runner`

**Inputs** code, slug, params, restrict\_commit\_rollback (named only, default false).

**Explicit results** run.

**Local steps**

- Bind local operation run for subsequent calls.
- Return run.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1262)

<a id="op-938adefa9a9ba7"></a>
### Make script runner.run

`operation_foundation_binding_foundation_flow_lib_resolver_make_script_runner_run`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** ctx, kwargs.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** ValueError.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1263)

<a id="op-e08fcab6012a87"></a>
### Schema from code

`operation_foundation_binding_foundation_flow_lib_resolver_schema_from_code`

**Inputs** code.

**Declared result** dict at tuple(str, Any).

**Explicit results** schema.

**Local steps**

- Set main from \_find\_main(ast.parse(code)).
- Set params from ((main.args.posonlyargs + main.args.args) + main.args.kwonlyargs).
- Set required from \_required\_arg\_names(main.args).
- Set properties from mapping of param.arg → \_annotation\_schema(param.annotation) for param drawn from params.
  - Draw param from params.
- Set schema from mapping(“type” → “object”, “properties” → properties, “additionalProperties” → false).
- Set ordered\_required from list of param.arg for param drawn from params where param.arg belongs to required.
  - Draw param from params, keep a combination only if (param.arg belongs to required).
- If ordered\_required.
  - Set schema at “required” from ordered\_required.
- Return schema.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1293) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1269)

<a id="op-f8da56cb0185b5"></a>
### Find main

`operation_foundation_binding_foundation_flow_lib_resolver_find_main`

**Inputs** tree.

**Declared result** ast.FunctionDef.

**Explicit results** node.

**Explicit failure paths** validation helper — translated “Code must define a top-level &lt;code&gt;main&lt;/code&gt; function.”.

**Local steps**

- For each node in tree.body.
  - If (isinstance(node, ast.FunctionDef) and node.name equals MAIN\_FUNCTION\_NAME).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ast.FunctionDef) → node.name equals MAIN\_FUNCTION\_NAME.
    - Return node.
- Call the validation error handler Platform.throw(translated “Code must define a top-level &lt;code&gt;main&lt;/code&gt; function.”, title = translated “Missing main()”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1259)

<a id="op-53eaaf11d793e2"></a>
### Required arg names

`operation_foundation_binding_foundation_flow_lib_resolver_required_arg_names`

**Inputs** params.

**Declared result** set at str.

**Explicit results** required.

**Local steps**

- Set required from set().
- Set positional from (params.posonlyargs + params.args).
- Set num\_required from (len(positional) − len(params.defaults)).
- For each tuple(i, arg) in enumerate(positional).
  - If i &lt; num\_required.
    - Evaluate required.add(arg.arg).
- For each tuple(arg, default) in zip(params.kwonlyargs, params.kw\_defaults, strict = true).
  - If default is identical to no value.
    - Evaluate required.add(arg.arg).
- Return required.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1264)

<a id="op-9802be68847ecc"></a>
### Annotation schema

`operation_foundation_binding_foundation_flow_lib_resolver_annotation_schema`

**Inputs** node.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping() · \_schema\_by\_name(node.id) · \_schema\_by\_name(node.attr) · \_schema\_by\_name(node.value) when isinstance(node.value, str), otherwise mapping() · \_subscript\_schema(node) · 1 additional forms in the steps below.

**Local steps**

- If node is identical to no value.
  - Return mapping().
- If isinstance(node, ast.Name).
  - Return \_schema\_by\_name(node.id).
- If isinstance(node, ast.Attribute).
  - Return \_schema\_by\_name(node.attr).
- If isinstance(node, ast.Constant).
  - Return \_schema\_by\_name(node.value) when isinstance(node.value, str), otherwise mapping().
    - Value choice on isinstance(node.value, str) — true gives \_schema\_by\_name(node.value), false gives mapping().
- If isinstance(node, ast.Subscript).
  - Return \_subscript\_schema(node).
- If (isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ast.BinOp) → isinstance(node.op, ast.BitOr).
  - Return \_union\_schema(list(node.left, node.right)).
- Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1257)

<a id="op-ce29a8eb881869"></a>
### Schema by name

`operation_foundation_binding_foundation_flow_lib_resolver_schema_by_name`

**Inputs** name.

**Declared result** dict at tuple(str, Any).

**Explicit results** dict(\_PRIMITIVE\_BY\_NAME at name) · mapping(“type” → “array”) · mapping(“type” → “object”) · mapping().

**Local steps**

- If name belongs to \_PRIMITIVE\_BY\_NAME.
  - Return dict(\_PRIMITIVE\_BY\_NAME at name).
- If name belongs to \_ARRAY\_NAMES.
  - Return mapping(“type” → “array”).
- If name belongs to \_OBJECT\_NAMES.
  - Return mapping(“type” → “object”).
- Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1292) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1268)

<a id="op-00919ec30df34a"></a>
### Subscript schema

`operation_foundation_binding_foundation_flow_lib_resolver_subscript_schema`

**Inputs** node.

**Declared result** dict at tuple(str, Any).

**Explicit results** \_literal\_schema(sliced) · \_annotated\_schema(sliced) · \_annotation\_schema(sliced) · \_union\_schema(elts) · mapping(“type” → “array”, “items” → items) when items, otherwise mapping(“type” → “array”) · 2 additional forms in the steps below.

**Local steps**

- Set base from node.value.
- Set base\_name from base.id when isinstance(base, ast.Name), otherwise base.attr when isinstance(base, ast.Attribute), otherwise no value.
  - Value choice on isinstance(base, ast.Name) — true gives base.id, false gives base.attr when isinstance(base, ast.Attribute), otherwise no value.
  - Value choice on isinstance(base, ast.Attribute) — true gives base.attr, false gives no value.
- Set sliced from node.slice.
- If base\_name equals “Literal”.
  - Return \_literal\_schema(sliced).
- If base\_name equals “Annotated”.
  - Return \_annotated\_schema(sliced).
- If base\_name equals “Optional”.
  - Return \_annotation\_schema(sliced).
- If base\_name equals “Union”.
  - Set elts from sliced.elts when isinstance(sliced, ast.Tuple), otherwise list(sliced).
    - Value choice on isinstance(sliced, ast.Tuple) — true gives sliced.elts, false gives list(sliced).
  - Return \_union\_schema(elts).
- If base\_name belongs to \_ARRAY\_NAMES.
  - Set element from sliced.elts at 0 when isinstance(sliced, ast.Tuple), otherwise sliced.
    - Value choice on isinstance(sliced, ast.Tuple) — true gives sliced.elts at 0, false gives sliced.
  - Set items from \_annotation\_schema(element).
  - Return mapping(“type” → “array”, “items” → items) when items, otherwise mapping(“type” → “array”).
    - Value choice on items — true gives mapping(“type” → “array”, “items” → items), false gives mapping(“type” → “array”).
- If base\_name belongs to \_OBJECT\_NAMES.
  - Return mapping(“type” → “object”).
- Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1270)

<a id="op-09a72d1ae75729"></a>
### Union schema

`operation_foundation_binding_foundation_flow_lib_resolver_union_schema`

**Inputs** nodes.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping() · schemas at 0 · mapping(“anyOf” → schemas).

**Local steps**

- Set schemas from list of \_annotation\_schema(n) for n drawn from nodes where not \_is\_none(n).
  - Draw n from nodes, keep a combination only if (not \_is\_none(n)).
- If not schemas.
  - Return mapping().
- If len(schemas) equals 1.
  - Return schemas at 0.
- Return mapping(“anyOf” → schemas).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1271)

<a id="op-e5820ee6525a8f"></a>
### Is none

`operation_foundation_binding_foundation_flow_lib_resolver_is_none`

**Inputs** node.

**Declared result** bool.

**Explicit results** node.value is identical to no value · (isinstance(node, ast.Name) and node.id equals “None”).

**Local steps**

- If isinstance(node, ast.Constant).
  - Return node.value is identical to no value.
- Return (isinstance(node, ast.Name) and node.id equals “None”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ast.Name) → node.id equals “None”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1260)

<a id="op-89a301ec2bf390"></a>
### Literal schema

`operation_foundation_binding_foundation_flow_lib_resolver_literal_schema`

**Inputs** sliced.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping() · schema.

**Local steps**

- Set elts from sliced.elts when isinstance(sliced, ast.Tuple), otherwise list(sliced).
  - Value choice on isinstance(sliced, ast.Tuple) — true gives sliced.elts, false gives list(sliced).
- Set values from list of e.value for e drawn from elts where isinstance(e, ast.Constant).
  - Draw e from elts, keep a combination only if (isinstance(e, ast.Constant)).
- If not values.
  - Return mapping().
- Set schema from mapping(“enum” → values).
- Set value\_types from set of type(v) for v drawn from values.
  - Draw v from values.
- If value\_types equals set(str).
  - Set schema at “type” from “string”.
- Otherwise.
  - If value\_types equals set(bool).
    - Set schema at “type” from “boolean”.
  - Otherwise.
    - If value\_types ≤ set(int).
      - Set schema at “type” from “integer”.
    - Otherwise.
      - If value\_types ≤ set(int, float).
        - Set schema at “type” from “number”.
- Return schema.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1261)

<a id="op-b2310171f52df5"></a>
### Annotated schema

`operation_foundation_binding_foundation_flow_lib_resolver_annotated_schema`

**Inputs** sliced.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping() · mapping(expand schema, “description” → meta.value) · schema.

**Local steps**

- If (not isinstance(sliced, ast.Tuple) or not sliced.elts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(sliced, ast.Tuple) → not sliced.elts.
  - Return mapping().
- Set schema from \_annotation\_schema(sliced.elts at 0).
- For each meta in sliced.elts at slice 1 to no value.
  - If (isinstance(meta, ast.Constant) and isinstance(meta.value, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(meta, ast.Constant) → isinstance(meta.value, str).
    - Return mapping(expand schema, “description” → meta.value).
- Return schema.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1256)

## Service · Retriever

<a id="op-c0302e963cbb5d"></a>
### Retrieve attachments

`operation_foundation_binding_foundation_flow_knowledge_retriever_retrieve_attachments`

**Inputs** query, session (named only), limit (named only, default DEFAULT\_LIMIT).

**Declared result** list at dict at tuple(str, Any).

**Record and data access** read “Flow Knowledge Settings” via get\_cached\_value.

**Explicit results** list() · attachment\_store.search(vector, session = session, text = text, limit = limit).

**Local steps**

- Set query from (query or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query → empty text.
- If (not query or not session).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not query → not session.
  - Return list().
- Bind dependencies attachment\_store.
- Bind dependencies embed\_texts.
- Set search\_type from Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “search\_type”).
- Set text from query when search\_type differs from “Vector”, otherwise no value.
  - Value choice on search\_type differs from “Vector” — true gives query, false gives no value.
- Set tuple(vector) from embed\_texts(list(query)).
- Return attachment\_store.search(vector, session = session, text = text, limit = limit).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “search\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L237) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1215)

<a id="op-e3ddec7c3c4e0a"></a>
### Retrieve

`operation_foundation_binding_foundation_flow_knowledge_retriever_retrieve`

**Inputs** query, kbs (named only), limit (named only, default DEFAULT\_LIMIT).

**Declared result** list at dict at tuple(str, Any).

**Record and data access** read “Flow Knowledge Settings” via get\_cached\_value.

**Explicit results** list() · results.

**Explicit failure paths** validation helper — translated “Knowledge search requires at least one knowledge base.”.

**Local steps**

- If not kbs.
  - Call the validation error handler Platform.throw(translated “Knowledge search requires at least one knowledge base.”, title = translated “No Knowledge Base”).
- Set query from (query or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query → empty text.
- If not query.
  - Return list().
- Set kbs from \_enabled\_kbs(kbs).
- If not kbs.
  - Return list().
- Bind dependencies store.
- Bind dependencies embed\_texts.
- Set search\_type from Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “search\_type”).
- Set text from query when search\_type differs from “Vector”, otherwise no value.
  - Value choice on search\_type differs from “Vector” — true gives query, false gives no value.
- Set tuple(vector) from embed\_texts(list(query)).
- Set hits from store.search(vector, text = text, kbs = kbs, limit = limit).
- If not hits.
  - Return list().
- Set chunks from \_hydrate(set of int(hit at “id”) for hit drawn from hits).
  - Draw hit from hits.
- Set titles from \_source\_titles(set of chunk at “source” for chunk drawn from chunks.values()).
  - Draw chunk from chunks.values().
- Set results from list().
- For each hit in hits.
  - Set chunk from chunks.get(int(hit at “id”)).
  - If chunk is identical to no value.
    - Continue with the next iteration or loop test.
  - Evaluate results.append(mapping(“content” → chunk at “content”, “score” → hit at “score”, “source” → titles.get(chunk at “source”, chunk at “source”), “reference\_doctype” → chunk.get(“reference\_doctype”), …)).
- Return results.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Flow Knowledge Settings”, “Flow Knowledge Settings”, “search\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L236) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1214)

<a id="op-bf97975166a6df"></a>
### Enabled kbs

`operation_foundation_binding_foundation_flow_knowledge_retriever_enabled_kbs`

**Inputs** kbs.

**Declared result** list at str.

**Record and data access** read KB\_DOCTYPE via get\_all.

**Explicit results** Platform.get\_all(KB\_DOCTYPE, filters = mapping(“name” → list(“in”, kbs), “enabled” → 1), pluck = “name”).

**Local steps**

- Return Platform.get\_all(KB\_DOCTYPE, filters = mapping(“name” → list(“in”, kbs), “enabled” → 1), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L234) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1212)

<a id="op-a1734347b9c1fe"></a>
### Hydrate

`operation_foundation_binding_foundation_flow_knowledge_retriever_hydrate`

**Inputs** ids.

**Declared result** dict at tuple(int, dict at tuple(str, Any)).

**Record and data access** read CHUNK\_DOCTYPE via get\_all.

**Explicit results** mapping of int(row at “name”) → row for row drawn from rows.

**Local steps**

- Set rows from Platform.get\_all(CHUNK\_DOCTYPE, filters = mapping(“name” → list(“in”, list(ids))), fields = list(“name”, “content”, “source”, “reference\_doctype”, …)).
- Return mapping of int(row at “name”) → row for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L235) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1213)
