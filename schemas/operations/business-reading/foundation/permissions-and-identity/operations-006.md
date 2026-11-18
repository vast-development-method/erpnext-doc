# Identity and access · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Permissions

<a id="op-d71faf9b2b47f7"></a>
### Get perms for

`operation_foundation_permissions_business_behavior_get_perms_for`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** roles, perm\_doctype, filters.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L5040) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1693)

<a id="op-69c6f064d134b3"></a>
### Get doctypes with custom docperms

`operation_foundation_permissions_business_behavior_get_record_types_with_custom_docperms`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L5248) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1698)

<a id="op-60245eaea6cba6"></a>
### Add user permission

`operation_foundation_permissions_business_behavior_add_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, user, ignore\_permissions, applicable\_for, is\_default, hide\_descendants.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L5365) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1679)

<a id="op-b5f1064c0afe06"></a>
### Remove user permission

`operation_foundation_permissions_business_behavior_remove_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, user, ignore\_permissions.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L5746) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1721)

<a id="op-d684dc9ea0a6d0"></a>
### Clear user permissions for doctype

`operation_foundation_permissions_business_behavior_clear_user_permissions_for_record_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, user.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L5930) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1685)

<a id="op-62ba713012ba8f"></a>
### Can import

`operation_foundation_permissions_business_behavior_can_import`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, raise\_exception.

**Explicit result forms** Boolean false, Boolean true.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L6143) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1682)

<a id="op-92a0d3515b7618"></a>
### Can export

`operation_foundation_permissions_business_behavior_can_export`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, raise\_exception, is\_owner.

**Explicit result forms** Boolean true, a value selected from the current context.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L6325) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1681)

<a id="op-9596dfe2df88ca"></a>
### Update permission property

`operation_foundation_permissions_business_behavior_update_permission_property`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, role, permlevel, ptype, value, validate, if\_owner.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L6637) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1724)

<a id="op-738c731adb5f3b"></a>
### Setup custom perms

`operation_foundation_permissions_business_behavior_setup_custom_perms`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** parent.

**Explicit result forms** Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L6927) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1723)

<a id="op-677232baca41f4"></a>
### Add permission

`operation_foundation_permissions_business_behavior_add_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, role, permlevel, ptype.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** record lookup, record mutation request, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1678)

<a id="op-4ddf95eeb28573"></a>
### Copy perms

`operation_foundation_permissions_business_behavior_copy_perms`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** parent.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L494) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1686)

<a id="op-be73b56cc8c488"></a>
### Reset perms

`operation_foundation_permissions_business_behavior_reset_perms`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L682) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1722)

<a id="op-f3a1ccea21eaef"></a>
### Get linked doctypes

`operation_foundation_permissions_business_behavior_get_linked_record_types`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** dt.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L870) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1691)

<a id="op-b6c65249d910bb"></a>
### Get doc name

`operation_foundation_permissions_business_behavior_get_record_name`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1108) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1694)

<a id="op-f511c3594faa92"></a>
### Get rights

`operation_foundation_permissions_business_behavior_get_rights`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1211) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1700)

<a id="op-afa0854ae5f3c9"></a>
### Allow everything

`operation_foundation_permissions_business_behavior_allow_everything`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1336) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1680)

<a id="op-003213012fd9e6"></a>
### Get allowed docs for doctype

`operation_foundation_permissions_business_behavior_get_allowed_records_for_record_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user\_permissions, doctype.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1413) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1690)

<a id="op-c4ebf48e213e25"></a>
### Filter allowed docs for doctype

`operation_foundation_permissions_business_behavior_filter_allowed_records_for_record_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user\_permissions, doctype, with\_default\_doc.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1487) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1688)

<a id="op-f3d9fb4f925286"></a>
### Push perm check log

`operation_foundation_permissions_business_behavior_push_permission_check_log`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** log, debug.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1820) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1720)

<a id="op-d64c895a67067f"></a>
### Has child permission

`operation_foundation_permissions_business_behavior_has_child_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** child\_doctype, ptype, child\_doc, user, parent\_doctype, debug, print\_logs.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 11 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L1983) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1710)

<a id="op-68eedf67e04906"></a>
### Is system user

`operation_foundation_permissions_business_behavior_is_system_user`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a comparison result.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L3309) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1716)

<a id="op-6e3ae1617cdf76"></a>
### Check doctype permission

`operation_foundation_permissions_business_behavior_check_record_type_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, ptype.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L3429) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1684)

<a id="op-af2f2a240802c0"></a>
### Handle does not exist error

`operation_foundation_permissions_business_behavior_handle_does_not_exist_error`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** fn.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L3651) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1708)

<a id="op-659234ce910696"></a>
### Handle does not exist error.wrapper

`operation_foundation_permissions_business_behavior_handle_does_not_exist_error_wrapper`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** e, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L3923) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1709)
