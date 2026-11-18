# Record lifecycle and persistence · operations 103

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User permission

[Record definition](../../../../data/record-types/user_permission.json)

<a id="op-ac775c6532554f"></a>
### User permission exists

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_exists`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, allow, for\_value, applicable\_for.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L4361) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L798)

<a id="op-a5bf606aec7ed8"></a>
### Get applicable for doctype list

`operation_foundation_core_record_definitions_user_permission_business_behavior_get_applicable_for_record_type_list`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, txt, searchfield, start, page\_len, filters.

**Explicit result forms** a structured result.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L4583) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L788)

<a id="op-e9f440185f7068"></a>
### Get permitted documents

`operation_foundation_core_record_definitions_user_permission_business_behavior_get_permitted_documents`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L5085) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L790)

<a id="op-494fae6a2cffa3"></a>
### Check applicable doc perm

`operation_foundation_core_record_definitions_user_permission_business_behavior_check_applicable_record_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype, docname.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L5284) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L786)

<a id="op-8a00053699764c"></a>
### Clear user permissions

`operation_foundation_core_record_definitions_user_permission_business_behavior_clear_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, for\_doctype.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L5761) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L787)

<a id="op-65b95367324fde"></a>
### Get user permission list

`operation_foundation_binding_foundation_core_doctype_user_permission_user_permission_get_user_permission_list`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** allow, txt, start, page\_length.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L641)

<a id="op-b0a83c898ab4b9"></a>
### Add user permissions

`operation_foundation_core_record_definitions_user_permission_business_behavior_add_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** data.

**Explicit result forms** a scalar literal.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L6032) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L785)

<a id="op-1b3b0a1ed27cdb"></a>
### Insert user perm

