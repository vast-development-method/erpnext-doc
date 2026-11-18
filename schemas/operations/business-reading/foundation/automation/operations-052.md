# Workflow, automation and dispatch · operations 52

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workflow

[Record definition](../../../../data/record-types/workflow.json)

<a id="op-028cfb3a549146"></a>
### Workflow.validate docstatus

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_validate_record_state`

**Inputs** self.

**Explicit failure paths** validation helper — Platform.\_(“Workflow State '{0}' has Document Status {1}, but DocType '{2}' is not submittable. Only Document Status 0 ( …”).format(state.state, state.doc\_status, self.document\_type) · validation helper — Platform.\_(“Cannot change state of Cancelled Document. Transition row {0}”).format(t.idx) · validation helper — Platform.\_(“Submitted Document cannot be converted back to draft. Transition row {0}”).format(t.idx) · validation helper — Platform.\_(“Cannot cancel before submitting. See Transition {0}”).format(t.idx).

**Local steps**

- Bind local operation get\_state for subsequent calls.
- Set meta from Platform.get\_meta(self.document\_type).
- Set is\_submittable from meta.is\_submittable.
- If not is\_submittable.
  - For each state in self.states.
    - If cint(state.doc\_status) differs from 0.
      - Call the validation error handler Platform.throw(Platform.\_(“Workflow State '{0}' has Document Status {1}, but DocType '{2}' is not submittable. Only Document Status 0 ( …”).format(state.state, state.doc\_status, self.document\_type)).
- For each t in self.transitions.
  - Set state from get\_state(t.state).
  - Set next\_state from get\_state(t.next\_state).
  - Set state\_docstatus from cint(state.doc\_status).
  - Set next\_state\_docstatus from cint(next\_state.doc\_status).
  - If state\_docstatus equals 2.
    - Call the validation error handler Platform.throw(Platform.\_(“Cannot change state of Cancelled Document. Transition row {0}”).format(t.idx)).
  - If (state\_docstatus equals 1 and next\_state\_docstatus equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in state\_docstatus equals 1 → next\_state\_docstatus equals 0.
    - Call the validation error handler Platform.throw(Platform.\_(“Submitted Document cannot be converted back to draft. Transition row {0}”).format(t.idx)).
  - If (state\_docstatus equals 0 and next\_state\_docstatus equals 2).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in state\_docstatus equals 0 → next\_state\_docstatus equals 2.
    - Call the validation error handler Platform.throw(Platform.\_(“Cannot cancel before submitting. See Transition {0}”).format(t.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L1996) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1638)

<a id="op-ba2bdf328741fe"></a>
### Workflow.validate docstatus.get state

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_validate_record_state_get_state`

**Inputs** state.

**Explicit results** s.

**Explicit failure paths** validation helper — Platform.\_(“{0} not a valid State”).format(state).

**Local steps**

- For each s in self.states.
  - If s.state equals state.
    - Return s.
- Call the validation error handler Platform.throw(Platform.\_(“{0} not a valid State”).format(state)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L2791) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1639)

