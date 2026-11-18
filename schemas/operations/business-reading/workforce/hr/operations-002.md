# Employment and attendance · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Appraisal

[Record definition](../../../../data/record-types/appraisal.json)

<a id="op-f1bff7b21b1c0e"></a>
### Appraisal.set appraisal template

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_set_appraisal_template`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Appraisee” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.appraisal\_cycle.
  - Return no value.
- Set appraisal\_template from Platform.db.get\_value(“Appraisee”, mapping(“employee” → self.employee, “parent” → self.appraisal\_cycle), “appraisal\_template”).
- If appraisal\_template.
  - Set self.appraisal\_template from appraisal\_template.
  - Evaluate self.set\_kras\_and\_rating\_criteria().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set kras and rating criteria](operations-002.md#op-cad21b9b707ac6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L4133) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L317) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L314)

<a id="op-cad21b9b707ac6"></a>
### Appraisal.set kras and rating criteria

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_set_kras_and_rating_criteria`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Appraisal Template” via get\_doc.

**Explicit results** no value · self.

**Local steps**

- If not self.appraisal\_template.
  - Return no value.
- Evaluate self.set(“appraisal\_kra”, list()).
- Evaluate self.set(“self\_ratings”, list()).
- Evaluate self.set(“goals”, list()).
- Set template from Platform.get\_doc(“Appraisal Template”, self.appraisal\_template).
- For each entry in template.goals.
  - Set table\_name from “goals” when self.rate\_goals\_manually, otherwise “appraisal\_kra”.
    - Value choice on self.rate\_goals\_manually — true gives “goals”, false gives “appraisal\_kra”.
  - Evaluate self.append(table\_name, mapping(“kra” → entry.key\_result\_area, “per\_weightage” → entry.per\_weightage)).
- For each entry in template.rating\_criteria.
  - Evaluate self.append(“self\_ratings”, mapping(“criteria” → entry.criteria, “per\_weightage” → entry.per\_weightage)).
- Return self.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L4346) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L320) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L317)

<a id="op-0ad816a7f7c1e1"></a>
### Appraisal.calculate total score

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_calculate_total_score`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Goal Score cannot be greater than {1}”.format(entry.idx, number\_of\_stars) · validation helper — translated “Total weightage for all {0} must add up to 100. Currently, it is {1}%”.format(table, total\_weightage).

**Local steps**

- Set tuple(total\_weightage, total, goal\_score\_percentage) from tuple(0, 0, 0).
- Set meta from Platform.get\_meta(“Appraisal Goal”).
- Set number\_of\_stars from (meta.get\_options(“score”) or 5).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_options(“score”) → 5.
- If self.rate\_goals\_manually.
  - Set table from translated “Goals”.
  - For each entry in self.goals.
    - If flt(entry.score) &gt; flt(number\_of\_stars).
      - Call the validation error handler Platform.throw(translated “Row {0}: Goal Score cannot be greater than {1}”.format(entry.idx, number\_of\_stars)).
    - Set entry.score\_earned from ((flt(entry.score) × flt(entry.per\_weightage)) ÷ 100).
    - Update total using + flt(entry.score\_earned).
    - Update total\_weightage using + flt(entry.per\_weightage).
- Otherwise.
  - Set table from translated “KRAs”.
  - For each entry in self.appraisal\_kra.
    - Update goal\_score\_percentage using + flt(entry.goal\_score).
    - Update total\_weightage using + flt(entry.per\_weightage).
  - Set self.goal\_score\_percentage from flt(goal\_score\_percentage, self.precision(“goal\_score\_percentage”)).
  - Set total from (flt(goal\_score\_percentage) ÷ 20).
- If (total\_weightage and flt(total\_weightage, 2) differs from 100.0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_weightage → flt(total\_weightage, 2) differs from 100.0.
  - Call the validation error handler Platform.throw(translated “Total weightage for all {0} must add up to 100. Currently, it is {1}%”.format(table, total\_weightage), title = translated “Incorrect Weightage Allocation”).
- Set self.total\_score from flt(total, self.precision(“total\_score”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L4783) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L316) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L313)

<a id="op-b7e4271f622c54"></a>
### Appraisal.calculate self appraisal score

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_calculate_self_appraisal_score`

**Inputs** self.

**Local steps**

- Set total from 0.
- Set meta from Platform.get\_meta(“Employee Feedback Rating”).
- Set number\_of\_stars from (meta.get\_options(“rating”) or 5).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_options(“rating”) → 5.
- For each entry in self.self\_ratings.
  - Set score from ((flt(entry.rating) × flt(number\_of\_stars)) × flt((entry.per\_weightage ÷ 100))).
  - Update total using + flt(score).
