# Forms, reports and navigation · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Notification log

[Record definition](../../../../data/record-types/notification_log.json)

<a id="op-34ea8dbd3466f0"></a>
### Enqueue create notification

`operation_foundation_desk_record_definitions_notification_log_business_behavior_enqueue_create_notification`

**Inputs** users, doc, dedupe\_on = no value.

**State and service calls** enqueue with “Platform.desk.doctype.notification\_log.notification\_log.make\_notification\_logs”.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install.
  - Return no value.
- Set doc from Platform.\_dict(doc).
- If dedupe\_on.
  - Set doc.dedupe\_on from dedupe\_on.
- If isinstance(users, str).
  - Set users from list of user.strip() for user drawn from users.split(“,”) where user.strip().
    - Draw user from users.split(“,”), keep a combination only if (user.strip()).
- Set users from list(set(users)).
- Evaluate Platform.enqueue(“Platform.desk.doctype.notification\_log.notification\_log.make\_notification\_logs”, doc = doc, users = users, now = Platform.in\_test, enqueue\_after\_commit = not Platform.in\_test).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.desk.doctype.notification\_log.notification\_log.make\_notification\_logs”, doc = doc, users = users, now = Platform.in\_test, enqueue\_after\_commit = not Platform.in\_test).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L7182) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L896)

<a id="op-cb5d3801f65170"></a>
### Make notification logs

`operation_foundation_desk_record_definitions_notification_log_business_behavior_make_notification_logs`

**Inputs** doc, users.

**State and service calls** request new\_doc for “Notification Log” · call insert on notification.

**Local steps**

- Set dedupe\_on from doc.pop(“dedupe\_on”, no value) when isinstance(doc, dict), otherwise no value.
  - Value choice on isinstance(doc, dict) — true gives doc.pop(“dedupe\_on”, no value), false gives no value.
- Set self\_notify\_types from get\_self\_notify\_types().
- For each user in \_get\_user\_ids(users).
  - If (dedupe\_on and \_notification\_exists(doc, user, dedupe\_on)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dedupe\_on → \_notification\_exists(doc, user, dedupe\_on).
    - Continue with the next iteration or loop test.
  - Set notification from Platform.new\_doc(“Notification Log”).
  - Evaluate notification.update(doc).
  - Set notification.for\_user from user.
  - If (notification.for\_user differs from notification.from\_user or doc.type belongs to self\_notify\_types).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in notification.for\_user differs from notification.from\_user → doc.type belongs to self\_notify\_types.
    - Evaluate notification.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L907)

<a id="op-9f16e3ab478387"></a>
### Notification exists

`operation_foundation_desk_record_definitions_notification_log_business_behavior_notification_exists`

**Inputs** doc, user, dedupe\_on.

**Declared result** bool.

**Record and data access** read “Notification Log” via exists.

**Explicit results** bool(Platform.db.exists(“Notification Log”, filters)).

**Local steps**

- Set filters from mapping(“for\_user” → user).
- For each fieldname in dedupe\_on.
  - Set filters at fieldname from doc.get(fieldname).
- Return bool(Platform.db.exists(“Notification Log”, filters)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L357) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L910)

<a id="op-3f7c5e3f42d087"></a>
### Get user ids

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_user_identifiers`

**Inputs** user\_emails.

**Record and data access** read “User” via get\_values.

**Explicit results** list of user for user drawn from user\_names where is\_notifications\_enabled(user).

**Local steps**

- Set user\_names from Platform.db.get\_values(“User”, mapping(“enabled” → 1, “email” → tuple(“in”, user\_emails)), “name”, pluck = true).
- Return list of user for user drawn from user\_names where is\_notifications\_enabled(user).
  - Draw user from user\_names, keep a combination only if (is\_notifications\_enabled(user)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L533) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L905)

<a id="op-c66d2a15c5caa1"></a>
### Send notification email

`operation_foundation_desk_record_definitions_notification_log_business_behavior_send_notification_email`

**Inputs** doc.

**Record and data access** read “User” via get\_value.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_url\_to\_form, strip\_html.
- Set user from Platform.db.get\_value(“User”, doc.for\_user, fieldname = list(“email”, “language”), as\_dict = true).
- If not user.
  - Return no value.
- Set header from get\_email\_header(doc, user.language).
- Set email\_subject from strip\_html(doc.subject).
- Set args from mapping(“body\_content” → doc.subject, “description” → doc.email\_content).
- If doc.link.
  - Set args at “doc\_link” from doc.link.
- Otherwise.
  - If (doc.document\_type and doc.document\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.document\_type → doc.document\_name.
    - Set args at “document\_type” from doc.document\_type.
    - Set args at “document\_name” from doc.document\_name.
    - Set args at “doc\_link” from get\_url\_to\_form(doc.document\_type, doc.document\_name).
- Evaluate Platform.sendmail(recipients = user.email, subject = email\_subject, template = “new\_notification”, args = args, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = user.email, subject = email\_subject, template = “new\_notification”, args = args, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L712) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L915)

<a id="op-4a055f32e83464"></a>
### Get email header

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_email_header`

