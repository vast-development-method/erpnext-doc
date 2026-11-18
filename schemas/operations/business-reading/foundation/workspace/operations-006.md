# Forms, reports and navigation · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Assign to

<a id="op-dbcde3fd4b3887"></a>
### Remove

`operation_foundation_desk_form_assign_to_business_behavior_remove`

**Inputs** doctype, name, assign\_to.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_remove(doctype, name, assign\_to, ignore\_permissions = false).

**Local steps**

- Return \_remove(doctype, name, assign\_to, ignore\_permissions = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L159)

<a id="op-c62d5fa0837667"></a>
### Remove

`operation_foundation_desk_form_assign_to_business_behavior_remove_2`

**Inputs** doctype, name, assign\_to, ignore\_permissions = false.

**Explicit results** set\_status(doctype, name, empty text, assign\_to, status = “Cancelled”, ignore\_permissions = ignore\_permissions).

**Local steps**

- Return set\_status(doctype, name, empty text, assign\_to, status = “Cancelled”, ignore\_permissions = ignore\_permissions).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L51) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L160)

<a id="op-82a228bc78cc2a"></a>
### Remove multiple

`operation_foundation_desk_form_assign_to_business_behavior_remove_multiple`

**Inputs** doctype, names.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set docname\_list from json.loads(names).
- For each name in docname\_list.
  - Set assignments from get(mapping(“doctype” → doctype, “name” → name)).
  - If not assignments.
    - Continue with the next iteration or loop test.
  - For each assignment in assignments.
    - Evaluate remove(doctype, name, assignment.get(“owner”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L52) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L161)

<a id="op-0f4ce057fdb756"></a>
### Close

`operation_foundation_desk_form_assign_to_business_behavior_close`

**Inputs** doctype, name, assign\_to.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** set\_status(doctype, name, empty text, assign\_to, status = “Closed”, ignore\_permissions = false).

**Explicit failure paths** validation helper — translated “Only the assignee can complete this to-do.”.

**Local steps**

- If assign\_to differs from Platform.session.user.
  - Call the validation error handler Platform.throw(translated “Only the assignee can complete this to-do.”).
- Return set\_status(doctype, name, empty text, assign\_to, status = “Closed”, ignore\_permissions = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L645) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L154)

<a id="op-e97ef7836f33bf"></a>
### Set status

`operation_foundation_desk_form_assign_to_business_behavior_set_status`

**Inputs** doctype, name, todo = no value, assign\_to = no value, status = “Cancelled”, ignore\_permissions = false.

**Record and data access** resolve a document from doctype via get\_doc · read “ToDo” via get\_value · resolve a document from “ToDo” via get\_doc.

**State and service calls** call save on todo · request set\_value on doctype.

**Explicit results** get(mapping(“doctype” → doctype, “name” → name)).

**Local steps**

- If not ignore\_permissions.
  - Evaluate Platform.get\_doc(doctype, name).check\_permission().
- Attempt the following.
  - If not todo.
    - Set todo from Platform.db.get\_value(“ToDo”, mapping(“reference\_type” → doctype, “reference\_name” → name, “allocated\_to” → assign\_to, “status” → tuple(“!=”, status))).
  - If todo.
    - Set todo from Platform.get\_doc(“ToDo”, todo).
    - Set todo.status from status.
    - Evaluate todo.save(ignore\_permissions = true).
    - Evaluate notify\_assignment(todo.assigned\_by, todo.allocated\_to, todo.reference\_type, todo.reference\_name).
- On failure (Platform.DoesNotExistError).
  - Take no action here.
- If (Platform.get\_meta(doctype).get\_field(“assigned\_to”) and status belongs to tuple(“Cancelled”, “Closed”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_meta(doctype).get\_field(“assigned\_to”) → status belongs to tuple(“Cancelled”, “Closed”).
  - Evaluate Platform.db.set\_value(doctype, name, “assigned\_to”, no value).
- Return get(mapping(“doctype” → doctype, “name” → name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L843) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L162)

<a id="op-3df071b93cedfe"></a>
### Clear

`operation_foundation_desk_form_assign_to_business_behavior_clear`

**Inputs** doctype, name, ignore\_permissions = false.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** false · true.

**Local steps**

- Set assignments from Platform.get\_all(“ToDo”, fields = list(“allocated\_to”, “name”), filters = dict(reference\_type = doctype, reference\_name = name)).
- If not assignments.
  - Return false.
- For each assign\_to in assignments.
  - Evaluate set\_status(doctype, name, todo = assign\_to.name, assign\_to = assign\_to.allocated\_to, status = “Cancelled”, ignore\_permissions = ignore\_permissions).
- Return true.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L1449) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L153)

