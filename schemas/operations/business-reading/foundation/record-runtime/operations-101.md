# Record lifecycle and persistence · operations 101

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · User doctype permissions

<a id="op-178a5b33c23313"></a>
### Execute

`operation_foundation_core_report_user_record_type_permissions_business_behavior_execute`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** filters.

**Explicit result forms** a structured result.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L4495) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L910)

<a id="op-3ba59088752999"></a>
### Get columns

`operation_foundation_core_report_user_record_type_permissions_business_behavior_get_columns`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L68) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L912)

<a id="op-f8cca61bef03fb"></a>
### Get data

`operation_foundation_core_report_user_record_type_permissions_business_behavior_get_data`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** filters.

**Explicit result forms** a value selected from the current context.

**Local structure** 4 condition or selection sites, 4 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L5193) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L913)

<a id="op-2db351191aed27"></a>
### Get all user roles

`operation_foundation_core_report_user_record_type_permissions_business_behavior_get_all_user_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L6031) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L911)

<a id="op-36fb085d82f747"></a>
### Get perm types

`operation_foundation_core_report_user_record_type_permissions_business_behavior_get_permission_types`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L6326) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L914)

## Record · User group

[Record definition](../../../../data/record-types/user_group.json)

<a id="op-c2d23389731d3d"></a>
### User Group.after insert

`operation_foundation_core_record_definitions_user_group_business_behavior_user_group_after_insert`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_key(“user\_groups”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L6029) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L738)

<a id="op-d4edcfa27669ad"></a>
### User Group.on trash

`operation_foundation_core_record_definitions_user_group_business_behavior_user_group_on_trash`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_key(“user\_groups”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L6087) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L739)

## Record · User invitation

[Record definition](../../../../data/record-types/user_invitation.json)

<a id="op-c932edd9a89961"></a>
### User Invitation.before insert

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.\_validate\_invite().
- Set self.invited\_by from Platform.session.user.
- Set self.status from “Pending”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate invite](operations-101.md#op-cfc3251916096a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L5407) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L749)

<a id="op-a377eded7fb9ed"></a>
### User Invitation.after insert

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.send\_invitation\_mail().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send invitation mail](operations-101.md#op-39b4b0e4859149).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L5500) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L748)

<a id="op-3f81ed69d1a39c"></a>
### User Invitation.accept

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_accept`

**Inputs** self, ignore\_permissions = false.

**State and service calls** call save on self · call save on user.

**Local steps**

- Evaluate self.\_accept().
- Set tuple(user, user\_inserted) from self.\_upsert\_user(ignore\_permissions).
- Evaluate self.save(ignore\_permissions).
- Evaluate user.save(ignore\_permissions).
- Evaluate self.\_run\_after\_accept\_hooks(user, user\_inserted).

If control reaches the end, it returns no value.

