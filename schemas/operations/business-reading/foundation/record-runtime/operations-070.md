# Record lifecycle and persistence · operations 70

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Permission log

[Record definition](../../../../data/record-types/permission_log.json)

<a id="op-f0ab6f67ed18c4"></a>
### Make perm log

`operation_foundation_core_record_definitions_permission_log_business_behavior_make_permission_log`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L91) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L24)

<a id="op-d96fddd65f2b66"></a>
### Insert perm log

`operation_foundation_core_record_definitions_permission_log_business_behavior_insert_permission_log`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, doc\_before\_save, for\_doctype, for\_document, fields.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L90) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L23)

<a id="op-3c14bf62459003"></a>
### Get changes

`operation_foundation_core_record_definitions_permission_log_business_behavior_get_changes`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, doc\_before\_save, fields.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L3691) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L19)

<a id="op-7e783a270bc945"></a>
### Get changes diff

`operation_foundation_core_record_definitions_permission_log_business_behavior_get_changes_diff`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** current\_changes, previous\_changes.

**Explicit result forms** a structured result.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L4003) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L20)

<a id="op-2c8cb9694a2f4a"></a>
### Get filtered changes

`operation_foundation_core_record_definitions_permission_log_business_behavior_get_filtered_changes`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** changes, filters.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L4520) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L21)

<a id="op-a44f431178ce89"></a>
### Get filtered changes.filter child docs

`operation_foundation_core_record_definitions_permission_log_business_behavior_get_filtered_changes_filter_child_records`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** child\_docs, filter\_keys.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L4913) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L22)

## Workspace · Permission manager

<a id="op-b4071779eaff66"></a>
### Get roles and doctypes

`operation_foundation_core_page_permission_manager_business_behavior_get_roles_and_record_types`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L4168) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L918)

<a id="op-b523e7749df9f7"></a>
### Get permissions

`operation_foundation_core_page_permission_manager_business_behavior_get_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, role.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 6 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L5427) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L917)

<a id="op-a80af47cc75f41"></a>
### Add

`operation_foundation_core_page_permission_manager_business_behavior_add`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** parent, role, permlevel.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L6215) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L916)

<a id="op-8ba01f82a1775f"></a>
### Update

`operation_foundation_core_page_permission_manager_business_behavior_update`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, role, permlevel, ptype, value, if\_owner.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L159) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L923)

<a id="op-ff3ede8174a972"></a>
### Update.clear cache

`operation_foundation_core_page_permission_manager_business_behavior_update_clear_cache`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L6897) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L924)

<a id="op-1baaa7c7b6640c"></a>
### Remove

`operation_foundation_core_page_permission_manager_business_behavior_remove`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, role, permlevel, if\_owner.

**Observed service boundaries** effective access lookup, record lookup, record mutation request, validation or user-notification service.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L921)

<a id="op-83dfd0e111b70e"></a>
### Reset

`operation_foundation_core_page_permission_manager_business_behavior_reset`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L158) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L922)

<a id="op-e2043efd86b6e3"></a>
### Get users with role

`operation_foundation_core_page_permission_manager_business_behavior_get_users_with_role`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** role.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L1053) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L920)

<a id="op-fb730ba1fc20d4"></a>
### Get standard permissions

`operation_foundation_core_page_permission_manager_business_behavior_get_standard_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a structured result, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L1150) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L919)

## Record · Permission type

[Record definition](../../../../data/record-types/permission_type.json)

<a id="op-b01b162de25610"></a>
### Permission Type.autoname

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_autoname`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5064) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L27)

<a id="op-096381c2cb8f96"></a>
### Permission Type.before insert

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_before_insert`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5186) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L29)

<a id="op-64a8b6786a6219"></a>
### Permission Type.validate

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_validate`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5260) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L38)

<a id="op-6ab4c44451ae63"></a>
### Permission Type.can write

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_can_write`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5391) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L30)

<a id="op-fd212554f35628"></a>
### Permission Type.should export

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_should_export`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5478) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L37)

<a id="op-2303c7163fafc6"></a>
### Permission Type.get folder path

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_get_folder_path`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5577) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L34)

<a id="op-23eb2a22abe196"></a>
### Permission Type.on update

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_on_update`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5688) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L36)

<a id="op-9071fc032eff4a"></a>
### Permission Type.before export

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_before_export`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, export\_doc.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L5990) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L28)

<a id="op-3f8cf19da921fd"></a>
### Permission Type.create custom field

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_create_custom_field`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, target.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L6150) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L31)
