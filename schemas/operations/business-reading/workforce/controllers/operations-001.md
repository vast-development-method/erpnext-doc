# Shared transaction rules · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Employee boarding controller

<a id="op-16043bf74ad805"></a>
### Employee Boarding Controller.validate

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_validate`

**Inputs** self.

**Local steps**

- If self.amended\_from.
  - For each activity in self.activities.
    - Set activity.task from empty text.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L1329) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L266) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L266)

<a id="op-0b652c754d6e7b"></a>
### Employee Boarding Controller.on submit

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_on_submit`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Project”, “project\_name” → project\_name, “expected\_start\_date” → self.date\_of\_joining when self.doctype equals “Employee Onboarding”, otherwise self.resignation\_letter\_date, “departmen … via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Project”, “project\_name” → project\_name, “expected\_start\_date” → self.date\_of\_joining when self.doctype equals “Employee Onboarding”, otherwise self.resignation\_letter … · call db\_set on self.

**Local steps**

- Set project\_name from (translated self.doctype + “ : ”).
- If self.doctype equals “Employee Onboarding”.
  - Update project\_name using + (self.job\_applicant or self.employee\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.job\_applicant → self.employee\_name.
- Otherwise.
  - Update project\_name using + self.employee.
- Set project from Platform.get\_doc(mapping(“doctype” → “Project”, “project\_name” → project\_name, “expected\_start\_date” → self.date\_of\_joining when nested operand in the contract.doctype equals “Employee Onboarding”, otherwi ….
  - Value choice on self.doctype equals “Employee Onboarding” — true gives self.date\_of\_joining, false gives self.resignation\_letter\_date.
- Evaluate self.db\_set(“project”, project.name).
- Evaluate self.db\_set(“boarding\_status”, “Pending”).
- Evaluate self.reload().
- Evaluate self.create\_task\_and\_notify\_user().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create task and notify user](operations-001.md#op-f4a692ce12b7ba).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L1409) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L264) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L264)

<a id="op-f4a692ce12b7ba"></a>
### Employee Boarding Controller.create task and notify user

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_create_task_and_notify_user`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Task”, “project” → self.project, “subject” → ((activity.activity\_name + “ : ”) + self.employee\_name), “description” → activity.description, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Task”, “project” → self.project, “subject” → ((activity.activity\_name + “ : ”) + self.employee\_name), “description” → activity.description, …)) · call db\_set on activity.

**Local steps**

- Set holiday\_list from self.get\_holiday\_list().
- For each activity in self.activities.
  - If activity.task.
    - Continue with the next iteration or loop test.
  - Set dates from self.get\_task\_dates(activity, holiday\_list).
  - Set task from Platform.get\_doc(mapping(“doctype” → “Task”, “project” → self.project, “subject” → ((nested operand in the contract.activity\_name + “ : ”) + self.employee\_name), “description” → activity.description, …)).i ….
  - Evaluate activity.db\_set(“task”, task.name).
  - Set users from list(activity.user) when activity.user, otherwise list().
    - Value choice on activity.user — true gives list(activity.user), false gives list().
  - If activity.role.
    - Set has\_role from Platform.qb.DocType(“Has Role”).
    - Set user from Platform.qb.DocType(“User”).
    - Set user\_list from nested operand in the contract(nested operand in the contract).distinct().where(((nested operand in the contract.parenttype equals “User” bitwise and nested operand in the contract.enabled equals 1) bitwis ….
    - Set users from unique((users + user\_list)).
    - If “Administrator” belongs to users.
      - Evaluate users.remove(“Administrator”).
  - If users.
    - Evaluate self.assign\_task\_to\_users(task, users).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get holiday list](operations-001.md#op-7a7a9a795d17d5), [get task dates](operations-001.md#op-58e7a0bffe1be3), [assign task to users](operations-001.md#op-310ef1012ba902).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L1858) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L260) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L260)

<a id="op-7a7a9a795d17d5"></a>
### Employee Boarding Controller.get holiday list

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_get_holiday_list`

**Inputs** self.

**Explicit results** get\_holiday\_list\_for\_employee(self.employee, as\_on = self.boarding\_begins\_on) · self.holiday\_list.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Please set the Holiday List.”.

**Local steps**

- If self.doctype equals “Employee Separation”.
  - Return get\_holiday\_list\_for\_employee(self.employee, as\_on = self.boarding\_begins\_on).
- Otherwise.
  - If self.employee.
    - Return get\_holiday\_list\_for\_employee(self.employee, as\_on = self.boarding\_begins\_on).
  - Otherwise.
    - If not self.holiday\_list.
      - Call the validation error handler Platform.throw(translated “Please set the Holiday List.”, Platform.MandatoryError).
    - Otherwise.
      - Return self.holiday\_list.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L5) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L261) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L261)

