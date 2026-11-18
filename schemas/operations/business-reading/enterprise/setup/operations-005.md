# Company and master data · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Department

[Record definition](../../../../data/record-types/department.json)

<a id="op-812f3c418b5556"></a>
### Add node

`operation_enterprise_setup_record_definitions_department_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from Platform.form\_dict.
- Set args from make\_tree\_args(expanded names args).
- Set args.doctype from “Department”.
- If args.parent\_department equals args.company.
  - Set args.parent\_department from no value.
- Evaluate Platform.get\_doc(args).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L792) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L350)

## Record · Driver

[Record definition](../../../../data/record-types/driver.json)

<a id="op-42dcfcdb423578"></a>
### Driver.validate

`operation_enterprise_setup_record_definitions_driver_business_behavior_driver_validate`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “The licence expiry date cannot precede its issuing date.”.

**Local steps**

- If (self.issuing\_date and self.expiry\_date and getdate(self.expiry\_date) &lt; getdate(self.issuing\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.issuing\_date → self.expiry\_date → getdate(self.expiry\_date) &lt; getdate(self.issuing\_date).
  - Call the validation error handler Platform.throw(translated “The licence expiry date cannot precede its issuing date.”).
- Set employee\_user from Platform.get\_value(“Employee”, self.employee, “user\_id”) when self.employee, otherwise no value.
  - Value choice on self.employee — true gives Platform.get\_value(“Employee”, self.employee, “user\_id”), false gives no value.
- If employee\_user.
  - Set self.user from employee\_user.
- Otherwise.
  - If (previous bound to self.get\_doc\_before\_save() and previous.employee and self.has\_value\_changed(“employee”) and not self.has\_value\_changed(“user”) and self.user equals Platform.get\_value(“Employee”, previou ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous bound to self.get\_doc\_before\_save() → previous.employee → self.has\_value\_changed(“employee”) → not self.has\_value\_changed(“user”) → self.user equals Platform.get\_value(“Employee”, previous.employee, “user\_id”).
    - Set self.user from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L362)

## Record · Email digest

[Record definition](../../../../data/record-types/email_digest.json)

<a id="op-972d0f5becc06e"></a>
### Email Digest.initialize

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set tuple(self.from\_date, self.to\_date) from self.get\_from\_to\_date().
- Evaluate self.set\_dates().
- Set self.\_accounts from mapping().
- Set self.currency from Platform.db.get\_value(“Company”, self.company, “default\_currency”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get from to date](operations-007.md#op-24a181f2c2de29), [set dates](operations-007.md#op-5620d8ab54702b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L3860) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L848) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L405)

<a id="op-5b975510968bc2"></a>
### Email Digest.validate

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Recipient {1} must be an enabled System User.”.format(row.idx, row.recipient).

**Local steps**

- Set valid\_users from self.get\_eligible\_recipients().
- For each row in self.recipients.
  - If row.recipient does not belong to valid\_users.
    - Call the validation error handler Platform.throw(translated “Row {0}: Recipient {1} must be an enabled System User.”.format(row.idx, row.recipient)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get eligible recipients](operations-005.md#op-676dae137aee67).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L151)

<a id="op-676dae137aee67"></a>
### Email Digest.get eligible recipients

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_get_eligible_recipients`

**Inputs** self.

**Record and data access** read “User” via get\_all.

**Explicit results** set() · set(Platform.get\_all(“User”, filters = mapping(“name” → list(“in”, recipients), “enabled” → 1, “user\_type” → “System User”), pluck = “name”)).

**Local steps**

- Set recipients from list of row.recipient for row drawn from self.recipients where row.recipient.
  - Draw row from self.recipients, keep a combination only if (row.recipient).
- If not recipients.
  - Return set().
