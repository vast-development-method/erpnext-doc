# Identity and access · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Oauth

<a id="op-86220fe11101de"></a>
### Generate json error response

`operation_foundation_delegated_authorization_business_behavior_generate_structured_data_error_response`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** e.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L6742) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1570)

<a id="op-a0ddfa0a549927"></a>
### Get server url

`operation_foundation_delegated_authorization_business_behavior_get_server_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L7017) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1573)

## Service · Permissions

<a id="op-cbc644612cd649"></a>
### Print has permission check logs

`operation_foundation_permissions_business_behavior_print_has_permission_check_logs`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** func.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1718)

<a id="op-ac3108b013221a"></a>
### Print has permission check logs.inner

`operation_foundation_permissions_business_behavior_print_has_permission_check_logs_inner`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** args, kwargs.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** validation or user-notification service.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L427) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1719)

<a id="op-a73008071ac849"></a>
### Debug log

`operation_foundation_permissions_business_behavior_debug_log`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** log.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L824) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1687)

<a id="op-23374fb0faa22f"></a>
### Pop debug log

`operation_foundation_permissions_business_behavior_post_office_protocol_debug_log`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L946) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1717)

<a id="op-3a83f3b349dea8"></a>
### Has permission

`operation_foundation_permissions_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, ptype, doc, user, parent\_doctype, print\_logs, debug, ignore\_share\_permissions.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 17 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L39) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1712)

<a id="op-ce8ac665a7dfeb"></a>
### Has permission.false if not shared

`operation_foundation_permissions_business_behavior_has_permission_false_if_not_shared`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L3496) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1713)

<a id="op-b960934fad3b46"></a>
### Get doc permissions

`operation_foundation_permissions_business_behavior_get_record_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user, ptype, debug.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 7 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L4112) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1695)

<a id="op-b48c5089931bf0"></a>
### Get doc permissions.is user owner

`operation_foundation_permissions_business_behavior_get_record_permissions_is_user_owner`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L5106) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1696)

<a id="op-62c67b45aceb86"></a>
### Get role permissions

`operation_foundation_permissions_business_behavior_get_role_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype\_meta, user, is\_owner, debug.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 6 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L5201) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1701)

<a id="op-f225cee25be8dc"></a>
### Get role permissions.is perm applicable

`operation_foundation_permissions_business_behavior_get_role_permissions_is_permission_applicable`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** perm.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L6680) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1703)

<a id="op-2a3fa9f6a42b2e"></a>
### Get role permissions.has permission without if owner enabled

`operation_foundation_permissions_business_behavior_get_role_permissions_has_permission_without_if_owner_enabled`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** ptype.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L6776) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1702)

<a id="op-77b7dd95c60756"></a>
### Get user permissions

`operation_foundation_permissions_business_behavior_get_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0310.json#L6344) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1706)

<a id="op-c966545bdb9273"></a>
### Has user permission

`operation_foundation_permissions_business_behavior_has_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user, debug, ptype.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 12 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L40) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1714)

<a id="op-d69c5c5c070436"></a>
### Has user permission.check user permission on link fields

`operation_foundation_permissions_business_behavior_has_user_permission_check_user_permission_on_link_fields`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 7 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L1944) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1715)

<a id="op-e66300234fd119"></a>
### Has controller permissions

`operation_foundation_permissions_business_behavior_has_controller_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, debug.

**Explicit result forms** Boolean true, the result of a delegated call.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L2707) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1711)

<a id="op-85881a9226a2bd"></a>
### Get doctypes with read

`operation_foundation_permissions_business_behavior_get_record_types_with_read`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L3092) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1699)

<a id="op-b1585b5ca1e083"></a>
### Get cached doctypes with read

`operation_foundation_binding_foundation_permissions_get_cached_doctypes_with_read`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L217) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1649)

<a id="op-4f115b2848edef"></a>
### Get valid perms

`operation_foundation_permissions_business_behavior_get_valid_perms`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, user, roles.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L3242) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1707)

<a id="op-b82f78a8c0355f"></a>
### Get all perms

`operation_foundation_permissions_business_behavior_get_all_perms`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** role.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L3637) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1689)

<a id="op-6500cf88b1a8fb"></a>
### Get roles

`operation_foundation_permissions_business_behavior_get_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, with\_standard.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L3936) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1704)

<a id="op-321e442c9caa72"></a>
### Get roles.get

`operation_foundation_permissions_business_behavior_get_roles_get`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L4529) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1705)

<a id="op-76a2f5dcf5f13d"></a>
### Get doctype roles

`operation_foundation_permissions_business_behavior_get_record_type_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, access\_type.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0311.json#L4893) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1697)
