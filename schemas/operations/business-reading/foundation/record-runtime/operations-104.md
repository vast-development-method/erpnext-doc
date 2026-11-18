# Record lifecycle and persistence · operations 104

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User type

[Record definition](../../../../data/record-types/user_type.json)

<a id="op-f1578758286a41"></a>
### User Type.validate

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_modules().
- Evaluate self.add\_select\_perm\_doctypes().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set modules](operations-104.md#op-f5a980b972a5db), [add select perm doctypes](operations-104.md#op-b862bcc3070c77).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L1674) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L862)

<a id="op-51bf62bbf659a5"></a>
### User Type.clear cache

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- If not self.is\_standard.
  - Evaluate Platform.cache.delete\_value(“non\_standard\_user\_types”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L1745) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L853)

<a id="op-3d040ba023fac2"></a>
### User Type.on update

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.is\_standard.
  - Return no value.
- Evaluate self.add\_role\_permissions\_for\_user\_doctypes().
- Evaluate self.add\_role\_permissions\_for\_select\_doctypes().
- Evaluate self.add\_role\_permissions\_for\_file().
- Evaluate self.update\_users().
- Evaluate self.remove\_permission\_for\_deleted\_doctypes().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add role permissions for user doctypes](operations-104.md#op-08ac2e7e2ea9e5), [add role permissions for select doctypes](operations-104.md#op-f2c9e816394017), [add role permissions for file](operations-104.md#op-cb73c10b05be67), [update users](operations-104.md#op-280b88b2dfecb1), [remove permission for deleted doctypes](operations-104.md#op-977676ac93d493).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L1846) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L855)

<a id="op-127f879ee48423"></a>
### User Type.on trash

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Standard user type {0} can not be deleted.”.format(Platform.bold(self.name)).

**Local steps**

- If self.is\_standard.
  - Call the validation error handler Platform.throw(translated “Standard user type {0} can not be deleted.”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L1997) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L854)

<a id="op-f5a980b972a5db"></a>
### User Type.set modules

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_set_modules`

**Inputs** self.

**Record and data access** read “DocType” via get\_all.

**Explicit results** no value.

**Local steps**

- If not self.user\_doctypes.
  - Return no value.
- Set modules from Platform.get\_all(“DocType”, filters = mapping(“name” → tuple(“in”, list of d.document\_type for d drawn from self.user\_doctypes)), distinct = true, pluck = “module”).
  - Draw d from self.user\_doctypes.
- Evaluate self.set(“user\_type\_modules”, list()).
- For each module in modules.
  - Evaluate self.append(“user\_type\_modules”, mapping(“module” → module)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L2122) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L858)

<a id="op-280b88b2dfecb1"></a>
### User Type.update users

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_update_users`

**Inputs** self.

**Record and data access** read “User” via get\_all · resolve a document from “User” via get\_cached\_doc.

**Local steps**

- For each row in Platform.get\_all(“User”, filters = mapping(“user\_type” → self.name)).
  - Set user from Platform.get\_cached\_doc(“User”, row.name).
  - Evaluate self.update\_roles\_in\_user(user).
  - Evaluate self.update\_modules\_in\_user(user).
  - Evaluate user.update\_children().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update roles in user](operations-104.md#op-7cb66c274a5dc8), [update modules in user](operations-104.md#op-bdf10782bd161d).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“User”, row.name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L2395) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L861)

<a id="op-7cb66c274a5dc8"></a>
### User Type.update roles in user

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_update_roles_in_user`

**Inputs** self, user.

**Local steps**

- Evaluate user.set(“roles”, list()).
- Evaluate user.append(“roles”, mapping(“role” → self.role)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L2610) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L860)

<a id="op-bdf10782bd161d"></a>
### User Type.update modules in user

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_update_modules_in_user`

**Inputs** self, user.

**Record and data access** read “Module Def” via get\_all.

**Local steps**

- Set block\_modules from Platform.get\_all(“Module Def”, fields = list(“name as module”), filters = mapping(“name” → list(“not in”, list of d.module for d drawn from self.user\_type\_modules))).
  - Draw d from self.user\_type\_modules.
- If block\_modules.
  - Evaluate user.set(“block\_modules”, block\_modules).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L2733) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L859)