**Inputs** doc, language = no value.

**Explicit results** doc.email\_header.

**Local steps**

- Set docname from doc.document\_name.
- Set header\_map from mapping(“Default” → \_(“New Notification”, lang = language), “Mention” → \_(“New Mention on {0}”, lang = language).format(docname), “Assignment” → \_(“Assignment Update on {0}”, lang = language).format(docnam ….
- If not doc.email\_header.
  - Set doc.email\_header from header\_map.get((doc.type or “Default”), header\_map at “Default”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.type → “Default”.
- Return doc.email\_header.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L1239) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L898)

<a id="op-7edf04c3797f94"></a>
### Format email header

`operation_foundation_desk_record_definitions_notification_log_business_behavior_format_email_header`

**Inputs** header\_map, language, docname.

**Explicit results** dict(zip(header\_map.keys(), messages, strict = true)).

**Local steps**

- Set messages from list().
- For each v in list(header\_map.values()).
  - Evaluate messages.append(\_(v at 0, lang = language).format(docname)).
- Return dict(zip(header\_map.keys(), messages, strict = true)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L1599) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L897)

<a id="op-35fa4e31286796"></a>
### Get notification logs

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_notification_logs`

**Inputs** limit = 20, read = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Notification Log” via get\_list.

**Explicit results** mapping(“notification\_logs” → notification\_logs, “user\_info” → user\_info).

**Local steps**

- Set filters from mapping(“for\_user” → Platform.session.user).
- If read is distinct from no value.
  - Set filters at “read” from read.
- Set notification\_logs from Platform.db.get\_list(“Notification Log”, fields = list(“\*”), filters = filters, limit = limit, order\_by = “creation desc”).
- Set users from list of log.from\_user for log drawn from notification\_logs.
  - Draw log from notification\_logs.
- Set users from list(expanded set(users)).
- Set user\_info from Platform.\_dict().
- For each user in users.
  - Evaluate Platform.utils.add\_user\_info(user, user\_info).
- Return mapping(“notification\_logs” → notification\_logs, “user\_info” → user\_info).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L20) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L899)

<a id="op-26e01f43938a9f"></a>
### Mark all as read

`operation_foundation_desk_record_definitions_notification_log_business_behavior_mark_all_as_read`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Notification Log”.

**Local steps**

- Evaluate Platform.db.set\_value(“Notification Log”, mapping(“read” → 0, “for\_user” → Platform.session.user), “read”, 1, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L2165) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L908)

<a id="op-8f7097521001a4"></a>
### Mark as read

`operation_foundation_desk_record_definitions_notification_log_business_behavior_mark_as_read`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Notification Log”.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.read\_only or not docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.read\_only → not docname.
  - Return no value.
- Evaluate Platform.db.set\_value(“Notification Log”, mapping(“name” → str(docname), “for\_user” → Platform.session.user, “read” → 0), “read”, 1, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L2307) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L909)

<a id="op-c32dbb1f648b43"></a>
### Trigger indicator hide

`operation_foundation_desk_record_definitions_notification_log_business_behavior_trigger_indicator_hide`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** publish realtime with “indicator\_hide”.

**Local steps**

- Evaluate Platform.publish\_realtime(“indicator\_hide”, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“indicator\_hide”, user = Platform.session.user).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L2528) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L917)

<a id="op-1121cc8787e1e6"></a>
### Set notifications as unseen

`operation_foundation_desk_record_definitions_notification_log_business_behavior_set_notifications_as_unseen`

**Inputs** user.

**State and service calls** request set\_value on “Notification Settings”.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Evaluate Platform.db.set\_value(“Notification Settings”, user, “seen”, 0, update\_modified = false).
- On failure (Platform.DoesNotExistError).
  - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0178.json#L2611) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L916)

## Record · Notification settings

[Record definition](../../../../data/record-types/notification_settings.json)

<a id="op-c4426ff1da2821"></a>
### Notification Settings.on update

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_notification_settings_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_notification\_config.
- Evaluate clear\_notification\_config(Platform.session.user).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L945)

<a id="op-60aa53461f2b8e"></a>
### Is notifications enabled

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_is_notifications_enabled`

**Inputs** user.

**Record and data access** read “Notification Settings” via get\_value.

**Explicit results** true · enabled.

**Local steps**

- Set enabled from Platform.db.get\_value(“Notification Settings”, user, “enabled”).
- If enabled is identical to no value.
  - Return true.
- Return enabled.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L74) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L944)

