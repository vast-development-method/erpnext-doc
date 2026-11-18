# Record lifecycle and persistence · operations 102

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User invitation

[Record definition](../../../../data/record-types/user_invitation.json)

<a id="op-8eee35d8482886"></a>
### User Invitation.validate role

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_validate_role`

**Inputs** app\_name.

**Wrappers, in declaration order** staticmethod.

**Declared result** no value.

**Local steps**

- Evaluate UserInvitation.validate\_app\_name(app\_name).
- Set user\_invitation\_hook from Platform.get\_hooks(“user\_invitation”, app\_name = app\_name).
- Set only\_for from list().
- If isinstance(user\_invitation\_hook, dict).
  - Set only\_for from list((user\_invitation\_hook.get(“allowed\_roles”) or dict()).keys()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_invitation\_hook.get(“allowed\_roles”) → dict().
- Evaluate Platform.only\_for(only\_for).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_invitation”, app\_name = app\_name) · effective access from Platform.only\_for(only\_for).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L2038) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L762)

<a id="op-2a7fd707ef3f57"></a>
### Mark expired invitations

`operation_foundation_core_record_definitions_user_invitation_business_behavior_mark_expired_invitations`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read “User Invitation” via get\_all · resolve a document from “User Invitation” via get\_doc.

**State and service calls** commit.

**Local steps**

- Set days from INVITATION\_EXPIRY\_DAYS.
- Set invitations\_to\_expire from Platform.db.get\_all(“User Invitation”, filters = mapping(“status” → “Pending”, “creation” → list(“&lt;”, Platform.utils.add\_days(nested operand in the contract.utils.now(), negative days)))).
- For each invitation in invitations\_to\_expire.
  - Set invitation from Platform.get\_doc(“User Invitation”, invitation.name).
  - Evaluate invitation.expire().
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L65) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L745)

<a id="op-00531dbc9b7eb3"></a>
### Get allowed apps

`operation_foundation_core_record_definitions_user_invitation_business_behavior_get_allowed_apps`

**Inputs** user.

**Declared result** list at str.

**Explicit results** allowed\_apps.

**Local steps**

- Set user\_roles from set(get\_user\_roles(user)).
- Set allowed\_apps from list().
- For each app in Platform.get\_installed\_apps().
  - Set user\_invitation\_hooks from Platform.get\_hooks(“user\_invitation”, app\_name = app).
  - If not isinstance(user\_invitation\_hooks, dict).
    - Continue with the next iteration or loop test.
  - Set only\_for from list((user\_invitation\_hooks.get(“allowed\_roles”) or dict()).keys()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_invitation\_hooks.get(“allowed\_roles”) → dict().
  - If (set(only\_for) bitwise and user\_roles).
    - Evaluate allowed\_apps.append(app).
- Return allowed\_apps.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_invitation”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L64) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L740)

<a id="op-0366437a9dbe02"></a>
### Get permission query conditions

`operation_foundation_core_record_definitions_user_invitation_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L2840) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L741)

<a id="op-9521ca03b30ea7"></a>
### Has permission

