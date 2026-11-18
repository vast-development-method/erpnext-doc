# Workflow, automation and dispatch · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Agent

<a id="op-8e77afe16c0d14"></a>
### Sync agents

`operation_foundation_binding_foundation_flow_lib_agent_sync_agents`

**Inputs** \_app = no value.

**Declared result** no value.

**Local steps**

- Set hooked from list().
- For each path in Platform.get\_hooks(“flow\_agents”).
  - Within skip\_if\_invalid(formatted text Flow Agents of {path} skipped).
    - Evaluate hooked.extend(Platform.get\_attr(path)()).
- Set declared from mapping().
- For each agent in hooked.
  - For each item in \_with\_sub\_agents(agent).
    - Evaluate declared.setdefault(item.name, item).
  - Set duplicate from next(generator of item for item drawn from \_with\_sub\_agents(agent) where declared at item.name is distinct from item, no value).
    - Draw item from \_with\_sub\_agents(agent), keep a combination only if (declared at item.name is distinct from item).
  - If duplicate.
    - Evaluate log\_skipped(formatted text Flow Agent {agent.name} skipped, translated “Flow Agent {0} is declared more than once.”.format(duplicate.name)).
    - Continue with the next iteration or loop test.
  - Within skip\_if\_invalid(formatted text Flow Agent {agent.name} skipped).
    - Evaluate agent.sync().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“flow\_agents”), Platform.get\_attr(path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1245)

<a id="op-061a3f397fe2a1"></a>
### With sub agents

`operation_foundation_binding_foundation_flow_lib_agent_with_sub_agents`

**Inputs** agent.

**Declared result** Iterator at Agent.

**Local steps**

- yield agent.
- For each child in agent.sub\_agents.
  - yield values from \_with\_sub\_agents(child).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1273) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1249)

<a id="op-be2581d0885ca3"></a>
### Sync tools

`operation_foundation_binding_foundation_flow_lib_agent_sync_tools`

**Inputs** \_app = no value.

**Declared result** no value.

**Local steps**

- For each path in Platform.get\_hooks(“flow\_tools”).
  - Within skip\_if\_invalid(formatted text Flow Tool {path} skipped).
    - Evaluate \_ensure\_tool(Platform.get\_attr(path)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“flow\_tools”), Platform.get\_attr(path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1246)

<a id="op-958893819f2123"></a>
### Agent.initialize

`operation_foundation_binding_foundation_flow_lib_agent_agent_init`

**Inputs** self, name (named only), model (named only), instructions (named only), description (named only, default empty text), tools (named only, default no value), knowledge (named only, default no value), skills (named only, default no value), sub\_agents (named only, default no value), max\_iterations (named only, default DEFAULT\_MAX\_ITERATIONS), auto\_approve (named only, default false).

**Local steps**