<a id="op-c6fb41f76c791a"></a>
### Is email notifications enabled

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_is_email_notifications_enabled`

**Inputs** user.

**Record and data access** read “Notification Settings” via get\_value.

**Explicit results** true · enabled.

**Local steps**

- Set enabled from Platform.db.get\_value(“Notification Settings”, user, “enable\_email\_notifications”).
- If enabled is identical to no value.
  - Return true.
- Return enabled.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L191) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L942)

<a id="op-b00acf268aa17d"></a>
### Is email enabled for feature

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_is_email_enabled_for_feature`

**Inputs** user, fieldname.

**Record and data access** read “Notification Settings” via get\_value.

**Explicit results** false · true when enabled is identical to no value, otherwise enabled.

**Local steps**

- If not is\_email\_notifications\_enabled(user).
  - Return false.
- Set enabled from Platform.db.get\_value(“Notification Settings”, user, fieldname, ignore = true).
- Return true when enabled is identical to no value, otherwise enabled.
  - Value choice on enabled is identical to no value — true gives true, false gives enabled.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L308) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L941)

<a id="op-dfe6746589c23c"></a>
### Is email notifications enabled for type

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_is_email_notifications_enabled_for_type`

**Inputs** user, notification\_type.

**Record and data access** resolve a document from “Notification Settings” via get\_cached\_doc.

**Explicit results** false · true · any(generator of row.notification\_type equals notification\_type for row drawn from settings.email\_notification\_types).

**Local steps**

- Bind dependencies get\_skip\_email\_types.
- If not is\_email\_notifications\_enabled(user).
  - Return false.
- If notification\_type belongs to get\_skip\_email\_types().
  - Return false.
- Attempt the following.
  - Set settings from Platform.get\_cached\_doc(“Notification Settings”, user).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return true.
- Return any(generator of row.notification\_type equals notification\_type for row drawn from settings.email\_notification\_types).
  - Draw row from settings.email\_notification\_types.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Notification Settings”, user).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L467) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L943)

<a id="op-475a5d855d7c04"></a>
### Create notification settings

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_create_notification_settings`

**Inputs** user.

**Record and data access** read “Notification Settings” via exists.

**State and service calls** request new\_doc for “Notification Settings” · call insert on \_doc.

**Local steps**

- If not Platform.db.exists(“Notification Settings”, user).
  - Set \_doc from Platform.new\_doc(“Notification Settings”).
  - Set \_doc.name from user.
  - For each notification\_type in get\_default\_email\_notification\_types().
    - Evaluate \_doc.append(“email\_notification\_types”, mapping(“notification\_type” → notification\_type)).
  - Evaluate \_doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L733) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L935)

<a id="op-c3b22ee59db2ab"></a>
### Get default email notification types

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_get_default_email_notification_types`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Notification Type” via get\_all.

**Explicit results** list of name for name drawn from Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), pluck = “name”) where name does not belong to skip.

**Local steps**

- Bind dependencies get\_skip\_email\_types.
- Set skip from get\_skip\_email\_types().
- Return list of name for name drawn from Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), pluck = “name”) where name does not belong to skip.
  - Draw name from Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), pluck = “name”), keep a combination only if (name does not belong to skip).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L962) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L936)

<a id="op-d67ac82fe7dd51"></a>
### Get emailable notification types

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_get_emailable_notification_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Record and data access** read “Notification Type” via get\_all.

**Explicit results** Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), pluck = “name”).

**Local steps**

- Evaluate Platform.only\_for(list(“Desk User”, “System Manager”)).
- Return Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), pluck = “name”).

**Values supplied outside this operation** effective access from Platform.only\_for(list(“Desk User”, “System Manager”)).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L21) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L937)

<a id="op-34f69b2206bf3b"></a>
### Toggle notifications

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_toggle_notifications`

**Inputs** user, enable = false, ignore\_permissions = false.

**Record and data access** resolve a document from “Notification Settings” via get\_doc.

**State and service calls** call save on settings.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set settings from Platform.get\_doc(“Notification Settings”, user).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return no value.
- If settings.enabled differs from enable.
  - Set settings.enabled from enable.
  - Evaluate settings.save(ignore\_permissions = ignore\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L1258) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L947)

<a id="op-60051e045a5c83"></a>
### Get subscribed documents

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_get_subscribed_documents`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Notification Settings” via exists · resolve a document from “Notification Settings” via get\_doc.

**Explicit results** list() · list of item.document for item drawn from doc.subscribed\_documents.

**Local steps**

- If not Platform.session.user.
  - Return list().
- Attempt the following.
  - If Platform.db.exists(“Notification Settings”, Platform.session.user).
    - Set doc from Platform.get\_doc(“Notification Settings”, Platform.session.user).
    - Return list of item.document for item drawn from doc.subscribed\_documents.
      - Draw item from doc.subscribed\_documents.
- On failure (ImportError).
  - Take no action here.
- Return list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L1481) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L939)

<a id="op-59e9759d00f678"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context, no value.

**Observed service boundaries** effective access lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L1708) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L938)

<a id="op-3e4eba9c446c2a"></a>
### Has permission

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, a comparison result.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L1910) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L940)