**Methods declared on this owner** [accept](operations-101.md#op-671fd169d02f0a), [upsert user](operations-101.md#op-34952aff23c853), [run after accept hooks](operations-101.md#op-8d2c356ec57181).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L5551) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L746)

<a id="op-f8717ca3745e61"></a>
### User Invitation.cancel invite

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_cancel_invite`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self · sendmail.

**Explicit results** false · true.

**Local steps**

- If self.status differs from “Pending”.
  - Return false.
- Set self.status from “Cancelled”.
- Evaluate self.save().
- Set email\_title from self.\_get\_email\_title().
- Evaluate Platform.sendmail(recipients = self.email, subject = translated “Invitation to join {0} cancelled”.format(email\_title), template = “user\_invitation\_cancelled”, args = mapping(“title” → email\_title), …).
- Return true.

**Methods declared on this owner** [get email title](operations-101.md#op-a9212faf29b21b).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.email, subject = translated “Invitation to join {0} cancelled”.format(email\_title), template = “user\_invitation\_cancelled”, args = mapping(“title” → email\_title), …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L5734) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L750)

<a id="op-b5bf1cc5012ce9"></a>
### User Invitation.expire

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_expire`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self · sendmail.

**Explicit results** no value.

**Local steps**

- If self.status differs from “Pending”.
  - Return no value.
- Set self.status from “Expired”.
- Evaluate self.save().
- Set email\_title from self.\_get\_email\_title().
- Evaluate Platform.sendmail(recipients = self.email, subject = translated “Invitation to join {0} expired”.format(email\_title), template = “user\_invitation\_expired”, args = mapping(“title” → email\_title), …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get email title](operations-101.md#op-a9212faf29b21b).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.email, subject = translated “Invitation to join {0} expired”.format(email\_title), template = “user\_invitation\_expired”, args = mapping(“title” → email\_title), …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L6016) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L751)

<a id="op-cfc3251916096a"></a>
### User Invitation.validate invite

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_validate_invite`

**Inputs** self.

**Record and data access** read “User Invitation” via get\_value · read “User” via get\_value.

**Explicit failure paths** validation helper.

**Local steps**

- Evaluate self.\_validate\_app\_name().
- Evaluate self.\_validate\_roles().
- Evaluate self.\_validate\_email().
- If Platform.db.get\_value(“User Invitation”, filters = mapping(“email” → self.email, “status” → “Accepted”, “app\_name” → self.app\_name, “user” → list(“is”, “set”))).
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation already accepted”).
- If Platform.db.get\_value(“User Invitation”, filters = mapping(“email” → self.email, “status” → “Pending”, “app\_name” → self.app\_name)).
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation already exists”).
- Set user\_enabled from Platform.db.get\_value(“User”, self.email, “enabled”).
- If (user\_enabled is distinct from no value and user\_enabled equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user\_enabled is distinct from no value → user\_enabled equals 0.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “User is disabled”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate app name](operations-101.md#op-a89738d3a10f4f), [validate roles](operations-101.md#op-34ed4b8837a542), [validate email](operations-101.md#op-d2c2521edaf633).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L6290) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L761)

<a id="op-39b4b0e4859149"></a>
### User Invitation.send invitation mail

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_send_invitation_mail`

**Inputs** self.

**State and service calls** call db\_set on self · sendmail.

**Explicit results** key.

**Local steps**

- Set key from Platform.generate\_hash().
- Evaluate self.db\_set(“key”, Platform.utils.sha256\_hash(key)).
- Set invite\_link from Platform.utils.get\_url(formatted text /api/method/Platform.core.api.user\_invitation.accept\_invitation?key={key}).
- Set email\_title from self.\_get\_email\_title().
- Evaluate Platform.sendmail(recipients = self.email, subject = translated “You've been invited to join {0}”.format(email\_title), template = “user\_invitation”, args = mapping(“title” → email\_title, “invite\_link” → in ….
- Evaluate self.db\_set(“email\_sent\_at”, Platform.utils.now()).
- Return key.

**Methods declared on this owner** [get email title](operations-101.md#op-a9212faf29b21b).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(), Platform.utils.now() · service or queued work from Platform.sendmail(recipients = self.email, subject = translated “You've been invited to join {0}”.format(email\_title), template = “user\_invitation”, args = mapping(“title” → email\_title, “invite\_link” → in ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0114.json#L6899) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L756)

<a id="op-671fd169d02f0a"></a>
### User Invitation.accept

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_accept_2`

**Inputs** self.

**Explicit results** true.

**Explicit failure paths** validation helper.

**Local steps**

- If self.status equals “Accepted”.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation already accepted”).
- If self.status equals “Expired”.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation is expired”).
- If self.status equals “Cancelled”.
  - Call the validation error handler Platform.throw(title = translated “Error”, msg = translated “Invitation is cancelled”).
- Set self.status from “Accepted”.
- Set self.accepted\_at from Platform.utils.now().
- Set self.user from self.email.
- Set self.key from no value.
- Return true.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L747)

<a id="op-34952aff23c853"></a>
### User Invitation.upsert user

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_upsert_user`

**Inputs** self, ignore\_permissions = false.

**Record and data access** read “User” via exists · resolve a document from “User” via get\_doc.

**State and service calls** request new\_doc for “User” · call insert on user.

**Explicit results** tuple(user, user\_inserted).

**Local steps**

- Set user from no value.
- Set user\_inserted from false.
- If Platform.db.exists(“User”, self.user).
  - Set user from Platform.get\_doc(“User”, self.user).
- Otherwise.
  - Set user from Platform.new\_doc(“User”).
  - Set user.user\_type from “System User”.
  - Set user.email from self.email.
  - Set user.first\_name from self.email.split(“@”) at 0.title().
  - Set user.send\_welcome\_email from false.
  - Evaluate user.insert(ignore\_permissions).
  - Set user\_inserted from true.
- Evaluate user.append\_roles(expanded list of r.role for r drawn from self.roles).
  - Draw r from self.roles.
- Return tuple(user, user\_inserted).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L397) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L757)

<a id="op-8d2c356ec57181"></a>
### User Invitation.run after accept hooks

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_run_after_accept_hooks`

**Inputs** self, user, user\_inserted.

**Explicit results** no value.

**Local steps**

- Set user\_invitation\_hook from Platform.get\_hooks(“user\_invitation”, app\_name = self.app\_name).
- If not isinstance(user\_invitation\_hook, dict).
  - Return no value.
- For each dot\_path in (user\_invitation\_hook.get(“after\_accept”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_invitation\_hook.get(“after\_accept”) → list().
  - Evaluate Platform.call(dot\_path, invitation = self, user = user, user\_inserted = user\_inserted).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_invitation”, app\_name = self.app\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L803) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L755)

<a id="op-a9212faf29b21b"></a>
### User Invitation.get email title

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_get_email_title`

**Inputs** self.

**Explicit results** Platform.get\_hooks(“app\_title”, app\_name = self.app\_name) at 0.

**Local steps**

- Return Platform.get\_hooks(“app\_title”, app\_name = self.app\_name) at 0.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = self.app\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L1031) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L753)

