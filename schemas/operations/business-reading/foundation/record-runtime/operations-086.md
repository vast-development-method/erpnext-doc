# Record lifecycle and persistence · operations 86

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Report

[Record definition](../../../../data/record-types/report.json)

<a id="op-0cedf92f09f977"></a>
### Get group by field

`operation_foundation_core_record_definitions_report_business_behavior_get_group_by_field`

**Inputs** args, doctype.

**Explicit results** group\_by\_field.

**Local steps**

- If args at “aggregate\_function” equals “count”.
  - Set group\_by\_field from mapping(“COUNT” → “\*”, “as” → “\_aggregate\_column”).
- Otherwise.
  - Set func\_name from args at “aggregate\_function”.upper().
  - Set group\_by\_field from mapping(func\_name → args at “aggregate\_on”, “as” → “\_aggregate\_column”).
- Return group\_by\_field.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L15) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L377)

<a id="op-bb9685f144bf96"></a>
### Get group by column label

`operation_foundation_binding_foundation_core_doctype_report_report_get_group_by_column_label`

**Inputs** args, meta.

**Explicit results** label.

**Local steps**

- If args at “aggregate\_function” equals “count”.
  - Set label from “Count”.
- Otherwise.
  - Set sql\_fn\_map from mapping(“avg” → “Average”, “sum” → “Sum”).
  - Set aggregate\_on\_label from meta.get\_label(args.aggregate\_on).
  - Set label from translated “{0} of {1}”.format(translated sql\_fn\_map at args.aggregate\_function, translated aggregate\_on\_label).
- Return label.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L639)

<a id="op-7a7a724a1f15c8"></a>
### Enable prepared report

`operation_foundation_core_record_definitions_report_business_behavior_enable_prepared_report`

**Inputs** report, site.

**State and service calls** request set\_value on “Report” · commit.

**Local steps**

- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Evaluate Platform.db.set\_value(“Report”, report, “prepared\_report”, 1).
- Evaluate Platform.db.commit().
- Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0098.json#L1924) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L376)

## Record · Role

[Record definition](../../../../data/record-types/role.json)

<a id="op-5e517d44f250eb"></a>
### Role.before rename

`operation_foundation_core_record_definitions_role_business_behavior_role_before_rename`

**Inputs** self, old, new, merge = false.

**Explicit failure paths** validation helper — Platform.\_(“Standard roles cannot be renamed”).

**Local steps**

- If old belongs to STANDARD\_ROLES.
  - Call the validation error handler Platform.throw(Platform.\_(“Standard roles cannot be renamed”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6343) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L433)

<a id="op-b65dcdc70af279"></a>
### Role.after insert

`operation_foundation_core_record_definitions_role_business_behavior_role_after_insert`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.hdel(“roles”, “Administrator”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6464) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L432)

<a id="op-7068e107435de2"></a>
### Role.validate

`operation_foundation_core_record_definitions_role_business_behavior_role_validate`

**Inputs** self.

**Local steps**

- If self.disabled.
  - Evaluate self.disable\_role().
- Otherwise.
  - Evaluate self.set\_desk\_properties().
- Evaluate self.validate\_homepage().

If control reaches the end, it returns no value.

**Methods declared on this owner** [disable role](operations-086.md#op-765b5239a2c84e), [set desk properties](operations-086.md#op-4357a549f41fb0), [validate homepage](operations-086.md#op-eeca1069092e45).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6531) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L271) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L441)

<a id="op-765b5239a2c84e"></a>
### Role.disable role

`operation_foundation_core_record_definitions_role_business_behavior_role_disable_role`

**Inputs** self.

**Explicit failure paths** validation helper — Platform.\_(“Standard roles cannot be disabled”).

**Local steps**

- If self.name belongs to STANDARD\_ROLES.
  - Call the validation error handler Platform.throw(Platform.\_(“Standard roles cannot be disabled”)).
- Otherwise.
  - Evaluate self.remove\_roles().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove roles](operations-086.md#op-c946f65d80bff6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6637) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L434)

<a id="op-eeca1069092e45"></a>
### Role.validate homepage

`operation_foundation_core_record_definitions_role_business_behavior_role_validate_homepage`

**Inputs** self.

**Local steps**

- If (Platform.request and self.home\_page).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.request → self.home\_page.
  - Evaluate validate\_path(self.home\_page).
- If self.has\_value\_changed(“home\_page”).
  - Evaluate clear\_routing\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6760) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L272) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L442)

