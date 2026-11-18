# Record lifecycle and persistence · operations 109

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Workflow

<a id="op-9bd274ff42e898"></a>
### Set workflow state on action

`operation_foundation_model_workflow_business_behavior_set_workflow_state_on_action`

**Inputs** doc, workflow\_name, action.

**Record and data access** resolve a document from “Workflow” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set workflow from Platform.get\_doc(“Workflow”, workflow\_name).
- Set workflow\_state\_field from workflow.workflow\_state\_field.
- For each state in workflow.states.
  - If (state.state equals doc.get(workflow\_state\_field) and doc.docstatus equals cint(state.doc\_status)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in state.state equals doc.get(workflow\_state\_field) → doc.docstatus equals cint(state.doc\_status).
    - Return no value.
- Set action\_map from mapping(“update\_after\_submit” → “1”, “submit” → “1”, “cancel” → “2”).
- Set docstatus from action\_map at action.
- For each state in workflow.states.
  - If state.doc\_status equals docstatus.
    - Evaluate doc.set(workflow\_state\_field, state.state).
    - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1366)
