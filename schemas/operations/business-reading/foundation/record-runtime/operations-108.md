# Record lifecycle and persistence · operations 108

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Virtual doctype

<a id="op-8b0ab6ca2b49f7"></a>
### Virtual Doctype.load from db

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_load_from_database`

**Inputs** self.

**Declared result** no value.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6257) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1349)

<a id="op-5eb69ca19936f0"></a>
### Virtual Doctype.db update

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_database_update`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6293) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1344)

<a id="op-6b7ab1ac8fea2b"></a>
### Virtual Doctype.delete

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_delete`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6339) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1345)

<a id="op-af300c8c444b77"></a>
### Validate controller

`operation_foundation_model_virtual_record_type_business_behavior_validate_controller`

**Inputs** doctype.

**Declared result** no value.

**State and service calls** msgprint with translated “Failed to import virtual doctype {}, is controller file present?”.format(doctype) · msgprint with translated “Virtual DocType {} requires a static method called {} found {}”.format(Platform.bold(doctype), Platform.bold(m), Platform.bold(\_as\_str(method))) · msgprint with translated “Virtual DocType {} requires overriding an instance method called {} found {}”.format(Platform.bold(doctype), Platform.bold(m), Platform.bold(\_as\_str(method))).

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set controller from get\_controller(doctype).
- On failure (ImportError).
  - Evaluate Platform.msgprint(translated “Failed to import virtual doctype {}, is controller file present?”.format(doctype)).
  - Return no value.
- Bind local operation \_as\_str for subsequent calls.
- Set expected\_static\_method from list(“get\_list”, “get\_count”, “get\_stats”).
- For each m in expected\_static\_method.
  - Set method from inspect.getattr\_static(controller, m, no value).
  - If not isinstance(method, staticmethod).
    - Evaluate Platform.msgprint(translated “Virtual DocType {} requires a static method called {} found {}”.format(Platform.bold(doctype), Platform.bold(m), Platform.bold(\_as\_str(method))), title = translated “Incomplet ….
- Set expected\_instance\_methods from list(“db\_insert”, “db\_update”, “load\_from\_db”, “delete”).
- Set parent\_class from controller.mro() at 1.
- For each m in expected\_instance\_methods.
  - Set method from getattr(controller, m, no value).
  - Set original\_method from getattr(parent\_class, m, no value).
  - If method equals original\_method.
    - Evaluate Platform.msgprint(translated “Virtual DocType {} requires overriding an instance method called {} found {}”.format(Platform.bold(doctype), Platform.bold(m), Platform.bold(\_as\_str(method))), title = transla ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_controller(doctype), getattr(controller, m, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6385) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1341)

<a id="op-d2334a00f8f7e0"></a>
### Validate controller.as str

`operation_foundation_model_virtual_record_type_business_behavior_validate_controller_as_text`

**Inputs** method.

**Explicit results** formatted text {method.\_\_module\_\_}.{method.\_\_qualname\_\_} · “None”.

**Local steps**

- If hasattr(method, “\_\_module\_\_”).
  - Return formatted text {method.\_\_module\_\_}.{method.\_\_qualname\_\_}.
- Return “None”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L7193) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1342)

## Service · Workflow

<a id="op-8f0809653d1a58"></a>
### Get workflow name

`operation_foundation_model_workflow_business_behavior_get_workflow_name`

**Inputs** doctype.

**Record and data access** read “Workflow” via get\_value.

**Explicit results** workflow\_name.

**Local steps**

- Set workflow\_name from Platform.cache.hget(“workflow”, doctype).
- If workflow\_name is identical to no value.
  - Set workflow\_name from Platform.db.get\_value(“Workflow”, mapping(“document\_type” → doctype, “is\_active” → 1), “name”).
  - Evaluate Platform.cache.hset(“workflow”, doctype, (workflow\_name or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in workflow\_name → empty text.
- Return workflow\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L7299) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1359)

<a id="op-455733806d0f05"></a>
### Get transitions

`operation_foundation_model_workflow_business_behavior_get_transitions`

**Inputs** doc, workflow = no value, raise\_exception = false.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** resolve a document from Platform.parse\_json(doc) via get\_doc.

**Explicit results** list() · transitions.

**Explicit failure paths** WorkflowStateError · validation helper with WorkflowStateError — translated “Workflow State not set”.

**Local steps**

- Bind dependencies Document.
- If not isinstance(doc, Document).
  - Set doc from Platform.get\_doc(Platform.parse\_json(doc)).
  - Evaluate doc.load\_from\_db().
- If doc.is\_new().
  - Return list().
- Evaluate doc.check\_permission(“read”).
- Set workflow from (workflow or get\_workflow(doc.doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in workflow → get\_workflow(doc.doctype).
- Set current\_state from doc.get(workflow.workflow\_state\_field).
- If not current\_state.
  - If raise\_exception.
    - Raise WorkflowStateError.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Workflow State not set”, WorkflowStateError).
- Set transitions from list().
- Set roles from Platform.get\_roles().
- For each transition in workflow.transitions.
  - If (transition.state equals current\_state and transition.allowed belongs to roles).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in transition.state equals current\_state → transition.allowed belongs to roles.
    - If not is\_transition\_condition\_satisfied(transition, doc).
      - Continue with the next iteration or loop test.
    - Evaluate transitions.append(transition.as\_dict()).
- Return transitions.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”), Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1356)

<a id="op-43244494087021"></a>
### Get workflow safe globals

`operation_foundation_model_workflow_business_behavior_get_workflow_safe_globals`

**Inputs** no declared parameters.

**Explicit results** dict(Platform = Platform.\_dict(db = Platform.\_dict(get\_value = Platform.db.get\_value, get\_list = Platform.db.get\_list), session = Platform.session, utils = Platform.\_dict(now\_datetime = Platform.utils.now\_ ….

**Local steps**

- Return dict(Platform = Platform.\_dict(db = Platform.\_dict(get\_value = Platform.db.get\_value, get\_list = Platform.db.get\_list), session = Platform.session, utils = Platform.\_dict(now\_datetime = Platform.utils.now\_ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L631) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1360)

<a id="op-b69e9873930986"></a>
### Is transition condition satisfied

`operation_foundation_model_workflow_business_behavior_is_transition_condition_satisfied`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** transition, doc.

**Explicit result forms** Boolean true, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L845) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1363)

<a id="op-cd37c6f4726b83"></a>
### Evaluate workflow value

`operation_foundation_model_workflow_business_behavior_evaluate_workflow_value`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** value, evaluate\_as\_expression, doc.

**Explicit result forms** a value selected from the current context, no value, the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L984) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1354)

<a id="op-725513594ee0f9"></a>
### Apply workflow

`operation_foundation_model_workflow_business_behavior_apply_workflow`

**Inputs** doc, action.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** run\_workflow\_transition(doc, action).copy\_with\_fieldlevel\_read\_permissions().

**Local steps**

- Return run\_workflow\_transition(doc, action).copy\_with\_fieldlevel\_read\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L18) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1350)

<a id="op-26263638fe4493"></a>
### Run workflow transition

`operation_foundation_binding_foundation_model_workflow_run_workflow_transition`

**Inputs** doc, action.

**Declared result** Document.

**Record and data access** resolve a document from Platform.parse\_json(doc) via get\_doc · read “Workflow Transition Task” via get\_all · resolve a document from “Webhook” via get\_doc · resolve a document from “Server Script” via get\_doc.

**State and service calls** enqueue with async\_task · call save on doc · call submit on doc · call cancel on doc.

**Explicit results** doc.

**Explicit failure paths** validation helper with WorkflowTransitionError — translated “Not a valid Workflow Action” · validation helper — translated “Self approval is not allowed” · validation helper — translated “There is no task called "{}"”.format(workflow\_transition.task) · validation helper — translated “Illegal Document Status for {0}”.format(next\_state.state).

**Local steps**

- Set doc from Platform.get\_doc(Platform.parse\_json(doc)).
- Evaluate doc.load\_from\_db().
- Set workflow from get\_workflow(doc.doctype).
- Set transitions from get\_transitions(doc, workflow).
- Set user from Platform.session.user.
- Set transition from no value.
- For each t in transitions.
  - If t.action equals action.
    - Set transition from t.
- If not transition.
  - Call the validation error handler Platform.throw(translated “Not a valid Workflow Action”, WorkflowTransitionError).
- If not has\_approval\_access(user, doc, transition).
  - Call the validation error handler Platform.throw(translated “Self approval is not allowed”).
- Evaluate doc.set(workflow.workflow\_state\_field, transition.next\_state).
- Set next\_state from next(generator of d for d drawn from workflow.states where d.state equals transition.next\_state).
  - Draw d from workflow.states, keep a combination only if (d.state equals transition.next\_state).
- If next\_state.update\_field.
  - Set update\_value from evaluate\_workflow\_value(next\_state.update\_value, next\_state.evaluate\_as\_expression, doc).
  - Evaluate doc.set(next\_state.update\_field, update\_value).
- If transition.transition\_tasks.
  - Set workflow\_transitions from Platform.db.get\_all(“Workflow Transition Task”, mapping(“parent” → transition.transition\_tasks, “enabled” → true), list(“task”, “link”, “asynchronous”), order\_by = “idx”).
  - Set tasks from mapping of i at “name” → i at “method” for i drawn from Platform.get\_hooks(“workflow\_methods”).
    - Draw i from Platform.get\_hooks(“workflow\_methods”).
  - Set sync\_tasks from list().
  - Set async\_tasks from list().
  - For each workflow\_transition in workflow\_transitions.
    - If workflow\_transition.task belongs to DEFAULT\_WORKFLOW\_TASKS.
      - Select the first matching pattern against workflow\_transition.task.
        - Pattern “Webhook”.
          - Set webhook from Platform.get\_doc(“Webhook”, workflow\_transition.link).
          - Set task\_method from webhook.execute\_for\_doc.
        - Pattern “Server Script”.
          - Set server\_script from Platform.get\_doc(“Server Script”, workflow\_transition.link).
          - Set task\_method from server\_script.execute\_workflow\_task.
    - Otherwise.
      - Attempt the following.
        - Set task\_method from Platform.get\_attr(tasks at workflow\_transition.task).
      - On failure (KeyError).
        - Call the validation error handler Platform.throw(translated “There is no task called "{}"”.format(workflow\_transition.task)).
    - If workflow\_transition.asynchronous.
      - Evaluate async\_tasks.append(task\_method).
    - Otherwise.
      - Evaluate sync\_tasks.append(task\_method).
  - For each sync\_task in sync\_tasks.
    - Evaluate sync\_task(doc).
  - For each async\_task in async\_tasks.
    - Evaluate Platform.enqueue(async\_task, doc = doc, enqueue\_after\_commit = true).
- Bind dependencies queue\_submission.
- Bind dependencies is\_scheduler\_inactive.
- Set new\_docstatus from DocStatus((next\_state.doc\_status or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in next\_state.doc\_status → 0.
- If (doc.docstatus.is\_draft() and new\_docstatus.is\_draft()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_draft() → new\_docstatus.is\_draft().
  - Evaluate doc.save().
- Otherwise.
  - If (doc.docstatus.is\_draft() and new\_docstatus.is\_submitted()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_draft() → new\_docstatus.is\_submitted().
    - If (doc.meta.queue\_in\_background and not is\_scheduler\_inactive()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.queue\_in\_background → not is\_scheduler\_inactive().
      - Evaluate queue\_submission(doc, “Submit”).
      - Return doc.
    - Evaluate doc.submit().
  - Otherwise.
    - If (doc.docstatus.is\_submitted() and new\_docstatus.is\_submitted()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_submitted() → new\_docstatus.is\_submitted().
      - Evaluate doc.save().
    - Otherwise.
      - If (doc.docstatus.is\_submitted() and new\_docstatus.is\_cancelled()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_submitted() → new\_docstatus.is\_cancelled().
        - If (doc.meta.queue\_in\_background and not is\_scheduler\_inactive()).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.queue\_in\_background → not is\_scheduler\_inactive().
          - Evaluate queue\_submission(doc, “Cancel”).
          - Return doc.
        - Evaluate doc.cancel().
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Illegal Document Status for {0}”.format(next\_state.state)).
- Evaluate doc.add\_comment(“Workflow”, translated next\_state.state).
- Return doc.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“workflow\_methods”), Platform.get\_attr(tasks at workflow\_transition.task) · service or queued work from Platform.enqueue(async\_task, doc = doc, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1642)

<a id="op-09dbd6e306a905"></a>
### Can cancel document

`operation_foundation_model_workflow_business_behavior_can_cancel_document`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** true · false.

**Local steps**

- Set workflow from get\_workflow(doctype).
- Set cancelling\_states from list of s.state for s drawn from workflow.states where s.doc\_status equals “2”.
  - Draw s from workflow.states, keep a combination only if (s.doc\_status equals “2”).
- If not cancelling\_states.
  - Return true.
- For each transition in workflow.transitions.
  - If transition.next\_state belongs to cancelling\_states.
    - Return false.
- Return true.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L3154) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1353)

<a id="op-d0b9396912ceeb"></a>
### Validate workflow

`operation_foundation_model_workflow_business_behavior_validate_workflow`

**Inputs** doc.

**Explicit failure paths** validation helper — translated “{0} is not a valid Workflow State. Please update your Workflow and try again.”.format(Platform.bold(current\_state)) · validation helper with WorkflowPermissionError — translated “Workflow State transition not allowed from {0} to {1}”.format(bold\_current, bold\_next).

**Local steps**

- Set workflow from get\_workflow(doc.doctype).
- Set current\_state from no value.
- If getattr(doc, “\_doc\_before\_save”, no value).
  - Set current\_state from doc.\_doc\_before\_save.get(workflow.workflow\_state\_field).
- Set next\_state from doc.get(workflow.workflow\_state\_field).
- If not next\_state.
  - Set next\_state from workflow.states at 0.state.
  - Evaluate doc.set(workflow.workflow\_state\_field, next\_state).
- If not current\_state.
  - Set current\_state from workflow.states at 0.state.
- Set state\_row from list of d for d drawn from workflow.states where d.state equals current\_state.
  - Draw d from workflow.states, keep a combination only if (d.state equals current\_state).
- If not state\_row.
  - Call the validation error handler Platform.throw(translated “{0} is not a valid Workflow State. Please update your Workflow and try again.”.format(Platform.bold(current\_state))).
- Set state\_row from state\_row at 0.
- If current\_state differs from next\_state.
  - Set bold\_current from Platform.bold(current\_state).
  - Set bold\_next from Platform.bold(next\_state).
  - If not doc.\_doc\_before\_save.
    - Call the validation error handler Platform.throw(translated “Workflow State transition not allowed from {0} to {1}”.format(bold\_current, bold\_next), WorkflowPermissionError).
  - Set transitions from get\_transitions(doc.\_doc\_before\_save).
  - Set transition from list of d for d drawn from transitions where d.next\_state equals next\_state.
    - Draw d from transitions, keep a combination only if (d.next\_state equals next\_state).
  - If not transition.
    - Call the validation error handler Platform.throw(translated “Workflow State transition not allowed from {0} to {1}”.format(bold\_current, bold\_next), WorkflowPermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, “\_doc\_before\_save”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L3375) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1368)

<a id="op-dd938e9982dbdb"></a>
### Get workflow

`operation_foundation_model_workflow_business_behavior_get_workflow`

**Inputs** doctype.

**Declared result** “Workflow”.

**Record and data access** resolve a document from “Workflow” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Workflow”, get\_workflow\_name(doctype)).

**Local steps**

- Return Platform.get\_cached\_doc(“Workflow”, get\_workflow\_name(doctype)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Workflow”, get\_workflow\_name(doctype)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L4144) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1357)

<a id="op-8e812636672f83"></a>
### Has approval access

`operation_foundation_model_workflow_business_behavior_has_approval_access`

**Inputs** user, doc, transition.

**Explicit results** (user equals “Administrator” or transition.get(“allow\_self\_approval”) or user differs from doc.get(“owner”)).

**Local steps**

- Return (user equals “Administrator” or transition.get(“allow\_self\_approval”) or user differs from doc.get(“owner”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user equals “Administrator” → transition.get(“allow\_self\_approval”) → user differs from doc.get(“owner”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L4227) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1362)

<a id="op-d1e8287f2b5f6d"></a>
### Get workflow state field

`operation_foundation_model_workflow_business_behavior_get_workflow_state_field`

**Inputs** workflow\_name.

**Explicit results** get\_workflow\_field\_value(workflow\_name, “workflow\_state\_field”).

**Local steps**

- Return get\_workflow\_field\_value(workflow\_name, “workflow\_state\_field”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L4359) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1361)

<a id="op-a642fda9f6bc8a"></a>
### Send email alert

`operation_foundation_model_workflow_business_behavior_send_email_alert`

**Inputs** workflow\_name.

**Explicit results** get\_workflow\_field\_value(workflow\_name, “send\_email\_alert”).

**Local steps**

- Return get\_workflow\_field\_value(workflow\_name, “send\_email\_alert”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L4420) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1365)

<a id="op-fabb7ea1a3d1c9"></a>
### Get workflow field value

`operation_foundation_model_workflow_business_behavior_get_workflow_field_value`

**Inputs** workflow\_name, field.

**Record and data access** read “Workflow” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Workflow”, workflow\_name, field).

**Local steps**

- Return Platform.get\_cached\_value(“Workflow”, workflow\_name, field).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Workflow”, workflow\_name, field).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0293.json#L4481) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1358)

<a id="op-bd40b5b59ef3dd"></a>
### Bulk workflow approval

`operation_foundation_model_workflow_business_behavior_bulk_workflow_approval`

**Inputs** docnames, doctype, action.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** msgprint with translated “Bulk {0} is enqueued in background.”.format(action) · enqueue with \_bulk\_workflow\_action.

**Explicit failure paths** validation helper — translated “Bulk approval only support up to 500 documents.”.

**Local steps**

- Set docnames from json.loads(docnames).
- If len(docnames) &lt; 20.
  - Evaluate \_bulk\_workflow\_action(docnames, doctype, action).
- Otherwise.
  - If len(docnames) ≤ 500.
    - Evaluate Platform.msgprint(translated “Bulk {0} is enqueued in background.”.format(action), alert = true).
    - Evaluate Platform.enqueue(\_bulk\_workflow\_action, docnames = docnames, doctype = doctype, action = action, queue = “short”, …).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Bulk approval only support up to 500 documents.”, title = translated “Too Many Documents”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(\_bulk\_workflow\_action, docnames = docnames, doctype = doctype, action = action, queue = “short”, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L20) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1352)

<a id="op-33ad5afd21d3cf"></a>
### Bulk workflow action

`operation_foundation_model_workflow_business_behavior_bulk_workflow_action`

**Inputs** docnames, doctype, action.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** commit · rollback.

**Local steps**

- Set failed\_transactions from defaultdict(list).
- Set successful\_transactions from defaultdict(list).
- Evaluate Platform.clear\_messages().
- For each tuple(idx, docname) in enumerate(docnames, 1).
  - Set message\_dict from mapping().
  - Attempt the following.
    - Evaluate show\_progress(docnames, translated “Applying: {0}”.format(action), idx, docname).
    - Evaluate run\_workflow\_transition(Platform.get\_doc(doctype, docname), action).
    - Evaluate Platform.db.commit().
  - On failure (Exception) bound to e.
    - If not Platform.message\_log.
      - Set message from formatted text {e.\_\_class\_\_.\_\_name\_\_}.
      - If e.args.
        - Update message using + formatted text  : {e.args at 0}.
      - Set message\_dict from mapping(“docname” → docname, “message” → message).
      - Evaluate failed\_transactions at docname.append(message\_dict).
    - Evaluate Platform.db.rollback().
    - Evaluate Platform.log\_error(title = formatted text Workflow {action} threw an error for {doctype} {docname}, reference\_doctype = “Workflow”, reference\_name = action).
  - On exit, including pending return or failure.
    - If not message\_dict.
      - If Platform.message\_log.
        - Set messages from Platform.get\_message\_log().
        - For each message in messages.
          - Evaluate Platform.message\_log.pop().
          - Set message\_dict from mapping(“docname” → docname, “message” → message.get(“message”)).
          - If (message.get(“raise\_exception”, false) or “Error” belongs to message.get(“message”, empty text)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in message.get(“raise\_exception”, false) → “Error” belongs to message.get(“message”, empty text).
            - Evaluate failed\_transactions at docname.append(message\_dict).
          - Otherwise.
            - Evaluate successful\_transactions at docname.append(message\_dict).
      - Otherwise.
        - Evaluate successful\_transactions at docname.append(mapping(“docname” → docname, “message” → no value)).
- If (failed\_transactions and successful\_transactions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in failed\_transactions → successful\_transactions.
  - Set indicator from “orange”.
- Otherwise.
  - If failed\_transactions.
    - Set indicator from “red”.
  - Otherwise.
    - Set indicator from “green”.
- Evaluate print\_workflow\_log(failed\_transactions, translated “Failed Transactions”, doctype, indicator).
- Evaluate print\_workflow\_log(successful\_transactions, translated “Successful Transactions”, doctype, indicator).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L19) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1351)

<a id="op-89ec749ef400a1"></a>
### Print workflow log

`operation_foundation_model_workflow_business_behavior_print_workflow_log`

**Inputs** messages, title, doctype, indicator.

**State and service calls** msgprint with msg.

**Local steps**

- If messages.keys().
  - Set msg from formatted text &lt;p&gt;{Platform.bold(title)}&lt;/p&gt;&lt;ul&gt;.
  - For each doc in messages.keys().
    - Set html from formatted text &lt;li&gt;{Platform.utils.get\_link\_to\_form(doctype, doc)}.
    - For each log in messages at doc.
      - If log.get(“message”).
        - Update html using + text in the contract.format(log.get(“message”)).
    - Update html using + “&lt;/li&gt;”.
    - Update msg using + html.
  - Update msg using + “&lt;/ul&gt;”.
  - Evaluate Platform.msgprint(msg, title = translated “Workflow Status”, indicator = indicator, is\_minimizable = true, realtime = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L22) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1364)

<a id="op-72b58f4da03e0d"></a>
### Get common transition actions

`operation_foundation_model_workflow_business_behavior_get_common_transition_actions`

**Inputs** docs, doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list() · list(common\_actions).

**Local steps**

- Set common\_actions from list().
- If isinstance(docs, str).
  - Set docs from json.loads(docs).
- Attempt the following.
  - For each tuple(i, doc) in enumerate(docs, 1).
    - If not doc.get(“doctype”).
      - Set doc at “doctype” from doctype.
    - Set actions from list of t.get(“action”) for t drawn from get\_transitions(doc, raise\_exception = true) where has\_approval\_access(Platform.session.user, doc, t).
      - Draw t from get\_transitions(doc, raise\_exception = true), keep a combination only if (has\_approval\_access(Platform.session.user, doc, t)).
    - If not actions.
      - Return list().
    - Set common\_actions from actions when i equals 1, otherwise set(common\_actions).intersection(actions).
      - Value choice on i equals 1 — true gives actions, false gives set(common\_actions).intersection(actions).
    - If not common\_actions.
      - Return list().
- On failure (WorkflowStateError).
  - Take no action here.
- Return list(common\_actions).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L21) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1355)

<a id="op-ce29df48f9e3ed"></a>
### Show progress

`operation_foundation_model_workflow_business_behavior_show_progress`

**Inputs** docnames, message, i, description.

**Local steps**

- Set n from len(docnames).
- If n ≥ 5.
  - Evaluate Platform.publish\_progress(((float(i) × 100) ÷ n), title = message, description = description).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1367)
