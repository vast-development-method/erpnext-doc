# Projects and time · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-7c73872c8cec2a"></a>
### Project.calculate gross margin

`operation_enterprise_projects_record_definitions_project_business_behavior_project_calculate_gross_margin`

**Inputs** self.

**Local steps**

- Set expense\_amount from ((flt(self.total\_costing\_amount) + flt(self.total\_purchase\_cost)) + flt(self.get(“total\_consumed\_material\_cost”, 0))).
- Set self.gross\_margin from (flt(self.total\_billed\_amount) − expense\_amount).
- If self.total\_billed\_amount.
  - Set self.per\_gross\_margin from ((self.gross\_margin ÷ flt(self.total\_billed\_amount)) × 100).
- Otherwise.
  - Set self.per\_gross\_margin from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L6847) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L681)

<a id="op-c7d1faaed65bb6"></a>
### Project.db set cost

`operation_enterprise_binding_enterprise_projects_doctype_project_project_project_db_set_cost`

**Inputs** self, cost\_field.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.calculate\_gross\_margin().
- Evaluate self.db\_set(mapping(cost\_field → self.get(cost\_field), “gross\_margin” → self.gross\_margin, “per\_gross\_margin” → self.per\_gross\_margin), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate gross margin](operations-007.md#op-7c73872c8cec2a).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L223) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1348)

<a id="op-dd61aefc751a73"></a>
### Project.update purchase costing

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_purchase_costing`

**Inputs** self.

**Local steps**

- Set self.total\_purchase\_cost from ProjectCostQueries(self.name).purchase\_cost().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L702)

<a id="op-6921967d707bcc"></a>
### Project.update sales amount

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_sales_amount`

**Inputs** self.

**Local steps**

- Set self.total\_sales\_amount from ProjectCostQueries(self.name).sales\_order\_amount().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L703)

<a id="op-43d0dee8ca9c2a"></a>
### Project.update billed amount

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_billed_amount`

**Inputs** self.

**Local steps**

- Set self.total\_billed\_amount from ProjectCostQueries(self.name).billed\_amount().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L697)

<a id="op-0d9ebae6a8e2ba"></a>
### Project.after rename

`operation_enterprise_projects_record_definitions_project_business_behavior_project_after_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**State and service calls** request set\_value on “Project”.

**Local steps**

- If old\_name equals self.copied\_from.
  - Evaluate Platform.db.set\_value(“Project”, new\_name, “copied\_from”, new\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L1096) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L678)

<a id="op-6b27d217b87388"></a>
### Project.send welcome email

`operation_enterprise_projects_record_definitions_project_business_behavior_project_send_welcome_email`

**Inputs** self.

**Record and data access** read “User” via get\_value.

**State and service calls** sendmail.

**Local steps**

- Set label from formatted text {self.project\_name} ({self.name}).
- Set url from get\_link\_to\_form(self.doctype, self.name, label).
- Set content from text in the contract.format(translated “You have been invited to collaborate on the project {0}.”.format(url)).
- For each user in self.users.
  - If user.welcome\_email\_sent equals 0.
    - Set user\_info from Platform.db.get\_value(“User”, user.user, list(“enabled”, “email”), as\_dict = true).
    - If (user\_info and user\_info.enabled and user\_info.email).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in user\_info → user\_info.enabled → user\_info.email.
      - Evaluate Platform.sendmail(recipients = list(user\_info.email), subject = translated “Project Collaboration Invitation”, content = content).
      - Set user.welcome\_email\_sent from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = list(user\_info.email), subject = translated “Project Collaboration Invitation”, content = content).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L1227) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L694)

<a id="op-1810b84baae99e"></a>
### Project.control access for project users

`operation_enterprise_projects_record_definitions_project_business_behavior_project_control_access_for_project_users`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind local operation revoke\_access\_for\_project\_users for subsequent calls.
- Bind local operation grant\_access\_for\_project\_users for subsequent calls.
- Set current\_users from set(list of d.user for d drawn from self.users).
  - Draw d from self.users.
- Set old\_doc from self.get\_doc\_before\_save().
- If not old\_doc.
  - Evaluate grant\_access\_for\_project\_users(current\_users).
  - Return no value.