<a id="op-58e7a0bffe1be3"></a>
### Employee Boarding Controller.get task dates

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_get_task_dates`

**Inputs** self, activity, holiday\_list.

**Explicit results** list(start\_date, end\_date).

**Local steps**

- Set start\_date, end\_date from no value.
- If activity.begin\_on is distinct from no value.
  - Set start\_date from add\_days(self.boarding\_begins\_on, activity.begin\_on).
  - Set start\_date from self.update\_if\_holiday(start\_date, holiday\_list).
  - If activity.duration is distinct from no value.
    - Set end\_date from add\_days(self.boarding\_begins\_on, (activity.begin\_on + activity.duration)).
    - Set end\_date from self.update\_if\_holiday(end\_date, holiday\_list).
- Return list(start\_date, end\_date).

**Methods declared on this owner** [update if holiday](operations-001.md#op-7615a728172652).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L2971) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L262) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L262)

<a id="op-7615a728172652"></a>
### Employee Boarding Controller.update if holiday

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_update_if_holiday`

**Inputs** self, date, holiday\_list.

**Explicit results** date.

**Local steps**

- While is\_holiday(holiday\_list, date).
  - Set date from add\_days(date, 1).
- Return date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L3256) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L265) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L265)

<a id="op-310ef1012ba902"></a>
### Employee Boarding Controller.assign task to users

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_assign_task_to_users`

**Inputs** self, task, users.

**Local steps**

- For each user in users.
  - Set args from mapping(“assign\_to” → list(user), “doctype” → task.doctype, “name” → task.name, “description” → (task.description or task.subject), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in task.description → task.subject.
  - Evaluate assign\_to.add(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L3367) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L259) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L259)

<a id="op-aa6706b3adff45"></a>
### Employee Boarding Controller.on cancel

`operation_workforce_controllers_employee_boarding_controller_business_behavior_employee_boarding_controller_on_cancel`

**Inputs** self.

**Record and data access** read “Task” via get\_all.

**State and service calls** request delete\_doc for “Task” · request delete\_doc for “Project” · call db\_set on self · call db\_set on activity · msgprint with translated “Linked Project {} and Tasks deleted.”.format(project).

**Local steps**

- Set project from self.project.
- For each task in Platform.get\_all(“Task”, filters = mapping(“project” → project)).
  - Evaluate Platform.delete\_doc(“Task”, task.name, force = 1).
- Evaluate Platform.delete\_doc(“Project”, project, force = 1).
- Evaluate self.db\_set(“project”, empty text).
- For each activity in self.activities.
  - Evaluate activity.db\_set(“task”, empty text).
- Evaluate Platform.msgprint(translated “Linked Project {} and Tasks deleted.”.format(project), alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L3578) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L263) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L263)

<a id="op-ce360c3f6f1ba7"></a>
### Get onboarding details

`operation_workforce_controllers_employee_boarding_controller_business_behavior_get_onboarding_details`

**Inputs** parent, parenttype.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Employee Boarding Activity” via get\_all.

**Explicit results** Platform.get\_all(“Employee Boarding Activity”, fields = list(“activity\_name”, “role”, “user”, “required\_for\_employee\_creation”, …), filters = mapping(“parent” → parent, “parenttype” → parenttype), order\_by = “idx”).

**Local steps**

- Evaluate Platform.has\_permission(parenttype, “read”, parent, throw = true).
- Return Platform.get\_all(“Employee Boarding Activity”, fields = list(“activity\_name”, “role”, “user”, “required\_for\_employee\_creation”, …), filters = mapping(“parent” → parent, “parenttype” → parenttype), order\_by = “idx”).

**Values supplied outside this operation** effective access from Platform.has\_permission(parenttype, “read”, parent, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L3946) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L267) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L267)

<a id="op-3762f33908fda3"></a>
### Update employee boarding status

`operation_workforce_controllers_employee_boarding_controller_business_behavior_update_employee_boarding_status`

**Inputs** project, event = no value.

**Record and data access** read “Employee Onboarding” via exists · read “Employee Separation” via exists.

**State and service calls** request set\_value on “Employee Onboarding” · request set\_value on “Employee Separation”.

**Explicit results** no value.

**Local steps**

- Set employee\_onboarding from Platform.db.exists(“Employee Onboarding”, mapping(“project” → project.name)).
- Set employee\_separation from Platform.db.exists(“Employee Separation”, mapping(“project” → project.name)).
- If not (employee\_onboarding or employee\_separation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_onboarding → employee\_separation.
  - Return no value.
- Set status from “Pending”.
- If (flt(project.percent\_complete) &gt; 0.0 and flt(project.percent\_complete) &lt; 100.0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(project.percent\_complete) &gt; 0.0 → flt(project.percent\_complete) &lt; 100.0.
  - Set status from “In Process”.
- Otherwise.
  - If flt(project.percent\_complete) equals 100.0.
    - Set status from “Completed”.
- If employee\_onboarding.
  - Evaluate Platform.db.set\_value(“Employee Onboarding”, employee\_onboarding, “boarding\_status”, status).
- Otherwise.
  - If employee\_separation.
    - Evaluate Platform.db.set\_value(“Employee Separation”, employee\_separation, “boarding\_status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L4230) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L268) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L268)

<a id="op-0dd326c9dd8aab"></a>
### Update task

`operation_workforce_controllers_employee_boarding_controller_business_behavior_update_task`

**Inputs** task, event = no value.

**Record and data access** resolve a document from “Project” via get\_cached\_doc.

**Local steps**

- If (task.project and not task.flags.from\_project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.project → not task.flags.from\_project.
  - Evaluate update\_employee\_boarding\_status(Platform.get\_cached\_doc(“Project”, task.project)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Project”, task.project).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L4700) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L269) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L269)

## Service · Employee reminders

<a id="op-38b0cc41846edf"></a>
### Send reminders in advance weekly

`operation_workforce_controllers_employee_reminders_business_behavior_send_reminders_in_advance_weekly`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set to\_send\_in\_advance from int(Platform.db.get\_single\_value(“HR Settings”, “send\_holiday\_reminders”)).
- Set frequency from Platform.db.get\_single\_value(“HR Settings”, “frequency”).
- If not (to\_send\_in\_advance and frequency equals “Weekly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_send\_in\_advance → frequency equals “Weekly”.
  - Return no value.
- Evaluate send\_advance\_holiday\_reminders(“Weekly”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_holiday\_reminders”), Platform.db.get\_single\_value(“HR Settings”, “frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L4828) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L281) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L281)

<a id="op-1055cc25377e8c"></a>
### Send reminders in advance monthly

`operation_workforce_controllers_employee_reminders_business_behavior_send_reminders_in_advance_monthly`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set to\_send\_in\_advance from int(Platform.db.get\_single\_value(“HR Settings”, “send\_holiday\_reminders”)).
- Set frequency from Platform.db.get\_single\_value(“HR Settings”, “frequency”).
- If not (to\_send\_in\_advance and frequency equals “Monthly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_send\_in\_advance → frequency equals “Monthly”.
  - Return no value.
- Evaluate send\_advance\_holiday\_reminders(“Monthly”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_holiday\_reminders”), Platform.db.get\_single\_value(“HR Settings”, “frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L5020) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L280) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L280)

<a id="op-e7fe67e87e6e78"></a>
### Send advance holiday reminders

`operation_workforce_controllers_employee_reminders_business_behavior_send_advance_holiday_reminders`

**Inputs** frequency.

**Record and data access** read “Employee” via get\_all.

**Explicit results** no value.

**Local steps**

- If frequency equals “Weekly”.
  - Set start\_date from getdate().
  - Set end\_date from add\_days(getdate(), 7).
- Otherwise.
  - If frequency equals “Monthly”.
    - Set start\_date from getdate().
    - Set end\_date from add\_months(getdate(), 1).
  - Otherwise.
    - Return no value.
- Set employees from Platform.db.get\_all(“Employee”, filters = mapping(“status” → “Active”), pluck = “name”).
- For each employee in employees.
  - Set holidays from get\_holidays\_for\_employee(employee, start\_date, end\_date, only\_non\_weekly = true, raise\_exception = false).
  - Evaluate send\_holidays\_reminder\_in\_advance(employee, holidays).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L5212) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L276) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L276)

<a id="op-4e17956eae23fd"></a>
### Send holidays reminder in advance

`operation_workforce_controllers_employee_reminders_business_behavior_send_holidays_reminder_in_advance`

**Inputs** employee, holidays.

**Record and data access** resolve a document from “Employee” via get\_doc · read “HR Settings” via get\_single\_value.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- If not holidays.
  - Return no value.
- Set employee\_doc from Platform.get\_doc(“Employee”, employee).
- Set employee\_email from get\_employee\_email(employee\_doc).
- Set frequency from Platform.db.get\_single\_value(“HR Settings”, “frequency”).
- Set sender\_email from get\_sender\_email().
- Set email\_header from translated “Holidays this Month.” when frequency equals “Monthly”, otherwise translated “Holidays this Week.”.
  - Value choice on frequency equals “Monthly” — true gives translated “Holidays this Month.”, false gives translated “Holidays this Week.”.
- Evaluate Platform.sendmail(sender = sender\_email, recipients = list(employee\_email), subject = translated “Upcoming Holidays Reminder”, template = “holiday\_reminder”, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “frequency”) · service or queued work from Platform.sendmail(sender = sender\_email, recipients = list(employee\_email), subject = translated “Upcoming Holidays Reminder”, template = “holiday\_reminder”, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L5592) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L279) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L279)

<a id="op-e6df1babc6e45e"></a>
### Send birthday reminders

`operation_workforce_controllers_employee_reminders_business_behavior_send_birthday_reminders`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set to\_send from int(Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”)).
- If not to\_send.
  - Return no value.
- Set sender from get\_sender\_email().
- Set employees\_born\_today from get\_employees\_who\_are\_born\_today().
- For each tuple(company, birthday\_persons) in employees\_born\_today.items().
  - Set employee\_emails from get\_all\_employee\_emails(company).
  - Set birthday\_person\_emails from list of get\_employee\_email(doc) for doc drawn from birthday\_persons.
    - Draw doc from birthday\_persons.
  - Set recipients from list((set(employee\_emails) − set(birthday\_person\_emails))).
  - Set tuple(reminder\_text, message) from get\_birthday\_reminder\_text\_and\_message(birthday\_persons).
  - Evaluate send\_birthday\_reminder(recipients, reminder\_text, birthday\_persons, message, …).
  - If len(birthday\_persons) &gt; 1.
    - For each person in birthday\_persons.
      - Set person\_email from (person at “user\_id” or person at “personal\_email” or person at “company\_email”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in person at “user\_id” → person at “personal\_email” → person at “company\_email”.
      - Set others from list of d for d drawn from birthday\_persons where d differs from person.
        - Draw d from birthday\_persons, keep a combination only if (d differs from person).
      - Set tuple(reminder\_text, message) from get\_birthday\_reminder\_text\_and\_message(others).
      - Evaluate send\_birthday\_reminder(person\_email, reminder\_text, others, message, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L6075) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L278) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L278)

<a id="op-428178dcfedc9e"></a>
### Get birthday reminder text and message

`operation_workforce_controllers_employee_reminders_business_behavior_get_birthday_reminder_text_and_message`

**Inputs** birthday\_persons.

**Explicit results** tuple(reminder\_text, message).

**Local steps**

- If len(birthday\_persons) equals 1.
  - Set birthday\_person\_text from birthday\_persons at 0 at “name”.
- Otherwise.
  - Set person\_names from list of d at “name” for d drawn from birthday\_persons.
    - Draw d from birthday\_persons.
  - Set birthday\_person\_text from comma\_sep(person\_names, Platform.\_(“{0} &amp; {1}”), false).
- Set reminder\_text from translated “Today is {0}'s birthday 🎉”.format(birthday\_person\_text).
- Set message from translated “A friendly reminder of an important date for our team.”.
- Update message using + text in the contract.
- Update message using + translated “Everyone, let’s congratulate {0} on their birthday.”.format(birthday\_person\_text).
- Return tuple(reminder\_text, message).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L6689) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L270) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L270)

<a id="op-926823eb0b2591"></a>
### Send birthday reminder

`operation_workforce_controllers_employee_reminders_business_behavior_send_birthday_reminder`

**Inputs** recipients, reminder\_text, birthday\_persons, message, sender = no value.

**State and service calls** sendmail.

**Local steps**

- Evaluate Platform.sendmail(sender = sender, recipients = recipients, subject = translated “Birthday Reminder”, template = “birthday\_reminder”, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(sender = sender, recipients = recipients, subject = translated “Birthday Reminder”, template = “birthday\_reminder”, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L7020) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L277) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L277)

<a id="op-b1e2508a57ec3c"></a>
### Get employees who are born today

`operation_workforce_controllers_employee_reminders_business_behavior_get_employees_who_are_born_today`

**Inputs** no declared parameters.

**Explicit results** get\_employees\_having\_an\_event\_today(“birthday”).

**Local steps**

- Return get\_employees\_having\_an\_event\_today(“birthday”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L7218) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L272) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L272)

<a id="op-c5d892ca17e4e2"></a>
### Get employees having an event today

`operation_workforce_controllers_employee_reminders_business_behavior_get_employees_having_an_event_today`

**Inputs** event\_type.

**Explicit results** no value · grouped\_employees.

**Local steps**

- Bind dependencies defaultdict.
- If event\_type equals “birthday”.
  - Set condition\_column from “date\_of\_birth”.
- Otherwise.
  - If event\_type equals “work\_anniversary”.
    - Set condition\_column from “date\_of\_joining”.
  - Otherwise.
    - Return no value.
- Set today\_date from getdate().
- Set Employee from Platform.qb.DocType(“Employee”).
- Set event\_date from Employee at condition\_column.
- Set employees\_born\_today from nested operand in the contract(nested operand in the contract).select(Employee.personal\_email, Employee.company, Employee.company\_email, Employee.user\_id, …).where((((nested operand in the contract equals  ….
- Set grouped\_employees from defaultdict(deferred anonymous expression).
- For each employee\_doc in employees\_born\_today.
  - Evaluate grouped\_employees at employee\_doc.get(“company”).append(employee\_doc).
- Return grouped\_employees.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0005.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L271) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L271)

<a id="op-b4763d8c2ed041"></a>
### Send work anniversary reminders

`operation_workforce_controllers_employee_reminders_business_behavior_send_work_anniversary_reminders`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set to\_send from int(Platform.db.get\_single\_value(“HR Settings”, “send\_work\_anniversary\_reminders”)).
- If not to\_send.
  - Return no value.
- Set sender from get\_sender\_email().
- Set employees\_joined\_today from get\_employees\_having\_an\_event\_today(“work\_anniversary”).
- Set message from translated “A friendly reminder of an important date for our team.”.
- Update message using + text in the contract.
- Update message using + translated “Everyone, let’s congratulate them on their work anniversary!”.
- For each tuple(company, anniversary\_persons) in employees\_joined\_today.items().
  - Set employee\_emails from get\_all\_employee\_emails(company).
  - Set anniversary\_person\_emails from list of get\_employee\_email(doc) for doc drawn from anniversary\_persons.
    - Draw doc from anniversary\_persons.
  - Set recipients from list((set(employee\_emails) − set(anniversary\_person\_emails))).
  - Set reminder\_text from get\_work\_anniversary\_reminder\_text(anniversary\_persons).
  - Evaluate send\_work\_anniversary\_reminder(recipients, reminder\_text, anniversary\_persons, message, …).
  - If len(anniversary\_persons) &gt; 1.
    - For each person in anniversary\_persons.
      - Set person\_email from (person at “user\_id” or person at “personal\_email” or person at “company\_email”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in person at “user\_id” → person at “personal\_email” → person at “company\_email”.
      - Set others from list of d for d drawn from anniversary\_persons where d differs from person.
        - Draw d from anniversary\_persons, keep a combination only if (d differs from person).
      - Set reminder\_text from get\_work\_anniversary\_reminder\_text(others).
      - Evaluate send\_work\_anniversary\_reminder(person\_email, reminder\_text, others, message, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_work\_anniversary\_reminders”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0005.json#L623) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L283) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L283)

<a id="op-a44ba9cfe5feba"></a>
### Get work anniversary reminder text

`operation_workforce_controllers_employee_reminders_business_behavior_get_work_anniversary_reminder_text`

**Inputs** anniversary\_persons.

**Declared result** str.

**Explicit results** translated “Today {0} completed {1} {2} at our Company! 🎉”.format(translated anniversary\_person, completed\_years, get\_year\_label(completed\_years)) · translated “Today {0} at our Company! 🎉”.format(translated anniversary\_person).

**Local steps**

- If len(anniversary\_persons) equals 1.
  - Set anniversary\_person from anniversary\_persons at 0 at “name”.
  - Set completed\_years from (getdate().year − anniversary\_persons at 0 at “date\_of\_joining”.year).
  - Return translated “Today {0} completed {1} {2} at our Company! 🎉”.format(translated anniversary\_person, completed\_years, get\_year\_label(completed\_years)).
- Set names\_grouped\_by\_years from mapping().
- For each person in anniversary\_persons.
  - Set completed\_years from (getdate().year − person at “date\_of\_joining”.year).
  - Evaluate names\_grouped\_by\_years.setdefault(completed\_years, list()).append(person at “name”).
- Set person\_names\_with\_years from list of translated “{0} completed {1} {2}”.format(comma\_sep(person\_names, translated “{0} &amp; {1}”, false), years, get\_year\_label(years)) for tuple(years, person\_names) drawn from names\_grouped\_by\_years.items().
  - Draw tuple(years, person\_names) from names\_grouped\_by\_years.items().
- Set anniversary\_person from comma\_sep(person\_names\_with\_years, translated “{0} &amp; {1}”, false).
- Return translated “Today {0} at our Company! 🎉”.format(translated anniversary\_person).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0005.json#L1288) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L274) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L274)

<a id="op-7c3b1b229cf84c"></a>
### Get year label

`operation_workforce_controllers_employee_reminders_business_behavior_get_year_label`

**Inputs** years.

**Declared result** str.

**Explicit results** translated “year” when years equals 1, otherwise translated “years”.

**Local steps**

- Return translated “year” when years equals 1, otherwise translated “years”.
  - Value choice on years equals 1 — true gives translated “year”, false gives translated “years”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0005.json#L1884) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L275) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L275)

<a id="op-e6f5020e6e7de5"></a>
### Send work anniversary reminder

`operation_workforce_controllers_employee_reminders_business_behavior_send_work_anniversary_reminder`

**Inputs** recipients, reminder\_text, anniversary\_persons, message, sender = no value.

**State and service calls** sendmail.

**Local steps**

- Evaluate Platform.sendmail(sender = sender, recipients = recipients, subject = translated “Work Anniversary Reminder”, template = “anniversary\_reminder”, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(sender = sender, recipients = recipients, subject = translated “Work Anniversary Reminder”, template = “anniversary\_reminder”, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0005.json#L1984) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L282) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L282)
