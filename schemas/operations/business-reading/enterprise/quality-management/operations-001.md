# Quality assurance · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Quality action

[Record definition](../../../../data/record-types/quality_action.json)

<a id="op-708cf93820cc98"></a>
### Quality Action.validate

`operation_enterprise_quality_management_record_definitions_quality_action_business_behavior_quality_action_validate`

**Inputs** self.

**Local steps**

- Set is\_completed from (self.resolutions and all(generator of d.status equals “Completed” for d drawn from self.resolutions)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.resolutions → all(generator of d.status equals “Completed” for d drawn from self.resolutions).
  - Draw d from self.resolutions.
- Set self.status from “Completed” when is\_completed, otherwise “Open”.
  - Value choice on is\_completed — true gives “Completed”, false gives “Open”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L909)

## Record · Quality feedback

[Record definition](../../../../data/record-types/quality_feedback.json)

<a id="op-34b14766c11d08"></a>
### Quality Feedback.set parameters

`operation_enterprise_quality_management_record_definitions_quality_feedback_business_behavior_quality_feedback_set_parameters`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Quality Feedback Template” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.template.
  - Return no value.
- Evaluate self.set(“parameters”, list()).
- For each d in Platform.get\_doc(“Quality Feedback Template”, self.template).parameters.
  - Evaluate self.append(“parameters”, dict(parameter = d.parameter)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L910)

<a id="op-c1e396b4dcf12f"></a>
### Quality Feedback.validate

`operation_enterprise_quality_management_record_definitions_quality_feedback_business_behavior_quality_feedback_validate`

**Inputs** self.

**Local steps**

- If not self.document\_name.
  - Set self.document\_type from “User”.
  - Set self.document\_name from Platform.session.user.
- If not self.parameters.
  - Evaluate self.set\_parameters().
- Otherwise.
  - Evaluate self.validate\_parameters().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set parameters](operations-001.md#op-34b14766c11d08), [validate parameters](operations-001.md#op-aaabdcfb2c9894).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L911)

<a id="op-aaabdcfb2c9894"></a>
### Quality Feedback.validate parameters

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_feedback_quality_feedback_qualityfeedback_validate_parameters`

**Inputs** self.

**Record and data access** read “Quality Feedback Template Parameter” via get\_all.

**Explicit failure paths** validation helper — translated “Row #{0}: Parameter {1} is not part of Quality Feedback Template {2}”.format(d.idx, Platform.bold(d.parameter), Platform.bold(self.template)).

**Local steps**

- Set parameters from Platform.get\_all(“Quality Feedback Template Parameter”, filters = mapping(“parent” → self.template, “parenttype” → “Quality Feedback Template”), pluck = “parameter”).
- For each d in self.get\_parameters\_to\_validate().
  - If d.parameter does not belong to parameters.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Parameter {1} is not part of Quality Feedback Template {2}”.format(d.idx, Platform.bold(d.parameter), Platform.bold(self.template))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get parameters to validate](operations-001.md#op-35543c3157a346).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L256) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1381)

<a id="op-35543c3157a346"></a>
### Quality Feedback.get parameters to validate

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_feedback_quality_feedback_qualityfeedback_get_parameters_to_validate`

**Inputs** self.

**Explicit results** self.parameters · list of d for d drawn from self.parameters where (d.name does not belong to previous or previous at d.name differs from d.parameter).

**Local steps**

- If self.has\_value\_changed(“template”).
  - Return self.parameters.
- Set previous from mapping of d.name → d.parameter for d drawn from self.get\_doc\_before\_save().parameters.
  - Draw d from self.get\_doc\_before\_save().parameters.
- Return list of d for d drawn from self.parameters where (d.name does not belong to previous or previous at d.name differs from d.parameter).
  - Draw d from self.parameters, keep a combination only if ((d.name does not belong to previous or previous at d.name differs from d.parameter)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.name does not belong to previous → previous at d.name differs from d.parameter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L255) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1380)

## Record · Quality feedback template

[Record definition](../../../../data/record-types/quality_feedback_template.json)

<a id="op-5b5ead7fab9fef"></a>
### Quality Feedback Template.validate

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_feedback_template_quality_feedback_template_qualityfeedbacktemplate_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Parameter {1} is already added”.format(d.idx, Platform.bold(d.parameter)).

**Local steps**

- Set parameters from set().
- For each d in self.parameters.
  - If d.parameter belongs to parameters.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Parameter {1} is already added”.format(d.idx, Platform.bold(d.parameter))).
  - Evaluate parameters.add(d.parameter).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L257) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1382)