- Set previous\_users from set(list of d.user for d drawn from old\_doc.users).
  - Draw d from old\_doc.users.
- Set new\_users from (current\_users − previous\_users).
- Set removed\_users from (previous\_users − current\_users).
- Evaluate revoke\_access\_for\_project\_users(removed\_users).
- Evaluate grant\_access\_for\_project\_users(new\_users).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L1657) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L685)

<a id="op-951b0ae4f7bd5e"></a>
### Project.control access for project users.revoke access for project users

`operation_enterprise_projects_record_definitions_project_business_behavior_project_control_access_for_project_users_revoke_access_for_project_users`

**Inputs** removed\_users.

**Local steps**

- Set users from set(list of d.user for d drawn from Platform.share.get\_users(self.doctype, self.name)).
  - Draw d from Platform.share.get\_users(self.doctype, self.name).
- For each user in removed\_users.
  - If user does not belong to users.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.share.remove(self.doctype, self.name, user).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L2210) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L687)

<a id="op-c4cca2cfd4f242"></a>
### Project.control access for project users.grant access for project users

`operation_enterprise_projects_record_definitions_project_business_behavior_project_control_access_for_project_users_grant_access_for_project_users`

**Inputs** new\_users.

**Local steps**

- For each user in new\_users.
  - Evaluate Platform.share.add\_docshare(self.doctype, self.name, user = user).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L2412) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L686)

<a id="op-db53e30b84981d"></a>
### Get timeline data

`operation_enterprise_projects_record_definitions_project_business_behavior_get_timeline_data`

**Inputs** doctype, name.

**Declared result** dict at tuple(int, int).

**Explicit results** dict(nested operand in the contract.where(nested operand in the contract &lt; nested operand in the contract).groupby(Date(timesheet\_detail.from\_time)).run()).

**Local steps**

- Set timesheet\_detail from Platform.qb.DocType(“Timesheet Detail”).
- Return dict(nested operand in the contract.where(nested operand in the contract &lt; nested operand in the contract).groupby(Date(timesheet\_detail.from\_time)).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L673)

<a id="op-f02b4599a2b47e"></a>
### Get project list

`operation_enterprise_projects_record_definitions_project_business_behavior_get_project_list`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, order\_by = “creation”.

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, fields = PORTAL\_LIST\_FIELDS, filters = filters, or\_filters = or\_filters, limit\_start = limit\_start, …).

**Local steps**