<a id="op-08ac2e7e2ea9e5"></a>
### User Type.add role permissions for user doctypes

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_add_role_permissions_for_user_record_types`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L2926) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L851)

<a id="op-b862bcc3070c77"></a>
### User Type.add select perm doctypes

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_add_select_permission_record_types`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.flags.ignore\_select\_perm.
  - Return no value.
- Set self.select\_doctypes from list().
- Set select\_doctypes from list().
- Set user\_doctypes from list of row.document\_type for row drawn from self.user\_doctypes.
  - Draw row from self.user\_doctypes.
- For each doctype in user\_doctypes.
  - Set doc from Platform.get\_meta(doctype).
  - Evaluate self.prepare\_select\_perm\_doctypes(doc, user\_doctypes, select\_doctypes).
  - For each child\_table in doc.get\_table\_fields().
    - Set child\_doc from Platform.get\_meta(child\_table.options).
    - If child\_doc.
      - Evaluate self.prepare\_select\_perm\_doctypes(child\_doc, user\_doctypes, select\_doctypes).
- If select\_doctypes.
  - Set select\_doctypes from set(select\_doctypes).
  - For each select\_doctype in select\_doctypes.
    - Evaluate self.append(“select\_doctypes”, mapping(“document\_type” → select\_doctype)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare select perm doctypes](operations-104.md#op-a457107eb0dd02).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L3206) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L852)

<a id="op-a457107eb0dd02"></a>
### User Type.prepare select perm doctypes

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_prepare_select_permission_record_types`

**Inputs** self, doc, user\_doctypes, select\_doctypes.

**Local steps**

- For each field in doc.get\_link\_fields().
  - If field.options does not belong to user\_doctypes.
    - Evaluate select\_doctypes.append(field.options).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L3607) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L856)

<a id="op-f2c9e816394017"></a>
### User Type.add role permissions for select doctypes

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_add_role_permissions_for_select_record_types`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L3738) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L850)

<a id="op-cb73c10b05be67"></a>
### User Type.add role permissions for file

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_add_role_permissions_for_file`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L3964) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L849)

<a id="op-977676ac93d493"></a>
### User Type.remove permission for deleted doctypes

`operation_foundation_core_record_definitions_user_type_business_behavior_user_type_remove_permission_for_deleted_record_types`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L4109) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L857)

<a id="op-b640ea97600cfa"></a>
### Add role permissions

`operation_foundation_core_record_definitions_user_type_business_behavior_add_role_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, role.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L4437) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L843)

<a id="op-bec8002eca8796"></a>
### Get non standard user types

`operation_foundation_core_record_definitions_user_type_business_behavior_get_non_standard_user_types`

**Inputs** no declared parameters.

**Record and data access** read “User Type” via get\_all.

**Explicit results** mapping of d.name → list(d.apply\_user\_permission\_on, d.user\_id\_field) for d drawn from user\_types.

**Local steps**

- Set user\_types from Platform.get\_all(“User Type”, fields = list(“apply\_user\_permission\_on”, “name”, “user\_id\_field”), filters = mapping(“is\_standard” → 0)).
- Return mapping of d.name → list(d.apply\_user\_permission\_on, d.user\_id\_field) for d drawn from user\_types.
  - Draw d from user\_types.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L4607) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L845)

<a id="op-259c2216566201"></a>
### Get user linked doctypes