- Set self.self\_score from flt(total, self.precision(“self\_score”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L5594) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L315) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L312)

<a id="op-53fb826f66ff2d"></a>
### Appraisal.calculate avg feedback score

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_calculate_average_feedback_score`

**Inputs** self, update = false.

**State and service calls** call db\_update on self.

**Local steps**

- Set avg\_feedback\_score from Platform.qb.avg(“Employee Performance Feedback”, “total\_score”, mapping(“employee” → self.employee, “appraisal” → self.name, “docstatus” → 1)).
- Set self.avg\_feedback\_score from flt(avg\_feedback\_score, self.precision(“avg\_feedback\_score”)).
- If update.
  - Evaluate self.calculate\_final\_score().
  - Evaluate self.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate final score](operations-002.md#op-70355f2163bdaa).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L5892) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L313) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L310)

<a id="op-70355f2163bdaa"></a>
### Appraisal.calculate final score

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_calculate_final_score`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L6149) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L314) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L311)

<a id="op-d67a60d0777844"></a>
### Appraisal.add feedback

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_add_feedback`

**Inputs** self, feedback, feedback\_ratings.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** Document.

**Record and data access** resolve a document from mapping(“doctype” → “Employee Performance Feedback”, “appraisal” → self.name, “employee” → self.employee, “added\_on” → now(), …) via get\_doc · read “Employee” via get\_value.

**State and service calls** call submit on feedback.

**Explicit results** feedback.

**Local steps**

- Set feedback from Platform.get\_doc(mapping(“doctype” → “Employee Performance Feedback”, “appraisal” → self.name, “employee” → self.employee, “added\_on” → now(), …)).
- For each entry in feedback\_ratings.
  - Evaluate feedback.append(“feedback\_ratings”, mapping(“criteria” → entry.get(“criteria”), “rating” → entry.get(“rating”), “per\_weightage” → entry.get(“per\_weightage”))).
- Evaluate feedback.submit().
- Return feedback.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L6719) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L312) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L309)

<a id="op-22592bc36b7639"></a>
### Appraisal.set goal score

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_set_goal_score`

**Inputs** self, update = false.

**State and service calls** call db\_update on kra · call db\_update on self.

**Explicit results** self.

**Local steps**

- For each kra in self.appraisal\_kra.
  - Set Goal from Platform.qb.DocType(“Goal”).
  - Set avg\_goal\_completion from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0.
  - Set kra.goal\_completion from flt(avg\_goal\_completion, kra.precision(“goal\_completion”)).
  - Set kra.goal\_score from flt(((kra.goal\_completion × kra.per\_weightage) ÷ 100), kra.precision(“goal\_score”)).
  - If update.
    - Evaluate kra.db\_update().
- Evaluate self.calculate\_total\_score().
- If update.
  - Evaluate self.calculate\_final\_score().
  - Evaluate self.db\_update().
- Return self.

