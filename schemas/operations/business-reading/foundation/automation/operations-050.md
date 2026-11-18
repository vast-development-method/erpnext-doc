# Workflow, automation and dispatch · operations 50

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Store

<a id="op-a409df15c1da2f"></a>
### Make personal

`operation_foundation_binding_foundation_flow_memory_store_make_personal`

**Inputs** names, user.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not names.
  - Return no value.
- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is distinct from no value.
    - Evaluate db.execute(formatted text update {TABLE\_NAME} set scope = 'User', user = ? where id in ({\_placeholders(names)}), list(user, expanded names)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1326)

<a id="op-b42f5d9ddb44b0"></a>
### Search

`operation_foundation_binding_foundation_flow_memory_store_search`

**Inputs** query, agent (named only), user (named only).

**Declared result** list at str.

**Explicit results** list() · keyword · list of name for tuple(\_score, name) drawn from scored at slice no value to TOP\_K.

**Local steps**

- Set dimension from ensure\_table().
- Set scope from “agent = ? and (scope = 'Agent' or user = ?)”.
- Within \_connect() bound as db.
  - If not db.execute(formatted text select 1 from {TABLE\_NAME} where {scope} limit 1, tuple(agent, user)).fetchone().
    - Return list().
  - Set keyword from \_keyword\_search(db, TABLE\_NAME, scope, list(agent, user), column = “id”, …).
- If not dimension.
  - Return keyword.
- Bind dependencies embed\_texts.
- Set tuple(vector) from embed\_texts(list(query)).
- Within \_connect() bound as db.
  - Set nearest from db.execute(formatted text select id, vec\_distance\_cosine(vector, ?) as distance from {TABLE\_NAME} where {scope} and distance is not null, tuple(\_vector\_bytes(vector), agent, user)).fetchall().
- Set scored from list().
- For each tuple(name, distance) in nearest.
  - Set score from ((1.0 − distance) + KEYWORD\_BONUS when name belongs to keyword, otherwise 0.0).
    - Value choice on name belongs to keyword — true gives KEYWORD\_BONUS, false gives 0.0.
  - If score ≥ MIN\_SCORE.
    - Evaluate scored.append(tuple(score, name)).
- Evaluate scored.sort(reverse = true).
- Return list of name for tuple(\_score, name) drawn from scored at slice no value to TOP\_K.
  - Draw tuple(\_score, name) from scored at slice no value to TOP\_K.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1330)

<a id="op-ead22161dd3a80"></a>
### Drop table

`operation_foundation_binding_foundation_flow_memory_store_drop_table`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Within \_connect(write = true) bound as db.
  - Evaluate \_drop\_table(db, TABLE\_NAME).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1323)

<a id="op-2f063aaa0c3ea3"></a>
### Ensure table

`operation_foundation_binding_foundation_flow_memory_store_ensure_table`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “Flow Agent Memory” via get\_all.

**Explicit results** dimension.

**Local steps**

- Set tuple(dimension, shape) from \_dimension\_and\_shape().
- Within \_connect() bound as db.
  - If \_shape(db, TABLE\_NAME) equals shape.
    - Return dimension.
- Set docs from Platform.get\_all(“Flow Agent Memory”, filters = mapping(“status” → “Active”), fields = list(“name”, “agent”, “scope”, “user”, …)).
- Set rows from \_rows(docs, dimension).
- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) equals shape.
    - Return dimension.
  - Evaluate \_drop\_table(db, TABLE\_NAME).
  - Evaluate \_create\_table(db, TABLE\_NAME, “seq integer primary key, id text unique, agent text, scope text, user text”, dimension, …).
  - Evaluate db.execute(formatted text create index {TABLE\_NAME}\_agent on {TABLE\_NAME}(agent)).
  - Evaluate \_insert(db, rows).
- Return dimension.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1324)

<a id="op-81964eeb273dd5"></a>
### Dimension and shape

`operation_foundation_binding_foundation_flow_memory_store_dimension_and_shape`

**Inputs** no declared parameters.

**Declared result** tuple at tuple(int, str).

**Record and data access** resolve a document from “Flow Knowledge Settings” via get\_cached\_doc · read “Flow Model” via get\_cached\_value.

**Explicit results** tuple(0, “0”) · tuple(dimension, formatted text {dimension} {model\_id} {(base\_url or empty text)}.strip()).

**Local steps**