- If (knowledge and not isinstance(knowledge, list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in knowledge → not isinstance(knowledge, list).
  - Set knowledge from list(knowledge).
- Set self.app from nested operand in the contract.\_getframe(1).f\_globals at “\_\_name\_\_”.split(“.”, 1) at 0.
- Set self.name from formatted text {self.app}/{name}.
- Set self.model from model.
- Set self.instructions from instructions.
- Set self.description from description.
- Set self.tools from list((tools or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tools → list().
- Set self.knowledge from list((knowledge or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in knowledge → list().
- Set self.skills from list((skills or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in skills → list().
- Set self.sub\_agents from list((sub\_agents or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sub\_agents → list().
- Set self.max\_iterations from max\_iterations.
- Set self.auto\_approve from auto\_approve.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1238)

<a id="op-d9f4fc23a23b03"></a>
### Agent.sync

`operation_foundation_binding_foundation_flow_lib_agent_agent_sync`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Flow Agent” via exists · resolve a document from “Flow Agent” via get\_doc · read “Flow Model” via exists · resolve a document from mapping(“doctype” → “Flow Agent”, “title” → self.name, “app” → self.app, “model” → self.model) via get\_doc.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper — translated “Flow Agent {0} already exists and is not owned by code.”.format(self.name).

**Local steps**

- For each child in self.sub\_agents.
  - Evaluate child.sync().
- If Platform.db.exists(“Flow Agent”, self.name).
  - Set doc from Platform.get\_doc(“Flow Agent”, self.name).
  - If not doc.is\_system\_generated.
    - Call the validation error handler Platform.throw(translated “Flow Agent {0} already exists and is not owned by code.”.format(self.name), title = translated “Agent Conflict”).
  - If not Platform.db.exists(“Flow Model”, doc.model).
    - Set doc.model from self.model.
- Otherwise.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Flow Agent”, “title” → self.name, “app” → self.app, “model” → self.model)).
- Set doc.description from self.description.
- Set doc.instructions from self.instructions.
- Set doc.max\_iterations from self.max\_iterations.
- Set doc.is\_system\_generated from 1.
- Evaluate doc.set(“tools”, list of mapping(“tool” → \_ensure\_tool(tool)) for tool drawn from self.tools).
  - Draw tool from self.tools.
- Evaluate doc.set(“knowledge\_bases”, list of mapping(“knowledge\_base” → kb.name) for kb drawn from self.knowledge).
  - Draw kb from self.knowledge.
- Evaluate doc.set(“skills”, list of mapping(“skill” → \_skill\_name(self.app, name)) for name drawn from self.skills).
  - Draw name from self.skills.
- Evaluate doc.set(“sub\_agents”, list of mapping(“agent” → child.name) for child drawn from self.sub\_agents).
  - Draw child from self.sub\_agents.
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1241)

<a id="op-c9e8d130b40e3a"></a>
### Agent.new session

`operation_foundation_binding_foundation_flow_lib_agent_agent_new_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, title.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1239)

<a id="op-09121b9dc872b6"></a>
### Agent.run

`operation_foundation_binding_foundation_flow_lib_agent_agent_run`

**Inputs** self, input, on\_complete (named only, default no value).

**Declared result** FlowRun.

**Explicit results** self.new\_session().chat(input, on\_complete = on\_complete).

**Local steps**

- Return self.new\_session().chat(input, on\_complete = on\_complete).

**Methods declared on this owner** [new session](operations-001.md#op-c9e8d130b40e3a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1240)

<a id="op-baf07d51eb5caa"></a>
### With app prefix

`operation_foundation_binding_foundation_flow_lib_agent_with_app_prefix`

**Inputs** app, name.

**Declared result** str.

**Explicit results** name when “/” belongs to name, otherwise formatted text {app}/{name}.

**Local steps**

- Return name when “/” belongs to name, otherwise formatted text {app}/{name}.
  - Value choice on “/” belongs to name — true gives name, false gives formatted text {app}/{name}.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1272) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1248)

<a id="op-677f1f6a28cf9b"></a>
### Skill name

`operation_foundation_binding_foundation_flow_lib_agent_skill_name`

**Inputs** app, name.

**Declared result** str.

**Record and data access** read “Flow Skill” via exists.

**Explicit results** own when Platform.db.exists(“Flow Skill”, own), otherwise name.

**Local steps**

- Set own from with\_app\_prefix(app, name).
- Return own when Platform.db.exists(“Flow Skill”, own), otherwise name.
  - Value choice on Platform.db.exists(“Flow Skill”, own) — true gives own, false gives name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1244)

<a id="op-47d26ea946f4c3"></a>
### Ensure tool

`operation_foundation_binding_foundation_flow_lib_agent_ensure_tool`

**Inputs** tool.

**Declared result** str.

**Record and data access** read “Flow Tool” via get\_value · resolve a document from “Flow Tool” via get\_doc · resolve a document from mapping(“doctype” → “Flow Tool”, “slug” → name, “title” → tool.name.replace(“\_”, one space).title(), “type” → “Imported”, …) via get\_doc.

**State and service calls** call save on doc · call insert on doc.

**Explicit results** name.

**Explicit failure paths** validation helper — translated “Tools {0} and {1} are both named {2}. Name one differently with @tool(name=...).”.format(row.import\_path, import\_path, tool.name).

**Local steps**

- Set import\_path from \_tool\_import\_path(tool).
- Set name from formatted text {import\_path.split(“.”, 1) at 0}/{tool.name}.
- Set definition from mapping(“import\_path” → import\_path, “description” → tool.description, “requires\_confirmation” → int(tool.requires\_confirmation is distinct from false), “background” → int(tool.background is identical to true), …).
- Set row from Platform.db.get\_value(“Flow Tool”, name, list(definition), as\_dict = true).
- If (row and row.import\_path differs from import\_path and \_exports\_another(row.import\_path, tool)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → row.import\_path differs from import\_path → \_exports\_another(row.import\_path, tool).
  - Call the validation error handler Platform.throw(translated “Tools {0} and {1} are both named {2}. Name one differently with @tool(name=...).”.format(row.import\_path, import\_path, tool.name), title = translated “Tool Conflict”).
- If (row and all(generator of row.get(key) equals value for tuple(key, value) drawn from definition.items())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → all(generator of row.get(key) equals value for tuple(key, value) drawn from definition.items()).
  - Draw tuple(key, value) from definition.items().
  - Return name.
- If row.
  - Set doc from Platform.get\_doc(“Flow Tool”, name).
  - Evaluate doc.update(definition).
  - Evaluate doc.save(ignore\_permissions = true).
- Otherwise.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Flow Tool”, “slug” → name, “title” → nested operand in the contract.name.replace(“\_”, one space).title(), “type” → “Imported”, …)).
  - Evaluate doc.insert(ignore\_permissions = true).
- Return name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1242)

<a id="op-f2f93b84fe5643"></a>
### Exports another

`operation_foundation_binding_foundation_flow_lib_agent_exports_another`

**Inputs** import\_path, tool.

**Declared result** bool.

**Explicit results** false · (isinstance(other, Tool) and other is distinct from tool and other.name equals tool.name).

**Local steps**

- Attempt the following.
  - Set other from Platform.get\_attr(import\_path).
- On failure (tuple(ImportError, AttributeError)).
  - Return false.
- Return (isinstance(other, Tool) and other is distinct from tool and other.name equals tool.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(other, Tool) → other is distinct from tool → other.name equals tool.name.

**Values supplied outside this operation** selected callable from Platform.get\_attr(import\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1243)

<a id="op-30acb50eaaea86"></a>
### Tool import path

`operation_foundation_binding_foundation_flow_lib_agent_tool_import_path`

**Inputs** tool.

**Declared result** str.

**Explicit results** formatted text {module\_name}.{name}.

**Explicit failure paths** validation helper — translated “Tool {0} must be exported as a module-level attribute by an installed app.”.format(tool.name).

**Local steps**

- Set module\_name from tool.func.\_\_module\_\_.
- If module\_name.split(“.”, 1) at 0 belongs to Platform.get\_installed\_apps().
  - Attempt the following.
    - Set module from importlib.import\_module(module\_name).
  - On failure (Exception).
    - Take no action here.
  - When the protected block completes normally.
    - For each tuple(name, value) in vars(module).items().
      - If value is identical to tool.
        - Return formatted text {module\_name}.{name}.
- Call the validation error handler Platform.throw(translated “Tool {0} must be exported as a module-level attribute by an installed app.”.format(tool.name), title = translated “Invalid Tool”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1271) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1247)

## Service · Api

<a id="op-d126426af37870"></a>
### Check config permission

`operation_foundation_binding_foundation_automation_engine_api_check_config_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L342)

<a id="op-9eba67dfddd19c"></a>
### Get automation capabilities

`operation_foundation_binding_foundation_automation_engine_api_get_automation_capabilities`

**Inputs** doctype = no value, trigger\_type = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“triggers” → TRIGGER\_TYPES, “custom\_events” → registered\_events(), “trigger\_events” → registered\_events(doctype) when doctype, otherwise list(), “fields” → \_doc\_fields(doctype) when doctype, otherw ….

**Local steps**

- Evaluate \_check\_config\_permission().
- If doctype.
  - Evaluate Platform.has\_permission(doctype, throw = true).
- Return mapping(“triggers” → TRIGGER\_TYPES, “custom\_events” → registered\_events(), “trigger\_events” → registered\_events(doctype) when doctype, otherwise list(), “fields” → \_doc\_fields(doctype) when doctype, otherw ….
  - Value choice on doctype — true gives registered\_events(doctype), false gives list().
  - Value choice on doctype — true gives \_doc\_fields(doctype), false gives list().
  - Draw a from get\_action\_registry().values(), keep a combination only if (\_applies(a, doctype, trigger\_type)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L344)

<a id="op-e9e813ee5af8e9"></a>
### Validate action params

`operation_foundation_binding_foundation_automation_engine_api_validate_action_params`

**Inputs** action\_type, doctype, params, trigger\_type = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“valid” → true, “errors” → list()) · mapping(“valid” → false, “errors” → list(mapping(“fieldname” → e.fieldname, “message” → str(e)))) · mapping(“valid” → false, “errors” → list(mapping(“fieldname” → no value, “message” → str(e)))).

**Local steps**

- Evaluate \_check\_config\_permission().
- Set action from get\_action(action\_type).
- Attempt the following.
  - Evaluate \_validate\_action\_context(action, doctype, trigger\_type).
  - Evaluate action.validate((Platform.parse\_json(params) or mapping()), doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(params) → mapping().
  - Return mapping(“valid” → true, “errors” → list()).
- On failure (AutomationParamError) bound to e.
  - Return mapping(“valid” → false, “errors” → list(mapping(“fieldname” → e.fieldname, “message” → str(e)))).
- On failure (Exception) bound to e.
  - Return mapping(“valid” → false, “errors” → list(mapping(“fieldname” → no value, “message” → str(e)))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L358)

<a id="op-0a47f6ced7d9fd"></a>
### Get param options

`operation_foundation_binding_foundation_automation_engine_api_get_param_options`

**Inputs** action\_type, fieldname, doctype, params = no value, search\_text = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** resolver(doctype, parsed\_params, search\_text) when resolver, otherwise list().

**Explicit failure paths** validation helper — translated “Unknown parameter: {0}”.format(fieldname).

**Local steps**

- Evaluate \_check\_config\_permission().
- Set action from get\_action(action\_type).
- Set field from next(generator of f for f drawn from action.params\_schema where f at “fieldname” equals fieldname, no value).
  - Draw f from action.params\_schema, keep a combination only if (f at “fieldname” equals fieldname).
- If not field.
  - Call the validation error handler Platform.throw(translated “Unknown parameter: {0}”.format(fieldname)).
- Set parsed\_params from Platform.parse\_json(params) when params, otherwise mapping().
  - Value choice on params — true gives Platform.parse\_json(params), false gives mapping().
- Evaluate \_reject\_client\_methods(parsed\_params).
- Set resolver from OPTION\_RESOLVERS.get(field.get(“options\_source”)).
- Return resolver(doctype, parsed\_params, search\_text) when resolver, otherwise list().
  - Value choice on resolver — true gives resolver(doctype, parsed\_params, search\_text), false gives list().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L345)

<a id="op-524208aa3c13be"></a>
### Run manually

`operation_foundation_binding_foundation_automation_engine_api_run_manually`

**Inputs** automation, docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from “Automation Flow” via get\_doc.

**Explicit results** mapping(“queued” → true).

**Explicit failure paths** validation helper — translated “Document-less automations do not accept a document name”.

**Local steps**

- Set rule from Platform.get\_doc(“Automation Flow”, automation).
- Evaluate Platform.has\_permission(“Automation Flow”, “write”, doc = rule, throw = true).
- If rule.document\_type.
  - Evaluate Platform.has\_permission(rule.document\_type, “read”, doc = docname, throw = true).
- Otherwise.
  - If docname.
    - Call the validation error handler Platform.throw(translated “Document-less automations do not accept a document name”).
- Set payload from mapping(“manual” → true, “manual\_run\_id” → Platform.generate\_hash(length = 12)).
- Evaluate queue\_trigger(automation, rule.document\_type, docname, payload = payload, depth = 1).
- Evaluate Platform.db.after\_commit.add(kick\_drainer).
- Return mapping(“queued” → true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Automation Flow”, “write”, doc = rule, throw = true), Platform.has\_permission(rule.document\_type, “read”, doc = docname, throw = true) · clock or generated value from Platform.generate\_hash(length = 12).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L350)

<a id="op-f7d65c75d6ff2d"></a>
### Get runs

`operation_foundation_binding_foundation_automation_engine_api_get_runs`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Record and data access** read RUN via get\_all.

**Explicit results** Platform.get\_all(RUN, filters = mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name), fields = list(“name”, “automation”, “automation\_title”, “status”, …), order\_by = “creation desc”).

**Local steps**

- Evaluate Platform.has\_permission(reference\_doctype, “read”, doc = reference\_name, throw = true).
- Return Platform.get\_all(RUN, filters = mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name), fields = list(“name”, “automation”, “automation\_title”, “status”, …), order\_by = “creation desc”).

**Values supplied outside this operation** effective access from Platform.has\_permission(reference\_doctype, “read”, doc = reference\_name, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L346)

<a id="op-d2223b0ae0957a"></a>
### Doc fields

`operation_foundation_binding_foundation_automation_engine_api_doc_fields`

**Inputs** doctype.

**Declared result** list.

**Explicit results** list of mapping(“fieldname” → df.fieldname, “label” → df.label, “fieldtype” → df.fieldtype, “options” → df.options) for df drawn from Platform.get\_meta(doctype).fields where df.fieldtype does not belong to ….

**Local steps**

- Return list of mapping(“fieldname” → df.fieldname, “label” → df.label, “fieldtype” → df.fieldtype, “options” → df.options) for df drawn from Platform.get\_meta(doctype).fields where df.fieldtype does not belong to ….
  - Draw df from Platform.get\_meta(doctype).fields, keep a combination only if (df.fieldtype does not belong to Platform.model.no\_value\_fields).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L343)

<a id="op-2b162cd30afd9e"></a>
### Applies

`operation_foundation_binding_foundation_automation_engine_api_applies`

**Inputs** action, doctype, trigger\_type = no value.

**Declared result** bool.

**Explicit results** false · (not trigger\_type or not action.supported\_trigger\_types or trigger\_type belongs to action.supported\_trigger\_types).

**Local steps**

- If (action.requires\_document and not doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in action.requires\_document → not doctype.
  - Return false.
- If (doctype and action.applicable\_doctypes is distinct from no value and doctype does not belong to action.applicable\_doctypes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → action.applicable\_doctypes is distinct from no value → doctype does not belong to action.applicable\_doctypes.
  - Return false.
- Return (not trigger\_type or not action.supported\_trigger\_types or trigger\_type belongs to action.supported\_trigger\_types).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not trigger\_type → not action.supported\_trigger\_types → trigger\_type belongs to action.supported\_trigger\_types.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L340)

<a id="op-e22322eb5b572b"></a>
### Validate action context

`operation_foundation_binding_foundation_automation_engine_api_validate_action_context`

**Inputs** action, doctype, trigger\_type.

**Explicit failure paths** AutomationParamError(translated “This action requires a Document Type”) · AutomationParamError(translated “This action does not support the selected trigger”).

**Local steps**

- If (action.requires\_document and not doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in action.requires\_document → not doctype.
  - Raise AutomationParamError(translated “This action requires a Document Type”).
- If (trigger\_type and action.supported\_trigger\_types and trigger\_type does not belong to action.supported\_trigger\_types).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in trigger\_type → action.supported\_trigger\_types → trigger\_type does not belong to action.supported\_trigger\_types.
  - Raise AutomationParamError(translated “This action does not support the selected trigger”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L357)

<a id="op-8d82eac95bcbf6"></a>
### Reject client methods

`operation_foundation_binding_foundation_automation_engine_api_reject_client_methods`

**Inputs** value.

**Explicit failure paths** validation helper — translated “Client-supplied resolver methods are not allowed”.

**Local steps**

- For each item in \_walk\_values(value).
  - If (isinstance(item, str) and (item.startswith(“method:”) or item.startswith(“Platform.”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → (item.startswith(“method:”) or item.startswith(“Platform.”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.startswith(“method:”) → item.startswith(“Platform.”).
    - Call the validation error handler Platform.throw(translated “Client-supplied resolver methods are not allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L349)

<a id="op-7d63fbfa3f0002"></a>
### Walk values

`operation_foundation_binding_foundation_automation_engine_api_walk_values`

**Inputs** value.

**Local steps**

- If isinstance(value, dict).
  - For each child in value.values().
    - yield values from \_walk\_values(child).
- Otherwise.
  - If isinstance(value, tuple(list, tuple)).
    - For each child in value.
      - yield values from \_walk\_values(child).
  - Otherwise.
    - yield value.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L359)

<a id="op-305a0c2016d0ef"></a>
### User options

`operation_foundation_binding_foundation_automation_engine_api_user_options`

**Inputs** doctype, params, search\_text.

**Record and data access** read “User” via get\_all.

**Explicit results** Platform.get\_all(“User”, filters = filters, fields = list(“name”, “full\_name”), limit = 20).

**Local steps**

- Set filters from mapping(“enabled” → 1).
- If search\_text.
  - Set filters at “name” from tuple(“like”, formatted text %{search\_text}%).
- Return Platform.get\_all(“User”, filters = filters, fields = list(“name”, “full\_name”), limit = 20).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L356)