- Return set(Platform.get\_all(“User”, filters = mapping(“name” → list(“in”, recipients), “enabled” → 1, “user\_type” → “System User”), pluck = “name”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L146)

<a id="op-993b424ed8720e"></a>
### Email Digest.send

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_send`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Local steps**

- Evaluate self.\_send().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-005.md#op-9b51034f93c6b7).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L407)

<a id="op-9b51034f93c6b7"></a>
### Email Digest.send

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_send`

**Inputs** self, continue\_on\_error = false.

**State and service calls** savepoint “email\_digest\_recipient” · rollback.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set valid\_users from self.get\_eligible\_recipients().
- For each row in self.recipients.
  - If row.recipient does not belong to valid\_users.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.db.savepoint(“email\_digest\_recipient”).
  - Attempt the following.
    - Evaluate self.send\_to\_recipient(row.recipient).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = “email\_digest\_recipient”).
    - If not continue\_on\_error.
      - Propagate the active failure.
    - Evaluate Platform.log\_error(title = formatted text Email Digest {self.name} failed for {row.recipient}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get eligible recipients](operations-005.md#op-676dae137aee67), [send to recipient](operations-005.md#op-5cc61c21b2f3ba).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L148)

<a id="op-5cc61c21b2f3ba"></a>
### Email Digest.send to recipient

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_send_to_recipient`

**Inputs** self, recipient.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Set original\_session from Platform.\_dict(Platform.session).
- Set original\_form from Platform.local.form\_dict.
- Attempt the following.
  - Evaluate Platform.set\_user(recipient).
  - If not self.can\_receive\_financial\_cards().
    - Return no value.
  - Set message from self.get\_msg\_html().
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(original\_session.user).
  - Evaluate Platform.local.session.update(original\_session).
  - Set Platform.local.form\_dict from original\_form.
- If message.
  - Evaluate Platform.sendmail(recipients = recipient, subject = translated “{0} Digest”.format(translated self.frequency), message = message, reference\_doctype = self.doctype, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can receive financial cards](operations-005.md#op-b32f9b5f73d801), [get msg html](operations-005.md#op-cfe278ac9f231d).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipient, subject = translated “{0} Digest”.format(translated self.frequency), message = message, reference\_doctype = self.doctype, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L149)

<a id="op-b32f9b5f73d801"></a>
### Email Digest.can receive financial cards

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_can_receive_financial_cards`

**Inputs** self.

**Record and data access** read doctype via get\_list · read doctype via count.

**Explicit results** true · false.

**Local steps**

- Set sections from mapping(“Account” → tuple(“income”, “expenses\_booked”, “income\_year\_to\_date”, “expense\_year\_to\_date”, …), “GL Entry” → tuple(“income”, “expenses\_booked”, “income\_year\_to\_date”, “expense\_year\_to\_date”, …),  ….
- Set doctypes from list of doctype for tuple(doctype, fields) drawn from sections.items() where any(generator of self.get(field) for field drawn from fields).
  - Draw tuple(doctype, fields) from sections.items(), keep a combination only if (any(generator of self.get(field) for field drawn from fields)).
  - Draw field from fields.
- If not doctypes.
  - Return true.
- If not Platform.has\_permission(“Company”, “read”, doc = self.company).
  - Return false.
- For each doctype in doctypes.
  - If not Platform.has\_permission(doctype, “read”).
    - Return false.
  - Set filters from mapping(“company” → self.company).
  - Set visible from Platform.get\_list(doctype, filters = filters, fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.
  - If visible differs from Platform.db.count(doctype, filters).
    - Return false.
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, doc = self.company), Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L145)

<a id="op-cfe278ac9f231d"></a>
### Email Digest.get msg html

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_message_document_markup`

**Inputs** self.

**Explicit results** self.\_get\_msg\_html().

**Local steps**

- Set previous from Platform.flags.get(“ignore\_account\_permission”).
- Attempt the following.
  - Return self.\_get\_msg\_html().
- On exit, including pending return or failure.
  - Set Platform.flags.ignore\_account\_permission from previous.

**Methods declared on this owner** [get msg html](operations-005.md#op-f91cc9afd01630).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L375)

<a id="op-f91cc9afd01630"></a>
### Email Digest.get msg html

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_get_msg_html`

**Inputs** self.

**Explicit results** no value · Platform.render\_template(“Enterprise/setup/doctype/email\_digest/templates/default.html”, context, is\_path = true).

**Local steps**

- Bind dependencies get\_random\_quote.
- Set context from Platform.\_dict().
- Evaluate context.update(self.\_\_dict\_\_).
- Evaluate self.set\_title(context).
- Evaluate self.set\_style(context).
- Evaluate self.set\_accounting\_cards(context).
- If self.get(“calendar\_events”).
  - Set tuple(context.events, context.event\_count) from self.get\_calendar\_events().
- If self.get(“todo\_list”).
  - Set context.todo\_list from self.get\_todo\_list().
  - Set context.todo\_count from self.get\_todo\_count().
- If self.get(“notifications”).
  - Set context.notifications from self.get\_notifications().
- If self.get(“issue”).
  - Set context.issue\_list from self.get\_issue\_list().
  - Set context.issue\_count from self.get\_issue\_count().
- If self.get(“project”).
  - Set context.project\_list from self.get\_project\_list().
  - Set context.project\_count from self.get\_project\_count().
- Set quote from get\_random\_quote().
- Set context.quote from mapping(“text” → quote at 0, “author” → quote at 1).
- If self.get(“purchase\_orders\_items\_overdue”).
  - Set context.purchase\_orders\_items\_overdue\_map from self.get\_purchase\_orders\_items\_overdue\_list().
- If not context.
  - Return no value.
- Return Platform.render\_template(“Enterprise/setup/doctype/email\_digest/templates/default.html”, context, is\_path = true).

**Methods declared on this owner** [set title](operations-005.md#op-c52111f1e5d832), [set style](operations-005.md#op-c34aaa103e6b8c), [set accounting cards](operations-005.md#op-eb3ff6ad85cbf2), [get calendar events](operations-005.md#op-4f7bf31de3e706), [get todo list](operations-005.md#op-68cc601e3358ae), [get todo count](operations-005.md#op-f20cb6769bc033), [get notifications](operations-005.md#op-c9694faaabe7a7), [get issue list](operations-005.md#op-b5db160613cc33), [get issue count](operations-005.md#op-e4c43cd5f72cdc), [get project list](operations-005.md#op-aee214c01a0ef6), [get project count](operations-005.md#op-a96ebc3367fa7e), [get purchase orders items overdue list](operations-007.md#op-d3be6b5d6e23d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L147)

<a id="op-c52111f1e5d832"></a>
### Email Digest.set title

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_set_title`

**Inputs** self, context.

**Local steps**

- If self.frequency equals “Daily”.
  - Set context.title from translated “Daily Reminders”.
  - Set context.subtitle from translated “Pending activities for today”.
- Otherwise.
  - If self.frequency equals “Weekly”.
    - Set context.title from translated “This Week's Summary”.
    - Set context.subtitle from translated “Summary for this week and pending activities”.
  - Otherwise.
    - If self.frequency equals “Monthly”.
      - Set context.title from translated “This Month's Summary”.
      - Set context.subtitle from translated “Summary for this month and pending activities”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L5601) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L411)

<a id="op-c34aaa103e6b8c"></a>
### Email Digest.set style

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_set_style`

**Inputs** self, context.

**Local steps**

- Set context.text\_muted from “#8D99A6”.
- Set context.text\_color from “#36414C”.
- Set context.h1 from “margin-bottom: 30px; margin-top: 40px; font-weight: 400; font-size: 30px;”.
- Set context.h2 from “margin-bottom: 30px; margin-top: -20px; font-weight: 400; font-size: 20px;”.
- Set context.label\_css from formatted text display: inline-block; color: {context.text\_muted};  padding: 3px 7px; margin-right: 7px;.
- Set context.section\_head from “margin-top: 60px; font-size: 16px;”.
- Set context.line\_item from “padding: 5px 0px; margin: 0; border-bottom: 1px solid #d1d8dd;”.
- Set context.link\_css from formatted text color: {context.text\_color}; text-decoration: none;.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L5900) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L410)