**Methods declared on this owner** [calculate total score](operations-002.md#op-0ad816a7f7c1e1), [calculate final score](operations-002.md#op-70355f2163bdaa).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0007.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L318) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L315)

<a id="op-dabc8e4aa428fa"></a>
### Get feedback history

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_get_feedback_history`

**Inputs** employee, appraisal.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Employee Performance Feedback” via get\_list · read “Employee Performance Feedback” via count · read “Appraisal” via get\_value.

**Explicit results** data.

**Local steps**

- Evaluate Platform.has\_permission(“Appraisal”, “read”, appraisal, throw = true).
- Set data from Platform.\_dict().
- Set data.feedback\_history from Platform.get\_list(“Employee Performance Feedback”, filters = mapping(“employee” → employee, “appraisal” → appraisal, “docstatus” → 1), fields = list(“feedback”, “reviewer”, “user”, “owner”, …), order\_by =  ….
- Set reviews\_per\_rating from list().
- Set feedback\_count from Platform.db.count(“Employee Performance Feedback”, filters = mapping(“appraisal” → appraisal, “employee” → employee, “docstatus” → 1)).
- For each i in range(1, 6).
  - Set count from Platform.db.count(“Employee Performance Feedback”, filters = mapping(“appraisal” → appraisal, “employee” → employee, “total\_score” → tuple(“between”, list(i, (i + 0.99))), “docstatus” → 1)).
  - Set percent from flt(((count ÷ feedback\_count) × 100), 0) when feedback\_count, otherwise 0.
    - Value choice on feedback\_count — true gives flt(((count ÷ feedback\_count) × 100), 0), false gives 0.
  - Evaluate reviews\_per\_rating.append(percent).
- Set data.reviews\_per\_rating from reviews\_per\_rating.
- Set data.avg\_feedback\_score from Platform.db.get\_value(“Appraisal”, appraisal, “avg\_feedback\_score”).
- Return data.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Appraisal”, “read”, appraisal, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0007.json#L616) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L323) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L320)

<a id="op-dfe66c3d49eb7e"></a>
### Get kras for employee

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_get_kras_for_employee`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** tuple at tuple at str.

**Record and data access** read “Appraisal” via get\_value · read “Appraisal KRA” via get\_all.

**Explicit results** Platform.get\_all(“Appraisal KRA”, filters = mapping(“parent” → appraisal, “kra” → tuple(“like”, formatted text {txt}%)), fields = list(“kra”), as\_list = 1).

**Local steps**

- Set appraisal from Platform.db.get\_value(“Appraisal”, mapping(“appraisal\_cycle” → filters.get(“appraisal\_cycle”), “employee” → filters.get(“employee”)), “name”).
- Return Platform.get\_all(“Appraisal KRA”, filters = mapping(“parent” → appraisal, “kra” → tuple(“like”, formatted text {txt}%)), fields = list(“kra”), as\_list = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0007.json#L1410) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L324) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L321)

## Record · Appraisal cycle

[Record definition](../../../../data/record-types/appraisal_cycle.json)

<a id="op-6fae56077772cc"></a>
### Appraisal Cycle.onload

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_onload`

**Inputs** self.

**Local steps**

- Evaluate self.set\_onload(“appraisals\_created”, self.check\_if\_appraisals\_exist()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if appraisals exist](operations-002.md#op-0ecdb337d6b155).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L559) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L330) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L327)

<a id="op-39f4d2e5670e24"></a>
### Appraisal Cycle.validate

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- Evaluate self.validate\_evaluation\_method\_change().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate evaluation method change](operations-002.md#op-a60f8606638ac3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L631) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L333) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L330)

<a id="op-a60f8606638ac3"></a>
### Appraisal Cycle.validate evaluation method change

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_validate_evaluation_method_change`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Evaluation Method cannot be changed as there are existing appraisals created for this cycle”.

**Local steps**

- If self.is\_new().
  - Return no value.
- If (self.has\_value\_changed(“kra\_evaluation\_method”) and self.check\_if\_appraisals\_exist()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“kra\_evaluation\_method”) → self.check\_if\_appraisals\_exist().
  - Call the validation error handler Platform.throw(translated “Evaluation Method cannot be changed as there are existing appraisals created for this cycle”, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if appraisals exist](operations-002.md#op-0ecdb337d6b155).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L720) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L334) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L331)

<a id="op-0ecdb337d6b155"></a>
### Appraisal Cycle.check if appraisals exist

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_check_if_appraisals_exist`

**Inputs** self.

**Record and data access** read “Appraisal” via exists.

**Explicit results** Platform.db.exists(“Appraisal”, mapping(“appraisal\_cycle” → self.name, “docstatus” → list(“!=”, 2))).

**Local steps**

- Return Platform.db.exists(“Appraisal”, mapping(“appraisal\_cycle” → self.name, “docstatus” → list(“!=”, 2))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L896) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L325) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L322)

<a id="op-93e21c4683b259"></a>
### Appraisal Cycle.set employees

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_set_employees`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “No employees found for the selected criteria”.

**Explicit results** self.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set employees from self.get\_employees\_for\_appraisal().
- Set appraisal\_templates from self.get\_appraisal\_template\_map().
- If employees.
  - Evaluate self.set(“appraisees”, list()).
  - Set template\_missing from false.
  - For each data in employees.
    - If not appraisal\_templates.get(data.designation).
      - Set template\_missing from true.
    - Evaluate self.append(“appraisees”, mapping(“employee” → data.name, “employee\_name” → data.employee\_name, “branch” → data.branch, “designation” → data.designation, …)).
  - If template\_missing.
    - Evaluate self.show\_missing\_template\_message().
- Otherwise.
  - Evaluate self.set(“appraisees”, list()).
  - Evaluate Platform.msgprint(translated “No employees found for the selected criteria”).
- Return self.

**Methods declared on this owner** [get employees for appraisal](operations-002.md#op-5c6f7e965fe15f), [get appraisal template map](operations-002.md#op-779a62fcd88ddd), [show missing template message](operations-002.md#op-8e27c6371e3e15).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L1011) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L331) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L328)

<a id="op-5c6f7e965fe15f"></a>
### Appraisal Cycle.get employees for appraisal

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_get_employees_for_appraisal`

**Inputs** self.

**Record and data access** read “Employee” via get\_all.

**Explicit results** employees.

**Local steps**

- Set filters from mapping(“status” → “Active”, “company” → self.company).
- If self.department.
  - Set filters at “department” from self.department.
- If self.branch.
  - Set filters at “branch” from self.branch.
- If self.designation.
  - Set filters at “designation” from self.designation.
- Set employees from Platform.db.get\_all(“Employee”, filters = filters, fields = list(“name”, “employee\_name”, “branch”, “designation”, …)).
- Return employees.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L1536) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L329) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L326)

<a id="op-779a62fcd88ddd"></a>
### Appraisal Cycle.get appraisal template map

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_get_appraisal_template_map`

**Inputs** self.

**Record and data access** read “Designation” via get\_all.

**Explicit results** appraisal\_templates.

**Local steps**

- Set designations from Platform.get\_all(“Designation”, fields = list(“name”, “appraisal\_template”)).
- Set appraisal\_templates from Platform.\_dict().
- For each entry in designations.
  - Set appraisal\_templates at entry.name from entry.appraisal\_template.
- Return appraisal\_templates.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L1856) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L328) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L325)

<a id="op-8d786797c58586"></a>
### Appraisal Cycle.create appraisals

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_create_appraisals`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with create\_appraisals\_for\_cycle · msgprint with translated “Appraisal creation is queued. It may take a few minutes.”.

**Explicit failure paths** validation helper — translated “Please select employees to create appraisals for”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- If not self.appraisees.
  - Call the validation error handler Platform.throw(translated “Please select employees to create appraisals for”, title = translated “No Employees Selected”).
- If not all(generator of appraisee.appraisal\_template for appraisee drawn from self.appraisees).
  - Draw appraisee from self.appraisees.
  - Evaluate self.show\_missing\_template\_message(raise\_exception = true).
- If len(self.appraisees) &gt; 30.
  - Evaluate Platform.enqueue(create\_appraisals\_for\_cycle, queue = “long”, timeout = 600, appraisal\_cycle = self).
  - Evaluate Platform.msgprint(translated “Appraisal creation is queued. It may take a few minutes.”, alert = true, indicator = “blue”).
- Otherwise.
  - Evaluate create\_appraisals\_for\_cycle(self, publish\_progress = true).
  - Evaluate self.reload().

If control reaches the end, it returns no value.

**Methods declared on this owner** [show missing template message](operations-002.md#op-8e27c6371e3e15).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue(create\_appraisals\_for\_cycle, queue = “long”, timeout = 600, appraisal\_cycle = self).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L2029) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L327) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L324)

<a id="op-8e27c6371e3e15"></a>
### Appraisal Cycle.show missing template message

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_show_missing_template_message`

**Inputs** self, raise\_exception = false.

**State and service calls** msgprint with msg.

**Local steps**

- Set msg from translated “Appraisal Template not found for some designations.”.
- Update msg using + text in the contract.
- Update msg using + translated “Please set the Appraisal Template for all the {0} or select the template in the Employees table below.”.format(formatted text &lt;a href='{Platform.utils.get\_url\_to\_list(“Designation”)}'&gt;Designations&lt;/a&gt;).
- Evaluate Platform.msgprint(msg, title = translated “Appraisal Template Missing”, indicator = “yellow”, raise\_exception = raise\_exception).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L2486) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L332) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L329)