## Record · Quality goal

[Record definition](../../../../data/record-types/quality_goal.json)

<a id="op-f1a4846443f8b1"></a>
### Quality Goal.validate

`operation_enterprise_quality_management_record_definitions_quality_goal_business_behavior_quality_goal_validate`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L5033) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L913)

## Record · Quality procedure

[Record definition](../../../../data/record-types/quality_procedure.json)

<a id="op-641d08926c83d8"></a>
### Quality Procedure.before save

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.check\_for\_incorrect\_child().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check for incorrect child](operations-001.md#op-46b1f799ee91a5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L5295) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L919)

<a id="op-388374615a5737"></a>
### Quality Procedure.on update

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_on_update`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_update(self).
- Evaluate self.set\_parent().
- Evaluate self.remove\_parent\_from\_old\_child().
- Evaluate self.add\_child\_to\_parent().
- Evaluate self.remove\_child\_from\_old\_parent().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set parent](operations-001.md#op-57444e534ae23e), [remove parent from old child](operations-001.md#op-c23c8a922bcb2c), [add child to parent](operations-001.md#op-9d65df195f0c8d), [remove child from old parent](operations-001.md#op-57ccb15fa7b3ab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L5346) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L922)

<a id="op-46b4a490408234"></a>
### Quality Procedure.on trash

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_on_trash`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- Evaluate Platform.db.sql(“update ′tabQuality Procedure Process′\\n\\t\\t\\tset ′procedure′='' where ′procedure′=%s”, self.name).
- Evaluate NestedSet.on\_trash(self, allow\_root\_deletion = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L921)

<a id="op-46b1f799ee91a5"></a>
### Quality Procedure.check for incorrect child

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_check_for_incorrect_child`

**Inputs** self.

**Record and data access** read “Quality Procedure” via get\_value.

**Explicit failure paths** validation helper — translated “{0} already has a Parent Procedure {1}.”.format(Platform.bold(process.procedure), Platform.bold(parent\_quality\_procedure)).

**Local steps**

- For each process in self.processes.
  - If process.procedure.
    - Set self.is\_group from 1.
    - Set parent\_quality\_procedure from Platform.db.get\_value(“Quality Procedure”, process.procedure, “parent\_quality\_procedure”).
    - If (parent\_quality\_procedure and parent\_quality\_procedure differs from self.name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_quality\_procedure → parent\_quality\_procedure differs from self.name.
      - Call the validation error handler Platform.throw(translated “{0} already has a Parent Procedure {1}.”.format(Platform.bold(process.procedure), Platform.bold(parent\_quality\_procedure)), title = translated “Invalid Child Procedure”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L5770) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L920)

<a id="op-57444e534ae23e"></a>
### Quality Procedure.set parent

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_set_parent`

**Inputs** self.

**Record and data access** read “Quality Procedure” via get\_value.

**Local steps**

- For each process in self.processes.
  - If process.procedure.
    - If not Platform.db.get\_value(“Quality Procedure”, process.procedure, “parent\_quality\_procedure”).
      - Evaluate self.set\_parent\_of\_child(process.procedure, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set parent of child](operations-001.md#op-6bc84af2f81b87).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L925)

<a id="op-c23c8a922bcb2c"></a>
### Quality Procedure.remove parent from old child

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_remove_parent_from_old_child`

**Inputs** self.

**Record and data access** read “Quality Procedure” via get\_all.

**Local steps**

- If old\_doc bound to self.get\_doc\_before\_save().
  - If old\_child\_procedures bound to set(list of d.procedure for d drawn from old\_doc.processes where d.procedure).
    - Draw d from old\_doc.processes, keep a combination only if (d.procedure).
    - Set current\_child\_procedures from set(list of d.procedure for d drawn from self.processes where d.procedure).
      - Draw d from self.processes, keep a combination only if (d.procedure).
    - If removed\_child\_procedures bound to list(old\_child\_procedures.difference(current\_child\_procedures)).
      - For each child\_procedure in Platform.get\_all(“Quality Procedure”, filters = mapping(“name” → list(“in”, removed\_child\_procedures), “parent\_quality\_procedure” → self.name), pluck = “name”).
        - Evaluate self.set\_parent\_of\_child(child\_procedure, no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set parent of child](operations-001.md#op-6bc84af2f81b87).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L924)

<a id="op-6bc84af2f81b87"></a>
### Quality Procedure.set parent of child

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_procedure_quality_procedure_qualityprocedure_set_parent_of_child`

**Inputs** self, procedure, parent.

**Record and data access** resolve a document from “Quality Procedure” via get\_doc · read “Quality Procedure” via get\_value.

**State and service calls** call save on child.

**Local steps**

- Set child from Platform.get\_doc(“Quality Procedure”, procedure).
- Set child.parent\_quality\_procedure from parent.
- Evaluate child.save().
- Set tuple(self.lft, self.rgt) from Platform.db.get\_value(“Quality Procedure”, self.name, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L258) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1383)

<a id="op-9d65df195f0c8d"></a>
### Quality Procedure.add child to parent

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_add_child_to_parent`

**Inputs** self.

**Record and data access** resolve a document from “Quality Procedure” via get\_doc.

**State and service calls** call save on parent.

**Local steps**

- If self.parent\_quality\_procedure.
  - Set parent from Platform.get\_doc(“Quality Procedure”, self.parent\_quality\_procedure).
  - If not list of d for d drawn from parent.processes where d.procedure equals self.name.
    - Draw d from parent.processes, keep a combination only if (d.procedure equals self.name).
    - Evaluate parent.append(“processes”, mapping(“procedure” → self.name, “process\_description” → self.name)).
    - Evaluate parent.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L6536) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L918)

<a id="op-57ccb15fa7b3ab"></a>
### Quality Procedure.remove child from old parent

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_quality_procedure_remove_child_from_old_parent`

**Inputs** self.

**Record and data access** resolve a document from “Quality Procedure” via get\_doc.

**State and service calls** call save on parent.

**Local steps**

- If old\_doc bound to self.get\_doc\_before\_save().
  - If old\_parent bound to old\_doc.parent\_quality\_procedure.
    - If self.parent\_quality\_procedure differs from old\_parent.
      - Set parent from Platform.get\_doc(“Quality Procedure”, old\_parent).
      - If rows bound to list of d for d drawn from parent.processes where d.procedure equals self.name.
        - Draw d from parent.processes, keep a combination only if (d.procedure equals self.name).
        - For each row in rows.
          - Evaluate parent.remove(row).
        - Evaluate parent.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L923)

