# Workflow declarations in frappe

Each dictionary part contains an ordered field list, source location, record settings and grants. The source column opens the declaration at the reviewed revision.

| Record | Storage | Fields | Dictionary | Source |
|---|---|---:|---|---|
| Workflow | ordinary | 12 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow/workflow.json) |
| Workflow Action | ordinary | 9 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_action/workflow_action.json) |
| Workflow Action Master | ordinary | 1 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_action_master/workflow_action_master.json) |
| Workflow Action Permitted Role | child | 1 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_action_permitted_role/workflow_action_permitted_role.json) |
| Workflow Document State | child | 14 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_document_state/workflow_document_state.json) |
| Workflow State | ordinary | 3 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_state/workflow_state.json) |
| Workflow Transition | child | 12 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_transition/workflow_transition.json) |
| Workflow Transition Task | child | 4 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_transition_task/workflow_transition_task.json) |
| Workflow Transition Tasks | ordinary | 1 | [Part 1](../catalog/frappe-workflow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/workflow/doctype/workflow_transition_tasks/workflow_transition_tasks.json) |