`operation_foundation_core_record_definitions_user_permission_business_behavior_insert_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype, docname, is\_default, hide\_descendants, apply\_to\_all, applicable.

**Observed service boundaries** record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L6906) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L793)

<a id="op-e3ce679ad928c5"></a>
### Remove applicable

`operation_foundation_core_record_definitions_user_permission_business_behavior_remove_applicable`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** perm\_applied\_docs, user, doctype, docname.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L7192) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L794)

<a id="op-d53c011772de5e"></a>
### Remove apply to all

`operation_foundation_core_record_definitions_user_permission_business_behavior_remove_apply_to_all`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype, docname.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L7360) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L795)

<a id="op-4101398ecb6209"></a>
### Update applicable

`operation_foundation_core_record_definitions_user_permission_business_behavior_update_applicable`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** already\_applied, to\_apply, user, doctype, docname.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L797)

## Record · User session display

[Record definition](../../../../data/record-types/user_session_display.json)

<a id="op-cdc658d9f94e64"></a>
### User Session Display.db insert

`operation_foundation_core_record_definitions_user_session_display_business_behavior_user_session_display_database_insert`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, args, kwargs.

**Locally raised failures** NotImplementedError.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L203) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L819)

<a id="op-e6f10c2ca859ba"></a>
### User Session Display.load from db

`operation_foundation_core_record_definitions_user_session_display_business_behavior_user_session_display_load_from_database`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, args, kwargs.

**Locally raised failures** NotImplementedError.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L255) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L822)

<a id="op-1a22416b4a523c"></a>
### User Session Display.db update

`operation_foundation_core_record_definitions_user_session_display_business_behavior_user_session_display_database_update`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, args, kwargs.

**Locally raised failures** NotImplementedError.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L307) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L820)

<a id="op-622aeeb43138be"></a>
### User Session Display.delete

`operation_foundation_core_record_definitions_user_session_display_business_behavior_user_session_display_delete`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, args, kwargs.

**Locally raised failures** NotImplementedError.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L359) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L821)

## Service · User settings

<a id="op-b077a13ec8613a"></a>
### Get user settings

`operation_foundation_model_utils_user_settings_business_behavior_get_user_settings`

**Inputs** doctype, for\_update = false.

**Record and data access** execute query text (SELECT).

**Explicit results** (user\_settings or “{}”).

**Local steps**

- Set user\_settings from Platform.cache.hget(“\_user\_settings”, formatted text {doctype}::{Platform.session.user}).
- If user\_settings is identical to no value.
  - Set user\_settings from Platform.db.sql(query text (SELECT), tuple(Platform.session.user, doctype)).
  - Set user\_settings from ((user\_settings and user\_settings at 0 at 0) or “{}”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (user\_settings and user\_settings at 0 at 0) → “{}”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user\_settings → user\_settings at 0 at 0.
  - If not for\_update.
    - Evaluate update\_user\_settings(doctype, user\_settings, true).
- Return (user\_settings or “{}”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_settings → “{}”.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L3970) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1336)

<a id="op-bc0aac42f5ebd5"></a>
### Update user settings

`operation_foundation_model_utils_user_settings_business_behavior_update_user_settings`

**Inputs** doctype, user\_settings, for\_update = false.

**Local steps**

- If for\_update.
  - Set current from json.loads(user\_settings).
- Otherwise.
  - Set current from json.loads(get\_user\_settings(doctype, for\_update = true)).
  - If isinstance(current, str).
    - Set current from mapping().
  - Evaluate current.update(user\_settings).
- Evaluate Platform.cache.hset(“\_user\_settings”, formatted text {doctype}::{Platform.session.user}, json.dumps(current)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L4312) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1339)

<a id="op-d8baa14325d965"></a>
### Clear user settings cache

`operation_foundation_model_utils_user_settings_business_behavior_clear_user_settings_cache`

**Inputs** doctype.

**Local steps**

- Set prefix from formatted text {doctype}::.
- Set keys from list of decoded for key drawn from Platform.cache.hkeys(“\_user\_settings”) where decoded bound to safe\_decode(key).startswith(prefix).
  - Draw key from Platform.cache.hkeys(“\_user\_settings”), keep a combination only if (decoded bound to safe\_decode(key).startswith(prefix)).
- If keys.
  - Evaluate Platform.cache.hdel(“\_user\_settings”, keys).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L4603) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1334)

<a id="op-035fa4d6750007"></a>
### Sync user settings

`operation_foundation_model_utils_user_settings_business_behavior_sync_user_settings`

**Inputs** no declared parameters.

**Local steps**

- For each tuple(key, data) in Platform.cache.hgetall(“\_user\_settings”).items().
  - Set key from safe\_decode(key).
  - Set tuple(doctype, user) from key.split(“::”).
  - Evaluate Platform.db.multisql(mapping(“mariadb” → query text (INSERT), “\*” → query text (INSERT)), tuple(user, doctype, data, data), as\_dict = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L4803) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1338)

<a id="op-533372fb956885"></a>
### Save

`operation_foundation_model_utils_user_settings_business_behavior_save`

**Inputs** doctype, user\_settings.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** user\_settings.

**Local steps**

- Set user\_settings from json.loads((user\_settings or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_settings → “{}”.
- Evaluate update\_user\_settings(doctype, user\_settings).
- Return user\_settings.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L17) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1337)

<a id="op-0a732dabb99f58"></a>
### Get

`operation_foundation_model_utils_user_settings_business_behavior_get`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_user\_settings(doctype).

**Local steps**

- Return get\_user\_settings(doctype).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L5357) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1335)

<a id="op-bfbb48d4ce5aa5"></a>
### Update user settings data

`operation_foundation_model_utils_user_settings_business_behavior_update_user_settings_data`

**Inputs** user\_setting, fieldname, old, new, condition\_fieldname = no value, condition\_values = no value.

**State and service calls** execute query text (UPDATE).

**Local steps**

- Set data from user\_setting.get(“data”).
- If data.
  - Set update from false.
  - Set data from json.loads(data).
  - For each view in list(“List”, “Gantt”, “Kanban”, “Calendar”, …).
    - Set view\_settings from data.get(view).
    - If (view\_settings and view\_settings.get(“filters”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in view\_settings → view\_settings.get(“filters”).
      - Set view\_filters from view\_settings.get(“filters”).
      - For each view\_filter in view\_filters.
        - If (condition\_fieldname and view\_filter at filter\_dict at condition\_fieldname differs from condition\_values).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in condition\_fieldname → view\_filter at filter\_dict at condition\_fieldname differs from condition\_values.
          - Continue with the next iteration or loop test.
        - If view\_filter at filter\_dict at fieldname equals old.
          - Set view\_filter at filter\_dict at fieldname from new.
          - Set update from true.
  - If update.
    - Evaluate Platform.db.sql(query text (UPDATE), tuple(json.dumps(data), user\_setting.doctype, user\_setting.user)).
    - Evaluate Platform.cache.hset(“\_user\_settings”, formatted text {user\_setting.doctype}::{user\_setting.user}, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L5432) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1340)

## Record · User social login

[Record definition](../../../../data/record-types/user_social_login.json)

<a id="op-ade38294771212"></a>
### User Social Login.validate

`operation_foundation_binding_foundation_core_doctype_user_social_login_user_social_login_usersociallogin_validate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L643)

<a id="op-839e3ad66310ca"></a>
### User Social Login.disallow Platform userid change

`operation_foundation_binding_foundation_core_doctype_user_social_login_user_social_login_usersociallogin_disallow_foundation_userid_change`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L642)