<a id="op-c9694faaabe7a7"></a>
### Email Digest.get notifications

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_notifications`

**Inputs** self.

**Explicit results** notifications.

**Local steps**

- Set notifications from Platform.desk.notifications.get\_notifications().
- Set notifications from sorted(notifications.get(“open\_count\_doctype”, mapping()).items(), key = deferred anonymous expression).
- Set notifications from list of mapping(“key” → n at 0, “value” → n at 1, “link” → get\_url\_to\_list(n at 0)) for n drawn from notifications where n at 1.
  - Draw n from notifications, keep a combination only if (n at 1).
- Return notifications.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L6121) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L378)

<a id="op-4f7bf31de3e706"></a>
### Email Digest.get calendar events

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_calendar_events`

**Inputs** self.

**Explicit results** tuple(events, event\_count).

**Local steps**

- Bind dependencies get\_events.
- Set tuple(from\_date, to\_date) from get\_future\_date\_for\_calendaer\_event(self.frequency).
- Set events from get\_events(from\_date, to\_date).
- Set event\_count from 0.
- For each tuple(\_i, e) in enumerate(events).
  - Set e.starts\_on\_label from format\_time(e.starts\_on).
  - Set e.ends\_on\_label from format\_time(e.ends\_on) when e.ends\_on, otherwise no value.
    - Value choice on e.ends\_on — true gives format\_time(e.ends\_on), false gives no value.
  - Set e.date from formatdate(e.starts).
  - Set e.link from get\_url\_to\_form(“Event”, e.name).
  - Update event\_count using + 1.
