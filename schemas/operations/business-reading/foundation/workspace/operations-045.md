# Forms, reports and navigation · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Notification settings

[Record definition](../../../../data/record-types/notification_settings.json)

<a id="op-d18d18908144a6"></a>
### Set seen value

`operation_foundation_desk_record_definitions_notification_settings_business_behavior_set_seen_value`

**Inputs** value, user.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Notification Settings”.

**Explicit results** no value.

**Local steps**

- If Platform.flags.read\_only.
  - Return no value.
- Evaluate Platform.db.set\_value(“Notification Settings”, Platform.session.user, “seen”, value, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L2117) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L946)

## Record · Notification type

[Record definition](../../../../data/record-types/notification_type.json)

<a id="op-32b847730f4729"></a>
### Notification Type.on trash

`operation_foundation_desk_record_definitions_notification_type_business_behavior_notification_type_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is a built-in Notification Type and cannot be deleted. Disable it instead.”.format(Platform.bold(self.name)).

**Local steps**

- If (self.name belongs to BUILTIN\_TYPE\_NAMES and not Platform.flags.in\_migrate and not Platform.flags.in\_patch).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.name belongs to BUILTIN\_TYPE\_NAMES → not Platform.flags.in\_migrate → not Platform.flags.in\_patch.
  - Call the validation error handler Platform.throw(translated “{0} is a built-in Notification Type and cannot be deleted. Disable it instead.”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L3152) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L957)

<a id="op-2e32ba004628d3"></a>
### Install notification types

`operation_foundation_desk_record_definitions_notification_type_business_behavior_install_notification_types`

**Inputs** no declared parameters.

**Record and data access** read “Notification Type” via exists.

**State and service calls** request new\_doc for “Notification Type” · call insert on doc.

**Local steps**

- For each definition in BUILTIN\_NOTIFICATION\_TYPES.
  - If Platform.db.exists(“Notification Type”, definition at “type\_name”).
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(“Notification Type”).
  - Evaluate doc.update(definition).
  - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L3329) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L956)

<a id="op-62515b1ad13f32"></a>
### Get notification types

`operation_foundation_desk_record_definitions_notification_type_business_behavior_get_notification_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = 300, stale\_while\_revalidate = (60 × 60)).

**Record and data access** read “Notification Type” via get\_all.

**Explicit results** Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), fields = list(“name”, “type\_name”, “enabled”)).

**Local steps**

- Evaluate Platform.only\_for(list(“Desk User”, “System Manager”)).
- Return Platform.get\_all(“Notification Type”, filters = mapping(“enabled” → 1), fields = list(“name”, “type\_name”, “enabled”)).

**Values supplied outside this operation** effective access from Platform.only\_for(list(“Desk User”, “System Manager”)).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L22) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L955)

<a id="op-8f2bfb9fd5e084"></a>
### Enable email for all users

`operation_foundation_desk_record_definitions_notification_type_business_behavior_enable_email_for_all_users`

**Inputs** notification\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Notification Type” via exists · read “Notification Type” via get\_value.

**State and service calls** enqueue with “Platform.desk.doctype.notification\_type.notification\_type.seed\_type\_into\_settings” · msgprint with translated “Enabling email for {0} across all users in the background.”.format(Platform.bold(notification\_type)).

**Explicit failure paths** validation helper — translated “{0} does not exist”.format(Platform.bold(notification\_type)) · validation helper — translated “Enable the notification type before emailing it to users.” · validation helper — translated “{0} never sends email, so it cannot be enabled for users.”.format(notification\_type).

**Local steps**

- Bind dependencies get\_skip\_email\_types.
- Evaluate Platform.only\_for(“System Manager”).
- If not Platform.db.exists(“Notification Type”, notification\_type).
  - Call the validation error handler Platform.throw(translated “{0} does not exist”.format(Platform.bold(notification\_type))).
- If not Platform.db.get\_value(“Notification Type”, notification\_type, “enabled”).
  - Call the validation error handler Platform.throw(translated “Enable the notification type before emailing it to users.”).
- If notification\_type belongs to get\_skip\_email\_types().
  - Call the validation error handler Platform.throw(translated “{0} never sends email, so it cannot be enabled for users.”.format(notification\_type)).
- Evaluate Platform.enqueue(“Platform.desk.doctype.notification\_type.notification\_type.seed\_type\_into\_settings”, notification\_type = notification\_type, enqueue\_after\_commit = true).
- Evaluate Platform.msgprint(translated “Enabling email for {0} across all users in the background.”.format(Platform.bold(notification\_type)), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · service or queued work from Platform.enqueue(“Platform.desk.doctype.notification\_type.notification\_type.seed\_type\_into\_settings”, notification\_type = notification\_type, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L3683) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L954)