<a id="op-af763f43d843cc"></a>
### Workflow.set active

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_set_active`

**Inputs** self.

**Local steps**

- If cint(self.is\_active).
  - Set Workflow from Platform.qb.DocType(“Workflow”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(Workflow.is\_active, 0).where(Workflow.document\_type equals self.document\_type).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L2934) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1635)

<a id="op-dcec73f709dbc8"></a>
### Get workflow state count

`operation_foundation_workflow_record_definitions_workflow_business_behavior_get_workflow_state_count`

**Inputs** doctype, workflow\_state\_field, states.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_all.

**Explicit results** list of r for r drawn from result where r at workflow\_state\_field.

**Local steps**

- Evaluate Platform.has\_permission(doctype = doctype, ptype = “read”, throw = true).
- Evaluate Platform.has\_permission(doctype = “Workflow”, ptype = “write”, throw = true).
- Set states from Platform.parse\_json(states).
- If workflow\_state\_field belongs to Platform.get\_meta(doctype).get\_valid\_columns().
  - Set result from Platform.get\_all(doctype, fields = list(workflow\_state\_field, mapping(“COUNT” → “\*”, “as” → “count”)), filters = mapping(workflow\_state\_field → list(“not in”, states)), group\_by = workflow\_state\_field).
  - Return list of r for r drawn from result where r at workflow\_state\_field.
    - Draw r from result, keep a combination only if (r at workflow\_state\_field).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype = doctype, ptype = “read”, throw = true), Platform.has\_permission(doctype = “Workflow”, ptype = “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L69) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1631)

<a id="op-8a7998533cf761"></a>
### Get workflow methods

`operation_foundation_workflow_record_definitions_workflow_business_behavior_get_workflow_methods`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Explicit results** (list of i at “name” for i drawn from Platform.get\_hooks(“workflow\_methods”) + DEFAULT\_WORKFLOW\_TASKS).

**Local steps**

- Return (list of i at “name” for i drawn from Platform.get\_hooks(“workflow\_methods”) + DEFAULT\_WORKFLOW\_TASKS).
  - Draw i from Platform.get\_hooks(“workflow\_methods”).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“workflow\_methods”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L3517) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1630)

## Record · Workflow action

[Record definition](../../../../data/record-types/workflow_action.json)

<a id="op-f433bb781a331d"></a>
### On doctype update

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Workflow Action”.

**Local steps**

- Evaluate Platform.db.add\_index(“Workflow Action”, list(“reference\_name”, “reference\_doctype”, “status”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L3637) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1622)

<a id="op-dab80ea3848567"></a>
### Get permission query conditions

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L3724) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1612)

<a id="op-20b73f38cf79f0"></a>
### Has permission

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** Boolean true, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L4099) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1620)

<a id="op-d9d02dd1cd299b"></a>
### Process workflow actions

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_process_workflow_actions`

**Inputs** doc, state.

**Record and data access** read “Workflow Document State” via get\_value.

**Explicit results** no value.

**Local steps**

- Set workflow from get\_workflow\_name(doc.get(“doctype”)).
- If not workflow.
  - Return no value.
- If state equals “on\_trash”.
  - Evaluate clear\_workflow\_actions(doc.get(“doctype”), doc.get(“name”)).
  - Return no value.
- If is\_workflow\_action\_already\_created(doc).
  - Return no value.
- Evaluate update\_completed\_workflow\_actions(doc, workflow = workflow, workflow\_state = get\_doc\_workflow\_state(doc)).
- Evaluate clear\_doctype\_notifications(“Workflow Action”).
- Set next\_possible\_transitions from get\_next\_possible\_transitions(workflow, get\_doc\_workflow\_state(doc), doc).
- If not next\_possible\_transitions.
  - Return no value.
- Set roles from set of t.allowed for t drawn from next\_possible\_transitions.
  - Draw t from next\_possible\_transitions.