- Return tuple(events, event\_count).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L6404) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L365)

<a id="op-68cc601e3358ae"></a>
### Email Digest.get todo list

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_todo_list`

**Inputs** self, user\_id = no value.

**Record and data access** execute query text (SELECT, To Do).

**Explicit results** todo\_list.

**Local steps**

- If not user\_id.
  - Set user\_id from Platform.session.user.
- Set todo\_list from Platform.db.sql(query text (SELECT, To Do), tuple(user\_id, user\_id), as\_dict = true).
- For each t in todo\_list.
  - Set t.link from get\_url\_to\_form(“ToDo”, t.name).
- Return todo\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L843) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L401)

<a id="op-f20cb6769bc033"></a>
### Email Digest.get todo count

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_todo_count`

**Inputs** self, user\_id = no value.

**Record and data access** execute query text (SELECT, To Do).

**Explicit results** Platform.db.sql(query text (SELECT, To Do), tuple(user\_id, user\_id)) at 0 at 0.

**Local steps**

- If not user\_id.
  - Set user\_id from Platform.session.user.
- Return Platform.db.sql(query text (SELECT, To Do), tuple(user\_id, user\_id)) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L842) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L400)

<a id="op-b5db160613cc33"></a>
### Email Digest.get issue list

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_issue_list`

**Inputs** self, user\_id = no value.

**Record and data access** read “Issue” via get\_list.

**Explicit results** no value · issue\_list.

**Local steps**

- If not user\_id.
  - Set user\_id from Platform.session.user.
- If not Platform.has\_permission(“Issue”, “read”, user = user\_id).
  - Return no value.
- Set issue\_list from Platform.get\_list(“Issue”, user = user\_id, filters = mapping(“status” → list(“in”, list(“Replied”, “Open”))), fields = list(“\*”), order\_by = “creation asc”, …).
- For each t in issue\_list.
  - Set t.link from get\_url\_to\_form(“Issue”, t.name).
- Return issue\_list.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Issue”, “read”, user = user\_id).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L374)

<a id="op-e4c43cd5f72cdc"></a>
### Email Digest.get issue count

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_issue_count`