<a id="op-c53eee356312da"></a>
### Seed type into settings

`operation_foundation_desk_record_definitions_notification_type_business_behavior_seed_type_into_settings`

**Inputs** notification\_type.

**Record and data access** read “Notification Type” via exists · read “Notification Settings” via get\_all · read “Notification Type Preference” via exists · resolve a document from “Notification Settings” via get\_doc.

**State and service calls** call save on settings.

**Explicit results** no value.

**Local steps**

- If not Platform.db.exists(“Notification Type”, notification\_type).
  - Return no value.
- Set settings\_names from Platform.get\_all(“Notification Settings”, pluck = “name”).
- For each name in settings\_names.
  - Set exists from Platform.db.exists(“Notification Type Preference”, mapping(“parent” → name, “notification\_type” → notification\_type)).
  - If exists.
    - Continue with the next iteration or loop test.
  - Set settings from Platform.get\_doc(“Notification Settings”, name).
  - Evaluate settings.append(“email\_notification\_types”, mapping(“notification\_type” → notification\_type)).
  - Evaluate settings.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L4243) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L958)

## Service · Notifications

<a id="op-8d7a97defcbeaf"></a>
### Get notifications

`operation_foundation_desk_notifications_business_behavior_get_notifications`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** out.

**Local steps**

- Set out from mapping(“open\_count\_doctype” → mapping(), “targets” → mapping()).
- If (Platform.flags.in\_install or not Platform.is\_setup\_complete()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → not Platform.is\_setup\_complete().
  - Return out.
- Set config from get\_notification\_config().
- If not config.
  - Return out.
- Set groups from (list(config.get(“for\_doctype”)) + list(config.get(“for\_module”))).
- Set notification\_count from mapping().
- Set notification\_percent from mapping().
- For each name in groups.
  - Set count from Platform.cache.hget((“notification\_count:” + name), Platform.session.user).
  - If count is distinct from no value.
    - Set notification\_count at name from count.
- Set out at “open\_count\_doctype” from get\_notifications\_for\_doctypes(config, notification\_count).
- Set out at “targets” from get\_notifications\_for\_targets(config, notification\_percent).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L5122) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L317)

<a id="op-1581a21a0073d8"></a>
### Get notifications for doctypes

`operation_foundation_desk_notifications_business_behavior_get_notifications_for_record_types`

**Inputs** config, notification\_count.

**Record and data access** read d via get\_list.

**Explicit results** open\_count\_doctype.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set can\_read from Platform.get\_user().get\_can\_read().
- Set open\_count\_doctype from mapping().
- For each d in config.for\_doctype.
  - If d belongs to can\_read.
    - Set condition from config.for\_doctype at d.
    - If d belongs to notification\_count.
      - Set open\_count\_doctype at d from notification\_count at d.
    - Otherwise.
      - Attempt the following.
        - If isinstance(condition, dict).
          - Set result from Platform.get\_list(d, fields = list(mapping(“COUNT” → “\*”, “as” → “count”)), filters = condition, ignore\_ifnull = true) at 0.count.
        - Otherwise.
          - Set result from Platform.get\_attr(condition)().
      - On failure (Platform.PermissionError).
        - Evaluate Platform.clear\_messages().
        - Take no action here.
      - On failure (Exception) bound to e.
        - If (e.args and e.args at 0 does not belong to tuple(1412, 1684)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 does not belong to tuple(1412, 1684).
          - Propagate the active failure.
      - When the protected block completes normally.
        - Set open\_count\_doctype at d from result.
        - Evaluate Platform.cache.hset((“notification\_count:” + d), Platform.session.user, result).
- Return open\_count\_doctype.

**Values supplied outside this operation** selected callable from Platform.get\_attr(condition).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L5620) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L318)

<a id="op-22de385005d5a2"></a>
### Get notifications for targets

`operation_foundation_desk_notifications_business_behavior_get_notifications_for_targets`

**Inputs** config, notification\_percent.

**Record and data access** read doctype via get\_list.