- Set settings from Platform.get\_cached\_doc(“Flow Knowledge Settings”).
- If not (settings.embedding\_model and settings.embedding\_dimension).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.embedding\_model → settings.embedding\_dimension.
  - Return tuple(0, “0”).
- Set tuple(model\_id, base\_url) from Platform.get\_cached\_value(“Flow Model”, settings.embedding\_model, list(“model\_id”, “base\_url”)).
- Set dimension from int(settings.embedding\_dimension).
- Return tuple(dimension, formatted text {dimension} {model\_id} {(base\_url or empty text)}.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in base\_url → empty text.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Flow Knowledge Settings”), Platform.get\_cached\_value(“Flow Model”, settings.embedding\_model, list(“model\_id”, “base\_url”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1322)

<a id="op-bea7061a313835"></a>
### Rows

`operation_foundation_binding_foundation_flow_memory_store_rows`

**Inputs** docs, dimension.

**Declared result** list at tuple.

**Explicit results** list of tuple(doc.name, doc.agent, doc.scope, (doc.user or empty text), …) for tuple(doc, vector) drawn from zip(docs, vectors, strict = true).

**Local steps**

- Set vectors from (list(no value) × len(docs)).
- If (dimension and docs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension → docs.
  - Bind dependencies embed\_texts.
  - Set vectors from list of \_vector\_bytes(vector) for vector drawn from embed\_texts(list of doc.content for doc drawn from docs).
    - Draw vector from embed\_texts(list of doc.content for doc drawn from docs).
    - Draw doc from docs.
- Return list of tuple(doc.name, doc.agent, doc.scope, (doc.user or empty text), …) for tuple(doc, vector) drawn from zip(docs, vectors, strict = true).
  - Draw tuple(doc, vector) from zip(docs, vectors, strict = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.user → empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1329)

<a id="op-253da399b6b74a"></a>
### Insert

`operation_foundation_binding_foundation_flow_memory_store_insert`

**Inputs** db, rows.

**Declared result** no value.

**Local steps**

- Evaluate db.executemany(formatted text insert into {TABLE\_NAME}(id, agent, scope, user, content, vector) values (?, ?, ?, ?, ?, ?), rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1325)

## Service · System generated

<a id="op-16ec6403563a96"></a>
### Validate immutable

`operation_foundation_binding_foundation_flow_utils_system_generated_validate_immutable`

**Inputs** doc, fields = tuple().

**Declared result** no value.

**Record and data access** read doc.doctype via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot remove the system-generated flag from {0} {1}.”.format(translated doc.doctype, doc.name) · validation helper — translated “Cannot change {0} of system-generated {1} {2}.”.format(translated doc.meta.get\_label(fieldname), translated doc.doctype, doc.name).

**Local steps**

- If (doc.is\_new() or doc.flags.ignore\_permissions).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → doc.flags.ignore\_permissions.
  - Return no value.
- Set tables from list of f for f drawn from fields where doc.meta.get\_field(f).fieldtype equals “Table MultiSelect”.
  - Draw f from fields, keep a combination only if (doc.meta.get\_field(f).fieldtype equals “Table MultiSelect”).
- Set columns from list of f for f drawn from fields where f does not belong to tables.
  - Draw f from fields, keep a combination only if (f does not belong to tables).
- Set before from Platform.db.get\_value(doc.doctype, doc.name, list(“is\_system\_generated”, expanded columns), as\_dict = true).
- If (not before or not before.is\_system\_generated).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not before → not before.is\_system\_generated.
  - Return no value.
- If not doc.is\_system\_generated.
  - Call the validation error handler Platform.throw(translated “Cannot remove the system-generated flag from {0} {1}.”.format(translated doc.doctype, doc.name), title = translated “Protected”).
- For each fieldname in fields.
  - If fieldname belongs to tables.
    - Set tuple(saved, current) from \_table\_links(doc, fieldname).
  - Otherwise.
    - Set tuple(saved, current) from tuple(before.get(fieldname), doc.get(fieldname)).
  - If saved differs from current.
    - Call the validation error handler Platform.throw(translated “Cannot change {0} of system-generated {1} {2}.”.format(translated doc.meta.get\_label(fieldname), translated doc.doctype, doc.name), title = translated “Protected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1454)

<a id="op-b9225849499506"></a>
### Table links

`operation_foundation_binding_foundation_flow_utils_system_generated_table_links`

**Inputs** doc, fieldname.

**Declared result** tuple at tuple(list, list).

**Record and data access** read df.options via get\_all.

**Explicit results** tuple(saved, list of row.get(link) for row drawn from doc.get(fieldname)).

**Local steps**

- Set df from doc.meta.get\_field(fieldname).
- Set link from next(generator of f.fieldname for f drawn from Platform.get\_meta(df.options).fields where f.fieldtype equals “Link”).
  - Draw f from Platform.get\_meta(df.options).fields, keep a combination only if (f.fieldtype equals “Link”).
- Set saved from Platform.get\_all(df.options, mapping(“parent” → doc.name, “parentfield” → fieldname), pluck = link, order\_by = “idx”).
- Return tuple(saved, list of row.get(link) for row drawn from doc.get(fieldname)).
  - Draw row from doc.get(fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1453)

<a id="op-2c2ff53a4d53bc"></a>
### Block delete

`operation_foundation_binding_foundation_flow_utils_system_generated_block_delete`

**Inputs** doc, always = false.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot delete system-generated {0} {1}.”.format(translated doc.doctype, doc.name).

**Local steps**

- If (doc.is\_system\_generated and (always or not doc.flags.ignore\_permissions)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_system\_generated → (always or not doc.flags.ignore\_permissions).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in always → not doc.flags.ignore\_permissions.
  - Call the validation error handler Platform.throw(translated “Cannot delete system-generated {0} {1}.”.format(translated doc.doctype, doc.name), title = translated “Protected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1447)

<a id="op-06c127063e48b3"></a>
### Block rename

`operation_foundation_binding_foundation_flow_utils_system_generated_block_rename`

**Inputs** doc, old.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot rename system-generated {0} {1}.”.format(translated doc.doctype, old).

**Local steps**

- If doc.is\_system\_generated.
  - Call the validation error handler Platform.throw(translated “Cannot rename system-generated {0} {1}.”.format(translated doc.doctype, old), title = translated “Protected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1449)

<a id="op-64745f9d4e2f54"></a>
### Block insert

`operation_foundation_binding_foundation_flow_utils_system_generated_block_insert`

**Inputs** doc.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Only an app can create a system-generated {0}.”.format(translated doc.doctype).

**Local steps**

- If ((doc.is\_system\_generated or doc.app) and not doc.flags.ignore\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (doc.is\_system\_generated or doc.app) → not doc.flags.ignore\_permissions.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_system\_generated → doc.app.
  - Call the validation error handler Platform.throw(translated “Only an app can create a system-generated {0}.”.format(translated doc.doctype), title = translated “Protected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1448)

<a id="op-d77b23ef785aab"></a>
### Block slash in name

`operation_foundation_binding_foundation_flow_utils_system_generated_block_slash_in_name`

**Inputs** doc, name = no value.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} names cannot contain /.”.format(translated doc.doctype).

**Local steps**

- If (not doc.app and “/” belongs to (name or doc.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.app → “/” belongs to (name or doc.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → doc.name.
  - Call the validation error handler Platform.throw(translated “{0} names cannot contain /.”.format(translated doc.doctype), title = translated “Invalid Name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1450)

<a id="op-484b6d006302ec"></a>
### Log skipped

`operation_foundation_binding_foundation_flow_utils_system_generated_log_skipped`

**Inputs** title, reason.

**Declared result** no value.

**Local steps**

- Evaluate click.secho(formatted text {title}: {Platform.utils.strip\_html\_tags(reason)}, fg = “yellow”).
- Evaluate Platform.log\_error(title = title, message = reason).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1451)

<a id="op-810013a8256206"></a>
### Skip if invalid

`operation_foundation_binding_foundation_flow_utils_system_generated_skip_if_invalid`

**Inputs** title.

**Wrappers, in declaration order** contextmanager.

**State and service calls** savepoint savepoint · rollback · release savepoint savepoint.

**Local steps**

- Set savepoint from formatted text flow\_{Platform.generate\_hash(length = 10)}.
- Evaluate Platform.db.savepoint(savepoint).
- Attempt the following.
  - yield no value.
- On failure (Platform.ValidationError) bound to e.
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Evaluate log\_skipped(title, str(e)).
- When the protected block completes normally.
  - Evaluate Platform.db.release\_savepoint(savepoint).

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1452)

## Service · Tool

<a id="op-7c9fd321b9837e"></a>
### Tool.post init

`operation_foundation_binding_foundation_flow_lib_tool_tool_post_init`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** TypeError(formatted text Tool {self.name} must take ′\*, ctx: ToolContext′.) · ValueError(formatted text Tool {self.name}'s display template names unknown argument(s): {names}.).

**Local steps**

- If “ctx” does not belong to inspect.signature(self.func).parameters.
  - Raise TypeError(formatted text Tool {self.name} must take ′\*, ctx: ToolContext′.).
- If self.display\_template.
  - Bind dependencies display\_template\_variables.
  - Set unknown from (set(display\_template\_variables(self.display\_template)) − set(self.parameters.get(“properties”, mapping()))).
  - If unknown.
    - Set names from “, ”.join(sorted(unknown)).
    - Raise ValueError(formatted text Tool {self.name}'s display template names unknown argument(s): {names}.).
- Bind dependencies ConfigDict, validate\_call.
- Set self.\_validated from validate\_call(config = ConfigDict(arbitrary\_types\_allowed = true))(self.func).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1303)

<a id="op-547c6d4a6aa689"></a>
### Tool.invoke

`operation_foundation_binding_foundation_flow_lib_tool_tool_call`

**Inputs** self, remaining named values kwargs.

**Declared result** Any.

**Explicit results** self.\_validated(expanded names kwargs).

**Local steps**

- Return self.\_validated(expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1302)

<a id="op-297b3592265292"></a>
### Tool.to dict

`operation_foundation_binding_foundation_flow_lib_tool_tool_to_dict`

**Inputs** self.

**Declared result** dict at tuple(str, Any).

**Explicit results** schema.

**Local steps**

- Set schema from mapping(“type” → “function”, “function” → mapping(“name” → self.name, “description” → self.description, “parameters” → self.parameters)).
- If self.display\_template.
  - Set schema at “display\_template” from self.display\_template.
- Return schema.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1304)

<a id="op-dce642eb9efbf6"></a>
### Tool

`operation_foundation_binding_foundation_flow_lib_tool_tool`

**Inputs** func = no value, name (named only, default no value), description (named only, default no value), requires\_confirmation (named only, default false), confirm\_prompt (named only, default no value), background (named only, default false), needs\_user (named only, default false), display\_template (named only, default no value).

**Declared result** (Tool bitwise or Callable at tuple(list(Callable at tuple(ellipsis, Any)), Tool)).

**Explicit results** wrap(func) when func is distinct from no value, otherwise wrap.

**Local steps**

- Bind local operation wrap for subsequent calls.
- Return wrap(func) when func is distinct from no value, otherwise wrap.
  - Value choice on func is distinct from no value — true gives wrap(func), false gives wrap.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1301)

<a id="op-3edb22357fb961"></a>
### Tool.wrap

`operation_foundation_binding_foundation_flow_lib_tool_tool_wrap`

**Inputs** f.

**Declared result** Tool.

**Explicit results** Tool(name = (name or f.\_\_name\_\_), description = (description or (nested operand in the contract.getdoc(f) or empty text).strip()), parameters = build\_schema(f), func = f, …).

**Explicit failure paths** TypeError(“@tool can only be applied to callables”).

**Local steps**

- If not callable(f).
  - Raise TypeError(“@tool can only be applied to callables”).
- Return Tool(name = (name or f.\_\_name\_\_), description = (description or (nested operand in the contract.getdoc(f) or empty text).strip()), parameters = build\_schema(f), func = f, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → f.\_\_name\_\_.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in description → (inspect.getdoc(f) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in inspect.getdoc(f) → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1305)

<a id="op-717775ef408c02"></a>
### Build schema

`operation_foundation_binding_foundation_flow_lib_tool_build_schema`

**Inputs** func.

**Declared result** dict at tuple(str, Any).

**Explicit results** schema.

**Local steps**

- Set sig from inspect.signature(func).
- Set hints from get\_type\_hints(func, include\_extras = true).
- Set properties from mapping().
- Set required from list().
- For each tuple(param\_name, param) in sig.parameters.items().
  - If (param\_name belongs to \_SKIP or param.kind belongs to tuple(param.VAR\_POSITIONAL, param.VAR\_KEYWORD)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in param\_name belongs to \_SKIP → param.kind belongs to tuple(param.VAR\_POSITIONAL, param.VAR\_KEYWORD).
    - Continue with the next iteration or loop test.
  - Set hint from hints.get(param\_name, Any).
  - Set tuple(actual\_type, description) from \_unwrap\_annotated(hint).
  - Set tuple(actual\_type, is\_optional) from \_unwrap\_optional(actual\_type).
  - Set prop\_schema from \_type\_to\_schema(actual\_type).
  - If description.
    - Set prop\_schema at “description” from description.
  - Set properties at param\_name from prop\_schema.
  - If (param.default is identical to inspect.Parameter.empty and not is\_optional).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in param.default is identical to inspect.Parameter.empty → not is\_optional.
    - Evaluate required.append(param\_name).
- Set schema from mapping(“type” → “object”, “properties” → properties, “additionalProperties” → false).
- If required.
  - Set schema at “required” from required.
- Return schema.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1297)

<a id="op-44d520ed572c67"></a>
### Unwrap annotated

`operation_foundation_binding_foundation_flow_lib_tool_unwrap_annotated`

**Inputs** t.

**Declared result** tuple at tuple(Any, (str bitwise or no value)).

**Explicit results** tuple(t, no value) · tuple(actual, description).

**Local steps**

- Set metadata from getattr(t, “\_\_metadata\_\_”, no value).
- If metadata is identical to no value.
  - Return tuple(t, no value).
- Set actual from getattr(t, “\_\_origin\_\_”, t).
- Set description from next(generator of m for m drawn from metadata where isinstance(m, str), no value).
  - Draw m from metadata, keep a combination only if (isinstance(m, str)).
- Return tuple(actual, description).

**Values supplied outside this operation** selected callable from getattr(t, “\_\_metadata\_\_”, no value), getattr(t, “\_\_origin\_\_”, t).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1307)

<a id="op-54a697c009b3ad"></a>
### Unwrap optional

`operation_foundation_binding_foundation_flow_lib_tool_unwrap_optional`

**Inputs** t.

**Declared result** tuple at tuple(Any, bool).

**Explicit results** tuple(t, false) · tuple(remaining at 0, true) · tuple(Any, true) · tuple(Union at remaining, true).

**Local steps**

- Set origin from get\_origin(t).
- If origin does not belong to tuple(Union, types.UnionType).
  - Return tuple(t, false).
- Set args from get\_args(t).
- If type(no value) does not belong to args.
  - Return tuple(t, false).
- Set remaining from tuple(generator of a for a drawn from args where a is distinct from type(no value)).
  - Draw a from args, keep a combination only if (a is distinct from type(no value)).
- If len(remaining) equals 1.
  - Return tuple(remaining at 0, true).
- If not remaining.
  - Return tuple(Any, true).
- Return tuple(Union at remaining, true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1308)

<a id="op-418a172d94d177"></a>
### Type to schema

`operation_foundation_binding_foundation_flow_lib_tool_type_to_schema`

**Inputs** t.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping() · dict(\_PRIMITIVE\_SCHEMAS at t) · mapping(“type” → “object”) · mapping(“type” → “array”) · mapping(“type” → “array”, “items” → items\_schema) · 4 additional forms in the steps below.

**Local steps**

- If (t is identical to Any or t is identical to object or t is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in t is identical to Any → t is identical to object → t is identical to no value.
  - Return mapping().
- If t belongs to \_PRIMITIVE\_SCHEMAS.
  - Return dict(\_PRIMITIVE\_SCHEMAS at t).
- If t is identical to dict.
  - Return mapping(“type” → “object”).
- If t is identical to list.
  - Return mapping(“type” → “array”).
- Set origin from get\_origin(t).
- Set args from get\_args(t).
- If origin belongs to tuple(list, tuple, set, frozenset).
  - Set items\_schema from \_type\_to\_schema(args at 0) when args, otherwise mapping().
    - Value choice on args — true gives \_type\_to\_schema(args at 0), false gives mapping().
  - Return mapping(“type” → “array”, “items” → items\_schema).
- If origin is identical to dict.
  - Return mapping(“type” → “object”).
- If origin is identical to Literal.
  - Return \_enum\_schema(list(args)).
- If origin belongs to tuple(Union, types.UnionType).
  - Return mapping(“anyOf” → list of \_type\_to\_schema(a) for a drawn from args).
    - Draw a from args.
- If isinstance(t, type).
  - Bind dependencies BaseModel.
  - If issubclass(t, BaseModel).
    - Return \_inline\_pydantic\_refs(t.model\_json\_schema()).
  - If issubclass(t, Enum).
    - Return \_enum\_schema(list of m.value for m drawn from t).
      - Draw m from t.
- Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1306)