`operation_foundation_core_record_definitions_user_invitation_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user, permission\_type.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L3119) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L744)

<a id="op-08b104e4f49638"></a>
### Get user roles

`operation_foundation_core_record_definitions_user_invitation_business_behavior_get_user_roles`

**Inputs** user.

**Declared result** list at str.

**Explicit results** get\_roles(get\_user(user)).

**Local steps**

- Return get\_roles(get\_user(user)).

**Values supplied outside this operation** effective access from get\_roles(get\_user(user)).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L3269) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L743)

<a id="op-42b2a749db6fd5"></a>
### Get user

`operation_foundation_core_record_definitions_user_invitation_business_behavior_get_user`

**Inputs** user.

**Declared result** Document.

**Explicit results** (user or Platform.session.user).

**Local steps**

- Return (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L3360) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L742)

## Service · User invitation

<a id="op-851d885fcb1465"></a>
### Invite by email

`operation_foundation_core_application_interface_user_invitation_business_behavior_invite_by_email`

**Inputs** emails, roles, redirect\_to\_path, app\_name = “Platform”, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, list at str).

**Record and data access** read “User” via get\_all · read “User Invitation” via get\_all · resolve a document from “User Invitation” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “User Invitation”, email = email, roles = list of dict(role = role) for role drawn from roles, app\_name = app\_name, …).

**Explicit results** mapping(“disabled\_user\_emails” → disabled\_user\_emails, “accepted\_invite\_emails” → accepted\_invite\_emails, “pending\_invite\_emails” → pending\_invite\_emails, “invited\_emails” → to\_invite).

**Explicit failure paths** validation helper.

**Local steps**

- Evaluate UserInvitation.validate\_role(app\_name).
- Evaluate Platform.utils.validate\_email\_address(emails, throw = true).
- Set email\_list from Platform.utils.split\_emails(emails).
- If not email\_list.
  - Call the validation error handler Platform.throw(title = translated “Invalid input”, msg = translated “No email addresses to invite”).
- Set disabled\_user\_emails from Platform.db.get\_all(“User”, filters = mapping(“email” → list(“in”, email\_list), “enabled” → 0), pluck = “email”).
- Set accepted\_invite\_emails from Platform.db.get\_all(“User Invitation”, filters = mapping(“email” → list(“in”, email\_list), “status” → “Accepted”, “app\_name” → app\_name, “user” → list(“is”, “set”)), pluck = “email”).
- Set pending\_invite\_emails from Platform.db.get\_all(“User Invitation”, filters = mapping(“email” → list(“in”, email\_list), “status” → “Pending”, “app\_name” → app\_name), pluck = “email”).
- Set to\_invite from list((((set(email\_list) − set(disabled\_user\_emails)) − set(accepted\_invite\_emails)) − set(pending\_invite\_emails))).
- Set extra\_args from get\_allowed\_invite\_params(app\_name, kwargs).
- For each email in to\_invite.
  - Evaluate Platform.get\_doc(doctype = “User Invitation”, email = email, roles = list of dict(role = role) for role drawn from roles, app\_name = app\_name, …).insert(ignore\_permissions = true).
    - Draw role from roles.
- Return mapping(“disabled\_user\_emails” → disabled\_user\_emails, “accepted\_invite\_emails” → accepted\_invite\_emails, “pending\_invite\_emails” → pending\_invite\_emails, “invited\_emails” → to\_invite).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L2161) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L911)

<a id="op-3a10674f47e910"></a>
### Get allowed invite params

`operation_foundation_core_application_interface_user_invitation_business_behavior_get_allowed_invite_parameters`

**Inputs** app\_name, kwargs.

**Declared result** dict.

**Explicit results** mapping() · allowed\_params.

**Local steps**

- Set allowed\_params from Platform.\_dict().
- Set user\_invitation\_hook from Platform.get\_hooks(“user\_invitation”, app\_name = app\_name).
- If not isinstance(user\_invitation\_hook, dict).
  - Return mapping().
- Set extra\_invite\_params from user\_invitation\_hook.get(“extra\_invite\_params”, list()).
- For each param in extra\_invite\_params.
  - If param belongs to kwargs.
    - Set allowed\_params at param from kwargs at param.
- Return allowed\_params.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_invitation”, app\_name = app\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L3174) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L909)

<a id="op-b9a5bbf3af9980"></a>
### Accept invitation

`operation_foundation_core_application_interface_user_invitation_business_behavior_accept_invitation`

**Inputs** key.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“GET”)).

**Declared result** no value.

**Local steps**

- Evaluate \_accept\_invitation(key, false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L3428) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L906)

<a id="op-dd598e21a5ab6b"></a>
### Cancel invitation

`operation_foundation_core_application_interface_user_invitation_business_behavior_cancel_invitation`

**Inputs** name, app\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“PATCH”, “POST”)).

**Record and data access** read “User Invitation” via exists · resolve a document from “User Invitation” via get\_doc.

**Explicit results** mapping(“cancelled\_now” → false) · mapping(“cancelled\_now” → invitation.cancel\_invite()).

**Explicit failure paths** validation helper.

**Local steps**

- Evaluate UserInvitation.validate\_role(app\_name).
- If not Platform.db.exists(“User Invitation”, name).
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation not found”).
- Set invitation from Platform.get\_doc(“User Invitation”, name).
- If invitation.app\_name differs from app\_name.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation not found”).
- If invitation.status equals “Cancelled”.
  - Return mapping(“cancelled\_now” → false).
- If invitation.status differs from “Pending”.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation cannot be cancelled”).
- Set invitation.flags.ignore\_permissions from true.
- Return mapping(“cancelled\_now” → invitation.cancel\_invite()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L3530) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L908)

<a id="op-1ea1542012c25b"></a>
### Resend invitation

`operation_foundation_core_application_interface_user_invitation_business_behavior_resend_invitation`

**Inputs** name, app\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** read “User Invitation” via exists · resolve a document from “User Invitation” via get\_doc.

**Explicit failure paths** validation helper.

**Local steps**

- Evaluate UserInvitation.validate\_role(app\_name).
- If not Platform.db.exists(“User Invitation”, name).
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation not found”).
- Set invitation from Platform.get\_doc(“User Invitation”, name).
- If invitation.app\_name differs from app\_name.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation not found”).
- If invitation.status differs from “Pending”.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Only pending invitations can be resent”).
- Evaluate invitation.send\_invitation\_mail().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L4056) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L912)

<a id="op-f5b183ff3e16d8"></a>
### Get pending invitations

`operation_foundation_core_application_interface_user_invitation_business_behavior_get_pending_invitations`

**Inputs** app\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** read “User Invitation” via get\_all · read “User Role” via get\_all.

**Explicit results** res.

**Local steps**

- Evaluate UserInvitation.validate\_role(app\_name).
- Set pending\_invitations from Platform.db.get\_all(“User Invitation”, fields = list(“name”, “email”), filters = mapping(“status” → “Pending”, “app\_name” → app\_name)).
- Set res from list().
- For each pending\_invitation in pending\_invitations.
  - Set roles from Platform.db.get\_all(“User Role”, fields = list(“role”), filters = mapping(“parent” → pending\_invitation.name)).
  - Evaluate res.append(mapping(“name” → pending\_invitation.name, “email” → pending\_invitation.email, “roles” → list of r.role for r drawn from roles)).
    - Draw r from roles.
- Return res.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L4500) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L910)

<a id="op-667227cf878e59"></a>
### Accept invitation

`operation_foundation_core_application_interface_user_invitation_business_behavior_accept_invitation_2`

**Inputs** key, in\_test.

**Declared result** no value.

**Record and data access** read “User Invitation” via get\_value · resolve a document from “User Invitation” via get\_doc · resolve a document from “User” via get\_doc.

**State and service calls** commit.

**Explicit failure paths** validation helper.

**Local steps**

- Set hashed\_key from Platform.utils.sha256\_hash(key).
- Set invitation\_name from Platform.db.get\_value(“User Invitation”, filters = mapping(“key” → hashed\_key)).
- If not invitation\_name.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invalid or expired key”).
- Set invitation from Platform.get\_doc(“User Invitation”, invitation\_name).
- Evaluate invitation.accept(ignore\_permissions = true).
- Set user from Platform.get\_doc(“User”, invitation.email).
- Set should\_update\_password from (not user.last\_password\_reset\_date and not bool(Platform.get\_system\_settings(“disable\_user\_pass\_login”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not user.last\_password\_reset\_date → not bool(Platform.get\_system\_settings(“disable\_user\_pass\_login”)).
- Set redirect\_to from Platform.utils.get\_url(invitation.get\_redirect\_to\_path()).
- If should\_update\_password.
  - Set redirect\_to from formatted text {user.\_reset\_password()}&amp;redirect\_to=/{invitation.get\_redirect\_to\_path()}.
- Evaluate Platform.db.commit().
- If (not in\_test and not should\_update\_password).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not in\_test → not should\_update\_password.
  - Evaluate Platform.local.login\_manager.login\_as(invitation.email).
- Set Platform.local.response at “type” from “redirect”.
- Set Platform.local.response at “location” from redirect\_to.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“disable\_user\_pass\_login”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L4927) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L907)

## Record · User permission

[Record definition](../../../../data/record-types/user_permission.json)

<a id="op-b82116dad25a1c"></a>
### User Permission.validate

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_validate`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L2074) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L802)