**Explicit results** doc\_target\_percents.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set can\_read from Platform.get\_user().get\_can\_read().
- Set doc\_target\_percents from mapping().
- For each doctype in config.targets.
  - If doctype belongs to can\_read.
    - If doctype belongs to notification\_percent.
      - Set doc\_target\_percents at doctype from notification\_percent at doctype.
    - Otherwise.
      - Set doc\_target\_percents at doctype from mapping().
      - Set d from config.targets at doctype.
      - Set condition from d at “filters”.
      - Set target\_field from d at “target\_field”.
      - Set value\_field from d at “value\_field”.
      - Attempt the following.
        - If isinstance(condition, dict).
          - Set doc\_list from Platform.get\_list(doctype, fields = list(“name”, target\_field, value\_field), filters = condition, limit\_page\_length = 100, ignore\_ifnull = true).
      - On failure (Platform.PermissionError).
        - Evaluate Platform.clear\_messages().
        - Take no action here.
      - On failure (Exception) bound to e.
        - If e.args at 0 does not belong to tuple(1412, 1684).
          - Propagate the active failure.
      - When the protected block completes normally.
        - For each doc in doc\_list.
          - Set value from doc at value\_field.
          - Set target from doc at target\_field.
          - Set doc\_target\_percents at doctype at doc.name from ((value ÷ target) × 100) when value &lt; target, otherwise 100.
            - Value choice on value &lt; target — true gives ((value ÷ target) × 100), false gives 100.
- Return doc\_target\_percents.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L6193) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L319)

<a id="op-7165c782351723"></a>
### Clear notifications

`operation_foundation_desk_notifications_business_behavior_clear_notifications`

**Inputs** user = no value.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install.
  - Return no value.
- Set config from get\_notification\_config().
- If not config.
  - Return no value.
- Set for\_doctype from list(config.get(“for\_doctype”)) when config.get(“for\_doctype”), otherwise list().
  - Value choice on config.get(“for\_doctype”) — true gives list(config.get(“for\_doctype”)), false gives list().
- Set for\_module from list(config.get(“for\_module”)) when config.get(“for\_module”), otherwise list().
  - Value choice on config.get(“for\_module”) — true gives list(config.get(“for\_module”)), false gives list().
- Set groups from (for\_doctype + for\_module).
- If user.
  - Evaluate Platform.cache.hdel\_names(list of formatted text notification\_count:{name} for name drawn from groups, user).
    - Draw name from groups.
- Otherwise.
  - Evaluate Platform.cache.delete\_value(list of formatted text notification\_count:{name} for name drawn from groups).
    - Draw name from groups.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L6839) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L302)

<a id="op-bed8d8d1c7146e"></a>
### Clear notification config

`operation_foundation_desk_notifications_business_behavior_clear_notification_configuration`

**Inputs** user.

**Local steps**

- Evaluate Platform.cache.hdel(“notification\_config”, user).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L7240) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L301)

<a id="op-e4c343e77d2ffd"></a>
### Delete notification count for

`operation_foundation_desk_notifications_business_behavior_delete_notification_count_for`

**Inputs** doctype.

**Local steps**

- Evaluate Platform.cache.delete\_key((“notification\_count:” + doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L7302) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L304)

<a id="op-73e7e1687af4a7"></a>
### Clear doctype notifications

`operation_foundation_desk_notifications_business_behavior_clear_record_type_notifications`

**Inputs** doc, method = no value, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set config from get\_notification\_config().
- If not config.
  - Return no value.
- If isinstance(doc, str).
  - Set doctype from doc.
- Otherwise.
  - Set doctype from doc.doctype.
- If doctype belongs to config.for\_doctype.
  - Evaluate delete\_notification\_count\_for(doctype).
  - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L7368) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L303)

<a id="op-85c2360bda3e79"></a>
### Get notification info

`operation_foundation_desk_notifications_business_behavior_get_notification_info`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Doc Type).

**Explicit results** out.

**Local steps**

- Set config from get\_notification\_config().
- Set out from get\_notifications().
- Set can\_read from Platform.get\_user().get\_can\_read().
- Set conditions from mapping().
- Set module\_doctypes from mapping().
- Set doctype\_info from dict(Platform.db.sql(query text (SELECT, Doc Type))).
- For each d in list(set((can\_read + list(config.for\_doctype)))).
  - If d belongs to config.for\_doctype.
    - Set conditions at d from config.for\_doctype at d.
  - If d belongs to doctype\_info.
    - Evaluate module\_doctypes.setdefault(doctype\_info at d, list()).append(d).
- Evaluate out.update(mapping(“conditions” → conditions, “module\_doctypes” → module\_doctypes)).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L316)

<a id="op-3f59edaed015be"></a>
### Get notification config

`operation_foundation_desk_notifications_business_behavior_get_notification_configuration`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.hget(“notification\_config”, user, \_get).

**Local steps**