<a id="op-722943d93cf939"></a>
### Notify assignment

`operation_foundation_desk_form_assign_to_business_behavior_notify_assignment`

**Inputs** assigned\_by, allocated\_to, doc\_type, doc\_name, action = “CLOSE”, description = no value.

**Record and data access** read “User” via get\_value · read “User” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not (assigned\_by and allocated\_to and doc\_type and doc\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in assigned\_by → allocated\_to → doc\_type → doc\_name.
  - Return no value.
- Set assigned\_user from Platform.db.get\_value(“User”, allocated\_to, list(“language”, “enabled”), as\_dict = true).
- If (assigned\_by equals allocated\_to or not assigned\_user.enabled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in assigned\_by equals allocated\_to → not assigned\_user.enabled.
  - Return no value.
- Set user\_name from Platform.get\_cached\_value(“User”, Platform.session.user, “full\_name”).
- Set title from get\_title(doc\_type, doc\_name).
- Set description\_html from formatted text &lt;div&gt;{description}&lt;/div&gt; when description, otherwise no value.
  - Value choice on description — true gives formatted text &lt;div&gt;{description}&lt;/div&gt;, false gives no value.
- If action equals “CLOSE”.
  - Set subject from \_(“Your assignment on {0} {1} has been removed by {2}”, lang = assigned\_user.language).format(Platform.bold(translated doc\_type), get\_title\_html(title), Platform.bold(user\_name)).
- Otherwise.
  - Set user\_name from Platform.bold(user\_name).
  - Set document\_type from Platform.bold(\_(doc\_type, lang = assigned\_user.language)).
  - Set title from get\_title\_html(title).
  - Set subject from \_(“{0} assigned a new task {1} {2} to you”, lang = assigned\_user.language).format(user\_name, document\_type, title).
- Set notification\_doc from mapping(“type” → “Assignment”, “document\_type” → doc\_type, “subject” → subject, “document\_name” → doc\_name, …).
- Evaluate enqueue\_create\_notification(allocated\_to, notification\_doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, Platform.session.user, “full\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L1716) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L158)

<a id="op-a2d0352e8db9d9"></a>
### Format message for assign to

`operation_foundation_desk_form_assign_to_business_behavior_format_message_for_assign_to`

**Inputs** users.

**Explicit results** (text in the contract + text in the contract.join(users)).

**Local steps**

- Return (text in the contract + text in the contract.join(users)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L2542) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L156)

## Service · Attribution

<a id="op-4f47ddf6205653"></a>
### Get context

`operation_foundation_public_pages_attribution_business_behavior_get_context`

**Inputs** context.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need to be a system user to access this page.”.

**Local steps**

- If not is\_system\_user().
  - Call the validation error handler Platform.throw(translated “You need to be a system user to access this page.”, Platform.PermissionError).
- Set inventory from collect(Platform.get\_installed\_apps()).
- Set apps from list().
- For each app in inventory.apps.
  - Set dependencies from list of mapping(“name” → package.name, “version” → package.version, “type” → PACKAGE\_TYPES at package.ecosystem, “license” → package.license.summary, …) for package drawn from inventory.direct\_dependencies(app).
    - Draw package from inventory.direct\_dependencies(app).
  - If any(list(app.authors, dependencies, app.description)).
    - Evaluate apps.append(mapping(“name” → app.name, “description” → app.description, “authors” → “, ”.join(app.authors), “dependencies” → dependencies)).
- Set context.apps from apps.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L65) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L26)

## Report · Audit system hooks

<a id="op-e1db7d17de4523"></a>
### Execute

`operation_foundation_custom_report_audit_system_hooks_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data()).

**Local steps**

- Return tuple(get\_columns(), get\_data()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L3481) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1025)

<a id="op-5b21a9472d7a2c"></a>
### Get columns

`operation_foundation_custom_report_audit_system_hooks_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set values\_field\_type from “Data”.
- Set columns from list(mapping(“label” → “Hook name”, “fieldname” → “hook\_name”, “fieldtype” → “Data”, “width” → 200), mapping(“label” → “Hook key (optional)”, “fieldname” → “hook\_key”, “fieldtype” → “Data”, “width” → 200), ….
- Set installed\_apps from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
- Update columns using + list of mapping(“label” → app, “fieldname” → app, “fieldtype” → values\_field\_type) for app drawn from installed\_apps.
  - Draw app from installed\_apps.
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L3549) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1026)