- Evaluate create\_workflow\_actions\_for\_roles(roles, doc).
- If (send\_email\_alert(workflow) and Platform.db.get\_value(“Workflow Document State”, filters = mapping(“parent” → workflow, “state” → get\_doc\_workflow\_state(doc)), fieldname = “send\_email”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in send\_email\_alert(workflow) → Platform.db.get\_value(“Workflow Document State”, filters = mapping(“parent” → workflow, “state” → get\_doc\_workflow\_state(doc)), fieldname = “send\_email”).
  - Evaluate enqueue(send\_workflow\_action\_email, queue = “short”, doc = doc, transitions = next\_possible\_transitions, enqueue\_after\_commit = true, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(send\_workflow\_action\_email, queue = “short”, doc = doc, transitions = next\_possible\_transitions, enqueue\_after\_commit = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L4251) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1623)

<a id="op-a4708222af72c2"></a>
### Apply action

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_apply_action`

**Inputs** action, doctype, docname, current\_state, user = no value, last\_modified = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- If not verify\_request().
  - Return no value.
- Set doc from Platform.get\_doc(doctype, docname).
- Set doc\_workflow\_state from get\_doc\_workflow\_state(doc).
- If doc\_workflow\_state equals current\_state.
  - Set action\_link from get\_confirm\_workflow\_action\_url(doc, action, user).
  - If (not last\_modified or get\_datetime(doc.modified) equals get\_datetime(last\_modified)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not last\_modified → get\_datetime(doc.modified) equals get\_datetime(last\_modified).
    - Evaluate return\_action\_confirmation\_page(doc, action, action\_link).
  - Otherwise.
    - Evaluate return\_action\_confirmation\_page(doc, action, action\_link, alert\_doc\_change = true).
- Otherwise.
  - Evaluate return\_link\_expired\_page(doc, doc\_workflow\_state).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L4894) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1602)

<a id="op-56f308161b63cb"></a>
### Confirm action

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_confirm_action`

**Inputs** doctype, docname, user, action.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- If not verify\_request().
  - Return no value.
- Set doc from Platform.get\_doc(doctype, docname).
- Set newdoc from run\_workflow\_transition(doc, action).
- Evaluate Platform.db.commit().
- Evaluate return\_success\_page(newdoc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L67) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1604)

<a id="op-5af7fd61351a06"></a>
### Return success page

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_return_success_page`

**Inputs** doc.

**Local steps**

- Evaluate Platform.respond\_as\_web\_page(translated “Success”, translated “{0}: {1} is set to state {2}”.format(doc.get(“doctype”), Platform.bold(doc.get(“name”)), Platform.bold(get\_doc\_workflow\_state(doc))), indicato ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L5609) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1626)

<a id="op-f889709e2c97d7"></a>
### Return action confirmation page

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_return_action_confirmation_page`

**Inputs** doc, action, action\_link, alert\_doc\_change = false.

**Local steps**

- Set template\_params from mapping(“title” → doc.get(“name”), “doctype” → doc.get(“doctype”), “docname” → doc.get(“name”), “action” → action, …).
- Set template\_params at “pdf\_link” from get\_pdf\_link(doc.get(“doctype”), doc.get(“name”)).
- Evaluate Platform.respond\_as\_web\_page(title = no value, html = no value, indicator\_color = “blue”, template = “confirm\_workflow\_action”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L5819) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1624)

<a id="op-8376c66e3357dc"></a>
### Return link expired page

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_return_link_expired_page`

**Inputs** doc, doc\_workflow\_state.

**Record and data access** read “User” via get\_value.

**Local steps**

- Set user\_full\_name from (get\_user\_who\_set\_workflow\_state(doc, doc\_workflow\_state) or Platform.get\_value(“User”, doc.get(“modified\_by”), “full\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_user\_who\_set\_workflow\_state(doc, doc\_workflow\_state) → Platform.get\_value(“User”, doc.get(“modified\_by”), “full\_name”).
- Evaluate Platform.respond\_as\_web\_page(translated “Link Expired”, translated “Document {0} has been set to state {1} by {2}”.format(Platform.bold(doc.get(“name”)), Platform.bold(doc\_workflow\_state), Platform.bold(us ….
  - Value choice on user\_full\_name — true gives user\_full\_name, false gives Platform.get\_value(“User”, doc.get(“modified\_by”), “full\_name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L6208) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1625)

<a id="op-c0aad4c2fc1fea"></a>
### Get user who set workflow state

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_user_who_set_workflow_state`

**Inputs** doc, doc\_workflow\_state.

**Record and data access** read “Workflow Transition” via get\_all · read “User” via get\_value.

**Explicit results** no value · Platform.get\_value(“User”, completed\_by at 0 at 0, “full\_name”).

**Local steps**

- Set workflow\_name from get\_workflow\_name(doc.get(“doctype”)).
- If not workflow\_name.
  - Return no value.
