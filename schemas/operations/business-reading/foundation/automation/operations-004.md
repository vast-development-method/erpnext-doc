# Workflow, automation and dispatch · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Assignment rule

[Record definition](../../../../data/record-types/assignment_rule.json)

<a id="op-2a1c8f7fd3245a"></a>
### Assignment Rule.validate

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_document\_types().
- Evaluate self.validate\_assignment\_days().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate document types](operations-004.md#op-71c315a6e9edfa), [validate assignment days](operations-004.md#op-c4beed2d55cfb5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L856) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L159)

<a id="op-027719092464dc"></a>
### Assignment Rule.clear cache

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- Evaluate clear\_doctype\_map(self.doctype, self.document\_type).
- Evaluate clear\_doctype\_map(self.doctype, formatted text due\_date\_rules\_for\_{self.document\_type}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L927) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L148)

<a id="op-71c315a6e9edfa"></a>
### Assignment Rule.validate document types

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_validate_document_types`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Assignment Rule is not allowed on document type {0}”.format(Platform.bold(translated “ToDo”)).

**Local steps**

- If self.document\_type equals “ToDo”.
  - Call the validation error handler Platform.throw(translated “Assignment Rule is not allowed on document type {0}”.format(Platform.bold(translated “ToDo”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L1065) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L161)

<a id="op-c4beed2d55cfb5"></a>
### Assignment Rule.validate assignment days

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_validate_assignment_days`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The following Assignment Days have been repeated: {0}”.format(comma\_and(list of translated day for day drawn from get\_repeated(assignment\_days), add\_quotes = false)).

**Local steps**