- Set user from (Platform.session.user or “Guest”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.session.user → “Guest”.
- Bind local operation \_get for subsequent calls.
- Return Platform.cache.hget(“notification\_config”, user, \_get).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L475) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L314)

<a id="op-81f8042c412cd9"></a>
### Get notification config.get

`operation_foundation_desk_notifications_business_behavior_get_notification_configuration_get`

**Inputs** no declared parameters.

**Explicit results** config.

**Local steps**

- Set subscribed\_documents from get\_subscribed\_documents().
- Set config from Platform.\_dict().
- Set hooks from Platform.get\_hooks().
- If hooks.
  - For each notification\_config in hooks.notification\_config.
    - Set nc from Platform.get\_attr(notification\_config)().
    - For each key in tuple(“for\_doctype”, “for\_module”, “for\_other”, “targets”).
      - Evaluate config.setdefault(key, mapping()).
      - If key equals “for\_doctype”.
        - If len(subscribed\_documents) &gt; 0.
          - Set key\_config from nc.get(key, mapping()).
          - Set subscribed\_docs\_config from Platform.\_dict().
          - For each document in subscribed\_documents.
            - If key\_config.get(document).
              - Set subscribed\_docs\_config at document from key\_config.get(document).
          - Evaluate config at key.update(subscribed\_docs\_config).
        - Otherwise.
          - Evaluate config at key.update(nc.get(key, mapping())).
      - Otherwise.
        - Evaluate config at key.update(nc.get(key, mapping())).
- Return config.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(), Platform.get\_attr(notification\_config).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L1108) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L315)

<a id="op-65e89a31c7ea70"></a>
### Get filters for

`operation_foundation_desk_notifications_business_behavior_get_filters_for`

**Inputs** doctype.

**Explicit results** no value when isinstance(doctype\_config, str), otherwise doctype\_config.

**Local steps**

- Set config from get\_notification\_config().
- Set doctype\_config from config.get(“for\_doctype”).get(doctype, mapping()).
- Return no value when isinstance(doctype\_config, str), otherwise doctype\_config.
  - Value choice on isinstance(doctype\_config, str) — true gives no value, false gives doctype\_config.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L1666) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L311)

<a id="op-29baa5f39713ca"></a>
### Get open count

`operation_foundation_desk_notifications_business_behavior_get_open_count`

**Inputs** doctype, name, items = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** mapping(“count” → list()) · \_get\_linked\_document\_counts(doctype, name, items).

**Explicit failure paths** propagate active failure.

**Local steps**

- If (Platform.flags.in\_migrate or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_install.
  - Return mapping(“count” → list()).
- Attempt the following.
  - Within Platform.db.execution\_timeout(1).
    - Return \_get\_linked\_document\_counts(doctype, name, items).
- On failure (Exception) bound to e.
  - If Platform.db.is\_statement\_timeout(e).
    - Return mapping(“count” → list()).
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L81) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L320)

<a id="op-21d762ec58ea4f"></a>
### Get linked document counts

`operation_foundation_desk_notifications_business_behavior_get_linked_document_counts`

**Inputs** doctype, name, items = no value.

**Explicit results** out.

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name, check\_permission = true).
- Set meta from doc.meta.
- Set links from meta.get\_dashboard\_data().
- If items is identical to no value.
  - Set items from list().
  - For each group in links.transactions.
    - Evaluate items.extend(group.get(“items”)).
- If not isinstance(items, list).
  - Set items from json.loads(items).
- Set out from mapping(“external\_links\_found” → list(), “internal\_links\_found” → list()).
- For each d in unique(items).
  - Set internal\_link\_for\_doctype from (links.get(“internal\_links”, mapping()).get(d) or links.get(“internal\_and\_external\_links”, mapping()).get(d)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in links.get(“internal\_links”, mapping()).get(d) → links.get(“internal\_and\_external\_links”, mapping()).get(d).
  - If internal\_link\_for\_doctype.
    - Set internal\_links\_data\_for\_d from get\_internal\_links(doc, internal\_link\_for\_doctype, d).
    - If internal\_links\_data\_for\_d at “count”.
      - Evaluate out at “internal\_links\_found”.append(internal\_links\_data\_for\_d).
    - Otherwise.
      - If has\_external\_link\_field(d, links).
        - For each fieldname in get\_external\_link\_fieldnames(d, links).
          - Evaluate out at “external\_links\_found”.append(get\_external\_links(d, name, links, fieldname)).
      - Otherwise.
        - Evaluate out at “external\_links\_found”.append(mapping(“doctype” → d, “open\_count” → 0, “count” → 0)).
  - Otherwise.
    - For each fieldname in get\_external\_link\_fieldnames(d, links).
      - Evaluate out at “external\_links\_found”.append(get\_external\_links(d, name, links, fieldname)).
- Set out from mapping(“count” → out).
- If not meta.custom.
  - Set module from Platform.get\_meta\_module(doctype).
  - If hasattr(module, “get\_timeline\_data”).
    - Set out at “timeline\_data” from module.get\_timeline\_data(doctype, name).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L80) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L313)