<a id="op-55a3a6c002151a"></a>
### User Permission.on update

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_on_update`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** notification or queued-work request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L2145) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L801)

<a id="op-bcd0332db1203f"></a>
### User Permission.on trash

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_on_trash`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** notification or queued-work request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L2257) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L800)

<a id="op-3c2bd418416b3f"></a>
### User Permission.validate user permission

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_validate_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L2369) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L804)

<a id="op-f534ac639626f7"></a>
### User Permission.validate default permission

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_validate_default_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L2657) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L803)

<a id="op-42433a3dcdfea0"></a>
### User Permission.get permission log options

`operation_foundation_core_record_definitions_user_permission_business_behavior_user_permission_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L3043) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L799)

<a id="op-7523c121a8a832"></a>
### Send user permissions

`operation_foundation_core_record_definitions_user_permission_business_behavior_send_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** bootinfo.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L3086) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L796)

<a id="op-01c58425795ea4"></a>
### Get current user permissions

`operation_foundation_core_record_definitions_user_permission_business_behavior_get_current_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L3150) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L789)

<a id="op-8fddb37c486f29"></a>
### Get user permissions

`operation_foundation_core_record_definitions_user_permission_business_behavior_get_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a structured result, a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 6 condition or selection sites, 2 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L67) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L791)

<a id="op-d473a164d6b534"></a>
### Get user permissions.add doc to perm

`operation_foundation_core_record_definitions_user_permission_business_behavior_get_user_permissions_add_record_to_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** perm, doc\_name, is\_default, hide\_descendants.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0116.json#L4120) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L792)