<a id="op-4357a549f41fb0"></a>
### Role.set desk properties

`operation_foundation_core_record_definitions_role_business_behavior_role_set_desk_properties`

**Inputs** self.

**Local steps**

- If self.name equals “Guest”.
  - Set self.desk\_access from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6892) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L439)

<a id="op-c946f65d80bff6"></a>
### Role.remove roles

`operation_foundation_core_record_definitions_role_business_behavior_role_remove_roles`

**Inputs** self.

**State and service calls** request delete on “Has Role”.

**Local steps**

- Evaluate Platform.db.delete(“Has Role”, mapping(“role” → self.name)).
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L6967) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L437)

<a id="op-d375e62417e4de"></a>
### Role.on update

`operation_foundation_core_record_definitions_role_business_behavior_role_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install.
  - Return no value.
- If self.has\_value\_changed(“desk\_access”).
  - Evaluate self.update\_user\_type\_on\_change().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update user type on change](operations-086.md#op-4789cb382d8b2f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0099.json#L7075) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L435)

<a id="op-4789cb382d8b2f"></a>
### Role.update user type on change

`operation_foundation_core_record_definitions_role_business_behavior_role_update_user_type_on_change`

**Inputs** self.

**Record and data access** read “User” via get\_all.

**State and service calls** call save on user.

**Local steps**

- Set users\_with\_role from get\_users(self.name).
- Set role\_user\_type from “System User” when self.desk\_access, otherwise “Website User”.
  - Value choice on self.desk\_access — true gives “System User”, false gives “Website User”.
- Set users\_with\_same\_user\_type from Platform.get\_all(“User”, mapping(“user\_type” → role\_user\_type), pluck = “name”).
- For each user\_name in (set(users\_with\_role) − set(users\_with\_same\_user\_type)).
  - Set user from Platform.get\_lazy\_doc(“User”, user\_name).
  - Set user\_type from user.user\_type.
  - Evaluate user.set\_system\_user().
  - If user\_type differs from user.user\_type.
    - Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L440)

<a id="op-257cda793231bc"></a>
### Role.replicate role

`operation_foundation_core_record_definitions_role_business_behavior_role_replicate_role`

**Inputs** self, cur\_role, new\_role.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read “Role” via get\_value · resolve a document from mapping(“doctype” → “Role”, “role\_name” → new\_role) via get\_doc · resolve a document from mapping(“doctype” → “Custom DocPerm”, expand perm) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Role”, “role\_name” → new\_role)) · call insert on Platform.get\_doc(mapping(“doctype” → “Custom DocPerm”, expand perm)).

**Explicit results** Platform.errprint(formatted text Role {new\_role} already exist.) · new\_role.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If Platform.db.get\_value(“Role”, new\_role, “name”).
  - Return Platform.errprint(formatted text Role {new\_role} already exist.).
- Set new\_role from Platform.get\_doc(mapping(“doctype” → “Role”, “role\_name” → new\_role)).insert().name.
- Set perms from get\_permissions(role = cur\_role).
- For each perm in perms.
  - Evaluate perm.update(mapping(“name” → no value, “creation” → no value, “modified” → no value, “modified\_by” → no value, …)).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Custom DocPerm”, expand perm)).insert().
- Return new\_role.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L334) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L438)

<a id="op-4af35d57482299"></a>
### Get info based on role

`operation_foundation_core_record_definitions_role_business_behavior_get_info_based_on_role`

**Inputs** role, field = “email”, ignore\_permissions = false.

**Record and data access** read “User” via get\_value · read “Has Role” via get\_list.

**Explicit results** list(user) when user, otherwise list() · get\_user\_info(users, field).

**Local steps**

- If role equals “Administrator”.
  - Set user from Platform.db.get\_value(“User”, “Administrator”, field).
  - Return list(user) when user, otherwise list().
    - Value choice on user — true gives list(user), false gives list().
- Set users from Platform.get\_list(“Has Role”, filters = mapping(“role” → role, “parenttype” → “User”), parent\_doctype = “User”, fields = list(“parent as user\_name”), ignore\_permissions = ignore\_permissions).
- Return get\_user\_info(users, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L856) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L429)

<a id="op-76761bb67a09a2"></a>
### Get user info

`operation_foundation_core_record_definitions_role_business_behavior_get_user_info`

**Inputs** users, field = “email”.

**Record and data access** read “User” via get\_value.

**Explicit results** info\_list.

**Local steps**

- Set info\_list from list().
- For each user in users.
  - Set tuple(user\_info, enabled) from Platform.db.get\_value(“User”, user.get(“user\_name”), list(field, “enabled”)).
  - If (enabled and user\_info does not belong to list(“admin@example.com”, “guest@example.com”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in enabled → user\_info does not belong to list(“admin@example.com”, “guest@example.com”).
    - Evaluate info\_list.append(user\_info).
- Return info\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L1152) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L430)

<a id="op-e8b2c76cdc0612"></a>
### Get users

`operation_foundation_core_record_definitions_role_business_behavior_get_users`

**Inputs** role.

**Record and data access** read “Has Role” via get\_all.

**Explicit results** list of d.parent for d drawn from Platform.get\_all(“Has Role”, filters = mapping(“role” → role, “parenttype” → “User”), fields = list(“parent”)).

**Local steps**

- Return list of d.parent for d drawn from Platform.get\_all(“Has Role”, filters = mapping(“role” → role, “parenttype” → “User”), fields = list(“parent”)).
  - Draw d from Platform.get\_all(“Has Role”, filters = mapping(“role” → role, “parenttype” → “User”), fields = list(“parent”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L1388) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L431)

<a id="op-3b93a6c4bcead1"></a>
### Role query

`operation_foundation_core_record_definitions_role_business_behavior_role_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Role” via get\_all.