- Set tuple(customers, suppliers) from get\_customers\_suppliers(“Project”, Platform.session.user).
- Set ignore\_permissions from false.
- If (is\_website\_user() and Platform.session.user differs from “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_website\_user() → Platform.session.user differs from “Guest”.
  - If not filters.
    - Set filters from list().
  - If customers.
    - Evaluate filters.append(list(doctype, “customer”, “in”, customers)).
    - Set ignore\_permissions from true.
- Set meta from Platform.get\_meta(doctype).
- Set or\_filters from list().
- If txt.
  - If meta.search\_fields.
    - For each f in meta.get\_search\_fields().
      - If (f equals “name” or meta.get\_field(f).fieldtype belongs to tuple(“Data”, “Text”, “Small Text”, “Text Editor”, …)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in f equals “name” → meta.get\_field(f).fieldtype belongs to tuple(“Data”, “Text”, “Small Text”, “Text Editor”, …).
        - Evaluate or\_filters.append(list(doctype, f, “like”, ((“%” + txt) + “%”))).
  - Otherwise.
    - If isinstance(filters, dict).
      - Set filters at “name” from tuple(“like”, ((“%” + txt) + “%”)).
    - Otherwise.
      - Evaluate filters.append(list(doctype, “name”, “like”, ((“%” + txt) + “%”))).
- Return Platform.get\_list(doctype, fields = PORTAL\_LIST\_FIELDS, filters = filters, or\_filters = or\_filters, limit\_start = limit\_start, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L671)

<a id="op-be99e8fb439f3c"></a>
### Get list context

`operation_enterprise_projects_record_definitions_project_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Projects”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L3642) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L670)

<a id="op-a68d3ccff5f046"></a>
### Get users for project

`operation_enterprise_projects_record_definitions_project_business_behavior_get_users_for_project`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, User).format(expanded names mapping(“key” → searchfield, “fcond” → get\_filters\_cond(doctype, filters, conditions), “mcond” → get\_match\_cond(doctype))).

**Explicit results** Platform.db.sql(query text (SELECT, User).format(expanded names mapping(“key” → searchfield, “fcond” → get\_filters\_cond(doctype, filters, conditions), “mcond” → get\_match\_cond(doctype))), mapping(“txt” → ( ….

**Local steps**

- Set conditions from list().
- Return Platform.db.sql(query text (SELECT, User).format(expanded names mapping(“key” → searchfield, “fcond” → get\_filters\_cond(doctype, filters, conditions), “mcond” → get\_match\_cond(doctype))), mapping(“txt” → ( ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L675)

<a id="op-884c9de29df184"></a>
### Get cost center name

`operation_enterprise_projects_record_definitions_project_business_behavior_get_cost_center_name`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Project” via get\_value.

**Explicit results** Platform.db.get\_value(“Project”, project, “cost\_center”).

**Local steps**

- Evaluate Platform.has\_permission(“Project”, “select”, project, throw = true).
- Return Platform.db.get\_value(“Project”, project, “cost\_center”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Project”, “select”, project, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L668)

<a id="op-513d9123de1d0e"></a>
### Hourly reminder

`operation_enterprise_projects_record_definitions_project_business_behavior_hourly_reminder`

**Inputs** no declared parameters.

**Local steps**

- Set fields from list(“from\_time”, “to\_time”).
- Set projects from get\_projects\_for\_collect\_progress(“Hourly”, fields).
- For each project in projects.
  - If is\_now\_between(project.from\_time, project.to\_time).
    - Evaluate send\_project\_update\_email\_to\_users(project.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L676)

<a id="op-cf2a8b3d61a997"></a>
### Is now between

`operation_enterprise_binding_enterprise_projects_doctype_project_project_is_now_between`

**Inputs** from\_time, to\_time.

**Declared result** bool.

**Explicit results** from\_time ≤ now ≤ to\_time · (now ≥ from\_time or now ≤ to\_time).

**Local steps**

- Set tuple(now, from\_time, to\_time) from tuple(get\_time(nowtime()), get\_time(from\_time), get\_time(to\_time)).
- If from\_time ≤ to\_time.
  - Return from\_time ≤ now ≤ to\_time.
    - Compare adjacent operands in order, stopping at the first false comparison in from\_time ≤ now ≤ to\_time.
- Return (now ≥ from\_time or now ≤ to\_time).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in now ≥ from\_time → now ≤ to\_time.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1283)

<a id="op-3c25e0e9fef065"></a>
### Project status update reminder

`operation_enterprise_projects_record_definitions_project_business_behavior_project_status_update_reminder`

**Inputs** no declared parameters.

**Local steps**

- Evaluate daily\_reminder().
- Evaluate twice\_daily\_reminder().
- Evaluate weekly\_reminder().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0601.json#L5084) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L696)

<a id="op-6d993ad285839c"></a>
### Daily reminder

`operation_enterprise_projects_record_definitions_project_business_behavior_daily_reminder`

**Inputs** no declared parameters.

**Local steps**

- Set fields from list(“daily\_time\_to\_send”).
- Set projects from get\_projects\_for\_collect\_progress(“Daily”, fields).
- For each project in projects.
  - If get\_due\_project\_updates(project.name, project.daily\_time\_to\_send).
    - Evaluate send\_project\_update\_email\_to\_users(project.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L667)

<a id="op-68edb803960148"></a>
### Twice daily reminder

`operation_enterprise_projects_record_definitions_project_business_behavior_twice_daily_reminder`

**Inputs** no declared parameters.

**Local steps**

- Set projects from get\_projects\_for\_collect\_progress(“Twice Daily”, list(“first\_email”, “second\_email”)).
- For each project in projects.
  - For each \_due in range(get\_due\_project\_updates(project.name, project.first\_email, project.second\_email)).
    - Evaluate send\_project\_update\_email\_to\_users(project.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L708)

<a id="op-57f3b6a9b2e001"></a>
### Weekly reminder

`operation_enterprise_projects_record_definitions_project_business_behavior_weekly_reminder`

**Inputs** no declared parameters.

**Local steps**

- Set fields from list(“day\_to\_send”, “weekly\_time\_to\_send”).
- Set projects from get\_projects\_for\_collect\_progress(“Weekly”, fields).
- Set current\_day from get\_datetime().strftime(“%A”).
- For each project in projects.
  - If current\_day differs from project.day\_to\_send.
    - Continue with the next iteration or loop test.
  - If get\_due\_project\_updates(project.name, project.weekly\_time\_to\_send).
    - Evaluate send\_project\_update\_email\_to\_users(project.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L711)

<a id="op-f825029c222cf1"></a>
### Get due project updates

`operation_enterprise_binding_enterprise_projects_doctype_project_project_get_due_project_updates`

**Inputs** project, remaining positional values times.

**Declared result** int.

**Record and data access** read “Project Update” via count.

**Explicit results** max((times\_passed − Platform.db.count(“Project Update”, mapping(“project” → project, “date” → today()))), 0).

**Local steps**

- Set now from get\_time(nowtime()).
- Set times\_passed from sum(generator of now ≥ get\_time(time) for time drawn from times).
  - Draw time from times.
- Return max((times\_passed − Platform.db.count(“Project Update”, mapping(“project” → project, “date” → today()))), 0).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1277)

<a id="op-74e626c13666af"></a>
### Create duplicate project

`operation_enterprise_projects_record_definitions_project_business_behavior_create_duplicate_project`

**Inputs** prev\_doc, project\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** request copy\_doc for prev\_doc · call insert on project · call db\_set on project.

**Explicit failure paths** validation helper — translated “Save the Project before duplicating it” · validation helper — translated “Use a name that is different from previous project name”.

**Local steps**

- Bind dependencies json.
- Set prev\_doc from json.loads(prev\_doc).
- Set source\_name from prev\_doc.get(“name”).
- If not source\_name.
  - Call the validation error handler Platform.throw(translated “Save the Project before duplicating it”).
- Evaluate Platform.has\_permission(“Project”, “read”, source\_name, throw = true).
- If project\_name equals source\_name.
  - Call the validation error handler Platform.throw(translated “Use a name that is different from previous project name”).
- Set project from Platform.copy\_doc(prev\_doc).
- Set project.name from project\_name.
- Set project.project\_template from empty text.
- Set project.project\_name from project\_name.
- Evaluate project.insert().
- Evaluate copy\_tasks(source\_name, project.name).
- Evaluate project.db\_set(“project\_template”, prev\_doc.get(“project\_template”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Project”, “read”, source\_name, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L665)

<a id="op-47e56b44538fa0"></a>
### Copy tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_project_copy_tasks`

**Inputs** source\_project, target\_project.

**Record and data access** resolve a document from “Task” via get\_doc · read “Task” via get\_all.

**State and service calls** request copy\_doc for source\_task · call insert on task · call save on task.

**Local steps**

- Set source\_tasks from list of Platform.get\_doc(“Task”, name) for name drawn from Platform.get\_all(“Task”, filters = mapping(“project” → source\_project), order\_by = “lft”, pluck = “name”).
  - Draw name from Platform.get\_all(“Task”, filters = mapping(“project” → source\_project), order\_by = “lft”, pluck = “name”).
- Set copied\_names from mapping().
- For each source\_task in source\_tasks.
  - Set task from Platform.copy\_doc(source\_task).
  - Set task.project from target\_project.
  - Set task.parent\_task from copied\_names.get(task.parent\_task).
  - Evaluate task.set(“depends\_on”, list()).
  - Set copied\_names at source\_task.name from task.insert().name.
- For each source\_task in source\_tasks.
  - If not source\_task.depends\_on.
    - Continue with the next iteration or loop test.
  - Set task from Platform.get\_doc(“Task”, copied\_names at source\_task.name).
  - Evaluate task.set(“depends\_on”, list of mapping(“task” → copied\_names.get(row.task, row.task)) for row drawn from source\_task.depends\_on).
    - Draw row from source\_task.depends\_on.
  - Evaluate task.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1276)