<a id="op-20d33793c61ab4"></a>
### Appraisal Cycle.complete cycle

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_appraisal_cycle_complete_cycle`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Appraisal” via count.

**State and service calls** call save on self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set draft\_appraisals from Platform.db.count(“Appraisal”, mapping(“appraisal\_cycle” → self.name, “docstatus” → 0)).
- If draft\_appraisals.
  - Set link from (Platform.utils.get\_url\_to\_list(“Appraisal”) + formatted text ?status=Draft&amp;appraisal\_cycle={self.name}).
  - Set link from formatted text &lt;a href="{link}"&gt;documents&lt;/a&gt;.
  - Set msg from translated “{0} Appraisal(s) are not submitted yet”.format(Platform.bold(draft\_appraisals)).
  - Update msg using + text in the contract.
  - Update msg using + translated “Please submit the {0} before marking the cycle as Completed”.format(link).
  - Call the validation error handler Platform.throw(msg, title = translated “Unsubmitted Appraisals”).
- Set self.status from “Completed”.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L2725) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L326) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L323)

<a id="op-42d7c423d0b996"></a>
### Create appraisals for cycle

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_create_appraisals_for_cycle`

**Inputs** appraisal\_cycle, publish\_progress = false.

**Record and data access** resolve a document from mapping(“doctype” → “Appraisal”, “company” → appraisal\_cycle.company, “appraisal\_template” → employee.appraisal\_template, “employee” → employee.employee, …) via get\_doc.