<a id="op-6a71a85dde77ab"></a>
### Get data

`operation_foundation_custom_report_audit_system_hooks_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** data.

**Local steps**

- Set hooks from Platform.get\_hooks().
- Set installed\_apps from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
- Bind local operation fmt\_hook\_values for subsequent calls.
- Set data from list().
- For each tuple(hook, values) in hooks.items().
  - If isinstance(values, dict).
    - For each tuple(k, v) in values.items().
      - Set row from mapping(“hook\_name” → hook, “hook\_key” → fmt\_hook\_values(k), “hook\_values” → fmt\_hook\_values(v)).
      - For each app in installed\_apps.
        - If app\_hooks bound to delist(Platform.get\_hooks(hook, app\_name = app)).
          - Set row at app from fmt\_hook\_values(app\_hooks.get(k)).
      - Evaluate data.append(row).
  - Otherwise.
    - Set row from mapping(“hook\_name” → hook, “hook\_values” → fmt\_hook\_values(values)).
    - For each app in installed\_apps.
      - Set row at app from fmt\_hook\_values(Platform.get\_hooks(hook, app\_name = app)).
    - Evaluate data.append(row).
- Return data.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(), Platform.get\_hooks(hook, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L3910) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1027)

<a id="op-aefe89030e702d"></a>
### Get data.fmt hook values

`operation_foundation_custom_report_audit_system_hooks_business_behavior_get_data_format_hook_values`

**Inputs** v.

**Explicit results** empty text · Platform.as\_json(v) · str(v).

**Local steps**

- If not v.
  - Return empty text.
- Set v from delist(v).
- If isinstance(v, (dict bitwise or list)).
  - Attempt the following.
    - Return Platform.as\_json(v).
  - On failure (Exception).
    - Take no action here.
- Return str(v).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L4642) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1028)

<a id="op-e2696de71b037c"></a>
### Delist

`operation_foundation_custom_report_audit_system_hooks_business_behavior_delist`

**Inputs** val.

**Explicit results** val at 0 · val.

**Local steps**

- If (isinstance(val, list) and len(val) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(val, list) → len(val) equals 1.
  - Return val at 0.
- Return val.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L4823) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1024)

## Workspace · Backups

<a id="op-9d36e1091ff7fc"></a>
### Get time

`operation_foundation_desk_page_backups_business_behavior_get_time`

**Inputs** path.

**Explicit results** convert\_utc\_to\_system\_timezone(datetime.datetime.fromtimestamp(nested operand in the contract.stat().st\_mtime, tz = datetime.UTC)).strftime(“%a %b %d %H:%M %Y”).

**Local steps**

- Return convert\_utc\_to\_system\_timezone(datetime.datetime.fromtimestamp(nested operand in the contract.stat().st\_mtime, tz = datetime.UTC)).strftime(“%a %b %d %H:%M %Y”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L6257) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L331)

<a id="op-5386d68ad2f04b"></a>
### Get encrytion status

`operation_foundation_desk_page_backups_business_behavior_get_encrytion_status`

**Inputs** path.

**Explicit results** “-enc” belongs to path.name.

**Local steps**

- Return “-enc” belongs to path.name.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L6380) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L329)

<a id="op-ed1799db9f216d"></a>
### Get size

`operation_foundation_desk_page_backups_business_behavior_get_size`

**Inputs** path.

**Explicit results** formatted text {(size ÷ mbase)}M · formatted text {(size ÷ 1024)}K.

**Local steps**

- Set size from path.stat().st\_size.
- Set mbase from (1024 × 1024).
- If size &gt; mbase.
  - Return formatted text {(size ÷ mbase)}M.
- Return formatted text {(size ÷ 1024)}K.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L6440) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L330)

<a id="op-df4f00edbe0c57"></a>
### Get context

`operation_foundation_desk_page_backups_business_behavior_get_context`

**Inputs** context.

**Explicit results** mapping(“files” → backup\_files at slice no value to backup\_limit).

**Local steps**

- Set context.no\_cache from true.
- Set backup\_limit from Platform.get\_system\_settings(“backup\_limit”).
- Set backups\_path from Path(get\_site\_path(“private”, “backups”)).
- Set backup\_files from list of tuple((“/backups/” + nested operand in the contract.relative\_to(backups\_path).as\_posix()), get\_time(x), get\_encrytion\_status(x), get\_size(x)) for x drawn from backups\_path.iterdir() where (x.is\_fil ….
  - Draw x from backups\_path.iterdir(), keep a combination only if ((x.is\_file() and x.name.endswith(“sql.gz”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in x.is\_file() → x.name.endswith(“sql.gz”).
- Evaluate backup\_files.sort(key = deferred anonymous expression, reverse = true).
- Return mapping(“files” → backup\_files at slice no value to backup\_limit).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“backup\_limit”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L6621) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L327)

<a id="op-6f2b415d933236"></a>
### Cleanup old backups

`operation_foundation_desk_page_backups_business_behavior_cleanup_old_backups`

**Inputs** backups, limit.

**Local steps**

- Set backups\_to\_delete from (len(backups) − limit).
- If backups\_to\_delete &gt; 0.
  - Set backups from dict(sorted(backups.items(), key = deferred anonymous expression, reverse = true)).
  - For each b\_files in list(backups.values()) at slice negative backups\_to\_delete to no value.
    - For each b\_file in b\_files.
      - Evaluate b\_file.unlink().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L7027) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L325)

<a id="op-f46431734f9460"></a>
### Delete downloadable backups

`operation_foundation_desk_page_backups_business_behavior_delete_downloadable_backups`

**Inputs** no declared parameters.

**Local steps**

- Set path from Path(get\_site\_path(“private”, “backups”)).
- Set backups from defaultdict(list).
- For each x in path.iterdir().
  - If not x.is\_file().
    - Continue with the next iteration or loop test.
  - Set backup\_name from x.name.rsplit((“-” + nested operand in the contract.local.site.replace(“.”, “\_”)), maxsplit = 1) at 0.
  - Evaluate backups at backup\_name.append(x).
- Set backup\_limit from Platform.get\_system\_settings(“backup\_limit”).
- Evaluate cleanup\_old\_backups(backups, backup\_limit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“backup\_limit”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L326)

<a id="op-274e98b5126975"></a>
### Schedule files backup

`operation_foundation_desk_page_backups_business_behavior_schedule_files_backup`

**Inputs** user\_email.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Queued for backup. You will receive an email with the download link” · msgprint with translated “Backup job is already queued. You will receive an email with the download link”.

**Local steps**

- Bind dependencies enqueue, get\_jobs.
- Evaluate Platform.only\_for(“System Manager”).
- Set queued\_jobs from get\_jobs(site = Platform.local.site, queue = “long”).
- Set method from “Platform.desk.page.backups.backups.backup\_files\_and\_notify\_user”.
- If method does not belong to queued\_jobs at Platform.local.site.
  - Evaluate enqueue(“Platform.desk.page.backups.backups.backup\_files\_and\_notify\_user”, queue = “long”, user\_email = user\_email).
  - Evaluate Platform.msgprint(translated “Queued for backup. You will receive an email with the download link”).
- Otherwise.
  - Evaluate Platform.msgprint(translated “Backup job is already queued. You will receive an email with the download link”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · service or queued work from enqueue(“Platform.desk.page.backups.backups.backup\_files\_and\_notify\_user”, queue = “long”, user\_email = user\_email).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L334) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L332)

<a id="op-32d53ace08cbf6"></a>
### Backup files and notify user

`operation_foundation_desk_page_backups_business_behavior_backup_files_and_notify_user`

**Inputs** user\_email = no value.

**State and service calls** sendmail.

**Local steps**

- Bind dependencies backup.
- Set backup\_files from backup(with\_files = true).
- Evaluate get\_downloadable\_links(backup\_files).
- Set subject from translated “File backup is ready”.
- Evaluate Platform.sendmail(recipients = list(user\_email), subject = subject, template = “file\_backup\_notification”, args = backup\_files, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = list(user\_email), subject = subject, template = “file\_backup\_notification”, args = backup\_files, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L762) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L324)

<a id="op-304154f5bf5116"></a>
### Get downloadable links

`operation_foundation_desk_page_backups_business_behavior_get_downloadable_links`

**Inputs** backup\_files.

**Local steps**

- For each key in list(“backup\_path\_files”, “backup\_path\_private\_files”).
  - Set path from backup\_files at key.
  - Set backup\_files at key from get\_url(“/”.join(path.split(“/”) at slice negative 2 to no value)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L963) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L328)

## Service · Billing

<a id="op-887484c4860735"></a>
### Get context

`operation_foundation_public_pages_billing_business_behavior_get_context`

**Inputs** context.

**State and service calls** commit.

**Explicit results** context.

**Local steps**

- Evaluate Platform.db.commit().
- Set context from Platform.\_dict().
- Set context.boot from get\_boot().
- Return context.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L2611) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L28)