`operation_foundation_core_record_definitions_user_type_business_behavior_get_user_linked_record_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “DocType” via get\_all · read “Custom Field” via get\_all.

**Explicit results** (doctypes + custom\_doctypes).

**Local steps**

- Set modules from list of d.get(“module\_name”) for d drawn from get\_modules\_from\_app(“Platform”).
  - Draw d from get\_modules\_from\_app(“Platform”).
- Set filters from list(list(“DocField”, “options”, “=”, “User”), list(“DocType”, “is\_submittable”, “=”, 0), list(“DocType”, “issingle”, “=”, 0), list(“DocType”, “module”, “not in”, modules), …).
- Set doctypes from Platform.get\_all(“DocType”, fields = list(“′tabDocType′.′name′”), filters = filters, order\_by = “idx desc”, limit\_start = start, …).
- Set custom\_dt\_filters from list(list(“Custom Field”, “dt”, “like”, formatted text %{txt}%), list(“Custom Field”, “options”, “=”, “User”), list(“Custom Field”, “fieldtype”, “=”, “Link”)).
- Set custom\_doctypes from Platform.get\_all(“Custom Field”, fields = list(“dt as name”), filters = custom\_dt\_filters, as\_list = 1).
- Return (doctypes + custom\_doctypes).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L4782) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L847)

<a id="op-767aefebb35ad6"></a>
### Get user id

`operation_foundation_core_record_definitions_user_type_business_behavior_get_user_identifier`

**Inputs** parent.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** data.

**Local steps**

- Set data from (Platform.get\_all(“DocField”, fields = list(“label”, “fieldname as value”), filters = mapping(“options” → “User”, “fieldtype” → “Link”, “parent” → parent)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“DocField”, fields = list(“label”, “fieldname as value”), filters = mapping(“options” → “User”, “fieldtype” → “Link”, “parent” → parent)) → list().
- Evaluate data.extend(Platform.get\_all(“Custom Field”, fields = list(“label”, “fieldname as value”), filters = mapping(“options” → “User”, “fieldtype” → “Link”, “dt” → parent))).
- Return data.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L5527) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L846)

<a id="op-050ecd6a7f1c5d"></a>
### User linked with permission on doctype

`operation_foundation_core_record_definitions_user_type_business_behavior_user_linked_with_permission_on_record_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0117.json#L5854) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L848)

<a id="op-63c6c18187ee8e"></a>
### Apply permissions for non standard user type

`operation_foundation_core_record_definitions_user_type_business_behavior_apply_permissions_for_non_standard_user_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 6 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L844)

<a id="op-f5b1a1f0a6e774"></a>
### Get data

`operation_foundation_core_record_definitions_user_type_user_type_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “user\_type”, “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“User”)))).

**Local steps**

- Return mapping(“fieldname” → “user\_type”, “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“User”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L1002) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L869)

## Service · Utils

<a id="op-234794b28cd73d"></a>
### Get parent doc

`operation_foundation_core_utils_business_behavior_get_parent_record`

**Inputs** doc.

**Record and data access** resolve a document from doc.reference\_doctype via get\_doc.

**Explicit results** doc.parent\_doc.

**Local steps**

- If not getattr(doc, “parent\_doc”, no value).
  - If (doc.reference\_doctype and doc.reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
    - Set doc.parent\_doc from Platform.get\_doc(doc.reference\_doctype, doc.reference\_name).
  - Otherwise.
    - Set doc.parent\_doc from no value.
- Return doc.parent\_doc.

**Values supplied outside this operation** selected callable from getattr(doc, “parent\_doc”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L6427) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L919)

<a id="op-16ddf0d180874f"></a>
### Set timeline doc

`operation_foundation_core_utils_business_behavior_set_timeline_record`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- Set parent\_doc from get\_parent\_doc(doc).
- If ((doc.timeline\_doctype and doc.timeline\_name) or not parent\_doc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (doc.timeline\_doctype and doc.timeline\_name) → not parent\_doc.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.timeline\_doctype → doc.timeline\_name.
  - Return no value.
- Set timeline\_field from parent\_doc.meta.timeline\_field.
- If not timeline\_field.
  - Return no value.
- Set doctype from parent\_doc.meta.get\_link\_doctype(timeline\_field).
- Set name from parent\_doc.get(timeline\_field).
- If (doctype and name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.
  - Set doc.timeline\_doctype from doctype.
  - Set doc.timeline\_name from name.
- Otherwise.
  - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L6592) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L921)

<a id="op-0e731ddc12bdd5"></a>
### Find

`operation_foundation_core_utils_business_behavior_find`

**Inputs** list\_of\_dict, match\_function.

**Explicit results** entry · no value.

**Local steps**

- For each entry in list\_of\_dict.
  - If match\_function(entry).
    - Return entry.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L6863) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L917)