- Set from\_states from Platform.get\_all(“Workflow Transition”, filters = mapping(“parent” → workflow\_name, “next\_state” → doc\_workflow\_state), pluck = “state”).
- If not from\_states.
  - Return no value.
- Set WorkflowAction from DocType(“Workflow Action”).
- Set completed\_by from nested operand in the contract(nested operand in the contract).orderby(WorkflowAction.modified, order = nested operand in the contract.qb.desc).limit(1).run().
- If (completed\_by and completed\_by at 0 at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in completed\_by → completed\_by at 0 at 0.
  - Return Platform.get\_value(“User”, completed\_by at 0 at 0, “full\_name”).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1615)

<a id="op-27ae17018fc462"></a>
### Update completed workflow actions

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_update_completed_workflow_actions`

**Inputs** doc, user = no value, workflow = no value, workflow\_state = no value.

**Explicit results** no value.

**Local steps**

- Set allowed\_roles from get\_allowed\_roles(user, workflow, workflow\_state).
- If not allowed\_roles.
  - Return no value.
- If workflow\_action bound to get\_workflow\_action\_by\_role(doc, allowed\_roles).
  - Evaluate update\_completed\_workflow\_actions\_using\_role(user, workflow\_action).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L623) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1628)

<a id="op-dc3dc75b7890ca"></a>
### Get allowed roles

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_allowed_roles`

**Inputs** user, workflow, workflow\_state.

**Record and data access** read “Workflow Transition” via get\_all.

**Explicit results** set(allowed\_roles).intersection(user\_roles).

**Local steps**

- Set user from user when user, otherwise Platform.session.user.
  - Value choice on user — true gives user, false gives Platform.session.user.
- Set allowed\_roles from Platform.get\_all(“Workflow Transition”, fields = “allowed”, filters = list(list(“parent”, “=”, workflow), list(“next\_state”, “=”, workflow\_state)), pluck = “allowed”).
- Set user\_roles from set(Platform.get\_roles(user)).
- Return set(allowed\_roles).intersection(user\_roles).

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L799) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1607)

<a id="op-db27f6c7175a38"></a>
### Get workflow action by role

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_workflow_action_by_role`

**Inputs** doc, allowed\_roles.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(WorkflowActionPermittedRole.role).limit(1).run(as\_dict = true).

**Local steps**

- Set WorkflowAction from DocType(“Workflow Action”).
- Set WorkflowActionPermittedRole from DocType(“Workflow Action Permitted Role”).
- Return nested operand in the contract(nested operand in the contract).orderby(WorkflowActionPermittedRole.role).limit(1).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L1073) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1618)

<a id="op-f17b7d69a7a055"></a>
### Update completed workflow actions using role

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_update_completed_workflow_actions_using_role`

**Inputs** user = no value, workflow\_action = no value.

**Explicit results** no value.

**Local steps**

- Set user from user when user, otherwise Platform.session.user.
  - Value choice on user — true gives user, false gives Platform.session.user.
- Set WorkflowAction from DocType(“Workflow Action”).
- If not workflow\_action.
  - Return no value.
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(WorkflowAction.modified\_by, user).where(WorkflowAction.name equals workflow\_action at 0.name).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L1506) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1629)

<a id="op-041d8c4fa0005b"></a>
### Get next possible transitions

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_next_possible_transitions`

**Inputs** workflow\_name, state, doc = no value.

**Record and data access** read “Workflow Transition” via get\_all.

**Explicit results** transitions\_to\_return.

**Local steps**

- Set transitions from Platform.get\_all(“Workflow Transition”, fields = list(“allowed”, “action”, “state”, “allow\_self\_approval”, …), filters = list(list(“parent”, “=”, workflow\_name), list(“state”, “=”, state))).
- Set transitions\_to\_return from list().
- For each transition in transitions.
  - Set is\_next\_state\_optional from get\_state\_optional\_field\_value(workflow\_name, transition.next\_state).
  - If is\_next\_state\_optional.
    - Continue with the next iteration or loop test.
  - If not is\_transition\_condition\_satisfied(transition, doc).
    - Continue with the next iteration or loop test.
  - Evaluate transitions\_to\_return.append(transition).
- Return transitions\_to\_return.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L1858) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1611)

<a id="op-fc3fa71a2464fd"></a>
### Get users next action data

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_users_next_action_data`