- Set assignment\_days from self.get\_assignment\_days().
- If len(set(assignment\_days)) differs from len(assignment\_days).
  - Call the validation error handler Platform.throw(translated “The following Assignment Days have been repeated: {0}”.format(comma\_and(list of translated day for day drawn from get\_repeated(assignment\_days), add\_quotes = false))).
    - Draw day from get\_repeated(assignment\_days).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get assignment days](operations-004.md#op-2f93f28e836d1a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L1219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L160)

<a id="op-9fdf6f2cc826f9"></a>
### Assignment Rule.apply unassign

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_apply_unassign`

**Inputs** self, doc, assignments.

**Explicit results** self.clear\_assignment(doc) · false.

**Local steps**

- If (self.unassign\_condition and self.name belongs to list of d.assignment\_rule for d drawn from assignments).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.unassign\_condition → self.name belongs to list of d.assignment\_rule for d drawn from assignments.
  - Draw d from assignments.
  - Return self.clear\_assignment(doc).
- Return false.

**Methods declared on this owner** [clear assignment](operations-004.md#op-2873a2bca72d07).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L1459) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L146)

<a id="op-8c873d43288ec3"></a>
### Assignment Rule.apply assign

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_apply_assign`

**Inputs** self, doc.

**Explicit results** self.do\_assignment(doc).

**Local steps**

- If self.safe\_eval(“assign\_condition”, doc).
  - Return self.do\_assignment(doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [safe eval](operations-004.md#op-31b83e09fc4d82), [do assignment](operations-004.md#op-f5c9554f19d880).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L1600) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L145)

<a id="op-f5c9554f19d880"></a>
### Assignment Rule.do assignment

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_do_assignment`

**Inputs** self, doc.

**Record and data access** read “User” via exists.

**State and service calls** call db\_set on self.

**Explicit results** false · true.

**Local steps**

- Evaluate assign\_to.clear(doc.get(“doctype”), doc.get(“name”), ignore\_permissions = true).
- Set user from self.get\_user(doc).
- If (not user or not Platform.db.exists(“User”, user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not user → not Platform.db.exists(“User”, user).
  - Return false.
- Evaluate assign\_to.\_add(dict(assign\_to = list(user), doctype = doc.get(“doctype”), name = doc.get(“name”), description = Platform.render\_template(self.description, doc, restrict\_globals = true), …), ignore\_permissi ….
  - Value choice on self.due\_date\_based\_on — true gives doc.get(self.due\_date\_based\_on), false gives no value.
- Evaluate self.db\_set(“last\_user”, user).
- Return true.

**Methods declared on this owner** [get user](operations-004.md#op-595c0d501429c6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L1700) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L150)

<a id="op-2873a2bca72d07"></a>
### Assignment Rule.clear assignment

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_clear_assignment`

**Inputs** self, doc.

**Explicit results** assign\_to.clear(doc.get(“doctype”), doc.get(“name”), ignore\_permissions = true).

**Local steps**

- If self.safe\_eval(“unassign\_condition”, doc).
  - Return assign\_to.clear(doc.get(“doctype”), doc.get(“name”), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [safe eval](operations-004.md#op-31b83e09fc4d82).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L2182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L147)

<a id="op-7f2f0f6337a1ba"></a>
### Assignment Rule.close assignments

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_close_assignments`

**Inputs** self, doc.

**Explicit results** assign\_to.close\_all\_assignments(doc.get(“doctype”), doc.get(“name”), ignore\_permissions = true).

**Local steps**

- If self.safe\_eval(“close\_condition”, doc).
  - Return assign\_to.close\_all\_assignments(doc.get(“doctype”), doc.get(“name”), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [safe eval](operations-004.md#op-31b83e09fc4d82).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L2339) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L149)

<a id="op-595c0d501429c6"></a>
### Assignment Rule.get user

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_get_user`

**Inputs** self, doc.

**Explicit results** self.get\_user\_round\_robin() · self.get\_user\_load\_balancing() · self.get\_user\_based\_on\_field(doc) · self.get\_weighted\_user().

**Local steps**

- If self.rule equals “Round Robin”.
  - Return self.get\_user\_round\_robin().
- Otherwise.
  - If self.rule equals “Load Balancing”.
    - Return self.get\_user\_load\_balancing().
  - Otherwise.
    - If self.rule equals “Based on Field”.
      - Return self.get\_user\_based\_on\_field(doc).
    - Otherwise.
      - If self.rule equals “Weighted Distribution”.
        - Return self.get\_weighted\_user().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get user round robin](operations-004.md#op-2ac35ab1a7e1b9), [get user load balancing](operations-004.md#op-6c558bb0b2d7dc), [get user based on field](operations-004.md#op-db14c2e0cd5c89), [get weighted user](operations-004.md#op-2ea75038383da4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L2496) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L152)

<a id="op-2ac35ab1a7e1b9"></a>
### Assignment Rule.get user round robin

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_get_user_round_robin`

**Inputs** self.

**Record and data access** read “Assignment Rule” via get\_value.

**Explicit results** self.users at 0.user · self.users at (i + 1).user.

**Local steps**

- Set last\_user from Platform.db.get\_value(“Assignment Rule”, self.name, “last\_user”, for\_update = true).
- If (not last\_user or last\_user equals self.users at negative 1.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not last\_user → last\_user equals self.users at negative 1.user.
  - Return self.users at 0.user.
- For each tuple(i, d) in enumerate(self.users).
  - If last\_user equals d.user.
    - Return self.users at (i + 1).user.
- Return self.users at 0.user.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L155)

<a id="op-6c558bb0b2d7dc"></a>
### Assignment Rule.get user load balancing

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_get_user_load_balancing`

**Inputs** self.

**Record and data access** read “ToDo” via count.

**Explicit results** sorted\_counts at 0.get(“user”).

**Local steps**

- Set counts from list of dict(user = d.user, count = Platform.db.count(“ToDo”, dict(reference\_type = self.document\_type, allocated\_to = d.user, status = “Open”))) for d drawn from self.users.
  - Draw d from self.users.
- Set sorted\_counts from sorted(counts, key = deferred anonymous expression).
- Return sorted\_counts at 0.get(“user”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L2964) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L154)

<a id="op-db14c2e0cd5c89"></a>
### Assignment Rule.get user based on field

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_get_user_based_on_field`

**Inputs** self, doc.

**Record and data access** read “User” via exists.

**Explicit results** val.

**Local steps**

- Set val from doc.get(self.field).
- If Platform.db.exists(“User”, val).
  - Return val.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L3225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L153)

<a id="op-2ea75038383da4"></a>
### Assignment Rule.get weighted user

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_get_weighted_user`

**Inputs** self.

**Record and data access** read “Assignment Rule” via get\_value.

**State and service calls** request set\_value on “Assignment Rule”.

**Explicit results** no value · user.

**Local steps**

- Set users from list of tuple(d.user, (d.weight or 1)) for d drawn from self.weighted\_users where d.user.
  - Draw d from self.weighted\_users, keep a combination only if (d.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.weight → 1.
- If not users.
  - Return no value.
- Set total\_weight from sum(generator of weight for tuple(\_, weight) drawn from users).
  - Draw tuple(\_, weight) from users.
- If total\_weight ≤ 0.
  - Return no value.
- Set current\_index from (Platform.db.get\_value(“Assignment Rule”, self.name, “current\_index”, for\_update = true) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Assignment Rule”, self.name, “current\_index”, for\_update = true) → 0.
- Set slot from (current\_index modulo or format total\_weight).
- Set cumulative\_weight from 0.
- For each tuple(user, weight) in users.
  - Update cumulative\_weight using + weight.
  - If slot &lt; cumulative\_weight.
    - Evaluate Platform.db.set\_value(“Assignment Rule”, self.name, “current\_index”, (current\_index + 1), update\_modified = false).
    - Return user.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L3342) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L156)

<a id="op-31b83e09fc4d82"></a>
### Assignment Rule.safe eval

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_safe_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, fieldname, doc.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L3793) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L158)

<a id="op-2f93f28e836d1a"></a>
### Assignment Rule.get assignment days

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_get_assignment_days`

**Inputs** self.

**Explicit results** list of d.day for d drawn from self.get(“assignment\_days”, list()).

**Local steps**

- Return list of d.day for d drawn from self.get(“assignment\_days”, list()).
  - Draw d from self.get(“assignment\_days”, list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L4019) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L151)

<a id="op-b616f7dfb7f77f"></a>
### Assignment Rule.is rule not applicable today

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_assignment_rule_is_rule_not_applicable_today`

**Inputs** self.

**Explicit results** (assignment\_days and today does not belong to assignment\_days).

**Local steps**

- Set today from (Platform.flags.assignment\_day or Platform.utils.get\_weekday()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.assignment\_day → Platform.utils.get\_weekday().
- Set assignment\_days from self.get\_assignment\_days().
- Return (assignment\_days and today does not belong to assignment\_days).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in assignment\_days → today does not belong to assignment\_days.

**Methods declared on this owner** [get assignment days](operations-004.md#op-2f93f28e836d1a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L4104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L157)

<a id="op-80c8bfc4d93f20"></a>
### Get assignments

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_get_assignments`

**Inputs** doc.

**Declared result** list at dict.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** Platform.get\_all(“ToDo”, fields = list(“name”, “assignment\_rule”), filters = dict(reference\_type = doc.get(“doctype”), reference\_name = str(doc.get(“name”)), status = tuple(“!=”, “Cancelled”)), limit = 5).

**Local steps**

- Return Platform.get\_all(“ToDo”, fields = list(“name”, “assignment\_rule”), filters = dict(reference\_type = doc.get(“doctype”), reference\_name = str(doc.get(“name”)), status = tuple(“!=”, “Cancelled”)), limit = 5).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L4238) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L164)

<a id="op-07a577768c4e3e"></a>
### Bulk apply

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_bulk_apply`

**Inputs** doctype, docnames.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**State and service calls** enqueue with “Platform.automation.doctype.assignment\_rule.assignment\_rule.apply”.

**Explicit results** background.

**Local steps**

- Set docnames from Platform.parse\_json(docnames).
- Set background from len(docnames) &gt; 5.
- For each name in docnames.
  - If background.
    - Evaluate Platform.enqueue(“Platform.automation.doctype.assignment\_rule.assignment\_rule.apply”, doc = no value, doctype = doctype, name = name).
  - Otherwise.
    - Evaluate apply(doctype = doctype, name = name).
- Return background.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.automation.doctype.assignment\_rule.assignment\_rule.apply”, doc = no value, doctype = doctype, name = name).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L162)

<a id="op-4db00245a50090"></a>
### Reopen closed assignment

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_reopen_closed_assignment`

**Inputs** doc.

**Record and data access** read “ToDo” via get\_all · resolve a document from “ToDo” via get\_doc.

**State and service calls** call save on todo\_doc.

**Explicit results** bool(todo\_list).

**Local steps**

- Set todo\_list from Platform.get\_all(“ToDo”, filters = mapping(“reference\_type” → doc.doctype, “reference\_name” → str(doc.name), “status” → “Closed”), pluck = “name”).
- For each todo in todo\_list.
  - Set todo\_doc from Platform.get\_doc(“ToDo”, todo).
  - Set todo\_doc.status from “Open”.
  - Evaluate todo\_doc.save(ignore\_permissions = true).
- Return bool(todo\_list).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L4886) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L166)

<a id="op-c567c9547c7dc2"></a>
### Apply

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_apply`

**Inputs** doc = no value, method = no value, doctype = no value, name = no value.

**Record and data access** resolve a document from doctype via get\_doc · resolve a document from “Assignment Rule” via get\_cached\_doc · read “ToDo” via get\_all · resolve a document from “ToDo” via get\_doc.

**State and service calls** call save on \_todo.

**Explicit results** no value.

**Local steps**

- Set doctype from (doctype or doc.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → doc.doctype.
- Set skip\_assignment\_rules from (Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_setup\_wizard or doctype belongs to log\_types).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_patch → Platform.flags.in\_install → Platform.flags.in\_setup\_wizard → doctype belongs to log\_types.
- If skip\_assignment\_rules.
  - Return no value.
- If (not doc and doctype and name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc → doctype → name.
  - Set doc from Platform.get\_doc(doctype, name).
  - Evaluate doc.check\_permission().
- Set assignment\_rules from get\_doctype\_map(“Assignment Rule”, doc.doctype, filters = mapping(“document\_type” → doc.doctype, “disabled” → 0), order\_by = “priority desc”).
- Set assignment\_rule\_docs from list of Platform.get\_cached\_doc(“Assignment Rule”, d.get(“name”)) for d drawn from assignment\_rules.
  - Draw d from assignment\_rules.
- If not assignment\_rule\_docs.
  - Return no value.
- Set doc from doc.as\_dict().
- Set assignments from get\_assignments(doc).
- Set clear from true.
- Set new\_apply from false.
- If assignments.
  - Set clear from false.
  - For each assignment\_rule in assignment\_rule\_docs.
    - If assignment\_rule.is\_rule\_not\_applicable\_today().
      - Continue with the next iteration or loop test.
    - Set clear from assignment\_rule.apply\_unassign(doc, assignments).
    - If clear.
      - Leave the innermost loop without its normal-exhaustion alternative.
- If clear.
  - For each assignment\_rule in assignment\_rule\_docs.
    - If assignment\_rule.is\_rule\_not\_applicable\_today().
      - Continue with the next iteration or loop test.
    - Set new\_apply from assignment\_rule.apply\_assign(doc).
    - If new\_apply.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set assignments from get\_assignments(doc).
- If assignments.
  - Set closed\_assignments\_checked from false.
  - For each assignment\_rule in assignment\_rule\_docs.
    - If assignment\_rule.is\_rule\_not\_applicable\_today().
      - Continue with the next iteration or loop test.
    - If not new\_apply.
      - Set to\_close\_todos from assignment\_rule.safe\_eval(“close\_condition”, doc).
      - If to\_close\_todos.
        - Set todos\_to\_close from Platform.get\_all(“ToDo”, filters = mapping(“reference\_type” → doc.doctype, “reference\_name” → str(doc.name)), pluck = “name”).
        - For each todo in todos\_to\_close.
          - Set \_todo from Platform.get\_doc(“ToDo”, todo).
          - Set \_todo.status from “Closed”.
          - Evaluate \_todo.save(ignore\_permissions = true).
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Otherwise.
        - If not closed\_assignments\_checked.
          - Set closed\_assignments\_checked from true.
          - Set reopened from reopen\_closed\_assignment(doc).
          - If reopened.
            - Leave the innermost loop without its normal-exhaustion alternative.
    - Evaluate assignment\_rule.close\_assignments(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission() · configured or stored value from Platform.get\_cached\_doc(“Assignment Rule”, d.get(“name”)).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L144)

<a id="op-f48c3dccfcf6f7"></a>
### Update due date

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_update_due_date`

**Inputs** doc, state = no value.

**Record and data access** resolve a document from “Assignment Rule” via get\_cached\_doc · read “ToDo” via get\_all · resolve a document from “ToDo” via get\_doc.

**State and service calls** call save on todo\_doc.

**Explicit results** no value.

**Local steps**

- Set skip\_document\_update from (Platform.flags.in\_migrate or Platform.flags.in\_patch or Platform.flags.in\_import or Platform.flags.in\_setup\_wizard or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_patch → Platform.flags.in\_import → Platform.flags.in\_setup\_wizard → Platform.flags.in\_install.
- If skip\_document\_update.
  - Return no value.
- Set assignment\_rules from get\_doctype\_map(doctype = “Assignment Rule”, name = formatted text due\_date\_rules\_for\_{doc.doctype}, filters = mapping(“due\_date\_based\_on” → list(“is”, “set”), “document\_type” → doc.doctype, “disabled” → 0)).
- For each rule in assignment\_rules.
  - Set rule\_doc from Platform.get\_cached\_doc(“Assignment Rule”, rule.get(“name”)).
  - Set due\_date\_field from rule\_doc.due\_date\_based\_on.
  - Set field\_updated from (doc.meta.has\_field(due\_date\_field) and doc.has\_value\_changed(due\_date\_field) and rule.get(“name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.has\_field(due\_date\_field) → doc.has\_value\_changed(due\_date\_field) → rule.get(“name”).
  - If field\_updated.
    - Set assignment\_todos from Platform.get\_all(“ToDo”, filters = mapping(“assignment\_rule” → rule.get(“name”), “reference\_type” → doc.doctype, “reference\_name” → str(doc.name), “status” → “Open”), pluck = “name”).
    - For each todo in assignment\_todos.
      - Set todo\_doc from Platform.get\_doc(“ToDo”, todo).
      - Set todo\_doc.date from doc.get(due\_date\_field).
      - Set todo\_doc.flags.updater\_reference from mapping(“doctype” → “Assignment Rule”, “docname” → rule.get(“name”), “label” → translated “via Assignment Rule”).
      - Evaluate todo\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Assignment Rule”, rule.get(“name”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L6305) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L167)

<a id="op-f382d0f6bf0b06"></a>
### Get assignment rules

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_get_assignment_rules`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Assignment Rule” via get\_all.

**Explicit results** Platform.get\_all(“Assignment Rule”, filters = mapping(“disabled” → 0), pluck = “document\_type”).

**Local steps**

- Return Platform.get\_all(“Assignment Rule”, filters = mapping(“disabled” → 0), pluck = “document\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L7152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L163)

<a id="op-9bfbb1f4fee578"></a>
### Get repeated

`operation_foundation_automation_record_definitions_assignment_rule_business_behavior_get_repeated`

**Inputs** values.

**Declared result** list.

**Explicit results** list of str(x) for x drawn from repeated.

**Local steps**

- Set unique from set().
- Set repeated from set().
- For each value in values.
  - If value belongs to unique.
    - Evaluate repeated.add(value).
  - Otherwise.
    - Evaluate unique.add(value).
- Return list of str(x) for x drawn from repeated.
  - Draw x from repeated.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0012.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L165)
