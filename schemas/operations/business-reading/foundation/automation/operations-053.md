# Workflow, automation and dispatch · operations 53

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workflow action

[Record definition](../../../../data/record-types/workflow_action.json)

<a id="op-4ddd191c078a0d"></a>
### Deduplicate actions

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_deduplicate_actions`

**Inputs** action\_list.

**Explicit results** action\_map.values().

**Local steps**

- Set action\_map from mapping().
- For each action\_data in action\_list.
  - If not action\_map.get(action\_data.action\_name).
    - Set action\_map at action\_data.action\_name from action\_data.
- Return action\_map.values().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L3703) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1606)

<a id="op-a67cc0fd22b85e"></a>
### Get workflow action url

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_workflow_action_resource_address`

**Inputs** action, doc, user.

**Explicit results** get\_url(((apply\_action\_method + “?”) + get\_signed\_params(params))).

**Local steps**

- Set apply\_action\_method from “/api/method/Platform.workflow.doctype.workflow\_action.workflow\_action.apply\_action”.
- Set params from mapping(“doctype” → doc.get(“doctype”), “docname” → doc.get(“name”), “action” → action, “current\_state” → get\_doc\_workflow\_state(doc), …).
- Return get\_url(((apply\_action\_method + “?”) + get\_signed\_params(params))).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L3838) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1619)

<a id="op-654acbde999c98"></a>
### Get confirm workflow action url

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_confirm_workflow_action_resource_address`

**Inputs** doc, action, user.

**Explicit results** get\_url(((confirm\_action\_method + “?”) + get\_signed\_params(params))).

**Local steps**

- Set confirm\_action\_method from “/api/method/Platform.workflow.doctype.workflow\_action.workflow\_action.confirm\_action”.
- Set params from mapping(“action” → action, “doctype” → doc.get(“doctype”), “docname” → doc.get(“name”), “user” → user).
- Return get\_url(((confirm\_action\_method + “?”) + get\_signed\_params(params))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L4133) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1609)

<a id="op-a478371409b701"></a>
### Is workflow action already created

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_is_workflow_action_already_created`

**Inputs** doc.

**Record and data access** read mapping(“doctype” → “Workflow Action”, “reference\_name” → doc.get(“name”), “reference\_doctype” → doc.get(“doctype”), “workflow\_state” → get\_doc\_workflow\_state(doc), …) via exists.

**Explicit results** Platform.db.exists(mapping(“doctype” → “Workflow Action”, “reference\_name” → doc.get(“name”), “reference\_doctype” → doc.get(“doctype”), “workflow\_state” → get\_doc\_workflow\_state(doc), …)).

**Local steps**

- Return Platform.db.exists(mapping(“doctype” → “Workflow Action”, “reference\_name” → doc.get(“name”), “reference\_doctype” → doc.get(“doctype”), “workflow\_state” → get\_doc\_workflow\_state(doc), …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L4367) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1621)

<a id="op-b6ebc973278f42"></a>
### Clear workflow actions

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_clear_workflow_actions`

**Inputs** doctype, name.

**State and service calls** request delete on “Workflow Action”.

**Explicit results** no value.

**Local steps**

- If not (doctype and name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.
  - Return no value.
- Evaluate Platform.db.delete(“Workflow Action”, filters = mapping(“reference\_name” → name, “reference\_doctype” → doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L4567) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1603)

<a id="op-5873b48884c61a"></a>
### Get doc workflow state

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_record_workflow_state`

**Inputs** doc.

**Explicit results** doc.get(workflow\_state\_field).

**Local steps**

- Set workflow\_name from get\_workflow\_name(doc.get(“doctype”)).
- Set workflow\_state\_field from get\_workflow\_state\_field(workflow\_name).
- Return doc.get(workflow\_state\_field).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L4710) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1613)

<a id="op-147dbba9c02a13"></a>
### Get common email args

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_common_email_arguments`

**Inputs** doc.

**Record and data access** read “Print Format” via get\_cached\_value.

**Explicit results** mapping(“template” → “workflow\_action”, “header” → “Workflow Action”, “attachments” → attachments, “subject” → subject, …).

**Local steps**

- Set doctype from doc.get(“doctype”).
- Set docname from doc.get(“name”).
- Set email\_template from get\_email\_template\_from\_workflow(doc).
- If email\_template.
  - Set subject from email\_template.get(“subject”).
  - Set response from email\_template.get(“message”).
- Otherwise.
  - Set subject from (translated “Workflow Action” + formatted text  on {doctype}: {docname}).
  - Set response from get\_link\_to\_form(doctype, docname, formatted text {doctype}: {docname}).
- Set print\_format from doc.meta.default\_print\_format.
- Set lang from (doc.get(“language”) or Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”) when print\_format, otherwise no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“language”) → Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”) when print\_format, otherwise no value.
  - Value choice on print\_format — true gives Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”), false gives no value.
- Attempt the following.
  - Set attachments from list(Platform.attach\_print(doctype, docname, file\_name = docname, doc = doc, lang = lang, print\_format = print\_format)).
- On failure (Platform.PermissionError).
  - Set attachments from list().
- Return mapping(“template” → “workflow\_action”, “header” → “Workflow Action”, “attachments” → attachments, “subject” → subject, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L68) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1608)

<a id="op-804bba6f68e23a"></a>
### Get email template from workflow

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_email_template_from_workflow`

**Inputs** doc.

**Record and data access** read “Workflow Document State” via get\_value · resolve a document from “Email Template” via get\_doc.

**Explicit results** no value · Platform.get\_doc(“Email Template”, template\_name).get\_formatted\_email(doc).

**Local steps**

- Set workflow\_name from get\_workflow\_name(doc.get(“doctype”)).
- Set doc\_state from get\_doc\_workflow\_state(doc).
- Set template\_name from Platform.db.get\_value(“Workflow Document State”, mapping(“parent” → workflow\_name, “state” → doc\_state), “next\_action\_email\_template”).
- If not template\_name.
  - Return no value.
- If isinstance(doc, Document).
  - Set doc from doc.as\_dict().
- Return Platform.get\_doc(“Email Template”, template\_name).get\_formatted\_email(doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L5439) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1610)

<a id="op-eaefd4943cc33e"></a>
### Get state optional field value

`operation_foundation_workflow_record_definitions_workflow_action_business_behavior_get_state_optional_field_value`

**Inputs** workflow\_name, state.

**Record and data access** read “Workflow Document State” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Workflow Document State”, mapping(“parent” → workflow\_name, “state” → state), “is\_optional\_state”).

**Local steps**

- Return Platform.get\_cached\_value(“Workflow Document State”, mapping(“parent” → workflow\_name, “state” → state), “is\_optional\_state”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Workflow Document State”, mapping(“parent” → workflow\_name, “state” → state), “is\_optional\_state”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L5748) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1614)