**Explicit results** Platform.get\_all(“Role”, limit\_start = start, limit\_page\_length = page\_len, filters = list(list(“Role”, “name”, “like”, formatted text %{txt}%), list(“Role”, “is\_custom”, “=”, 0), list(“Role”, “name”, “!=” ….

**Local steps**

- Return Platform.get\_all(“Role”, limit\_start = start, limit\_page\_length = page\_len, filters = list(list(“Role”, “name”, “like”, formatted text %{txt}%), list(“Role”, “is\_custom”, “=”, 0), list(“Role”, “name”, “!=” ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L1540) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L436)

## Record · Role permission for page and report

[Record definition](../../../../data/record-types/role_permission_for_page_and_report.json)

<a id="op-34d0537ee0babe"></a>
### Role Permissionfor Pageand Report.set report page data

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_set_report_page_data`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L3296) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L450)

<a id="op-7e27b909d668cc"></a>
### Role Permissionfor Pageand Report.set custom roles

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_set_custom_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L3385) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L449)

<a id="op-758aeb24557718"></a>
### Role Permissionfor Pageand Report.check prepared report disabled

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_check_prepared_report_disabled`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L3649) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L274) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L444)

<a id="op-cffc01db397773"></a>
### Role Permissionfor Pageand Report.get standard roles

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_get_standard_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L3729) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L277) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L447)

<a id="op-92db2cf70c90a0"></a>
### Role Permissionfor Pageand Report.reset roles

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_reset_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L3874) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L448)

<a id="op-d257f1d9754f32"></a>
### Role Permissionfor Pageand Report.update report page data

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_update_report_page_data`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4022) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L453)

<a id="op-03f8fe40ec018e"></a>
### Role Permissionfor Pageand Report.update custom roles

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_update_custom_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** effective access lookup, record lookup, record mutation request.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4111) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L451)