<a id="op-c79f8580bfc1fc"></a>
### Get children

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_get_children`

**Inputs** doctype, parent = no value, parent\_quality\_procedure = no value, is\_root = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Quality Procedure” via get\_doc · read “Quality Procedure” via get\_value · read “Quality Procedure” via get\_list.

**Explicit results** list of dict(value = d.procedure, expandable = Platform.db.get\_value(“Quality Procedure”, d.procedure, “is\_group”)) for d drawn from parent\_procedure.processes where d.procedure · Platform.get\_list(“Quality Procedure”, fields = list(“name as value”, “is\_group as expandable”), filters = dict(parent\_quality\_procedure = parent), order\_by = “name asc”).

**Local steps**

- If (parent is identical to no value or parent equals “All Quality Procedures”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent is identical to no value → parent equals “All Quality Procedures”.
  - Set parent from empty text.
- If parent.
  - Set parent\_procedure from Platform.get\_doc(“Quality Procedure”, parent).
  - Evaluate parent\_procedure.check\_permission(“read”).
  - Return list of dict(value = d.procedure, expandable = Platform.db.get\_value(“Quality Procedure”, d.procedure, “is\_group”)) for d drawn from parent\_procedure.processes where d.procedure.
    - Draw d from parent\_procedure.processes, keep a combination only if (d.procedure).
- Otherwise.
  - Return Platform.get\_list(“Quality Procedure”, fields = list(“name as value”, “is\_group as expandable”), filters = dict(parent\_quality\_procedure = parent), order\_by = “name asc”).

**Values supplied outside this operation** effective access from parent\_procedure.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L917)

<a id="op-cdf7e54400c274"></a>
### Add node

`operation_enterprise_quality_management_record_definitions_quality_procedure_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Explicit results** Platform.get\_doc(args).insert().

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from Platform.form\_dict.
- Set args from make\_tree\_args(expanded names args).
- If args.parent\_quality\_procedure equals “All Quality Procedures”.
  - Set args.parent\_quality\_procedure from no value.
- Return Platform.get\_doc(args).insert().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0614.json#L657) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L916)

## Record · Quality review

[Record definition](../../../../data/record-types/quality_review.json)

<a id="op-51efe9c7702e90"></a>
### Quality Review.validate

`operation_enterprise_quality_management_record_definitions_quality_review_business_behavior_quality_review_validate`

**Inputs** self.

**Local steps**

- If not self.reviews.
  - Evaluate self.set\_objectives().