**State and service calls** call insert on appraisal.

**Local steps**

- Set count from 0.
- For each employee in appraisal\_cycle.appraisees.
  - Attempt the following.
    - Set appraisal from Platform.get\_doc(mapping(“doctype” → “Appraisal”, “company” → appraisal\_cycle.company, “appraisal\_template” → employee.appraisal\_template, “employee” → employee.employee, …)).
    - Set appraisal.rate\_goals\_manually from 1 when appraisal\_cycle.kra\_evaluation\_method equals “Manual Rating”, otherwise 0.
      - Value choice on appraisal\_cycle.kra\_evaluation\_method equals “Manual Rating” — true gives 1, false gives 0.
    - Evaluate appraisal.set\_kras\_and\_rating\_criteria().
    - Evaluate appraisal.insert().
    - If publish\_progress.
      - Update count using + 1.
      - Evaluate Platform.publish\_progress(((count × 100) ÷ len(appraisal\_cycle.appraisees)), title = (translated “Creating Appraisals” + “...”)).
  - On failure (Platform.DuplicateEntryError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L3210) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L335) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L332)

<a id="op-482decb2ca8f9e"></a>
### Validate active appraisal cycle

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_validate_active_appraisal_cycle`

**Inputs** appraisal\_cycle.

**Declared result** no value.

**Record and data access** read “Appraisal Cycle” via get\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If Platform.db.get\_value(“Appraisal Cycle”, appraisal\_cycle, “status”) equals “Completed”.
  - Set msg from translated “Cannot create or change transactions against an Appraisal Cycle with status {0}.”.format(Platform.bold(translated “Completed”)).
  - Update msg using + text in the contract.
  - Update msg using + translated “Set the status to {0} if required.”.format(Platform.bold(translated “In Progress”)).
  - Call the validation error handler Platform.throw(msg, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L3646) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L339) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L336)

<a id="op-80ed5086cb7f28"></a>
### Get appraisal cycle summary

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_get_appraisal_cycle_summary`

**Inputs** cycle\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Appraisal” via count.

**Explicit results** summary.

**Local steps**

- Evaluate Platform.has\_permission(“Appraisal Cycle”, “read”, cycle\_name, throw = true).
- Set summary from Platform.\_dict().
- Set summary at “appraisees” from Platform.db.count(“Appraisal”, mapping(“appraisal\_cycle” → cycle\_name, “docstatus” → tuple(“!=”, 2))).
- Set summary at “self\_appraisal\_pending” from Platform.db.count(“Appraisal”, mapping(“appraisal\_cycle” → cycle\_name, “docstatus” → 0, “self\_score” → 0)).
- Set summary at “goals\_missing” from get\_employees\_without\_goals(cycle\_name).
- Set summary at “feedback\_missing” from get\_employees\_without\_feedback(cycle\_name).
- Return summary.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Appraisal Cycle”, “read”, cycle\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L3948) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L336) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L333)

<a id="op-5e3b554ff021ab"></a>
### Get employees without goals

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_get_employees_without_goals`

**Inputs** cycle\_name.

**Declared result** int.

**Explicit results** goals\_missing at 0.count.

**Local steps**

- Set Goal from Platform.qb.DocType(“Goal”).
- Set Appraisal from Platform.qb.DocType(“Appraisal”).
- Set count from Count(“\*”).as\_(“count”).
- Set filtered\_records from SubQuery(nested operand in the contract.select(nested operand in the contract.employee).distinct().where((Goal.appraisal\_cycle equals cycle\_name bitwise and Goal.status differs from “Archived”))).
- Set goals\_missing from nested operand in the contract(nested operand in the contract).select(count).where(((nested operand in the contract.appraisal\_cycle equals cycle\_name bitwise and nested operand in the contract.docstatus di ….
- Return goals\_missing at 0.count.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L4351) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L338) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L335)