<a id="op-137e525a2227b2"></a>
### Get internal links

`operation_foundation_desk_notifications_business_behavior_get_internal_links`

**Inputs** doc, link, link\_doctype.

**Explicit results** data.

**Local steps**

- Set names from list().
- Set data from mapping(“doctype” → link\_doctype).
- If isinstance(link, str).
  - Set value from doc.get(link).
  - If (value and value does not belong to names).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → value does not belong to names.
    - Evaluate names.append(value).
- Otherwise.
  - If isinstance(link, list).
    - Set tuple(table\_fieldname, link\_fieldname) from link.
    - For each row in (doc.get(table\_fieldname) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(table\_fieldname) → list().
      - Set value from row.get(link\_fieldname).
      - If (value and value does not belong to names).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → value does not belong to names.
        - Evaluate names.append(value).
- Set data at “open\_count” from 0.
- Set data at “count” from len(names).
- Set data at “names” from names.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L3055) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L312)

<a id="op-feaf50316f5d48"></a>
### Get external link fieldname

`operation_foundation_desk_notifications_business_behavior_get_external_link_fieldname`

**Inputs** doctype, links.

**Explicit results** links.get(“non\_standard\_fieldnames”, mapping()).get(doctype, links.get(“fieldname”)).

**Local steps**

- Return links.get(“non\_standard\_fieldnames”, mapping()).get(doctype, links.get(“fieldname”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L3508) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L308)

<a id="op-80a785d4b371e0"></a>
### Get external link fieldnames

`operation_foundation_binding_foundation_desk_notifications_get_external_link_fieldnames`

**Inputs** doctype, links.

**Explicit results** (unique(list of (nested operand in the contract(nested operand in the contract, nested operand in the contract).get(doctype) or group.get(“fieldname”) or default\_fieldname) for group drawn from links.trans ….

**Local steps**

- Set default\_fieldname from get\_external\_link\_fieldname(doctype, links).
- Return (unique(list of (nested operand in the contract(nested operand in the contract, nested operand in the contract).get(doctype) or group.get(“fieldname”) or default\_fieldname) for group drawn from links.trans ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in unique(list of (nested operand in the contract.get(“fieldnames”, mapping()).get(doctype) or group.get(“fieldname”) or default\_fieldname) for group drawn from links.transactions where doctype belongs to gro … → list(default\_fieldname).
  - Draw group from links.transactions, keep a combination only if (doctype belongs to group at “items”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in group.get(“fieldnames”, mapping()).get(doctype) → group.get(“fieldname”) → default\_fieldname.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L792)

<a id="op-767799e7fac3ff"></a>
### Has external link field

`operation_foundation_desk_notifications_business_behavior_has_external_link_field`

**Inputs** doctype, links.

**Explicit results** false · (Platform.get\_meta(doctype).has\_field(fieldname) or bool(get\_child\_doctypes\_with\_field(doctype, fieldname))).

**Local steps**

- Set fieldname from get\_external\_link\_fieldname(doctype, links).
- If not fieldname.
  - Return false.
- Return (Platform.get\_meta(doctype).has\_field(fieldname) or bool(get\_child\_doctypes\_with\_field(doctype, fieldname))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_meta(doctype).has\_field(fieldname) → bool(get\_child\_doctypes\_with\_field(doctype, fieldname)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L3613) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L322)

<a id="op-c17e4c3ab978c3"></a>
### Get child doctypes with field

`operation_foundation_desk_notifications_business_behavior_get_child_record_types_with_field`

**Inputs** doctype, fieldname.

**Explicit results** list() · list of df.options for df drawn from meta.get\_table\_fields() where Platform.get\_meta(df.options).has\_field(fieldname).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If meta.has\_field(fieldname).
  - Return list().
- Return list of df.options for df drawn from meta.get\_table\_fields() where Platform.get\_meta(df.options).has\_field(fieldname).
  - Draw df from meta.get\_table\_fields(), keep a combination only if (Platform.get\_meta(df.options).has\_field(fieldname)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L3783) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L306)