- Otherwise.
  - Evaluate self.validate\_objectives().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set objectives](operations-001.md#op-3a616199516554), [validate objectives](operations-001.md#op-c34b199c6f7602), [set status](operations-001.md#op-d064524103b342).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L933)

<a id="op-3a616199516554"></a>
### Quality Review.set objectives

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_review_quality_review_qualityreview_set_objectives`

**Inputs** self.

**Record and data access** resolve a document from “Quality Goal” via get\_doc.

**Local steps**

- For each d in Platform.get\_doc(“Quality Goal”, self.goal).objectives.
  - Evaluate self.append(“reviews”, dict(objective = d.objective, target = d.target, uom = d.uom, status = “Open”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L261) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1386)

<a id="op-c34b199c6f7602"></a>
### Quality Review.validate objectives

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_review_quality_review_qualityreview_validate_objectives`

**Inputs** self.

**Record and data access** read “Quality Goal Objective” via get\_all.

**Explicit failure paths** validation helper — translated “Row #{0}: Objective {1} is not part of Quality Goal {2}”.format(d.idx, Platform.bold(d.objective), Platform.bold(self.goal)).

**Local steps**

- Set objectives from Platform.get\_all(“Quality Goal Objective”, filters = mapping(“parent” → self.goal, “parenttype” → “Quality Goal”), pluck = “objective”).
- For each d in self.get\_reviews\_to\_validate().
  - If d.objective does not belong to objectives.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Objective {1} is not part of Quality Goal {2}”.format(d.idx, Platform.bold(d.objective), Platform.bold(self.goal))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reviews to validate](operations-001.md#op-d58f27c0615134).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L262) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1387)

<a id="op-d58f27c0615134"></a>
### Quality Review.get reviews to validate

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_review_quality_review_qualityreview_get_reviews_to_validate`

**Inputs** self.

**Explicit results** self.reviews · list of d for d drawn from self.reviews where (d.name does not belong to previous or previous at d.name differs from d.objective).

**Local steps**

- If self.has\_value\_changed(“goal”).
  - Return self.reviews.
- Set previous from mapping of d.name → d.objective for d drawn from self.get\_doc\_before\_save().reviews.
  - Draw d from self.get\_doc\_before\_save().reviews.
- Return list of d for d drawn from self.reviews where (d.name does not belong to previous or previous at d.name differs from d.objective).
  - Draw d from self.reviews, keep a combination only if ((d.name does not belong to previous or previous at d.name differs from d.objective)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.name does not belong to previous → previous at d.name differs from d.objective.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L260) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1385)

<a id="op-d064524103b342"></a>
### Quality Review.set status

`operation_enterprise_quality_management_record_definitions_quality_review_business_behavior_quality_review_set_status`

**Inputs** self.

**Local steps**

- If (not self.reviews or any(generator of d.status does not belong to tuple(“Passed”, “Failed”) for d drawn from self.reviews)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.reviews → any(generator of d.status does not belong to tuple(“Passed”, “Failed”) for d drawn from self.reviews).
  - Draw d from self.reviews.
  - Set self.status from “Open”.
- Otherwise.
  - If any(list of d.status equals “Failed” for d drawn from self.reviews).
    - Draw d from self.reviews.
    - Set self.status from “Failed”.
  - Otherwise.
    - Set self.status from “Passed”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L932)

<a id="op-51b8560f1a0627"></a>
### Review

`operation_enterprise_quality_management_record_definitions_quality_review_business_behavior_review`

**Inputs** no declared parameters.

**Record and data access** read “Quality Goal” via get\_list.

**Local steps**

- Set today from Platform.utils.getdate().
- Set weekday from today.strftime(“%A”).
- Set month from today.strftime(“%B”).
- For each goal in Platform.get\_list(“Quality Goal”, fields = list(“name”, “frequency”, “date”, “weekday”)).
  - If goal.frequency equals “Daily”.
    - Evaluate create\_review(goal.name).
  - Otherwise.
    - If (goal.frequency equals “Weekly” and goal.weekday equals weekday).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in goal.frequency equals “Weekly” → goal.weekday equals weekday.
      - Evaluate create\_review(goal.name).
    - Otherwise.
      - If (goal.frequency equals “Monthly” and is\_review\_date(goal.date, today)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in goal.frequency equals “Monthly” → is\_review\_date(goal.date, today).
        - Evaluate create\_review(goal.name).
      - Otherwise.
        - If (goal.frequency equals “Quarterly” and is\_review\_date(goal.date, today) and get\_quarter(month)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in goal.frequency equals “Quarterly” → is\_review\_date(goal.date, today) → get\_quarter(month).
          - Evaluate create\_review(goal.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L934)