<a id="op-a89738d3a10f4f"></a>
### User Invitation.validate app name

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_validate_application_name`

**Inputs** self.

**Local steps**

- Evaluate UserInvitation.validate\_app\_name(self.app\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L1108) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L758)

<a id="op-d8fdd1ddff9aca"></a>
### User Invitation.get allowed roles

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_get_allowed_roles`

**Inputs** self.

**Explicit results** list() · list(res).

**Local steps**

- Set user\_invitation\_hook from Platform.get\_hooks(“user\_invitation”, app\_name = self.app\_name).
- If not isinstance(user\_invitation\_hook, dict).
  - Return list().
- Set res from set at str().
- Set allowed\_roles\_mp from (user\_invitation\_hook.get(“allowed\_roles”) or dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_invitation\_hook.get(“allowed\_roles”) → dict().
- Set only\_for from set(allowed\_roles\_mp.keys()).
- For each role in (only\_for bitwise and set(Platform.get\_roles())).
  - Evaluate res.update(allowed\_roles\_mp at role).
- Return list(res).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_invitation”, app\_name = self.app\_name) · effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L1170) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L752)

<a id="op-34ed4b8837a542"></a>
### User Invitation.validate roles

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_validate_roles`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- If self.app\_name equals “Platform”.
  - Return no value.
- Set allowed\_roles from self.\_get\_allowed\_roles().
- For each r in self.roles.
  - If r.role belongs to allowed\_roles.
    - Continue with the next iteration or loop test.
  - Call the validation error handler Platform.throw(title = translated “Invalid role”, msg = translated “{0} is not an allowed role for {1}”.format(r.role, self.app\_name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get allowed roles](operations-101.md#op-d8fdd1ddff9aca).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L1491) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L763)

<a id="op-d2c2521edaf633"></a>
### User Invitation.validate email

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_validate_email`

**Inputs** self.

**Local steps**

- Evaluate Platform.utils.validate\_email\_address(self.email, throw = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L1725) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L760)

<a id="op-7ad6ae0734cff5"></a>
### User Invitation.get redirect to path

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_get_redirect_to_path`

**Inputs** self.

**Explicit results** self.redirect\_to\_path at slice start\_index to no value.

**Local steps**

- Set start\_index from 1 when self.redirect\_to\_path.startswith(“/”), otherwise 0.
  - Value choice on self.redirect\_to\_path.startswith(“/”) — true gives 1, false gives 0.
- Return self.redirect\_to\_path at slice start\_index to no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0115.json#L1797) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L754)

<a id="op-d2159174d4c00a"></a>
### User Invitation.validate app name

`operation_foundation_core_record_definitions_user_invitation_business_behavior_user_invitation_validate_application_name_2`

**Inputs** app\_name.

**Wrappers, in declaration order** staticmethod.

**Explicit failure paths** validation helper.

**Local steps**

- If app\_name does not belong to Platform.get\_installed\_apps().
  - Call the validation error handler Platform.throw(title = translated “Invalid app”, msg = translated “Application is not installed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L66) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L759)