**Inputs** transitions, doc.

**Record and data access** read “User” via get\_value.

**Explicit results** user\_data\_map.

**Local steps**

- Set user\_data\_map from mapping().
- Bind local operation user\_has\_permission for subsequent calls.
- For each transition in transitions.
  - Set users from get\_users\_with\_role(transition.allowed).
  - Set filtered\_users from list of user for user drawn from users where (has\_approval\_access(user, doc, transition) and user\_has\_permission(user)).
    - Draw user from users, keep a combination only if ((has\_approval\_access(user, doc, transition) and user\_has\_permission(user))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_approval\_access(user, doc, transition) → user\_has\_permission(user).
  - If (doc.get(“owner”) belongs to filtered\_users and not transition.get(“send\_email\_to\_creator”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“owner”) belongs to filtered\_users → not transition.get(“send\_email\_to\_creator”).
    - Evaluate filtered\_users.remove(doc.get(“owner”)).
  - For each user in filtered\_users.
    - If not user\_data\_map.get(user).
      - Set user\_data\_map at user from Platform.\_dict(mapping(“possible\_actions” → list(), “email” → Platform.db.get\_value(“User”, user, “email”))).
    - Evaluate user\_data\_map at user.get(“possible\_actions”).append(Platform.\_dict(mapping(“action\_name” → transition.action, “action\_link” → get\_workflow\_action\_url(transition.action, doc, user)))).
- Return user\_data\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L2203) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1616)

<a id="op-d501a6168f22fc"></a>
### Get users next action data.user has permission

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_users_next_action_data_user_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L2846) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1617)

<a id="op-a74d83266cf004"></a>
### Create workflow actions for roles

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_create_workflow_actions_for_roles`

**Inputs** roles, doc.

**Record and data access** resolve a document from mapping(“doctype” → “Workflow Action”, “reference\_doctype” → doc.get(“doctype”), “reference\_name” → doc.get(“name”), “workflow\_state” → get\_doc\_workflow\_state(doc), …) via get\_doc.

**State and service calls** call insert on workflow\_action.

**Explicit results** no value.

**Local steps**

- If not roles.
  - Return no value.
- Set workflow\_action from Platform.get\_doc(mapping(“doctype” → “Workflow Action”, “reference\_doctype” → doc.get(“doctype”), “reference\_name” → doc.get(“name”), “workflow\_state” → get\_doc\_workflow\_state(doc), …)).
- For each role in roles.
  - Evaluate workflow\_action.append(“permitted\_roles”, mapping(“role” → role)).
- Evaluate workflow\_action.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L2936) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1605)

<a id="op-0295db2b983e55"></a>
### Send workflow action email

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_send_workflow_action_email`

**Inputs** doc, transitions.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Set users\_data from get\_users\_next\_action\_data(transitions, doc).
- Set common\_args from get\_common\_email\_args(doc).
- Set message from common\_args.pop(“message”, no value).
- For each data in users\_data.values().
  - Set email\_args from mapping(“recipients” → list(data.get(“email”)), “args” → mapping(“actions” → list(deduplicate\_actions(data.get(“possible\_actions”))), “message” → message), “reference\_name” → doc.name, “reference\_doctype”  ….
  - Evaluate email\_args.update(common\_args).
  - Attempt the following.
    - Evaluate Platform.sendmail(expanded names email\_args).
  - On failure (Platform.OutgoingEmailError).
    - Evaluate Platform.log\_error(“Failed to send workflow action email”).
    - Return no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(expanded names email\_args).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L3257) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1627)