**Inputs** self.

**Record and data access** read “Issue” via get\_list.

**Explicit results** 0 · Platform.get\_list(“Issue”, filters = mapping(“status” → list(“in”, list(“Open”, “Replied”))), fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.

**Local steps**

- If not Platform.has\_permission(“Issue”, “read”).
  - Return 0.
- Return Platform.get\_list(“Issue”, filters = mapping(“status” → list(“in”, list(“Open”, “Replied”))), fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Issue”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L373)

<a id="op-aee214c01a0ef6"></a>
### Email Digest.get project list

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_project_list`

**Inputs** self, user\_id = no value.

**Record and data access** read “Project” via get\_list.

**Explicit results** list() · project\_list.

**Local steps**

- If not user\_id.
  - Set user\_id from Platform.session.user.
- If not Platform.has\_permission(“Project”, “read”, user = user\_id).
  - Return list().
- Set project\_list from Platform.get\_list(“Project”, user = user\_id, filters = mapping(“status” → “Open”, “project\_type” → “External”), fields = list(“\*”), order\_by = “creation asc”, …).
- For each t in project\_list.
  - Set t.link from get\_url\_to\_form(“Project”, t.name).
- Return project\_list.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Project”, “read”, user = user\_id).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L827) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L385)

<a id="op-a96ebc3367fa7e"></a>
### Email Digest.get project count

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_project_count`

**Inputs** self.

**Record and data access** read “Project” via get\_list.

**Explicit results** 0 · Platform.get\_list(“Project”, filters = mapping(“status” → “Open”, “project\_type” → “External”), fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.

**Local steps**

- If not Platform.has\_permission(“Project”, “read”).
  - Return 0.
- Return Platform.get\_list(“Project”, filters = mapping(“status” → “Open”, “project\_type” → “External”), fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Project”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L826) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L384)

<a id="op-eb3ff6ad85cbf2"></a>
### Email Digest.set accounting cards

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_set_accounting_cards`

**Inputs** self, context.

**Local steps**

- Set previous from Platform.flags.get(“ignore\_account\_permission”).
- Set Platform.flags.ignore\_account\_permission from true.
- Attempt the following.
  - Evaluate self.\_set\_accounting\_cards(context).
- On exit, including pending return or failure.
  - Set Platform.flags.ignore\_account\_permission from previous.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set accounting cards](operations-005.md#op-f80ce0a0b1501e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L408)

<a id="op-f80ce0a0b1501e"></a>
### Email Digest.set accounting cards

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_emaildigest_set_accounting_cards`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, context.

**Observed service boundaries** record mutation request.

**Local structure** 11 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L150)

<a id="op-4963cc01e4ef0e"></a>
### Email Digest.get income

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_income`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Explicit results** mapping(“label” → label, “value” → income, “last\_value” → past\_income, “count” → count).

**Local steps**

- Set tuple(income, past\_income, count) from self.get\_period\_amounts(self.get\_roots(“income”), “income”).
- Set income\_account from Platform.db.get\_all(“Account”, fields = list(“name”), filters = mapping(“root\_type” → “Income”, “parent\_account” → empty text, “company” → self.company)).
- Set label from get\_link\_to\_report(“General Ledger”, translated self.meta.get\_label(“income”), filters = mapping(“from\_date” → self.future\_from\_date, “to\_date” → self.future\_to\_date, “account” → income\_account at 0.name,  ….
- Return mapping(“label” → label, “value” → income, “last\_value” → past\_income, “count” → count).

**Methods declared on this owner** [get period amounts](operations-006.md#op-764ba5967d03a1), [get roots](operations-006.md#op-da3be14bab2e42).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L370)
